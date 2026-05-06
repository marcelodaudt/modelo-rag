from fastapi import APIRouter
from services.queryService import query_simple

router = APIRouter()

@router.post('/api/query/simple', summary="Query the database vector simple")
async def query(search: str):

    response = query_simple(search=search)

    matches = response.matches

    # transformar objetos em algo serializável
    jsonResponse = [
        {
            "id": match.id,
            "score": match.score,
            "metadata": match.metadata      # exemplo de atributo que pode estar presente
        }
        for match in matches
    ]

    return jsonResponse   