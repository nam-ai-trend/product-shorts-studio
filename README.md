# 🎬 Product Shorts Studio (쇼핑 쇼츠 자동 제작 스튜디오)

> 상품 URL이나 사진만 입력하면 **제품/회사 분석 → 스토리텔링/촬영 플랜 → 고속 TTS 음성 → Whisper STT 자막 씬 데이터(`scene_data.json`) → 실사 AI 에셋 & 영상 프롬프트 → Remotion 최종 영상 렌더링**까지 한 번에 자동 완성하는 올인원 쇼츠 제작 시스템입니다.

---

## 🌟 파이프라인 개요

Product Shorts Studio는 채널의 성격과 상품의 특성에 맞춰 **3가지 워크플로우**와 **5개의 전문 에이전트 스킬**을 제공합니다.

### 1. 2대 핵심 쇼츠 제작 파이프라인 비교

| 구분 | 1. 단일 제품 시연 쇼핑쇼츠 🛍️ | 2. 팩션(Faction) 썰 쇼핑쇼츠 📖🔥 |
|---|---|---|
| **슬래시 커맨드** | `/product-shorts-full-pipeline` | `/faction-shorts-full-pipeline` |
| **핵심 스킬** | `product-shorts-studio` | `faction-shorts-studio` |
| **핵심 컨셉** | **직접 시연 & 제품 USP 중심** (1초 만에 증명) | **재밌는 썰 스토리텔링으로 위장한 Soft Sell** |
| **영상 길이 / 배속** | **15초** / **1.2배속** TTS | **30초** / **1.5배속** TTS |
| **서사 구조** | **6비트 촬영 플랜** (결과 선공개 → 대비 → 시연 → 루프) | **4단계 팩션 서사** (도파민 후킹 → 빌드업 → 반전 → 여운) |
| **비주얼 연출** | 5-Cut 실물 누끼/사용 컷 & 손 앵커 고정 | 6-Cut 시네마틱 실사 컷 (Hands-Only & POV 룰) |
| **CTA 방식** | 루프 엔딩 + 직접적 전환 CTA | **Soft Sell** (품절 대란/군중심리 자극, 직접 CTA 지양) |
| **주요 적용 대상** | 제형/기능/비포애프터가 직관적인 상품 (뷰티, 청소 등) | 비하인드 스토리, 개발자 집착, 품절 대란이 있는 모든 상품 |

### 2. 고속 오디오/자막 생성 파이프라인

- **슬래시 커맨드**: `/tts-to-scene-pipeline`
- **핵심 스킬**: `tts-generate`, `stt-scene-align`
- **설명**: 작성된 대본(`script.md`)을 읽어 고품질 배속 TTS 음성을 생성하고, Whisper STT 기반으로 쇼츠 호흡(2~4단어)에 최적화된 자막 씬 데이터(`scene_data.json`)를 단독으로 생성합니다.

---

## 🛠️ 제공 스킬 (Agents Skills)

`.agents/skills/` 폴더 내에 탑재된 독립형 모듈들입니다:

| 스킬명 | 설명 및 주요 기능 |
|---|---|
| 🛍️ **`product-shorts-studio`** | 단일 제품 쇼츠 기획. 8대 카테고리 매핑, 15초 6비트 촬영 플랜, 5-Cut 실물/누끼 에셋 번들 생성 및 프롬프트 작성 |
| 📖 **`faction-shorts-studio`** | 팩션 썰 쇼츠 기획. 4단계 서사 구조(후킹→빌드업→클라이맥스→여운), Hands-Only & POV 룰 기반 6-Cut 종합 에셋 시트 생성 |
| 🔊 **`tts-generate`** | 로컬 Qwen3-TTS API 연동 및 FFmpeg 음정 유지 배속(1.2x / 1.5x) 변환 스크립트 (`generate.py`) |
| 🎯 **`stt-scene-align`** | OpenAI Whisper API 연동 및 쇼츠 자막 최적화 분할. 대본 기반 한글 숫자/기호 교정 및 프레임(30fps) 정밀 동기화 (`align.py`) |
| 🎥 **`remotion-render`** | Remotion 기반 9:16 비디오 자동 렌더링. 하이브리드 비디오 모드(단일/씬별), 중앙 볼드 자막 오버레이, 원본 오디오 보존(`--no-audio`) 옵션 (`render.py`) |

---

## 📦 시스템 요구사항 및 설치 (Prerequisites & Setup)

### 1. 시스템 요구사항
- **Python**: `>= 3.9`
- **Node.js**: `>= 18.0.0` (Remotion 렌더링용)
- **FFmpeg**: 시스템 PATH에 등록 필수 (오디오 배속 및 비디오 최적화용)
  ```bash
  # macOS (Homebrew)
  brew install ffmpeg
  ```
- **로컬 Qwen3-TTS 서버**: Pinokio 등을 통해 `http://127.0.0.1:7860`에서 가동

### 2. 의존성 설치

#### Python 패키지 설치
프로젝트 루트에서 아래 명령어를 실행합니다:
```bash
pip install -r requirements.txt
```

#### Remotion (Node.js) 패키지 설치
`my-video` 디렉터리로 이동하여 의존성을 설치합니다:
```bash
cd my-video
npm install
cd ..
```

### 3. 환경 변수 설정 (.env)
루트의 `.env.example` 파일을 복사하여 `.env` 파일을 만들고 OpenAI API 키를 입력합니다:
```bash
cp .env.example .env
```
`.env` 파일 내용:
```env
OPENAI_API_KEY=sk-...your_openai_api_key_here...
```

