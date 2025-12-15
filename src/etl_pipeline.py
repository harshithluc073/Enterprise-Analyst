import os
import pandas as pd
from datetime import date
from dotenv import load_dotenv
from sqlalchemy import text
from llama_index.core import VectorStoreIndex, Document, StorageContext
from llama_index.vector_stores.postgres import PGVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding

from db_config import engine, SessionLocal
from models import Base, FinancialRecord

load_dotenv()

# --- 1. SETUP & CLEANUP ---
print("⚙️  Starting ETL Pipeline...")

# Drop existing tables to start fresh (for development only)
Base.metadata.drop_all(bind=engine)
# Create SQL tables
Base.metadata.create_all(bind=engine)

# --- 2. INGEST SQL DATA (Quantitative) ---
print("📊 Ingesting Structured SQL Data...")
session = SessionLocal()

# Synthetic Financial Data
financial_data = [
    FinancialRecord(date=date(2023, 10, 1), department="IT", category="Software", vendor="AWS", amount=15400.00, description="Cloud Infrastructure Q3"),
    FinancialRecord(date=date(2023, 10, 5), department="Marketing", category="Ads", vendor="Google Ads", amount=4500.50, description="Q3 Campaign"),
    FinancialRecord(date=date(2023, 11, 1), department="IT", category="Software", vendor="AWS", amount=16200.00, description="Cloud Infrastructure Q4 Start"),
    FinancialRecord(date=date(2023, 11, 15), department="HR", category="Training", vendor="Udemy", amount=1200.00, description="Python Training"),
    FinancialRecord(date=date(2023, 12, 1), department="IT", category="Hardware", vendor="Dell", amount=8500.00, description="New Laptops"),
]

session.add_all(financial_data)
session.commit()
print(f"✅ Inserted {len(financial_data)} financial records into SQL.")

# --- 3. INGEST VECTOR DATA (Qualitative) ---
print("🧠 Ingesting Unstructured Text Data...")

# Synthetic Strategic Documents
documents = [
    Document(text="The Q3 Cloud Strategy focused on scaling our AWS infrastructure to handle the Black Friday traffic surge. This resulted in a 10% increase in spend compared to Q2."),
    Document(text="Marketing spend for Q4 is projected to decrease as we shift from paid ads to organic social media growth."),
    Document(text="The IT Hardware budget was utilized to upgrade developer laptops. We chose Dell over Apple to maintain compatibility with Windows legacy systems.")
]

# Setup PGVector
vector_store = PGVectorStore.from_params(
    database=os.getenv("DB_NAME"),
    host=os.getenv("DB_HOST"),
    password=os.getenv("DB_PASS"),
    port=os.getenv("DB_PORT"),
    user=os.getenv("DB_USER"),
    table_name="strategic_docs",
    embed_dim=1536  # OpenAI embedding dimension
)

storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)

print("✅ Indexed strategic documents into PGVector.")
print("🚀 ETL Pipeline Completed Successfully.")