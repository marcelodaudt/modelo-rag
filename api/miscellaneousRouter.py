# ...
#  STEPS:
# 1 - Send a PDF
# 2 - Extract text from PDF
# 3 - Send the text to the embeddingsService
# ...

from fastapi import APIRouter, File, UploadFile
from services.miscellaneousService import extract_text_from_pdf, split_text_into_chunks, extract_text_from_txt
from services.embeddingsService import embeddingsService

router = APIRouter()

# Função para extrair o texto de arquivos PDF
@router.post('/api/miscellaneous/pdf', summary="SERVIÇO: Extrair texto de arquivo PDF (extract text from a PDF file)")
async def pdf_to_text(filepdf: UploadFile = File(...)):
    response = extract_text_from_pdf(filepdf)

    return response

# Função para extrair o texto de arquivos TXT
@router.post('/api/miscellaneous/txt', summary="SERVIÇO: Extrair texto de arquivo TXT (extract text from a TXT file)")
async def txt_to_text(filetxt: UploadFile = File(...)):
    response = extract_text_from_txt(filetxt)

    return response

# Função que quebra o texto em partes (chunks)
@router.post('/api/miscellaneous/split_in_chunks', summary="SERVIÇO: Quebrando o texto em pedaços (split text into chuncks).")
async def split_in_chunks_simple(text: str):
    response = split_text_into_chunks(text=text)

    return response

# Função que quebra o texto em partes (chunks) e já vetoriza (embeddings)
@router.post('/api/miscellaneous/split_in_chunks_embeddings', summary="SERVIÇO: Quebrando o texto em pedaços e criar uma lista de vetores (split text into chunks and create a list of embeddings).")
async def split_in_chunks_embeddings(text: str):
    chunks_list = split_text_into_chunks(text=text)

    try:
        embeddings = []
        for chunk in chunks_list:
            embeddings.append(embeddingsService(chunk=chunk))
        return embeddings
    except Exception as e:
        return {"error": str(e)}

