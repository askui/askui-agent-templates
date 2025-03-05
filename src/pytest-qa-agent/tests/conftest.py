import pytest
from askui import VisionAgent


@pytest.fixture(scope="session")
def agent():
    with VisionAgent() as agent:
        yield agent
    
