# 통신사 고객 이탈(Churn) EDA 요약 (모델링 제외)

## 범위
- 제공된 노트북 산출물 기반 EDA 요약이며, **모델링(학습/검증/성능평가)은 제외** :contentReference[oaicite:0]{index=0}

## 데이터
- 관측치 **7,043**, 원본 변수 **21**, 타깃 `Churn → Churn01(0/1)` :contentReference[oaicite:1]{index=1}  
- 주요 결측: `DeviceProtection` **49.17% (3,463건)** :contentReference[oaicite:2]{index=2}  
- 출처: :contentReference[oaicite:3]{index=3} 샘플 구조 + :contentReference[oaicite:4]{index=4} 배포 데이터 :contentReference[oaicite:5]{index=5}

## 전처리 핵심
- `TotalCharges` 문자열 → 숫자 변환(불가 값 결측 처리) :contentReference[oaicite:6]{index=6}  
- 수치형 결측: **중앙값 대체**, 범주형 결측: **'Unknown'**, 인터넷 미가입 맥락: **'No internet service'** :contentReference[oaicite:7]{index=7}  
- 이상치 행 제거는 하지 않고, `value_gap`은 **qcut binning**으로 왜곡 완화 :contentReference[oaicite:8]{index=8}

## 핵심 파생변수(분석 결과에 영향 큼)
- `tenure_stage`: early(0–3), mid(4–12), late(13+) :contentReference[oaicite:9]{index=9}  
- `friction_score(0–3)`: Contract/PaymentMethod/PaperlessBilling 조합으로 “거래 마찰” 단순화 :contentReference[oaicite:10]{index=10}  
- `value_gap`: 동일 번들 대비 **상대 과금 차이**(절대 요금 아님) :contentReference[oaicite:11]{index=11}  
- 주의: `DeviceProtection` 결측이 많아 보안/지원 지수 해석 시 “미가입 vs 미기재” 혼재 가능 :contentReference[oaicite:12]{index=12}

## EDA 핵심 결과
- tenure별 이탈률: **early 56.2% → mid 39.1% → late 17.1% (전체 26.5%)** :contentReference[oaicite:13]{index=13}  
- `friction_score`가 높을수록 모든 단계에서 이탈 급증(early: 1→2→3이 36.5%→55.4%→77.1%) :contentReference[oaicite:14]{index=14}  
- `entertainment_index`(스트리밍 번들 강도)는 이탈과 **양(+)의 경향** :contentReference[oaicite:15]{index=15}  
- `security_support_index`(보안/지원 번들)는 (특히 2 이상) 이탈과 **음(-)의 경향** :contentReference[oaicite:16]{index=16}  
- **고 value_gap × 고 friction** 조합에서 이탈이 크게 증폭 :contentReference[oaicite:17]{index=17}

## 실행 제안(요약)
- **early(0–3)**: 온보딩/초기 품질·초기 문의 대응 강화 + friction 2–3 우선 타깃(결제수단 전환, 1년 약정 업셀) + 스트리밍 프로모션 종료 관리 :contentReference[oaicite:18]{index=18}  
- **mid(4–12)**: value_gap 상위 고객에 요금제 재추천/번들 재구성 + 결제수단 전환 & 장기계약 전환 :contentReference[oaicite:19]{index=19}  
- **late(13+)**: 고 friction × 고 value_gap을 “이탈 직전군”으로 보고 맞춤 혜택 + 보안/지원 번들 패키지 검토 :contentReference[oaicite:20]{index=20}  
- 데이터 품질: `DeviceProtection` 결측 원인 점검 + Unknown 표준화/관리 :contentReference[oaicite:21]{index=21}

## 참고(원문 링크)
- IBM Docs / Kaggle 원문 링크는 보고서 말미에 기재 :contentReference[oaicite:22]{index=22}
