import streamlit as st
from datetime import date

st.title("🌤️ 僕が生まれた日の空は")
st.caption("まずは画面が出るかの確認用")

birthday = st.date_input(
    "生年月日",
    value=date(1990, 1, 1),
    min_value=date(1940, 1, 1),
    max_value=date.today(),
)

st.write("選択された日付:", birthday)

city = st.selectbox(
    "生まれた場所",
    ["東京", "大阪", "札幌", "福岡", "那覇"]
)

st.write("選択された都市:", city)
