# ThinkGraph 시스템 아키텍처

## 전체 아키텍처 개요

```
┌─────────────────────────────────────────────────────────────┐
│                        사용자 (User)                          │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│                    프론트엔드 (Vue.js 3)                      │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────────┐    │
│  │   Router    │  │   Pinia     │  │  Vue Components  │    │
│  │  (페이지)    │  │  (상태관리)  │  │   (UI 컴포넌트)   │    │
│  └─────────────┘  └─────────────┘  └──────────────────┘    │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Vue Flow (마인드맵 캔버스)                 │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────┬───────────────────────────────────────────┘
                  │ HTTP/REST API
                  ▼
┌─────────────────────────────────────────────────────────────┐
│                   백엔드 (FastAPI)                           │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                  API Layer                             │  │
│  │  ┌─────────┐  ┌─────────┐  ┌──────────┐  ┌────────┐ │  │
│  │  │ Boards  │  │  Nodes  │  │   AI     │  │  Auth  │ │  │
│  │  │   API   │  │   API   │  │   API    │  │  (TODO)│ │  │
│  │  └─────────┘  └─────────┘  └──────────┘  └────────┘ │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Service Layer                             │  │
│  │  ┌──────────────────┐  ┌─────────────────────────┐   │  │
│  │  │  Board Service   │  │   AI Expansion Service  │   │  │
│  │  │  Node Service    │  │   (GPT-4 통합)           │   │  │
│  │  └──────────────────┘  └─────────────────────────┘   │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Data Layer                                │  │
│  │  ┌────────┐  ┌────────┐  ┌────────┐  ┌──────────┐   │  │
│  │  │  User  │  │ Board  │  │  Node  │  │   Edge   │   │  │
│  │  │ Model  │  │ Model  │  │ Model  │  │  Model   │   │  │
│  │  └────────┘  └────────┘  └────────┘  └──────────┘   │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────┬───────────────────────┬──────────────────┘
                  │                       │
                  ▼                       ▼
    ┌─────────────────────────┐  ┌──────────────────┐
    │   PostgreSQL Database   │  │  Redis Cache     │
    │   (영구 저장소)           │  │  (세션, 캐싱)     │
    └─────────────────────────┘  └──────────────────┘

                  │
                  ▼
    ┌─────────────────────────┐
    │   OpenAI GPT-4 API      │
    │   (AI 기능)              │
    └─────────────────────────┘
```

## 컴포넌트 상세

### 1. 프론트엔드 아키텍처

#### Vue.js 3 기반 SPA
- **Framework**: Vue 3 Composition API
- **Language**: TypeScript
- **Build Tool**: Vite
- **Routing**: Vue Router 4
- **State Management**: Pinia
- **UI Library**: Element Plus
- **Canvas Library**: Vue Flow

#### 주요 컴포넌트

```
frontend/src/
├── components/
│   └── CustomNode.vue          # 마인드맵 노드 컴포넌트
├── views/
│   ├── HomeView.vue            # 홈 페이지
│   ├── BoardsView.vue          # 보드 목록
│   └── BoardView.vue           # 마인드맵 편집기
├── stores/
│   └── boardStore.ts           # 보드 상태 관리
├── services/
│   ├── api.ts                  # API 클라이언트
│   ├── boardService.ts         # 보드 API
│   ├── nodeService.ts          # 노드 API
│   └── aiService.ts            # AI API
└── types/
    └── index.ts                # TypeScript 타입 정의
```

#### 데이터 플로우

```
User Action → Component → Store (Pinia) → Service → API
                                ↓
                            State Update
                                ↓
                          UI Re-render
```

### 2. 백엔드 아키텍처

#### FastAPI 기반 비동기 REST API
- **Framework**: FastAPI
- **Language**: Python 3.11+
- **ORM**: SQLAlchemy (Async)
- **Migration**: Alembic
- **Validation**: Pydantic

#### 레이어 아키텍처

```
backend/app/
├── api/                        # API 엔드포인트
│   ├── boards.py               # 보드 CRUD
│   ├── nodes.py                # 노드 CRUD
│   └── ai.py                   # AI 기능
├── services/                   # 비즈니스 로직 (TODO)
├── ai/                         # AI 서비스
│   └── idea_expansion.py       # GPT-4 통합
├── models/                     # 데이터베이스 모델
│   ├── user.py
│   ├── board.py
│   ├── node.py
│   └── edge.py
├── schemas/                    # Pydantic 스키마
│   ├── board.py
│   ├── node.py
│   └── ai.py
└── core/                       # 핵심 설정
    ├── config.py               # 환경 설정
    ├── database.py             # DB 연결
    └── redis.py                # Redis 연결
```

#### 요청 처리 플로우

```
HTTP Request → API Router → Pydantic Validation
                                ↓
                          Service Layer (AI/Business)
                                ↓
                          Database (SQLAlchemy)
                                ↓
                          Pydantic Schema → JSON Response
```

### 3. 데이터베이스 설계

#### ERD (Entity Relationship Diagram)

```
┌──────────────┐         ┌──────────────┐
│    User      │         │    Board     │
├──────────────┤         ├──────────────┤
│ id (PK)      │────┬───▶│ id (PK)      │
│ email        │    │    │ user_id (FK) │
│ username     │    │    │ title        │
│ password     │    │    │ description  │
│ created_at   │    │    │ is_public    │
└──────────────┘    │    │ created_at   │
                    │    └──────────────┘
                    │            │
                    │            │ 1:N
                    │            ▼
                    │    ┌──────────────┐
                    │    │    Node      │
                    │    ├──────────────┤
                    │    │ id (PK)      │
                    └───▶│ board_id (FK)│
                         │ title        │
                         │ content      │
                         │ position_x   │
                         │ position_y   │
                         │ color        │
                         │ impact_score │
                         │ feasibility  │
                         │ priority     │
                         │ ai_generated │
                         └──────────────┘
                                │
                                │ N:M
                                ▼
                         ┌──────────────┐
                         │    Edge      │
                         ├──────────────┤
                         │ id (PK)      │
                         │ board_id (FK)│
                         │ source_id(FK)│
                         │ target_id(FK)│
                         │ edge_type    │
                         │ label        │
                         └──────────────┘
```

