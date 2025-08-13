#!/usr/bin/env python3
"""
IA-JUR - Sistema de Pesquisa Jurídica Inteligente
Backend FastAPI integrado com o agente de pesquisa existente
"""

import os
import sys
import time
import json
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path

# Adiciona o diretório raiz ao path para importar os módulos do agente
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn

# Importa o agente de pesquisa existente
from src.agents.simple_orchestrator import SimpleLegalOrchestrator

# Configuração do FastAPI
app = FastAPI(
    title="IA-JUR",
    description="Sistema de Pesquisa Jurídica Inteligente",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuração de templates e arquivos estáticos
# Usa caminhos absolutos para evitar problemas de diretório
current_dir = Path(__file__).parent
templates = Jinja2Templates(directory=str(current_dir / "templates"))
app.mount("/static", StaticFiles(directory=str(current_dir / "static")), name="static")

# Modelos Pydantic
class ConsultaRequest(BaseModel):
    pergunta: str

class ConsultaResponse(BaseModel):
    resumo: str
    resposta_completa: str
    fontes: int  # Número de fontes encontradas
    workflow_id: str
    duracao: float
    timestamp: str

class MetricasResponse(BaseModel):
    total_consultas: int
    consultas_pesquisa: int
    tempo_medio: float
    fontes_totais: int
    uptime: str

# Variáveis globais para métricas
metrics = {
    "total_consultas": 0,
    "consultas_pesquisa": 0,
    "tempo_medio": 0.0,
    "fontes_totais": 0,
    "start_time": time.time(),
    "consultas_tempo": []
}

# Instância do orquestrador (inicializada lazy)
orchestrator = None

def configurar_llms():
    """Configura os LLMs para o agente pesquisador"""
    # Configuração padrão usando Gemini
    default_config = {
        'provider': 'gemini',
        'model': 'gemini-2.5-flash',
        'api_key': os.getenv('GEMINI_API_KEY'),
        'temperature': 0.1,
        'max_tokens': 4000
    }

    # Configurações específicas para o agente pesquisador
    llm_configs = {
        'default': default_config,
        'research': {
            **default_config,
            'temperature': 0.1,
            'max_tokens': 6000
        }
    }

    return llm_configs

def get_orchestrator():
    """Inicializa o orquestrador de forma lazy"""
    global orchestrator
    if orchestrator is None:
        try:
            # Configura LLMs
            llm_configs = configurar_llms()

            # Cria orquestrador com configuração correta
            orchestrator = SimpleLegalOrchestrator(llm_configs, output_dir='./respostas')
            print("✅ Orquestrador inicializado com sucesso")
        except Exception as e:
            print(f"❌ Erro ao inicializar orquestrador: {e}")
            raise
    return orchestrator

@app.on_event("startup")
async def startup_event():
    """Evento de inicialização da aplicação"""
    print("🚀 IA-JUR iniciando...")
    print("📁 Diretório de trabalho:", os.getcwd())
    print("🔧 Verificando dependências...")

    try:
        # Testa a inicialização do orquestrador
        get_orchestrator()
        print("✅ Sistema IA-JUR iniciado com sucesso!")
    except Exception as e:
        print(f"❌ Erro na inicialização: {e}")
        print("⚠️  O sistema pode não funcionar corretamente")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Página principal do IA-JUR"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/consulta", response_model=ConsultaResponse)
