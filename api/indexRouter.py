from fastapi import APIRouter
from services.indexService import create_index, list_index, detail_index

router = APIRouter()

@router.post('/api/index/create', summary="SERVIÇO: Criar um Índice no Pinecone (create index by Pinecone)")
async def create_index_router(name_index: str):
    response = create_index(name=name_index)
    return{f'The index {response}'}

@router.get('/api/index/list', summary="SERVIÇO: Listar os Índices existente no Pinecone (list the index of Pinecone)")
async def list_index_router():
    response = list_index()
    return response

@router.post('/api/index/detail', summary="SERVIÇO: Mostrar detalhes de um determinado Índice (show details from index)")
async def detail_index_router(name_index: str):
    response = detail_index(name=name_index)
    return response