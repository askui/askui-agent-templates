from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional


class ValidationErrorType(Enum):
    INVALID_FILE_PATH = "invalid_file_path"
    INVALID_YAML = "invalid_yaml"
    MISSING_FILE = "missing_file"
    MANIFEST_FILE_SIZE_EXCEEDED = "manifest_file_size_exceeded"
    SCHEMA_VIOLATION = "schema_violation"


@dataclass
class ValidationError:
    error_type: ValidationErrorType
    message: str
    details: Optional[Dict[str, Any]] = None
    path: Optional[str] = None


class ValidationErrors:
    def __init__(self) -> None:
        self.errors: list[ValidationError] = []

    def add(self, error: ValidationError) -> None:
        self.errors.append(error)

    def extend(self, errors: list[ValidationError]) -> None:
        for error in errors:
            self.add(error)

    def has_errors(self) -> bool:
        return len(self.errors) > 0

    def get_formatted_errors(self) -> str:
        error_groups: Dict[ValidationErrorType, list[str]] = {}
        for error in self.errors:
            message = f"- {error.message}"
            if error.details:
                details_str = " ".join(f"{k}={v}" for k, v in error.details.items())
                message += f" ({details_str})"
            if error.error_type not in error_groups:
                error_groups[error.error_type] = []
            error_groups[error.error_type].append(message)

        formatted = ["Validation failed with the following errors:"]
        for error_type, messages in error_groups.items():
            formatted.append(f"\n{error_type.value.upper()}:")
            formatted.extend(messages)
        return "\n".join(formatted)