async def processar_consulta(consulta: ConsultaRequest):
    """
    Processa uma consulta jurídica usando o agente existente
    """
    global metrics

    if not consulta.pergunta.strip():
        raise HTTPException(status_code=400, detail="Pergunta não pode estar vazia")

    start_time = time.time()

    try:
        # Obtém o orquestrador
        orch = get_orchestrator()

        # Processa a consulta
        print(f"🔍 Processando consulta: {consulta.pergunta[:100]}...")

        # Chama o orquestrador existente (é assíncrono)
        resultado = await orch.process_query(consulta.pergunta)

        end_time = time.time()
        duracao = end_time - start_time

        # Extrai informações do resultado (mapeia campos corretos)
        resumo = resultado.get('summary', 'Resumo não disponível')
        resposta_completa = resultado.get('formatted_response', 'Resposta não disponível')
        fontes = resultado.get('sources_found', 0)  # Número real de fontes encontradas
        workflow_id = resultado.get('metadata', {}).get('workflow_id', f"wf_{int(time.time())}")

        # Atualiza métricas
        metrics["total_consultas"] += 1
        metrics["consultas_pesquisa"] += 1
        metrics["fontes_totais"] += fontes  # fontes é um número, não uma lista
        metrics["consultas_tempo"].append(duracao)

        # Calcula tempo médio (últimas 10 consultas)
        if len(metrics["consultas_tempo"]) > 10:
            metrics["consultas_tempo"] = metrics["consultas_tempo"][-10:]
        metrics["tempo_medio"] = sum(metrics["consultas_tempo"]) / len(metrics["consultas_tempo"])

        print(f"✅ Consulta processada em {duracao:.2f}s")

        return ConsultaResponse(
            resumo=resumo,
            resposta_completa=resposta_completa,
            fontes=fontes,
            workflow_id=workflow_id,
            duracao=duracao,
            timestamp=datetime.now().isoformat()
        )

    except Exception as e:
        end_time = time.time()
        duracao = end_time - start_time

        print(f"❌ Erro ao processar consulta: {e}")

        # Retorna erro estruturado
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao processar consulta: {str(e)}"
        )

@app.get("/api/metricas", response_model=MetricasResponse)
async def obter_metricas():
    """
    Retorna métricas do sistema em tempo real
    """
    global metrics

    uptime = time.time() - metrics["start_time"]
    uptime_hours = int(uptime // 3600)
    uptime_minutes = int((uptime % 3600) // 60)
    uptime_str = f"{uptime_hours}h {uptime_minutes}m"

    return MetricasResponse(
        total_consultas=metrics["total_consultas"],
        consultas_pesquisa=metrics["consultas_pesquisa"],
        tempo_medio=round(metrics["tempo_medio"], 2),
        fontes_totais=metrics["fontes_totais"],
        uptime=uptime_str
    )

@app.get("/api/health")
async def health_check():
    """
    Verificação de saúde do sistema
    """
    try:
        # Testa se o orquestrador está funcionando
        orch = get_orchestrator()

        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "orchestrator": "operational",
            "version": "1.0.0"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "error": str(e),
            "version": "1.0.0"
        }

@app.get("/api/info")
async def system_info():
    """
    Informações do sistema
    """
    return {
        "sistema": "IA-JUR",
        "versao": "1.0.0",
        "descricao": "Sistema de Pesquisa Jurídica Inteligente",
        "tecnologia": "FastAPI + Python + IA Gemini",
        "integracao": "Agente de Pesquisa Jurídica",
        "timestamp": datetime.now().isoformat()
    }

# Middleware para logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware para logging de requisições"""
    start_time = time.time()

    # Processa a requisição
    response = await call_next(request)

    # Calcula duração
    duration = time.time() - start_time

    # Log da requisição
    print(f"📝 {request.method} {request.url.path} - {response.status_code} - {duration:.3f}s")

    return response

# Tratamento de erros personalizado
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    """Handler para páginas não encontradas"""
    return JSONResponse(
        status_code=404,
        content={
            "error": "Página não encontrada",
            "path": request.url.path,
            "message": "A página solicitada não existe no IA-JUR"
        }
    )

@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    """Handler para erros internos"""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Erro interno do servidor",
            "path": request.url.path,
            "message": "Ocorreu um erro interno no IA-JUR"
        }
    )

if __name__ == "__main__":
    print("🚀 Iniciando IA-JUR...")
    print("📁 Diretório:", os.getcwd())
    print("🌐 Servidor web iniciando em http://localhost:8000")

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )
