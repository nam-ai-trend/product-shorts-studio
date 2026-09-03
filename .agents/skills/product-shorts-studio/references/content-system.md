# 단일 생활용품 콘텐츠 시스템

## 결과 정의

최종 산출물은 한 가지 제품을 홍보하는 9:16 영상 한 편이다.
여러 제품 추천·순위·비교·미니하울은 만들지 않는다.
클립을 여러 개 생성하더라도 모두 같은 제품의 다른 구도이며, 최종 결과는 한 편으로 조립한다.

---

## 검증된 15초 6비트 구조

| 비트 | 역할 | 길이 | 제품 노출 | 내용 |
|---|---|---|---|---|
| 1 | **결과 선공개** | 3초 | 없음 | 완성된 결과물 클로즈업. 손이 살짝 건드려 질감 증명 |
| 2 | 대비 | 2초 | 없음 | 기존 방식의 나쁜 결과. 같은 앵글 하드컷 |
| 3 | 제품 공개 | 2초 | 정면 고정 | 손이 제품을 들어올려 정지. 미세 푸시인 |
| 4 | **핵심 시연** | 4초 | 사용 각도 | 한 가지 동작. 결과물이 실제로 생성되는 순간 |
| 5 | 재훅 | 2초 | 프레임 밖 | 결과물을 손으로 집어 증거 클로즈업 |
| 6 | 루프 엔딩 + CTA | 2초 | 정면 packshot | 비트 1과 동일 앵글. 제품을 결과물 옆에 내려놓음 |

합계 15초. 정수 초 배분 필수 (3+2+2+4+2+2=15).
**첫 컷은 완성 결과물부터.** 제품은 최소 3초 뒤에 등장한다.

---

## 세 가지 크리에이티브 각도

모두 같은 제품으로 작성한다. 기본안은 시각적 증명이 가장 빠른 각도다.

1. **문제 해결형**: 불편 → 제품 공개 → 한 동작 → 해결 결과
2. **비포·애프터형**: 같은 장소·구도에서 전 → 사용 → 후
3. **손 중심 ASMR형**: 포장·재질·딸깍임·닦는 소리 → 실제 사용 → 제품 홀드

---

## 5-Cut 에셋 번들

### 왜 에셋 번들이 필요한가

Image-to-Video 생성에서 가장 흔한 실패는 **컷마다 제품 색·형태·로고 위치가 달라지는 일관성 붕괴**다.
에셋 번들은 각 비트에 "이 컷에서는 이 각도 이미지로 생성한다"를 미리 고정해 이 문제를 차단한다.

### 6비트 1:1 직관적 에셋 컷 정의 (비트 번호 = 컷 번호)

사용자 혼선을 방지하기 위해 **비트 번호와 에셋 컷 번호(Cut 1~6)를 1:1로 완전히 일치**시킨다.

| # | 컷 명칭 | 구도 및 내용 | 6비트 1:1 연결 | 비주얼 역할 |
|---|---|---|---|---|
| **Cut 1** | **Result / Hook Shot** | 완성된 결과물의 극단적 클로즈업/텍스처 컷 | **비트 1 (오프닝 훅)** | 첫 프레임 시선 강탈 (제품 노출 X) |
| **Cut 2** | **Before / Bad Problem** | 기존 방식의 불편하거나 번들거리는 문제 컷 | **비트 2 (대비/비포)** | 문제점 대비 및 공감 유도 |
| **Cut 3** | **Hero / Product Shot** | 깨끗한 배경의 제품 본품 정면 대표 누끼 컷 | **비트 3 (제품 공개)** | 제품 정체성 및 형태 고정 |
| **Cut 4** | **Action / Detail Shot** | 제형 롤링, 절삭, 작동 등 핵심 시연 컷 | **비트 4 (핵심 시연)** | 1초 만에 증명되는 핵심 쾌감 |
| **Cut 5** | **Re-Hook / Proof Shot** | 해결된 결과물의 재확인 및 디테일 컷 | **비트 5 (재훅/증명)** | 구매 욕구 확신 부여 |
| **Cut 6** | **Loop / Anchor Shot** | 제품 본품을 손에 쥐거나 옆에 둔 앵커 컷 | **비트 6 (루프 엔딩+CTA)** | 첫 컷과 이어지는 루프 앵글 |

> Cut 6(또는 Cut 3)은 영상 전체의 **손(피부톤/손톱/소매) 및 착용 인물(턱선/헤어/실루엣)의 일관성을 유지하는 앵커 이미지** 역할을 겸한다.

### 에셋 품질 게이트

아래 조건을 모두 만족해야 일반 생성 모드로 진행한다.

- 서로 다른 유효 각도 최소 3장 (Cut 1, Cut 2, Cut 3 또는 Cut 4 중 3장 이상)
- 긴 변 가급적 800px 이상
- 제품명·색·옵션이 모든 이미지에서 동일
- 사용할 기능과 접촉부가 최소 한 장에 명확히 보임
- 라벨·버튼·이음새·재질·비율을 구분할 수 있음

