import json
import pickle
import os 
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

with open('rag/fraud_docs.json', 'r') as f:
    documents = json.load(f)    

embeddings = model.encode(documents)
index = faiss.IndexFlatL2(embeddings.shape[1])
#print(index)

index.add(np.array(embeddings, dtype = "float32"))
faiss.write_index(index,'rag/fraud_index.faiss')
with open('rag/documents.pkl', 'wb') as f:
    pickle.dump(documents, f)

print(f'Index built and saved successfully with {len(documents)} documents.')