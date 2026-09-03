# 팩션(Faction) 쇼핑쇼츠 이미지 & 영상 프롬프트 전략 가이드

이 문서는 팩션 썰 쇼핑쇼츠의 **시네마틱 실사 이미지(Text-to-Image)**와 **Image-to-Video(I2V) 모션 프롬프트**를 작성할 때 기준이 되는 마스터 가이드다.

---

## 🧭 1단계: 4-Axis 마스터 에셋 시트 규격 (Ground Truth)

AI가 제품의 3차원 형태를 완벽하게 학습하고 시점/앞뒤/작동면의 왜곡(Hallucination)을 100% 방지하기 위해, 모든 상품은 **4대 핵심 축(Axis)**으로 원천 이미지를 구성한다.

```
┌────────────────────────────────────────────────────────────────────────┐
│                   UNIVERSAL 4-AXIS MASTER ASSET SHEET                  │
├──────────────────┬──────────────────┬──────────────────┬───────────────┤
│ [1. 외관/기본형] │ [2. 개방/작동형] │ [3. 구조/디테일] │ [4. 실사용/손]│
│ Closed / Default │ Open / Functional│ Profile / Detail │ In-Hand Action│
│ (제품 기본 정체성)│ (핵심 기능/속살) │ (스펙/후면/단면) │ (크기감/결과물)│
└──────────────────┴──────────────────┴──────────────────┴───────────────┘
```

### 1-1. 카테고리별 4대 축 표준 매핑

| 카테고리 | 1. 외관/기본형 (Default) | 2. 개방/작동형 (Functional) | 3. 구조/디테일 (Structure) | 4. 실사용/손 (In-Hand Action) |
|---|---|---|---|---|
| **📱 전자기기/가전** | **닫힌 본체 정면** (커버 화면, 슬림 외형) | **열린 작동면** (내부 대화면, 작동 패널) | **후면/측면 두께** (카메라 섬, 힌지, 단자) | **손에 쥔 실사용** (1인칭 POV 화면 조작) |
| **🧴 뷰티/스킨케어** | **뚜껑 닫힌 본품** (라벨 정면, 패키지) | **뚜껑 열린 토출부** (노즐, 펌프, 립스틱 심) | **제형 텍스처** (크림 질감, 미세 거품) | **손등/얼굴 롤링 샷** (바르는 순간의 촉촉함) |
| **🍕 식품/디저트** | **포장 패키지/원물** (라벨 정면, 신선 원물) | **개봉/조리된 완성형** (플레이팅된 요리) | **초근접 단면 컷** (늘어나는 치즈, 바삭한 층) | **숟가락/포크 샷** (한 입 떠올린 김 모락모락) |
| **🍳 주방/생활용품** | **제품 전체 정면 샷** (뚜껑 닫힌 외관) | **입구/내부 개방 샷** (내부 스테인리스, 칼날) | **손잡이/단열 두께 컷** (마감 디테일) | **손으로 작동하는 샷** (물 따르기, 칼질) |

---

## 🎨 2단계: 이미지 프롬프트 작성 규칙 (T2I)

### 2-1. 씬별 1:1 타깃 레퍼런스 바인딩 (No Confusion)
- 씬의 연출 목적에 맞춰 4대 축 에셋 중 **단 1~2개만 명확히 지정하여 `ImagePaths`로 바인딩**한다.
  - 외관/휴대성 씬 ➡️ `ref_1_default` 또는 `ref_3_detail`
  - 기능/대화면/제형 씬 ➡️ `ref_2_active` 또는 `ref_4_action`

### 2-2. 인물 노출 원칙 (Face vs Hands-Only)
- **얼굴 노출 필수**: 뷰티/의류/액세서리 등 신체 착용 및 피부 표현이 핵심인 경우에만 인물 얼굴/표정을 노출.
- **손 중심(Hands-Only) 기본**: 디지털/가전, 주방, 생활용품, 식품 등은 **인물 얼굴을 완전히 배제하고 손(Hands-only close-up, wrist-level, 1인칭 POV)** 위주로 연출하여 AI 얼굴 변형(morphing)을 차단.

### 2-3. 시점(POV) 및 앞뒤 방향성 앵커링
- **1인칭 POV (기능 증명)**: 카메라가 제품의 전면 작동면/디스플레이/제형을 정면으로 마주 봄. (`Camera is strictly viewing the front functional display/nozzle.`)
- **3인칭 샷 (사용자 시선)**: 인물이 제품을 바라보면 카메라는 제품의 반대편(후면/외관/로고)을 마주 봄. (`Camera is strictly viewing the rear backplate with camera island/brand logo.`)

---

## 🎬 3단계: 영상 생성 프롬프트 전략 (Image-to-Video)

I2V 모델(Kling, Runway, Luma 등)에서 기준 이미지의 왜곡 없이 완벽한 연속성을 유지하기 위한 철칙이다.

### 3-1. 기준 이미지 100% 구도/시점 보존 (Orientation Lock)
- 입력된 기준 이미지의 시점(1인칭 POV, 3인칭 후면, 측면 등)과 제품 앞뒤 방향성을 절대 바꾸지 않는다.
- 360도 회전, 급격한 카메라 앵글 전환, 뜬금없는 인물/배경 점프 지시를 일체 금지한다.

### 3-2. 미세 타깃 포인트 모션 (Targeted Micro Motion)
- 전체를 다 움직이지 않고, 기준 이미지에 이미 존재하는 핵심 요소 1~2개의 자연스러운 움직임에만 집중한다.
  - **빛 반사 (Lighting Sweep)**: `A smooth light sweep glides slowly across the metallic edge, product remains steady.`
  - **작동/발광 반응 (Display/Fluid Glow)**: `The vibrant screen subtly pulses with soft glowing light, hands maintain stable POV framing.`
  - **촉각적 미세 동작 (Tactile Action)**: `A thumb gently swipes across the smooth surface, locked camera focus.`
  - **환경 이펙트 (Ambient Atmosphere)**: `Delicate steam/sparks rise softly, camera performs a subtle 3% slow push-in.`

### 3-3. I2V 프롬프트 표준 템플릿
```text
Maintain exact [framing/POV/orientation] of the [product/hands] from the reference image.
[핵심 1~2개 포인트 모션 지시].
[안정적인 카메라 워킹 (3% slow push-in or subtle locked focus)].
No rotation, no angle change, photorealistic cinematic quality.
```
