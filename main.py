import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------------------------------------------------------
# 기본 설정
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    layout="wide",
)

st.title("영화 데이터 그래프 도감 1 - 시간")
st.caption("KOBIS 일별 박스오피스 데이터를 활용한 시간 축 그래프 모음")

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"


# ----------------------------------------------------------------------------
# 데이터 불러오기
# ----------------------------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)
    # 날짜 열(예: 20250901)을 진짜 날짜 타입으로 변환
    df["날짜"] = pd.to_datetime(df["날짜"], format="%Y%m%d")
    return df


df = load_data()


# ============================================================================
# 구역 1. 영화별 일별 관객 수 변화 (선 그래프)
# ============================================================================
st.header("1. 영화별 일별 관객 수 변화")

movie_list = sorted(df["영화명"].unique())
selected_movie = st.selectbox("영화를 선택하세요", movie_list)

movie_df = df[df["영화명"] == selected_movie].sort_values("날짜")

fig1 = px.line(
    movie_df,
    x="날짜",
    y="일관객",
    markers=True,
    title=f"'{selected_movie}' 일별 관객 수 변화",
    labels={"날짜": "날짜", "일관객": "일일 관객 수"},
)
fig1.update_traces(
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>관객 수: %{y:,}명<extra></extra>"
)
fig1.update_layout(hovermode="x unified")

st.plotly_chart(fig1, use_container_width=True)

st.info("**이 그래프로 알 수 있는 것:** (여기에 문구를 입력하세요)")


# ============================================================================
# 구역 2. (다음 그래프를 위한 자리)
# ============================================================================
st.header("2. 다음 그래프 자리")
st.write("앞으로 이 자리에 새로운 그래프를 추가할 예정입니다.")


# ============================================================================
# 구역 3. (다음 그래프를 위한 자리)
# ============================================================================
st.header("3. 다음 그래프 자리")
st.write("앞으로 이 자리에 새로운 그래프를 추가할 예정입니다.")
