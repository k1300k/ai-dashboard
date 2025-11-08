"""Board endpoints"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from uuid import UUID
from app.core.database import get_db
from app.schemas.board import BoardCreate, BoardUpdate, BoardResponse, BoardWithNodes
from app.models.board import Board
from app.models.node import Node

router = APIRouter()


@router.post("/", response_model=BoardResponse, status_code=201)
async def create_board(
    board: BoardCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new board"""
    # TODO: Get user_id from authentication
    # For now, using a dummy UUID
    from uuid import uuid4
    user_id = uuid4()
    
    db_board = Board(
        **board.dict(),
        user_id=user_id
    )
    db.add(db_board)
    await db.commit()
    await db.refresh(db_board)
    
    return db_board


@router.get("/", response_model=List[BoardResponse])
async def list_boards(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """List all boards"""
    # TODO: Filter by authenticated user
    result = await db.execute(
        select(Board).offset(skip).limit(limit)
    )
    boards = result.scalars().all()
    return boards


@router.get("/{board_id}", response_model=BoardWithNodes)
async def get_board(
    board_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific board with its nodes"""
    result = await db.execute(
        select(Board).where(Board.id == board_id)
    )
    board = result.scalar_one_or_none()
    
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    
    # Get nodes
    nodes_result = await db.execute(
        select(Node).where(Node.board_id == board_id)
    )
    nodes = nodes_result.scalars().all()
    
    # Create response
    board_dict = {
        "id": board.id,
        "title": board.title,
        "description": board.description,
        "is_public": board.is_public,
        "user_id": board.user_id,
        "created_at": board.created_at,
        "updated_at": board.updated_at,
        "nodes": nodes
    }
    
    return board_dict


@router.put("/{board_id}", response_model=BoardResponse)
async def update_board(
    board_id: UUID,
    board_update: BoardUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update a board"""
    result = await db.execute(
        select(Board).where(Board.id == board_id)
    )
    board = result.scalar_one_or_none()
    
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    
    # Update fields
    update_data = board_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(board, field, value)
    
    await db.commit()
    await db.refresh(board)
    
    return board


@router.delete("/{board_id}", status_code=204)
async def delete_board(
    board_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Delete a board"""
    result = await db.execute(
        select(Board).where(Board.id == board_id)
    )
    board = result.scalar_one_or_none()
    
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    
    await db.delete(board)
    await db.commit()
    
    return None
