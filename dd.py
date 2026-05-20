import random
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# ==========================================
# [백엔드] 1. 감정 키워드 및 노래 데이터베이스
# ==========================================
MUSIC_DATABASE = {
    "기쁨/행복": [
        {"title": "Dynamite", "artist": "BTS", "url": "https://www.youtube.com/results?search_query=BTS+Dynamite"},
        {"title": "New Jeans", "artist": "NewJeans", "url": "https://www.youtube.com/results?search_query=NewJeans+New+Jeans"},
        {"title": "도도독", "artist": "르세라핌", "url": "https://www.youtube.com/results?search_query=LE+SSERAFIM+Perfect+Night"}
    ],
    "지침/위로": [
        {"title": "수고했어, 오늘도", "artist": "옥상달빛", "url": "https://www.youtube.com/results?search_query=옥상달빛+수고했어오늘도"},
        {"title": "한숨", "artist": "이하이", "url": "https://www.youtube.com/results?search_query=이하이+한숨"},
        {"title": "서른즈음에", "artist": "김광석", "url": "https://www.youtube.com/results?search_query=김광석+서른즈음에"}
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
    """사용자가 입력한 문장에서 키워드를 찾아 감정을 분석합니다."""
    if any(word in text for word in ["힘들다", "지친다", "피곤", "피곤해", "고생", "바빴다"]):
        return "지침/위로"
    elif any(word in text for word in ["슬프다", "우울", "눈물", "외롭다", "짜증"]):
        return "우울/슬픔"
    elif any(word in text for word in ["좋다", "행복", "기쁘다", "최고", "신나", "웃음"]):
        return "기쁨/행복"
    else:
        return "평온/일상"

# ==========================================
# [프론트엔드] 2. HTML/CSS/JS (UI 화면 디자인)
# ==========================================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>오늘의 한 줄, 오늘의 노래</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%); }
    </style>
</head>
<body class="text-slate-100 min-h-screen flex items-center justify-center font-sans px-4">

    <div class="max-w-md w-full p-6 bg-slate-800/80 backdrop-blur-md rounded-2xl shadow-2xl border border-slate-700/50">
        <h1 class="text-2xl font-bold text-center mb-2 text-indigo-400">🌙 하루 끝, 음악 처방</h1>
        <p class="text-sm text-slate-400 text-center mb-6">오늘 하루는 어땠나요? 짧은 한 줄로 기록해보세요.</p>
        
        <div class="mb-4">
            <textarea id="diaryInput" rows="3" 
                class="w-full p-3 bg-slate-900/50 border border-slate-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-indigo-500 placeholder-slate-500 resize-none transition" 
                placeholder="오늘 너무 피곤했지만 보람찬 하루였다..."></textarea>
        </div>
        
        <button onclick="getRecommendation()" 
            class="w-full bg-indigo-600 hover:bg-indigo-500 text-white font-semibold py-3 px-4 rounded-lg transition duration-200 active:scale-[0.98]">
            오늘의 노래 추천받기
        </button>

        <div id="resultBox" class="mt-6 p-5 bg-slate-900/60 border border-indigo-500/30 rounded-xl hidden transition-all duration-300">
            <p class="text-xs text-indigo-300 font-semibold uppercase tracking-wider">
                오늘의 감정 상태: <span id="emotionResult" class="text-white bg-indigo-900/50 px-2 py-0.5 rounded ml-1"></span>
            </p>
            <div class="mt-4 border-l-4 border-indigo-500 pl-3">
                <h3 id="songTitle" class="text-lg font-bold text-white"></h3>
                <p id="songArtist" class="text-sm text-slate-400 mt-0.5"></p>
            </div>
            <a id="songLink" href="#" target="_blank" 
                class="mt-4 inline-block text-sm text-indigo-400 hover:text-indigo-300 font-medium transition">
                👉 YouTube에서 검색 결과 보기
            </a>
        </div>
    </div>

    <script>
        async function getRecommendation() {
            const text = document.getElementById('diaryInput').value;
            if (!text.trim()) {
                alert('오늘의 문장을 입력해주세요!');
                return;
            }

            try {
                const response = await fetch('/recommend', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text: text })
                });

                if (response.ok) {
                    const data = await response.json();
                    document.getElementById('emotionResult').innerText = data.emotion;
                    document.getElementById('songTitle').innerText = data.title;
                    document.getElementById('songArtist').innerText = data.artist;
                    document.getElementById('songLink').href = data.url;
                    
                    const resultBox = document.getElementById('resultBox');
                    resultBox.classList.remove('hidden');
                } else {
                    alert('서버 응답에 문제가 있습니다.');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('연결에 실패했습니다.');
            }
        }
    </script>
</body>
</html>
"""

# ==========================================
# [라우팅] 3. Flask 웹 서버 URL 매핑
# ==========================================
@app.route('/')
def home():
    # 외부 파일 없이 스트링 형태의 HTML을 바로 렌더링합니다.
    return render_template_string(HTML_TEMPLATE)

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json or {}
    diary_text = data.get("text", "")
    
    if not diary_text.strip():
        return jsonify({"error": "문장이 비어있습니다."}), 400
    
    emotion = analyze_emotion(diary_text)
    song_list = MUSIC_DATABASE.get(emotion, MUSIC_DATABASE["평온/일상"])
    recommended_song = random.choice(song_list)
    
    return jsonify({
        "emotion": emotion,
        "title": recommended_song["title"],
        "artist": recommended_song["artist"],
        "url": recommended_song["url"]
    })

if __name__ == '__main__':
    # 로컬에서 테스트할 때 웹 서버를 실행합니다.
    app.run(host='0.0.0.0', port=5000, debug=True)
