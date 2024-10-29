# Tư Tưởng Hồ Chí Minh Chatbot

This repository contains a chatbot project designed to assist users in learning about **Tư tưởng Hồ Chí Minh** (Ho Chi Minh's ideology). The chatbot provides interactive features for both **learning** and **quiz-based assessments** to test users' knowledge on the subject.

## Features

- **Learn**: Users can explore key concepts and philosophies related to Hồ Chí Minh's ideology.
- **Quiz**: Test your knowledge with interactive multiple-choice quizzes based on the content.

## Prerequisites

Make sure the following software is installed on your system:
- Docker
- Docker Compose

## Getting Started

### 1. Prepare environment variables

The project requires specific environment variables for services such as database connection, authentication, and external APIs. First, create a `.env` file in the `app/` directory:

```bash
cd app/
touch .env
```

Add the following content to the `.env` file, replacing the placeholders with your actual values:

```
ASTRADB_APPLICATION_TOKEN=AstraCS:<your-astradb-token>
ASTRADB_API_URL=https://<your-endpoint>.apps.astra.datastax.com
EMBEDDINGS_TOKENS=<your-embedding-tokens>
POSTGRES_DATABASE_URL=<your-postgres-url>
CHAINLIT_AUTH_SECRET=<your-chainlit-auth-secret>
OPENAI_API_KEY=sk-proj-<your-openai-api-key>
CHAINLIT_CUSTOM_AUTH=true
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
LANGCHAIN_API_KEY=<your-langchain-api-key>
LANGCHAIN_PROJECT="TTHCM"
OAUTH_GOOGLE_CLIENT_ID=<your-google-client-id>
OAUTH_GOOGLE_CLIENT_SECRET=<your-google-client-secret>
CHAINLIT_URL=<your-domain-name>
```

### 2. Build and run the project

Once the `.env` file is ready, use Docker Compose to build and run the chatbot:

```bash
docker compose up -d --build
```

This command will build and run the required services in the background.

### 3. Access the chatbot

After the services have started, you can access the chatbot via the URL specified in the `CHAINLIT_URL` environment variable.

## Environment Variables

- `ASTRADB_APPLICATION_TOKEN`: Token for connecting to AstraDB.
- `ASTRADB_API_URL`: AstraDB API endpoint URL.
- `EMBEDDINGS_TOKENS`: Tokens for embeddings services.
- `POSTGRES_DATABASE_URL`: PostgreSQL database URL.
- `CHAINLIT_AUTH_SECRET`: Secret for Chainlit authentication.
- `OPENAI_API_KEY`: API key for OpenAI services.
- `CHAINLIT_CUSTOM_AUTH`: Set to `true` for custom Chainlit authentication.
- `LANGCHAIN_TRACING_V2`: Enable LangChain tracing.
- `LANGCHAIN_ENDPOINT`: LangChain API URL.
- `LANGCHAIN_API_KEY`: API key for LangChain.
- `LANGCHAIN_PROJECT`: LangChain project name, e.g., "TTHCM".
- `OAUTH_GOOGLE_CLIENT_ID`: Google OAuth client ID for user authentication.
- `OAUTH_GOOGLE_CLIENT_SECRET`: Google OAuth client secret.
- `CHAINLIT_URL`: The URL where the chatbot will be accessible.

## Notes

- Ensure the environment variables are set correctly for the chatbot to function.
- To stop the services, run:

```bash
docker compose down
```

## License

This project is licensed under the [GNU Affero General Public License v3.0](LICENSE).
