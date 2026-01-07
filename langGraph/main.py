from config.config import client

from langgraph.graph import StateGraph, END_NODE
from typing import TypedDict, Annotated
import operator
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, ToolMessage
from langchain_groq import GroqChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults