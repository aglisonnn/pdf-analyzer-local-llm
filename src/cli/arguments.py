import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        description="Ferramenta CLI para análise de PDFS e geração de resumo com LLM local"
    )
    
    parser.add_argument(
        "--pdf",
        type=str,
        required=True,
        help="Caminho para o arquivo PDF"
    )
    
    parser.add_argument(
        "--images",
        action="store_true",
        help="Extrair imagens do PDF"
    )
    
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Gerar resumo usando LLM local"
    )
    
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Arquivo Markdown (.md) para salvar o relatório final"
    )
    
    return parser.parse_args()