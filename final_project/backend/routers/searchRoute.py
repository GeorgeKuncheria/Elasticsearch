from fastapi import APIRouter, status, HTTPException
from config import INDEX_NAME_DEFAULT
from utils import get_es_client


router = APIRouter(
    tags=["Search"],
    prefix="/api"
)


@router.get("/v1/search", status_code=status.HTTP_200_OK)
async def search(search_query: str,skip: int = 0,limit: int = 10,) -> dict:
    try:
        es = get_es_client(max_retries=1, sleep_time=0)
        response = es.search(
            index=INDEX_NAME_DEFAULT,
            body={
                "query":{
                    "multi_match":{
                        "query":search_query,
                        "fields":["title","explanation"],
                    }
                },
                "from":skip,
                "size":limit,
            },
            filter_path=['hits.hits._source.hits.hits._score']
        )

        hits=response['hits']['hits']
        return {"hits":hits}

    


    except Exception as e:
        return {"error": str(e)}


