from services.authenticationService import authentication_openai

clientOpenAI = authentication_openai()              # autenticação na OpenAI

def embeddingsService(chunk: str):

    embedding = clientOpenAI.embeddings.create(
        # EXPERIMENTOS:
        # Experimento 1, 2 e 5
        #model='text-embedding-3-small',             # modelo mais barato e rápido da OpenAI para gerar vetores (embeddings)
        # Experimento 3 e 4
        model='text-embedding-3-large',
        input=chunk,                                # texto (ou pedaço de texto - chunk) que será convertido em vetor (embedding)
        dimensions=1536
    )

    response = embedding.to_dict()                  # embedding retorna da OpenAI como dicionário
    vector = response["data"][0]["embedding"]       # armazeno somente o VETOR (embedding) - linha 0 (zero)

    return vector
