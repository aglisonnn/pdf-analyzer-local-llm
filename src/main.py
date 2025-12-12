import os

from src.utils.logger import setup_logger
from src.cli.arguments import parse_args
from src.utils.text import print_stats
from src.pdf.extractor import contar_paginas, extrair_texto, tamanho_arquivo
from src.utils.text import calcular_estatisticas
from src.pdf.images import extrair_imagens
from src.llm.model import load_model
from src.llm.summarize import summarize_text
from src.utils.files import save_markdown

logger = setup_logger()

def format_report_md(
    pdf_name: str,
    paginas: int,
    tamanho: int,
    stats: dict,
    summary: str | None
) -> str:
    top_10_md = "\n".join(
        [f"{i+1}. **{p}** ({f})" for i, (p, f) in enumerate(stats["top_10"])]
    )

    return f"""# Relatório de Análise do PDF

## Informações do Documento
- **Arquivo:** {pdf_name}
- **Número de páginas:** {paginas}
- **Tamanho (bytes):** {tamanho:,}

## Estatísticas do Texto
- **Total de palavras:** {stats['total_palavras']:,}
- **Vocabulário único:** {stats['vocabulario_unico']:,}

## Top 10 Palavras Mais Frequentes
{top_10_md}

## Resumo Gerado por LLM
{summary if summary else "_Resumo não solicitado._"}
"""


def main():
    args = parse_args()

    arquivo_alvo = args.pdf
    output_dir = args.output if args.output else "output"

    if not os.path.exists(arquivo_alvo):
        logger.error(f"Arquivo PDF não encontrado: {arquivo_alvo}")
        return

    logger.info("Analisando PDF...")

    paginas = contar_paginas(arquivo_alvo)
    tamanho = tamanho_arquivo(arquivo_alvo)
    texto = extrair_texto(arquivo_alvo)
    stats = calcular_estatisticas(texto)

    resumo = None

    if args.summary:
        logger.info("Carregando modelo...")
        tokenizer, model = load_model()

        logger.info("Gerando resumo...")
        resumo = summarize_text(texto, tokenizer, model)

    if args.images:
        logger.info("Extraindo imagens...")
        extrair_imagens(arquivo_alvo,output_dir)

    if resumo:
        md_content = format_report_md(
            pdf_name=os.path.basename(arquivo_alvo),
            paginas=paginas,
            tamanho=tamanho,
            stats=stats,
            summary=resumo
        )

        saved_file = save_markdown(
            content=md_content,
            output_dir=output_dir,
            filename="relatorio_pdf"
        )

    print("\nInformações do PDF")
    print(f"- Número total de páginas : {paginas}")
    print(f"- Tamanho do PDF (bytes)  : {tamanho:,}".replace(",", "."))
    
    print_stats(stats)

    if resumo:
        print(f"\nResumo salvo em: {saved_file}\n")


if __name__ == "__main__":
    main()
