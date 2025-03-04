from askui import VisionAgent


def test_my_test(agent: VisionAgent):
    agent.click("Hello World")
    anser = agent.get("Is the mouse over 'Hello World'? Answer with 'yes' or 'no'.")

    assert anser == "yes"