---
name: faction-shorts-full-pipeline
description: 제품 링크 또는 제품 이미지를 입력하면 제품/회사 썰 리서치, 4단계 팩션 서사 스크립트 작성, 1.5배속 TTS 음성 생성 및 자막 씬 데이터(scene_data.json) 생성 후, 확정된 타임코드에 맞춰 씬별 AI 에셋과 종합 에셋 시트, 영상 프롬프트를 자동으로 완성하는 워크플로우입니다. (영상 클립 생성 제외)
---

# 팩션(Faction) 썰 쇼핑쇼츠 풀 파이프라인

이 워크플로우는 제품 링크(URL) 또는 사용자가 직접 제공한 제품 이미지를 받아, 제품/회사 썰을 리서치하고 머지한 뒤 영상 제작 직전 단계까지 완전 자동으로 진행한다.
최종 영상 클립 생성(Kling, Runway, Luma 등)은 사용자가 직접 도구에서 실행한다.

**콘셉트**: 대놓고 "이거 사세요" 하면 스와이프 당하니까, 철저하게 '재밌는 이야기'로 위장해서 끝까지 보게 만들고 스스로 제품을 검색하게 만든다.

## 전제 조건 (시작 전 반드시 확인)

- [ ] 로컬 Qwen3-TTS 서버가 `http://127.0.0.1:7860`에서 실행 중인가
- [ ] `/Users/gwn/antigravity/voice/reference_voice.mp3` 또는 프로젝트 루트의 `reference_voice.mp3` 파일이 존재하는가
- [ ] `.env` 파일에 `OPENAI_API_KEY`가 설정되어 있는가

## 입력 (둘 중 하나)

- **방식 A (URL 입력)**: 상품 링크 (쿠팡·스마트스토어·Amazon URL) + 제품명 + 회사명
- **방식 B (직접 이미지 제공)**: 제품 실물 이미지 파일들 (1~6장) + 제품명 + 회사명

---

## 실행 단계

### STEP 1 — 제품·회사 리서치, 원천 레퍼런스 풀 확보 & STORY_TRUTH 작성

**에이전트 실행**

1. **원천 레퍼런스 풀 (Reference Pool) 수집**:
   - **URL 제공 시**: `browser_subagent`로 상품 페이지에 접속해 다각도 실물 사진을 **신속하게 (최대 2~3분 이내)** 캡처하여 `outputs/YYMMDD_HHMM/assets/ref_cut1.png` ~ `ref_cut6.png`로 저장한다. (제품 외형, 제형, 비포애프터 실측 컷 위주로 집중 확보)
   - **사용자 이미지 제공 시**: 사용자가 올린 이미지를 `outputs/YYMMDD_HHMM/assets/ref_cut1.png` ~ `ref_cutN.png`로 저장한다.
   - 💡 *수집된 원천 사진들은 특정 씬에 구속되지 않는 공용 참조 풀(Pool)로 관리하며, 실제 제품 외형과 100% 일치하도록 보장한다.*

2. **제품 썰 리서치** (웹 검색 + 상품 페이지 크롤링)
   - 제품 개발 비하인드, 히트 스토리, 품절 대란, 논란, 밈화 사례
   - 제품의 USP(핵심 차별점), 시각적·감각적 타격감 포인트
   - 커뮤니티 반응, 유명인 언급, 뉴스 기사

3. **회사 썰 리서치** (웹 검색)
   - 창업자 스토리, 위기·실패·반전 에피소드
   - 집착·광기 사례, 전 재산 투입 같은 드라마
   - 성장 서사, 어이없는 매출·성공 현상

4. **두 썰 머지** → `STORY_TRUTH` 작성:

