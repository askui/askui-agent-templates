from dataclasses import dataclass


@dataclass
class TemplateInfo:
    id: str
    url: str
    last_modified: str
    name: str
    description: str | None = None


@dataclass
class TemplateManifest:
    agent_templates: list[TemplateInfo]
