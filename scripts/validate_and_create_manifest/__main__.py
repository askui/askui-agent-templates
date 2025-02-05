from dataclasses import asdict
import os
import re
import json
import yaml
import logging
import jsonschema
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional, Tuple, TypedDict
from pathlib import Path
from pathspec import PathSpec
from pathspec.patterns import GitWildMatchPattern
import subprocess

from .models.exceptions import ValidationErrorType
from .models.exceptions import ValidationError
from .models.exceptions import ValidationErrors
from .models.manifest import TemplateInfo
from .models.manifest import TemplateManifest

# Constants
MAX_MANIFEST_SIZE_BYTES = 1_000_000  # 1MB
MAX_S3_KEY_LENGTH = 1_024
S3_PATH_PREFIX = "agent/templates/"
MAX_PATH_LENGTH = MAX_S3_KEY_LENGTH - len(S3_PATH_PREFIX)
PATH_SEGMENT_PATTERN = r"^[a-zA-Z0-9-_.]{0,64}$"
GITHUB_REPO_URL = "https://github.com/askui/askui-agent-templates"
IGNORE_FILES = {".gitignore"}
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class FilePathError(TypedDict, total=False):
    error: str
    message: str
    segment: str


def get_last_modified_iso(directory: str) -> str:
    latest = max(
        os.path.getmtime(os.path.join(root, file))
        for root, _, files in os.walk(directory)
        for file in files
    )
    return datetime.fromtimestamp(latest, tz=timezone.utc).isoformat()


def validate_path_segment(segment: str) -> Optional[str]:
    if not re.match(PATH_SEGMENT_PATTERN, segment):
        return f"Invalid path segment: {segment}. Path segment must match {PATH_SEGMENT_PATTERN}."
    return None


def validate_path(path: str) -> list[FilePathError]:
    """Validate complete S3 path against AWS restrictions."""
    path_str = str(path)
    errors: list[FilePathError] = []

    # Check total path length
    if len(path_str) > MAX_PATH_LENGTH:
        errors.append(
            FilePathError(
                error="path_too_long",
                message=f"Path exceeds {MAX_PATH_LENGTH} characters",
            )
        )

    # Validate each path component
    for segment in Path(path_str).parts:
        if error := validate_path_segment(segment):
            errors.append(
                FilePathError(
                    error="invalid_file_path",
                    message=error,
                    segment=segment,
                )
            )

    return errors


def get_path_spec(template_dir: str) -> PathSpec:
    """Create PathSpec from ignore files in template directory."""
    patterns = []
    for ignore_file in IGNORE_FILES:
        ignore_path = Path(template_dir) / ignore_file
        if ignore_path.exists():
            patterns.extend(ignore_path.read_text().splitlines())
    return PathSpec.from_lines(GitWildMatchPattern, patterns)


def validate_template_paths(
    template_dir: str, path_spec: PathSpec
) -> List[ValidationError]:
    errors: List[ValidationError] = []

    for root, _, files in os.walk(template_dir):
        if path_spec.match_file(root):
            continue
        for file in files:
            file_path = os.path.join(root, file)
            if path_spec.match_file(file_path):
                continue
            relative_path = os.path.relpath(file_path)
            if _errors := validate_path(relative_path):
                errors.extend(
                    ValidationError(
                        ValidationErrorType.INVALID_FILE_PATH,
                        f"Invalid path '{relative_path}': {error['message']}",
                        dict(error),
                        relative_path,
                    )
                    for error in _errors
                )
    return errors


def load_and_validate_agent_config(
    agent_yml_path: str, schema: Dict[str, Any]
) -> Tuple[Optional[Dict[str, Any]], Optional[ValidationError]]:
    try:
        with open(agent_yml_path, "r") as f:
            agent_config = yaml.safe_load(f)
            jsonschema.validate(agent_config, schema)
            return agent_config, None
    except yaml.YAMLError as e:
        return None, ValidationError(
            ValidationErrorType.INVALID_YAML,
            f"Invalid YAML in {agent_yml_path}",
            {"error": str(e)},
            agent_yml_path,
        )
    except jsonschema.exceptions.ValidationError as e:
        return None, ValidationError(
            ValidationErrorType.SCHEMA_VIOLATION,
            f"Schema validation failed for {agent_yml_path}",
            {"error": str(e)},
            agent_yml_path,
        )


