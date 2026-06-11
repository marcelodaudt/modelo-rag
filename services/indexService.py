from services.authenticationService import authentication_pinecone
from pinecone import ServerlessSpec

pc = authentication_pinecone()                                      # faz autenticação no Pinecone

def create_index(name: str):

    response = pc.create_index(
        name=name,
        dimension=1536,                                             # dimensão dos vetores
        metric="cosine",                                            # método de similaridade
        spec=ServerlessSpec(cloud="aws", region="us-east-1")        # tipo do servidor - nuvem
        )
    
    return response

def list_index():
    response = pc.list_indexes()

    return response.to_dict()

def detail_index(name: str):
    response = pc.describe_index(name=name)
    return response.to_dict()