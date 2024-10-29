from ..client import astra_client
from ..helpers import generate_embeddings
from langchain_core.tools import tool
from ..environment import viewd_id
import random
from typing import Annotated
import chainlit as cl


@tool
def update_score(status: Annotated[bool, "True if answer is correct else False"]) -> None:
    '''Update the score of the user based on the status of the answer'''
    cl.user_session.set("score", cl.user_session.get("score") + 1 if status else cl.user_session.get("score"))

@tool
def get_total_score() -> int:
    '''Get the total score of the user'''
    return cl.user_session.get("score")
