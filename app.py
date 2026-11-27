import pandas as pd
import streamlit as st

# 같은 폴더에 있는 CSV 파일을 읽어옵니다.
data = pd.read_csv("sales_sample.csv")

# 날짜 열을 날짜 형식으로 바꿉니다.
data["date"] = pd.to_datetime(data["date"])

# 대시보드 제목을 화면에 표시합니다.
st.title("매출 대시보드")

# 날짜 범위 필터로 선택한 기간의 데이터만 확인합니다.
date_range = st.date_input(
    "날짜 범위",
    value=(data["date"].min().date(), data["date"].max().date()),
)

# 지역 필터에서 여러 지역을 선택할 수 있습니다.
selected_regions = st.multiselect(
    "지역 선택",
    options=sorted(data["region"].unique()),
    default=sorted(data["region"].unique()),
)

# 카테고리 필터에서 여러 카테고리를 선택할 수 있습니다.
selected_categories = st.multiselect(
    "카테고리 선택",
    options=sorted(data["category"].unique()),
    default=sorted(data["category"].unique()),
)

# 날짜, 지역, 카테고리 선택 조건에 맞는 데이터를 저장합니다.
filtered = data[
    (data["date"] >= pd.Timestamp(date_range[0]))
    & (data["date"] < pd.Timestamp(date_range[1]) + pd.Timedelta(days=1))
    & (data["region"].isin(selected_regions))
    & (data["category"].isin(selected_categories))
]

# 조건에 맞는 데이터가 없으면 안내 메시지를 보여주고 실행을 멈춥니다.
if filtered.empty:
    st.warning("조건에 맞는 데이터가 없습니다. 날짜, 지역 또는 카테고리를 변경해 주세요.")
    st.stop()

# 필터링된 데이터의 전체 매출액과 판매 수량을 계산합니다.
total_sales = filtered["sales"].sum()
total_quantity = filtered["quantity"].sum()

# 두 요약 값을 나란히 보여줍니다.
sales_col, quantity_col = st.columns(2)
sales_col.metric("전체 매출액", f"{total_sales:,.0f}원")
quantity_col.metric("판매 수량", f"{total_quantity:,.0f}개")

# 지역별 매출액을 합산해 막대 그래프로 보여줍니다.
st.subheader("지역별 매출")
sales_by_region = filtered.groupby("region")["sales"].sum().sort_values(ascending=False)
st.bar_chart(sales_by_region)

# 카테고리별 매출액을 합산해 막대 그래프로 보여줍니다.
st.subheader("카테고리별 매출")
sales_by_category = filtered.groupby("category")["sales"].sum().sort_values(ascending=False)
st.bar_chart(sales_by_category)

# 필터링된 원본 데이터를 표로 보여줍니다.
st.subheader("원본 데이터")
st.dataframe(filtered, use_container_width=True)