```yaml
STORY_TRUTH:
  product_name:        # 제품명
  company_name:        # 회사명
  category:            # 식품/뷰티/패션/생활/가전 등
  product_url:         # 상품 링크 (있는 경우)

  # 제품 썰
  product_story:
    hook_material:     # 후킹에 쓸 자극적 소재 (분노/광기/집착)
    origin_drama:      # 개발 배경의 드라마 (결핍/빡침/우연)
    usp_visual:        # 시각적 타격감으로 표현할 USP
    usp_sensory:       # 감각적 언어로 포장할 USP
    viral_fact:        # 바이럴 팩트 (품절/매출/유명인 언급)

  # 회사 썰
  company_story:
    founder_drama:     # 창업자의 미친 에피소드
    crisis_moment:     # 위기/실패 순간
    obsession_proof:   # 집착/광기의 증거
    comeback_result:   # 반전 결과 (대박/성공)

  # 머지된 서사 뼈대
  merged_narrative:
    hook_line:         # 도파민 후킹 한 줄
    conflict:          # 핵심 갈등
    climax:            # 반전 (제품 등판)
    afterglow:         # 여운 (Soft Sell)
```

---

### STEP 2 — 4단계 팩션 스크립트 작성 & 프로젝트 폴더 초기화

**에이전트 실행**

`references/faction-strategy.md`와 `references/script-rules.md`를 참고하여:

1. **30초(1.5배속 기준) 4단계 팩션 스크립트** 작성 (약 350~400자, 문장 단위 줄바꿈)

| 단계 | 목표 시간 | 역할 | 핵심 전략 |
|---|---|---|---|
| **도파민 후킹** | 0~3초 | 뇌 정지 유발 | `[대중적 키워드]` + `[부정적 감정]` + `[궁금증 유발]` |
| **빌드업과 갈등** | 3~13초 | 서사 몰입 | 회사/개발자의 결핍·분노·집착 200% 과장 |
| **클라이맥스와 반전** | 13~23초 | 제품 극적 등판 | USP를 시각적·감각적 타격감 언어로 포장 |
| **여운과 바이럴** | 23~30초 | Soft Sell | 품절 대란·군중심리·어이없는 현상 전달 |

2. **훅 3종** — 분노형·광기형·집착형, 기본안 표시
3. 현재 시각 기준 폴더 생성 (`outputs/YYMMDD_HHMM/`) 및 `script.md`, `plan.md` 저장

`script.md` 작성 규칙:
- 문장 단위 줄 분리 (align_scenes.py가 1:1로 씬에 매핑)
- 숫자는 한글 발음으로 표기 (예: `300만` → `삼백만`)
- 구어체 반말 톤 — 친구에게 썰 풀어주는 느낌
- 직접적 CTA 금지 — Soft Sell만

---

### STEP 3 — TTS 음성 생성 (1.5배속)

**에이전트가 스크립트 실행**

> ⚠️ Qwen3-TTS 서버(`http://127.0.0.1:7860`)가 실행 중이어야 한다.

```bash
python3 .agents/skills/faction-shorts-studio/scripts/generate_tts.py outputs/{project}
```

결과물: `outputs/{project}/output_1.5x.wav`

실행 후 에이전트가 파일 생성 여부를 확인한다.
실패 시 → 서버 상태를 확인하고 사용자에게 알린다.

---

### STEP 4 — 자막 씬 데이터 생성 & 타임코드 확정

**에이전트가 스크립트 실행**

```bash
python3 .agents/skills/faction-shorts-studio/scripts/align_scenes.py outputs/{project}
```

결과물:
- `outputs/{project}/raw_stt.json`
- `outputs/{project}/scene_data.json`

실제 발화 음성의 각 씬별 시작/종료 타임코드를 분석하여 6개 씬의 정확한 지속 시간(초)을 확정한다.

---

### STEP 5 — 1x3 다중 에셋 시트 생성 (`asset_sheet_*.jpg`, 완벽한 9:16 비율) & 자동 분리

**에이전트 실행**

개별 컷을 하나씩 따로 생성하지 않고, 확정된 씬 타임코드와 서사에 맞춰 **16:9 가로 캔버스에 1행 3열(1x3) 배열**로 고화질 에셋 시트를 생성한다.

