from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from services.miscellaneousService import extract_text_from_pdf, extract_text_from_txt
from api.miscellaneousRouter import split_in_chunks_embeddings, split_in_chunks_simple
from services.upsertService import upsertService, upsertService_metadata, upsertService_registro_metadata
import json

import uuid
import asyncio
from typing import List
from services.embeddingsService import embeddingsService
from fastapi import APIRouter, UploadFile, File, Form, HTTPException

router = APIRouter()

### ARQUIVOS PDF
################

@router.post('/api/upsert/pdf', summary="SERVIÇO: Inserindo (upsert) um documento PDF no Banco de Dados (upsert a document PDF into the database).")
async def upsert(filepdf: UploadFile = File(...)):

    textfromPDF = extract_text_from_pdf(filepdf)
    chunkslistEmbeddings = await split_in_chunks_embeddings(text=textfromPDF)
    response = upsertService(embeddings=chunkslistEmbeddings)
    
    return response

@router.post('/api/upsert/pdf_metadata', summary="SERVIÇO: Inserindo (upsert) um documento no Banco de Dados com Metadados (upsert a document into the database with metadata).")
async def upsert_metadata(filepdf: UploadFile = File(...), metadata: str = Form(...)):      # Form(...) = Formulário

    try:
        metadataJson = json.loads(metadata)
        textfromPDF = extract_text_from_pdf(filepdf)
        chunkslistText = await split_in_chunks_simple(text=textfromPDF)
        response = upsertService_metadata(metadata=metadataJson, chunkslistText=chunkslistText)
        
        #return response
        return {"message": f"Successfully upserted {response} documents"}

    except Exception as e:

        return {"error": str(e)}

### ARQUIVOS TXT
################

@router.post('/api/upsert/txt', summary="SERVIÇO: Inserindo (upsert) um documento TXT no Banco de Dados (upsert a document TXT into the database).")
async def upsert(filetxt: UploadFile = File(...)):

    textfromTXT = extract_text_from_txt(filetxt)
    chunkslistEmbeddings = await split_in_chunks_embeddings(text=textfromTXT)
    response = upsertService(embeddings=chunkslistEmbeddings)
    
    return response

##########################################
####### EXPERIMENTOS 1 a 4- INÍCIO #######
##########################################

# FUNÇÃO PARA INSERIR UM DOCUMENTO TXT + METADADOS - é feito o upload do arquivo, depois esse arquivo é quebrado em pedaços (chunks); depois, cada chunk é vetorizado (embedding) e inserido no banco (upsert).
@router.post('/api/upsert/txt_metadata', summary="SERVIÇO: Inserindo (upsert) um documento TXT no Banco de Dados com Metadados (upsert a document TXT into the database with metadata).")
async def upsert_metadata(filetxt: UploadFile = File(...), metadata: str = Form(...)):      # Form(...) = Formulário

    try:
        metadataJson = json.loads(metadata)
        textfromTXT = extract_text_from_txt(filetxt)
        chunkslistText = await split_in_chunks_simple(text=textfromTXT)
        response = upsertService_metadata(metadata=metadataJson, chunkslistText=chunkslistText)
        
        #return response
        return {"message": f"Successfully upserted {response} documents"}

    except Exception as e:

        return {"error": str(e)}

####### EXPERIMENTOS 1 a 4- FINAL #######

######################################
####### EXPERIMENTO 5 - INÍCIO #######
######################################

# FUNÇÃO PARA INSERIR UM REGISTRO DE CHAMADO (arquivo TXT) - upload do arquivo, que será um chunk; depois esse chunck é vetorizado (embedding) e inserido no banco (upsert).
@router.post('/api/upsert/txt_registro_metadata', summary="SERVIÇO: Inserindo (upsert) um registro de chamado de arquivo TXT no Banco de Dados com Metadados (upsert a register from TXT into the database with metadata).")
async def upsert_registro_metadata(filetxt: UploadFile = File(...), metadata: str = Form(...)):

    try:
        metadataJson = json.loads(metadata)
        textfromTXT = extract_text_from_txt(filetxt)
        response = upsertService_registro_metadata(metadata=metadataJson, chunk=textfromTXT)
        
        return {"message": f"Successfully upserted {response} documents"}

    except Exception as e:

        return {"error": str(e)}

