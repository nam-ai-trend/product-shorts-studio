---
name: tts-to-scene-pipeline
description: 특정 폴더의 대본을 TTS로 변환하고, 자막용 씬 데이터(JSON) 및 음성 파일까지 생성하는 워크플로우입니다. (렌더링 제외)
---

# tts-to-scene-pipeline

이 워크플로우는 영상 제작을 위한 음성 소스(1.2배속)와 자막 데이터를 생성하는 공정입니다. 최종 비디오 렌더링은 이 단계 이후에 개별적으로 진행됩니다.

## 실행 단계

### 1단계: 음성 생성 (tts-generate)
- `reference_voice.mp3`를 사용하여 보이스 클로닝을 수행합니다.
- 생성된 음성을 1.2배속으로 변환하여 `output_1.2x.wav`를 생성합니다.

### 2단계: 자막 및 씬 데이터 생성 (stt-scene-align)
- 생성된 음성을 Whisper STT로 변환합니다.
- 원본 대본과 대조하여 숫자, 고유명사 등을 교정합니다.
- 한 문장(블록) 단위로 씬을 분리하여 `scene_data.json`을 생성합니다.

## 실행 방법

루트의 `outputs/` 폴더 내에 주제별 폴더(예: `outputs/my_topic`)를 생성하고, 해당 경로 또는 하위 폴더명을 인자로 주어 아래 스크립트를 순차적으로 실행합니다.

```bash
# 1. TTS 생성 (인자가 없으면 outputs/ 내 미처리 최신 폴더를 자동 추적합니다)
python3 .agents/skills/tts-generate/scripts/generate.py outputs/my_topic

# 2. STT 및 씬 데이터 생성
python3 .agents/skills/stt-scene-align/scripts/align.py outputs/my_topic
```

## 완료 시 결과물 (`outputs/하위폴더/` 하위)
- `output_1.2x.wav`: 1.2배속 음성 파일
- `raw_stt.json`: 원본 STT 데이터
- `scene_data.json`: 최종 자막용 씬 데이터
- `script.md`: 원본 대본


