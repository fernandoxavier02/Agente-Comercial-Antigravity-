from __future__ import annotations
from typing import Optional, List, Literal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from .models import Lead, Draft, Feedback
from .schemas import LeadClassification, OutreachDraft, FeedbackEvent

class LeadStore:
    """Camada de Acesso a Dados (SQLAlchemy)"""
    
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save_lead(self, lead_data: LeadClassification) -> None:
        from fastapi.encoders import jsonable_encoder
        
        # Verifica se já existe
        result = await self.db.execute(select(Lead).where(Lead.lead_id == lead_data.lead_id))
        existing_lead = result.scalars().first()

        # Radical conversion to ensure JSON campatibility
        lead_dict = jsonable_encoder(lead_data)
        
        # Restore datetime objects for SQLAlchemy
        lead_dict['timestamp'] = lead_data.timestamp

        # DEBUG: Remove profile_image_url to check if column exists
        if 'profile_image_url' in lead_dict:
            del lead_dict['profile_image_url']
        
        if existing_lead:
            # Update
            for key, value in lead_dict.items():
                setattr(existing_lead, key, value)
        else:
            # Insert
            new_lead = Lead(**lead_dict)
            self.db.add(new_lead)
        
        await self.db.commit()

    async def get_lead(self, lead_id: str) -> Optional[LeadClassification]:
        result = await self.db.execute(select(Lead).where(Lead.lead_id == lead_id))
        lead = result.scalars().first()
        if not lead:
            return None
        return LeadClassification.model_validate(lead)

    async def list_leads(
        self, 
        limit: int = 50, 
        offset: int = 0, 
        sort_by: Literal["timestamp", "wealth_score", "visual_fit_score", "lead_score"] = "timestamp"
    ) -> List[LeadClassification]:
        
        stmt = select(Lead)
        
        # Sorting logic - um pouco mais complexa com JSON fields no SQL
        # Por simplicidade no MVP, vamos buscar tudo e ordenar em memória se o campo for JSON profundo
        # Ou ordenar por Timestamp no banco e o resto em memória
        
        # Idealmente: cast(Lead.visual_analysis['wealth_score'], Integer)
        # Mas SQLite vs Postgres tem sintaxes diferentes para JSON.
        
        stmt = stmt.order_by(desc(Lead.timestamp))
        
        # Para evitar problemas com dialetos JSON agora, buscamos os top 100 mais recentes
        # e ordenamos em memória se for wealth_score.
        # Se a base crescer, implementamos ordenação nativa SQL.
        
        result = await self.db.execute(stmt.limit(200)) # Fetch more allowing sort
        leads_orm = result.scalars().all()
        
        leads_pydantic = [LeadClassification.model_validate(l) for l in leads_orm]
        
        if sort_by == "wealth_score":
            leads_pydantic.sort(key=lambda x: x.visual_analysis.wealth_score if x.visual_analysis else 0, reverse=True)
        elif sort_by == "visual_fit_score":
            leads_pydantic.sort(key=lambda x: x.visual_analysis.visual_fit_score if x.visual_analysis else 0, reverse=True)
        elif sort_by == "lead_score":
            leads_pydantic.sort(key=lambda x: x.scores.lead_score, reverse=True)
            
        return leads_pydantic[offset : offset + limit]

    async def save_draft(self, draft_data: OutreachDraft) -> None:
        new_draft = Draft(
            lead_id=draft_data.lead_id,
            approach_style=draft_data.approach_style,
            approach_cta=draft_data.approach_cta,
            content=draft_data.content,
            triage_questions=draft_data.triage_questions,
            version=draft_data.version
        )
        self.db.add(new_draft)
        await self.db.commit()

    async def get_draft(self, lead_id: str) -> Optional[OutreachDraft]:
        # Pega o último draft
        stmt = select(Draft).where(Draft.lead_id == lead_id).order_by(desc(Draft.created_at))
        result = await self.db.execute(stmt)
        draft = result.scalars().first()
        
        if not draft:
            return None
            
        return OutreachDraft(
            lead_id=draft.lead_id,
            approach_style=draft.approach_style,
            approach_cta=draft.approach_cta,
            content=draft.content,
            triage_questions=draft.triage_questions,
            version=draft.version
        )
