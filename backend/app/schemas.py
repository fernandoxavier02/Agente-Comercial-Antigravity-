from pydantic import BaseModel, Field, AnyUrl, ConfigDict
from typing import Literal, Any
from datetime import datetime

IntentStage = Literal["discovery", "consideration", "decision"]
MaturityLabel = Literal["beginner", "intermediate", "advanced"]
ApproachStyle = Literal["educational", "empathetic", "authority_medical", "conversational"]
ApproachCta = Literal["send_info", "invite_evaluation", "ask_question"]
RiskFlag = Literal["minor_possible", "medical_sensitive", "self_harm", "harassment", "spam_risk", "tos_risk"]

class PainPoint(BaseModel):
    label: str
    confidence: float = Field(ge=0, le=1)

class Stage(BaseModel):
    label: IntentStage
    confidence: float = Field(ge=0, le=1)

class Maturity(BaseModel):
    label: MaturityLabel
    score: int = Field(ge=0, le=100)

class Scores(BaseModel):
    fit: int = Field(ge=0, le=100)
    intent: int = Field(ge=0, le=100)
    urgency: int = Field(ge=0, le=100)
    risk: int = Field(ge=0, le=100)
    lead_score: int = Field(ge=0, le=100)
    evidence_quality: int = Field(ge=0, le=100)

class Evidence(BaseModel):
    text: str = Field(max_length=400)
    url: AnyUrl

class CategoryScore(BaseModel):
    score: int = Field(ge=0, le=100)
    justification: str

class VisualAnalysis(BaseModel):
    wealth_score: int = Field(ge=0, le=100)
    visual_fit_score: int = Field(ge=0, le=100)
    categories: dict[str, CategoryScore]
    tags: list[str]
    technical_justification: str
    red_flags: list[str] = []

class LeadClassification(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    lead_id: str
    source: str
    source_url: AnyUrl
    author_handle: str
    profile_image_url: AnyUrl | None = None
    timestamp: datetime
    text_excerpt: str = Field(max_length=1500)

    pain_point: PainPoint
    intent_stage: Stage
    maturity: Maturity
    scores: Scores
    visual_analysis: VisualAnalysis | None = None
    evidence: list[Evidence]
    risk_flags: list[RiskFlag] = []
    version: str

class Approach(BaseModel):
    style: ApproachStyle
    cta: ApproachCta
    do_not: list[str] = []

class OutreachDraft(BaseModel):
    lead_id: str
    approach: Approach
    drafts: list[str] = Field(min_length=1, max_length=5)
    triage_questions: list[str] = []
    version: str

class FeedbackEvent(BaseModel):
    lead_id: str
    event_type: Literal[
        "lead_approved", "lead_rejected", "message_used", "message_edited",
        "reply_received", "appointment_booked", "opt_out"
    ]
    value: Any = None
    timestamp: datetime
    notes: str | None = Field(default=None, max_length=1000)
