from services.authenticationService import authentication_pinecone
from services.embeddingsService import embeddingsService
import uuid

pc = authentication_pinecone()

def upsertService(embeddings: list):

    # Obs.: RECOMENDAÇÃO: usar o HOST do Índice no Pinecone, não o NAME do Índice - recomendado pelo próprio Pinecone
    index = pc.Index(host="https://base-de-conhecimento-chamados-3-k6qbag2.svc.aped-4627-b74a.pinecone.io")

    try:

        vectors = []

        for chunk_unit in embeddings:
            vectors.append({"id": f"{uuid.uuid4()}", "values": chunk_unit})

        response = index.upsert(vectors=vectors, namespace="ti-suporte-desenvolvimento")

        return {"message": "Document upserted successfully"}
    
    except Exception as e:
        
        return {"error": str(e)}

###
### EXPERIMENTOS
###

###
### Função utilizada para os EXPERIMENTOS 1 a 4
###
def upsertService_metadata(metadata: dict, chunkslistText: list):

    # Experimento 1
    index = pc.Index(host="https://experiment-1-knowledge-base-chunk-500-k6qbag2.svc.aped-4627-b74a.pinecone.io")
    # Experimento 2
    #index = pc.Index(host="https://experiment-2-knowledge-base-chunk-1000-k6qbag2.svc.aped-4627-b74a.pinecone.io")
    # Experimento 3
    #index = pc.Index(host="https://experiment-3-knowledge-base-chunk-2000-k6qbag2.svc.aped-4627-b74a.pinecone.io")
    # Experimento 4
    #index = pc.Index(host="https://experiment-4-knowledge-base-chunk-1000-k6qbag2.svc.aped-4627-b74a.pinecone.io")

    try:

        vectors = []

        for chunkstext in chunkslistText:
            embeddingchunk = embeddingsService(chunkstext)
            metadatacomplete = {**metadata, "chunk": chunkstext}
            '''
            variável metadata
            {"aula": "aula 1", "professor": "nicksson", "chunk": "texto do chunk 1"}
            {"aula": "aula 1", "professor": "nicksson", "chunk": "texto do chunk 2"}
            {"aula": "aula 1", "professor": "nicksson", "chunk": "texto do chunk 3"}
            '''
            vectors.append({"id": f"{uuid.uuid4()}", "values": embeddingchunk, "metadata": metadatacomplete})
        
        response = index.upsert(vectors=vectors, namespace="knowledge-base")

        #return {"message": f"Successfully upserted documents with metadata"}
        return response.upserted_count
    
    except Exception as e:

        return {"error": str(e)}

###
### Função utilizada para o EXPERIMENTO 5
###
def upsertService_registro_metadata(metadata: dict, chunk: str):

    # Experimento 5
    index = pc.Index(host="https://experiment-5-knowledge-base-chunk-by-call-k6qbag2.svc.aped-4627-b74a.pinecone.io")

    try:

        vectors = []

        embeddingchunk = embeddingsService(chunk)
        metadatacomplete = {**metadata, "chunk": chunk}
        vectors.append({"id": f"{uuid.uuid4()}", "values": embeddingchunk, "metadata": metadatacomplete})
        
        response = index.upsert(vectors=vectors, namespace="knowledge-base")

        return response.upserted_count
    
    except Exception as e:

        return {"error": str(e)}