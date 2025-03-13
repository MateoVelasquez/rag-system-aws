# rag-system-aws

![Static Badge](https://img.shields.io/badge/v3.13-%233776AB?logo=Python&logoColor=%233776AB&label=Python&labelColor=white)
![Static Badge](https://img.shields.io/badge/fastapi-v0.115.8-%23009688?logo=FastAPI)
![Static Badge](https://img.shields.io/badge/OpenSearch-2.7-blue?logo=opensearch&logoColor=%23005EB8&labelColor=white)
![Static Badge](https://img.shields.io/badge/Models-gray?logo=Ollama&logoColor=%23000000&label=Ollama&labelColor=white)
![Static Badge](https://img.shields.io/badge/Docker-Images%20%7C%20Compose%20-%232496ED?logo=docker)
![GitHub License](https://img.shields.io/github/license/MateoVelasquez/rag-system-aws)
![GitHub watchers](https://img.shields.io/github/watchers/MateoVelasquez/rag-system-aws)
![GitHub forks](https://img.shields.io/github/forks/MateoVelasquez/rag-system-aws)

### Table of Contents

- [About the project](#about-the-project)
    - [Built with](#built-with)
    - [RAG: Tech Specs](#rag-tech-specs)
- [Getting started](#getting-started)
    - [Installation](#installation)
    - [Folder structure](#folder-structure)
- [Deployment](#deployment)
    - [Local Deployment](#local-deployment)
    - [Docker Deployment](#docker-deployment)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)
- [Acknowledgments](#acknowledgments)

# About the project

This project is designed as a study on Retrieval-Augmented Generation (RAG), focusing on leveraging AWS infrastructure to build an intelligent knowledge retrieval system. The system indexes Wikipedia articles, retrieves relevant data, and generates contextual responses using the Llama 3 language model.

The key objectives of this project are:
- Efficiently index and retrieve structured data from Wikipedia.
- Implement a semantic search mechanism with OpenSearch.
- Generate responses using an advanced LLM (Llama 3).
- Deploy the system as a REST API using AWS Lambda.
- Ensure scalability and reliability using Docker and EC2.

![chat bot](/docs/rag_system_chat.png)

## Built with

The Rag System was built with the following technologies:

- [OpenSearch](https://opensearch.org/): Stores and indexes text embeddings for semantic search.
- [Llama3](https://www.llama.com/): An open-source LLM used to generate responses.
- [AWS Lambda](https://aws.amazon.com/es/pm/lambda/#Learn_more_about_building_with_AWS_Lambda): Serves as the API endpoint handling user queries.
- [AWS S3](https://aws.amazon.com/es/s3/?nc2=h_ql_prod_st_s3): ASGI server used to run the FastAPI application.
- [Docker](https://www.docker.com/) and [EC2](https://aws.amazon.com/es/ec2/): Used for deployment and containerized execution.

These technologies were chosen to provide a robust, scalable, and efficient solution.

## RAG Tech Specs

For more detailed specifications of the solution, see the file [RAG_Specs](./docs/RAG_Specs.md).

![architecture](./docs/rag_system.png)

# Getting Started

## Installation

To install the Rag System in your machine, follow these steps:

1. Clone this repository to your local machine:
    ```bash
    git clone https://github.com/MateoVelasquez/rag-system-aws
    ```
2. Navigate to the project directory:
    ```bash
    cd rag-system-aws
    ```
3. You can install the Rag System AWS using pip.

    Using pip:
    ```bash
    pip install .
    ```
4. Set up your .env variables:
    ```bash
    cp .env_template .env
    ```
    Configure the following required environment variables in your `.env` file:
    - `ENV_STATE`: Set to 'dev' or 'localdev' to determine the LLM model
    - AWS credentials for OpenSearch access:
        - `AWS_ACCESS_KEY_ID`
        - `AWS_SECRET_ACCESS_KEY`
        - `AWS_DEFAULT_REGION`
    - OpenSearch connection details:
        - `AWS_OPENSEARCH_HOST`
        - `AWS_OPENSEARCH_USER`
        - `AWS_OPENSEARCH_PASSWORD`

5. Install Ollama:
    ```bash
    # For Linux
    curl -fsSL https://ollama.com/install.sh | sh
    # For MacOS
    brew install ollama
    # For Windows
    # Download from https://ollama.com/download/windows
    ```
    
    After installation, pull the required model based on your `ENV_STATE`:
    ```bash
    # For ENV_STATE=dev
    ollama pull qwen2.5:0.5b
    # For ENV_STATE=localdev
    ollama pull llama3
    ```

## Folder structure
The project directory structure is organized as follows:
```
rag-system-aws/
┣ app/
┃ ┣ api/
┃ ┃ ┣ __init__.py
┃ ┃ ┣ routes.py
┃ ┃ ┗ schemas.py
┃ ┣ services/
┃ ┃ ┣ __init__.py
┃ ┃ ┣ embedding.py
┃ ┃ ┣ llm.py
┃ ┃ ┣ rag_pipeline.py
┃ ┃ ┣ retrieval.py
┃ ┃ ┣ s3.py
┃ ┃ ┗ wikipedia.py
┃ ┣ utils/
┃ ┃ ┣ __init__.py
┃ ┃ ┗ load_initial_data.py
┃ ┣ __init__.py
┃ ┣ config.py
┃ ┗ main.py
┣ scripts/
┃ ┣ docs_to_os_index.py
┣ .env_template
┣ .gitignore
┣ LICENSE
┣ README.md
┣ dockerfile
┣ pyproject.toml
┣ requirements.txt
┗ ruff.toml
```
The application follows a **FastAPI-based architecture**, structured into distinct layers to ensure maintainability and scalability:

- **`api/`**: Defines FastAPI endpoints and request/response schemas.  
- **`services/`**: Implements core business logic, including retrievers and managers that interact with external systems.  
- **`utils/`**: Provides utility functions, including routines for loading initial data into S3 and OpenSearch.  
- **`scripts/`**: Contains scripts designed for execution in **AWS Lambda**, triggered by S3 file uploads.  
- **`main.py`**: The application's entry point, responsible for initializing FastAPI and routing requests.  

This modular structure ensures **clear separation of concerns**, improving maintainability, scalability, and ease of extension. 🚀  

# Deployment

## Local Deployment:
To run the Rag System on your local machine, follow these steps:

1. Navigate to the project directory:
    ```bash
    cd rag-system-aws
    ```

2. Run the FastAPI application using Uvicorn:

    With uvicorn:
    ```bash
    uvicorn app.main:app --reload
    ```

**Note:** The application requires a running Ollama instance with the appropriate model (qwen2.5:0.5b for dev or llama3 for localdev). Ensure Ollama is running before starting the application:
```bash
ollama serve
```

## Docker Deployment:

1. Navigate to the project directory:
    ```bash
    cd rag-system-aws
    ```

2. Build Docker image:

    ```bash
    docker build -t rag-system-img .
    ```

3. Run Docker image:
    ```bash
    docker run -p 8000:8000 --name rag-system rag-system-img
    ```

Docker won't detect Ollama by default since it runs in an isolated network. There are two ways to connect Docker to Ollama:

1. Using host network (recommended for development):
    ```bash
    docker run --network=host -p 8000:8000 --name rag-system rag-system-img
    ```

2. Using Docker Compose with a dedicated network (recommended for production):
    Create a docker-compose.yml file that defines both services and their networking. This approach is pending implementation.

# Usage  

Access the RAG System at [http://localhost:8000](http://localhost:8000) using your web browser or an API testing tool.
The RAG System provides a simple chat interface where you can inquire about topics related to:  

- **APIs:** FastAPI, ASGI, RESTful APIs, OAuth, JSON Schema, Swagger, OpenAPI, CORS.  
- **Amazon Web Services:** AWS Lambda, Amazon S3, Amazon DynamoDB, Amazon EC2, Amazon SageMaker, OpenSearch.  
- **Artificial Intelligence & Machine Learning:** Machine Learning, Deep Learning, NLP, Transformer architectures.  
- **Models & Tools:** GPT, LLaMA, Mistral AI, Hugging Face, Vector Databases, Embeddings.  

You can also interact with the available endpoints at [http://localhost:8000/docs](http://localhost:8000/docs) using tools like **cURL, Postman,** or any HTTP client library in your preferred programming language.  

> **Note:** The bot may take some time to respond as it is not a high-powered model.

# Contributing
Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement". Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (git checkout -b feature/1. AmazingFeature)
3. Commit your Changes (git commit -m 'Add some AmazingFeature')
4. Push to the Branch (git push origin feature/AmazingFeature)
5. Open a Pull Request

# License

Distributed under GNU License. See [LICENSE](LICENSE) for more information.

# Contact

If you have any questions, feedback, or suggestions, feel free to reach out to us:

- **Mateo Velásquez:** mateo10velasquez@hotmail.com
- **Project Link:** https://github.com/MateoVelasquez/rag-system-aws

We appreciate your interest and value your input!
