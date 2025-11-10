from typing import Annotated, Sequence, TypedDict
from dotenv import load_dotenv  
from langchain_core.messages import BaseMessage # The foundational class for all message types in LangGraph
from langchain_core.messages import ToolMessage # Passes data back to LLM after it calls a tool such as the content and the tool_call_id
from langchain_core.messages import SystemMessage # Message for providing instructions to the LLM
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode


load_dotenv()

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

@tool
def add(a: int, b:int):
    """This is an addition function that adds 2 numbers together"""
    print("<<<<<<Vaibhav I am going to do Addition>>>>>>")
    return a + b 

@tool
def subtract(a: int, b: int):
    """Subtraction function"""
    print("<<<<<<<<<<<<Vaibhav I am going to do Subtraction>>>>>>>>")
    return a - b

@tool
def multiply(a: int, b: int):
    """Multiplication function"""
    print("<<<<<<<<<<<<Vaibhav I am going to do Multiplication>>>>>>>>>>>")
    return a * b

tools = [add, subtract, multiply]

model = ChatOpenAI(model = "gpt-4o-mini").bind_tools(tools)


def model_call(state:AgentState) -> AgentState:
    print(f"Sujata1: {state}")
    system_prompt = SystemMessage(content=
        "You are my AI assistant, please answer my query to the best of your ability."
    )
    response = model.invoke([system_prompt] + state["messages"])
    print(f"<<<<<Agarwal:>>>>> {state}")
    print(f"<<<<<<Sujata2:>>>>> {response}")
    return {"messages": [response]}


def should_continue(state: AgentState): 
    print(f"<<<<<<<<<Avika>>>>> : {state}")
    messages = state["messages"]
    print(f"<<<<<<<<<Rani>>>>>>>>>>  : {messages}")
    last_message = messages[-1]
    print(f"<<<<<LastMessage>>>>>>> =  : {last_message}")
    if not last_message.tool_calls: 
        print(f"<<<<<<InsideIF >>>>>>>>>>  : {last_message.tool_calls}")
        return "end"
    else:
        print(f"<<<<<<<<InsideElse>>>>>>>>>   : {last_message.tool_calls}")
        return "continue"
    
graph = StateGraph(AgentState)
graph.add_node("our_agent", model_call)


tool_node = ToolNode(tools=tools)
graph.add_node("tools", tool_node)

graph.set_entry_point("our_agent")

graph.add_conditional_edges(
    "our_agent",
    should_continue,
    {
        "continue": "tools",
        "end": END,
    },
)

graph.add_edge("tools", "our_agent")

app = graph.compile()

def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()

inputs = {"messages": [("user", "Add 40 + 12 and then multiply the result by 6. Also answer in one single word that what is the capital of India")]}
print("Going to print GOODY GOODY MESSAGE")
print_stream(app.stream(inputs, stream_mode="values"))
print("ENDING GOODY GOODY MESSAGE")