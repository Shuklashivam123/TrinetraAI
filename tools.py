import math
from dotenv import load_dotenv
load_dotenv()

from langchain_tavily import TavilySearch
from langchain_core.tools import tool

from langchain.tools import tool
import math

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

