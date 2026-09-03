---
name: faction-shorts-studio
description: 제품 링크 또는 사용자 제공 이미지를 바탕으로 제품/회사 썰을 리서치·머지하여, 4단계 팩션(Faction) 서사 구조의 30초(1.5배속 기준) 바이럴 썰 쇼핑쇼츠를 기획·제작한다. 4-Axis 마스터 에셋 시트 기반으로 왜곡 없는 실사 AI 에셋과 I2V 영상 프롬프트를 조립한다.
---

# 팩션(Faction) 썰 쇼핑쇼츠 파이프라인

## 목적

제품 링크(URL) 또는 사용자가 직접 제공한 제품 이미지를 받아, **제품 썰과 회사 썰을 웹 리서치**하고, 두 썰을 머지한 **팩션(fact+fiction) 스토리**로 30초 바이럴 쇼츠를 기획한다.

대놓고 "이거 사세요" 하면 스와이프 당하기 때문에, 철저하게 **'재밌는 이야기'로 위장**해서 끝까지 보게 만들고 스스로 제품을 검색하게 만드는 것이 핵심이다.

항상 다음 원칙을 지킨다.

- 한 영상에는 하나의 제품 + 하나의 스토리만 담는다.
- 직접적인 구매 유도(CTA)를 절대 하지 않는다. **Soft Sell** 전략만 사용한다.
- 제품 스펙을 나열하지 않고, **시각적·감각적 타격감**이 느껴지는 언어로 포장한다.
- 서사의 200% 과장은 허용하되, 완전한 허위 사실 날조는 하지 않는다.
- 파이프라인 공정: **대본 작성 → TTS 음성(1.5x) → STT 자막 데이터 및 타임코드 확정 → 4-Axis 마스터 에셋 시트 & 씬별 실사 AI 에셋 생성 → I2V 영상 프롬프트 최종 확정**
- TTS는 **1.5배속** 전용 스크립트(`generate_tts.py`)로 위임한다.
- STT + 씬 정렬은 전용 래퍼(`align_scenes.py`)로 위임한다.
- 영상 생성 도구(Kling, Runway, Luma 등)는 사용자 선택. 특정 도구에 종속되지 않는다.
- **적용 대상 (전 카테고리):** 식품/음료, 뷰티, 패션, 주방, 생활, 가전, 여행, 문구 등 모든 상품.

---

## 기본 경로 — 먼저 읽는다

새 제품이 들어오면 다음 세 문서를 **가장 먼저 읽고 기본값으로 삼는다.**

1. [4단계 팩션 서사 전략](references/faction-strategy.md): 도파민 후킹, 빌드업, 클라이맥스, 여운의 구체적 공식
2. [이미지/영상 프롬프트 전략](references/visual-prompt-guide.md): 4-Axis 마스터 에셋 시트, Hands-Only 룰, 시점(POV) 일관성, I2V 모션 가이드
3. [대본 작성 규칙](references/script-rules.md): 30초 1.5배속 전용 대본 포맷팅 룰

---

## 시작 조건

- **방식 A (URL 입력)**: 상품 링크 (쿠팡·스마트스토어·Amazon URL) + 제품명 + 회사명
- **방식 B (직접 이미지 제공)**: 제품 실물 이미지 파일들 (1~4장) + 제품명 + 회사명
- 원하는 길이: 기본값 30초 (1.5배속 기준)

---

## 6단계 파이프라인

### Phase 1 — 제품·회사 리서치, 4-Axis 원천 레퍼런스 확보 & STORY_TRUTH 작성

1. **4-Axis 원천 레퍼런스 풀 (Universal 4-Axis Ground Truth) 확보**:
   - 상품의 3차원 형태를 정의하는 4대 축 이미지를 수집/저장한다:
     - `ref_1_default.png`: 외관/기본 닫힘 뷰 (제품 정체성)
     - `ref_2_active.png`: 개방/작동면 뷰 (핵심 기능/디스플레이/내용물)
     - `ref_3_detail.png`: 후면/측면 두께/단면/제형 뷰 (디테일 구조)
     - `ref_4_action.png`: 손에 쥔 실사용 샷 (크기감/1인칭 조작/결과)
   - URL 제공 시 브라우저 서브에이전트로 **최대 2~3분 이내에 신속히 캡처**, 직접 업로드 시 사용자 이미지로 등록.
2. **제품 썰 리서치** (`search_web` + 상품 페이지 크롤링)
3. **회사 썰 리서치** (`search_web`)
4. **두 썰 머지** → `STORY_TRUTH` 작성

---

### Phase 2 — 4단계 팩션 스크립트 작성 & 프로젝트 폴더 초기화

1. **4단계 팩션 스크립트** 작성 (30초 / 1.5배속 기준, 약 350~400자, 문장 단위 줄바꿈)
2. **훅 3종** 제안 — 분노형·광기형·집착형, 기본안 표시
3. `outputs/YYMMDD_HHMM/` 생성 및 `script.md`, `plan.md` 저장

