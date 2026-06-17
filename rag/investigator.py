import requests
from rag.retrieve import retrieve_query

def generate_report(transaction_text):

    similar_cases = retrieve_query(transaction_text)
    content ="\n\n".join(similar_cases)

    prompt =f"""
    Transaction: {transaction_text}
    Similar Cases: {content}
    Explain:
    1. Why it is suspicious?
    2. What are the red flags?
    3. Recommended actions.
"""
    response = requests.post( "http://localhost:11434/api/generate",
                             json={"prompt": prompt,
                                   "model":"mistral",
                                   "stream": False}
    )

    
    data = response.json()

    return data['response']


