# Windows용 설치 스크립트
$ErrorActionPreference = "Stop"

# Python이 설치되어 있는지 확인
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Python이 설치되어 있지 않습니다. Python 3.8 이상을 설치해주세요."
    exit 1
}

# pip가 설치되어 있는지 확인
if (-not (Get-Command pip -ErrorAction SilentlyContinue)) {
    Write-Host "pip가 설치되어 있지 않습니다. Python과 함께 설치해주세요."
    exit 1
}

# 가상환경 생성 및 활성화
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 패키지 설치
pip install -e .

Write-Host "deeply-vault가 성공적으로 설치되었습니다."
Write-Host "사용 방법: deeply-vault --help" 