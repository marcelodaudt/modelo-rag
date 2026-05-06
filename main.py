from fastapi import FastAPI, Request
from api.indexRouter import router as api_index_router
from api.embeddingsRouter import router as api_embeddings_router
from api.miscellaneousRouter import router as api_miscellaneous_router
from api.upsertRouter import router as api_upsert_router
from api.queryRouter import router as api_query_router
from api.assistantRouter import router as api_assistant_router

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()

app.include_router(api_index_router)
app.include_router(api_embeddings_router)
app.include_router(api_miscellaneous_router)
app.include_router(api_upsert_router)
app.include_router(api_query_router)
app.include_router(api_assistant_router)

# Rota para abrir a página de upload
@app.get("/", response_class=HTMLResponse)
async def main():
    # Verifica se o arquivo existe para evitar erro 500
    if not os.path.exists("index.html"):
        return "<h1>Erro: Arquivo index.html não encontrado!</h1>"
    
    with open("index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    
    return HTMLResponse(content=html_content)