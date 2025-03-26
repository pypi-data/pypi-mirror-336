import importlib.metadata

try:
    __version__ = importlib.metadata.version(__package__)
except importlib.metadata.PackageNotFoundError:
    # Case where package metadata is not available.
    __version__ = ""


from gwenflow.llms import ChatGwenlake, ChatOpenAI, ChatAzureOpenAI, ChatOllama
from gwenflow.readers import SimpleDirectoryReader
from gwenflow.agents import Agent, ChatAgent
from gwenflow.tools import Tool
from gwenflow.flows import Flow, AutoFlow
from gwenflow.types import Document, Message
from gwenflow.retriever import Retriever


__all__ = [
    "ChatGwenlake",
    "ChatOpenAI",
    "ChatAzureOpenAI",
    "ChatOllama",
    "Document",
    "Message",
    "SimpleDirectoryReader",
    "Retriever",
    "Agent",
    "ChatAgent",
    "Tool",
    "Flow",
    "AutoFlow",
]