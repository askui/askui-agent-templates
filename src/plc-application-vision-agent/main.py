from askui import VisionAgent
import subprocess

with VisionAgent() as agent:

    # Manual mode test

    agent.act("""
    wait until you the screen is fully loaded.
    You are currently looking at a PLC screen.
    You are in Manual mode. 
    You need to pull the manual tank level to 50%
    """)

    is_equal = agent.get("Is the Handle of the slider equal the procentage of the water tank level?", response_schema=bool)
    if is_equal:
        print("✅ Slider and water tank levels are synchronized")
    else:
        print("❌ Slider and water tank levels are not synchronized")
    
    assert is_equal, "The slider is not at the correct level"

    # Auto mode test

    agent.act("""
    Wait until you see the screen is fully loaded.
    You are currently looking at a PLC screen.
    You have to activate auto mode.
    Then you need to click on Stop Pump
    Wait until it reaches 0%
    If there is a pop up, simulate closing it.
    """)

    is_equal = agent.get("Is the Handle of the slider equal the procentage of the water tank level?", response_schema=bool)
    if is_equal:
        subprocess.run(["echo", "✅ Slider and water tank levels are synchronized"])
    else:
        subprocess.run(["echo", "❌ Slider and water tank levels are not synchronized"])
    
    assert is_equal, "The slider is not at the correct level"