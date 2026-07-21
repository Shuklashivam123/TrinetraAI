import math
from dotenv import load_dotenv
load_dotenv()

from langchain_tavily import TavilySearch
from langchain_core.tools import tool

from langchain.tools import tool
import math

# database.py
from database import save_memory,search_memory
from rag import retrieve_from_rag


CURRENT_THREAD_ID="deafault"

def set_current_thread_id(thread_id:str):
    global CURRENT_THREAD_ID
    CURRENT_THREAD_ID=thread_id



# Creating Tools
# 1)
web_search=TavilySearch(
    max_results=5,
    topic="general",
    search_depth="advanced"
)

#2)
@tool
def calculator(expression: str) -> str:
    """
    Tool Description:
    - Used for simple mathematical calculations.
    - The input should be a valid Python math expression.
    - Examples:
        2 + 2
        math.sqrt(16)
        10 * 5
    """

    try:
        # Dictionary containing only the functions/modules
        # that we want to allow inside eval().
        # This prevents access to unwanted Python functions.
        allowed = {
            "math": math,      # Allows math.sqrt(), math.sin(), math.pi, etc.
            "abs": abs,        # Absolute value
            "round": round,    # Round numbers
            "min": min,        # Find minimum value
            "max": max,        # Find maximum value
            "sum": sum,        # Sum of iterable (e.g., sum([1,2,3]))
            "pow": pow,        # Power calculation (pow(2,3))
            "len": len,        # Length of a list/string, etc.
        }

        # eval() evaluates the expression entered by the user.
        #
        # First argument:
        #   expression -> User's math expression.
        #
        # Second argument:
        #   {"__builtins__": {}}
        #   Disables access to Python built-in functions
        #   like open(), exec(), eval(), __import__(), etc.
        #
        # Third argument:
        #   allowed
        #   Only the names present in this dictionary
        #   can be used inside the expression.
        result = eval(expression, {"__builtins__": {}}, allowed)

        # Convert the result into string because LangChain tools
        # generally return text.
        return str(result)

    except Exception as e:
        # If the expression is invalid, return the error message
        # instead of crashing the program.
        return f"Calculation error: {str(e)}"


@tool
def remember_this(memory:str)->str:
    """
    Save an important user preference or fact into long-term memory.
    Use this when the user asks you to remember something.
    """

    return save_memory(
        thread_id=CURRENT_THREAD_ID,
        memory=memory
    )


@tool
def recall_memory(query:str)->str:
    """
    Recall saved long-term memories about the user or this conversation.
    """

    return search_memory(
       thread_id= CURRENT_THREAD_ID,
       query=query
    )

# RAG tool from rag.py

def search_uploaded_documents(query:str)->str:
    """
    Search uploaded documents for relevant information.
    Use this when the user asks about uploaded PDFs, DOCX, TXT, notes, files, or documents.
    """

    return retrieve_from_rag(
        query=query,
        thread_id=CURRENT_THREAD_ID
    )




tools=[calculator,search_uploaded_documents,remember_this,recall_memory,web_search]