# 🚀 PDF to Excel Agent

This repository contains a PDF to Excel conversion agent that uses OpenAI's Vision API or AskUI's Vision capabilities to extract data from PDF invoices and convert it into structured Excel files. The agent consists of:

- 📄 `agent.yml`: Metadata configuration file for the agent.
- 🐍 `main.py`: Core Python script containing the extraction and conversion logic.
- 📘 `README.md`: Setup and running instructions (you are reading it now!).

## 📚 Table of Contents

- [🚀 PDF to Excel Agent](#-pdf-to-excel-agent)
  - [📚 Table of Contents](#-table-of-contents)
  - [⚙️ Prerequisites](#️-prerequisites)
  - [🔧 Setup](#-setup)
  - [▶️ Run Your Agent](#️-run-your-agent)
  - [📋 Usage Guide](#-usage-guide)
- [🛠️ Edit and Sync Changes](#️-edit-and-sync-changes)
  - [✏️ Edit Your Agent](#️-edit-your-agent)
  - [🔄 Sync Changes to AskUI Hub](#-sync-changes-to-askui-hub)
- [📤 Share Agent in AskUI Hub](#-share-agent-in-askui-hub)
- [🤝 Support and Contribution](#-support-and-contribution)
- [📜 License](#-license)

## ⚙️ Prerequisites

Before you can set up and run your agent, ensure you have the following:

- 🔄 [AskUI Shell](https://docs.askui.com) - The command line tool for AskUI Agents
- 🖊️ A code editor of your choice (e.g., VSCode, PyCharm)
- 🔑 OpenAI API key (if using OpenAI Vision capabilities)
- 📦 Required Python packages (see requirements.txt)

## 🔧 Setup

1. **Start AskUI Shell:**
    ```sh
    askui-shell
    ```

2. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

3. **Set up environment variables:**
    ```sh
    export OPENAI_API_KEY='your-api-key-here'  # Required for OpenAI Vision
    ```

## ▶️ Run Your Agent

1. **Prepare your PDFs:**
   - Create a folder named `pdfs` in your project directory
   - Place your PDF invoices in this folder

2. **Run the agent:**
    ```sh
    python main.py
    ```

## 📋 Usage Guide

**OpenAI Vision Mode (Default)**
   - Uses OpenAI's Vision API for high-accuracy data extraction
   - Extracts structured data including:
     - Invoice numbers
     - Dates
     - Line items (quantity, weights, prices, etc.)
  
The extracted data is saved to `extraction.xlsx` with:
- One sheet per PDF
- Structured columns for invoice details
- Separate rows for each line item

# 🛠️ Edit and Sync Changes

## ✏️ Edit Your Agent

You can customize the agent by modifying:

- 🐍 `main.py`: Adjust extraction logic, data processing, or output format
- ⚙️ `agent.yml`: Update agent configuration
- 🔧 Extraction parameters in the OpenAI prompt (within `main.py`)
- 🖼️ Assets: Manage images, data files, or other assets required by the agent.

## 🔄 Sync Changes to AskUI Hub

After editing, sync your changes using:

```sh
AskUI-SyncAgents -Direction UP
```

This uploads your local changes to AskUI Hub, making them available to other team members.

# 📤 Share Agent in AskUI Hub

Once your changes are synced, you can share your agent with others in your team or organization:

1. Open to [AskUI Hub](https://hub.askui.com) in your browser
2. Navigate to the Agents Overview clicking on `Agents` in the sidebar
3. See your Agents

Inform your team members that the updated agent is now available on AskUI Hub!

# 🤝 Support and Contribution

If you encounter issues or have suggestions for improvements:

- 🐛 Open an issue on this repository.
- 🔧 Submit a pull request with your changes.
Contributions are always welcome!

# 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

🎉 Happy Coding! 🚀
