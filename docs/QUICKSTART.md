# ThinkGraph 빠른 시작 가이드

## 📋 목차
1. [사전 요구사항](#사전-요구사항)
2. [설치 방법](#설치-방법)
3. [실행 방법](#실행-방법)
4. [사용 방법](#사용-방법)
5. [문제 해결](#문제-해결)

## 사전 요구사항

### 로컬 개발 환경
- Python 3.11 이상
- Node.js 18 이상
- PostgreSQL 15 이상
- Redis 7 이상
- OpenAI API 키 (필수)

### Docker 환경 (권장)
- Docker 20.10 이상
- Docker Compose 2.0 이상
- OpenAI API 키 (필수)

## 설치 방법

### 옵션 1: Docker Compose (권장)

1. **저장소 클론**
```bash
git clone https://github.com/k1300k/ai-dashboard.git
cd ai-dashboard
```

2. **환경 변수 설정**
```bash
# 백엔드 환경 변수
cp backend/.env.example backend/.env

# frontend/.env 파일을 편집하여 OPENAI_API_KEY 설정
# backend/.env 파일을 열고 다음 값을 수정:
# OPENAI_API_KEY=sk-your-actual-api-key-here
```

3. **서비스 시작**
```bash
docker-compose up -d
```

4. **데이터베이스 초기화**
```bash
# 컨테이너에 접속하여 마이그레이션 실행
docker-compose exec backend alembic upgrade head
```

5. **접속**
- 프론트엔드: http://localhost:3000
- 백엔드 API: http://localhost:8000
- API 문서: http://localhost:8000/docs

### 옵션 2: 로컬 개발 환경

#### 백엔드 설정

1. **PostgreSQL 설정**
```bash
# PostgreSQL에 접속
psql -U postgres

# 데이터베이스 생성
CREATE DATABASE thinkgraph;
CREATE USER thinkgraph WITH PASSWORD 'thinkgraph_password';
GRANT ALL PRIVILEGES ON DATABASE thinkgraph TO thinkgraph;
```

2. **Redis 시작**
```bash
redis-server
```

3. **백엔드 설치 및 실행**
```bash
cd backend

# 가상 환경 생성
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
cp .env.example .env
# .env 파일을 편집하여 OPENAI_API_KEY와 DATABASE_URL 설정

# 데이터베이스 마이그레이션
alembic upgrade head

# 서버 실행
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 프론트엔드 설정

1. **프론트엔드 설치 및 실행**
```bash
cd frontend

# 의존성 설치
npm install

# 환경 변수 설정
cp .env.example .env
# .env 파일을 편집 (기본값으로도 동작)

# 개발 서버 실행
npm run dev
```

2. **접속**
- 프론트엔드: http://localhost:3000
- 백엔드 API: http://localhost:8000
- API 문서: http://localhost:8000/docs

## 실행 방법

### Docker Compose 사용 시

```bash
# 서비스 시작
docker-compose up -d

# 로그 확인
docker-compose logs -f

# 특정 서비스 로그 확인
docker-compose logs -f backend
docker-compose logs -f frontend

# 서비스 중지
docker-compose down

# 데이터와 함께 완전히 제거
docker-compose down -v
```

### 로컬 환경 사용 시

**터미널 1 (백엔드):**
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

**터미널 2 (프론트엔드):**
```bash
cd frontend
npm run dev
```

## 사용 방법

### 1. 첫 보드 만들기

1. 브라우저에서 http://localhost:3000 접속
2. "시작하기" 버튼 클릭
3. "새 보드 만들기" 클릭
4. 제목과 설명 입력 후 "만들기" 클릭

### 2. 노드 추가하기

1. 보드 화면에서 "노드 추가" 버튼 클릭
2. 노드를 클릭하여 제목과 내용 편집
3. 노드를 드래그하여 위치 조정

### 3. AI 아이디어 확장

1. 노드를 클릭하여 선택
2. 노드 위의 ✨ 버튼 클릭
3. AI가 자동으로 5개의 관련 아이디어 생성
4. 생성된 아이디어들이 자동으로 노드에 연결됨

### 4. AI 아이디어 평가

1. 노드를 클릭하여 선택
2. 노드 위의 📊 버튼 클릭
3. AI가 임팩트, 실현가능성, 우선순위 점수 산출
4. 노드 상세 패널에서 점수 확인

### 5. AI 마인드맵 요약

1. 상단의 "AI 요약" 버튼 클릭
2. AI가 전체 마인드맵을 분석하여 요약 생성
3. 주요 인사이트와 추천 사항 확인

## 문제 해결

### OpenAI API 오류

**문제:** "OpenAI API key not found" 오류
**해결:**
```bash
# backend/.env 파일 확인
cat backend/.env | grep OPENAI_API_KEY

# 키가 없다면 추가
echo "OPENAI_API_KEY=sk-your-actual-key" >> backend/.env

# 서버 재시작
docker-compose restart backend  # Docker 사용 시
# 또는 uvicorn을 재시작 (로컬 환경)
```

### 데이터베이스 연결 오류

**문제:** "Could not connect to PostgreSQL"
**해결:**
```bash
# PostgreSQL 서비스 확인
docker-compose ps  # Docker 사용 시
# 또는
sudo systemctl status postgresql  # Linux
brew services list  # macOS

# 연결 테스트
psql -U thinkgraph -d thinkgraph -h localhost
```

### 프론트엔드 빌드 오류

**문제:** npm install 실패
**해결:**
```bash
# 캐시 정리
cd frontend
rm -rf node_modules package-lock.json
npm cache clean --force

# 재설치
npm install
```

### CORS 오류

**문제:** "Access-Control-Allow-Origin" 오류
**해결:**
```bash
# backend/.env 파일에서 ALLOWED_ORIGINS 확인
cat backend/.env | grep ALLOWED_ORIGINS

# 프론트엔드 URL이 포함되어 있는지 확인
# 예: ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

### Docker 컨테이너 재시작

```bash
# 모든 컨테이너 재시작
docker-compose restart

# 특정 컨테이너만 재시작
docker-compose restart backend
docker-compose restart frontend

# 컨테이너 재빌드
docker-compose up -d --build
```

## 개발 모드

### 백엔드 개발

```bash
cd backend

# 테스트 실행
pytest

# 코드 포맷팅
black app/

# 린트 검사
flake8 app/

# 타입 체크
mypy app/
```

### 프론트엔드 개발

```bash
cd frontend

# 린트 검사
npm run lint

# 코드 포맷팅
npm run format

# 프로덕션 빌드
npm run build

# 빌드 미리보기
npm run preview
```

## 환경 변수 상세

### 백엔드 (.env)

```env
# 데이터베이스
DATABASE_URL=postgresql://thinkgraph:thinkgraph_password@localhost:5432/thinkgraph

# Redis
REDIS_URL=redis://localhost:6379

# OpenAI (필수)
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_MODEL=gpt-4-turbo-preview

# 보안
SECRET_KEY=your-secret-key-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173

# 환경
ENVIRONMENT=development
DEBUG=True
```

### 프론트엔드 (.env)

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000/ws
```

## 추가 리소스

- [API 문서](http://localhost:8000/docs) - Swagger UI
- [API 문서 (ReDoc)](http://localhost:8000/redoc) - ReDoc
- [GitHub 저장소](https://github.com/k1300k/ai-dashboard)
- [이슈 리포트](https://github.com/k1300k/ai-dashboard/issues)

## 다음 단계

1. [Architecture.md](./ARCHITECTURE.md) - 시스템 아키텍처 이해
2. [API.md](./API.md) - API 상세 문서
3. [Contributing.md](./CONTRIBUTING.md) - 기여 가이드
