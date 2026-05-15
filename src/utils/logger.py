"""
Módulo utilitário para instrumentação e observabilidade.
Fornece um padrão Singleton arquitetural para o gerenciamento global de logs através da biblioteca 'loguru'.
"""

from loguru import logger
import sys

def setup_logger():
    """
    Configura múltiplos destinos (handlers) e formatações para o rastreamento da aplicação.
    
    A implementação substitui a biblioteca 'logging' nativa do Python por conta de sua
    sintaxe concisa, processamento assíncrono e formatação automatizada (coloração).
    
    Returns:
        O objeto global e parametrizado do logger.
    """
    # Remove a injeção inicial padrão para prevenir a duplicação na emissão de mensagens
    logger.remove()
    
    # Handler 1: Standard Error (Terminal)
    # Objetivo: Feedback imediato da execução durante o tempo de execução (runtime).
    # Tags XML (<green>, <cyan>) são nativas do loguru para destacar informações visuais.
    logger.add(
        sys.stderr, 
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>",
        level="INFO"
    )
    
    # Handler 2: Persistência Física em Disco (.log)
    # Objetivo: Rastreabilidade passiva de histórico e auditoria (debug assíncrono).
    # Implementa rotação inteligente (rotation) com compactação de arquivos antigos (compression),
    # prevenindo que logs massivos estourem o espaço de alocação em disco a longo prazo.
    logger.add(
        "logs/pipeline.log", 
        rotation="10 MB", 
        retention="10 days", 
        compression="zip",
        level="DEBUG"
    )
    
    return logger