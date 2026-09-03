---
name: remotion-render
description: outputs 하위폴더의 scene_data.json, 음성, 그리고 배경 비디오(단일 비디오 또는 씬별 비디오)를 합성하고 자막을 입혀 Remotion 비디오를 9:16 해상도로 렌더링합니다.
---

# remotion-render

`outputs/` 하위 폴더에 생성된 `scene_data.json`, `output_1.2x.wav`, 그리고 단일 배경 비디오 파일(예: `video.mov`, `video.mp4` 등) 또는 각 씬에 해당하는 개별 비디오 파일(`scene1.mp4`, `scene2.mp4` 등)을 읽어와서, Remotion을 사용해 음성과 자막이 싱크에 맞게 결합된 최종 9:16 비디오(`output.mp4`)를 자동 렌더링하는 스킬입니다.

## 주요 기능
- **하이브리드 비디오 모드**: 작업 폴더 내에 단일 비디오(예: `video.mov`, `video.mp4` 등)가 있으면 이를 전체 배경 비디오로 재생하며, 없을 경우에는 기존 방식대로 각 씬에 해당하는 개별 비디오(`scene{id}.mp4`)들을 순서대로 배치하여 재생합니다.
- **파라미터화된 렌더링**: 각 작업 폴더의 `scene_data.json` 데이터와 폴더명, 단일 비디오 파일명을 Remotion에 `inputProps`로 넘겨 동적으로 렌더링합니다.
- **비디오 최적화 및 음성 합성**: 기본적으로 비디오 파일에 대해 GOP=1(All-Intra) 변환 및 오디오 제거(Muted) 최적화를 진행하며, 전체 1.2배속 음성(나레이션)을 오디오 트랙으로 합성합니다.
- **오디오 제외 및 원본 오디오 보존 (disableAudio)**: 대본의 TTS 나레이션 음성(`output_1.2x.wav`)을 사용하지 않고, 배경 동영상의 원본 소리를 그대로 살리고 싶다면 `disableAudio: true` 프롭(또는 스크립트 실행 인자 `--no-audio`)을 사용할 수 있습니다. 이 경우 FFmpeg 최적화 단계에서 동영상의 원래 소리가 보존되며, Remotion의 `<Video>`도 음소거 해제(`muted={false}`) 상태로 렌더링됩니다.
- **자동 자막 생성**: `scene_data.json`에 정의된 개별 자막 블록의 타임스탬프(`start`, `end`)에 맞추어 Noto Sans KR 폰트 기반의 세련된 반투명 자막 오버레이(**63px of big subtitles**)를 **화면 정중앙(가운데) 정렬**하여 띄웁니다.
- **자동 폴더 탐색**: `outputs` 디렉토리 내에서 처리되지 않은 가장 최신의 하위폴더(즉, `scene_data.json`은 있지만 `output.mp4`는 없는 폴더)를 자동으로 찾아 렌더링을 진행할 수 있습니다.

## 사용 방법
아래 방식들 중 하나를 사용해 렌더링 스크립트를 실행합니다.

```bash
# 방법 1: 인자 없이 실행 (outputs 폴더 내 미처리된 최신 하위 폴더 자동 렌더링)
python3 .agents/skills/remotion-render/scripts/render.py

# 방법 2: 하위 폴더 이름만 지정
python3 .agents/skills/remotion-render/scripts/render.py test_project

# 방법 3: 전체 상대/절대 경로 지정
python3 .agents/skills/remotion-render/scripts/render.py outputs/test_project

# 방법 4: 원본 오디오 보존 및 TTS 나레이션 제외하고 실행 (--no-audio 추가)
python3 .agents/skills/remotion-render/scripts/render.py outputs/test_project --no-audio
```

## 완료 시 결과물 (`outputs/하위폴더/` 하위)
- `output.mp4`: 최종 합성 완료된 자막 및 음성 포함 비디오 파일
