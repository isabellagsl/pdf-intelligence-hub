"""
Módulo especialista para identificação e parser estrutural de matrizes de dados (tabelas) em PDFs.
"""

import pandas as pd
from loguru import logger

class TableExtractor:
    """
    Classe projetada para buscar arranjos geométricos que configuram tabelas
    e transmutá-los para formatos semânticos puros (Markdown).
    """
    
    def __init__(self):
        # Construtor vazio no momento, pode ser utilizado para injetar parâmetros de OCR ou modelos visuais
        pass

    def extrair_tabelas(self, pagina):
        """
        Inspeciona a topologia de uma página buscando linhas convergentes que denotam tabelas.
        
        A extração ocorre em duas fases de conversão:
        1. PDF-Layout -> DataFrame do Pandas (para manipulação estruturada)
        2. Pandas -> Markdown Tabular (para preservação do formato perante sistemas downstream como RAG)
        
        Args:
            pagina: O objeto da página capturado pela iteração no documento PyMuPDF.
            
        Returns:
            list[str]: Uma coleção de strings contendo as tabelas renderizadas em padrão Markdown.
        """
        num_pag = pagina.number + 1
        
        # A engine interna do PyMuPDF realiza inferência sobre linhas verticais/horizontais e blocos de texto
        tabs = pagina.find_tables()
        
        tabelas_markdown = []

        for i, tab in enumerate(tabs):
            # O método to_pandas() mapeia coordenadas vetoriais para uma estrutura de Data Frame 2D
            df = tab.to_pandas()
            
            # Validação para evitar processar entidades nulas ou grades vazias
            if df.empty:
                continue

            # Conversão final para Markdown usando a biblioteca auxiliar tabulate (executada nativamente pelo Pandas)
            # index=False evita a inserção da numeração da linha como coluna na tabela final
            md_table = df.to_markdown(index=False)
            tabelas_markdown.append(md_table)
            
            logger.info(f"Matriz de dados (Tabela {i+1}) mapeada e extraída da página {num_pag}.")
            
        return tabelas_markdown