from rag.retrieve import retrieve_query
from pprint import pprint
query = """
Transaction amount: 30000
Country: Nigeria

"""

results = retrieve_query(query)
pprint(results)