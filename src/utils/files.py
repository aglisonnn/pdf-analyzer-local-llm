from pathlib import Path

def save_markdown(
    content: str, 
    output_dir: str, 
    filename: str
) -> Path:
    """
    Salva o conteúdo em um arquivo Markdown (.md).

    Argumentos:
        content (str): Texto a ser salvo
        output_dir (str): Diretório de saída
        filename (str): Nome do arquivo sem extensão

    Retorna:
        Path: Caminho do arquivo gerado
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    file_path = output_path / f"{filename}.md"
    
    with file_path.open("w", encoding="utf-8") as f:
        f.write(content)
        
    return file_path