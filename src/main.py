"""
Módulo principal de orquestração do pipeline de extração de PDFs.
Este script atua como o ponto de entrada (entry point) da aplicação,
coordenando as chamadas para extratores e processadores.
"""

import fitz
import os
import argparse

# Oculta avisos inofensivos de formatação interna do MuPDF
fitz.TOOLS.mupdf_display_errors(False)
from src.processors.cleaner import limpar_texto_basico
from src.utils.logger import setup_logger
from src.extractors.image_extractor import ImageExtractor
from src.extractors.table_extractor import TableExtractor

log = setup_logger()

def pipeline_completo(caminho_pdf, output_base):
    """
    Executa o processo de extração completo de um documento PDF.
    
    A execução segue o padrão sequencial:
    1. Validação de existência do arquivo.
    2. Instanciação dos extratores (Tabelas e Imagens).
    3. Criação da estrutura de diretórios para output.
    4. Iteração sobre as páginas do documento.
    5. Extração e consolidação (Texto + Tabelas) em formato Markdown.
    
    Args:
        caminho_pdf (str): Caminho absoluto ou relativo para o arquivo PDF.
        output_base (str): Diretório raiz onde os resultados serão armazenados.
    """
    try:
        # Validação inicial para evitar quebra caso o arquivo não exista
        if not os.path.exists(caminho_pdf):
            log.error(f"Arquivo não encontrado: {caminho_pdf}")
            return

        # Abertura do documento utilizando o PyMuPDF (fitz)
        doc = fitz.open(caminho_pdf)
        
        # Inicialização das classes especialistas responsáveis por imagens e tabelas
        img_ext = ImageExtractor(output_dir=os.path.join(output_base, "images"))
        tab_ext = TableExtractor()
        
        # Criação do diretório para arquivos de texto, evitando erro caso a pasta já exista
        text_output_dir = os.path.join(output_base, "text")
        os.makedirs(text_output_dir, exist_ok=True)

        log.info(f"Iniciando: {os.path.basename(caminho_pdf)} ({len(doc)} páginas)")

        # Iteração página por página para extração controlada e em memória
        for pagina in doc:
            num_pag = pagina.number + 1
            
            # Etapa de extração utilizando os métodos especialistas
            tabelas = tab_ext.extrair_tabelas(pagina)
            texto_limpo = limpar_texto_basico(pagina.get_text("text"))
            img_ext.extrair_da_pagina(doc, pagina)

            # Estruturação e salvamento dos dados agregados em formato Markdown (.md)
            nome_txt = f"pagina_{num_pag}.md"
            caminho_save = os.path.join(text_output_dir, nome_txt)
            
            with open(caminho_save, "w", encoding="utf-8") as f:
                # O formato Markdown facilita a injeção em bancos vetoriais para aplicações de IA
                f.write(f"# Extração Página {num_pag}\n\n")
                f.write("## Texto\n" + texto_limpo + "\n\n")
                if tabelas:
                    f.write("## Tabelas\n" + "\n\n".join(tabelas))

        log.success(f"Sucesso! Resultados armazenados no diretório: {output_base}")

    except Exception as e:
        # O bloco except garante que falhas estruturais em PDFs quebrados não encerrem a aplicação silenciosamente
        log.critical(f"Erro inesperado no pipeline de extração: {e}")

def main():
    """
    Função principal que encapsula a lógica de linha de comando (CLI).
    Utiliza argparse para prover uma interface amigável via terminal.
    """
    # Definição dos argumentos aceitos via linha de comando
    parser = argparse.ArgumentParser(description="PDF Intelligence Hub - Pipeline Orquestrador")
    
    # Argumento posicional obrigatório
    parser.add_argument("arquivo", help="Caminho para o arquivo PDF a ser processado")
    
    # Argumento opcional com valor padrão
    parser.add_argument("--out", default="output", help="Diretório de saída (padrão: output)")

    args = parser.parse_args()

    # Repasse dos argumentos validados para a orquestração
    pipeline_completo(args.arquivo, args.out)

if __name__ == "__main__":
    # Garante que o pipeline só inicie se o script for invocado diretamente via terminal
    main()