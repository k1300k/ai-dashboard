/* TypeScript type definitions */

export interface Node {
  id: string
  board_id: string
  title: string
  content?: string
  url?: string
  position_x: number
  position_y: number
  width: number
  height: number
  color: string
  impact_score?: number
  feasibility_score?: number
  priority_score?: number
  ai_generated: boolean
  metadata?: Record<string, any>
  created_at: string
  updated_at: string
}

export interface Board {
  id: string
  title: string
  description?: string
  is_public: boolean
  user_id: string
  created_at: string
  updated_at: string
  nodes?: Node[]
}

export interface Edge {
  id: string
  board_id: string
  source_id: string
  target_id: string
  edge_type: string
  label?: string
  color: string
  style: string
  metadata?: Record<string, any>
  created_at: string
  updated_at: string
}

export interface AIIdea {
  title: string
  description: string
  relation_type: 'extends' | 'alternative' | 'prerequisite' | 'application'
}

export interface AIExpansionRequest {
  node_id: string
  node_content: string
  num_ideas: number
  context?: Record<string, any>
}

export interface AIExpansionResponse {
  ideas: AIIdea[]
  metadata: Record<string, any>
  error?: string
}

export interface AIEvaluationRequest {
  node_id: string
  idea: string
  context?: Record<string, any>
}

export interface AIEvaluationResponse {
  impact_score: number
  feasibility_score: number
  priority_score: number
  impact_reasoning: string
  feasibility_reasoning: string
  recommendations: string[]
  error?: string
}

export interface AISummaryRequest {
  board_id: string
}

export interface AISummaryResponse {
  summary: string
  error?: string
}

// VueFlow types
export interface VueFlowNode {
  id: string
  type?: string
  position: { x: number; y: number }
  data: {
    label: string
    node: Node
  }
  style?: Record<string, any>
}

export interface VueFlowEdge {
  id: string
  source: string
  target: string
  type?: string
  label?: string
  style?: Record<string, any>
}
