#!/bin/bash
# Script de deploy automatizado para Railway
# IA-JUR - Sistema de Pesquisa Jurídica Inteligente

echo "🚀 DEPLOY AUTOMATIZADO PARA RAILWAY"
echo "====================================="

# Verifica se o git está configurado
if ! git config --get user.name > /dev/null 2>&1; then
    echo "❌ Git não está configurado"
    echo "💡 Configure com: git config --global user.name 'Seu Nome'"
    echo "💡 Configure com: git config --global user.email 'seu@email.com'"
    exit 1
fi

# Verifica se estamos no diretório correto
if [ ! -f "start_web_server.py" ]; then
    echo "❌ Execute este script do diretório deploy_github/"
    exit 1
fi

echo "📁 Diretório atual: $(pwd)"
echo "🔍 Verificando arquivos essenciais..."

# Lista de arquivos essenciais
ESSENTIAL_FILES=(
    "start_web_server.py"
    "requirements.txt"
    "railway.json"
    "src/agents/simple_orchestrator.py"
    "web/main.py"
    "web/templates/index.html"
    "web/static/css/style.css"
    "web/static/js/app.js"
)

# Verifica arquivos essenciais
MISSING_FILES=()
for file in "${ESSENTIAL_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        MISSING_FILES+=("$file")
    fi
done

if [ ${#MISSING_FILES[@]} -gt 0 ]; then
    echo "❌ Arquivos essenciais faltando:"
    for file in "${MISSING_FILES[@]}"; do
        echo "    - $file"
    done
    exit 1
fi

echo "✅ Todos os arquivos essenciais encontrados"

# Inicializa git se necessário
if [ ! -d ".git" ]; then
    echo "🔧 Inicializando repositório Git..."
    git init
    git add .
    git commit -m "🚀 Deploy inicial IA-JUR"
fi

# Verifica status do git
echo "📊 Status do Git:"
git status --short

echo ""
echo "🎯 PRÓXIMOS PASSOS PARA DEPLOY:"
echo "================================="
echo ""
echo "1. 📤 Push para GitHub:"
echo "   git remote add origin https://github.com/brutaro/IA-JUR.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "2. 🌐 Deploy no Railway:"
echo "   - Acesse: https://railway.app"
echo "   - Clique em 'New Project'"
echo "   - Selecione 'Deploy from GitHub repo'"
echo "   - Escolha o repositório: brutaro/IA-JUR"
echo "   - Configure as variáveis de ambiente:"
echo "     * GEMINI_API_KEY"
echo "     * PINECONE_API_KEY"
echo "     * PINECONE_ENVIRONMENT"
echo "     * PINECONE_INDEX_NAME"
echo ""
echo "3. 🔧 Configurações Railway:"
echo "   - Builder: NIXPACKS (automático)"
echo "   - Build Command: (deixar vazio - automático)"
echo "   - Start Command: python start_web_server.py"
echo "   - Health Check Path: /api/health"
echo "   - NIXPACKS detecta automaticamente Python e dependências!"
echo ""
echo "✅ Script de deploy concluído!"
echo "🚀 Agora siga os passos acima para finalizar o deploy"
