import json
from pprint import pprint
from typing import List
from tqdm import tqdm

from elasticsearch import Elasticsearch
from config import INDEX_NAME_DEFAULT,INDEX_NAME_N_GRAM
from utils import get_es_client



def index_data(documents: List[dict]):
    es=get_es_client()
    _ = _create_index(es=es)
    _=_index_documents(es=es,documents=documents)

    pprint(f"Indexed {len(documents)} documents into index '{INDEX_NAME_DEFAULT}' successfully.")



def _create_index(es:Elasticsearch) -> dict:
    es.indices.delete(index=INDEX_NAME_DEFAULT,ignore_unavailable=True)
    return es.indices.create(index=INDEX_NAME_DEFAULT)


def _index_documents(es:Elasticsearch,documents:List[dict]) -> dict:
    operations=[]
    for document in tqdm(documents,total=len(documents),desc='Indexing documents'):
        operations.append({'index':{'_index':INDEX_NAME_DEFAULT}})
        operations.append(document)

    return es.bulk(body=operations,refresh=True)



if __name__=="__main__":
    try:
        with open("../../data/apod.json") as f:
            documents=json.load(f)

        index_data(documents=documents)

    except Exception as e:
        pprint(f"Error: {e}")