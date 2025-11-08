# ThinkGraph - AI 기반 아이디어 확장 플랫폼

## 프로덕트 개요

**비전:** AI의 창의적 사고 지원을 통해 사용자의 아이디어를 체계적으로 확장하고 실현 가능한 프로젝트로 발전시키는 지능형 마인드맵 플랫폼

**핵심 가치 제안:** 단순한 시각화를 넘어 AI가 아이디어 확장, 분석, 우선순위 제안까지 지원하는 차세대 사고 도구

## 주요 기능

### AI 핵심 기능
- ✨ **AI 아이디어 확장**: 선택한 노드 기반으로 관련 아이디어 3-5개 자동 생성
- 📊 **AI 분석 및 평가**: 아이디어별 실현가능성, 임팩트 점수 산출
- 🎯 **AI 클러스터링**: 유사한 아이디어들을 자동으로 그룹화 및 분류
- 🔍 **AI 검색 연동**: 관련 자료, 논문, 코드 저장소 자동 검색 및 링크 제안
- 📝 **AI 요약**: 전체 마인드맵 또는 특정 브랜치의 핵심 내용 요약

### 마인드맵 기능
- 🗺️ 무한 확장 가능한 계층 구조
- 🔗 노드 간 다양한 관계 타입 (연관, 의존, 대립 등)
- 👥 실시간 협업 편집 (WebSocket)
- 📚 버전 관리 및 변경 이력 추적
- ⚡ 고성능 렌더링 (1000+ 노드 지원)

## 기술 스택

### Backend
- **Framework**: FastAPI + Python 3.11+
- **AI Engine**: OpenAI GPT-4
- **Database**: PostgreSQL 15+
- **Cache**: Redis
- **Real-time**: Socket.IO

### Frontend
- **Framework**: Vue.js 3 + TypeScript
- **State Management**: Pinia
- **UI Components**: Element Plus
- **Canvas**: Vue Flow / D3.js
- **Build Tool**: Vite

### DevOps
- **Containerization**: Docker + Docker Compose
- **Deployment**: Kubernetes
- **CI/CD**: GitHub Actions

## 프로젝트 구조

```
thinkgraph/
├── backend/                 # FastAPI 백엔드
│   ├── app/
│   │   ├── api/            # API 엔드포인트
│   │   ├── models/         # 데이터베이스 모델
│   │   ├── services/       # 비즈니스 로직
│   │   ├── ai/             # AI 서비스
│   │   └── core/           # 설정 및 유틸리티
│   ├── tests/              # 테스트 코드
│   ├── requirements.txt    # Python 의존성
│   └── Dockerfile
├── frontend/               # Vue.js 프론트엔드
│   ├── src/
│   │   ├── components/     # Vue 컴포넌트
│   │   ├── views/          # 페이지 뷰
│   │   ├── stores/         # Pinia 스토어
│   │   ├── services/       # API 클라이언트
│   │   └── composables/    # Vue Composables
│   ├── public/             # 정적 파일
│   ├── package.json
│   └── Dockerfile
├── docs/                   # 문서
├── docker-compose.yml      # Docker Compose 설정
└── README.md
```

## 빠른 시작

### 사전 요구사항
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+
- Docker & Docker Compose (선택사항)

### 로컬 개발 환경 설정

#### 1. 백엔드 설정
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 환경 변수 설정
cp .env.example .env
# .env 파일을 편집하여 필요한 값 설정

# 데이터베이스 마이그레이션
alembic upgrade head

# 서버 실행
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 2. 프론트엔드 설정
```bash
cd frontend
npm install

# 환경 변수 설정
cp .env.example .env
# .env 파일을 편집하여 필요한 값 설정

# 개발 서버 실행
npm run dev
```

#### 3. Docker Compose로 실행
```bash
docker-compose up -d
```

### 환경 변수

#### Backend (.env)
```env
DATABASE_URL=postgresql://user:password@localhost:5432/thinkgraph
REDIS_URL=redis://localhost:6379
OPENAI_API_KEY=your_openai_api_key
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

#### Frontend (.env)
```env
VITE_API_BASE_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000/ws
```

## API 문서

백엔드 서버 실행 후 다음 주소에서 API 문서를 확인할 수 있습니다:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 개발 로드맵

### Phase 1: MVP (4-6주) ✅ 진행 중
- [x] 프로젝트 구조 설정
- [ ] 기본 마인드맵 인터페이스
- [ ] AI 확장 기능 (GPT-4 통합)
- [ ] 기본 평가 시스템
- [ ] 사용자 인증 및 데이터 저장

### Phase 2: 고도화 (6-8주)
- [ ] 실시간 협업 기능
- [ ] 버전 관리 시스템
- [ ] 고급 AI 분석
- [ ] 검색 연동 (논문, GitHub)
- [ ] 성능 최적화

### Phase 3: 확장 (8-12주)
- [ ] 모바일 앱
- [ ] 플러그인 시스템
- [ ] 팀 관리 기능
- [ ] 분석 대시보드

## 기여 방법

1. 이 저장소를 Fork 합니다
2. Feature 브랜치를 생성합니다 (`git checkout -b feature/AmazingFeature`)
3. 변경사항을 커밋합니다 (`git commit -m 'Add some AmazingFeature'`)
4. 브랜치에 Push 합니다 (`git push origin feature/AmazingFeature`)
5. Pull Request를 생성합니다

## 라이선스

MIT License - 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 연락처

프로젝트 관리자: ThinkGraph Team
- 이메일: contact@thinkgraph.ai
- 웹사이트: https://thinkgraph.ai

## 감사의 말

- OpenAI GPT-4 for AI capabilities
- Vue.js Team for the amazing framework
- FastAPI Team for the high-performance backend framework
