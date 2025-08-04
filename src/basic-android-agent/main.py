"""
AskUI Android Agent Demo - Interactive Android Device Automation

This script demonstrates the core capabilities of the AskUI Android Vision Agent,
showing how to interact with Android devices using natural language commands
and programmatic controls.
"""

from askui import AndroidVisionAgent
from askui import locators as loc
import time


def main():
    """
    Main demonstration function showcasing AskUI Android agent capabilities.
    """
    print("🤖 Starting AskUI Android Agent Demo...")
    print("=" * 50)

    # Initialize your agent context manager
    with AndroidVisionAgent() as agent:
        print("✅ Agent initialized successfully!")

        # Select device by serial number in case of multiple devices
        # Uncomment and modify if you have multiple devices connected
        # agent.set_device_by_serial_number("emulator-5554")

        # Demo 1: Natural Language Screen Analysis
        print("\n📱 Demo 1: Screen Analysis")
        print("-" * 30)
        screen_description = agent.get("What can you see on the screen?")
        print(f"Screen contains: {screen_description}")

        # Demo 2: Assertion-based Testing
        print("\n✅ Demo 2: Assertion Testing")
        print("-" * 30)
        try:
            has_gmail = agent.get(
                'Does the screen contain the text "Gmail"?', response_schema=bool
            )
            print(f"Gmail text found: {has_gmail}")

            if has_gmail:
                print("🎯 Tapping on Gmail app...")
                agent.tap(loc.Text("Gmail"))
                time.sleep(2)  # Wait for app to open
        except Exception as e:
            print(f"⚠️  Gmail not found or error: {e}")

        # Demo 3: Device Navigation
        print("\n🏠 Demo 3: Device Navigation")
        print("-" * 30)

        # Go to home screen
        print("Pressing HOME button...")
        agent.key_tap("HOME")
        time.sleep(1)

        # Demonstrate key combinations
        print("Pressing HOME + BACK combination...")
        agent.key_combination(["HOME", "BACK"], duration_in_ms=1000)
        time.sleep(1)

        # Demo 4: Touch Gestures
        print("\n Demo 4: Touch Gestures")
        print("-" * 30)

        # Drag and drop demonstration
        print("Performing drag and drop gesture...")
        agent.drag_and_drop(x1=100, y1=100, x2=200, y2=200, duration_in_ms=1000)
        time.sleep(1)

        # Swipe demonstration
        print("Performing swipe gesture...")
        agent.swipe(x1=100, y1=100, x2=200, y2=200, duration_in_ms=1000)
        time.sleep(1)

        # Demo 5: Text Input
        print("\n⌨️  Demo 5: Text Input")
        print("-" * 30)
        print("Typing 'Hello AskUI World'...")
        agent.type("Hello AskUI World")
        time.sleep(1)

        # Demo 6: Shell Commands
        print("\n Demo 6: Shell Commands")
        print("-" * 30)
        try:
            print("Executing shell command: ls -l")
            shell_response = agent.shell("ls -l")
            print(f"Shell output: {shell_response}")
        except Exception as e:
            print(f"⚠️  Shell command failed: {e}")

        # Demo 7: Agentic Behavior (Natural Language Commands)
        print("\n🧠 Demo 7: Agentic Behavior")
        print("-" * 30)
        print("Instructing agent to search for AskUI company...")
        try:
            agent.act(
                "Search for the company AskUI in the browser, and open the first result."
            )
            print("✅ Agent successfully executed the search command!")
        except Exception as e:
            print(f"⚠️  Agentic command failed: {e}")

        print("\n🎉 Demo completed successfully!")
        print("=" * 50)


if __name__ == "__main__":
    main()
