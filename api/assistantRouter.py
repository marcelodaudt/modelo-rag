from fastapi import APIRouter
from services.queryService import query_simple
from services.assistantService import assistant_question
import re

router = APIRouter()

# -----------------------------
# Funções auxiliares
# -----------------------------

# Função para limpar o texto
def clean_text(text: str) -> str:
    text = re.sub(r'\s+', ' ', text)       # remove quebras e tabs
    text = re.sub(r'<.*?>', '', text)      # remove HTML
    return text.strip()

# Função para filtrar por palavras-chave da pergunta
def is_relevant(text: str, query: str) -> bool:
    query_terms = query.lower().split()
    text_lower = text.lower()
    return any(term in text_lower for term in query_terms)

# Função para remover redundância
def deduplicate(matches):
    seen = set()
    unique = []

    for m in matches:
        text = m.metadata.get("chunk", "")
        if text not in seen:
            seen.add(text)
            unique.append(m)

    return unique

# -----------------------------
# Endpoint
# -----------------------------
@router.post('/api/assistant/query', summary="Query the database vector simple and return a intelligent response")
async def assistant_query(search: str):

    # 1. Buscar no Pinecone
    response = query_simple(search=search)
    matches = response.matches

    # 2. Ordenação: ordenar por score
    matches = sorted(matches, key=lambda x: x.score, reverse=True)

    # 3. Filtro: filtrar o ruído
    matches = [m for m in matches if m.score >= 0.60]

    # 4. Limite: limitar a quantidade de contextos (evitar overload de informações)
    matches = matches[:3]

    # 5. Contexto Estruturado: construir contexto limpo, ou seja, extrai só o texto relevante que está no metadata: "chunk" (texto)
    contexts = []
    for i, match in enumerate(matches):
        # 
        text = clean_text(match.metadata.get("chunk", ""))
        contexts.append(f"Contexto {i+1}:\n{text}")

    # 6. Cria o bloco final
    context_block = "\n\n".join(contexts)

    # 7. Enviar ao LLM
    answer = assistant_question(
        question=search,
        context_block=context_block
    )

    return {
        "question": search,
        "answer": answer
    }