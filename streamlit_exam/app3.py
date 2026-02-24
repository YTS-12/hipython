# import streamlit as st

# layout 요소 2

# st.sidebar.radio("이동", ["메인페이지", "분석보고서", "설정"])
# st.sidebar.metric('접속자수:', '백만명', '+백만명')

# if st.sidebar.button('눌러봐!!!') : 
#  st.balloons()


# 파이썬 스트림릿 대시보드를 만들어주세요.
# 아래의 구조를 실행가능한 파이썬 코드로 완성하세요
# 기본구성
# 페이지 제목 표시, 이미지 1장 넣기
# 사이드바는 컨트롤 센터로 지정
# 사이드바에 메뉴이동 라디오버튼(메인페이지, 분석보고서, 설정)
# 메인페이지
# 2개의 컬럼으로 kpi 대시보드 구성
# 방문자수, 활성 사용자수를 메트릭 카드로 구성
# 분석페이지
# 탭으로 구성 차트/데이터/설정
# 차트탭에는 간단한 사용자 방문현황 그래프
# 테이터탭에는 데이터 테이블 출력
# 설정 탭에는 연결시 옵션 체크박스
# 추가요구사항
# steramlit 함수 : 기발하고 예쁜 것 위주로 적용
# 코드 전체를 한번에 출력
# 꼭 실행가능한 코드여야함.

import os
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import matplotlib as mpl
from matplotlib import font_manager


# ----------------------------
# 0) 폰트(한글) 설정
# ----------------------------
def set_korean_font():
    candidates = ["Malgun Gothic", "맑은 고딕", "AppleGothic", "NanumGothic", "Noto Sans CJK KR"]
    available = {f.name for f in font_manager.fontManager.ttflist}

    for c in candidates:
        if c in available:
            mpl.rcParams["font.family"] = c
            break

    mpl.rcParams["axes.unicode_minus"] = False


set_korean_font()


# ----------------------------
# 1) 테마/CSS (F1 + Mercedes AMG PETRONAS)
# ----------------------------
def inject_f1_mercedes_css():
    st.markdown("""
    <style>
    /* ====== Global ====== */
    .stApp {
        background: radial-gradient(1200px 600px at 20% 0%, rgba(0,210,190,0.14), rgba(0,0,0,0)),
                    linear-gradient(180deg, #0B0F14 0%, #070A0E 100%);
    }

    /* 기본 텍스트 */
    html, body, [class*="css"]  {
        letter-spacing: 0.2px;
    }

    /* ====== Sidebar ====== */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0F1720 0%, #0B0F14 100%);
        border-right: 1px solid rgba(0,210,190,0.25);
    }

    section[data-testid="stSidebar"] .stRadio {
        padding: 14px 12px;
        border-radius: 16px;
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(0,210,190,0.18);
        box-shadow: 0 10px 30px rgba(0,0,0,0.35);
    }

    /* ====== Header ====== */
    .f1-header {
        display:flex;
        align-items:center;
        justify-content:space-between;
        gap: 12px;
        padding: 14px 18px;
        border-radius: 18px;
        background: linear-gradient(90deg, rgba(0,210,190,0.18), rgba(255,255,255,0.03));
        border: 1px solid rgba(0,210,190,0.25);
        box-shadow: 0 18px 45px rgba(0,0,0,0.45);
        margin-bottom: 14px;
    }

    .f1-title {
        font-size: 22px;
        font-weight: 900;
        margin: 0;
        line-height: 1.1;
    }

    .f1-sub {
        margin: 0;
        color: rgba(230,241,255,0.72);
        font-size: 13px;
    }

    .f1-badge {
        padding: 8px 10px;
        border-radius: 999px;
        background: rgba(0,210,190,0.16);
        border: 1px solid rgba(0,210,190,0.35);
        color: #E6F1FF;
        font-weight: 800;
        font-size: 12px;
        white-space: nowrap;
    }

    /* ====== Cards ====== */
    .card {
        padding: 16px 16px;
        border-radius: 18px;
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 16px 40px rgba(0,0,0,0.40);
        margin-bottom: 12px;
    }

    .card-accent {
        border: 1px solid rgba(0,210,190,0.28);
        background: linear-gradient(180deg, rgba(0,210,190,0.08), rgba(255,255,255,0.02));
    }

    .kpi {
        display:flex; justify-content:space-between; align-items:flex-end;
        gap: 10px;
    }
    .kpi .label { color: rgba(230,241,255,0.70); font-size: 12px; }
    .kpi .value { font-size: 26px; font-weight: 950; }

    /* ====== Plot frame ====== */
    div[data-testid="stPlotlyChart"], div[data-testid="stPyplotFigure"] {
        border-radius: 18px;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.10);
        box-shadow: 0 16px 40px rgba(0,0,0,0.40);
    }

    /* 버튼 */
    .stButton button {
        border-radius: 14px !important;
        border: 1px solid rgba(0,210,190,0.35) !important;
        background: rgba(0,210,190,0.14) !important;
        font-weight: 800 !important;
    }
    </style>
    """, unsafe_allow_html=True)


def render_header():
    st.markdown("""
    <div class="f1-header">
        <div>
            <p class="f1-title">통신사 고객이탈 데이터 분석</p>
            <p class="f1-sub">Mercedes-AMG PETRONAS mood · Retention Dashboard</p>
        </div>
        <div class="f1-badge">#63 · George Russell</div>
    </div>
    """, unsafe_allow_html=True)


def show_table_with_chart(df_table, chart_type: str, title: str):
    st.markdown(f"#### {title}")

    if isinstance(df_table, pd.Series):
        df_table = df_table.to_frame()

    if df_table is None or df_table.empty:
        st.info("표시할 데이터가 없습니다.")
        return

    if chart_type == "bar":
        fig, ax = plt.subplots(figsize=(5.3, 2.9), dpi=120)
        df_table.plot(kind="bar", ax=ax)
        ax.set_title(title)
        ax.set_ylabel("Churn Rate (%)")
        ax.set_xlabel("")
        ax.tick_params(axis="x", rotation=0)

        # 범례가 커지면 그래프가 과하게 커 보이므로 아래로 내림
        ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.18), ncol=3, frameon=False)

        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    elif chart_type == "heat":
        fig, ax = plt.subplots(figsize=(6.8, 3.8), dpi=110)
        ax.imshow(df_table.values)

        ax.set_title(title)
        ax.set_xlabel("Value Gap Bin")
        ax.set_ylabel("Friction Score")

        ax.set_xticks(np.arange(df_table.shape[1]))
        ax.set_yticks(np.arange(df_table.shape[0]))
        ax.set_xticklabels(df_table.columns.astype(str))
        ax.set_yticklabels(df_table.index.astype(str))

        for i in range(df_table.shape[0]):
            for j in range(df_table.shape[1]):
                v = df_table.values[i, j]
                ax.text(j, i, "NA" if np.isnan(v) else f"{v:.1f}", ha="center", va="center", fontsize=9)

        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    st.dataframe(df_table.round(2), use_container_width=True, height=260)




def pick_col(df: pd.DataFrame, candidates):
    cols_lower = {c.lower(): c for c in df.columns}
    for cand in candidates:
        if cand.lower() in cols_lower:
            return cols_lower[cand.lower()]
    return None


def to_binary_churn(series: pd.Series) -> pd.Series:
    s = series.copy()
    if pd.api.types.is_numeric_dtype(s):
        return s.fillna(0).astype(float).clip(0, 1).round().astype(int)

    s = s.astype(str).str.strip().str.lower()
    mapping = {"yes": 1, "y": 1, "true": 1, "1": 1, "no": 0, "n": 0, "false": 0, "0": 0}
    return s.map(lambda x: mapping.get(x, np.nan))


def build_tenure_stage(tenure_months: pd.Series) -> pd.Series:
    t = pd.to_numeric(tenure_months, errors="coerce")
    bins = [-np.inf, 3, 12, np.inf]
    labels = ["Early(0-3)", "Mid(4-12)", "Late(13+)"]
    return pd.cut(t, bins=bins, labels=labels)


# ----------------------------
# 2) 페이지 기본 설정 + CSS/헤더
# ----------------------------
st.set_page_config(
    page_title="통신사 고객이탈 데이터 분석",
    page_icon="📊",
    layout="wide"
)

inject_f1_mercedes_css()
render_header()


# ----------------------------
# 3) 경로 설정 (메인 로고)
# ----------------------------
F1_LOGO_PATH = r"C:\Users\Admin\hipython\streamlit_exam\image\F1 로고.jpg"
MERC_LOGO_PATH = r"C:\Users\Admin\hipython\streamlit_exam\image\메르세데스 AMG 페트로나스.webp"
DEFAULT_DATA_PATH = "cust_data_v1.csv"


# ----------------------------
# 4) 데이터 로드 (상대경로 + 업로드)
# ----------------------------
@st.cache_data
def load_csv_from_path(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

@st.cache_data
def load_csv_from_upload(uploaded_file) -> pd.DataFrame:
    return pd.read_csv(uploaded_file)


# ----------------------------
# 5) 사이드바 메뉴
# ----------------------------
with st.sidebar:
    st.markdown("### 🏁 GARAGE")
    st.caption("AMG PETRONAS · Strategy Dashboard")
    st.markdown("---")

menu = st.sidebar.radio(
    "메뉴 이동",
    ["메인", "프로젝트 목적", "데이터 불러오기", "EDA", "데이터전처리", "시각화", "인사이트", "향후전략"]
)


# ----------------------------
# 6) 세션 데이터 확보
# ----------------------------
if "df" not in st.session_state:
    st.session_state.df = None


# ----------------------------
# 7) 메인 페이지 (팬심 + 로고)
# ----------------------------
if menu == "메인":
    st.markdown("""
    <div class="card card-accent">
        <div style="display:flex; justify-content:space-between; align-items:flex-end; gap:10px;">
            <div>
                <div style="font-size:18px; font-weight:950;">Mercedes-AMG PETRONAS · Fan Mode</div>
                <div style="color: rgba(230,241,255,0.75); margin-top:6px;">
                    조지 러셀(#63) 팬 시점으로 보는 <b>리텐션 레이스 엔지니어링</b> 대시보드
                </div>
            </div>
            <div class="f1-badge">#63 · George Russell</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 팀 로고")

    c1, c2 = st.columns([1, 1])
    with c1:
        if os.path.exists(F1_LOGO_PATH):
            st.image(F1_LOGO_PATH, caption="Formula 1", use_container_width=True)
        else:
            st.warning(f"F1 로고 파일을 찾지 못함: {F1_LOGO_PATH}")

    with c2:
        if os.path.exists(MERC_LOGO_PATH):
            st.image(MERC_LOGO_PATH, caption="Mercedes-AMG PETRONAS", use_container_width=True)
        else:
            st.warning(f"메르세데스 로고 파일을 찾지 못함: {MERC_LOGO_PATH}")

    st.markdown("""
    <div class="card">
        <div style="font-size:14px; font-weight:900; margin-bottom:6px;">오늘의 Race Plan</div>
        <div style="color: rgba(230,241,255,0.78);">
            1) 데이터 불러오기 → 2) 전처리(파생변수) → 3) 시각화(Stage/파생/조합) → 4) 인사이트 → 5) 향후전략
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.stop()


# ----------------------------
# 8) 데이터 불러오기 페이지
# ----------------------------
if menu == "데이터 불러오기":
    st.subheader("데이터 불러오기")

    mode = st.radio("불러오기 방식", ["CSV 업로드", "로컬 경로"], horizontal=True)

    if mode == "CSV 업로드":
        uploaded = st.file_uploader("cust_data_v1.csv 업로드", type=["csv"])
        if uploaded is not None:
            st.session_state.df = load_csv_from_upload(uploaded)
            st.success(f"업로드 완료: {st.session_state.df.shape[0]:,} rows × {st.session_state.df.shape[1]:,} cols")
            st.dataframe(st.session_state.df.head(30), use_container_width=True)

    else:
        path = st.text_input("CSV 파일 경로", value=DEFAULT_DATA_PATH)
        if st.button("경로로 로드"):
            st.session_state.df = load_csv_from_path(path)
            st.success(f"로드 완료: {st.session_state.df.shape[0]:,} rows × {st.session_state.df.shape[1]:,} cols")
            st.dataframe(st.session_state.df.head(30), use_container_width=True)


# 다른 페이지는 df 필요
if menu != "데이터 불러오기":
    if st.session_state.df is None:
        st.warning("먼저 [데이터 불러오기]에서 CSV를 로드하세요.")
        st.stop()

df = st.session_state.df.copy()

