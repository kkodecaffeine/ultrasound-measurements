# 초음파 측정

이 저장소는 초음파 영상에서 태아 측정을 추출하고 분석하는 도구를 제공합니다.  
초음파 영상을 처리하여 태아의 치수를 추정하고, 의료 및 연구 목적으로 활용할 수 있는 기능을 제공합니다.

## 주요 기능

- **태아 측정 추정**: 초음파 영상에서 자동으로 주요 치수를 탐지하고 계산합니다.
- **영상 전처리**: 다양한 영상 포맷을 지원하며, 일관된 분석을 위해 데이터를 전처리합니다.
- **확장 가능한 프레임워크**: 대규모 초음파 영상 데이터를 처리할 수 있도록 설계되었습니다.
- **유연한 디자인**: 추가 측정 항목이나 영상 포맷을 손쉽게 확장할 수 있습니다.

## 시작하기

### 필수 조건

이 프로젝트를 사용하기 전에 다음이 설치되어 있어야 합니다:

- [Python](https://www.python.org/) (v3.8 이상)
- 영상 처리 도구 `ffmpeg`

### 설치

1. 저장소를 클론합니다:
   ```bash
   git clone https://github.com/kkodecaffeine/ultrasound-measurements.git
   cd ultrasound-measurements