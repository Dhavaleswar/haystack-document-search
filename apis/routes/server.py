import os

from fastapi import FastAPI, Request, APIRouter
from fastapi.responses import JSONResponse
from haystack.document_stores.faiss import FAISSDocumentStore
from haystack.nodes import EmbeddingRetriever
from haystack.pipelines import DocumentSearchPipeline
from pydantic import BaseModel
from typing import List

__routes_path  = os.path.abspath(os.path.dirname(__file__))
model_dir = os.path.join(__routes_path, '', '../..', 'model')

ravis_apis = APIRouter()

document_store = FAISSDocumentStore.load(
    # sql_url="sqlite:///" + os.path.join(model_dir, "faiss_document_store.db"),
    index_path=os.path.join(model_dir, "my_faiss_index.faiss"),
    config_path=os.path.join(model_dir,"my_faiss_index.json")
)

# Load the JSON configuration file for the retriever (assuming you have one)
retriever = EmbeddingRetriever(
    document_store=document_store, embedding_model="sentence-transformers/multi-qa-mpnet-base-dot-v1",top_k=3)

semantic_search_pipeline = DocumentSearchPipeline(retriever=retriever)



def get_response(question):
    prediction = semantic_search_pipeline.run(query=question)
    search_results = []
    for i, pred in enumerate(prediction['documents']):
        name = pred.meta['name']
        content = pred.content[0:200]
        search_results.append({'file_name': name, 'file_content':content})
    return search_results

@ravis_apis.post("/test_query")
async def index(query:str):
    if query:
        search_results = get_response(query)
        return JSONResponse(content={'query':query, 'result':search_results}, status_code=200)
    else:
        return JSONResponse(content={'query':query, 'result':'None'}, status_code=404)