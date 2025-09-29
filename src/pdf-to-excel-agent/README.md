# PDF → Excel Agent (AskUI + MCP)

This demo shows how to build a modular AskUI agent that extracts data from a PDF and writes it into an Excel file that follows a given template. It highlights how AskUI agents can plug in Model Context Protocol (MCP) tools to extend capabilities—in this case, an Excel MCP server.

## Why this matters

- **Modularity**: AskUI agents are tool-agnostic. You can plug in different MCP tools without changing core logic.  
- **MCP Support**: This repo uses an **Excel MCP server** to read/write spreadsheets as tools available to the agent.  
- **Deterministic I/O**: The scripted demo constrains file access to a single directory for safety and reproducibility.  

## What the demo does

- Reads a PDF to extract data  
- Reads an Excel template  
- Writes a new Excel file that follows the template and fills it with the extracted data  

All demo files are under `source_files`, which is the only location the demo script reads and writes to by design.  

## Project structure

```bash
src/pdf-to-excel-agent/
  main.py                 # Demo script wiring AskUI agent + MCP tools
  helpers/tools.py        # Custom AskUI tools (e.g., PDF file reader)
  source_files/
    demo_data.pdf         # Input PDF
    demo_template.xlsx    # Excel template
    target.xlsx           # Output written by the agent
  requirements.txt        # AskUI + Excel MCP server dependency
  chat/
    assistants/
      asst_68d3d3073045083a7047d6da.json # Custom assistant called PDF to Excel Agent
    mcp_configs/
      mcpcnf_68d6586e304508462ee46c82.json # Custom MCP config called Excel MCP server
  README.md
```

## Setup

### Prerequisites

- [AskUI Suite Installed](https://docs.askui.com/01-tutorials/00-installation)

### Steps

1. **Open AskUI Shell**

   ```bash
   askui-shell
   ```

2. **Configure AskUI Credentials** (first-time setup only)

   1. Create an access token: [Access Token Guide](https://docs.askui.com/02-how-to-guides/01-account-management/04-tokens)  
   2. Set up credentials: [Credentials Setup Guide](https://docs.askui.com/04-reference/02-askui-suite/02-askui-suite/ADE/Public/AskUI-SetSettings)  

3. **Enable Python Environment**

   ```bash
   AskUI-EnablePythonEnvironment -name 'AskUIDemo' -CreateIfNotExists
   ```

4. **Install Dependencies** (re-run if `requirements.txt` changes)

   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Agent**  
   This will start the agent and execute the task defined in `main.py`:

   ```bash
   python ./main.py
   ```

## Interactive chat mode

There is also an interactive way to use the agent via the chat functionality:

- **Attach files in the chat UI** and provide **absolute file paths** to the agent.  
- In chat mode, the MCP file tools are allowed to **read and write files anywhere on disk** (unlike the scripted demo, which is constrained to `source_files`).  
- You can ask the agent to perform tasks step by step and iterate interactively.  

To run chat mode, follow setup steps 1–4, then run the following command from the root of this example project:

```bash
python -m askui.chat
```

Then open [AskUI Caesr](https://app.caesr.ai/) and start a new interactive chat with the agent.  
To access the custom tools, select **PDF to Excel Agent** from the dropdown menu.  

### Example usage

1. Select **PDF to Excel Agent** from the dropdown menu.  
2. Attach the PDF using the file picker icon.  
3. Use a prompt like the following to create a new Excel file that follows the template and contains the data from the PDF:  

```Text
Read the attached PDF and the Excel template from "$PROJECT_ROOT/source_files/demo_template.xlsx".
Create a new Excel file at "$PROJECT_ROOT/source_files/target.xlsx" that follows the template and has the data from the PDF.
```

## Notes and tips

- Replace `demo_data.pdf` and `demo_template.xlsx` in `source_files/` with your own files to adapt the demo.  
