"""Node endpoints"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from uuid import UUID
from app.core.database import get_db
from app.schemas.node import NodeCreate, NodeUpdate, NodeResponse
from app.models.node import Node
from app.models.board import Board

router = APIRouter()


@router.post("/", response_model=NodeResponse, status_code=201)
async def create_node(
    node: NodeCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new node"""
    # Verify board exists
    board_result = await db.execute(
        select(Board).where(Board.id == node.board_id)
    )
    board = board_result.scalar_one_or_none()
    
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    
    db_node = Node(**node.dict())
    db.add(db_node)
    await db.commit()
    await db.refresh(db_node)
    
    return db_node


@router.get("/board/{board_id}", response_model=List[NodeResponse])
async def list_nodes_by_board(
    board_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """List all nodes for a specific board"""
    result = await db.execute(
        select(Node).where(Node.board_id == board_id)
    )
    nodes = result.scalars().all()
    return nodes


@router.get("/{node_id}", response_model=NodeResponse)
async def get_node(
    node_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific node"""
    result = await db.execute(
        select(Node).where(Node.id == node_id)
    )
    node = result.scalar_one_or_none()
    
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    
    return node


@router.put("/{node_id}", response_model=NodeResponse)
async def update_node(
    node_id: UUID,
    node_update: NodeUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update a node"""
    result = await db.execute(
        select(Node).where(Node.id == node_id)
    )
    node = result.scalar_one_or_none()
    
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    
    # Update fields
    update_data = node_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(node, field, value)
    
    await db.commit()
    await db.refresh(node)
    
    return node


@router.delete("/{node_id}", status_code=204)
async def delete_node(
    node_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Delete a node"""
    result = await db.execute(
        select(Node).where(Node.id == node_id)
    )
    node = result.scalar_one_or_none()
    
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    
    await db.delete(node)
    await db.commit()
    
    return None


@router.post("/batch", response_model=List[NodeResponse], status_code=201)
async def create_nodes_batch(
    nodes: List[NodeCreate],
    db: AsyncSession = Depends(get_db)
):
    """Create multiple nodes at once (for AI-generated ideas)"""
    db_nodes = [Node(**node.dict()) for node in nodes]
    
    db.add_all(db_nodes)
    await db.commit()
    
    for node in db_nodes:
        await db.refresh(node)
    
    return db_nodes
