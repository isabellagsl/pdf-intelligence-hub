"""
Módulo de processamento de linguagem natural focado na normalização de texto bruto.
Aplica regras baseadas em Expressões Regulares (Regex) para corrigir ruídos oriundos do formato PDF.
"""

import re

def limpar_texto_basico(texto_bruto: str) -> str:
    """
    Executa transformações sequenciais para sanitizar o texto extraído do documento vetorial.
    PDFs geralmente introduzem quebras arbitrárias e espaços em excesso que prejudicam análises semânticas.
    
    Args:
        texto_bruto (str): A string original capturada diretamente do buffer do PyMuPDF.
        
    Returns:
        str: Texto contínuo padronizado para injeção limpa.
    """
    # 1. Recomposição Silábica (De-hyphenation)
    # Padrão: localiza uma palavra incompleta seguida de hífen (-), quebra de linha opcional (\n) e o restante da palavra.
    # Exemplo PDF: "in- \nteligência" -> Substituição: "inteligência" (junta grupo 1 \1 e grupo 2 \2)
    texto = re.sub(r'(\w+)-\s*\n\s*(\w+)', r'\1\2', texto_bruto)

    # 2. Compressão Vertical (Remoção de parágrafos vazios repetidos)
    # Padrão: substitui duas ou mais quebras de linha subjacentes (\n+) por uma quebra simples (\n)
    texto = re.sub(r'\n+', '\n', texto)

    # 3. Compressão Horizontal (Remoção de tabulações e recuos fantasmas)
    # Padrão: substitui qualquer combinação de espaços em branco ou tabs por um único espaço
    texto = re.sub(r'[ \t]+', ' ', texto)

    # 4. Trimming Topológico
    # Padrão: Remove resquícios invisíveis de espaços em branco presentes no limite (início/fim) de cada linha gerada
    linhas = [linha.strip() for linha in texto.split('\n')]
    
    # Consolida a lista de linhas processadas novamente em uma string sólida
    return '\n'.join(linhas).strip()