# 핵심 컬럼 탐지
churn_col = pick_col(df, ["Churn", "churn", "Exited", "is_churn", "Attrition"])
tenure_col = pick_col(df, ["tenure", "Tenure", "tenure_months", "MonthsInService", "가입기간"])

# 공통 작업용
df_work = df.copy()
if churn_col:
    df_work["_churn_bin"] = to_binary_churn(df_work[churn_col])
else:
    df_work["_churn_bin"] = np.nan

if tenure_col:
    df_work["_tenure_stage"] = build_tenure_stage(df_work[tenure_col])
else:
    df_work["_tenure_stage"] = None


# ----------------------------
# 9) 페이지별 렌더링
# ----------------------------
if menu == "프로젝트 목적":
    st.subheader("프로젝트 목적")
    st.write("""
- 고객 이탈(Churn) 요인을 탐색하고, 가입기간(Tenure) 단계(Early/Mid/Late)별로 진단하여 실행 전략을 도출합니다.
- 결과물은 EDA 중심 인사이트 + 실행 전략에 초점을 둡니다.
    """)

    st.subheader("대시보드 구성")
    st.markdown("""
- 메인 → 데이터 불러오기 → EDA → 전처리 → 시각화 → 인사이트 → 향후전략
    """)

elif menu == "EDA":
    st.subheader("EDA (탐색적 데이터 분석)")

    st.markdown("### 결측치 요약")
    miss = (df_work.isna().mean().sort_values(ascending=False) * 100).round(2)
    st.dataframe(pd.DataFrame({"missing_%": miss}).head(30), use_container_width=True)

    st.markdown("### 타깃(Churn) 분포")
    if churn_col and df_work["_churn_bin"].notna().any():
        churn_rate = df_work["_churn_bin"].mean() * 100
        st.metric("전체 이탈률(%)", f"{churn_rate:.1f}")

        vc = df_work["_churn_bin"].value_counts(dropna=False)
        fig, ax = plt.subplots(figsize=(5.6, 2.6), dpi=120)
        ax.bar(vc.index.astype(str), vc.values)
        ax.set_title("Churn (0=유지, 1=이탈) 분포")
        ax.tick_params(axis="x", rotation=0)
        st.pyplot(fig)
        plt.close(fig)
    else:
        st.warning("Churn 컬럼을 찾지 못했거나 0/1 변환이 어려워 분포를 표시할 수 없습니다.")

    st.markdown("### Tenure 단계별 분포/이탈률")
    if tenure_col:
        c1, c2 = st.columns(2)
        with c1:
            vc = df_work["_tenure_stage"].value_counts(dropna=False)
            fig, ax = plt.subplots()
            ax.bar(vc.index.astype(str), vc.values)
            ax.set_title("Tenure Stage 분포 (Early/Mid/Late)")
            ax.tick_params(axis="x", rotation=0)
            st.pyplot(fig)
            plt.close(fig)

        with c2:
            if df_work["_churn_bin"].notna().any():
                grp = df_work.groupby("_tenure_stage")["_churn_bin"].mean().mul(100)
                st.dataframe(grp.round(2).rename("churn_%"), use_container_width=True)
            else:
                st.info("Churn 0/1 변환이 불완전하여 단계별 이탈률 표시는 생략합니다.")
    else:
        st.info("Tenure 컬럼을 찾지 못해 단계 분석을 생략합니다.")

