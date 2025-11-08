<template>
  <div class="board-view">
    <!-- Header -->
    <div class="board-header">
      <div class="board-title">
        <el-button icon="ArrowLeft" @click="goBack" circle />
        <h2 v-if="boardStore.currentBoard">{{ boardStore.currentBoard.title }}</h2>
        <h2 v-else>Loading...</h2>
      </div>
      <div class="board-actions">
        <el-button @click="showAISummary = true" :loading="aiLoading">
          AI 요약
        </el-button>
        <el-button type="primary" @click="addNewNode">
          노드 추가
        </el-button>
      </div>
    </div>

    <!-- MindMap Canvas -->
    <div class="mindmap-container">
      <VueFlow
        v-model:nodes="nodes"
        v-model:edges="edges"
        @node-click="onNodeClick"
        @node-drag-stop="onNodeDragStop"
        @pane-click="onPaneClick"
        :fit-view-on-init="true"
      >
        <Background />
        <Controls />
        <MiniMap />
        
        <template #node-custom="{ data }">
          <CustomNode :data="data" @expand="expandNode" @evaluate="evaluateNode" />
        </template>
      </VueFlow>
    </div>

    <!-- Node Details Drawer -->
    <el-drawer
      v-model="showNodeDetails"
      :title="selectedNode?.title || 'Node Details'"
      size="400px"
    >
      <div v-if="selectedNode" class="node-details">
        <el-form label-width="100px">
          <el-form-item label="제목">
            <el-input v-model="selectedNode.title" @blur="updateSelectedNode" />
          </el-form-item>
          <el-form-item label="내용">
            <el-input
              v-model="selectedNode.content"
              type="textarea"
              :rows="4"
              @blur="updateSelectedNode"
            />
          </el-form-item>
          <el-form-item label="URL">
            <el-input v-model="selectedNode.url" @blur="updateSelectedNode" />
          </el-form-item>
          <el-form-item label="색상">
            <el-color-picker v-model="selectedNode.color" @change="updateSelectedNode" />
          </el-form-item>
          
          <div v-if="selectedNode.impact_score" class="scores">
            <h4>AI 평가 점수</h4>
            <div class="score-item">
              <span>임팩트:</span>
              <el-progress :percentage="selectedNode.impact_score * 10" />
            </div>
            <div class="score-item">
              <span>실현가능성:</span>
              <el-progress :percentage="selectedNode.feasibility_score! * 10" />
            </div>
            <div class="score-item">
              <span>우선순위:</span>
              <el-progress
                :percentage="selectedNode.priority_score! * 10"
                :color="getPriorityColor(selectedNode.priority_score!)"
              />
            </div>
          </div>
        </el-form>
        
        <div class="node-actions">
          <el-button @click="deleteSelectedNode" type="danger">
            노드 삭제
          </el-button>
        </div>
      </div>
    </el-drawer>

    <!-- AI Summary Dialog -->
    <el-dialog v-model="showAISummary" title="AI 마인드맵 요약" width="600px">
      <div v-if="aiSummary" class="ai-summary">
        <p>{{ aiSummary }}</p>
      </div>
      <div v-else class="loading">
        <el-icon class="is-loading"><Loading /></el-icon>
        <p>AI가 마인드맵을 분석 중입니다...</p>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { VueFlow } from '@vueflow/core'
import { Background } from '@vueflow/background'
import { Controls } from '@vueflow/controls'
import { MiniMap } from '@vueflow/minimap'
import { useBoardStore } from '@/stores/boardStore'
import { nodeService } from '@/services/nodeService'
import { aiService } from '@/services/aiService'
import type { Node, VueFlowNode, VueFlowEdge } from '@/types'
import CustomNode from '@/components/CustomNode.vue'
import { ElMessage } from 'element-plus'
import { Loading } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const boardStore = useBoardStore()

const showNodeDetails = ref(false)
const selectedNode = ref<Node | null>(null)
const showAISummary = ref(false)
const aiSummary = ref('')
const aiLoading = ref(false)

// Convert nodes to VueFlow format
const nodes = computed<VueFlowNode[]>(() => {
  return boardStore.currentNodes.map((node) => ({
    id: node.id,
    type: 'custom',
    position: { x: node.position_x, y: node.position_y },
    data: {
      label: node.title,
      node: node
    },
    style: {
      background: node.color,
      width: `${node.width}px`,
      minHeight: `${node.height}px`
    }
  }))
})

const edges = ref<VueFlowEdge[]>([])

onMounted(async () => {
  const boardId = route.params.id as string
  await boardStore.fetchBoard(boardId)
})

