***

```markdown
# 🛡️ Agent-Dome: Autonomous Threat-Response Pipeline

Agent-Dome is an enterprise-grade, microservices-based architecture designed to simulate, ingest, and autonomously analyze network traffic for cybersecurity threats. 

It bridges the gap between **High-Performance Data Engineering** and **Generative AI**, utilizing an asynchronous FastAPI backend for log ingestion and a Retrieval-Augmented Generation (RAG) AI Agent for real-time threat intelligence analysis.

## 🏗️ System Architecture

The project is structured as a scalable monorepo divided into isolated microservices:

1. **The Attacker (Log Simulator):** A highly realistic traffic generator using `Faker` to simulate standard web traffic interspersed with malicious payloads (SQLi, XSS, Path Traversal).
2. **The Receiver (FastAPI Ingestion):** A lightweight, asynchronous API that catches thousands of logs per second using background tasks without blocking.
3. **The Ledger (PostgreSQL & Docker):** A containerized persistent storage layer where raw logs are permanently recorded via SQLAlchemy's async drivers (`asyncpg`).
4. **The Brain (AI ReAct Agent):** A dedicated AI reasoning engine using **LangChain** and **ChromaDB**. It uses RAG to fetch historical threat intelligence and analyze incoming database logs for anomalies.

## 🚀 Tech Stack

* **Backend:** Python 3.13, FastAPI, Uvicorn, Pydantic
* **Database & ORM:** PostgreSQL 15, SQLAlchemy (Async), asyncpg
* **Infrastructure:** Docker, Docker Compose
* **AI & Machine Learning:** LangChain, ChromaDB (Vector DB), Sentence-Transformers, OpenAI / Google Gemini API
* **Utilities:** Faker, Requests

## 📂 Repository Structure

```text
Agent-Dome/
├── api/                  # High-performance asynchronous ingestion engine
│   ├── main.py           # FastAPI server & background tasks
│   ├── database.py       # SQLAlchemy ORM and asyncpg connection
│   └── requirements.txt  # Isolated API dependencies
├── agent/                # AI Reasoning and RAG framework
│   ├── memory.py         # ChromaDB vector initialization & Threat Intel ingestion
│   ├── react_agent.py    # LangChain reasoning loop
│   └── requirements.txt  # Isolated AI/ML dependencies
├── scripts/              # Utility scripts and mock data generation
│   └── log_simulator.py  # Realistic web traffic simulator 
├── docker-compose.yml    # Database containerization setup
└── .gitignore            # Security and environment exclusion
```

## ⚙️ Local Setup & Installation

This project strictly uses isolated Python virtual environments to prevent dependency conflicts between the lightweight API and the heavy AI libraries.

### 1. Start the Database
Ensure Docker Desktop is running, then spin up the PostgreSQL container:
```bash
docker-compose up -d
```

### 2. Launch the Ingestion API
Navigate to the API service, initialize its environment, and start the server:
```bash
cd api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```
*The API will automatically connect to Docker and verify the database tables upon startup.*

### 3. Start the Threat Simulator
In a **new terminal**, use the API's virtual environment to run the traffic simulator:
```bash
cd api
source venv/bin/activate
cd ../scripts
python log_simulator.py
```
*You will immediately see logs flowing into the FastAPI terminal and being saved persistently to PostgreSQL.*

### 4. Initialize the AI Agent (Phase 2)
In a **new terminal**, setup the AI service and seed the Vector Database with Threat Intelligence:
```bash
cd agent
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Set your API keys in an .env file here
python memory.py
```

## 🧠 Why This Architecture?
* **Asynchronous I/O:** The ingestion API uses FastAPI's `BackgroundTasks` and `asyncpg` to ensure database writes do not bottleneck incoming web traffic.
* **Separation of Concerns:** Distinct virtual environments prevent the API's lightweight Docker image from being bloated by the Agent's massive ML libraries (like `PyTorch` or `transformers`).
* **Data-Driven AI:** Instead of relying purely on an LLM's base knowledge, the system utilizes a Vector Database (ChromaDB) to perform semantic searches against documented CVEs and threat intelligence, grounding the AI's logic in factual security data.