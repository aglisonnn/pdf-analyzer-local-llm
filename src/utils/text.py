import re
from collections import Counter
from typing import Dict, Any

# Quarto, quinto e segundo requisito de analise de de PDF
def calcular_estatisticas(text: str) -> Dict[str, Any]:
    """
    Recebe o texto bruto e retorna um dicionário com todas as estatíticas
    """
    
    # Normalização
    text_lower = text.lower()
    
    # Regex para capturar as palavras
    palavras_brutas = re.findall(r'[a-zá-ú]+', text_lower)
    
    # Definir stopwords
    stopwords = {
        "a", "o", "e", "é", "de", "do", "da", "em", "um", "uma", "que", "com", "não", 
        "para", "os", "as", "dos", "das", "se", "na", "no", "por", "mais", "como", "mas", "ao"
    }
    
    # Filtragem
    palavras_uteis = [
        p for p in palavras_brutas 
        if p not in stopwords and len(p) > 1
        ]
    
    # Cálculos 
    stats = {
        "total_palavras": len(palavras_brutas),
        "vocabulario_unico": len(set(palavras_uteis)),
        "top_10": Counter(palavras_uteis).most_common(10)
    }
    
    return stats