---

### Phase 3 — TTS 음성 생성 (1.5배속)

```bash
python3 .agents/skills/faction-shorts-studio/scripts/generate_tts.py outputs/{project}
```
결과물: `outputs/{project}/output_1.5x.wav`

---

### Phase 4 — 자막 씬 데이터 생성 & 타임코드 확정

```bash
python3 .agents/skills/faction-shorts-studio/scripts/align_scenes.py outputs/{project}
```
결과물: `outputs/{project}/raw_stt.json`, `outputs/{project}/scene_data.json`

---

### Phase 5 — 4-Axis 기반 순수 실사 종합 에셋 시트 생성 (`asset_sheet.jpg`, 9:16 멀티 패널 그리드) & 자동 분리

1. **한 번에 순수 실사 종합 에셋 시트 생성 (9:16 멀티 패널 그리드)**: 
   - 개별 컷을 하나씩 따로 생성하지 않고, 영상 길이(15초, 30초, 60초 등)와 기획된 씬 수(4~8컷)에 맞춰 4-Axis 원천 에셋을 `ImagePaths` 레퍼런스로 주입한다.
   - **9:16 패널 격자(Grid) 배치 원칙**:
     - **4~6컷 (기본 표준)**: `2x3 Multi-row Grid (2 rows of 3 vertical 9:16 portrait panels separated by thin clean white grid lines)`
     - **7~8컷 (확장)**: `2x4 Multi-row Grid (2 rows of 4 vertical 9:16 portrait panels)`
     - **3컷 (요약)**: `1x3 Single Row (3 vertical 9:16 panels side-by-side)`
   - **배치 중심 묘사 & 실제 제품 라벨 인쇄 텍스트 보존 룰**:
     - 'No text' 금지어 대신, **순수 상업 실사 사진(Pure commercial photographic contact sheet)**과 격자 배치만 명확히 묘사하여 화면에 불필요한 자막/UI가 생기지 않도록 방지한다.
     - **실제 제품 표면의 인쇄 텍스트(브랜드 로고, 제품명 영문/한글)는 레퍼런스 이미지와 100% 동일하게 본체 표면에 선명하게 인쇄되어 있도록 프롬프트에 명시**한다.
     - *프롬프트 표준 템플릿:*
       `"A professional commercial photographic contact sheet arranged in a balanced 2x3 grid. Each panel is a high-resolution vertical 9:16 portrait photo with thin clean white borders. The product packaging accurately reflects the reference image, including the exact color, shape, and the authentic printed typography/label on the item."`
   - 이후 자동 크롭 스크립트(`crop_asset_sheet.py`)를 실행하여 각 패널을 9:16 개별 에셋(`assets/cut1_9_16.jpg`...)으로 자동 슬라이스 및 스마트 보정한다:
   ```bash
   python3 .agents/skills/faction-shorts-studio/scripts/crop_asset_sheet.py outputs/{project}
   ```
2. **제품 실물 일치 & 일관성 유지**:
   - 수집된 원천 레퍼런스 풀과 100% 일치하도록 제품 형태/로고/컬러를 고정.
   - 인물/손 씬 연출 시 동일 인물 앵커 및 손 모양·톤 일관성 고정.
3. **종합 에셋 시트 및 가이드 문서 저장**:
   - 완성된 16:9 스토리보드 콘택트 시트(`asset_sheet.jpg`)와 가이드(`asset_sheet.md`)를 `outputs/{project}/`에 저장한다.

---

### Phase 6 — I2V 영상 프롬프트 & 배포 킷 최종 확정

1. **영상 프롬프트 작성 철칙 적용 (`prompts.md`)**:
   - 기준 이미지 구도/시점 100% 고정 (`Orientation Lock`).
   - 임의의 360도 회전이나 앵글 전환 금지.
   - 표면 빛 반사, 화면 발광, 손끝 스와이프 등 기준 이미지에 존재하는 핵심 요소의 미세 모션만 지시.
2. 유튜브 쇼츠, 인스타 릴스, 틱톡용 배포 킷(`publish_kit.md`) 작성.

---

## 최종 인도물

1. `plan.md` — STORY_TRUTH, 6씬 타임라인, 훅 3종
2. `script.md` — 팩션 보이스오버 대본
3. `output_1.5x.wav` — 1.5배속 음성 파일
4. `raw_stt.json` — Whisper 원본 STT 데이터
5. `scene_data.json` — 자막 타임코드 씬 데이터
6. `asset_sheet.jpg` — 6-Cut 종합 에셋 시트 이미지
7. `asset_sheet.md` — 에셋 씬 매핑 가이드
8. `assets/` — 씬별 9:16 이미지 에셋 6장 및 4-Axis 원천 레퍼런스 컷들
9. `prompts.md` — 씬별 T2I/I2V 영상 생성 프롬프트 (타임코드 & Orientation Lock 반영)
10. `publish_kit.md` — 썸네일 카피, 제목, 설명, SEO 태그, 플랫폼별 문구
