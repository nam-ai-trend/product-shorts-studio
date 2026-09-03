---
name: product-shorts-full-pipeline
description: 상품 URL 또는 이미지를 입력하면 제품 분석, 6비트 촬영 플랜, 보이스오버 대본 작성부터 TTS 음성 생성, 자막 씬 데이터(scene_data.json) 생성 후, 확정된 타임코드에 맞춰 1x3 기반 AI 에셋 시트 및 영상 프롬프트를 자동으로 완성하는 워크플로우입니다. (영상 클립 생성 제외)
---

# 상품 쇼핑쇼츠 풀 파이프라인

이 워크플로우는 상품 URL 또는 이미지를 받아 영상 제작 직전 단계까지 완전 자동으로 진행한다.
최종 영상 클립 생성(Kling, Runway 등)은 사용자가 직접 도구에서 실행한다.

## 전제 조건 (시작 전 반드시 확인)

- [ ] 로컬 Qwen3-TTS 서버가 `http://127.0.0.1:7860`에서 실행 중인가
- [ ] `/Users/gwn/antigravity/voice/reference_voice.mp3` 또는 프로젝트 루트의 `reference_voice.mp3` 파일이 존재하는가
- [ ] `.env` 파일에 `OPENAI_API_KEY`가 설정되어 있는가

---

## 실행 단계

### STEP 1 — 제품 분석 & 원천 레퍼런스 풀 확보 & PRODUCT_TRUTH 작성

**에이전트 실행**

1. **원천 레퍼런스 수집**:
   - 상품 URL이 있으면 브라우저로 접속해 다각도 실물 사진을 신속하게(최대 2~3분 내) 캡처하여 `outputs/YYMMDD_HHMM/assets/ref_cut1.png` 등으로 저장한다.
   - 사용자 이미지 제공 시: 사용자가 올린 이미지를 `outputs/YYMMDD_HHMM/assets/ref_cut1.png` 등으로 저장한다.
2. 아래 항목을 채운 `PRODUCT_TRUTH`를 작성한다.

```yaml
PRODUCT_TRUTH:
  name:           # 제품명
  identifier:     # 상품 ID / ASIN / 옵션 코드
  color:          # 색상
  material:       # 재질
  size:           # 크기·용량
  shape:          # 외형 특징 (버튼, 이음새, 로고 위치 등)
  verified_use:   # 확인된 용도 한 가지
  verified_result: # 눈으로 보이는 결과 한 가지
```

3. **카테고리 판별 및 전략 매핑**: 식품, 뷰티, 패션, 주방, 생활, 가전, 여행, 문구 등 카테고리를 분류하고 `references/category-strategies.md`의 훅/시연/사운드 전략을 잠근다.

---

### STEP 2 — 6비트 촬영 플랜 & 보이스오버 대본 작성 & 폴더 생성

**에이전트 실행**

1. **현재 시각 기준 폴더 생성**: `outputs/YYMMDD_HHMM/`
2. **6비트 타임라인 설계** (기본: 3+2+2+4+2+2 = 15초)
3. **훅 3종** — 문제 해결형·비포애프터형·ASMR형, 기본안 표시
4. `plan.md`와 `script.md` 작성 및 저장:

| 비트 | 역할 | 기본 초 | 에셋 컷 (1:1 매칭) | 구도 | 손 동작 |
|---|---|---|---|---|---|
| **비트 1** | **결과 선공개 (오프닝)** | 3초 | **Cut 1 (Result / Hook)** | 45도 또는 정면 클로즈업 | — |
| **비트 2** | 대비 (비포) | 2초 | **Cut 2 (Before / Problem)** | 같은 앵글 하드컷 | — |
| **비트 3** | 제품 공개 | 2초 | **Cut 3 (Hero / Product)** | 정면 고정 | 들어올리기 |
| **비트 4** | **핵심 시연** | 4초 | **Cut 4 (Action / Detail)** | 탑다운 또는 45도 | 핵심 동작 하나 |
| **비트 5** | 재훅 (결과 증명) | 2초 | **Cut 5 (Re-Hook / Proof)** | 클로즈업 | 집어 올리기 |
| **비트 6** | 루프 엔딩 + CTA | 2초 | **Cut 6 (Loop / Anchor)** | 정면 packshot | 내려놓기 |

`script.md` 작성 규칙:
- 문장 단위 줄 분리 (stt-scene-align이 1:1로 씬에 매핑)
- 숫자는 한글 발음으로 표기 (예: `46그램` → `사십육 그램`)
- 총 발화 구간: 목표 길이 − 마지막 CTA 2초 (15초 영상이면 약 12–13초)
- 마지막 CTA 문장은 별도 줄로 분리

---

### STEP 3 — TTS 음성 생성 (1.2배속)

**에이전트가 스크립트 실행**

> ⚠️ Qwen3-TTS 서버(`http://127.0.0.1:7860`)가 실행 중이어야 한다.

```bash
python3 .agents/skills/tts-generate/scripts/generate.py outputs/{project}
```

결과물: `outputs/{project}/output_1.2x.wav`
실행 후 에이전트가 파일 생성 여부를 확인한다.

