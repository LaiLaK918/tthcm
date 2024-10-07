from ..client import astra_client
from ..helpers import generate_embeddings
from langchain_core.tools import tool
from ..environment import viewd_id
import random


@tool
def search_similarity(query: str, limit: int = 20, threshold=0.7, viewd_id: list=viewd_id) -> str:
    """
    Searches for documents similar to the given query based on embeddings. Retrieve a fact about Ho Chi Minh to generate a question.

    Args:
        query (str): The query string to search for similarity.
        limit (int): The maximum number of documents to return (default is 20).
        threshold (float): The similarity threshold for document retrieval (default is 0.7).

    Returns:
        list: A list of documents similar to the query based on the threshold.
    """
    vector  = generate_embeddings(query)["embeddings"]
    documents = astra_client.find(sort={'$vector': vector}, limit=limit, filter={'_id': {'$nin': viewd_id}}, include_similarity=True)
    ret = []
    for document in documents:
        if document['$similarity'] >= threshold:
            ret.append(document)
            
    fact = random.choice(ret) if ret else None # type: dict
    viewd_id.append(fact.pop("_id"))
    return fact
