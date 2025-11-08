/* Board store */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Board, Node } from '@/types'
import { boardService } from '@/services/boardService'
import { nodeService } from '@/services/nodeService'

export const useBoardStore = defineStore('board', () => {
  // State
  const boards = ref<Board[]>([])
  const currentBoard = ref<Board | null>(null)
  const currentNodes = ref<Node[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Getters
  const getBoardById = computed(() => {
    return (id: string) => boards.value.find((b) => b.id === id)
  })

  // Actions
  async function fetchBoards() {
    loading.value = true
    error.value = null
    try {
      boards.value = await boardService.getBoards()
    } catch (e: any) {
      error.value = e.message || 'Failed to fetch boards'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function fetchBoard(id: string) {
    loading.value = true
    error.value = null
    try {
      const board = await boardService.getBoard(id)
      currentBoard.value = board
      currentNodes.value = board.nodes || []
      return board
    } catch (e: any) {
      error.value = e.message || 'Failed to fetch board'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function createBoard(data: { title: string; description?: string; is_public?: boolean }) {
    loading.value = true
    error.value = null
    try {
      const board = await boardService.createBoard(data)
      boards.value.push(board)
      return board
    } catch (e: any) {
      error.value = e.message || 'Failed to create board'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function updateBoard(id: string, data: Partial<Board>) {
    loading.value = true
    error.value = null
    try {
      const board = await boardService.updateBoard(id, data)
      const index = boards.value.findIndex((b) => b.id === id)
      if (index !== -1) {
        boards.value[index] = board
      }
      if (currentBoard.value?.id === id) {
        currentBoard.value = board
      }
      return board
    } catch (e: any) {
      error.value = e.message || 'Failed to update board'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function deleteBoard(id: string) {
    loading.value = true
    error.value = null
    try {
      await boardService.deleteBoard(id)
      boards.value = boards.value.filter((b) => b.id !== id)
      if (currentBoard.value?.id === id) {
        currentBoard.value = null
        currentNodes.value = []
      }
    } catch (e: any) {
      error.value = e.message || 'Failed to delete board'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function addNode(node: Node) {
    currentNodes.value.push(node)
  }

  async function updateNode(nodeId: string, data: Partial<Node>) {
    const index = currentNodes.value.findIndex((n) => n.id === nodeId)
    if (index !== -1) {
      const updated = await nodeService.updateNode(nodeId, data)
      currentNodes.value[index] = updated
    }
  }

  async function removeNode(nodeId: string) {
    await nodeService.deleteNode(nodeId)
    currentNodes.value = currentNodes.value.filter((n) => n.id !== nodeId)
  }

  return {
    // State
    boards,
    currentBoard,
    currentNodes,
    loading,
    error,
    // Getters
    getBoardById,
    // Actions
    fetchBoards,
    fetchBoard,
    createBoard,
    updateBoard,
    deleteBoard,
    addNode,
    updateNode,
    removeNode
  }
})
