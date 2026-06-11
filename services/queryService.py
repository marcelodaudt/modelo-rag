from services.authenticationService import authentication_pinecone
from services.embeddingsService import embeddingsService

def query_simple(search: str, experiment: int = 2):

    pc = authentication_pinecone()

    try:

        vectors = embeddingsService(search)

        # EXPERIMENTOS:
        INDEXES = {
            1: "https://experiment-1-knowledge-base-chunk-500-k6qbag2.svc.aped-4627-b74a.pinecone.io",
            2: "https://experiment-2-knowledge-base-chunk-1000-k6qbag2.svc.aped-4627-b74a.pinecone.io",
            3: "https://experiment-3-knowledge-base-chunk-2000-k6qbag2.svc.aped-4627-b74a.pinecone.io",
            4: "https://experiment-4-knowledge-base-chunk-1000-k6qbag2.svc.aped-4627-b74a.pinecone.io",
            5: "https://experiment-5-knowledge-base-chunk-by-call-k6qbag2.svc.aped-4627-b74a.pinecone.io"
        }

        index = pc.Index(host=INDEXES[experiment])

        response = index.query(namespace="knowledge-base", vector=vectors, top_k=10, include_metadata=True)
        
        return response
    
    except Exception as e:

        return {"message": str(e)}
