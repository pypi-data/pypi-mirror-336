# Datagusto SDK for Python

This is the official Python SDK for Datagusto AI platform.

## Installation

You can install the package using pip:

```bash
pip install datagusto-sdk
```

## Quick Start

```python
import os
from datagusto.callback import LangchainCallbackHandler

# Initialize the handler
os.environ["DATAGUSTO_SECRET_KEY"] = "sk-dg-xxxxx"
handler = LangchainCallbackHandler()

# Integrate the handler into your agent
from typing import Annotated
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[list, add_messages]
 
graph_builder = StateGraph(State)
 
llm = ChatOpenAI(model = "gpt-4o-mini", temperature = 0.2)
 
def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}
 
graph_builder.add_node("chatbot", chatbot)
graph_builder.set_entry_point("chatbot")
graph_builder.set_finish_point("chatbot")
graph = graph_builder.compile().with_config({"callbacks": [handler]})
 
for s in graph.stream({"messages": [HumanMessage(content = "What is autonomous AI agent?")]}):
    print(s)
```

## Requirements

- Python 3.12 or later
- Dependencies:
  - langchain>=0.3.21
  - langchain-core>=0.3.48

