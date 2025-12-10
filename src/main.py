import os

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
    arquivo_alvo = "data/Apostila_Inteligência_Artificial.pdf"
    output_dir = "output"

    print("Analisando PDF...")
    paginas = contar_paginas(arquivo_alvo)
    tamanho = tamanho_arquivo(arquivo_alvo)
    texto = extrair_texto(arquivo_alvo)
    stats = calcular_estatisticas(texto)

    print("Carregando modelo...")
    tokenizer, model = load_model()

    print("Gerando resumo...")
    resumo = summarize_text(texto, tokenizer, model)

    md_content = format_summary_md(
        pdf_name=os.path.basename(arquivo_alvo),
        summary=resumo
    )

    saved_file = save_markdown(
        content=md_content,
        output_dir=output_dir,
        filename="resumo_pdf"
    )

    print("\n--- RESULTADOS ---")
    print(f"Páginas: {paginas}")
    print(f"Tamanho (bytes): {tamanho}")
    print("Estatísticas:", stats)
    print(f"Resumo salvo em: {saved_file}")


if __name__ == "__main__":
    main()
