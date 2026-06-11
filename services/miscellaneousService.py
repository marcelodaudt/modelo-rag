from PyPDF2 import PdfReader
from fastapi import UploadFile
from io import BytesIO              # classe BytesIO - audio, video, arquivo (PDF) -> binário

# FUnção para extrair o texto de um arquivo PDF
def extract_text_from_pdf(filepdf: UploadFile):

    # lê o arquivo PDF - binário
    pdf_byte = filepdf.file.read()

    # cria um leitor de PDF
    pdf_stream = BytesIO(pdf_byte)

    readerPDF = PdfReader(pdf_stream)
    text = ""
    for page in readerPDF.pages:
        text += page.extract_text()
    return text

# FUnção para extrair o texto de um arquivo TXT
def extract_text_from_txt(filetxt: UploadFile):
    # lê todo o arquivo e decodifica
    content = filetxt.file.read()
    
    try:
        # tenta UTF-8 (padrão mais comum)
        text = content.decode("utf-8")
    except UnicodeDecodeError:
        text = content.decode("latin-1")
    
    return text

# Função para dividir o texto em partes (CHUNKS) -> ex.: chunk_size=1000, overlap=200 para chunk_size=1500, overlap=300
# EXPERIMENTOS
# Experimento 1: chunk_size=500, overlap=100
# Experimento 2: chunk_size=1000, overlap=200
# Experimento 3: chunk_size=2000, overlap=400
# Experimento 4: chunk_size=1000, overlap=200
# Experimento 5: por registro, sem sobreposição
def split_text_into_chunks(text: str, chunk_size=1000, overlap=200) -> list:
    chunks = []
    for i in range(0, len(text), chunk_size - overlap):
        chunks.append(text[i:i + chunk_size])
    
    return chunks