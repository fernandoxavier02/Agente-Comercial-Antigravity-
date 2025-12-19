# Guia de Deploy: Firebase + Cloud Run + Supabase

## Arquitetura Definida

* **Frontend**: Firebase Hosting.
* **Backend**: Google Cloud Run.
* **Database**: Supabase (PostgreSQL).

## Passo 1: Configurar Supabase

1. Acesse [Supabase.com](https://supabase.com) e crie um projeto novo.
2. Vá em **Project Settings** -> **Database**.
3. Copie a **Connection String (URI)**.
    * Deve parecer com: `postgresql://postgres:[PASSWORD]@db.PROJECT_ID.supabase.co:5432/postgres`
    * **Importante**: Adicione `?sslmode=require` ao final se não tiver.
4. Substitua a senha real no lugar de `[PASSWORD]`.
5. (Opcional) configure o MCP em `.vscode/mcp.json` com essa URL para gerenciar o banco pelo editor.

## Passo 2: Instalar Ferramentas

Execute o script auxiliar:

```powershell
./setup_infra.ps1
```

Ou instale manualmente:

* [Google Cloud CLI](https://cloud.google.com/sdk/docs/install)
* Firebase: `npm install -g firebase-tools`

## Passo 3: Deploy Backend (Cloud Run)

1. Login:

    ```bash
    gcloud auth login
    gcloud config set project SEU_PROJETO_GCP
    ```

2. Deploy API:

    ```bash
    gcloud run deploy estetica-api --source . --region us-central1 --allow-unauthenticated --set-env-vars="DATABASE_URL=sua_url_supabase_aqui"
    ```

3. Anote a URL gerada (ex: `https://estetica-api.a.run.app`).

## Passo 4: Deploy Frontend (Firebase)

1. Login:

    ```bash
    firebase login
    ```

2. Configure a URL da API no arquivo `dashboard/.env.production`:

    ```
    NEXT_PUBLIC_API_URL=https://estetica-api.a.run.app
    ```

3. Deploy:

    ```bash
    firebase deploy --only hosting
    ```

## Pronto

Seu SaaS está rodando com Frontend rápido no Firebase, Backend escalável no Cloud Run e Banco de Dados robusto no Supabase.
