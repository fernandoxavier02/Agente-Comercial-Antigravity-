# Worker (pipeline)

Este worker executa tarefas assíncronas (Celery). No MVP, existe um `run_mock_ingestion` para validar:
- contratos JSON
- armazenamento
- dashboard

Depois você substitui o mock por:
- collectors reais (fontes públicas e permitidas)
- classificador via LLM (prompts + validação JSON Schema)
- composer via LLM (prompts + validação JSON Schema)

Rodar (após subir Redis + API):
```bash
celery -A worker.celery_app worker --loglevel=INFO
celery -A worker.celery_app call worker.tasks.run_mock_ingestion
```
