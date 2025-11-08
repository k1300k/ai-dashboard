"""Board schemas"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from .node import NodeResponse


class BoardBase(BaseModel):
    """Base board schema"""
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    is_public: bool = False


class BoardCreate(BoardBase):
    """Schema for creating a board"""
    pass


class BoardUpdate(BaseModel):
    """Schema for updating a board"""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    is_public: Optional[bool] = None


class BoardResponse(BoardBase):
    """Schema for board response"""
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class BoardWithNodes(BoardResponse):
    """Schema for board with nodes"""
    nodes: List[NodeResponse] = []
