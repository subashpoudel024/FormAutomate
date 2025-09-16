from pydantic import BaseModel, ConfigDict , Field
from typing import  Annotated , TypedDict
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[list, add_messages]
    form_code: str
    css_code: str
    whole_code: str
