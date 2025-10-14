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

### Docker Quickstart

Build and run the backend service inside a container to verify the Docker image:

1. **Build the Image**

   ```bash
   docker build -f build/Dockerfile -t pr-cybr-backend-agent .
   ```

2. **Start the Container**

   ```bash
   docker run --rm -p 8000:8000 pr-cybr-backend-agent
   ```

   The container prints `Agent is running` to confirm the backend service launched successfully. Override the default runtime settings by passing environment variables such as `AGENT_ENV` or `AGENT_PORT` via `-e` flags if needed.

### Cloud Deployment

To deploy the agent to a cloud environment:

1. **Configure Repository Secrets**

- Navigate to `Settings` > `Secrets and variables` > `Actions` in your GitHub repository.
- Add the required secrets:
   - `CLOUD_API_KEY`
   - `DOCKERHUB_USERNAME`
   - `DOCKERHUB_PASSWORD`
   - Any other cloud-specific credentials.

2. **Deploy Using GitHub Actions**

- The Docker Compose configuration used for deployment lives at `docker-compose.yml` in the repository root.
- The automated deployment workflow is defined in `.github/workflows/docker-compose.yml`.
- Add a repository secret named `DEPLOY_ENV_FILE` that contains the key/value pairs required for the Compose deployment.
  This secret should mirror the values that would normally live in your `.env` file so the workflow can write it to `.env` at runtime.
- Push changes to the `main` branch or trigger the workflow manually from the **Actions** tab to run the deployment.

3. **Manual Deployment**

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
