<template>
  <div class="custom-node" :style="nodeStyle">
    <div class="node-header">
      <h4>{{ data.label }}</h4>
      <div class="node-actions">
        <el-button
          size="small"
          circle
          @click.stop="$emit('expand', data.node)"
          title="AI 확장"
        >
          ✨
        </el-button>
        <el-button
          size="small"
          circle
          @click.stop="$emit('evaluate', data.node)"
          title="AI 평가"
        >
          📊
        </el-button>
      </div>
    </div>
    
    <div v-if="data.node.content" class="node-content">
      {{ truncateText(data.node.content, 100) }}
    </div>
    
    <div v-if="data.node.priority_score" class="node-score">
      <el-tag :type="getScoreType(data.node.priority_score)" size="small">
        우선순위: {{ data.node.priority_score.toFixed(1) }}
      </el-tag>
    </div>
    
    <div v-if="data.node.ai_generated" class="ai-badge">
      AI
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Node } from '@/types'

interface Props {
  data: {
    label: string
    node: Node
  }
}

const props = defineProps<Props>()

defineEmits<{
  expand: [node: Node]
  evaluate: [node: Node]
}>()

const nodeStyle = computed(() => ({
  backgroundColor: props.data.node.color,
  width: `${props.data.node.width}px`,
  minHeight: `${props.data.node.height}px`
}))

const truncateText = (text: string, length: number) => {
  if (text.length <= length) return text
  return text.substring(0, length) + '...'
}

const getScoreType = (score: number) => {
  if (score >= 7) return 'success'
  if (score >= 4) return 'warning'
  return 'danger'
}
</script>

<style scoped>
.custom-node {
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  background: white;
  cursor: move;
  position: relative;
  transition: all 0.3s ease;
}

.custom-node:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

.node-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 0.5rem;
}

.node-header h4 {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-primary);
  flex: 1;
}

.node-actions {
  display: flex;
  gap: 0.25rem;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.custom-node:hover .node-actions {
  opacity: 1;
}

.node-content {
  font-size: 0.875rem;
  color: var(--text-secondary);
  line-height: 1.4;
  margin-bottom: 0.5rem;
}

.node-score {
  margin-top: 0.5rem;
}

.ai-badge {
  position: absolute;
  top: -8px;
  right: -8px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 0.2rem 0.5rem;
  border-radius: 12px;
  font-size: 0.7rem;
  font-weight: 600;
}
</style>
