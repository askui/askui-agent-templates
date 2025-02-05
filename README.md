# askui-agent-templates
Templates for AskUI Agents that can be created through the AskUI Hub

We have now too ways files are ignored:
- Not in an agent template directory
- Or inside an ignore file

An agent template directory may not start with a dot

What about making it easier basically syncing everything but the things in the ignore files?

We want to use the template directory as otherwise it would not be clear what to copy as part of the agent template when creating the agent. But we could also allow for shared files by allowing to specify inside the agent template what is part of the agent template and what is not.

We need an ignore file at the moment as there may be pycaches, index files etc. in an agent template folder.

Depends on git being installed and set up

LOG_LEVEL for setting log levels

Manifest file my not be bigger than 1MB
