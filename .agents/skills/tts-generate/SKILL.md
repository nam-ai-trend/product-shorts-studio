---
name: tts-generate
description: 로컬 Qwen3-TTS를 사용하여 텍스트를 음성으로 변환하고 1.2배속 후처리를 수행합니다.
---

# tts-generate

로컬 Qwen3-TTS (Pinokio) API를 호출하여 고정된 레퍼런스 목소리로 음성을 생성하고, FFmpeg를 사용하여 1.2배속으로 변환하는 스킬입니다.

## 주요 기능
- **고정 레퍼런스 보이스**: `/Users/gwn/antigravity/voice/reference_voice.mp3` 파일을 레퍼런스로 활용합니다.
- **고정 레퍼런스 텍스트**: 보이스 복제의 정확도를 극대화하고 처리 성능을 높이기 위해 아래의 지정된 스크립트 텍스트를 고정하여 사용합니다.
  > "안녕하세요 여러분. 반갑습니다. 오늘도 저희 채널을 찾아주셔서 감사합니다. 영상이 도움되셨다면 구독과 좋아요를 눌러주세요."
- **1.2배속 후처리**: FFmpeg `atempo` 필터를 사용하여 음정 변화 없이 속도만 1.2배속으로 조절합니다.
- **자동화된 outputs 하위폴더 감지**:
  - `outputs` 폴더 하위에 작업별 폴더(예: `outputs/my_project`)를 만들고 그 안에 `.md` 스크립트 파일을 준비합니다.
  - 스크립트 실행 시 폴더명만 인자로 주거나, 인자 없이 실행하여 아직 처리되지 않은 가장 최신의 하위폴더를 자동으로 추적해 TTS 음성을 생성할 수 있습니다.

## 사용 방법
1. 로컬 Qwen3-TTS 서버가 `http://127.0.0.1:7860`에서 정상 작동하고 있는지 확인합니다.
2. `outputs/` 폴더 하위에 임의의 폴더를 생성하고, 그 안에 대사를 담은 `.md` 파일을 준비합니다. (예: `outputs/test_folder/script.md`)
3. 아래 방식들 중 하나를 사용해 스킬을 실행합니다.

```bash
# 방법 1: 인자 없이 실행 (outputs 폴더 내 미처리된 최신 하위 폴더 자동 탐색)
python3 .agents/skills/tts-generate/scripts/generate.py

# 방법 2: 하위 폴더 이름만 지정
python3 .agents/skills/tts-generate/scripts/generate.py test_folder

# 방법 3: 전체 상대/절대 경로 지정
python3 .agents/skills/tts-generate/scripts/generate.py outputs/test_folder
```

## 환경 요구 사항
- Python 3.9+
- `requests` 라이브러리
- `ffmpeg` 설치 (시스템 경로)