통과하지 못하면 → `LIMITED_MOTION` 모드 또는 필요한 각도만 사용자에게 요청.

### 9:16 패딩 규칙 (필수)

일부 Image-to-Video 모델은 출력 비율이 입력 이미지를 따라간다.
정사각 이미지를 넣으면 9:16 쇼츠 규격이 나오지 않는다.

**모든 에셋 이미지를 9:16으로 패딩한 뒤 사용한다.**

- 흰(또는 크림) 배경으로 9:16 캔버스를 만들고 원본 이미지를 중앙 배치
- 피사체를 세로 **55–65%** 지점에 놓아 **상단 약 25%를 자막 안전영역으로 비운다**
- 판매처 스크린샷이면 공유 아이콘·링크 텍스트 같은 UI 잔여물을 잘라낸다

---

## 에셋 사이즈 × 손 동작 매칭 규칙

이미지 기반 영상 생성에서 **에셋 이미지 속 제품의 화면 점유 크기**에 따라 손 동작 범위와 속도를 조절해야 자연스러운 결과가 나온다.

### 에셋 사이즈 기준

| 크기 분류 | 제품이 화면을 차지하는 비율 | 예시 |
|---|---|---|
| **소형** (Small) | 10–30% | 작은 부엌 소도구, 캡슐형 제품, 소형 기기 |
| **중형** (Medium) | 30–60% | 일반 주방용품, 청소 도구, 수납 박스 |
| **대형** (Large) | 60–80% | 패드형·시트형 제품, 납작 도마, 넓은 수납망 |

### 크기별 손 동작 프롬프트 규칙

**소형 에셋 (Small)**
- 손이 화면에서 차지하는 비중이 커야 제품과 자연스럽게 매칭됨
- 손을 제품 쪽으로 **가까이 당겨** 잡거나 핀치(pinch) 그립 사용
- 손목 이하만 보이는 타이트 클로즈업 구도
- 프롬프트 키워드: `close-up hand grip`, `fingertip pinch`, `wrist-level tight frame`

**중형 에셋 (Medium)**
- 손과 제품이 화면을 함께 분할하는 자연스러운 비율
- 손바닥 전체 또는 손 + 전완 하단까지 보이는 미디엄 클로즈업
- 제품을 **들어올리기·눌러쓰기·밀기** 동작이 모두 가능
- 프롬프트 키워드: `hand holds product at center frame`, `natural palm grip`, `medium close-up`

**대형 에셋 (Large)**
- 제품이 화면 대부분을 차지하므로 손은 프레임 **한쪽 가장자리에서 진입**해야 자연스러움
- 한 손 또는 양손이 제품 가장자리를 잡는 구도
- 큰 제품 위에 손을 올려 쓸거나 두드리는 동작
- 프롬프트 키워드: `hand enters from edge`, `flat-lay overhead touch`, `edge grip on large surface`

### 손 동작 일반 원칙

- 한 비트에서 손동작은 **하나만** 지정한다. 복합 동작은 비트를 나눈다.
- 손가락은 5개가 항상 보여야 한다. 가려지거나 잘리면 해당 컷은 불합격.
- 손과 제품의 **물리적 접촉이 명확히 보이는 프레임**이 최소 1개 이상 있어야 한다.
- 제품을 회전시켜 보이지 않던 면을 새로 만들게 하지 않는다. 참조 이미지가 있는 면만 노출.

---

## 구도 선택 규칙

- **탑다운**: 수납·정리·조리대·포장 개봉처럼 평면상의 변화가 핵심일 때
- **45도 사선**: 손과 제품이 실제 공간에서 만나는 사용 장면
- **정면 클로즈업**: 제품 형태·버튼·접힘·부착·최종 결과 홀드

화면 중앙 또는 중앙 아래에 제품을 크게 두고 **상단 25%는 자막 안전영역**으로 비운다.
카메라는 대부분 고정. 작은 자연스러운 핸드헬드만 허용.

---

## 제품군별 특화 연출

세부 카테고리별 훅, 시연 기법, 사운드 및 인물 연출 룰은 [카테고리별 전략 플레이북](category-strategies.md)을 준수한다.

- **푸드/식품/음료**: 극단적 클로즈업 식감(바삭함, 김, 끓음, 쏟아짐) 선공개 → 불어나거나 조리되는 마법 같은 1초 시연 → 씹는/끓는 ASMR.
- **뷰티/스킨케어**: 세안/정돈 직후 매끈한 수분결 선공개 → 닿자마자 유화/흡수되는 텍스처 롤링 시연 → 섬세한 손동작과 자연광.
- **패션/잡화/모자**: 두상/실루엣에 착 감긴 착용 핏감 선공개 → 구김 복원/방수/수납 시연 → 챙 살짝 잡는 자연스러운 제스처.
- **키친/주방**: 균일하고 얇게 썰린 대량의 결과물 선공개 → 힘들이지 않고 쓱쓱 나가는 쾌감 절삭 시연 → 사각거리는 절삭음.
- **생활용품/청소**: 새것처럼 하얘진 줄눈/물때 제로 선공개 → 지나간 자리만 하얗게 뚫리는 찌든 때 제거 시연 → 비포/애프터 카타르시스.
- **가전/디지털**: 강력한 분무/충전/흡입 반응 선공개 → 버튼 누르자마자 0.1초 즉각 작동하는 기계적 쾌감 시연 → 마그네틱/모터 사운드.
- **여행/아웃도어**: 압축 완료되어 넉넉해진 캐리어 내부 선공개 → 지퍼 당겨 부피 반토막 내는 폴딩 시연 → 방수/초경량 증명.
- **문구/오피스**: 칼각 정돈된 감성 데스크 셋업 선공개 → 부드러운 필기감/찰칵 달라붙는 마그네틱 조작 시연 → 사각거리는 필기음.