elif menu == "데이터전처리":
    st.subheader("데이터 전처리")

    df_prep = df.copy()

    st.markdown("### 1) 결측치 처리")
    missing_table = (df_prep.isna().mean() * 100).round(2)
    st.dataframe(pd.DataFrame({"missing_%": missing_table}).sort_values("missing_%", ascending=False), use_container_width=True)

    obj_cols = df_prep.select_dtypes(include="object").columns
    df_prep[obj_cols] = df_prep[obj_cols].fillna("UNKNOWN")

    num_cols = df_prep.select_dtypes(include=np.number).columns
    for col in num_cols:
        df_prep[col] = df_prep[col].fillna(df_prep[col].median())

    st.success("문자형 → 'UNKNOWN', 수치형 → 중앙값으로 결측치 처리 완료")

    st.markdown("### 2) 파생변수 생성")

    sec_support_cols = ["OnlineSecurity", "TechSupport", "DeviceProtection"]
    ent_cols = ["StreamingTV", "StreamingMovies"]
    backup_cols = ["OnlineBackup"]

    sec_support_cols = [c for c in sec_support_cols if c in df_prep.columns]
    ent_cols = [c for c in ent_cols if c in df_prep.columns]
    backup_cols = [c for c in backup_cols if c in df_prep.columns]

    for col in sec_support_cols + ent_cols + backup_cols:
        df_prep[col] = (df_prep[col].astype(str).str.strip() == "Yes").astype(int)

    df_prep["security_support_index"] = df_prep[sec_support_cols].sum(axis=1) if sec_support_cols else 0
    df_prep["entertainment_index"] = df_prep[ent_cols].sum(axis=1) if ent_cols else 0
    df_prep["backup_index"] = df_prep[backup_cols].sum(axis=1) if backup_cols else 0

    required_cols = ["Contract", "PaymentMethod", "PaperlessBilling", "MonthlyCharges", "Churn", "tenure"]
    miss_required = [c for c in required_cols if c not in df_prep.columns]
    if miss_required:
        st.error(f"파생변수/시각화에 필요한 컬럼이 없습니다: {miss_required}")
        st.stop()

    df_prep["friction_score"] = (
        (df_prep["Contract"] == "Month-to-month").astype(int)
        + (df_prep["PaymentMethod"] == "Electronic check").astype(int)
        + (df_prep["PaperlessBilling"] == "Yes").astype(int)
    )

    df_prep["bundle_total_index"] = (
        df_prep["security_support_index"] + df_prep["entertainment_index"] + df_prep["backup_index"]
    )

    group_mean = df_prep.groupby("bundle_total_index")["MonthlyCharges"].transform("mean")
    df_prep["value_gap"] = df_prep["MonthlyCharges"] - group_mean

    try:
        df_prep["value_gap_bin"] = pd.qcut(df_prep["value_gap"], q=4, labels=["Low", "Mid-Low", "Mid-High", "High"])
    except Exception:
        df_prep["value_gap_bin"] = pd.cut(df_prep["value_gap"], bins=4, labels=["Low", "Mid-Low", "Mid-High", "High"])

    st.success("파생변수 생성 완료")

    st.markdown("### 파생변수 설명")
    st.markdown("""
| 변수 | 의미 |
|---|---|
| security_support_index | 보안/기술지원/장비보호 서비스 개수(Yes 합) |
| entertainment_index | TV/영화 스트리밍 서비스 개수(Yes 합) |
| backup_index | 백업 서비스 여부(Yes=1) |
| bundle_total_index | 번들 총합(보안/지원 + 엔터 + 백업) |
| friction_score | 마찰 점수(계약 Month-to-month + 결제 Electronic check + PaperlessBilling Yes) |
| value_gap | 동일 번들 대비 월요금 차이(월요금 - 번들그룹 평균) |
| value_gap_bin | value_gap 사분위 구간 |
""")

    st.session_state.df_prep = df_prep
    st.dataframe(df_prep.head(20), use_container_width=True)

