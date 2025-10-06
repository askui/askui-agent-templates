import os

from askui import VisionAgent
from askui.models.shared.tools import Tool

class AskUIGetFromFileTool(Tool):
    """
    A tool that can be used to get information from a file based on the provided query.
    """

    def __init__(self, absolute_source_file_parent_directory_name):
        super().__init__(
            name="askui_get_from_file_tool",
            description="It reads and extracts information from a PDF or office document file based on the provided query",
            input_schema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The query describing what information to retrieve from the file.",
                    },
                    "file_path": {
                        "type": "string",
                        "description": "The name of the file to read and extract information from. It must end with .pdf, .docx, or .doc.",
                    },
                },
                "required": ["query", "file_path"],
            },
        )
        self._absolute_source_file_parent_directory_name = (
            absolute_source_file_parent_directory_name
        )

    def __call__(self, query: str, file_path: str) -> str:
        absolute_file_path = os.path.join(
            self._absolute_source_file_parent_directory_name, file_path
        )
        if not os.path.exists(absolute_file_path):
            return f"File not found. At {absolute_file_path}."
        if not absolute_file_path.endswith((".pdf", ".docx", ".doc")):
            return "Only files with .pdf, .docx, or .doc extensions are supported."
        return VisionAgent().get(query, source=absolute_file_path, response_schema=str)


class PrintTool(Tool):
    """
    A tool that can be used to print a message to the console.
    """

    def __init__(self):
        super().__init__(
            name="print_tool",
            description="A tool that can be used to print a message to the console. It's useful to keep the user updated on the progress of the task.",
            input_schema={
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "The message to print to the console.",
                    },
                },
                "required": ["message"],
            },
        )

    def __call__(self, message: str) -> str:
        print(f"[Message from the Agent] {message}")
        return "Message printed to the console."
