from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Literal, List
from .core.config import settings
from .core.database import get_db
from .store import LeadStore
from .schemas import LeadClassification, OutreachDraft, FeedbackEvent
from .services.pipeline import generate_outreach_draft
from .api.demo import router as demo_router
from datetime import datetime, timezone

from fastapi.responses import JSONResponse

app = FastAPI(title=settings.APP_NAME, version="0.1.0")

@app.exception_handler(Exception)
async def debug_exception_handler(request, exc):
    import traceback
    return JSONResponse(
        status_code=500,
        content={"message": str(exc), "traceback": traceback.format_exc()},
    )

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(demo_router, prefix="/api", tags=["demo"])

@app.get("/health")
def health():
    return {"status": "ok", "time": datetime.now(timezone.utc).isoformat()}

@app.post("/admin/init-db")
async def init_database():
    """Endpoint de emergência para inicializar tabelas remotamente."""
    from .core.database import get_engine, Base
    engine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all) # Create only, dont drop
    return {"status": "tables_created", "tables": list(Base.metadata.tables.keys())}

@app.post("/leads", response_model=LeadClassification)
async def create_lead(lead: LeadClassification, db: AsyncSession = Depends(get_db)):
    store = LeadStore(db)
    await store.save_lead(lead)
    return lead

@app.get("/leads", response_model=List[LeadClassification])
async def list_leads(
    sort_by: Literal["timestamp", "wealth_score", "visual_fit_score", "lead_score"] = "timestamp",
    limit: int = 50,
    db: AsyncSession = Depends(get_db)
):
    store = LeadStore(db)
    return await store.list_leads(limit=limit, sort_by=sort_by)

@app.get("/leads/{lead_id}", response_model=LeadClassification)
async def get_lead(lead_id: str, db: AsyncSession = Depends(get_db)):
    store = LeadStore(db)
    lead = await store.get_lead(lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead

@app.post("/leads/{lead_id}/draft", response_model=OutreachDraft)
async def create_draft(lead_id: str, db: AsyncSession = Depends(get_db)):
    store = LeadStore(db)
    lead = await store.get_lead(lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    draft = await generate_outreach_draft(lead)
    await store.save_draft(draft)
    return draft
