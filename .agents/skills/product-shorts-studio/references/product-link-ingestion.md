# 상품 링크·이미지 수집 & 에셋 번들 구성 규칙

## 목적

사용자가 쿠팡·스마트스토어·Amazon 상품 링크 또는 직접 제공 이미지를 주면
제품 정보와 이미지를 수집하고, **5-Cut 에셋 번들**을 구성한다.
페이지 접근 제한을 우회하거나 보이지 않는 제품 구조를 추측하지 않는다.

---

## 인풋 경로 선택

### 경로 A — URL 자동 수집

1. URL의 최종 도메인과 리디렉션 목적지를 확인한다.
   쿠팡(`coupang.com`), 스마트스토어(`smartstore.naver.com`), Amazon 계열 외 다른 도메인이면 사용자에게 알린다.
2. 상품 식별자와 선택 옵션을 잠근다.
   - 쿠팡: `productId`, `vendorItemId`, 선택 옵션
   - 스마트스토어: `productId`, 옵션 조합
   - Amazon: ASIN, 국가 스토어, 색·크기·스타일
3. 브라우저 도구로 상품 페이지를 열고 공식 갤러리 원본 이미지 URL을 찾는다.
4. 선택 옵션과 일치하는 공식 갤러리 이미지만 수집한다.
   리뷰 사진·다른 판매자 이미지·다른 색상·다른 용량은 섞지 않는다.
5. URL·파일 해시·육안 기준으로 중복을 제거한다.
   작은 썸네일·깨진 이미지·긴 설명 인포그래픽·옵션 불명확 이미지를 제외한다.

CAPTCHA·로그인 장벽·지역 제한·robots 정책이 있으면 우회하지 않는다.
접근이 막히면 즉시 경로 B로 전환하고 사용자에게 알린다.

### 경로 B — 사용자 직접 제공

사용자가 이미지와 내용을 직접 주는 경우다.

- 이미지: 대표·측면·상세·사용 중 컷 등 보유 이미지 전체를 받는다
- 내용: 제품명·옵션·색상·핵심 기능·확인된 스펙을 텍스트로 받는다
- 확인되지 않은 스펙(뒷면·내부 구조)은 `PRODUCT_TRUTH`에 포함하지 않는다

---

## 수집할 이미지 우선순위

가능하면 5종의 에셋 역할을 채울 수 있는 이미지를 최대한 확보한다.

| 우선순위 | 역할 | 에셋 컷 매핑 |
|---|---|---|
| 1 | 정면 또는 대표 hero | Cut 1 (Hero) |
| 2 | 손으로 쥔 사용 상태 | Cut 2 (In-Hand) |
| 3 | 핵심 작동 부위 또는 측면 상세 | Cut 3 (Action/Detail) |
| 4 | 완성된 결과물 단독 | Cut 4 (Result) |
| 5 | 기존 방식의 불편한 결과 (대비용) | Cut 5 (Bad Result) |

Cut 5는 없어도 된다. Cut 1·3·4 중 최소 3종이 있어야 일반 생성 모드로 진행한다.

---

## 품질 게이트

다음 조건을 모두 만족해야 일반 생성 모드로 진행한다.

- 서로 다른 유효 각도 최소 3장
- 대표 이미지의 긴 변 가급적 800px 이상
- 제품명·모델·색·크기·옵션이 모든 이미지에서 일치
- 사용할 기능과 접촉부가 최소 한 이미지에 명확히 보임
- 라벨·버튼·이음새·재질·비율을 구분할 수 있음

통과하지 못하면 자동으로 다음 중 하나를 선택한다.

- `LIMITED_MOTION` 모드: 제품을 정면으로 유지한 채 카메라 이동과 단순 접촉만 허용
- 필요한 각도를 구체적으로 요청 (예: "오른쪽 측면과 작동 버튼 클로즈업 사진")
- 링크가 잘못됐거나 옵션을 특정할 수 없으면 생성 중단

---

## AI 레퍼런스 기반 5-Cut 에셋 생성 (에이전트 필수 실행)

