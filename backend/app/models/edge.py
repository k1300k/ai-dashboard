"""Edge model"""
from sqlalchemy import Column, String, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.core.database import Base


class Edge(Base):
    """Edge (Connection) model"""
    __tablename__ = "edges"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    board_id = Column(UUID(as_uuid=True), ForeignKey("boards.id"), nullable=False)
    source_id = Column(UUID(as_uuid=True), ForeignKey("nodes.id"), nullable=False)
    target_id = Column(UUID(as_uuid=True), ForeignKey("nodes.id"), nullable=False)
    
    # Edge type: 'related', 'depends', 'conflicts', etc.
    edge_type = Column(String(50), default="related")
    label = Column(String(255))
    
    # Style
    color = Column(String(20), default="#9CA3AF")
    style = Column(String(50), default="solid")  # solid, dashed, dotted
    
    # Metadata
    metadata = Column(JSON)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    board = relationship("Board", back_populates="edges")
