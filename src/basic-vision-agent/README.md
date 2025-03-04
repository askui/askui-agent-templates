# 🚀 Basic Agent

This repository contains a basic agent designed for use with AskUI Hub. The agent consists of the following key components:

- 📄 `agent.yml`: Metadata configuration file for the agent.
- 🧩 Logic and assets files: Python scripts and other necessary assets for the agent's functionality.
- 📘 `README.md`: Setup and running instructions (you are reading it now!).

## 📚 Table of Contents
1. [⚙️ Prerequisites](#-prerequisites)
2. [🔧 Setup](#-setup)
3. [▶️ Run Your Agent](#-run-your-agent)
4. [🛠️ Edit and Sync Changes](#-edit-and-sync-changes)
5. [📤 Share Agent in AskUI Hub](#-share-agent-in-askui-hub)
6. [🤝 Support and Contribution](#-support-and-contribution)
7. [📜 License](#-license)

## ⚙️ Prerequisites

Before you can set up and run your agent, ensure you have the following installed:

- 🔄 [AskUI Shell](https://docs.askui.com) - The command line tool for AskUI Agnets.
- 🖊️ A code editor of your choice (e.g., VSCode, PyCharm).


## 🔧 Setup

Follow these steps to set up your agent:

1. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

## ▶️ Run Your Agent

Your agent is essentially a folder containing:

- 📄 `agent.yml` - Contains metadata about the agent.
- 🧩 `main.py` - Files with logic and assets of the agent, such as Python files.
- 📘 `README.md` - Contains setup and running instructions (this file).

To run your agent locally:

```sh
python main.py
```

>💡 Tip: Check the configuration in agent.yml to ensure the agent is connected to the correct environment.

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
