"""AI endpoints"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.schemas.ai import (
    AIExpansionRequest,
    AIExpansionResponse,
    AIEvaluationRequest,
    AIEvaluationResponse,
    AISummaryRequest,
    AISummaryResponse,
)
from app.models.node import Node
from app.models.board import Board
from app.ai.idea_expansion import idea_expansion_service

router = APIRouter()


@router.post("/expand", response_model=AIExpansionResponse)
async def expand_idea(
    request: AIExpansionRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Expand an idea using AI
    
    Takes a node's content and generates related sub-ideas
    """
    # Verify node exists
    result = await db.execute(select(Node).where(Node.id == request.node_id))
    node = result.scalar_one_or_none()
    
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    
    # Build context
    context = request.context or {}
    
    # Get board context
    board_result = await db.execute(select(Board).where(Board.id == node.board_id))
    board = board_result.scalar_one_or_none()
    if board:
        context["board_title"] = board.title
    
    # Get related nodes
    related_result = await db.execute(
        select(Node).where(Node.board_id == node.board_id).limit(10)
    )
    related_nodes = related_result.scalars().all()
    if related_nodes:
        context["related_nodes"] = [n.title for n in related_nodes if n.id != node.id]
    
    # Call AI service
    expansion_result = await idea_expansion_service.expand_idea(
        node_content=request.node_content,
        context=context,
        num_ideas=request.num_ideas
    )
    
    return expansion_result


@router.post("/evaluate", response_model=AIEvaluationResponse)
async def evaluate_idea(
    request: AIEvaluationRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Evaluate an idea's impact and feasibility using AI
    """
    # Verify node exists
    result = await db.execute(select(Node).where(Node.id == request.node_id))
    node = result.scalar_one_or_none()
    
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    
    # Call AI service
    evaluation_result = await idea_expansion_service.evaluate_idea(
        idea=request.idea,
        context=request.context
    )
    
    # Update node with scores
    node.impact_score = evaluation_result.get("impact_score")
    node.feasibility_score = evaluation_result.get("feasibility_score")
    node.priority_score = evaluation_result.get("priority_score")
    
    await db.commit()
    
    return evaluation_result


@router.post("/summarize", response_model=AISummaryResponse)
async def summarize_mindmap(
    request: AISummaryRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Generate AI summary of a mindmap
    """
    # Get board
    board_result = await db.execute(select(Board).where(Board.id == request.board_id))
    board = board_result.scalar_one_or_none()
    
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    
    # Get all nodes
    nodes_result = await db.execute(
        select(Node).where(Node.board_id == request.board_id)
    )
    nodes = nodes_result.scalars().all()
    
    # Convert to dict for AI service
    nodes_data = [
        {
            "title": node.title,
            "content": node.content,
            "impact_score": node.impact_score,
            "feasibility_score": node.feasibility_score,
        }
        for node in nodes
    ]
    
    # Call AI service
    summary = await idea_expansion_service.summarize_mindmap(
        nodes=nodes_data,
        board_title=board.title
    )
    
    return {"summary": summary}
