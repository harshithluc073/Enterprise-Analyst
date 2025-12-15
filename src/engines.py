import os
from sqlalchemy import text
from llama_index.core import SQLDatabase, VectorStoreIndex
from llama_index.core.query_engine import NLSQLTableQueryEngine
from llama_index.vector_stores.postgres import PGVectorStore
from llama_index.core import StorageContext

from db_config import engine
from llm_setup import init_settings

# Initialize settings (Embeddings + LLM)
init_settings()

def get_sql_engine():
    """
    Creates an engine that can translate natural language to SQL
    and execute it against the 'financial_records' table.
    """
    # 1. Inspect the specific table
    sql_database = SQLDatabase(engine, include_tables=["financial_records"])
    
    # 2. Create the engine
    query_engine = NLSQLTableQueryEngine(
        sql_database=sql_database,
        tables=["financial_records"],
    )
    return query_engine

def get_vector_engine():
    """
    Creates an engine that can perform semantic search
    on the 'strategic_docs' table in Postgres.
    """
    # 1. Connect to PGVector
    vector_store = PGVectorStore.from_params(
        database=os.getenv("DB_NAME"),
        host=os.getenv("DB_HOST"),
        password=os.getenv("DB_PASS"),
        port=os.getenv("DB_PORT"),
        user=os.getenv("DB_USER"),
        table_name="strategic_docs",
        embed_dim=384 # Must match the BAAI model
    )
    
    # 2. Load Index
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store, storage_context=storage_context)
    
    # 3. Return Engine
    return index.as_query_engine()

# Simple Test
if __name__ == "__main__":
    print("\n--- Testing SQL Engine ---")
    sql_engine = get_sql_engine()
    response = sql_engine.query("What is the total amount spent on AWS?")
    print(f"Q: Total AWS Spend?\nA: {response}\n")

    print("\n--- Testing Vector Engine ---")
    vector_engine = get_vector_engine()
    response = vector_engine.query("What is the strategy for Q3?")
    print(f"Q: Q3 Strategy?\nA: {response}\n")