/* AI API service */
import apiClient from './api'
import type {
  AIExpansionRequest,
  AIExpansionResponse,
  AIEvaluationRequest,
  AIEvaluationResponse,
  AISummaryRequest,
  AISummaryResponse
} from '@/types'

export const aiService = {
  async expandIdea(request: AIExpansionRequest): Promise<AIExpansionResponse> {
    const response = await apiClient.post('/api/ai/expand', request)
    return response.data
  },

  async evaluateIdea(request: AIEvaluationRequest): Promise<AIEvaluationResponse> {
    const response = await apiClient.post('/api/ai/evaluate', request)
    return response.data
  },

  async summarizeMindmap(request: AISummaryRequest): Promise<AISummaryResponse> {
    const response = await apiClient.post('/api/ai/summarize', request)
    return response.data
  }
}