#### 인덱스 전략

- `users.email` - UNIQUE INDEX
- `users.username` - UNIQUE INDEX
- `boards.user_id` - INDEX
- `nodes.board_id` - INDEX
- `edges.board_id` - INDEX
- `edges.source_id` - INDEX
- `edges.target_id` - INDEX

### 4. AI 서비스 아키텍처

#### GPT-4 통합 플로우

```
User Request (노드 확장)
        ↓
API Endpoint (/api/ai/expand)
        ↓
IdeaExpansionService
        ↓
1. 컨텍스트 수집
   - 현재 노드 내용
   - 보드 제목
   - 관련 노드들
        ↓
2. 프롬프트 생성
   - 시스템 프롬프트
   - 사용자 컨텍스트
        ↓
3. OpenAI API 호출
   - Model: gpt-4-turbo-preview
   - Temperature: 0.8 (창의성)
   - Response Format: JSON
        ↓
4. 응답 파싱 및 검증
        ↓
5. 노드 생성 (배치)
        ↓
Response (새 노드 리스트)
```

#### AI 기능 목록

1. **아이디어 확장**
   - 입력: 노드 내용
   - 출력: 5개 관련 아이디어
   - 모델: GPT-4
   - 토큰: ~1500

2. **아이디어 평가**
   - 입력: 아이디어 텍스트
   - 출력: Impact (1-10), Feasibility (1-10), Priority
   - 모델: GPT-4
   - 토큰: ~500

3. **마인드맵 요약**
   - 입력: 전체 노드 리스트
   - 출력: 요약 텍스트 (3-5 문단)
   - 모델: GPT-4
   - 토큰: ~800

### 5. 보안 아키텍처

#### 인증 & 권한 (TODO)

```
┌──────────────────────────────┐
│   JWT Token Authentication   │
├──────────────────────────────┤
│ 1. 사용자 로그인             │
│ 2. Access Token 발급         │
│ 3. Refresh Token 저장(Redis) │
│ 4. 토큰 검증 미들웨어        │
└──────────────────────────────┘
```

#### CORS 설정

```python
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
    "https://thinkgraph.ai"  # 프로덕션
]
```

#### 환경 변수 관리

- `.env` 파일 사용
- `.env.example` 템플릿 제공
- 민감 정보 Git 제외 (.gitignore)

### 6. 성능 최적화

#### 백엔드 최적화

1. **비동기 I/O**
   - AsyncIO + asyncpg
   - 동시 요청 처리 능력 향상

2. **Redis 캐싱**
   - 세션 데이터
   - API 응답 캐싱 (TODO)

3. **데이터베이스 최적화**
   - 인덱스 활용
   - N+1 쿼리 방지 (Eager Loading)

#### 프론트엔드 최적화

1. **코드 스플리팅**
   - 라우트 기반 Lazy Loading
   - 동적 import

2. **상태 관리**
   - Pinia를 통한 효율적 상태 관리
   - 불필요한 리렌더링 방지

3. **Vue Flow 최적화**
   - 가상화 (1000+ 노드 지원)
   - 렌더링 최적화

### 7. 배포 아키텍처

#### 개발 환경

```
Docker Compose
├── PostgreSQL (5432)
├── Redis (6379)
├── Backend (8000)
└── Frontend (3000)
```

#### 프로덕션 환경 (TODO)

```
┌──────────────────────┐
│   Load Balancer      │
│   (Nginx/Caddy)      │
└──────────┬───────────┘
           │
     ┌─────┴─────┐
     ▼           ▼
┌─────────┐ ┌─────────┐
│Frontend │ │Frontend │
│ (Static)│ │ (Static)│
└─────────┘ └─────────┘
           │
     ┌─────┴─────┐
     ▼           ▼
┌─────────┐ ┌─────────┐
│Backend  │ │Backend  │
│ (API)   │ │ (API)   │
└─────────┘ └─────────┘
     │           │
     └─────┬─────┘
           ▼
    ┌─────────────┐
    │ PostgreSQL  │
    │ (Primary)   │
    └─────────────┘
           │
           ▼
    ┌─────────────┐
    │   Redis     │
    │ (Cluster)   │
    └─────────────┘
```

## 기술 결정 (Tech Decisions)

### 왜 Vue.js 3?
- Composition API로 로직 재사용성 향상
- TypeScript 완벽 지원
- 작은 번들 크기
- 뛰어난 성능

### 왜 FastAPI?
- 비동기 I/O 지원
- 자동 API 문서 생성
- Pydantic 타입 검증
- 뛰어난 성능

### 왜 PostgreSQL?
- 강력한 JSON 지원
- 복잡한 쿼리 지원
- ACID 트랜잭션
- 확장성

### 왜 Redis?
- 빠른 세션 관리
- 캐싱 성능
- Pub/Sub (실시간 협업용)

## 향후 개선 사항

1. **인증 시스템**
   - JWT 기반 인증
   - OAuth2 소셜 로그인

2. **실시간 협업**
   - WebSocket 통합
   - Operational Transform

3. **검색 기능**
   - Elasticsearch 통합
   - 전문 검색

4. **모니터링**
   - Prometheus + Grafana
   - 로그 수집 (ELK)

5. **CI/CD**
   - GitHub Actions
   - 자동 테스트
   - 자동 배포
