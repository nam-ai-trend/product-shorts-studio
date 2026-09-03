---
name: stt-scene-align
description: .wav 파일과 대본을 비교하여 쇼츠 영상에 최적화된 짧은 자막용 씬 데이터를 생성합니다. (의미 단위를 고려한 분할)
---

# stt-scene-align

OpenAI Whisper API를 사용하여 음성을 텍스트로 변환하고, 원본 대본(`script.md`)을 참고하여 텍스트 교정 및 쇼츠용 자막 최적화 분할 작업을 수행합니다.

## 주요 기능
- **Whisper STT**: OpenAI API를 통한 정확한 타임라인 추출.
- **하이브리드 교정**: 발음 위주의 대본을 자막용(숫자, 기호, 고유명사)으로 자동 변환 및 정렬.
- **쇼츠 자막 최적화 분할**: 모바일 쇼츠 환경에 어울리도록 문맥과 의미 단위를 분석하여 한 화면에 2~4단어(15자 내외) 정도의 짧고 직관적인 자막 호흡으로 씬을 쪼개어 `scene_data.json`을 구성합니다.
- **프레임 계산**: 30 FPS 기준 `duration_frames` 자동 계산.

## 사용 방법
1. `.env` 파일에 `OPENAI_API_KEY`가 설정되어 있는지 확인합니다.
2. 대상 폴더(예: `outputs/my_project`)에 `output_1.2x.wav`와 `script.md` 파일이 있어야 합니다.
3. 아래 명령어를 통해 스킬을 실행합니다.

```bash
python3 .agents/skills/stt-scene-align/scripts/align.py outputs/my_project
```

## 결과물
- `raw_stt.json`: Whisper에서 추출한 원본 데이터.
- `scene_data.json`: 최종 교정 및 문장 단위로 분할된 씬 데이터.
