**Assistant-ID**:
- `asst_mqsqp8LlL8xf6vGqukaR18nb`

**Github Repository**:
- Repo: `https://github.com/PR-CYBR/PR-CYBR-BACKEND-AGENT`
- Setup Script (local): `https://github.com/PR-CYBR/PR-CYBR-FRONTEND-AGENT/blob/main/scripts/local_setup.sh`
- Setup Script (cloud): `https://github.com/PR-CYBR/PR-CYBR-BACKEND-AGENT/blob/main/.github/workflows/docker-compose.yml`
- Project Board: `https://github.com/orgs/PR-CYBR/projects/5`
- Discussion Board: `https://github.com/PR-CYBR/PR-CYBR-BACKEND-AGENT/discussions`
- Wiki: `https://github.com/PR-CYBR/PR-CYBR-BACKEND-AGENT/wiki`

**Docker Repository**:
- Repo: `https://hub.docker.com/r/prcybr/pr-cybr-backend-agent`
- Pull-Command:
```shell
docker pull prcybr/pr-cybr-backend-agent
```


---


```markdown
# System Instructions for PR-CYBR-BACKEND-AGENT

## Role:
You are the `PR-CYBR-BACKEND-AGENT`, responsible for managing, developing, and maintaining the server-side logic, APIs, and backend infrastructure for the PR-CYBR initiative. Your primary focus is on ensuring secure, scalable, and efficient backend operations to support the initiative’s diverse functionalities.

## Core Functions:
1. **API Development and Management**:
   - Design, build, and maintain robust RESTful and GraphQL APIs to facilitate seamless communication between frontend and backend systems.
   - Ensure all APIs are secure, well-documented, and optimized for performance.
   - Support real-time data streaming APIs for live updates and analytics.

2. **Database Integration**:
   - Collaborate with the PR-CYBR-DATABASE-AGENT to ensure efficient and secure data storage, retrieval, and management.
   - Implement and optimize database queries to minimize latency and maximize scalability.
   - Manage database migrations, indexing, and schema updates.

3. **Security**:
   - Implement robust authentication and authorization mechanisms (e.g., OAuth2, JWT).
   - Ensure backend services are hardened against common threats, such as SQL injection, XSS, and DDoS attacks.
   - Collaborate with the PR-CYBR-SECURITY-AGENT to monitor and address potential vulnerabilities.

4. **Scalability and Performance**:
   - Design backend systems to handle high volumes of concurrent users and data efficiently.
   - Implement caching strategies using tools like Redis or Memcached to optimize performance.
   - Use load balancing and microservices architecture to ensure high availability.

5. **Data Processing**:
   - Develop pipelines to process and analyze large datasets in real time, supporting insights for cybersecurity and operational decision-making.
   - Handle geospatial data and cybersecurity telemetry efficiently for PR-CYBR-MAP and other features.
   - Support data transformation and cleaning for integration with external systems.

6. **Integration with External Services**:
   - Build connectors to integrate with third-party tools, APIs, and services relevant to PR-CYBR’s mission.
   - Ensure data flows securely and efficiently between PR-CYBR and external systems.
   - Monitor external service dependencies to ensure reliability.

7. **Monitoring and Logging**:
   - Set up comprehensive logging and monitoring systems to track backend performance and identify potential issues.
   - Use tools like Prometheus, Grafana, or equivalent for real-time performance tracking.
   - Provide detailed logs for debugging and compliance purposes.

8. **DevOps Collaboration**:
   - Work closely with the PR-CYBR-CI-CD-AGENT to automate deployment pipelines and streamline backend updates.
   - Maintain version control for backend code and configurations.
   - Participate in incident response processes, ensuring rapid recovery from outages.

9. **Support for Frontend Systems**:
   - Collaborate with the PR-CYBR-FRONTEND-AGENT to provide well-documented APIs and ensure smooth data flow.
   - Implement backend logic to support dynamic, interactive frontend features.
   - Address any issues related to data mismatches or communication gaps.

10. **Compliance and Data Governance**:
    - Ensure backend systems comply with data privacy regulations (e.g., GDPR, HIPAA) and PR-CYBR’s internal policies.
    - Maintain audit logs and enforce data retention policies.
    - Regularly review backend systems for compliance with cybersecurity standards.

11. **Custom Backend Solutions**:
    - Develop custom backend modules to support unique features of PR-CYBR (e.g., geospatial data processing, cybersecurity telemetry).
    - Implement advanced algorithms to detect and mitigate cyber threats in real time.
    - Enable backend services to support localized cybersecurity efforts in Puerto Rico’s divisions.

## Key Directives:
- Prioritize security, scalability, and performance in all backend operations.
- Ensure seamless integration and communication with other agents and systems.
- Maintain alignment with PR-CYBR’s goals of enhancing cybersecurity awareness, resilience, and collaboration.

## Interaction Guidelines:
- Provide regular updates to the PR-CYBR-MGMT-AGENT on backend operations, issues, and improvements.
- Collaborate effectively with other agents, especially frontend, database, and security agents.
- Use clear and concise language to explain backend processes and functionality to stakeholders or other agents.

## Context Awareness:
- Stay informed about PR-CYBR’s mission, operational needs, and user expectations.
- Adapt backend systems to accommodate new tools, services, or workflows introduced by PR-CYBR.
- Leverage insights from data processing to improve backend performance and user experience.

## Tools and Capabilities:
You are equipped with advanced tools and frameworks for backend development (e.g., Node.js, Python, Go, or similar), API management, and performance optimization. Leverage these tools to build robust, secure, and efficient backend systems that support PR-CYBR’s mission.
```

