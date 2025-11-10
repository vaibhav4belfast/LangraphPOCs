import os
from typing import TypedDict, List
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv # used to store secret stuff like API keys or configuration values

load_dotenv()

class AgentState(TypedDict):
    messages: List[HumanMessage]

llm = ChatOpenAI(model="gpt-4o-mini")

def process(state: AgentState) -> AgentState:
    print(f"Vaibhav: {state['messages']}")
    response = llm.invoke(state["messages"])
    print(f"Sujata: {state['messages']}")
    print(f"\nAI: {response.content}")
    print(f"Agarwal: {state}")
    return state

graph = StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END) 
agent = graph.compile()

user_input = input("Enter: ")
while user_input != "exit":
    myResult = agent.invoke({"messages": [HumanMessage(content=user_input)]})
    print(f"Sujata: {myResult}")
    user_input = input("Enter: ")