### 4. 레퍼런스 보이스 준비
- 루트 디렉터리에 `reference_voice.mp3` 파일을 배치하거나, 원하는 샘플 음성 파일을 지정합니다.

---

## 🚀 파이프라인별 상세 실행 방법

### 📌 1. 단일 제품 시연 쇼핑쇼츠 (15초)
상품 URL이나 제품 이미지를 제시한 후 아래 명령어 실행:
```text
/product-shorts-full-pipeline
```
1. **STEP 1**: `PRODUCT_TRUTH` 작성 & 8대 카테고리 전략 매핑
2. **STEP 2**: 15초 6비트 촬영 플랜 & 영상 프롬프트 작성
3. **STEP 3**: 프로젝트 폴더(`outputs/YYMMDD_HHMM/`) 생성 & 5-Cut 에셋 생성
4. **STEP 4**: 로컬 Qwen3-TTS 실행 (`output_1.2x.wav`)
5. **STEP 5**: OpenAI Whisper STT 정렬 (`scene_data.json`)
6. **STEP 6**: 씬 길이 검토 및 조정

---

### 📌 2. 팩션(Faction) 썰 쇼핑쇼츠 (30초)
상품 링크 또는 제품 사진 + 제품명/회사명을 제시한 후 아래 명령어 실행:
```text
/faction-shorts-full-pipeline
```
1. **STEP 1**: 제품·회사 리서치 & `STORY_TRUTH` 작성, 공용 레퍼런스 풀 확보
2. **STEP 2**: 4단계 팩션 스크립트 작성 (`script.md`, `plan.md`)
3. **STEP 3**: 1.5배속 고속 TTS 음성 생성 (`output_1.5x.wav`)
4. **STEP 4**: STT 자막 씬 데이터 생성 (`scene_data.json`) 및 정밀 타임코드 확정
5. **STEP 5**: 씬별 AI 에셋 & 6-Cut 종합 에셋 시트(`asset_sheet.jpg`) 생성
6. **STEP 6**: AI 영상 프롬프트(`prompts.md`) & 배포 킷(`publish_kit.md`) 최종 확정

---

### 📌 3. 최종 비디오 렌더링 (`remotion-render`)
생성된 씬 데이터와 영상 클립(단일 비디오 또는 씬별 `scene1.mp4`~`sceneN.mp4`)을 합성하여 최종 9:16 쇼츠 비디오를 제작합니다:

```bash
# 최신 미처리 outputs 폴더 자동 감지 및 렌더링
python3 .agents/skills/remotion-render/scripts/render.py

# 특정 작업 폴더 지정 렌더링
python3 .agents/skills/remotion-render/scripts/render.py outputs/260903_2326

# 원본 배경 영상 오디오 보존 (TTS 나레이션 제외 모드)
python3 .agents/skills/remotion-render/scripts/render.py outputs/260903_2326 --no-audio
```

---

## 📂 프로젝트 디렉토리 구조

```text
12_product-shorts-studio/
├── .agents/
│   ├── skills/
│   │   ├── faction-shorts-studio/    # 팩션 썰 기획 스킬
│   │   ├── product-shorts-studio/    # 단일 제품 시연 쇼츠 기획 스킬
│   │   ├── remotion-render/          # Remotion 자동 렌더링 스크립트
│   │   ├── stt-scene-align/          # Whisper STT 자막 싱크 스크립트
│   │   └── tts-generate/             # Qwen3-TTS 연동 및 배속 스크립트
│   └── workflows/
│       ├── faction-shorts-full-pipeline.md
│       ├── product-shorts-full-pipeline.md
│       └── tts-to-scene-pipeline.md
├── my-video/                         # Remotion React 프로젝트 (자막 오버레이 및 비디오 컴포지션)
├── outputs/                          # 파이프라인 작업별 산출물 폴더 (gitignore 대상)
├── .env.example                      # 환경변수 템플릿
├── .gitignore                        # Git 추적 제외 설정
├── reference_voice.mp3               # TTS 클로닝용 기본 레퍼런스 음성
├── requirements.txt                  # Python 의존성 목록
└── README.md                         # 프로젝트 안내 문서
```

---

## 📁 산출물 세부 구성 (`outputs/YYMMDD_HHMM/`)

| 파일명 | 용도 및 내용 |
|---|---|
| 📄 `plan.md` | 기획안 (`PRODUCT_TRUTH` / `STORY_TRUTH`), 타임라인, 훅 가이드 |
| 📄 `script.md` | TTS 및 자막용 보이스오버 대본 (발음 표기 최적화) |
| 🔊 `output_*.wav` | 1.2배속 / 1.5배속 고음질 나레이션 음성 파일 |
| 📊 `raw_stt.json` | Whisper STT 원본 타임코드 데이터 |
| 🎬 `scene_data.json` | 2~4단어 호흡으로 분할/교정된 최종 자막 씬 데이터 |
| 🖼️ `asset_sheet.jpg` | 전체 씬 에셋을 한눈에 보는 콘택트 시트 (팩션 파이프라인) |
| 📁 `assets/` | 씬별 9:16 실사 이미지 및 원본 레퍼런스 이미지 |
| 📄 `prompts.md` | Kling / Runway / Luma용 I2V 및 T2I 영상 프롬프트 |
| 📄 `publish_kit.md` | 썸네일 카피, 유튜브 쇼츠·릴스·틱톡용 제목/설명/해시태그 |
| 🎥 `output.mp4` | Remotion 스킬 실행 시 최종 완성되는 9:16 쇼츠 영상 |
