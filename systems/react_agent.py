import os
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
import operator
from tools.calculator import Calculator
from tools.wikipedia import Wikipedia
from dotenv import load_dotenv
load_dotenv()


@tool
def calculator(expression: str) -> str:
    """
    Evaluate a mathematical expression and return the result as a string.
    
    Uses SymPy's symbolic math engine to safely parse and evaluate the
    expression. Supports arithmetic operations, algebraic expressions,
    and common mathematical functions.
    
    Args:
        expression: A string containing the mathematical expression to evaluate.
            Examples: "2 + 2", "sin(pi/4)", "x**2 + 3*x", "sqrt(16) + 5"
    
    Returns:
        The computed result as a string. Returns an error message string
        if the expression cannot be parsed or evaluated.
    """  
    calc = Calculator()
    response = calc.run(expression) 
    return response      

@tool
def wikipedia_search(search_term: str) -> str:
    """
    Search Wikipedia and return a summary of the article.
    
    Retrieves the first 1020 characters of the Wikipedia article summary
    for the given search term. Automatically resolves disambiguation pages
    by selecting the first suggested option.
    
    Args:
        search_term: The topic or keyword to search for on Wikipedia.
            Can be a person, place, concept, event, or any encyclopedic topic.
            Examples: "Python programming language", "Albert Einstein",
            "Machine learning", "Eiffel Tower"
    
    Returns:
        A string containing the article summary (max 1020 characters).
        If the term is ambiguous, returns the summary for the most relevant
        option. Returns an error message string if the search fails or
        no article is found.
    """  
    wiki = Wikipedia()
    response = wiki.run(search_term) 
    return response

class AgentState(TypedDict):
    messages: Annotated[list, operator.add]
    trace: Annotated[list, operator.add]


class ReActAgents:
    def __init__(self, model_name: str, api_key: str):   
        self.tools = [calculator, wikipedia_search]
        self.llm = ChatGroq(
            model= "llama-3.1-8b-instant",        
            temperature=0,  
            api_key= os.getenv("COMPLETE_RUN")
        )
        
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        self.app = self._build_graph()

    def _agent_node(self, state: AgentState) -> AgentState:
        messages = state["messages"]
        response = self.llm_with_tools.invoke(messages)
        
        trace_entry = {
            "thought": response.content,
            "tool_calls": response.tool_calls
        }
        return {
            "messages": [response],
            "trace": [trace_entry]
        }

    def _should_continue(self, state: AgentState) -> str:
        last_message = state["messages"][-1]
        if last_message.tool_calls:  
            return "tools"
        return END

    def _build_graph(self) -> StateGraph:
        tool_node = ToolNode(self.tools)
        
        graph = StateGraph(AgentState)
        
        # add nodes — fill in the method calls
        graph.add_node("agent", self._agent_node)
        graph.add_node("tools", tool_node)
        
        # add edges — fill in
        graph.set_entry_point("agent")
        graph.add_conditional_edges("agent", self._should_continue)
        graph.add_edge("tools", "agent")
        
        return graph.compile()

    def run(self, question: str) -> dict:
        system_prompt = """You are a research assistant.
        Think step by step before acting.
        Always show your reasoning before using a tool.
        Format your thoughts as:
        Thought: [your reasoning]
        Action: [tool to use]"""
        
        initial_state = {
            "messages": [
                SystemMessage(content=system_prompt),
                HumanMessage(content=question)
            ],
            "trace": []
        }
        
        result = self.app.invoke(initial_state)
        return {
            "final_answer": result["messages"][-1].content,
            "trace": result["trace"]
        }