// Watch for AI summary dialog
watch(showAISummary, async (newVal) => {
  if (newVal && !aiSummary.value) {
    try {
      const result = await aiService.summarizeMindmap({
        board_id: route.params.id as string
      })
      aiSummary.value = result.summary
    } catch (e: any) {
      ElMessage.error('AI 요약 생성에 실패했습니다')
    }
  }
})

const onNodeClick = ({ node }: { node: VueFlowNode }) => {
  const nodeData = boardStore.currentNodes.find((n) => n.id === node.id)
  if (nodeData) {
    selectedNode.value = { ...nodeData }
    showNodeDetails.value = true
  }
}

const onNodeDragStop = ({ node }: { node: VueFlowNode }) => {
  boardStore.updateNode(node.id, {
    position_x: node.position.x,
    position_y: node.position.y
  })
}

const onPaneClick = () => {
  showNodeDetails.value = false
}

const addNewNode = async () => {
  const newNode = {
    board_id: route.params.id as string,
    title: '새 아이디어',
    content: '',
    position_x: Math.random() * 500,
    position_y: Math.random() * 500,
    width: 200,
    height: 100,
    color: '#3B82F6'
  }

  try {
    const created = await nodeService.createNode(newNode)
    await boardStore.addNode(created)
    ElMessage.success('노드가 추가되었습니다')
  } catch (e: any) {
    ElMessage.error('노드 추가에 실패했습니다')
  }
}

const updateSelectedNode = async () => {
  if (!selectedNode.value) return

  try {
    await boardStore.updateNode(selectedNode.value.id, selectedNode.value)
    ElMessage.success('노드가 업데이트되었습니다')
  } catch (e: any) {
    ElMessage.error('노드 업데이트에 실패했습니다')
  }
}

const deleteSelectedNode = async () => {
  if (!selectedNode.value) return

  try {
    await boardStore.removeNode(selectedNode.value.id)
    showNodeDetails.value = false
    selectedNode.value = null
    ElMessage.success('노드가 삭제되었습니다')
  } catch (e: any) {
    ElMessage.error('노드 삭제에 실패했습니다')
  }
}

const expandNode = async (node: Node) => {
  aiLoading.value = true
  try {
    const result = await aiService.expandIdea({
      node_id: node.id,
      node_content: node.content || node.title,
      num_ideas: 5
    })

    // Create new nodes from AI suggestions
    const newNodes = result.ideas.map((idea, index) => ({
      board_id: node.board_id,
      title: idea.title,
      content: idea.description,
      position_x: node.position_x + (index - 2) * 250,
      position_y: node.position_y + 200,
      width: 200,
      height: 100,
      color: '#8B5CF6',
      metadata: { relation_type: idea.relation_type }
    }))

    const created = await nodeService.createNodesBatch(newNodes)
    created.forEach((n) => boardStore.addNode(n))

    ElMessage.success(`${result.ideas.length}개의 아이디어가 생성되었습니다`)
  } catch (e: any) {
    ElMessage.error('AI 확장에 실패했습니다')
  } finally {
    aiLoading.value = false
  }
}

const evaluateNode = async (node: Node) => {
  aiLoading.value = true
  try {
    const result = await aiService.evaluateIdea({
      node_id: node.id,
      idea: node.content || node.title
    })

    await boardStore.updateNode(node.id, {
      impact_score: result.impact_score,
      feasibility_score: result.feasibility_score,
      priority_score: result.priority_score
    })

    ElMessage.success('AI 평가가 완료되었습니다')
  } catch (e: any) {
    ElMessage.error('AI 평가에 실패했습니다')
  } finally {
    aiLoading.value = false
  }
}

const getPriorityColor = (score: number) => {
  if (score >= 7) return '#10B981'
  if (score >= 4) return '#F59E0B'
  return '#EF4444'
}

const goBack = () => {
  router.push('/boards')
}
</script>

<style scoped>
.board-view {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--bg-color);
}

.board-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  background: white;
  border-bottom: 1px solid var(--border-color);
}

.board-title {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.board-title h2 {
  margin: 0;
  color: var(--text-primary);
}

.board-actions {
  display: flex;
  gap: 0.5rem;
}

.mindmap-container {
  flex: 1;
  position: relative;
}

.node-details {
  padding: 1rem 0;
}

.scores {
  margin-top: 2rem;
}

.scores h4 {
  margin-bottom: 1rem;
}

.score-item {
  margin-bottom: 1rem;
}

.score-item span {
  display: block;
  margin-bottom: 0.5rem;
  color: var(--text-secondary);
}

.node-actions {
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid var(--border-color);
}

.ai-summary {
  line-height: 1.8;
  color: var(--text-primary);
}

.loading {
  text-align: center;
  padding: 2rem;
  color: var(--text-secondary);
}

.loading .el-icon {
  font-size: 2rem;
  margin-bottom: 1rem;
}
</style>
