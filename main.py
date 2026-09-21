import subprocess
import sys

import streamlit as st
import pandas as pd

# plotly가 설치되어 있지 않은 배포 환경(예: requirements.txt 미반영)을 대비해
# 자동으로 설치를 시도합니다.
try:
    import plotly.express as px
except ModuleNotFoundError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "plotly"])
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
# 구역 2. 누적 관객 상위 5편의 일별 관객 수 변화 (다중 선 그래프)
# ============================================================================
st.header("2. 이 기간 일관객 합계 상위 5편의 변화")

# 영화별 일관객 합계를 구해 상위 5편 선정
top5_movies = (
    df.groupby("영화명")["일관객"].sum().sort_values(ascending=False).head(5).index
)

top5_df = df[df["영화명"].isin(top5_movies)].sort_values("날짜")

fig2 = px.line(
    top5_df,
    x="날짜",
    y="일관객",
    color="영화명",
    markers=True,
    title="일관객 합계 상위 5편의 날짜별 일관객 변화",
    labels={"날짜": "날짜", "일관객": "일일 관객 수", "영화명": "영화명"},
)
fig2.update_traces(
    hovertemplate="영화: %{fullData.name}<br>날짜: %{x|%Y-%m-%d}<br>관객 수: %{y:,}명<extra></extra>"
)
fig2.update_layout(hovermode="x unified", legend_title_text="영화명 (클릭해서 켜고 끄기)")

st.plotly_chart(fig2, use_container_width=True)

st.info("**이 그래프로 알 수 있는 것:** (여기에 문구를 입력하세요)")


# ============================================================================
# 구역 3. 날짜별 10위권 일관객 합계 (영역 그래프)
# ============================================================================
st.header("3. 날짜별 박스오피스 10위권 일관객 합계")

daily_total = df.groupby("날짜", as_index=False)["일관객"].sum()
daily_total = daily_total.rename(columns={"일관객": "합계관객"})

# 합계가 가장 컸던 날 3일 선정
top3_days = daily_total.sort_values("합계관객", ascending=False).head(3)

fig3 = px.area(
    daily_total,
    x="날짜",
    y="합계관객",
    title="날짜별 박스오피스 10위권 일관객 합계",
    labels={"날짜": "날짜", "합계관객": "일관객 합계"},
)
fig3.update_traces(
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>합계 관객 수: %{y:,}명<extra></extra>"
)

# 상위 3일을 점으로 표시하고 날짜를 라벨로 표기
fig3.add_scatter(
    x=top3_days["날짜"],
    y=top3_days["합계관객"],
    mode="markers+text",
    text=top3_days["날짜"].dt.strftime("%Y-%m-%d"),
    textposition="top center",
    marker=dict(color="red", size=10, symbol="star"),
    name="합계 상위 3일",
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>합계 관객 수: %{y:,}명<extra></extra>",
)

st.plotly_chart(fig3, use_container_width=True)

st.info("**이 그래프로 알 수 있는 것:** (여기에 문구를 입력하세요)")


# ============================================================================
# 구역 4. 누적 관객 TOP 10 영화 (가로 막대 그래프)
# ============================================================================
st.header("4. 이 기간 일관객 합계 TOP 10 영화")

movie_summary = (
    df.groupby("영화명")
    .agg(관객합계=("일관객", "sum"), 상영일수=("날짜", "count"))
    .reset_index()
)

top10_summary = movie_summary.sort_values("관객합계", ascending=False).head(10)
# 관객이 많은 영화가 그래프 위쪽에 오도록 오름차순으로 재정렬
top10_summary = top10_summary.sort_values("관객합계", ascending=True)

fig4 = px.bar(
    top10_summary,
    x="관객합계",
    y="영화명",
    orientation="h",
    title="일관객 합계 TOP 10 영화",
    labels={"관객합계": "일관객 합계", "영화명": "영화명"},
    custom_data=["상영일수"],
)
fig4.update_traces(
    hovertemplate="영화: %{y}<br>관객 합계: %{x:,}명<br>10위권 든 날수: %{customdata[0]}일<extra></extra>"
)

st.plotly_chart(fig4, use_container_width=True)

st.info("**이 그래프로 알 수 있는 것:** (여기에 문구를 입력하세요)")


# ============================================================================
# 구역 5. (다음 그래프를 위한 자리)
# ============================================================================
st.header("5. 다음 그래프 자리")
st.write("앞으로 이 자리에 새로운 그래프를 추가할 예정입니다.")
