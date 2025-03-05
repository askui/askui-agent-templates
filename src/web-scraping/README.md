# 🕸️ Web Scraping Agent

This repository contains a data scraping agent designed for use with AskUI Hub. The agent demonstrates how to scrape product information from web pages automatically.

- 📄 agent.yml: Metadata configuration file for the agent.
- 🧩 main.py: Python script that implements the web scraping functionality.
- 📘 README.md: Setup and running instructions (you are reading it now!).

## 📚 Table of Contents

- [🚀 Web Scraping Agent](#-web-scraping-agent)
  - [📚 Table of Contents](#-table-of-contents)
  - [⚙️ Prerequisites](#️-prerequisites)
  - [🔧 Setup](#-setup)
  - [▶️ Run Your Agent](#️-run-your-agent)
- [🛠️ Edit and Sync Changes](#️-edit-and-sync-changes)
  - [✏️ Edit Your Agent](#️-edit-your-agent)
  - [🔄 Sync Changes to AskUI Hub](#-sync-changes-to-askui-hub)
- [📤 Share Agent in AskUI Hub](#-share-agent-in-askui-hub)
- [🤝 Support and Contribution](#-support-and-contribution)
- [📜 License](#-license)

## ⚙️ Prerequisites

Before you can set up and run your agent, ensure you have the following installed:

- 🔄 [AskUI Shell](https://docs.askui.com) - The command line tool for AskUI Agnets.
- 🖊️ A code editor of your choice (e.g., VSCode, PyCharm).
- 🌐 A web browser (for the scraping functionality).

## 🔧 Setup

Follow these steps to set up your agent:

1. **Start AskUI Shell:**

    ```sh
    askui-shell
    ```

2. **Install dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

## ▶️ Run Your Agent

This agent scrapes product data from Miinto's men shirts page and saves it to a text file. When run, it:

1. Opens the Miinto website
2. Scrolls through product listings
3. Extracts product names and prices
4. Saves the data to a file named data.txt

To run your agent locally:

```sh
python main.py
```

>💡 Tip: You can modify the target website and extraction logic in `main.py` to scrape different websites or data formats.

# 🛠️ Edit and Sync Changes

After making changes to your agent locally, you need to sync them back to AskUI Hub.

## ✏️ Edit Your Agent

Open and edit your agent files using your preferred code editor. Common files to edit include:

- 🐍 Python Files: Modify your agent's logic.
- ⚙️ Configuration Files: Update settings in agent.yml.
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