---

### STEP 4 — 자막 씬 데이터 생성 & 타임코드 확정

**에이전트가 스크립트 실행**

```bash
python3 .agents/skills/stt-scene-align/scripts/align.py outputs/{project}
```

결과물:
- `outputs/{project}/raw_stt.json`
- `outputs/{project}/scene_data.json`

실제 발화 음성의 각 씬별 시작/종료 타임코드를 분석하여 6개 비트의 정확한 지속 시간(초)을 확정한다.

---

### STEP 5 — 1x3 다중 에셋 시트 생성 (`asset_sheet_*.jpg`, 완벽한 9:16 비율) & 자동 분리

**에이전트 실행**

확정된 타임코드와 6비트 플랜에 맞춰 **16:9 가로 캔버스에 1행 3열(1x3) 배열**로 에셋 시트를 생성한다.
> 💡 **수학적 종횡비 일치 원리**: 16:9 가로 캔버스에 1행 3열을 나열하면 각 패널의 종횡비는 가로 $16/3 = 5.33$, 세로 $9 \rightarrow 9 / 5.33 \approx \mathbf{1.69}$로, 쇼츠 규격인 9:16 ($\approx \mathbf{1.78}$)과 거의 완벽히 일치하여 좌우 잘림 없는 초고화질 에셋을 얻을 수 있다.

1. **시트 분할 생성 (1x3 기준)**:
   - 6비트 영상인 경우: 3컷씩 2장으로 나누어 생성
     - `asset_sheet_1.jpg`: 비트 1 (오프닝 훅), 비트 2 (비포/대비), 비트 3 (히어로 제품)
     - `asset_sheet_2.jpg`: 비트 4 (시연), 비트 5 (재훅/결과), 비트 6 (루프 엔딩+CTA)
2. **빈 슬롯(Blank / Black Panel) 처리 룰**:
   - 총 컷 수가 4컷, 5컷 등 3의 배수가 아닌 경우, 마지막 시트의 남는 패널은 `"The 3rd panel must be left completely empty as a pure solid black background"`와 같이 명시하여 검정 배경으로 둔다.
   - 크롭 스크립트(`crop_asset_sheet.py`)가 검정/단색 빈 패널을 자동으로 감지하여 스킵하고 필요한 에셋만 순차 저장한다.
3. **제품 실물 일치 & 프롬프트 룰**:
   - 수집된 원천 레퍼런스 이미지를 `ImagePaths`에 주입하여 제품 형태·색상·로고 폰트를 보존한다.
   - 불필요한 UI나 자막이 생성되지 않도록 순수 상업 실사 사진(Pure commercial photographic contact sheet)으로 묘사한다.
4. **자동 분할 스크립트 실행**:
   ```bash
   python3 .agents/skills/product-shorts-studio/scripts/crop_asset_sheet.py outputs/{project}
   ```
   - 개별 9:16 에셋들(`assets/cut1_9_16.jpg` ~ `cut6_9_16.jpg`)이 오차 없이 1080×1920 해상도로 자동 저장된다.
   - 가이드 문서(`asset_sheet.md`)를 작성하여 저장한다.

---

### STEP 6 — 영상 프롬프트 & 발행 킷 최종 확정

**에이전트 실행**

1. `scene_data.json`의 실제 발화 타임코드와 컷별 에셋 이미지 파일을 1:1로 매핑하여 `prompts.md`를 작성한다. (Kling/Runway/Luma 공통 형식)
2. 유튜브 쇼츠, 인스타 릴스, 틱톡용 썸네일 카피와 본문 문구가 포함된 `publish_kit.md`를 작성한다.

---

## 최종 결과물 (`outputs/YYMMDD_HHMM/`)

| 파일 | 내용 |
|---|---|
| `plan.md` | PRODUCT_TRUTH, 6비트 타임라인 (실제 싱크 반영), 훅 3종 |
| `script.md` | 보이스오버 대본 |
| `output_1.2x.wav` | 1.2배속 음성 파일 |
| `raw_stt.json` | Whisper 원본 STT 데이터 |
| `scene_data.json` | 자막 타임코드 씬 데이터 |
| `asset_sheet_1.jpg`, `asset_sheet_2.jpg` | 1x3 단일 행 고화질 에셋 시트 이미지들 |
| `asset_sheet.md` | 실물 에셋 매핑 가이드 |
| `assets/` | 비트별 9:16 개별 이미지 에셋 (`cut1_9_16.jpg`...) |
| `prompts.md` | 비트별 영상 생성 프롬프트 (실제 타임코드 반영) |
| `publish_kit.md` | 썸네일·제목·설명·SEO 태그·플랫폼 문구 |

---

## 이후 단계 (사용자 직접)

1. 영상 생성 도구(Kling, Runway, Luma 등)에 `prompts.md`의 프롬프트 + `assets/`의 9:16 에셋 이미지 입력
2. 생성된 클립을 편집기(CapCut, Premiere 등) 또는 Remotion에서 조립
3. `scene_data.json` 기반 자막 타임코드를 편집기에서 적용
