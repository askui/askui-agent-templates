from askui import VisionAgent

# Initialize your agent context manager
with VisionAgent() as agent:
    # Use the webbrowser tool to start browsing
    agent.tools.webbrowser.open_new("http://www.google.com")

    # Start to automate individual steps
    agent.click("url bar")
    agent.type("http://www.google.com")
    agent.keyboard("enter")

    # Extract information from the screen
    datetime = agent.get("What is the datetime at the top of the screen?")
    print(datetime)

    # Or let the agent work on its own
    agent.act("search for a flight from Berlin to Paris in January")