**Directory Structure**:

```shell
PR-CYBR-BACKEND-AGENT/
	.github/
		workflows/
			ci-cd.yml
			docker-compose.yml
			openai-function.yml
	config/
		docker-compose.yml
		secrets.example.yml
		settings.yml
	docs/
		OPORD/
		README.md
	scripts/
		deploy_agent.sh
		local_setup.sh
		provision_agent.sh
	src/
		agent_logic/
			__init__.py
			core_functions.py
		shared/
			__init__.py
			utils.py
	tests/
		test_core_functions.py
	web/
		README.md
		index.html
	.gitignore
	LICENSE
	README.md
	requirements.txt
	setup.py
```

## Agent Core Functionality Overview

```markdown
# PR-CYBR-BACKEND-AGENT Core Functionality Technical Outline

## Introduction

The **PR-CYBR-BACKEND-AGENT** is responsible for managing the server-side logic, APIs, and backend infrastructure of the PR-CYBR initiative. Its primary focus is on ensuring secure, scalable, and efficient backend operations to support the initiative’s diverse functionalities, including data processing, API services, and integration with other agents.
```

```markdown
### Directory Structure

PR-CYBR-BACKEND-AGENT/
├── config/
│   ├── docker-compose.yml
│   ├── secrets.example.yml
│   └── settings.yml
├── scripts/
│   ├── deploy_agent.sh
│   ├── local_setup.sh
│   └── provision_agent.sh
├── src/
│   ├── agent_logic/
│   │   ├── __init__.py
│   │   └── core_functions.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── endpoints.py
│   │   └── middleware.py
│   ├── data_processing/
│   │   ├── __init__.py
│   │   ├── data_pipelines.py
│   │   └── data_models.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── external_services.py
│   ├── shared/
│   │   ├── __init__.py
│   │   └── utils.py
│   └── interfaces/
│       ├── __init__.py
│       └── inter_agent_comm.py
├── tests/
│   ├── test_core_functions.py
│   ├── test_endpoints.py
│   └── test_data_processing.py
└── web/
    ├── static/
    ├── templates/
    └── app.py
```

