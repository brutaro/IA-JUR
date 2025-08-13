# 🤖 Sistema de Agentes Jurídicos - Versão Simplificada

Sistema de inteligência artificial para pesquisa jurídica automatizada, utilizando modelos Gemini da Google e base de conhecimento vetorial Pinecone.

## 🌟 Características

* **Agente Pesquisador Inteligente**: Análise automática de documentos jurídicos
* **Interface Web Moderna**: Frontend responsivo para consultas online
* **Base de Conhecimento Vetorial**: Pesquisa semântica em documentos oficiais
* **Respostas Formatadas**: Saída estruturada em formato documental
* **API REST Completa**: Endpoints para integração com outros sistemas
* **Deploy Automático**: Configuração para Railway e outras plataformas

## 🚀 Deploy Rápido

### Railway (Recomendado)

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/new?template=https://github.com/brutaro/IA-JUR)

### Heroku

[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/brutaro/IA-JUR)

## 🛠️ Tecnologias

* **Backend**: Python 3.10+, FastAPI, Uvicorn
* **IA**: Google Gemini 2.5 Pro/Flash
* **Base de Dados**: Pinecone (vetorial)
* **Frontend**: HTML5, CSS3, JavaScript ES6+
* **Deploy**: Railway, Docker, Heroku

## 📋 Pré-requisitos

* Python 3.8+
* Chave API Google Gemini
* Conta Pinecone com índice configurado
* Conta Railway/Heroku para deploy

## 🔧 Instalação Local

### 1. Clone o repositório

```bash
git clone https://github.com/brutaro/IA-JUR.git
cd IA-JUR
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Configure as variáveis de ambiente

```bash
cp env.example .env
# Edite .env com suas chaves API
```

### 4. Execute o servidor

```bash
python start_web_server.py
```

Acesse: http://127.0.0.1:8000

## 🌐 Deploy na Nuvem

### Railway (Recomendado)

1. **Fork** este repositório
2. Acesse [Railway](https://railway.app)
3. Clique em "New Project" → "Deploy from GitHub repo"
4. Selecione seu fork
5. Configure as variáveis de ambiente:
   * `GEMINI_API_KEY`
   * `PINECONE_API_KEY`
   * `PINECONE_ENVIRONMENT`
   * `PINECONE_INDEX_NAME`
6. Deploy automático!

### Heroku

1. **Fork** este repositório
2. Acesse [Heroku](https://heroku.com)
3. Crie nova app
4. Conecte com GitHub
5. Configure as variáveis de ambiente
6. Deploy!

## 🔌 API Endpoints

### Consulta Jurídica

```http
POST /api/consulta
Content-Type: application/json

{
    "pergunta": "Sua pergunta jurídica aqui"
}
```

### Métricas do Sistema

```http
GET /api/metricas
```

### Status do Sistema

```http
GET /api/health
GET /api/status
```

## 📱 Interface Web

* **Responsiva**: Funciona em desktop, tablet e mobile
* **Intuitiva**: Menu claro e navegação simples
* **Funcional**: Formulário de consulta com validação
* **Resultados**: Exibição formatada das respostas

## 🧪 Testes

### Testes Automatizados

```bash
python test_frontend.py
```

### Testes Manuais

1. Acesse cada seção do menu
2. Teste formulário com dados válidos/inválidos
3. Verifique responsividade
4. Teste funcionalidades de copiar e navegação

## 📊 Monitoramento

* **Health Checks**: Verificação automática de saúde
* **Logs Estruturados**: Logs detalhados para produção
* **Métricas**: Contadores de uso e performance
* **Alertas**: Notificações de erro automáticas

## 🔒 Segurança

* **Validação de Entrada**: Sanitização de dados
* **CORS Configurável**: Controle de origens
* **Rate Limiting**: Proteção contra abuso
* **Logs de Auditoria**: Rastreamento de consultas

## 🚀 Roadmap

* Autenticação de usuários
* Histórico de consultas
* Exportação em múltiplos formatos
* API para terceiros
* Dashboard administrativo
* Integração com sistemas jurídicos

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 📞 Suporte

* **Issues**: [GitHub Issues](https://github.com/brutaro/IA-JUR/issues)
* **Documentação**: [Wiki](https://github.com/brutaro/IA-JUR/wiki)

## 🙏 Agradecimentos

* Google Gemini pela tecnologia de IA
* Pinecone pela base de dados vetorial
* FastAPI pela framework web
* Comunidade open source

---

**⭐ Se este projeto te ajudou, considere dar uma estrela no repositório!**

**🚀 Desenvolvido com ❤️ para simplificar a pesquisa jurídica através de IA**
