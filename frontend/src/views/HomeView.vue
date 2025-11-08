<template>
  <div class="home-view">
    <div class="hero-section">
      <h1 class="title">
        <span class="gradient-text">ThinkGraph</span>
      </h1>
      <p class="subtitle">
        AI-Powered Idea Expansion Platform
      </p>
      <p class="description">
        단순한 시각화를 넘어 AI가 아이디어 확장, 분석, 우선순위 제안까지 지원하는 차세대 사고 도구
      </p>
      
      <div class="cta-buttons">
        <el-button type="primary" size="large" @click="goToBoards">
          시작하기
        </el-button>
        <el-button size="large" @click="showDemo">
          데모 보기
        </el-button>
      </div>
    </div>

    <div class="features-section">
      <h2>주요 기능</h2>
      <div class="features-grid">
        <div class="feature-card">
          <div class="feature-icon">✨</div>
          <h3>AI 아이디어 확장</h3>
          <p>선택한 노드 기반으로 관련 아이디어 3-5개 자동 생성</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">📊</div>
          <h3>AI 분석 및 평가</h3>
          <p>아이디어별 실현가능성, 임팩트 점수 산출</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">🎯</div>
          <h3>AI 클러스터링</h3>
          <p>유사한 아이디어들을 자동으로 그룹화 및 분류</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">🔍</div>
          <h3>AI 검색 연동</h3>
          <p>관련 자료, 논문, 코드 저장소 자동 검색</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const goToBoards = () => {
  router.push('/boards')
}

const showDemo = () => {
  // TODO: Implement demo
  console.log('Show demo')
}
</script>

<style scoped>
.home-view {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem;
}

.hero-section {
  max-width: 800px;
  margin: 0 auto;
  text-align: center;
  padding: 4rem 0;
}

.title {
  font-size: 4rem;
  font-weight: 800;
  margin: 0;
  margin-bottom: 1rem;
}

.gradient-text {
  background: linear-gradient(135deg, #ffffff 0%, #e0e7ff 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.subtitle {
  font-size: 1.5rem;
  margin: 0;
  margin-bottom: 1rem;
  opacity: 0.9;
}

.description {
  font-size: 1.1rem;
  line-height: 1.6;
  margin-bottom: 2rem;
  opacity: 0.8;
}

.cta-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.features-section {
  max-width: 1200px;
  margin: 4rem auto;
  padding: 3rem;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  backdrop-filter: blur(10px);
}

.features-section h2 {
  text-align: center;
  font-size: 2.5rem;
  margin-bottom: 3rem;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}

.feature-card {
  background: rgba(255, 255, 255, 0.1);
  padding: 2rem;
  border-radius: 15px;
  text-align: center;
  transition: transform 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
  background: rgba(255, 255, 255, 0.15);
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.feature-card h3 {
  font-size: 1.3rem;
  margin-bottom: 0.5rem;
}

.feature-card p {
  opacity: 0.8;
  line-height: 1.5;
}
</style>
