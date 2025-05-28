# 🎮 Tic Tac Toe Agent

This repository contains an AI agent that plays Tic Tac Toe using AskUI. The agent implements strategic gameplay and can play against the computer on playtictactoe.org.

## 🎥 Demo

![Click here for the video](https://www.loom.com/embed/621e2dd6fb4d44d2b1181f1b11e013c9?sid=64422ffa-20f3-4325-a02c-ec2a613788ba)

## 📚 Table of Contents

- [🎮 Tic Tac Toe Agent](#-tic-tac-toe-agent)
  - [🎥 Demo](#-demo)
  - [📚 Table of Contents](#-table-of-contents)
  - [⚙️ Prerequisites](#️-prerequisites)
  - [🔧 Setup](#-setup)
  - [▶️ Run Your Agent](#️-run-your-agent)
  - [🎯 Game Strategy](#-game-strategy)
  - [🤝 Support and Contribution](#-support-and-contribution)
  - [📜 License](#-license)

## ⚙️ Prerequisites

Before you can set up and run your agent, ensure you have the following installed:

- 🔄 [AskUI Shell](https://docs.askui.com) - The command line tool for AskUI Agents
- 🖊️ A code editor of your choice (e.g., VSCode, PyCharm)
- 🐍 Python 3.x

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

To run the Tic Tac Toe agent:

```sh
python main.py
```

The agent will:
1. Open playtictactoe.org in your browser
2. Play as player X
3. Implement strategic moves
4. Automatically reset the game if needed

## 🎯 Game Strategy

The agent implements the following strategic rules:

1. **First Move Strategy:**
   - Takes center if available
   - Takes a corner if center is taken

2. **Winning Strategy (in priority order):**
   - Win: Complete any line with two X's
   - Block: Stop opponent's two-in-a-row
   - Fork: Create multiple winning paths
   - Defense: Take opposite corner if opponent has corner, or side middle if they have two corners

3. **Game Flow:**
   - Waits 2 seconds between moves
   - Verifies opponent's moves
   - Resets game if needed

4. **Error Handling:**
   - Closes any popups
   - Refreshes if game freezes
   - Retries failed moves

## 🤝 Support and Contribution

If you encounter issues or have suggestions for improvements:

- 🐛 Open an issue on this repository
- 🔧 Submit a pull request with your changes

Contributions are always welcome!

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

�� Happy Gaming! 🚀
