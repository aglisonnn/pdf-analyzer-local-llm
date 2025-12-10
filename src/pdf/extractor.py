import pymupdf
import os

# Primeiro requisito de analise de de PDF
def contar_paginas(caminho_pdf: str) -> int:
    """"1 - Abre o pdf somente para contar as paginas e depois fecha."""
    with pymupdf.open(caminho_pdf) as doc:
        return doc.page_count
    
def extrair_texto(caminho_pdf: str) -> str:
    """Extrai todo o texto do PDF e retorna como uma única string bruta."""
    texto_completo = ""
    
    with pymupdf.open(caminho_pdf) as doc:
        for page in doc:
            texto_completo += page.get_text() + "\n"
            
    return texto_completo

# Terceiro requisito de analise de PDF
def tamanho_arquivo(caminho_pdf: str) -> int:
    """3 - Retorna o tamanho do arquivo em bytes."""
    # Validando se o arquivo existe
    if not os.path.exists(caminho_pdf):
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho_pdf}")
    return os.path.getsize(caminho_pdf)


    
    