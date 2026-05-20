import streamlit as st
import random

# 페이지 기본 설정
st.set_page_config(page_title="하루 끝, 음악 처방", page_icon="🌙", layout="centered")

# 감정 키워드 및 노래 데이터베이스
MUSIC_DATABASE = {
    "기쁨/행복": [
        {"title": "Dynamite", "artist": "BTS", "url": "https://www.youtube.com/results?search_query=BTS+Dynamite"},
        {"title": "New Jeans", "artist": "NewJeans", "url": "https://www.youtube.com/results?search_query=NewJeans+New+Jeans"},
        {"title": "Perfect Night", "artist": "르세라핌", "url": "https://www.youtube.com/results?search_query=LE+SSERAFIM+Perfect+Night"}
    ],
    "지침/위로": [
        {"title": "수고했어, 오늘도", "artist": "옥상달빛", "url": "https://www.youtube.com/results?search_query=옥상달빛+수고했어오늘도"},
        {"title": "한숨", "artist": "이하이", "url": "https://www.youtube.com/results?search_query=이하이+한숨"},
        {"title": "서른 즈음에", "artist": "김광석", "url": "https://www.youtube.com/results?search_query=김광석+서른즈음에"}
    ],
    "우울/슬픔": [
        {"title": "비도 오고 그래서", "artist": "헤이즈", "url": "https://www.youtube.com/results?search_query=헤이즈+비도오고그래서"},
        {"title": "정거장", "artist": "아이유", "url": "https://www.youtube.com/results?search_query=아이유+정거장"},
        {"title": "그때 헤어지면 돼", "artist": "로이킴", "url": "https://www.youtube.com/results?search_query=로이킴+그때헤어지면돼"}
    ],
    "평온/일상": [
        {"title": "밤편지", "artist": "아이유", "url": "https://www.youtube.com/results?search_query=아이유+밤편지"},
        {"title": "주저하는 연인들을 위해", "artist": "잔나비", "url": "https://www.youtube.com/results?search_query=잔나비+주저하는연인들을위해"},
        {"title": "사랑은 은하수 다방에서", "artist": "10cm", "url": "https://www.youtube.com/results?search_query=10cm+사랑은은하수다방에서"}
    ]
}

def analyze_emotion(text):
    if any(word in text for word in ["힘들다", "지친다", "피곤", "피곤해", "고생", "바빴다", "지침"]):
        return "지침/위로"
    elif any(word in text for word in ["슬프다", "우울", "눈물", "외롭다", "짜증", "화나"]):
        return "우울/슬픔"
    elif any(word in text for word in ["좋다", "행복", "기쁘다", "최고", "신나", "웃음"]):
        return "기쁨/행복"
    else:
        return "평온/일상"

# --- 화면 UI 디자인 ---
st.title("🌙 하루 끝, 음악 처방")
st.caption("오늘 하루는 어땠나요? 짧은 한 줄로 기록해보세요.")

# 사용자 입력창
diary_text = st.text_area("오늘의 한 줄 일기", placeholder="오늘 너무 피곤했지만 보람찬 하루였다...", label_visibility="collapsed")

# 버튼 클릭 시 로직 실행
if st.button("오늘의 노래 추천받기", use_container_width=True):
    if not diary_text.strip():
        st.warning("오늘의 문장을 입력해주세요!")
    else:
        emotion = analyze_emotion(diary_text)
        song_list = MUSIC_DATABASE.get(emotion, MUSIC_DATABASE["평온/일상"])
        recommended_song = random.choice(song_list)
        
        # 결과 디자인 출력
        st.success(f"오늘의 감정 상태: **{emotion}**")
        
        st.markdown(f"""
        ### 🎵 {recommended_song['title']}
        **아티스트:** {recommended_song['artist']}
        
        [👉 YouTube에서 검색 결과 보기]({recommended_song['url']})
        """)
