"""Node schemas"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID


class NodeBase(BaseModel):
    """Base node schema"""
    title: str = Field(..., min_length=1, max_length=500)
    content: Optional[str] = None
    url: Optional[str] = None
    position_x: float = 0.0
    position_y: float = 0.0
    width: int = 200
    height: int = 100
    color: str = "#3B82F6"
    metadata: Optional[Dict[str, Any]] = None


class NodeCreate(NodeBase):
    """Schema for creating a node"""
    board_id: UUID


class NodeUpdate(BaseModel):
    """Schema for updating a node"""
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    content: Optional[str] = None
    url: Optional[str] = None
    position_x: Optional[float] = None
    position_y: Optional[float] = None
    width: Optional[int] = None
    height: Optional[int] = None
    color: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class NodeResponse(NodeBase):
    """Schema for node response"""
    id: UUID
    board_id: UUID
    impact_score: Optional[float] = None
    feasibility_score: Optional[float] = None
    priority_score: Optional[float] = None
    ai_generated: bool = False
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
