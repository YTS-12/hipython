# 통신사 고객 이탈(Churn) EDA 요약 (모델링 제외)

## 데이터 출처
- IBM Cognos Analytics 샘플 데이터(“Telco customer churn”) 기반
- Kaggle에 공개된 동일/파생 버전 데이터셋(일반적으로 `WA_Fn-UseC_-Telco-Customer-Churn.csv`) 사용

## 분석 목적
- 고객 이탈을 **tenure 단계(early/mid/late)**로 나눠,
  - 단계별 이탈 수준
  - 이탈과 함께 움직이는 **조정 가능한 운영 레버(계약/결제/청구/번들 구성)**를 찾는다.

## 전처리 핵심(요약)
- 금액 컬럼 타입 정리(문자 → 숫자)
- 결측: 수치형 대표값 대체 / 범주형 Unknown 보정(서비스 미가입 맥락은 의미 보존)
- 비교 왜곡을 줄이기 위해 일부 지표는 구간화(binning)

## 핵심 파생변수(요약)
- `tenure_stage`: early(0–3) / mid(4–12) / late(13+)
- `friction_score(0–3)`: 계약 형태 + 결제수단 + 전자청구 여부를 묶어 “거래 마찰” 점수화
- `value_gap`: 동일 번들 대비 상대 과금 차이(비싸게 느끼는 정도)

## EDA 핵심 인사이트
- **early(0–3개월) 이탈률이 가장 높고**, tenure가 길수록 이탈률이 낮아지는 패턴
- `friction_score`가 높을수록 모든 단계에서 이탈이 상승(특히 early에서 상승폭 큼)
- **고 value_gap × 고 friction** 조합에서 이탈이 크게 증폭(“비싸게 느끼는데 절차도 번거로운” 케이스)

## 실행 제안(짧게)
- **early(0–3)**: 온보딩/초기 장애·문의 대응 강화 + 결제수단 전환/약정 전환 인센티브를 friction 높은 군에 집중
- **mid(4–12)**: value_gap 상위 고객에 요금제/번들 재추천(가격-가치 재정렬) + friction 완화 병행
- **late(13+)**: 고 value_gap × 고 friction을 “이탈 직전군”으로 보고 맞춤 혜택/개입 우선 적용
- 데이터 품질: 결측이 큰 서비스 변수는 원천 수집/정의 표준화 우선


## 참고 링크
- IBM Telco churn sample (Cognos Analytics):
  https://www.ibm.com/docs/en/cognos-analytics/12.0.x?topic=samples-telco-customer-churn
- Kaggle Telco Customer Churn dataset:
  https://www.kaggle.com/datasets/blastchar/telco-customer-churn
