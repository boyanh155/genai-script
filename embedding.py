# generate_embeddings.py
from transformers import pipeline, AutoModel, AutoTokenizer

from pymongo import MongoClient
from dotenv import load_dotenv
import os
import torch

from pyvi.ViTokenizer import tokenize


load_dotenv() 

# model list:
##  - vinai/phobert-base-v2
##  - sentence-transformers/all-MiniLM-L6-v2
##  - dangvantuan/vietnamese-embedding
phobert = AutoModel.from_pretrained("dangvantuan/vietnamese-embedding")
tokenizer = AutoTokenizer.from_pretrained("dangvantuan/vietnamese-embedding")

# 


# 

hugging_face_token = os.getenv("hugging_face_token")
model_id =  os.getenv("model_id")
embedding_url = os.getenv("embedding_url")
headers= {"Authorization":f"Bearer {hugging_face_token}"}

# mongodb
connection_string = os.getenv("mongodb_connection_string")
 
BATCH_SIZE = os.getenv("BATCH_SIZE") and int(os.getenv("BATCH_SIZE")) or 1000


# def query(payload:json) -> list[float]:
 
#     response = requests.post(embedding_url, headers=headers, json=payload)
#     return response.json()

# def queryTilSuccess(payload:json) -> list[float]:
   
        
#     if(retry >= 5):
#         raise Exception("Failed to get embeddings")
#     return response.json()

mongodb_client = MongoClient(connection_string)

services_collection = mongodb_client[os.getenv("db_name")][os.getenv("collection_name")]

def search_query(query:str) ->list:
    try:
        print("=== Searching ===")
        print(query)
        query_vector = generate_embeddings(query)
        # print(query_vector)
        all_services = services_collection.aggregate([
            {
                "$vectorSearch":{
                    "path": "embedding",
                    "queryVector": query_vector,
                    "numCandidates": 500,
                    "path": "embedding",
                    "limit":5,
                    "index":"nameSemanticSearch"
                }
            },{
                # exclude embedding field
                "$project": {
                    "name": 1,  "score": {
                        "$meta": "vectorSearchScore",
                    }
                }
            }
        ])
        # print(list(all_services))
        return list(all_services)
    except Exception as e:
        raise e

def generate_embeddings(payload:str) -> list[float]:
    # embedding = query(payload)
    try:
        inputSegment = torch.tensor([tokenizer.encode(payload)]) 
        
        with torch.no_grad():
            embeddings = phobert(inputSegment).last_hidden_state.mean(dim=1).squeeze().tolist()
            return embeddings
    except Exception as e:
        raise e


def add_embedding(): 
    all_services = services_collection.find({})
    for i in range(0, services_collection.count_documents({}), BATCH_SIZE):
        batch = all_services[i:i+BATCH_SIZE]
        for service in batch:
            embeddings = generate_embeddings(service["name"])
            # print(embeddings)
            services_collection.update_one({"_id": service["_id"]}, {"$set": {"embedding": embeddings}})

if __name__ == "__main__":
    
    #  1. Add embeddings to all services
    # add_embedding()
    #  2. Search for services
    search_query("Da tôi bị mụn, có dịch vụ nào không?")