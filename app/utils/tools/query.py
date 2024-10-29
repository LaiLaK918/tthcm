from ..client import astra_client
from ..helpers import generate_embeddings
from langchain_core.tools import tool, InjectedToolArg
from ..environment import viewd_id
import random
from typing import Annotated


@tool
def search_similarity(query: Annotated[str, "The query string to search for similarity"], 
                      limit: Annotated[int, "The maximum number of documents to return"] = 20, 
                      threshold: Annotated[str, "The similarity threshold for document retrieval"] = 0.7, 
                      viewd_id: Annotated[list, InjectedToolArg] = viewd_id) -> str:
    """Searches for documents similar to the given query based on embeddings. Retrieve a fact about Ho Chi Minh to generate a question."""
    vector  = generate_embeddings(query)["embeddings"]
    documents = astra_client.find(sort={'$vector': vector}, limit=limit, filter={'_id': {'$nin': viewd_id}}, include_similarity=True)
    ret = []
    for document in documents:
        if document['$similarity'] >= threshold:
            ret.append(document)
            
    fact = random.choice(ret) if ret else None # type: dict
    viewd_id.append(fact.pop("_id"))
    return fact
