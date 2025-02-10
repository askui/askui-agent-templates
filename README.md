# askui-agent-templates

Templates for AskUI Agents that can be created through the AskUI Hub.

## Usage

### Quickstart

Create a template by adding a directory inside `src/` containing an `agent.yml` file. The `agent.yml` should follow the [agent schema](./agent-schema.yml) and allows you to define metadata of the agent template and the actual agent to be created from it when a user selects it in the AskUI Hub. Place all additional files, e.g., a `README.md`, `requirements.txt`, and the actual agent code, e.g., `main.py`, in the template directory to include it with the agent when it is created. All these files are going to be copied to the actual agent's directory in the user's workspace on creation of an agent from the template.

Create, update or delete agent templates by pushing to the `main` or `dev` branch on the repository making the templates available in the AskUI Hub. While `dev` syncs to the dev environment ([hub-dev.askui.com](https://hub-dev.askui.com)), `main` syncs to the production environment ([hub.askui.com](https://hub.askui.com)).


### More details

Directories within `src/` that don't contain an `agent.yml` file are not regarded as agent templates and, therefore, ignored.

Agent templates including a `manifest.yml` are synced to S3 and the sync is triggered by a push to the `main` or `dev` branch. The `manifest.yml` is created within the CI pipeline. It is a summary of all templates in the repository and is used for providing an overview of all available templates in the AskUI Hub. 

AWS S3 is used as the actual backend for retrieving the templates and an overview of all templates (the manifest) by the AskUI Hub. The AskUI Hub has no direct dependency on this repository.


### Agent Template Validation

If you would like to test wether your agent template is valid, you can run the script for validating agent templates and creating a manifest file locally:

```bash
# Setup venv
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r scripts/requirements.txt

# Set log level
export LOG_LEVEL=INFO # alternatives: CRITICAL, FATAL, ERROR, WARN, WARNING, INFO, DEBUG, NOTSET

# Run the script
python -m scripts.validate_and_create_manifest
```

The script is also run in the CI pipeline ([`validate-and-sync.yml`](./.github/workflows/validate-and-sync.yml)) on PR and push to the `main` or `dev` branch.