def get_git_sha() -> str:
    """Get current git SHA."""
    try:
        return (
            subprocess.check_output(
                ["git", "rev-parse", "HEAD"], stderr=subprocess.PIPE
            )
            .decode("utf-8")
            .strip()
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            f"Failed to get git SHA. Are you in a git repository? Error: {e.stderr.decode('utf-8')}"
        ) from e


def create_template_info(
    template_dir: str, agent_config: Dict[str, Any]
) -> TemplateInfo:
    return TemplateInfo(
        id=template_dir,
        url=f"{GITHUB_REPO_URL}/blob/{get_git_sha()}/{template_dir}/agent.yml",
        last_modified=get_last_modified_iso(template_dir),
        name=agent_config["template"]["name"],
        description=agent_config["template"]["description"],
    )


def validate_entrypoint_exists(
    template_dir: str, entrypoint: str
) -> ValidationError | None:
    entrypoint_path = os.path.join(template_dir, entrypoint)
    if not os.path.exists(entrypoint_path):
        return ValidationError(
            ValidationErrorType.MISSING_FILE,
            f"Entrypoint {entrypoint_path} does not exist",
            {"entrypoint": entrypoint_path},
            template_dir,
        )

    return None


def validate_template_directory(
    template_dir: str, schema: Dict[str, Any], path_spec: PathSpec
) -> Tuple[Optional[TemplateInfo], List[ValidationError]]:
    logger.info(f"Validating template directory: {template_dir}")
    errors: List[ValidationError] = []
    errors.extend(validate_template_paths(template_dir, path_spec))
    if errors:
        return None, errors

    agent_yml_path = os.path.join(template_dir, "agent.yml")
    agent_config, error = load_and_validate_agent_config(agent_yml_path, schema)
    if error or not agent_config:
        if error:
            errors.append(error)
        return None, errors

    if entrypoint_error := validate_entrypoint_exists(
        template_dir, agent_config["entrypoint"]
    ):
        errors.append(entrypoint_error)
        return None, errors

    logger.info(f"Template directory {template_dir} is valid")
    template_info = create_template_info(template_dir, agent_config)
    logger.debug(f"Template info: {template_info}")
    return template_info, []


def get_manifest_size(manifest: TemplateManifest) -> int:
    return len(json.dumps(asdict(manifest)).encode("utf-8"))


def main() -> None:
    logger.info("Starting template validation")
    validation_errors = ValidationErrors()
    try:
        with open("agent-schema.yml", "r") as f:
            schema = yaml.safe_load(f)
    except Exception as e:
        raise RuntimeError(
            f"Failed to load agent-schema.yml: {e}. Are you sure you are running this script from the root of the agent-templates repository?"
        ) from e

    path_spec = get_path_spec(".")  # Create PathSpec once at root level
    manifest = TemplateManifest(agent_templates=[])

    for item in os.listdir("."):
        if not os.path.isdir(item):
            logger.debug(f"Skipping {item}: not a directory")
            continue

        if item.startswith("."):
            logger.debug(f"Skipping {item}: starts with .")
            continue

        agent_yml_path = os.path.join(item, "agent.yml")
        if not os.path.exists(agent_yml_path):
            logger.debug(f"Skipping {item}: no agent.yml found")
            continue

        template_info, errors = validate_template_directory(item, schema, path_spec)
        validation_errors.extend(errors)
        if template_info:
            manifest.agent_templates.append(template_info)

    # Validate manifest size
    manifest_size = get_manifest_size(manifest)
    if manifest_size > MAX_MANIFEST_SIZE_BYTES:
        validation_errors.add(
            ValidationError(
                ValidationErrorType.MANIFEST_FILE_SIZE_EXCEEDED,
                f"Manifest file size ({manifest_size} bytes) exceeds maximum size of {MAX_MANIFEST_SIZE_BYTES} bytes",
            )
        )

    if validation_errors.has_errors():
        raise ValueError(validation_errors.get_formatted_errors())

    logger.info("Validation successful!")

    logger.info("Creating manifest.yml")
    with open("manifest.yml", "w") as f:
        yaml.dump(asdict(manifest), f)

    logger.info("Manifest created")


if __name__ == "__main__":
    main()
