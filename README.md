<!--
Updates that need to be made:
1. 
-->

# PR-CYBR-BACKEND-AGENT

## Overview

The **PR-CYBR-BACKEND-AGENT** is a core component of the PR-CYBR ecosystem, responsible for managing backend functionalities that power the platform’s critical operations, including secure API management, data processing, and integration with other agents. This agent is built for robust and scalable performance to support the PR-CYBR mission of protecting Puerto Rico’s digital infrastructure.

## Key Features

- **Secure API Management**: Handles endpoints for frontend applications and other agents.
- **Data Handling**: Processes incoming data streams, validates information, and manages secure storage.
- **Integration with PR-CYBR Ecosystem**: Communicates with other agents to maintain smooth operations.
- **Scalable Design**: Built to handle increasing loads as PR-CYBR grows.

## Getting Started

### Prerequisites

- **Git**: For cloning the repository.
- **Python 3.8+**: Necessary for running the backend services.
- **Docker**: Required for containerization and deployment.
- **Access to GitHub Actions**: For automated workflows.

### Local Setup

To set up the `PR-CYBR-BACKEND-AGENT` locally on your machine:

1. **Clone the Repository**

```bash
git clone https://github.com/PR-CYBR/PR-CYBR-BACKEND-AGENT.git
cd PR-CYBR-BACKEND-AGENT
```

2. **Run Local Setup Script**

```bash
./scripts/local_setup.sh
```
_This script will install necessary dependencies and set up the local environment._

### Cloud Deployment

To deploy the agent to a cloud environment while centralizing secrets in Terraform Cloud:

1. **Configure Terraform Cloud**

- Connect the target Terraform Cloud workspace to this repository using the native VCS integration.
- Store all environment variables, Terraform variables, and credentials inside Terraform Cloud.

2. **Populate GitHub repository variables for the workflow bridge**

- Navigate to `Settings` > `Secrets and variables` > `Actions` > `Variables` in GitHub.
- Add the variables referenced in [`docs/terraform-cloud-bridge.md`](docs/terraform-cloud-bridge.md) (for example `TFC_ORGANIZATION`, `TFC_WORKSPACE_NAME`, `TFC_WORKFLOW_ID`, and the token exchange details supplied by Terraform Cloud).
- No GitHub secrets are required for the Terraform Cloud workflow bridge; all sensitive values remain inside Terraform Cloud.

3. **Deploy Using GitHub Actions**

- The remote execution workflow is defined in `.github/workflows/terraform-cloud-bridge.yml`.
- Push changes to the tracked branches or open a pull request to queue a Terraform Cloud run automatically.

4. **Manual Deployment**

- Use the deployment script for manual deployment:

```bash
./scripts/deploy_agent.sh
```

- Ensure you have Docker and cloud CLI tools installed and configured on your machine.

## Integration

The `PR-CYBR-BACKEND-AGENT` integrates with other PR-CYBR agents to provide essential backend services. It communicates with:

- **PR-CYBR-FRONTEND-AGENT**: Serves APIs and data required by the frontend interface.
- **PR-CYBR-DATABASE-AGENT**: Handles data storage and retrieval operations.
- **PR-CYBR-SECURITY-AGENT**: Ensures secure data handling and compliance with security policies.
- **PR-CYBR-DATA-INTEGRATION-AGENT**: Processes and integrates data from various sources.

## Usage

- **Development**

  - Start the development server:

```bash
python setup.py develop
```

  - The backend services will run locally, listening on the configured port (default is `http://localhost:8000`).
  - Make changes to the source code in the `src/` directory; the server will need to be restarted to apply changes.

- **Testing**

  - Run unit and integration tests:

```bash
python -m unittest discover tests
```

- **Building for Production**

  - Create a production build:

```bash
python setup.py install
```

  - The build artifacts will be installed as a Python package on your system.

## License

This project is licensed under the **MIT License**. See the [`LICENSE`](LICENSE) file for details.

---

For more information, refer to the [Django Documentation](https://docs.djangoproject.com/en/stable/) or contact the PR-CYBR team.
