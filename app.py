import streamlit as st
from google import genai
import pandas as pd
import os
import random
from datetime import datetime

# --- [1. 경로 및 설정] ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_PATH = os.path.join(BASE_DIR, "unnamed.jpg")
BOARD_PATH = os.path.join(BASE_DIR, "gion_board.csv")
FISHING_LOG = os.path.join(BASE_DIR, "fishing_draft.csv")

# ★ 스님의 API 키를 여기에 한 번만 입력해두세요 ★
MY_API_KEY = "AIzaSyB7iiGWtoHPALlcH6RFOB6JDPzjGXbAMII" 

# --- [2. 디자인: 녹색(#2E7D32), 주황(#EF6C00), 유튜브 빨강(#FF0000)] ---
st.set_page_config(page_title="온라인 기원정사", layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nanum+Myeongjo:wght@700&display=swap');
    html, body, [class*="css"] { font-family: 'Nanum Myeongjo', serif; background-color: #FDFBF7; }
    
    /* 중앙 현판 디자인 */
    .plaque { background-color: #2E7D32; color: #EF6C00; padding: 40px; border-radius: 20px; border: 10px double #EF6C00; text-align: center; margin-bottom: 20px; }
    
    /* 일반 버튼 (녹색) */
    .stButton>button { height: 100px !important; font-size: 2rem !important; background-color: #2E7D32 !important; color: white !important; border: 4px solid #EF6C00 !important; border-radius: 20px !important; width: 100%; font-weight: bold; }
    
    /* ★ 유튜브 전용 빨간색 버튼 ★ */
    .stLinkButton>a { 
        height: 100px !important; font-size: 2rem !important; 
        background-color: #FF0000 !important; color: white !important; 
        border: 4px solid #FFFFFF !important; border-radius: 20px !important; 
        width: 100%; display: flex; align-items: center; justify-content: center; text-decoration: none !important; font-weight: bold;
    }
    
    .wisdom-box { background-color: #F8F4E3; padding: 30px; border-left: 15px solid #2E7D32; border-radius: 10px; font-size: 1.8rem; line-height: 2.2; color: #2C2C2C; }
    </style>
    """, unsafe_allow_html=True)

def safe_load(path, columns):
    try:
        if os.path.exists(path) and os.path.getsize(path) > 0: return pd.read_csv(path)
    except: pass
    return pd.DataFrame(columns=columns)

def go_fishing():
    try:
        client = genai.Client(api_key=MY_API_KEY)
        site = random.choice(["SuttaCentral", "CBETA", "동국대 학술원", "84000: Buddha Words"])
        topic = random.choice(["위로", "용기", "무소유", "자비"])
        res = client.models.generate_content(model='gemini-flash-latest', contents=f"당신은 불교 전문가입니다. '{site}'를 참고하여 '{topic}'에 관한 짧은 경전 구절과 윤월 스님 말투의 현대어 해설을 작성하세요.")
        df = safe_load(FISHING_LOG, ["날짜", "출처", "주제", "내용"])
        new_fish = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d"), site, topic, res.text]], columns=["날짜", "출처", "주제", "내용"])
        pd.concat([new_fish, df]).to_csv(FISHING_LOG, index=False, encoding='utf-8-sig')
        return f"성공: {site}에서 지혜를 낚았습니다!"
    except Exception as e: return f"낚시 실패: {e}"

if 'step' not in st.session_state: st.session_state.step = 'home'
def move_to(target): st.session_state.step = target; st.rerun()

# --- [3. 사이드바 메뉴] ---
with st.sidebar:
    st.markdown("<h1 style='color: #2E7D32;'>🏯 기원정사</h1>", unsafe_allow_html=True)
    if st.button("🏠 처음으로 (일주문)"): move_to('home')
    if st.button("📜 스님 인사말"): move_to('intent')
    if st.button("🕯️ 즉문즉설 (상담)"): move_to('consult')
    if st.button("🍵 지대방 (게시판)"): move_to('jidaebang')
    st.divider()
    admin_pw = st.text_input("㊙️ 관리자 암호:", type="password")
    if admin_pw == "1080":
        if st.button("🎣 비밀 낚시터"): move_to('admin_fish')

# --- [4. 본 화면 구성] ---
if st.session_state.step == 'home':
    st.markdown('<div class="plaque"><h1>🏯 온라인 기원정사</h1><p style="font-size:1.5rem;">지혜의 무인 등대</p></div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏮 도량 입성하기"): move_to('intent')
    with col2:
        st.link_button("📺 유튜브 바로가기", "https://www.youtube.com/channel/UCqszikE30Jzc5pMXS8YWuQw")
    if os.path.exists(IMAGE_PATH): st.image(IMAGE_PATH, width='stretch')

elif st.session_state.step == 'intent':
    st.markdown('<div class="plaque"><h1>📜 윤월 스님 인사말</h1></div>', unsafe_allow_html=True)
    st.markdown('<div class="wisdom-box"><b>"반갑습니다. 기원정사 주지 윤월입니다."</b><br><br>세상이 소란하고 마음 둘 곳 없을 때, 언제든 찾아와 지혜의 등불을 켤 수 있는 무인 도량을 세웠습니다. 유니가 전하는 화엄경의 지혜로 잠시나마 평온을 찾으시길 발원합니다.</div>', unsafe_allow_html=True)
    if st.button("🧘 고민 상담하러 가기"): move_to('consult')

elif st.session_state.step == 'consult':
    st.markdown('<div class="plaque"><h1>🕯️ 자비의 즉문즉설</h1></div>', unsafe_allow_html=True)
    user_story = st.text_area("🧘 고민을 남겨주시면 윤월 스님의 지혜를 전해드립니다:", height=200)
    if st.button("🕯️ 지혜 답변 도출하기"):
        if user_story:
            with st.spinner("유니가 지혜를 길어오는 중..."):
                try:
                    client = genai.Client(api_key=MY_API_KEY)
                    res = client.models.generate_content(model='gemini-flash-latest', contents=f"당신은 윤월 스님입니다. 화엄경의 지혜로 답하세요: {user_story}")
                    st.markdown(f'<div class="wisdom-box">{res.text}</div>', unsafe_allow_html=True)
                except: st.error("🏮 현재 접속자가 많습니다. 잠시 후 다시 시도해 주세요.")
        else: st.warning("고민 내용을 먼저 적어주세요.")

elif st.session_state.step == 'jidaebang':
    st.markdown('<div class="plaque"><h1>🍵 지대방 (자유게시판)</h1></div>', unsafe_allow_html=True)
    with st.expander("✍️ 안부 남기기"):
        name = st.text_input("이름:", value="익명")
        msg = st.text_area("내용:")
        if st.button("📤 올리기"):
            df = safe_load(BOARD_PATH, ["날짜", "작성자", "내용"])
            pd.concat([pd.DataFrame([[datetime.now().strftime("%Y-%m-%d"), name, msg]], columns=["날짜", "작성자", "내용"]), df]).to_csv(BOARD_PATH, index=False, encoding='utf-8-sig')
            st.rerun()
    df = safe_load(BOARD_PATH, ["날짜", "작성자", "내용"])
    for _, row in df.iterrows():
        st.markdown(f"**{row['작성자']}** ({row['날짜']})")
        st.info(row['내용'])

elif st.session_state.step == 'admin_fish':
    st.markdown('<div class="plaque"><h1>🎣 비밀 낚시 기록부</h1></div>', unsafe_allow_html=True)
    st.write("스님, 일주일간 낚인 지혜를 확인해 보세요.")
    if st.button("🌊 지금 낚시 던지기"): st.toast(go_fishing())
    st.divider()
    fish_df = safe_load(FISHING_LOG, ["날짜", "출처", "주제", "내용"])
    if not fish_df.empty:
        for _, row in fish_df.iterrows():
            with st.expander(f"📌 {row['날짜']} | {row['출처']}"): st.write(row['내용'])
        if st.button("🗑️ 기록부 비우기"): os.remove(FISHING_LOG); st.rerun()
    else: st.info("아직 낚인 지혜가 없습니다.")