elif menu == "시각화":
    st.subheader("시각화")

    if "df_prep" not in st.session_state:
        st.warning("먼저 [데이터 전처리] 페이지에서 전처리를 실행하세요.")
        st.stop()

    df_viz = st.session_state.df_prep.copy()

    if "Churn" not in df_viz.columns or "tenure" not in df_viz.columns:
        st.error("시각화에 필요한 컬럼(Churn, tenure)이 없습니다.")
        st.stop()

    df_viz["churn_bin"] = (df_viz["Churn"].astype(str).str.strip() == "Yes").astype(int)
    df_viz["stage"] = pd.cut(
        pd.to_numeric(df_viz["tenure"], errors="coerce"),
        bins=[-1, 3, 12, np.inf],
        labels=["Early(0-3)", "Mid(4-12)", "Late(13+)"]
    )
    stage_order = ["Early(0-3)", "Mid(4-12)", "Late(13+)"]

    st.markdown("## 1) Stage별 이탈률(%)")
    stage_churn = (df_viz.groupby("stage")["churn_bin"].mean() * 100).reindex(stage_order)
    show_table_with_chart(stage_churn.rename("churn_%"), "bar", "Stage별 이탈률(%)")

    st.markdown("## 2) 파생변수 값별 이탈률(Stage별)")
    derived_cols = [c for c in [
        "friction_score", "bundle_total_index", "value_gap_bin",
        "security_support_index", "entertainment_index", "backup_index"
    ] if c in df_viz.columns]

    if not derived_cols:
        st.warning("파생변수 컬럼이 없습니다. [데이터 전처리]에서 파생변수를 생성했는지 확인하세요.")
        st.stop()

    pick = st.selectbox("파생변수 선택", derived_cols, index=0)

    pivot = df_viz.pivot_table(
        index="stage",
        columns=pick,
        values="churn_bin",
        aggfunc="mean"
    ) * 100
    pivot = pivot.reindex(stage_order)
    show_table_with_chart(pivot, "bar", f"{pick} 값별 이탈률(%) - Stage별")

    st.markdown("## 3) Friction Score × Value Gap Bin 이탈률(%)")
    required = {"friction_score", "value_gap_bin"}
    if not required.issubset(df_viz.columns):
        st.warning("friction_score 또는 value_gap_bin 컬럼이 없어 히트맵을 만들 수 없습니다.")
        st.stop()

    heat = df_viz.pivot_table(
        index="friction_score",
        columns="value_gap_bin",
        values="churn_bin",
        aggfunc="mean"
    ) * 100

    desired_cols = ["Low", "Mid-Low", "Mid-High", "High"]
    heat = heat.reindex(columns=[c for c in desired_cols if c in heat.columns])
    show_table_with_chart(heat, "heat", "Friction Score × Value Gap Bin 이탈률(%)")

elif menu == "인사이트":
    st.subheader("인사이트")

    if "df_prep" not in st.session_state:
        st.warning("먼저 [데이터 전처리] 페이지에서 전처리를 실행하세요.")
        st.stop()

    df_i = st.session_state.df_prep.copy()
    if "Churn" not in df_i.columns or "tenure" not in df_i.columns:
        st.error("인사이트에 필요한 컬럼(Churn, tenure)이 없습니다.")
        st.stop()

    df_i["churn_bin"] = (df_i["Churn"].astype(str).str.strip() == "Yes").astype(int)
    df_i["stage"] = pd.cut(
        pd.to_numeric(df_i["tenure"], errors="coerce"),
        bins=[-1, 3, 12, np.inf],
        labels=["Early(0-3)", "Mid(4-12)", "Late(13+)"]
    )

    st.markdown("### 핵심 발견")
    stage_churn2 = (df_i.groupby("stage")["churn_bin"].mean() * 100).dropna()
    if not stage_churn2.empty:
        worst_stage = stage_churn2.idxmax()
        worst_rate = stage_churn2.max()
        st.write(f"- 가장 이탈률이 높은 구간: **{worst_stage}** / **{worst_rate:.1f}%**")

    if "friction_score" in df_i.columns:
        fric = (df_i.groupby("friction_score")["churn_bin"].mean() * 100).dropna()
        if not fric.empty:
            st.write(f"- friction_score 최고 이탈 구간: **{fric.idxmax()}** / **{fric.max():.1f}%**")

    if "value_gap_bin" in df_i.columns:
        vg = (df_i.groupby("value_gap_bin")["churn_bin"].mean() * 100).dropna()
        if not vg.empty:
            st.write(f"- value_gap_bin 최고 이탈 구간: **{vg.idxmax()}** / **{vg.max():.1f}%**")

    st.markdown("### 해석 가이드(운영 관점)")
    st.write("""
- Early 이탈률이 높으면: 온보딩/초기 마찰 제거가 1순위
- friction_score가 높을수록 이탈 증가: 계약/결제/청구 흐름 개선이 직접 레버리지
- value_gap_bin High에서 이탈 증가: 동일 번들 대비 가격 체감 불만 → 요금/혜택 재구성 필요
""")

elif menu == "향후전략":
    st.subheader("향후 전략")

    st.markdown("""
### 1) Early Stage (0~3개월)
- 온보딩 집중(개통/설치/첫 청구 전후 케어)
- month-to-month + electronic check + paperless 조합 고객에 선제 안내/간소화

### 2) Mid Stage (4~12개월)
- 번들 업셀/리번들링(보안/지원/백업/엔터)
- 장기 계약 전환 인센티브(혜택을 “가치”로 체감시키기)

### 3) Late Stage (13개월+)
- VIP 케어/리워드
- 불만 신호(가격/지원) 기반 선제 리텐션 오퍼
""")
