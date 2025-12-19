from sqlalchemy import Column, String, Integer, DateTime, JSON, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .core.database import Base

class Lead(Base):
    __tablename__ = "leads"

    lead_id = Column(String, primary_key=True, index=True)
    source = Column(String, index=True)
    source_url = Column(String)
    author_handle = Column(String, index=True)
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    text_excerpt = Column(String)
    
    # JSON Fields for complex structures
    pain_point = Column(JSON)
    intent_stage = Column(JSON)
    maturity = Column(JSON)
    scores = Column(JSON)
    visual_analysis = Column(JSON, nullable=True) # VisionEngine Storage
    evidence = Column(JSON)
    risk_flags = Column(JSON)
    profile_image_url = Column(String, nullable=True)
    
    # Metadata
    version = Column(String)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relations
    drafts = relationship("Draft", back_populates="lead")
    feedback = relationship("Feedback", back_populates="lead")

class Draft(Base):
    __tablename__ = "drafts"

    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(String, ForeignKey("leads.lead_id"))
    approach_style = Column(String)
    approach_cta = Column(String)
    content = Column(JSON) # List of messages
    triage_questions = Column(JSON)
    version = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    lead = relationship("Lead", back_populates="drafts")

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(String, ForeignKey("leads.lead_id"))
    event_type = Column(String)
    value = Column(JSON, nullable=True)
    notes = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    lead = relationship("Lead", back_populates="feedback")
