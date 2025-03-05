from askui import VisionAgent


def test_my_test(agent: VisionAgent):
    agent.click("Hello World")
    answer = agent.get("Is the mouse over 'Hello World'? Answer with 'yes' or 'no'.")

    assert answer == "yes"
