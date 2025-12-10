from pathlib import Path
import pymupdf

def extrair_imagens(pdf_path: str, output_dir: str) -> int:
    """
    Extrai todas as imagens de um PDF e salve em:
    output_dir/<nome_do_pdf>/
    
    Retorna o número de imagens extraídas.
    """
    pdf_path = Path(pdf_path)
    output_dir = Path(output_dir)
    
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF não encontrado: {pdf_path}")
    
    pdf_name = pdf_path.stem
    imagens_pdf_dir = output_dir / pdf_name
    imagens_pdf_dir.mkdir(parents=True, exist_ok=True)
    
    imagens_extraidas = 0
    
    with pymupdf.open(pdf_path) as doc:
        for page_index, page in enumerate(doc):
            imagens = page.get_images(full=True)
            
            for img_index, img in enumerate(imagens):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                
                image_name = (
                    f"page_{page_index + 1}_img_{img_index + 1}.{image_ext}"
                )
                
                image_path = imagens_pdf_dir / image_name
                with open(image_path, "wb") as f:
                    f.write(image_bytes)
                    
                imagens_extraidas += 1
                
        return imagens_extraidas