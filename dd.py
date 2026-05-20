import random
import os
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

MUSIC_DATABASE = {
    "기쁨/행복": [
        {"title": "Dynamite", "artist": "BTS", "url": "https://www.youtube.com/results?search_query=BTS+Dynamite"},
        {"title": "New Jeans", "artist": "NewJeans", "url": "https://www.youtube.com/results?search_query=NewJeans+New+Jeans"}
    ],
    "지침/위로": [
        {"title": "수고했어, 오늘도", "artist": "옥상달빛", "url": "https://www.youtube.com/results?search_query=옥상달빛+수고했어오늘도"},
        {"title": "한숨", "artist": "이하이", "url": "https://www.youtube.com/results?search_query=이하이+한숨"}
    ],
    "우울/슬픔": [
        {"title": "비도 오고 그래서", "artist": "헤이즈", "url": "https://www.youtube.com/results?search_query=헤이즈+비도오고그래서"}
    ],
    "평온/일상": [
        {"title": "밤편지", "artist": "아이유", "url": "https://www.youtube.com/results?search_query=아이유+밤편지"}
    ]
}

def analyze_emotion(text):
    if any(word in text for word in ["힘들다", "지친다", "피곤", "고생", "지침"]):
        return "지침/위로"
    elif any(word in text for word in ["슬프다", "우울", "눈물", "외롭다"]):
        return "우울/슬픔"
    elif any(word in text for word in ["좋다", "행복", "기쁘다", "신나"]):
        return "기쁨/행복"
    else:
        return "평온/일상"

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>오늘의 노래</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-900 text-white min-h-screen flex items-center justify-center">
    <div class="max-w-md w-full p-6 bg-slate-800 rounded-2xl shadow-xl">
        <h1 class="text-2xl font-bold text-center mb-4 text-indigo-400">🌙 하루 끝, 음악 처방</h1>
        <textarea id="diaryInput" rows="3" class="w-full p-3 bg-slate-700 rounded-lg text-white resize-none" placeholder="오늘 하루는 어땠나요?"></textarea>
        <button onclick="getRecommendation()" class="w-full bg-indigo-600 hover:bg-indigo-500 py-3 rounded-lg mt-4 font-semibold">추천 노래 받기</button>
        <div id="resultBox" class="mt-6 p-4 bg-slate-900 rounded-xl hidden">
            <p class="text-sm text-indigo-300">감정: <span id="emotionResult"></span></p>
            <h3 id="songTitle" class="text-lg font-bold mt-2"></h3>
            <p id="songArtist" class="text-sm text-slate-400"></p>
            <a id="songLink" href="#" target="_blank" class="text-indigo-400 block mt-2 text-sm hover:underline">👉 들어보기</a>
        </div>
    </div>
    <script>
        async function getRecommendation() {
            const text = document.getElementById('diaryInput').value;
            if(!text.trim()) return;
            const res = await fetch('/recommend', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({text})
            });
            if(res.ok) {
                const data = await res.json();
                document.getElementById('emotionResult').innerText = data.emotion;
                document.getElementById('songTitle').innerText = data.title;
                document.getElementById('songArtist').innerText = data.artist;
                document.getElementById('songLink').href = data.url;
                document.getElementById('resultBox').classList.remove('hidden');
            }
        }
    </script>
</body>
</html>"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json or {}
    diary_text = data.get("text", "")
    emotion = analyze_emotion(diary_text)
    song = random.choice(MUSIC_DATABASE.get(emotion, MUSIC_DATABASE["평온/일상"]))
    return jsonify({
        "emotion": emotion,
        "title": song["title"],
        "artist": song["artist"],
        "url": song["url"]
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8501))
    app.run(host='0.0.0.0', port=port, debug=False)