> 💡 **수학적 종횡비 일치 원리**: 
> 16:9 가로 캔버스에 1행 3열을 나열하면 각 패널의 종횡비는 가로 $16/3 = 5.33$, 세로 $9 \rightarrow 9 / 5.33 \approx \mathbf{1.69}$로, 쇼츠 규격인 9:16 ($\approx \mathbf{1.78}$)과 거의 완벽히 일치하여 크롭 시 좌우 잘림 없는 초고화질 에셋을 얻을 수 있다.

1. **시트 분할 생성 (1x3 기준)**:
   - 6씬 서사인 경우: 3컷씩 2장으로 나누어 생성
     - `asset_sheet_1.jpg`: Scene 1 (도파민 훅), Scene 2 (빌드업), Scene 3 (갈등)
     - `asset_sheet_2.jpg`: Scene 4 (클라이맥스/제품), Scene 5 (효능 반전), Scene 6 (여운/Soft Sell)
2. **빈 슬롯(Blank / Black Panel) 처리 룰**:
   - 총 씬 수가 4씬, 5씬 등 3의 배수가 아닌 경우, 마지막 시트의 남는 패널은 `"The 3rd panel must be left completely empty as a pure solid black background"`와 같이 프롬프트에 명시하여 검정 배경으로 둔다.
   - 크롭 스크립트(`crop_asset_sheet.py`)가 검정/단색 빈 패널을 자동으로 감지하여 스킵하고 필요한 에셋만 순차 저장한다.
3. **원천 레퍼런스 주입 & 제품 실물 일치**:
   - STEP 1에서 수집한 원천 레퍼런스 풀(`ref_cut1~N.png`)을 `ImagePaths` 인자에 주입하여 실제 제품 외형·디자인을 100% 동일하게 반영한다.
4. **인물/손 일관성 (Consistency) 유지**:
   - 인물이 등장하는 경우 동일 모델/캐릭터 앵커를 유지하고, 손 중심(Hands-Only) 클로즈업/1인칭 POV 연출 시 손 모양과 톤의 일관성을 고정한다.
5. **자동 분할 스크립트 실행**:
   ```bash
   python3 .agents/skills/faction-shorts-studio/scripts/crop_asset_sheet.py outputs/{project}
   ```
   - 개별 9:16 에셋들(`assets/scene1_9_16.jpg` ~ `scene6_9_16.jpg`)이 오차 없이 1080×1920 해상도로 자동 저장된다.
   - 가이드 문서(`asset_sheet.md`)를 작성하여 저장한다.

---

### STEP 6 — 영상 프롬프트 & 배포 킷 최종 확정

**에이전트 실행**

1. `scene_data.json`의 실제 발화 타임코드와 씬별 에셋 이미지 파일을 1:1로 매핑하여 `prompts.md`를 작성한다.
2. 유튜브 쇼츠, 인스타 릴스, 틱톡용 썸네일 카피와 본문 문구가 포함된 `publish_kit.md`를 작성한다.

---

## 최종 결과물 (`outputs/YYMMDD_HHMM/`)

| 파일 | 내용 |
|---|---|
| `plan.md` | STORY_TRUTH, 6씬 타임라인, 훅 3종 |
| `script.md` | 팩션 보이스오버 대본 |
| `output_1.5x.wav` | 1.5배속 음성 파일 |
| `raw_stt.json` | Whisper 원본 STT 데이터 |
| `scene_data.json` | 자막 타임코드 씬 데이터 |
| `asset_sheet.jpg` | 6-Cut 종합 에셋 시트 이미지 |
| `asset_sheet.md` | 실물 에셋 매핑 가이드 |
| `assets/` | 씬별 9:16 이미지 에셋 6장 및 원천 레퍼런스 컷들 |
| `prompts.md` | 씬별 이미지 + 영상 생성 프롬프트 (실제 타임코드 반영) |
| `publish_kit.md` | 썸네일 카피·제목·설명·SEO 태그·플랫폼 문구 |

---

## 이후 단계 (사용자 직접)

1. 영상 생성 도구(Kling, Runway, Luma 등)에 `prompts.md`의 프롬프트 + 에셋 이미지 입력
2. 생성된 클립을 편집기(CapCut, Premiere 등)에서 조립
3. `scene_data.json` 기반 자막 타임코드를 편집기에서 적용