---

## 영상 생성 프롬프트 템플릿

```text
Create a [DURATION]-second vertical 9:16 promotional shot for one Korean household product.

PRODUCT_TRUTH
- Product: [PRODUCT_NAME]
- Locked variant: [COLOR, SIZE, OPTION]
- Exact visible appearance: [MATERIAL, SHAPE, PROPORTIONS, LABEL, BUTTONS, JOINTS]
- Verified use and result: [ONE VERIFIED ACTION AND BELIEVABLE RESULT]

ASSET_BINDING
- Cut used for this shot: Cut [번호] — [컷 설명]
- Primary identity reference: [HERO/SIDE/DETAIL IMAGE]
- Do not reveal or invent any surface, control, or internal part not shown in references.

HAND_SCALE_RULE
- Asset size class: [SMALL / MEDIUM / LARGE]
- [소형: close-up hand grip, fingertip pinch, wrist-level tight frame]
  [중형: hand holds product at center frame, natural palm grip, medium close-up]
  [대형: hand enters from edge, flat-lay overhead touch, edge grip on large surface]

ACTOR_AND_HAND_ANCHOR (일관성 불변 블록)
- Hands/Body: Clean fair natural skin tone, short manicured natural nails, no rings, no accessories.
- Clothing/Sleeve: Neutral off-white or soft gray sleeve visible at wrist/shoulder.
- Face Rule: Hands-only close-up, OR tight partial crop (jawline, chin, cheek, or head silhouette only). NO full front facial features to prevent AI face morphing.
- Anatomy: Exactly 5 fingers, realistic skin folds, believable physical contact.

REFERENCE_DNA
- Hands-only or partial-body authentic UGC aesthetic.
- Bright soft daylight, off-white and light-gray interior, restrained neutral palette.
- Composition: [TOP-DOWN / 45-DEGREE / FRONT TIGHT CLOSE-UP].
- Mostly locked camera, subtle natural movement, hard-cut-friendly ending.

SHOT_BEATS
- [TIME] [ONE PRECISE ACTION].
- [TIME] Hold the believable result clearly.

CONTINUITY
- Preserve exact product color, shape, thickness, scale, label, button and joint positions.
- Keep the exact same hand/actor anchor, location, lighting and product variant throughout.
- No morphing, extra fingers, impossible motion, floating objects or background changes.

CLEAN_PLATE
- No generated text, subtitles, prices, watermarks or graphic typography.
- Keep the upper 25% of frame (caption safe area) uncluttered.

AUDIO_PLAN
- [NATIVE PRODUCT SOUND / QUIET ROOM TONE / SEPARATE KOREAN VOICEOVER via external TTS].
```

## `LIMITED_MOTION` 템플릿

이미지가 부족할 때는 제품 자체를 변형하거나 크게 회전시키지 않는다.

```text
Keep the product rigid and visually identical to the supplied hero image at all times.
Use only a subtle camera push-in, a small hand approach, and a simple touch on a fully visible surface.
Do not rotate, open, unfold, disassemble, bend, or reveal the back or interior.
Do not infer missing geometry. End on the same product-facing angle as the reference image.
```

---

## 자막·보이스오버

- **보이스오버는 외부 TTS 스킬로 위임한다.** 에이전트가 직접 생성하지 않는다.
- `stt-scene-align`이 만든 `scene_data.json`의 씬별 타임코드로 자막 큐 표를 작성한다.
- 자막 위치: 화면 세로 25–35% 구간. 상단 12%와 하단 20%는 플랫폼 UI가 덮는다.
- 흰 글씨 + 얇은 검정 외곽선. 한 화면 최대 두 줄.
- 첫 자막은 0.2초에 띄운다. 소리 끄고 보는 시청자가 1.5초 안에 판단한다.
- 마지막 자막에만 CTA. 영상 안에 URL을 넣지 않는다.

---

## 단일 제품 발행 킷

1. 썸네일 카피 10–14자
2. 문제·결과 중심 제목
3. 확인 가능한 제품 장점과 링크 위치가 포함된 설명
4. SEO 태그 10개
5. 틱톡 본문 문구
6. 인스타그램 릴스 본문 문구
7. 유튜브 쇼츠 제목 + 설명 + 태그

모든 문구는 같은 제품과 같은 핵심 가치 제안을 유지한다.
