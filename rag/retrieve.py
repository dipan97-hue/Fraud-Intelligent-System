import json
import pickle
import os 
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

index = faiss.read_index('rag/fraud_index.faiss')
documents = pickle.load(open('rag/documents.pkl','rb'))

def retrieve_query(query, top_k = 3):

    embedding = model.encode([query])
    distance, ids = index.search(embedding.astype('float32'),top_k )
    result =[]

    for idx in ids[0]:
        result.append(documents[idx])

    return result