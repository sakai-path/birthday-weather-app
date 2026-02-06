import requests
import streamlit as st
from datetime import date

st.set_page_config(page_title="僕が生まれた日の空は", page_icon="🌤️")

st.title("🌤️ 僕が生まれた日の空は")
st.caption("Open-Meteoを直叩きして、過去の天気を取得します（まずは成功体験）")

# 都市（緯度・経度）
CITIES = {
    "東京": (35.6895, 139.6917),
    "大阪": (34.6937, 135.5023),
    "札幌": (43.0621, 141.3544),
    "福岡": (33.5902, 130.4017),
    "那覇": (26.2124, 127.6809),
}

def build_weather_url(d: str, lat: float, lon: float) -> str:
    return (
        "https://archive-api.open-meteo.com/v1/archive"
        f"?latitude={lat}"
        f"&longitude={lon}"
        f"&start_date={d}"
        f"&end_date={d}"
        "&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,windspeed_10m_max"
        "&timezone=Asia/Tokyo"
    )

def fetch_open_meteo(url: str) -> dict:
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    return resp.json()

# 入力
col1, col2 = st.columns(2)
with col1:
    birthday = st.date_input(
        "生年月日",
        value=date(1990, 1, 1),
        min_value=date(1940, 1, 1),
        max_value=date.today(),
    )
with col2:
    city = st.selectbox("生まれた場所（都市）", list(CITIES.keys()))

# 実行
if st.button("天気を調べる", type="primary"):
    lat, lon = CITIES[city]
    url = build_weather_url(str(birthday), lat, lon)

    with st.spinner("取得中..."):
        try:
            data = fetch_open_meteo(url)
            daily = data.get("daily")

            if not daily:
                st.error("daily が見つかりませんでした。取得結果を確認してください。")
                st.json(data)
                st.stop()

            st.success(f"📅 {birthday.strftime('%Y年%m月%d日')}（{city}）の天気")

            cols = st.columns(4)
            cols[0].metric("最高気温", f"{daily['temperature_2m_max'][0]}℃")
            cols[1].metric("最低気温", f"{daily['temperature_2m_min'][0]}℃")
            cols[2].metric("最大風速", f"{daily['windspeed_10m_max'][0]}m/s")
            cols[3].metric("降水量", f"{daily['precipitation_sum'][0]}mm")

            with st.expander("取得したJSON（デバッグ用）"):
                st.json(data)

        except Exception as e:
            st.error("取得に失敗しました。")
            st.write(e)
            st.write("URL:", url)
