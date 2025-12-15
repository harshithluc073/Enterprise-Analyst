```markdown
# 📊 Enterprise Conversational Analyst

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![LlamaIndex](https://img.shields.io/badge/AI-LlamaIndex-purple?style=for-the-badge)
![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL%20%2B%20pgvector-blue?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Infrastructure-Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)

## 🚀 The Problem
In modern enterprise environments, critical business data is fragmented:
1.  **Structured Data:** Financial records, transaction logs, and vendor spend live in SQL databases.
2.  **Unstructured Data:** Strategy documents, quarterly reports, and emails live in PDFs or text files.

Standard LLMs (like ChatGPT) cannot query private SQL databases accurately (often hallucinating numbers), and standard SQL tools cannot understand the semantic context of a PDF report.

## 💡 The Solution
This project implements a **Hybrid Retrieval-Augmented Generation (RAG)** system that acts as an **Intelligent Router**. It bridges the gap between data silos by dynamically selecting the correct retrieval tool based on user intent.

*   **Qualitative Queries** (e.g., *"What is the Q3 strategy?"*) $\rightarrow$ Routed to **Vector Search** (PGVector).
*   **Quantitative Queries** (e.g., *"Total spend on AWS?"*) $\rightarrow$ Routed to **Text-to-SQL Engine**.

## 🏗️ Architecture
The system is built on the **Router-Solver Pattern**:

1.  **Ingestion Pipeline (ETL):**
    *   Parses unstructured text into embeddings using **HuggingFace (BAAI/bge-small)**.
    *   Loads structured financial data into **PostgreSQL**.
2.  **Orchestration (LlamaIndex):**
    *   Uses a **RouterQueryEngine** to classify user intent.
    *   **SQL Tool:** Generates safe, read-only SQL queries to fetch precise numbers.
    *   **Vector Tool:** Performs semantic similarity search for narrative context.
3.  **Inference:**
    *   Uses **DeepSeek-V3** (via OpenRouter) to synthesize the final answer.
4.  **Interface:**
    *   Interactive **Streamlit** dashboard with a customized dark-mode enterprise theme.

## 🛠️ Tech Stack
*   **Language:** Python 3.11
*   **Orchestration:** LlamaIndex
*   **Database:** PostgreSQL (with `pgvector` extension)
*   **LLM:** DeepSeek-V3 (via OpenRouter API)
*   **Embeddings:** HuggingFace `BAAI/bge-small-en-v1.5` (Local execution)
*   **Frontend:** Streamlit
*   **Infrastructure:** Docker & Docker Compose

## ⚡ How to Run Locally

### 1. Clone the Repository
```bash
git clone https://github.com/harshithluc073/Enterprise-Analyst.git
cd Enterprise-Analyst
```

### 2. Environment Setup
Create a `.env` file in the root directory with your credentials:

```ini
# Database Configuration
DB_HOST=127.0.0.1
DB_NAME=enterprise_db
DB_USER=admin
DB_PASS=adminpassword
DB_PORT=5433

# LLM Provider (OpenRouter)
OPENROUTER_API_KEY=sk-or-v1-your-key-here
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
LLM_MODEL=nex-agi/deepseek-v3.1-nex-n1:free
```

### 3. Start Infrastructure
Spin up the PostgreSQL vector database using Docker:
```bash
docker-compose up -d
```

### 4. Run ETL Pipeline
Ingest the synthetic financial data and strategy documents into the database:
```bash
python src/etl_pipeline.py
```

### 5. Launch the Analyst
Start the web interface:
```bash
streamlit run src/app.py
```
*Access the app at `http://localhost:8501`*

## 🧪 Example Queries
Once the app is running, try asking:
*   **SQL Test:** "What is the total amount spent on AWS?"
*   **Vector Test:** "Why did the marketing spend increase in Q3?"
*   **SQL Test:** "List all vendors in the IT department."

---
*Developed by [Harshith](https://github.com/harshithluc073)*
```