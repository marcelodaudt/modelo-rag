from services.embeddingsService import embeddingsService
from fastapi import APIRouter

router = APIRouter()

@router.post('/api/embeddings', summary="SERVIÇO: Criar Vetores (embeddings) com a OpenAI (create embeddings by OpenAI)")
async def embeddings_router(chuck: str):
    response = embeddingsService(chunk=chuck)
    
    return response
