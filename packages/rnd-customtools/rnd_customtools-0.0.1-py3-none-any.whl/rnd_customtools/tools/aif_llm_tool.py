from promptflow import tool
from jinja2 import Template
from promptflow.connections import CustomConnection
from promptflow.contracts.types import PromptTemplate


@tool
def call_llm(input_text: str,connection: CustomConnection,
         api: str,
         deployment_name: str,
         temperature: float,
         prompt: PromptTemplate,
         **kwargs
         ) -> str:
    # Replace with your tool code.
    # Usually connection contains configs to connect to an API.
    # Use CustomConnection is a dict. You can use it like: connection.api_key, connection.api_base
    # Not all tools need a connection. You can remove it if you don't need it.
    return "Hello " + input_text