#!/bin/bash

# Python이 설치되어 있는지 확인
if ! command -v python3 &> /dev/null; then
    echo "Python이 설치되어 있지 않습니다. Python 3.8 이상을 설치해주세요."
    exit 1
fi

# pip가 설치되어 있는지 확인
if ! command -v pip3 &> /dev/null; then
    echo "pip가 설치되어 있지 않습니다. Python과 함께 설치해주세요."
    exit 1
fi

# 가상환경 생성 및 활성화
python3 -m venv .venv
source .venv/bin/activate

# 패키지 설치
pip install -e .

echo "deeply-vault가 성공적으로 설치되었습니다."
echo "사용 방법: deeply-vault --help" 