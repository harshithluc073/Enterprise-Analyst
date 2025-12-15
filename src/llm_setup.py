import os
from dotenv import load_dotenv
from llama_index.llms.openai_like import OpenAILike
from llama_index.core import Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

load_dotenv()

def init_settings():
    """
    Initializes the global LlamaIndex settings with:
    1. HuggingFace for Embeddings (Local)
    2. DeepSeek (via OpenRouter) for Generation
    """
    
    # 1. Setup Embedding Model (Same as ETL)
    print("⚙️  Loading Embedding Model...")
    Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

    # 2. Setup LLM (DeepSeek via OpenRouter)
    print("🤖 Connecting to DeepSeek via OpenRouter...")
    Settings.llm = OpenAILike(
        model=os.getenv("LLM_MODEL"),
        api_base=os.getenv("OPENROUTER_BASE_URL"),
        api_key=os.getenv("OPENROUTER_API_KEY"),
        is_chat_model=True,
        context_window=32000,
        max_tokens=512,
        temperature=0.1, # Low temperature for factual accuracy
    )
    
    print("✅ AI Core Initialized.")

if __name__ == "__main__":
    # Test the connection independently
    init_settings()
    response = Settings.llm.complete("Hello, are you ready to analyze financial data?")
    print(f"\n🤖 Model Response: {response}")