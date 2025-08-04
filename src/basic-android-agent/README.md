# AskUI Android Agent Demo

A comprehensive demonstration of the AskUI Android Vision Agent library, showcasing how to automate Android devices using natural language commands and programmatic controls.

## 🚀 What is AskUI?

AskUI is a powerful Android automation library that allows you to interact with Android devices using:
- **Natural language commands** - Tell the agent what you want to do in plain English
- **Vision-based interaction** - The agent "sees" what's on screen and can interact accordingly
- **Programmatic controls** - Direct API calls for precise automation
- **Shell command execution** - Run system commands on the device

## ✨ Key Features Demonstrated

### 1. Screen Analysis
- **Natural Language Queries**: Ask what's visible on screen
- **Boolean Assertions**: Check if specific elements exist
- **Contextual Understanding**: The agent understands screen content

### 2. Touch Interactions
- **Tap**: Click on specific elements or text
- **Drag & Drop**: Move elements around the screen
- **Swipe**: Navigate through content
- **Key Combinations**: Execute complex key sequences

### 3. Text Input
- **Direct Typing**: Type text directly into input fields
- **Natural Language**: Describe what you want to type

### 4. Device Navigation
- **Home Button**: Return to home screen
- **Back Button**: Navigate back
- **Key Combinations**: Execute multiple key presses

### 5. Shell Commands
- **System Commands**: Execute shell commands on the device
- **File Operations**: List files, check system status

### 6. Agentic Behavior
- **Natural Language Instructions**: Give high-level commands
- **Autonomous Execution**: Agent figures out how to accomplish tasks
- **Context Awareness**: Understands current screen state

## Installation

### Prerequisites
- AskUI Shell installed
- ADB (Android Debug Bridge) installed and configured

### Setup

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Connect your Android device**
   - Enable Developer Options and USB Debugging
   - Connect via USB or start an emulator
   - Verify connection: `adb devices` (it should show a list of connected devices)

## 🎯 Usage

### Basic Usage
```bash
python main.py
```

### Customization
Edit `main.py` to:
- Change device selection (uncomment and modify the serial number line)
- Add your own automation scenarios
- Modify timing and delays
- Add error handling for your specific use cases

## 📱 Demo Scenarios

The demo includes several scenarios that showcase different capabilities:

1. **Screen Analysis**: Ask what's visible on the current screen
2. **App Interaction**: Find and tap on the Gmail app
3. **Navigation**: Use device buttons and gestures
4. **Text Input**: Type text into input fields
5. **Shell Commands**: Execute system commands
6. **Agentic Behavior**: Give natural language instructions

## Configuration

### Device Selection
If you have multiple devices connected, uncomment and modify this line in `main.py`:
```python
agent.set_device_by_serial_number("your-device-serial")
```

### Timing Adjustments
Modify the `time.sleep()` calls to adjust delays based on your device's performance.

## 🎨 Customization Examples

### Adding Your Own Scenarios
```python
# Example: Open a specific app
agent.act("Open the Settings app")

# Example: Fill a form
agent.type("your-email@example.com")
agent.tap(loc.Text("Submit"))

# Example: Navigate through menus
agent.tap(loc.Text("Menu"))
agent.tap(loc.Text("Settings"))
```

### Error Handling
```python
try:
    agent.tap(loc.Text("Some Button"))
except Exception as e:
    print(f"Button not found: {e}")
    # Fallback action
```

## 🐛 Troubleshooting

### Common Issues

1. **Device Not Found**
   - Ensure ADB is properly installed
   - Check device connection: `adb devices`
   - Enable USB debugging on device

2. **Permission Errors**
   - Grant necessary permissions on the Android device
   - Check if the device is authorized for debugging

3. **Element Not Found**
   - Verify the element text/description is correct
   - Check if the element is visible on screen
   - Try using different locator strategies

4. **Timing Issues**
   - Increase delays for slower devices
   - Add wait conditions for dynamic content

### Debug Mode
Enable verbose logging by modifying the agent initialization:
```python
with AndroidVisionAgent(
    log_level=logging.DEBUG
) as agent:
```

## AskUI Chat

You can test the agentic behavior directly through AskUI's web-based chat interface without writing any code. This allows you to interact with your Android device using natural language commands through a user-friendly chat interface.

### Getting Started with AskUI Chat

1. **Start the Chat Server**
   ```bash
   python -m askui.chat
   ```

2. **Access the Web Interface**
   - Open your web browser and navigate to [hub.askui.com](https://hub.askui.com)
   - Use the chat interface to interact with your connected Android device

### What You Can Do

- **Natural Language Commands**: "Open Gmail and check for new messages"
- **Screen Analysis**: "What apps are currently visible on my home screen?"
- **Device Control**: "Go back to the home screen and open Settings"
- **Interactive Testing**: Experiment with different commands and see how the agent responds

### Benefits

- **No Coding Required**: Test automation ideas quickly without writing Python code
- **Real-time Interaction**: See immediate responses and device actions
- **Learning Tool**: Understand how the agent interprets and executes commands
- **Rapid Prototyping**: Validate automation workflows before implementing them in code

This is perfect for exploring AskUI's capabilities or demonstrating the technology to others!


## �� API Reference

### Core Methods

- `agent.get(question, response_schema=bool)` - Ask questions about screen content
- `agent.tap(locator)` - Tap on elements
- `agent.type(text)` - Type text
- `agent.key_tap(key)` - Press device keys
- `agent.swipe(x1, y1, x2, y2)` - Swipe gesture
- `agent.drag_and_drop(x1, y1, x2, y2)` - Drag and drop
- `agent.shell(command)` - Execute shell commands
- `agent.act(instruction)` - Natural language instructions

### Locators
- `loc.Text("text")` - Find by text content
- `loc.Id("id")` - Find by element ID
- `loc.Class("class")` - Find by CSS class

## 🔗 Resources

- [AskUI Documentation](https://docs.askui.com)
- [Android Developer Guide](https://developer.android.com)
- [ADB Documentation](https://developer.android.com/studio/command-line/adb)

---

**Happy Automating! 🚀**
