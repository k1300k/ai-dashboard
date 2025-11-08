"""AI service schemas"""
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from uuid import UUID


class AIExpansionRequest(BaseModel):
    """Request schema for AI idea expansion"""
    node_id: UUID
    node_content: str = Field(..., min_length=1)
    num_ideas: int = Field(default=5, ge=1, le=10)
    context: Optional[Dict[str, Any]] = None


class AIIdeaResponse(BaseModel):
    """Single expanded idea response"""
    title: str
    description: str
    relation_type: str  # extends, alternative, prerequisite, application


class AIExpansionResponse(BaseModel):
    """Response schema for AI idea expansion"""
    ideas: List[AIIdeaResponse]
    metadata: Dict[str, Any]
    error: Optional[str] = None


class AIEvaluationRequest(BaseModel):
    """Request schema for AI idea evaluation"""
    node_id: UUID
    idea: str = Field(..., min_length=1)
    context: Optional[Dict[str, Any]] = None


class AIEvaluationResponse(BaseModel):
    """Response schema for AI idea evaluation"""
    impact_score: float = Field(..., ge=1, le=10)
    feasibility_score: float = Field(..., ge=1, le=10)
    priority_score: float = Field(..., ge=1, le=10)
    impact_reasoning: str
    feasibility_reasoning: str
    recommendations: List[str]
    error: Optional[str] = None


class AISummaryRequest(BaseModel):
    """Request schema for AI mindmap summary"""
    board_id: UUID


class AISummaryResponse(BaseModel):
    """Response schema for AI mindmap summary"""
    summary: str
    error: Optional[str] = None
