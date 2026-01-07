import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from config.config import client



# 2. Charger ce fichier spécifique

load_dotenv()

tavily_key = os.getenv("TAVILY_API_KEY")

from langchain_groq import ChatGroq  # <-- CORRECTION 2 : Import nécessaire pour Groq
from langchain_core.messages import HumanMessage, AnyMessage, SystemMessage, ToolMessage
from langchain_community.tools import TavilySearchResults
from langchain_tavily import TavilySearch

from langgraph.graph import StateGraph,END
from typing import TypedDict, Annotated 
import operator

from IPython.display import Image

# Initialisation de l’outil de recherche Tavily
tool = TavilySearch(max_results=4, tavily_api_key=tavily_key) #augmentation du nombre de résultats
#print(type(tool))
#print(tool.name)

# Définition de l’état de l’agent
class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
# Définition de l’agent
class Agent:

    def __init__(self, model, tools, system=""):
        self.system = system
        graph = StateGraph(AgentState)
        graph.add_node("llm", self.call_llm)
        graph.add_node("action", self.take_action)
        graph.add_conditional_edges(
            "llm",
            self.exists_action,
            {True: "action", False: END}
        )
        graph.add_edge("action", "llm")
        graph.set_entry_point("llm")
        self.graph = graph.compile()
        self.tools = {t.name: t for t in tools}
        self.model = model.bind_tools(tools)
# Méthode pour vérifier l’existence d’une action
    def exists_action(self, state: AgentState):
        result = state['messages'][-1]
        return len(result.tool_calls) > 0
# Appel du LLM
    def call_llm(self, state: AgentState):
        messages = state['messages']
        if self.system:
            messages = [SystemMessage(content=self.system)] + messages
        message = self.model.invoke(messages)
        return {'messages': [message]}
# Prise d’action en fonction des appels d’outils
    def take_action(self, state: AgentState):
        tool_calls = state['messages'][-1].tool_calls
        results = []
        for t in tool_calls:
            print(f"Calling: {t}")
            if not t['name'] in self.tools:      # check for bad tool name from LLM
                print("\n ....bad tool name....")
                result = "bad tool name, retry"  # instruct LLM to retry if bad
            else:
                result = self.tools[t['name']].invoke(t['args'])
            results.append(ToolMessage(tool_call_id=t['id'], name=t['name'], content=str(result)))
        print("Back to the model!")
        return {'messages': results}

# Exemple d’utilisation de l’agent avec l’outil de recherche
prompt = """You are a smart research assistant. Use the search engine to look up information. \
You are allowed to make multiple calls (either together or in sequence). \
Only look up information when you are sure of what you want. \
If you need to look up some information before asking a follow up question, you are allowed to do that!
"""
# Initialisation de l’agent avec le modèle Groq
print("--- TEST GROQ ---")
model = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
abot = Agent(model, [tool], system=prompt)
# 1. Générer l'image via l'API Mermaid (plus compatible)
try:
    png_bytes = abot.graph.get_graph().draw_mermaid_png()
    
    # 2. Sauvegarder dans un fichier
    with open("mon_agent_graph.png", "wb") as f:
        f.write(png_bytes)
    
    print("✅ Le schéma du graphe a été sauvegardé sous 'mon_agent_graph.png'")

except Exception as e:
    print(f"⚠️ Impossible de dessiner le graphe : {e}")

messages = [HumanMessage(content="What is the weather in sf?")]
result = abot.graph.invoke({"messages": messages})

result

result['messages'][-1].content

messages = [HumanMessage(content="What is the weather in SF and LA?")]
result = abot.graph.invoke({"messages": messages})

result['messages'][-1].content

query = "Who won the super bowl in 2024? In what state is the winning team headquarters located? \
What is the GDP of that state? Answer each question." 
messages = [HumanMessage(content=query)]

model = ChatGroq(model="llama-3.3-70b-versatile")
abot = Agent(model, [tool], system=prompt)
result = abot.graph.invoke({"messages": messages})

print(result['messages'][-1].content)