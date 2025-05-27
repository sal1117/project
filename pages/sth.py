import streamlit as st
import requests
from datetime import datetime

# NASA API 정보
API_URL = "https://api.nasa.gov/planetary/apod"
API_KEY = "DEMO_KEY"  # 여기다 본인 키 넣어도 돼요

st.set_page_config(page_title="오늘의 우주 사진", layout="centered")
st.title("🌌 NASA 오늘의 우주 사진 (APOD)")

# 날짜 선택
today = datetime.today().date()
date = st.date_input("날짜를 선택하세요", value=today, max_value=today)

# API 요청
params = {
    "api_key": API_KEY,
    "date": str(date)
}

response = requests.get(API_URL, params=params)

if response.status_code == 200:
    data = response.json()

    st.subheader(data["title"])
    st.write(f"📅 날짜: {data['date']}")

    # 미디어 타입 확인
    if data["media_type"] == "image":
        st.image(data["url"], caption=data["title"], use_column_width=True)
    elif data["media_type"] == "video":
        st.video(data["url"])
    else:
        st.write("지원되지 않는 미디어 형식입니다.")

    st.write("📝 설명:")
    st.write(data["explanation"])

else:
    st.error("NASA API에서 데이터를 가져오지 못했습니다.")
    st.write(response.text)
