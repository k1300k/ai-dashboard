"""Node model"""
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Float, Integer, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.core.database import Base


class Node(Base):
    """Node (Idea) model"""
    __tablename__ = "nodes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    board_id = Column(UUID(as_uuid=True), ForeignKey("boards.id"), nullable=False)
    title = Column(String(500), nullable=False)
    content = Column(Text)
    url = Column(String(2048))
    
    # Position and style
    position_x = Column(Float, nullable=False, default=0.0)
    position_y = Column(Float, nullable=False, default=0.0)
    width = Column(Integer, default=200)
    height = Column(Integer, default=100)
    color = Column(String(20), default="#3B82F6")
    
    # AI-generated scores
    impact_score = Column(Float)  # 1-10
    feasibility_score = Column(Float)  # 1-10
    priority_score = Column(Float)  # Calculated from impact and feasibility
    
    # Metadata
    metadata = Column(JSON)  # Additional flexible data
    ai_generated = Column(String, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    board = relationship("Board", back_populates="nodes")
