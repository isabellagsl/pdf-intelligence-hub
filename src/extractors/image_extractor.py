"""
Módulo especialista para extração de imagens embutidas em documentos PDF.
"""

import fitz
import os
from loguru import logger

class ImageExtractor:
    """
    Classe responsável por identificar e salvar objetos de imagem contidos nas páginas de um PDF.
    """
    
    def __init__(self, output_dir="output/images"):
        self.output_dir = output_dir
        # Garante a existência da infraestrutura de diretórios (mkdir -p)
        os.makedirs(self.output_dir, exist_ok=True)

    def extrair_da_pagina(self, doc, pagina):
        """
        Extrai todas as imagens vinculadas a uma página específica e as salva em disco.
        
        Args:
            doc: O objeto do documento PDF gerado pelo PyMuPDF.
            pagina: O objeto correspondente à página atual sob iteração.
            
        Returns:
            int: A quantidade de imagens extraídas e salvas na referida página.
        """
        # Coleta uma matriz de metadados referentes às imagens na página
        images_list = pagina.get_images(full=True)
        num_pagina = pagina.number + 1
        
        if not images_list:
            logger.debug(f"Página {num_pagina}: Nenhuma imagem encontrada.")
            return 0

        for img_index, img in enumerate(images_list):
            # O índice 0 (XREF) atua como um ID único do recurso (imagem) dentro do arquivo PDF
            xref = img[0]
            
            # Utiliza o XREF para extrair os bytes binários brutos da imagem
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            extensao = base_image["ext"]  # Pode ser png, jpeg, tiff, etc.
            
            # Padronização da nomenclatura para facilitar rastreamento e auditoria posterior
            nome_arquivo = f"pag_{num_pagina}_img_{img_index + 1}.{extensao}"
            caminho_final = os.path.join(self.output_dir, nome_arquivo)
            
            # Gravação em formato binário ('wb') para não corromper o cabeçalho da imagem
            with open(caminho_final, "wb") as f:
                f.write(image_bytes)
            
            logger.info(f"Imagem salva com sucesso: {nome_arquivo} (Referência XREF: {xref})")
            
        return len(images_list)