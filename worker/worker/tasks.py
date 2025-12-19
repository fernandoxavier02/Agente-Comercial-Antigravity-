import os
import uuid
from datetime import datetime, timezone
import requests
from dotenv import load_dotenv
from .celery_app import celery_app

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

# MVP: fonte mock (substituir por conectores reais respeitando ToS)
MOCK_ITEMS = [
    {
        "source": "web_forum",
        "url": "https://example.com/thread/123",
        "author_handle": "user123",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "text": "Alguém já conseguiu melhorar melasma? Depois dos 40 piorou muito."
    },
    {
        "source": "web_forum",
        "url": "https://example.com/thread/456",
        "author_handle": "user456",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "text": "Estou em dúvida entre bioestimulador e laser para flacidez no rosto. Vale a pena?"
    }
]

@celery_app.task
def run_mock_ingestion():
    """Pipeline mock: cria leads sintéticos e manda para a API.
    Depois substitua por:
    1) collector (fontes públicas)
    2) classifier (LLM + schema)
    3) composer (LLM + schema)
    """
    for item in MOCK_ITEMS:
        lead_id = f"L{uuid.uuid4().hex[:8]}"
        lead = {
            "lead_id": lead_id,
            "source": item["source"],
            "source_url": item["url"],
            "author_handle": item["author_handle"],
            "timestamp": item["timestamp"],
            "text_excerpt": item["text"][:1500],
            "pain_point": {"label": "melasma/manchas" if "melasma" in item["text"].lower() else "flacidez/colágeno", "confidence": 0.75},
            "intent_stage": {"label": "consideration", "confidence": 0.7},
            "maturity": {"label": "beginner", "score": 35},
            "scores": {"fit": 75, "intent": 70, "urgency": 40, "risk": 10, "lead_score": 67, "evidence_quality": 70},
            "evidence": [{"text": item["text"][:200], "url": item["url"]}],
            "risk_flags": [],
            "version": os.getenv("CLASSIFIER_PROMPT_VERSION", "v0.1"),
        }
        r = requests.post(f"{API_BASE_URL}/leads", json=lead, timeout=30)
        r.raise_for_status()

        # gerar draft via API
        d = requests.post(f"{API_BASE_URL}/leads/{lead_id}/drafts", timeout=30)
        d.raise_for_status()

    return {"ok": True, "count": len(MOCK_ITEMS)}
