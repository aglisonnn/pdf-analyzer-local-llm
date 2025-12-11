# 📘 PDF Analyzer & Summarizer CLI

Uma ferramenta completa de linha de comando (CLI) desenvolvida em **Python**, capaz de:

- Analisar arquivos **PDF** (páginas, palavras, vocabulário, tamanho).
- Extrair **imagens internas** do PDF.
- Gerar **resumos automáticos** usando um modelo **LLM local** (Hugging Face).
- Gerar um **Relatório Final em Markdown** com todas as análises.

> Projeto desenvolvido como desafio técnico, com foco em organização, modularização e boas práticas de engenharia de software.

---

## Funcionalidades

### 1. Análise do PDF
A ferramenta extrai e exibe:
- Número total de páginas.
- Número total de palavras.
- Tamanho do PDF em bytes.
- Top 10 palavras mais frequentes (ignorando stopwords).
- Tamanho do vocabulário único.

### 2. Extração de Imagens
- Detecta todas as imagens do PDF.
- Exporta cada imagem para `images/<nome_do_pdf>/`.
- Garante nomes únicos para cada arquivo exportado.

### 3. Geração de Resumo com LLM Local
- Carrega um modelo local da Hugging Face (ex: Qwen, Mistral, Gemma).
- Divide PDFs grandes em partes (*chunking* inteligente).
- Gera resumo consolidado no final.

### 4. Relatório Final em Markdown
Gera automaticamente um arquivo `.md` contendo:
- Informações do PDF.
- Estatísticas detalhadas.
- Top 10 palavras.
- Resumo completo gerado por IA.
- Caminho de exportação salvo automaticamente.

---

## Estrutura do Projeto

src/
│
├── cli/
│   └── arguments.py
│
├── llm/
│   ├── model.py
│   ├── summarize.py
│   └── test_llm.py
│
├── pdf/
│   ├── extractor.py
│   └── images.py
│
├── utils/
│   ├── text.py
│   ├── files.py
│   └── logger.py
│
├── main.py
├── data/       # PDFs de entrada (não incluso no repositório)
├── output/     # Arquivos .md gerados
└── images/     # Imagens extraídas

---

## Instalação

### 1. Criar ambiente virtual

```bash
python -m venv venv
```

### 2. Ativar ambiente

**Windows:**

```bash
venv\Scripts\activate
```

**Linux/Mac:**

```bash
source venv/bin/activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

---

## Como Usar

A ferramenta é executada via módulo na raiz do projeto:

```bash
python -m src.main --pdf caminho/do/arquivo.pdf [opções]
```

### Opções disponíveis

| Flag | Descrição |
| :--- | :--- |
| `--pdf <arquivo>` | **Obrigatório** — Caminho do arquivo PDF. |
| `--summary` | Gera resumo usando LLM local. |
| `--images` | Extrai imagens contidas no PDF. |
| `--output <pasta>` | Define onde salvar o relatório final (padrão: `output/`). |

---

## 📌 Exemplos de Uso

### 1. Executar análise completa + resumo + imagens

```bash
python -m src.main --pdf data/Relatorio.pdf --summary --images
```

### 2. Apenas análise estatística do PDF

```bash
python -m src.main --pdf data/Relatorio.pdf
```

### 3. Salvar relatório em outra pasta personalizada

```bash
python -m src.main --pdf data/Relatorio.pdf --summary --output resultados
```


---

## Teste do LLM Local

Para garantir que o modelo funciona e baixar os pesos antes de rodar toda a pipeline:

```bash
python src/llm/test_llm.py
```

---

## Logs

O projeto utiliza sistema de logging para acompanhar o progresso. Exemplo de saída no terminal:

text
15:26:34 - INFO - Carregando modelo...
15:27:38 - INFO - Gerando resumo...
15:27:38 - WARNING - Partes do modelo foram carregadas no disco...


---

## Tecnologias Utilizadas

- **Python 3.11+**
- **PyMuPDF** (Manipulação de PDF)
- **Transformers** (Hugging Face - LLM)
- **PyTorch** (Backend de ML)
- **Argparse** (CLI)
- **Logging** (Rastreabilidade)

---

## Exemplo de Relatório Gerado

O arquivo final `.md` terá o seguinte formato:

# Relatório de Análise do PDF

## Informações do Documento
- Arquivo: Relatorio.pdf
- Número de páginas: 37
- Tamanho (bytes): 2.065.506

## Estatísticas do Texto
- Total de palavras: 8256
- Vocabulário único: 2069

## Top 10 Palavras Mais Frequentes
1. **governo** (60)
2. **estado** (56)
...

## Resumo Gerado por LLM
Este documento trata das diretrizes de segurança pública...

---

## 🧹 .gitignore recomendado

gitignore
venv/
__pycache__/
output/
images/
data/
*.pdf
.env