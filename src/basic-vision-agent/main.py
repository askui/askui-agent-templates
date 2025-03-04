from askui import VisionAgent

# Initialize your agent context manager
with VisionAgent() as agent:
    # Use the webbrowser tool to start browsing
    agent.tools.webbrowser.open_new("http://www.google.com")

    # Start to automate individual steps
    agent.click("url bar")
    agent.type("http://www.google.com")
    agent.keyboard("enter")
