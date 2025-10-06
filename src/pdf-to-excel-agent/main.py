from pathlib import Path
from fastmcp import Client
from fastmcp.mcp_config import MCPConfig

from askui import VisionAgent
from askui.models.shared.tools import ToolCollection
from askui.tools.mcp.config import StdioMCPServer

from helpers.tools import AskUIGetFromFileTool, PrintTool


def main():
    # --- Paths ---
    base_dir = Path(__file__).parent.resolve()
    source_dir = base_dir / "source_files"

    pdf_source = "demo_data.pdf"
    excel_template_file = "demo_template.xlsx"
    target_file = "target.xlsx"

    # --- MCP Server for Excel ---
    excel_mcp_server = MCPConfig(
        mcpServers={
            "excel_mcp_server": StdioMCPServer(
                command="excel-mcp-server",
                args=[
                    "stdio",
                    "--excel-files-path",
                    str(source_dir),
                ],
            )
        }
    )
    client = Client(excel_mcp_server)
    custom_tools = ToolCollection(mcp_client=client)

    # --- Add custom tools ---
    custom_tools.append_tool(
        AskUIGetFromFileTool(str(source_dir)),
        PrintTool(),
    )

    # --- Run VisionAgent task ---
    with VisionAgent() as desktop_agent:
        desktop_agent.act(
            f"""
            Read "{pdf_source}" and "{excel_template_file}".
            Create a new Excel file at "{target_file}" that follows the template and has the data from the PDF.
            Keep me updated on the progress of the task using the print_tool.
            """,
            tools=custom_tools,
        )


if __name__ == "__main__":
    main()
