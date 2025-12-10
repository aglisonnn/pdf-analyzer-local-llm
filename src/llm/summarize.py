from typing import List
from transformers import PreTrainedTokenizer, PreTrainedModel
import torch


def split_text(text: str, max_words: int = 500) -> List[str]:
    """
    Divide o texto em blocos maiores para reduzir o número
    de chamadas ao modelo e melhorar desempenho.
    """
    words = text.split()
    chunks = []

    for i in range(0, len(words), max_words):
        chunks.append(" ".join(words[i:i + max_words]))

    return chunks


def summarize_chunk(
    chunk: str,
    tokenizer: PreTrainedTokenizer,
    model: PreTrainedModel,
    max_new_tokens: int = 80
) -> str:
    """
    Gera um resumo curto e informativo de um bloco de texto.
    """
    prompt = (
        "Resuma o texto abaixo em português, de maneira objetiva, "
        "destacando o tema principal. Evite detalhes excessivos.\n\n"
        f"{chunk}\n\nResumo:"
    )

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False
        )

    texto = tokenizer.decode(output[0], skip_special_tokens=True)

    if "Resumo:" in texto:
        texto = texto.split("Resumo:")[-1].strip()

    return texto


def summarize_text(
    text: str,
    tokenizer: PreTrainedTokenizer,
    model: PreTrainedModel
) -> str:
    """
    Resume textos grandes em múltiplos estágios:
    1. Chunking
    2. Resumos parciais
    3. Resumo final consolidado
    """
    chunks = split_text(text)
    partial_summaries = []

    for idx, chunk in enumerate(chunks, start=1):
        print(f"Resumindo parte {idx}/{len(chunks)}...")
        resumo = summarize_chunk(chunk, tokenizer, model)
        partial_summaries.append(resumo)

    # Se só houve um chunk, retorna direto
    if len(partial_summaries) == 1:
        return partial_summaries[0]

    final_prompt = (
        "Com base nos resumos parciais a seguir, escreva um resumo final "
        "em português claro e objetivo, explicando o tema geral do documento "
        "e seu propósito principal. Evite listas e repetições.\n\n"
        + "\n\n".join(partial_summaries)
        + "\n\nResumo final:"
    )

    inputs = tokenizer(final_prompt, return_tensors="pt").to(model.device)

    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=300,
            do_sample=False
        )

    resumo_final = tokenizer.decode(output[0], skip_special_tokens=True)

    if "Resumo final:" in resumo_final:
        resumo_final = resumo_final.split("Resumo final:")[-1].strip()

    return resumo_final