####### OU #######

# FUNÇÃO PARA INSERIR VÁRIOS REGISTROS DE CHAMADO (vários arquivos TXT)
@router.post('/api/upsert/multiple_txt_files', summary="SERVIÇO: Inserir múltiplos arquivos TXT no Banco de Dados Vetorial com Metadados")
async def upsert_multiple_files(files: List[UploadFile] = File(...), metadata: str = Form(...)):
    """
    Insere múltiplos arquivos TXT no banco de dados vetorial Pinecone.
    
    Args:
        files: Lista de arquivos TXT para processar
        metadata_list: JSON string contendo lista de objetos de metadados
                      (um para cada arquivo, na mesma ordem)
    
    Returns:
        Resultado do upsert para cada arquivo
    """
    try:
        metadataJson = json.loads(metadata)
        
        results = []
        
        # Processar cada arquivo sequencialmente
        for i, filetxt in enumerate(files):
            try:
                # Extrair texto do arquivo
                textfromTXT = await extract_text_from_txt_async(filetxt)
                
                # Inserir no banco de dados
                result = upsertService_registro_metadata(metadata=metadataJson, chunk=textfromTXT)
                
                results.append({
                    "filename": filetxt.filename,
                    "status": "success",
                    "upserted_count": result if isinstance(result, int) else 0,
                    "message": f"Arquivo {i+1}/{len(files)} processado com sucesso"
                })
                
                # Pequena pausa para não sobrecarregar a API
                await asyncio.sleep(0.1)
                
            except Exception as file_error:
                results.append({
                    "filename": filetxt.filename,
                    "status": "error",
                    "error": str(file_error),
                    "message": f"Erro ao processar arquivo {i+1}/{len(files)}"
                })
        
        return {
            "message": f"Processamento de {len(files)} arquivos concluído",
            "results": results,
            "summary": {
                "total_files": len(files),
                "successful": sum(1 for r in results if r["status"] == "success"),
                "failed": sum(1 for r in results if r["status"] == "error")
            }
        }

    except Exception as e:
        return {"error": str(e)}

# Versão assíncrona da extração de texto
async def extract_text_from_txt_async(filetxt: UploadFile):
    """
    Versão assíncrona para extrair texto de arquivo TXT
    """
    content = await filetxt.read()
    return content.decode('utf-8')

#################
# NOVA FUNÇÃO PARA INSERIR VÁRIOS REGISTROS DE CHAMADO (vários arquivos TXT)
@router.post('/api/upsert/folder_upload', summary="SERVIÇO: NOVA FUNÇÃO para inserir múltiplos arquivos TXT  (FOLDER) no Banco de Dados Vetorial com Metadados")
async def upsert_from_folder(
    # O segredo está aqui: o navegador enviará uma lista de arquivos
    files: List[UploadFile] = File(...), 
    metadata: str = Form(...)
):
    try:
        # 1. Carrega os metadados (que serão aplicados a todos os arquivos)
        import json
        metadata_dict = json.loads(metadata)

        # 2. Criamos as tarefas para processar todos os arquivos em paralelo
        # Isso evita que o processo seja lento se você selecionar 50 arquivos
        tasks = [process_and_upsert(f, metadata_dict) for f in files]
        
        # 3. Executa tudo simultaneamente
        results = await asyncio.gather(*tasks)

        return {
            "message": f"Processados {len(files)} arquivos com sucesso.",
            "details": results
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro geral: {str(e)}")

async def process_and_upsert(file: UploadFile, metadata: dict):
    """Função auxiliar para processar cada arquivo da lista"""
    try:
        content = await file.read()
        text = content.decode('utf-8')
        
        # Chama sua função de persistência (Pinecone/OpenAI)
        # Se 'upsertService_registro_metadata' for síncrona, ela roda aqui
        result = upsertService_registro_metadata(metadata=metadata, chunk=text)
        
        return {"file": file.filename, "status": "success"}
    except Exception as e:
        return {"file": file.filename, "status": "error", "reason": str(e)}
    
####### EXPERIMENTO 5 - FINAL #######