<template>
  <div class="boards-view">
    <div class="header">
      <h1>내 보드</h1>
      <el-button type="primary" @click="showCreateDialog = true">
        새 보드 만들기
      </el-button>
    </div>

    <div v-if="boardStore.loading" class="loading">
      <el-icon class="is-loading">
        <Loading />
      </el-icon>
      <p>로딩 중...</p>
    </div>

    <div v-else-if="boardStore.error" class="error">
      <p>{{ boardStore.error }}</p>
    </div>

    <div v-else class="boards-grid">
      <div
        v-for="board in boardStore.boards"
        :key="board.id"
        class="board-card"
        @click="openBoard(board.id)"
      >
        <h3>{{ board.title }}</h3>
        <p v-if="board.description" class="description">{{ board.description }}</p>
        <div class="board-meta">
          <span class="date">{{ formatDate(board.created_at) }}</span>
          <span v-if="board.is_public" class="public-badge">공개</span>
        </div>
      </div>

      <div class="board-card create-card" @click="showCreateDialog = true">
        <div class="create-icon">+</div>
        <p>새 보드 만들기</p>
      </div>
    </div>

    <!-- Create Board Dialog -->
    <el-dialog v-model="showCreateDialog" title="새 보드 만들기" width="500px">
      <el-form :model="newBoard" label-width="100px">
        <el-form-item label="제목" required>
          <el-input v-model="newBoard.title" placeholder="보드 제목을 입력하세요" />
        </el-form-item>
        <el-form-item label="설명">
          <el-input
            v-model="newBoard.description"
            type="textarea"
            :rows="3"
            placeholder="보드 설명 (선택사항)"
          />
        </el-form-item>
        <el-form-item label="공개 설정">
          <el-switch v-model="newBoard.is_public" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showCreateDialog = false">취소</el-button>
        <el-button type="primary" @click="createBoard" :loading="creating">
          만들기
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useBoardStore } from '@/stores/boardStore'
import { ElMessage } from 'element-plus'
import { Loading } from '@element-plus/icons-vue'

const router = useRouter()
const boardStore = useBoardStore()

const showCreateDialog = ref(false)
const creating = ref(false)
const newBoard = ref({
  title: '',
  description: '',
  is_public: false
})

onMounted(async () => {
  await boardStore.fetchBoards()
})

const openBoard = (id: string) => {
  router.push(`/board/${id}`)
}

const createBoard = async () => {
  if (!newBoard.value.title.trim()) {
    ElMessage.warning('제목을 입력해주세요')
    return
  }

  creating.value = true
  try {
    const board = await boardStore.createBoard(newBoard.value)
    ElMessage.success('보드가 생성되었습니다')
    showCreateDialog.value = false
    newBoard.value = { title: '', description: '', is_public: false }
    router.push(`/board/${board.id}`)
  } catch (e: any) {
    ElMessage.error(e.message || '보드 생성에 실패했습니다')
  } finally {
    creating.value = false
  }
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('ko-KR')
}
</script>

<style scoped>
.boards-view {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.header h1 {
  margin: 0;
  color: var(--text-primary);
}

.loading,
.error {
  text-align: center;
  padding: 4rem 0;
  color: var(--text-secondary);
}

.loading .el-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.boards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.board-card {
  background: white;
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 1.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.board-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.board-card h3 {
  margin: 0 0 0.5rem 0;
  color: var(--text-primary);
}

.board-card .description {
  color: var(--text-secondary);
  font-size: 0.9rem;
  margin: 0 0 1rem 0;
  line-height: 1.4;
}

.board-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.85rem;
  color: var(--text-secondary);
}

.public-badge {
  background: var(--success-color);
  color: white;
  padding: 0.2rem 0.6rem;
  border-radius: 12px;
  font-size: 0.75rem;
}

.create-card {
  border: 2px dashed var(--border-color);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: var(--bg-color);
}

.create-card:hover {
  border-color: var(--primary-color);
  background: rgba(59, 130, 246, 0.05);
}

.create-icon {
  font-size: 3rem;
  color: var(--primary-color);
  margin-bottom: 0.5rem;
}

.create-card p {
  margin: 0;
  color: var(--text-secondary);
}
</style>