수집된 실제 상품 이미지는 **AI 이미지 생성기(`generate_image`)의 레퍼런스(`ImagePaths`)로 전달**되어, 제품의 외형·로고·색상을 100% 보존한 상태로 컷별 고화질 9:16 실사 씬으로 재탄생한다.

1. **Cut 1 (Hero Shot):** 실제 제품 이미지를 레퍼런스로 입력하여 광고 스튜디오급 고화질 누끼/정면 샷 생성
2. **Cut 2 (In-Hand / Wearing Anchor):** 실제 제품을 깨끗한 손/착용 모델이 쥐고 있는 인물/손 앵커 샷 생성
3. **Cut 3 (Action / Detail):** 제품의 제형(거품, 텍스처, 블레이드 날 등)을 타이트하게 시연하는 매크로 샷 생성
4. **Cut 4 (Result Shot):** 제품 사용 후 완성된 극상의 결과물(맑은 피부결, 썰린 재료 등) 샷 생성
5. **Cut 5 (Bad / Before):** 사용 전 문제점(번들거림, 지저분함 등)을 보여주는 비포 샷 생성

생성된 5개 컷은 `outputs/YYMMDD_HHMM/assets/`에 저장되며, 2000×1000 고화질 종합 에셋 시트 이미지(`asset_sheet.jpg`)로 자동 합성된다.

```python
# 에이전트 내부 자동 패딩 예시 (Python Pillow)
from PIL import Image

def pad_to_9_16(src, dst):
    img = Image.open(src).convert("RGB")
    target_w, target_h = 1080, 1920
    scale = min((target_w * 0.85) / img.width, (target_h * 0.55) / img.height)
    resized = img.resize((int(img.width * scale), int(img.height * scale)), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (target_w, target_h), (248, 249, 250))
    paste_x = (target_w - resized.width) // 2
    paste_y = int(target_h * 0.58 - resized.height // 2)
    canvas.paste(resized, (paste_x, paste_y))
    canvas.save(dst, "JPEG", quality=95)
```

---

## 변형 잠금

링크를 열었을 때 기본 옵션이 바뀔 수 있으므로 이미지 URL만으로 옵션을 추정하지 않는다.
페이지 제목·식별자·선택 옵션·색·크기·판매자·수집 시각을 함께 기록한다.
가격은 수집 시각과 통화를 표시하고 영상 제작 직전에 다시 확인한다.

---

## 매니페스트 (`product-source-manifest.json`)

사용자 작업공간 `outputs/<프로젝트명>/` 폴더에 저장한다.
쿠키·토큰·서명된 임시 URL·개인 정보는 저장하지 않는다.

```json
{
  "source_url": "canonical product page URL",
  "marketplace": "coupang | smartstore | amazon | direct",
  "product_id": "productId/ASIN",
  "title": "page title",
  "variant": {"color": "", "size": "", "option": ""},
  "fetched_at": "ISO-8601 timestamp",
  "verified_claims": [],
  "asset_bundle": [
    {"cut": 1, "role": "hero",       "file": "cut1_hero_padded.jpg",    "source": "gallery URL or direct"},
    {"cut": 2, "role": "in_hand",    "file": "cut2_in_hand_padded.jpg", "source": "gallery URL or direct"},
    {"cut": 3, "role": "action",     "file": "cut3_action_padded.jpg",  "source": "gallery URL or direct"},
    {"cut": 4, "role": "result",     "file": "cut4_result_padded.jpg",  "source": "gallery URL or direct"},
    {"cut": 5, "role": "bad_result", "file": "cut5_bad_padded.jpg",     "source": "gallery URL or direct"}
  ]
}
```

---

## 생성 전 최종 확인

- 한 제품의 한 옵션만 포함됐는가?
- 모든 에셋 이미지가 9:16으로 패딩됐는가?
- 각 비트(6비트)에 연결할 에셋 컷 번호가 지정됐는가?
- 에셋 이미지 속 제품의 화면 점유 크기(소형/중형/대형)를 확인해 손 동작 프롬프트를 맞췄는가?
- 상품 페이지에서 확인되지 않은 기능이나 성능을 프롬프트에 넣지 않았는가?
- 뒷면·내부·두께·버튼 위치를 추측하도록 요구하지 않았는가?
