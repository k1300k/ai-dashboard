/* Board API service */
import apiClient from './api'
import type { Board } from '@/types'

export interface CreateBoardData {
  title: string
  description?: string
  is_public?: boolean
}

export interface UpdateBoardData {
  title?: string
  description?: string
  is_public?: boolean
}

export const boardService = {
  async getBoards(): Promise<Board[]> {
    const response = await apiClient.get('/api/boards/')
    return response.data
  },

  async getBoard(id: string): Promise<Board> {
    const response = await apiClient.get(`/api/boards/${id}`)
    return response.data
  },

  async createBoard(data: CreateBoardData): Promise<Board> {
    const response = await apiClient.post('/api/boards/', data)
    return response.data
  },

  async updateBoard(id: string, data: UpdateBoardData): Promise<Board> {
    const response = await apiClient.put(`/api/boards/${id}`, data)
    return response.data
  },

  async deleteBoard(id: string): Promise<void> {
    await apiClient.delete(`/api/boards/${id}`)
  }
}
