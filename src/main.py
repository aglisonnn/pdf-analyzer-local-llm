import os

from src.cli.arguments import parse_args
from src.utils.text import print_stats
from src.pdf.extractor import contar_paginas, extrair_texto, tamanho_arquivo
from src.utils.text import calcular_estatisticas
from src.pdf.images import extrair_imagens
from src.llm.model import load_model
from src.llm.summarize import summarize_text
from src.utils.files import save_markdown


def format_summary_md(pdf_name: str, summary: str) -> str:
    return f"""# Resumo do Documento

**Arquivo:** {pdf_name}

---

## Resumo

{summary}
"""


def main():
    args = parse_args()

    arquivo_alvo = args.pdf
    output_dir = args.output if args.output else "output"

    if not os.path.exists(arquivo_alvo):
        raise FileNotFoundError(f"Arquivo PDF não encontrado: {arquivo_alvo}")

    print("Analisando PDF...")

    paginas = contar_paginas(arquivo_alvo)
    tamanho = tamanho_arquivo(arquivo_alvo)
    texto = extrair_texto(arquivo_alvo)
    stats = calcular_estatisticas(texto)

    resumo = None

    if args.summary:
        print("Carregando modelo...")
        tokenizer, model = load_model()

        print("Gerando resumo...")
        resumo = summarize_text(texto, tokenizer, model)

    if args.images:
        print("Extraindo imagens...")
        extrair_imagens(arquivo_alvo)

    if resumo:
        md_content = format_summary_md(
            pdf_name=os.path.basename(arquivo_alvo),
            summary=resumo
        )

        saved_file = save_markdown(
            content=md_content,
            output_dir=output_dir,
            filename="resumo_pdf"
        )

    print_stats(stats)

    if resumo:
        print(f"\nResumo salvo em: {saved_file}")


if __name__ == "__main__":
    main()
