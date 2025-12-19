# Guia de Deploy para Nuvem (Railway.app)

Nao seria melhor ja colocar o back end e o front end na nuvem? **Sim!** Isso permite que os scrapers rodem 24/7 e o dashboard seja acessível de qualque lugar.

Preparei o repositório para deploy fácil no **Railway** (recomendado pela simplicidade e suporte a Python/Celery/Postgres).

## 1. Backend + Worker + Database (Railway)

O Railway detectará automaticamente o arquivo `Procfile` e `requirements.txt` na raiz.

1. Crie uma conta em [Railway.app](https://railway.app/).
2. Clique em **+ New Project** -> **GitHub Repo** -> Selecione este repositório.
3. O Railway vai identificar o projeto.
4. **Adicione um Database**:
    * No painel do projeto, clique em **+ New** -> **Database** -> **PostgreSQL**.
    * Faça o mesmo para **Redis** (necessário para o Celery).
5. **Variáveis de Ambiente**:
    * Vá em **Settings** -> **Variables**.
    * Adicione todas as variáveis do seu `.env` local (OPENAI_API_KEY, etc).
    * **Importante**: O Railway fornece `DATABASE_URL` e `REDIS_URL` automaticamente. Você deve usar essas (ele injeta `DATABASE_URL`, o código já lê isso).
    * Ajuste `CELERY_BROKER_URL` para o valor de `REDIS_URL`.
6. **Inicialização do Banco**:
    * O banco começa vazio. Você pode conectar nele externamente (usando as credenciais do Railway) e rodar o script localmente apontando para lá, ou adicionar um "Start Command" customizado.
    * Recomendado: Adicione um "Service" temporário ou rode via CLI do Railway: `railway run python backend/init_db.py`.

## 2. Frontend (Vercel)

1. Crie conta em [Vercel.com](https://vercel.com).
2. **Add New Project** -> Importe o mesmo repositório do GitHub.
3. Em **Root Directory**, edite para selecionar a pasta `dashboard`. O Vercel precisa saber que o Next.js está lá dentro.
4. Em **Environment Variables**, adicione (se necessário):
    * `NEXT_PUBLIC_API_URL`: A URL do seu backend no Railway (ex: `https://seu-projeto-railway.app`).

## 3. Benefícios

* **Persistent**: Seus leads não somem.
* **Background Jobs**: O Worker roda separado da API.
* **Escalável**: Aumente a memória se precisar processar muitas fotos.
