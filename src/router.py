from llama_index.core.tools import QueryEngineTool
from llama_index.core.query_engine import RouterQueryEngine
from llama_index.core.selectors import LLMSingleSelector
from engines import get_sql_engine, get_vector_engine
from llm_setup import init_settings

def get_router_engine():
    """
    Constructs a Router Engine that selects between SQL and Vector tools
    based on the user's question.
    """
    # Ensure settings are loaded
    init_settings()

    # 1. Prepare the SQL Tool (The "Math" Brain)
    sql_tool = QueryEngineTool.from_defaults(
        query_engine=get_sql_engine(),
        description=(
            "Useful for translating a natural language query into a SQL query over "
            "a table containing: financial_records, containing date, department, category, vendor, amount. "
            "Use this for questions about money, spending, costs, or totals."
        ),
    )

    # 2. Prepare the Vector Tool (The "Text" Brain)
    vector_tool = QueryEngineTool.from_defaults(
        query_engine=get_vector_engine(),
        description=(
            "Useful for answering semantic questions about business strategy, "
            "decisions, quarterly reports, and qualitative rationale. "
            "Use this for questions asking 'Why', 'How', or for summaries."
        ),
    )

    # 3. Create the Router
    # LLMSingleSelector uses the LLM to pick the best tool
    router_engine = RouterQueryEngine(
        selector=LLMSingleSelector.from_defaults(),
        query_engine_tools=[sql_tool, vector_tool],
        verbose=True # Prints which tool was selected in the console
    )

    return router_engine