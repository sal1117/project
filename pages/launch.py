import streamlit as st
st.title('오늘의 급식')

import streamlit as st
import datetime
import pytz


# 대한민국 시간 기준으로 오늘 날짜 출력
kst = pytz.timezone('Asia/Seoul')
now = datetime.datetime.now(kst)
today_str = now.strftime("%Y%m%d")


st.title("📅 오늘의 날짜")
st.write(f"오늘 날짜는 {today_str} 입니다.")

import streamlit as st
import requests
import datetime
import re
import pytz


kst = pytz.timezone('Asia/Seoul')
now = datetime.datetime.now(kst)
today_str = now.strftime("%Y%m%d")

# secrets.toml에서 값 불러오기
KEY = st.secrets['API_KEY']
education_office_code = st.secrets['education_office_code']
school_code = st.secrets['school_code']
meal_code = "2"  # 중식 코드


# 급식 정보 가져오기 함수
def get_meal_data(date_str):
    params = {
        "KEY": KEY,
        "Type": "json",
        "ATPT_OFCDC_SC_CODE": education_office_code,
        "SD_SCHUL_CODE": school_code,
        "MMEAL_SC_CODE": meal_code,
        "MLSV_YMD": date_str
    }
    try:
        response = requests.get("https://open.neis.go.kr/hub/mealServiceDietInfo", params=params)
        if response.status_code == 200:
            data = response.json()
            meal_data = data["mealServiceDietInfo"][1]["row"]
            for meal in meal_data:
                if meal.get("MLSV_YMD") == date_str:
                    meal_name = meal.get("DDISH_NM", "정보 없음")
                    return meal_name.replace('<br/>', '\n')
            return "급식 정보가 없습니다."
        else:
            return f"API 요청 실패: {response.status_code}"
    except Exception as e:
        return f"오류 발생: {e}"


st.title("🍱 오늘의 급식")
meal_info = get_meal_data(today_str)
st.text(meal_info)

import streamlit as st
import requests
import datetime
import re
import pytz


kst = pytz.timezone('Asia/Seoul')
now = datetime.datetime.now(kst)
today_str = now.strftime("%Y%m%d")


# secrets.toml에서 값 불러오기
KEY = st.secrets['API_KEY']
education_office_code = st.secrets['education_office_code']
school_code = st.secrets['school_code']
meal_code = "2"  # 중식 코드


# 급식 정보 가져오기 함수
def get_meal_data(date_str):
    params = {
        "KEY": KEY,
        "Type": "json",
        "ATPT_OFCDC_SC_CODE": education_office_code,
        "SD_SCHUL_CODE": school_code,
        "MMEAL_SC_CODE": meal_code,
        "MLSV_YMD": date_str
    }
    try:
        response = requests.get("https://open.neis.go.kr/hub/mealServiceDietInfo", params=params)
        if response.status_code == 200:
            data = response.json()
            meal_data = data["mealServiceDietInfo"][1]["row"]
            for meal in meal_data:
                if meal.get("MLSV_YMD") == date_str:
                    meal_name = meal.get("DDISH_NM", "정보 없음")
                    return meal_name.replace('<br/>', '\n')
            return "급식 정보가 없습니다."
        else:
            return f"API 요청 실패: {response.status_code}"
    except Exception as e:
        return f"오류 발생: {e}"


meal_info = get_meal_data(today_str)


heart_emoji_list = ["❤️", "🧡", "💛", "💚", "💙", "💜", "🖤", "🤍", "🤎"]


# 급식 정보 출력
if meal_info:
    st.markdown("<h2 style='text-align:center;'>🍴 오늘의 급식 🍱</h2>", unsafe_allow_html=True)
    meal_items = meal_info.split('\n')
    for i, item in enumerate(meal_items):
        heart = heart_emoji_list[i % len(heart_emoji_list)]
        st.markdown(f"<div class='meal-item'><span>{heart}</span><span>{item}</span><span>{heart}</span></div>", unsafe_allow_html=True)


# CSS 스타일 추가
st.markdown("""
<style>
.meal-item {
    padding: 10px;
    margin-bottom: 10px;
    border-radius: 5px;
    text-align: center;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
body {
    background-color: #ffffff;
    color: black;
}
@media (prefers-color-scheme: dark) {
    body {
        background-color: #121212;
        color: white;
    }
    .meal-item {
        background-color: #333333;
        color: white;
    }
}
@media (prefers-color-scheme: light) {
    .meal-item {
        background-color: #f0f0f0;
        color: black;
    }
}
</style>
""", unsafe_allow_html=True)
