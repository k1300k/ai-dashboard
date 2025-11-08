/* Node API service */
import apiClient from './api'
import type { Node } from '@/types'

export interface CreateNodeData {
  board_id: string
  title: string
  content?: string
  url?: string
  position_x: number
  position_y: number
  width?: number
  height?: number
  color?: string
  metadata?: Record<string, any>
}

export interface UpdateNodeData {
  title?: string
  content?: string
  url?: string
  position_x?: number
  position_y?: number
  width?: number
  height?: number
  color?: string
  metadata?: Record<string, any>
}

export const nodeService = {
  async getNodesByBoard(boardId: string): Promise<Node[]> {
    const response = await apiClient.get(`/api/nodes/board/${boardId}`)
    return response.data
  },

  async getNode(id: string): Promise<Node> {
    const response = await apiClient.get(`/api/nodes/${id}`)
    return response.data
  },

  async createNode(data: CreateNodeData): Promise<Node> {
    const response = await apiClient.post('/api/nodes/', data)
    return response.data
  },

  async createNodesBatch(nodes: CreateNodeData[]): Promise<Node[]> {
    const response = await apiClient.post('/api/nodes/batch', nodes)
    return response.data
  },

  async updateNode(id: string, data: UpdateNodeData): Promise<Node> {
    const response = await apiClient.put(`/api/nodes/${id}`, data)
    return response.data
  },

  async deleteNode(id: string): Promise<void> {
    await apiClient.delete(`/api/nodes/${id}`)
  }
}
