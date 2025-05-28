# 🚀 PLC Application Vision Agent

## 🎥 Demo

Watch a demo of the PLC Application Vision Agent in action:

[![PLC Application Vision Agent Demo - Watch Video](https://cdn.loom.com/sessions/thumbnails/86fc3b4591e94aa197a4eab1df8b61ed-2e5f840315419694-full-play.gif)](https://www.loom.com/share/86fc3b4591e94aa197a4eab1df8b61ed)


This repository contains a vision agent designed for testing a PLC (Programmable Logic Controller) water tank simulation application. The agent consists of the following key components:

- 📄 `agent.yml`: Metadata configuration file for the agent.
- 🧩 `main.py`: Contains the vision agent test cases for the PLC application.
- 🧩 `plc_desktop.py`: The PLC water tank simulation application.
- 📘 `README.md`: Setup and running instructions (you are reading it now!).

## 📚 Table of Contents

- [🚀 PLC Application Vision Agent](#-plc-application-vision-agent)
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

- 🔄 [AskUI Shell](https://docs.askui.com) - The command line tool for AskUI Agents.
- 🖊️ A code editor of your choice (e.g., VSCode, PyCharm).
- 🐍 Python 3.x
- 📦 Required Python packages:
  - PySide6
  - pyqtgraph
  - askui

## 🔧 Setup

Follow these steps to set up your agent:

1. **Install dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

## ▶️ Run Your Agent

To run the PLC application and test it with the vision agent:

1. **Start the PLC Application:**

    ```sh
    python plc_desktop.py
    ```

2. **Maximize the PLC Application Window:**
   - Make sure the PLC application window is in full screen mode
   - The application should show a water tank simulation with controls

3. **Run the Vision Agent Tests:**

    ```sh
    python main.py
    ```

The vision agent will perform two tests:
- Manual mode test: Verifies the manual tank level control
- Auto mode test: Tests the automatic pump control functionality

>💡 Tip: The PLC application must be running and visible before starting the vision agent tests.

# 🛠️ Edit and Sync Changes

After making changes to your agent locally, you need to sync them back to AskUI Hub.

## ✏️ Edit Your Agent

Open and edit your agent files using your preferred code editor. Common files to edit include:

- 🐍 `main.py`: Modify the vision agent test cases
- 🐍 `plc_desktop.py`: Update the PLC simulation application
- ⚙️ `agent.yml`: Update agent configuration

## 🔄 Sync Changes to AskUI Hub

After editing, sync your changes using:

```sh
AskUI-SyncAgents -Direction UP
```

This uploads your local changes to AskUI Hub, making them available to other team members.

# 📤 Share Agent in AskUI Hub

Once your changes are synced, you can share your agent with others in your team or organization:

1. Open [AskUI Hub](https://hub.askui.com) in your browser
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

�� Happy Coding! 🚀
