import os
from pathlib import Path
import logging


logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')



list_of_files = [
    ".gitignore",
    ".github/workflows/.gitkeep",
    f'simulator/transaction_generator.py',
    f'storage/storage.py',
    'main.py',
    'models',
    f'Rules/amount_rules.py',
    f'Rules/country_rules.py',
    f'Rules/device_rules.py',
    f'Rules/velocity_rules.py',
    '.env',
    'storage/db.py',
    'config/config.py',
    f'ml/export_transactions.py',

    f'Data/transactions.csv',
    f'rag/create_documents.py',
    f'rag/build_index.py',
    f'rag/retrieve.py',
    f'rag/investigator.py',
    'Readme.md'


]


for file in list_of_files:
    filepath = Path(file)
    filedir, filename = os.path.split(filepath)
    if not os.path.exists(filedir) and filedir!= '':
        os.makedirs(filedir)
        logging.info(f"Directory created: {filedir}")
    
    if not os.path.exists(filepath):
        with open(filepath, 'w') as file:
            pass
        logging.info(f"File created: {filepath}")
    else:
        logging.info(f"File already exists: {filename}")