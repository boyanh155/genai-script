# generate_embeddings.py
from transformers import pipeline
import sys
import json
import requests
from pymongo import MongoClient
from dotenv import load_dotenv
import os



load_dotenv() 

hugging_face_token = os.getenv("hugging_face_token")
model_id =  os.getenv("model_id")
embedding_url = os.getenv("embedding_url")
headers= {"Authorization":f"Bearer {hugging_face_token}"}

# mongodb
connection_string = os.getenv("mongodb_connection_string")
 
BATCH_SIZE = os.getenv("BATCH_SIZE") and int(os.getenv("BATCH_SIZE")) or 1000


def query(payload:json) -> list[float]:
 
    response = requests.post(embedding_url, headers=headers, json=payload)
    return response.json()

def queryTilSuccess(payload:json) -> list[float]:
    response = query(payload)
    retry = 0
    while response.status_code != 200 and retry < 5:
        response = query(payload)
        retry += 1
        
    if(retry >= 5):
        raise Exception("Failed to get embeddings")
    return response.json()



def generate_embeddings(payload):
    embedding = query(payload)
    
    return embedding
   

if __name__ == "__main__":
    mongodb_client = MongoClient(connection_string)
    
    services_collection = mongodb_client[os.getenv("db_name")][os.getenv("collection_name")]
    all_services = services_collection.find({})
    
    
    for i in range(0, services_collection.count_documents({}), BATCH_SIZE):
        batch = all_services[i:i+BATCH_SIZE]
        for service in batch:
            embeddings = generate_embeddings(service["name"])
            services_collection.update_one({"_id": service["_id"]}, {"$set": {"embedding": embeddings}})
            
    
    embeddings = generate_embeddings(json.loads(text))
    # return embeddings
    print(json.dumps(embeddings))