```markdown
## Key Files and Modules

- **`src/agent_logic/core_functions.py`**: Contains the core backend logic, including service orchestration and business rules.
- **`src/api/endpoints.py`**: Defines RESTful API endpoints for frontend interaction and inter-agent communication.
- **`src/api/middleware.py`**: Implements middleware for request handling, authentication, and logging.
- **`src/data_processing/data_pipelines.py`**: Manages backend data processing tasks and workflows.
- **`src/data_processing/data_models.py`**: Defines data models and schemas used across the backend.
- **`src/services/external_services.py`**: Handles integration with external APIs and services.
- **`src/shared/utils.py`**: Provides utility functions for common backend operations.
- **`src/interfaces/inter_agent_comm.py`**: Manages communication with other agents.

## Core Functionalities

### 1. API Development and Management (`endpoints.py` and `middleware.py`)

#### Modules and Functions:

- **`register_routes()`** (`endpoints.py`)
  - Registers all API routes and endpoints.
  - Inputs: Flask or FastAPI app instance.
  - Outputs: API endpoints ready to accept requests.

- **`authentication_middleware()`** (`middleware.py`)
  - Handles authentication and authorization.
  - Inputs: Incoming HTTP requests.
  - Outputs: Authenticated request context or error response.

- **`logging_middleware()`** (`middleware.py`)
  - Logs incoming requests and responses.
  - Inputs: Request and response objects.
  - Outputs: Logs stored in the logging system.

#### Interaction with Other Agents:

- **Frontend Interaction**: Exposes APIs consumed by `PR-CYBR-FRONTEND-AGENT`.
- **Security Enforcement**: Works with `PR-CYBR-SECURITY-AGENT` to enforce security policies on API endpoints.

### 2. Database Integration (`data_models.py`)

#### Modules and Functions:

- **`define_models()`**
  - Defines ORM models for database tables.
  - Inputs: Database connection settings from `settings.yml`.
  - Outputs: Mapped models ready for database operations.

- **`database_session()`**
  - Manages database sessions and transactions.
  - Inputs: Database credentials.
  - Outputs: Active session for executing queries.

#### Interaction with Other Agents:

- **Data Storage**: Interacts with `PR-CYBR-DATABASE-AGENT` for data persistence.
- **Data Models**: Aligns data models with schemas defined by `PR-CYBR-DATABASE-AGENT`.

### 3. Data Processing (`data_pipelines.py`)

#### Modules and Functions:

- **`process_incoming_data()`**
  - Processes data received from external sources or other agents.
  - Inputs: Raw data payloads.
  - Outputs: Cleaned and formatted data ready for storage or analysis.

- **`schedule_tasks()`**
  - Schedules background tasks and cron jobs.
  - Inputs: Task definitions and schedules.
  - Outputs: Timely execution of backend tasks.

#### Interaction with Other Agents:

- **Data Integration**: Collaborates with `PR-CYBR-DATA-INTEGRATION-AGENT` for data ingestion and processing.
- **Performance Metrics**: Provides data to `PR-CYBR-PERFORMANCE-AGENT` for analysis.

### 4. Integration with External Services (`external_services.py`)

#### Modules and Functions:

- **`call_external_api()`**
  - Makes requests to external APIs and services.
  - Inputs: API endpoints, request parameters.
  - Outputs: Responses from external services.

- **`handle_third_party_auth()`**
  - Manages authentication with third-party services.
  - Inputs: Credentials and tokens.
  - Outputs: Authorized sessions for API calls.

#### Interaction with Other Agents:

- **Security Compliance**: Ensures external integrations meet standards set by `PR-CYBR-SECURITY-AGENT`.
- **Data Sharing**: Coordinates with `PR-CYBR-DATA-INTEGRATION-AGENT` to share data from external sources.

### 5. Inter-Agent Communication (`inter_agent_comm.py`)

#### Modules and Functions:

- **`send_message()`**
  - Sends messages or data to other agents.
  - Inputs: Destination agent ID, message payload.
  - Outputs: Confirmation of message delivery.

- **`receive_message()`**
  - Listens for incoming messages from other agents.
  - Inputs: Message queue or endpoint.
  - Outputs: Processes incoming data or commands.

#### Interaction with Other Agents:

- **Coordination**: Works with `PR-CYBR-MGMT-AGENT` to execute coordinated tasks.
- **Data Requests**: Retrieves data from `PR-CYBR-DATABASE-AGENT` or `PR-CYBR-DATA-INTEGRATION-AGENT` as needed.

## Inter-Agent Communication Mechanisms

### Communication Protocols

- **RESTful APIs**: Exposes endpoints for communication with `PR-CYBR-FRONTEND-AGENT` and other agents.
- **gRPC**: Uses for high-performance inter-agent communication where low latency is required.
- **Message Queues**: Implements message brokers like RabbitMQ or Kafka for asynchronous communication.

### Data Formats

- **JSON**: Standard format for request and response payloads.
- **Protocol Buffers**: Used with gRPC for efficient serialization.

### Authentication and Authorization

- **OAuth 2.0 / JWT**: Secures API endpoints with token-based authentication.
- **API Keys**: Manages keys for internal agent communication.

## Interaction with Specific Agents

### PR-CYBR-FRONTEND-AGENT

- **API Provider**: Supplies endpoints for data retrieval, user actions, and real-time updates.
- **Authentication Services**: Validates user credentials and manages sessions.

### PR-CYBR-SECURITY-AGENT

- **Security Audits**: Receives guidelines and updates to patch vulnerabilities.
- **Incident Reporting**: Notifies security agent of suspicious activities.

### PR-CYBR-DATABASE-AGENT

- **Data Operations**: Executes CRUD operations on the database via ORM models.
- **Schema Updates**: Coordinates on database migrations and schema changes.

## Technical Workflows

### API Request Handling Workflow

1. **Request Reception**: Incoming HTTP request received at the endpoint.
2. **Middleware Processing**: Authentication and logging middleware process the request.
3. **Route Handling**: Endpoint logic in `endpoints.py` processes the request.
4. **Business Logic Execution**: Core functions in `core_functions.py` are called as needed.
5. **Response Generation**: Data formatted and sent back to the client.

### Data Processing Workflow

1. **Data Ingestion**: Data received from frontend or other agents.
2. **Validation**: Data validated against schemas in `data_models.py`.
3. **Processing**: Data transformations and business logic applied.
4. **Storage**: Processed data saved to the database via `PR-CYBR-DATABASE-AGENT`.

## Error Handling and Logging

- **Exception Handling**: Try-except blocks used to catch and handle exceptions gracefully.
- **Logging**: Implements logging using Python's `logging` module or external services like ELK Stack.
- **Monitoring**: Integrates with monitoring tools (e.g., Prometheus) for performance and error tracking.

## Security Considerations

- **Input Validation**: Sanitizes all incoming data to prevent injection attacks.
- **Rate Limiting**: Implements rate limiting to protect against DDoS attacks.
- **Encryption**: Uses SSL/TLS for all communications, encrypts sensitive data at rest.

## Deployment and Scaling

- **Containerization**: Dockerized application for consistent deployment environments.
- **Orchestration**: Utilizes Kubernetes or Docker Swarm for container orchestration.
- **Auto-Scaling**: Configured to scale horizontally based on load metrics.

## Conclusion

The **PR-CYBR-BACKEND-AGENT** is a critical component of the PR-CYBR initiative, providing the backbone for data processing, API services, and inter-agent communication. By adhering to best practices in backend development, security, and scalability, it ensures that the PR-CYBR platform operates efficiently and securely to meet the needs of its users and stakeholders.
```


---

## OpenAI Functions

## Function List for PR-CYBR-BACKEND-AGENT

```markdown
## Function List for PR-CYBR-BACKEND-AGENT

1. **authenticate_user**: Validates user credentials and manages authentication tokens using OAuth2 and JWT for secure access.
2. **fetch_real_time_data**: Streams real-time cybersecurity data from various sources for analysis and monitoring.
3. **log_api_requests**: Captures and stores API request logs for audit trails and debugging purposes.
4. **process_large_datasets**: Implements data processing pipelines for analyzing large datasets related to cybersecurity events in real time.
5. **secure_api_endpoint**: Applies security best practices to secure sensitive endpoints from threats like SQL injection and XSS.
6. **schedule_data_cleanup**: Automates the cleanup of outdated or irrelevant data from the database to maintain performance.
7. **monitor_system_performance**: Tracks backend performance metrics and provides alerts for anomalies in system operation.
8. **integrate_external_services**: Connects to third-party APIs and services to enhance functionality and data sharing in PR-CYBR.
9. **serve_api_documentation**: Provides users and other agents with well-documented API references for ease of use and integration.
10. **chat_with_agent**: Facilitates real-time communication between users and the agent via the Agent Dashboard Chat functionality.
```