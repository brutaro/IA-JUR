#!/usr/bin/env python3
"""
IA-JUR - Sistema de Pesquisa Jurídica Inteligente
Servidor web principal para deploy em produção
"""

import os
import sys
from pathlib import Path

# Adiciona o diretório src ao path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from web.main import app
import uvicorn

def main():
    """Função principal para iniciar o servidor"""
    print("🚀 IA-JUR iniciando...")
    
    # Configurações de produção
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    reload = os.getenv("DEBUG", "false").lower() == "true"
    
    print(f"🌐 Servidor configurado para: {host}:{port}")
    print(f"🔧 Modo debug: {'Ativado' if reload else 'Desativado'}")
    
    # Inicia o servidor
    uvicorn.run(
        "web.main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )

if __name__ == "__main__":
    main()
