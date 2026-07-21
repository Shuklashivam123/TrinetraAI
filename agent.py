import os, sqlite3
from pathlib import Path

from dotenv import load_dotenv
import certifi

load_dotenv()

os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph, START, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.sqlite import SqliteSaver
from tools import tools
from langchain_groq import ChatGroq


Path("data").mkdir(exist_ok=True)

DEFAULT_MODEL=os.getenv("GROQ_MODEL","openai/gpt-oss-120b")


ALLOWED_MODELS = {
    "gemini-2.5-flash",
    "gemini-2.5-pro",
    "gemini-2.5-flash-lite", # Included the lite version if needed
    "gemini-1.5-flash",      # Kept for fallback compatibility 
    "gemini-1.5-pro"
}

SYSTEM_PROMPT="""
Hey you are a very helpful AI Assistant named TrinetraAI made by Shivam Shukla. Always remember the name of the creator who created you!
But you should remember that all the answers should be given in some funny ways, always use emojis while giving answers so that users feel nice...

Always start every response with:

"Jai Mahakal 🙏
Hi! I am TrinetraAI, your AI assistant."

Then continue with the rest of the response naturally.

You can perform tasks such as :
1. Answer normal day to day questions
2. Use tools whenever required
3. Can search via uploaded documents and provide answers
4. You can recall memory when needed
5. Remember important info using the memory tool

Rules:
- Use Tavily Search for latest, current, recent, live, or time-sensitive information.
- Use search_uploaded_documents for questions about uploaded documents.
- Use remember_this when the user asks to save or remember something.
- Use recall_memory when the user asks about saved memories or preferences.
- Use calculator for math.
- If using web search, summarize the results and mention the answer is based on web search.
- Be clear, concise, and helpful.
"""


def normalize_model_name(model_name:str|None)->str:
    if not model_name:
        return DEFAULT_MODEL
    model_name=model_name.strip()

    if model_name not in ALLOWED_MODELS:
        return DEFAULT_MODEL

    return model_name



def build_agent(model_name:str):
    """
    Build one LangGraph agent for a selected Gemini model.
    """
    selected_model=normalize_model_name(model_name)

    llm=ChatGroq(model=selected_model,temperature=0.5,streaming=True)

    llm_with_tools=llm.bind_tools(tools)

    def chatbot_node(state:MessagesState):
        messages=[SystemMessage(content=SYSTEM_PROMPT)]+state['messages']

        response=llm_with_tools.invoke(messages)

        return {
            "messages":[response]
        }

    tool_node=ToolNode(tools)

    workflow=StateGraph(MessagesState)

    workflow.add_node("chatbot",chatbot_node)
    workflow.add_node("tools",tool_node)

    workflow.add_edge(START,"chatbot")
    workflow.add_conditional_edges("chatbot",tools_condition)
    workflow.add_edge("tools","chatbot")

    conn=sqlite3.connect(
        "data/langgraph_checkpoints.sqlite",
        check_same_thread=False
    )

    checkpointer=SqliteSaver(conn)

    return workflow.compile(checkpointer=checkpointer)


_AGENT_CACHE={}

def get_agent(model_name:str|None=None):
    """
    Return cached LangGraph agent for selected model.
    If not created yet, create it once and reuse it.
    """

    selected_model=normalize_model_name(model_name)

    if selected_model not in _AGENT_CACHE:
        _AGENT_CACHE[selected_model]=build_agent(selected_model)

    return _AGENT_CACHE[selected_model]