import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 등급 분류 함수
def get_grade(value, pm_type='pm10'):
    if pd.isna(value):
        return "정보 없음"
    if pm_type == 'pm10':
        if value <= 30:
            return "좋음"
        elif value <= 80:
            return "보통"
        else:
            return "나쁨"
    elif pm_type == 'pm25':
        if value <= 15:
            return "좋음"
        elif value <= 35:
            return "보통"
        else:
            return "나쁨"

# 사용자 입력
st.title("🌫️ 지역별 대기질 등급 확인")
sido = st.selectbox("시/도를 선택하세요", ["서울", "부산", "대구", "인천", "광주", "대전", "울산"])

# API 요청
API_key = st.secrets['API_key']  # API_KEY -> API_key로 수정
url = f"http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty"
params = {
    "sidoName": sido,
    "returnType": "json",
    "numOfRows": "100",
    "pageNo": "1",
    "serviceKey": API_key,
    "ver": "1.0"
}

# API 요청 및 응답 상태 코드 체크
res = requests.get(url, params=params)

if res.status_code == 200:  # HTTP 요청 성공 시
    try:
        # 응답 데이터 출력
        st.write(res.json())  # 여기서 응답 전체 데이터를 출력해서 어떤 형식인지 확인

        # 응답 데이터에서 필요한 부분 추출
        data = res.json().get('response', {}).get('body', {}).get('items', [])

        if data:  # 데이터가 있을 경우
            # 데이터프레임 변환
            df = pd.DataFrame(data)
            df["pm10Value"] = pd.to_numeric(df["pm10Value"], errors="coerce")
            df["pm25Value"] = pd.to_numeric(df["pm25Value"], errors="coerce")
            df["PM10 등급"] = df["pm10Value"].apply(lambda x: get_grade(x, 'pm10'))
            df["PM2.5 등급"] = df["pm25Value"].apply(lambda x: get_grade(x, 'pm25'))

            st.write(f"### {sido}의 실시간 대기질 정보")
            st.dataframe(df[["stationName", "pm10Value", "PM10 등급", "pm25Value", "PM2.5 등급"]])

            # PM10과 PM2.5 시각화
            st.subheader("PM10과 PM2.5 실시간 분포")
            fig, ax = plt.subplots(1, 2, figsize=(14, 6))

            # PM10 바 차트
            sns.barplot(x="stationName", y="pm10Value", data=df, ax=ax[0], palette="coolwarm")
            ax[0].set_title("PM10 대기질")
            ax[0].set_xticklabels(ax[0].get_xticklabels(), rotation=45, ha='right')

            # PM2.5 바 차트
            sns.barplot(x="stationName", y="pm25Value", data=df, ax=ax[1], palette="coolwarm")
            ax[1].set_title("PM2.5 대기질")
            ax[1].set_xticklabels(ax[1].get_xticklabels(), rotation=45, ha='right')

            st.pyplot(fig)

            # PM10 등급 분포
            st.subheader("PM10 대기질 등급 분포")
            pm10_grade_counts = df["PM10 등급"].value_counts()
            st.bar_chart(pm10_grade_counts)

            # PM2.5 등급 분포
            st.subheader("PM2.5 대기질 등급 분포")
            pm25_grade_counts = df["PM2.5 등급"].value_counts()
            st.bar_chart(pm25_grade_counts)

            # 추가: 시간대별 대기질 변화
            if 'dataTime' in df.columns:
                df['dataTime'] = pd.to_datetime(df['dataTime'], format='%Y-%m-%d %H:%M')
                df.set_index('dataTime', inplace=True)
                st.subheader("시간대별 PM10 대기질 변화")
                st.line_chart(df['pm10Value'])
                
                st.subheader("시간대별 PM2.5 대기질 변화")
                st.line_chart(df['pm25Value'])

        else:
            st.error("대기질 데이터를 찾을 수 없습니다.")
        
    except ValueError as e:
        st.error(f"응답 데이터 형식에 오류가 발생했습니다: {e}")
else:
    st.error(f"API 요청에 실패했습니다. 상태 코드: {res.status_code}")
