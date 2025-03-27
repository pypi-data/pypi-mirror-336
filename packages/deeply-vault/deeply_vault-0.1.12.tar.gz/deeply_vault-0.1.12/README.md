# Deeply CLI

`dotenv-vault`와 유사한 환경 변수 관리 CLI 도구입니다. 프로젝트의 `.env` 파일들을 중앙 서버에 안전하게 관리하고 팀원들과 공유할 수 있습니다.

## 설치 방법

```bash
# 개발 모드로 설치
pip install -e .

# 또는 일반 설치
pip install .
```

## 사용 방법

### 프로젝트 초기화

```bash
# 현재 디렉토리를 프로젝트로 초기화
deeply init

# 특정 볼트 이름으로 초기화
deeply init --vault my-project
```

### 로그인

```bash
# 서버에 로그인
deeply login

# 다른 서버 주소 지정
deeply login --server https://env.example.com
```

### 볼트 생성

```bash
# 새로운 볼트 생성
deeply new my-project

# 설명과 함께 볼트 생성
deeply new my-project --description "내 프로젝트 환경 변수" --kms-key-id "키ID"
```

### 환경 파일 목록 조회

```bash
# 로컬 환경 파일 목록 조회
deeply list

# 서버에 저장된 환경 목록 조회
deeply list --remote
```

### 환경 파일 업로드

```bash
# development 환경 파일 업로드
deeply push

# production 환경 파일 업로드
deeply push production

# 모든 환경 파일 업로드
deeply push --all

# 특정 파일만 업로드
deeply push --file .env.staging --file server/api/.env.staging
```

### 환경 파일 다운로드

```bash
# development 환경 파일 다운로드
deeply pull

# production 환경 파일 다운로드
deeply pull production

# 다른 디렉토리에 다운로드
deeply pull production --output ./config

# 기존 파일 덮어쓰기
deeply pull production --force
```

## 설정 파일

프로젝트 루트에 `.env.vault.yml` 파일이 생성되며, 다음과 같은 설정을 포함합니다:

```yaml
vault: my-project
server: http://localhost:8000
environments:
  - development
  - production
  - staging
token: YOUR_API_TOKEN
```

## 보안

- 모든 환경 변수는 서버에서 암호화되어 저장됩니다.
- API 토큰은 로컬에 저장되며, 절대 공유하지 마세요.
- AWS KMS를 사용하여 높은 수준의 보안을 제공합니다.
