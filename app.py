import streamlit as st
import random
import time
from datetime import datetime, timezone
from supabase import create_client, Client

st.set_page_config(page_title="UFO HACK NÃO", page_icon="🛸", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Inter:wght@400;600;800&display=swap');
.stApp{background:radial-gradient(ellipse at top,#17275b 0%,#080d22 52%,#03050e 100%);color:#f3f7ff}
[data-testid="stHeader"]{background:transparent}
.block-container{max-width:1200px;padding-top:1rem}
h1,h2,h3{font-family:Orbitron,sans-serif!important}
.ufo-title{text-align:center;font-family:Orbitron,sans-serif;font-size:clamp(2rem,5vw,4rem);font-weight:900;color:#8af8ff;text-shadow:0 0 12px #2beaff,0 0 32px #7d50ff}
.ufo-sub{text-align:center;color:#c8d4ff;margin-bottom:1.4rem}
div.stButton>button{width:100%;border-radius:12px;border:1px solid #67f5ff;background:linear-gradient(90deg,#2662b9,#743dd1);color:white;font-weight:800;min-height:2.7rem}
.panel{background:linear-gradient(135deg,rgba(28,44,95,.88),rgba(13,18,48,.92));border:1px solid rgba(103,245,255,.4);border-radius:18px;padding:16px}
div[data-testid="stTextInput"] input{border-radius:10px}
@keyframes floaty{0%,100%{transform:translateY(0) rotate(-3deg)}50%{transform:translateY(-15px) rotate(3deg)}}
.ufo{font-size:64px;text-align:center;animation:floaty 2s ease-in-out infinite;filter:drop-shadow(0 0 18px #6ef5ff)}
</style>
<div class="ufo-title">🛸 UFO HACK NÃO</div>
<div class="ufo-sub">PHÒNG CHUNG • GỌI PHI HÀNH GIA • GIẢI MÃ • BẢNG XẾP HẠNG</div>
""", unsafe_allow_html=True)

st.sidebar.header("⚙️ Cài đặt")
max_players = st.sidebar.slider("Giới hạn người chơi", 2, 100, 40)
room_code = st.sidebar.text_input("Mã phòng", value="UFO2026", max_chars=20).strip().upper()
st.sidebar.caption("Tất cả người chơi cần nhập cùng mã phòng.")

@st.cache_resource
def get_supabase():
    try:
        url = st.secrets["supabase"]["url"]
        key = st.secrets["supabase"]["key"]
        return create_client(url, key)
    except Exception:
        return None

sb = get_supabase()

if not sb:
    st.error("Chưa kết nối Supabase. Hãy tạo .streamlit/secrets.toml theo mẫu trong README, sau đó thêm URL và anon key của dự án Supabase.")
    st.code('[supabase]\nurl = "https://YOUR_PROJECT.supabase.co"\nkey = "YOUR_SUPABASE_ANON_KEY"', language="toml")
    st.stop()

def rows(table, **filters):
    q = sb.table(table).select("*")
    for k,v in filters.items():
        q = q.eq(k,v)
    return q.execute().data or []

def upsert(table, data, on_conflict=None):
    q = sb.table(table).upsert(data, on_conflict=on_conflict) if on_conflict else sb.table(table).upsert(data)
    return q.execute().data

def update(table, data, **filters):
    q = sb.table(table).update(data)
    for k,v in filters.items(): q=q.eq(k,v)
    return q.execute().data

def delete(table, **filters):
    q=sb.table(table).delete()
    for k,v in filters.items(): q=q.eq(k,v)
    return q.execute().data

# Ensure room row exists

def get_supabase():
    try:
        url = st.secrets["supabase"]["url"].strip()
        key = st.secrets["supabase"]["key"].strip()

        if not url.startswith("https://"):
            raise ValueError("URL Supabase phải bắt đầu bằng https://")

        if "/rest/v1" in url:
            raise ValueError(
                "URL không được có /rest/v1 ở cuối. "
                "Hãy dùng URL gốc của dự án."
            )

        return create_client(url, key)

    except Exception as e:
        st.error(f"Lỗi kết nối Supabase: {type(e).__name__}: {e}")
        return None


sb = get_supabase()

if not sb:
    st.stop()


st.markdown(f'<div class="panel">🌐 <b>MÃ PHÒNG:</b> {room_code}　　👥 <b>GIỚI HẠN:</b> {max_players} người</div>', unsafe_allow_html=True)
st.write("")

tab_play, tab_teacher, tab_board, tab_help = st.tabs(["🧑‍🚀 Vào chơi", "🧑‍🏫 Giáo viên", "🏆 Bảng xếp hạng", "ℹ️ Hướng dẫn"])

with tab_play:
    players = rows("players", room_code=room_code)
    with st.container(border=True):
        st.subheader("Đăng ký phi hành gia")
        name = st.text_input("Tên hiển thị", key="player_name", max_chars=24, placeholder="Ví dụ: Minh Anh")
        role = st.radio("Bạn là", ["Học sinh", "Giáo viên"], horizontal=True)
        if st.button("🚀 VÀO PHÒNG"):
            if not name.strip():
                st.warning("Nhập tên trước nhé.")
            elif role == "Học sinh" and len(players) >= max_players and not any(p.get("name")==name.strip() for p in players):
                st.error("Phòng đã đủ người. Giáo viên có thể tăng giới hạn ở thanh bên.")
            else:
                existing = next((p for p in players if p["name"].lower()==name.strip().lower()), None)
                pid = existing["id"] if existing else f"{int(time.time()*1000)}-{random.randint(100,999)}"
                data={"id":pid,"room_code":room_code,"name":name.strip(),"role":role,"score":existing.get("score",0) if existing else 0,"joined_at":datetime.now(timezone.utc).isoformat()}
                upsert("players",data,on_conflict="id")
                st.session_state["ufo_pid"]=pid
                st.session_state["ufo_name"]=name.strip()
                st.session_state["ufo_role"]=role
                st.success("Đã vào phòng! Hãy mở tab Giáo viên để bắt đầu câu hỏi.")
                st.rerun()
    if st.session_state.get("ufo_pid") and st.session_state.get("ufo_room", room_code)==room_code:
        st.session_state["ufo_room"]=room_code
        me=next((p for p in rows("players",room_code=room_code) if p["id"]==st.session_state["ufo_pid"]),None)
        if me:
            st.success(f"Xin chào {me['name']}! Điểm hiện tại: {me['score']}")
        roomdata=rows("rooms",code=room_code)
        roomdata=roomdata[0] if roomdata else {}
        called=next((p for p in rows("players",room_code=room_code) if p["id"]==roomdata.get("called_player_id")),None)
        st.markdown('<div class="ufo">🛸</div>',unsafe_allow_html=True)
        if called:
            st.markdown(f'<div class="panel" style="text-align:center;font-size:1.3rem">🛸 UFO đang gọi <b>{called["name"]}</b> lên giải mã!</div>',unsafe_allow_html=True)
        qid=roomdata.get("current_question_id")
        question=next((q for q in rows("questions",room_code=room_code) if q["id"]==qid),None) if qid else None
        if question and question.get("active",True):
            st.subheader(f"📡 Tín hiệu: {question['question']}")
            answered=rows("answers",question_id=question["id"],player_id=me["id"])
            if not answered:
                choice=st.radio("Chọn đáp án",question["options"],key=f"answer_{question['id']}_{me['id']}",index=None)
                if st.button("🔐 GỬI ĐÁP ÁN",key=f"send_{question['id']}"):
                    if choice is None: st.warning("Hãy chọn đáp án.")
                    else:
                        correct=choice==question["options"][int(question["correct_index"])]
                        upsert("answers",{"id":f"{question['id']}_{me['id']}","room_code":room_code,"question_id":question["id"],"player_id":me["id"],"player_name":me["name"],"choice":choice,"correct":correct,"created_at":datetime.now(timezone.utc).isoformat()},on_conflict="id")
                        if correct: update("players",{"score":int(me["score"])+10},id=me["id"])
                        st.success("Chính xác! +10 điểm." if correct else "Đã ghi nhận. Chưa chính xác nhé.")
                        st.rerun()
            else:
                st.info("Bạn đã gửi đáp án cho câu hỏi này. Xem bảng xếp hạng để theo dõi điểm.")
        if st.button("🔄 Làm mới dữ liệu"):
            st.rerun()
    else:
        st.info("Nhập tên và bấm VÀO PHÒNG. Tất cả người chơi cùng nhập một mã phòng.")

with tab_teacher:
    st.subheader("🧑‍🏫 Bảng điều khiển giáo viên")
    st.caption("Mẹo: vào phòng bằng vai trò Giáo viên để mở chức năng điều khiển.")
    if st.session_state.get("ufo_role") != "Giáo viên" or st.session_state.get("ufo_room") != room_code:
        st.warning("Hãy đăng ký vào phòng ở tab Vào chơi với vai trò Giáo viên trước.")
    else:
        current_players=rows("players",room_code=room_code)
        st.write(f"Đang có **{len(current_players)}** phi hành gia trong phòng.")
        st.markdown("#### Tạo câu đố")
        with st.form("new_question"):
            qtext=st.text_input("Nội dung câu hỏi")
            a1=st.text_input("Đáp án A")
            a2=st.text_input("Đáp án B")
            a3=st.text_input("Đáp án C")
            a4=st.text_input("Đáp án D")
            correct_label=st.selectbox("Đáp án đúng",["A","B","C","D"])
            submitted=st.form_submit_button("➕ Lưu câu hỏi")
            if submitted:
                opts=[a1.strip(),a2.strip(),a3.strip(),a4.strip()]
                if not qtext.strip() or any(not x for x in opts):
                    st.error("Điền đủ câu hỏi và 4 đáp án.")
                else:
                    qid=f"q-{int(time.time()*1000)}"
                    upsert("questions",{"id":qid,"room_code":room_code,"question":qtext.strip(),"options":opts,"correct_index":["A","B","C","D"].index(correct_label),"active":True,"created_at":datetime.now(timezone.utc).isoformat()})
                    st.success("Đã lưu câu hỏi.")
                    st.rerun()
        st.markdown("#### Gọi một học sinh")
        students=[p for p in current_players if p["role"]=="Học sinh"]
        if students:
            student_names={f'{p["name"]} (điểm {p["score"]})':p["id"] for p in students}
            selected=st.selectbox("Chọn phi hành gia",list(student_names))
            if st.button("🛸 GỌI UFO ĐẾN BẠN NÀY"):
                update("rooms",{"called_player_id":student_names[selected],"status":"playing"},code=room_code)
                st.success("Đã gọi! Các màn hình sẽ thấy tên người được gọi khi làm mới.")
        else:
            st.info("Chưa có học sinh nào vào phòng.")
        st.markdown("#### Phát câu hỏi cho cả phòng")
        questions=rows("questions",room_code=room_code)
        if questions:
            qlabels={f'{q["question"][:70]}':q["id"] for q in questions}
            selected_q=st.selectbox("Chọn câu hỏi để phát",list(qlabels))
            if st.button("📡 PHÁT CÂU HỎI"):
                update("rooms",{"current_question_id":qlabels[selected_q],"status":"playing"},code=room_code)
                st.success("Đã phát câu hỏi. Học sinh bấm Làm mới dữ liệu để thấy câu hỏi.")
        else:
            st.info("Chưa có câu hỏi. Tạo câu hỏi ở trên.")

with tab_board:
    st.subheader("🏆 Bảng xếp hạng phòng")
    board=sorted(rows("players",room_code=room_code),key=lambda p:int(p.get("score",0)),reverse=True)
    if board:
        for i,p in enumerate(board,1):
            medal="🥇" if i==1 else "🥈" if i==2 else "🥉" if i==3 else "👨‍🚀"
            st.markdown(f'<div class="panel" style="margin:.4rem 0;display:flex;justify-content:space-between"><span>{medal} <b>{i}. {p["name"]}</b></span><span>{p["score"]} điểm</span></div>',unsafe_allow_html=True)
    else: st.info("Chưa có điểm. Hãy vào phòng để bắt đầu.")

with tab_help:
    st.markdown("""
    **Cách chơi**
    1. Giáo viên tạo phòng bằng một mã phòng, ví dụ `UFO2026`.
    2. Học sinh mở cùng đường link, nhập đúng mã phòng và tên riêng.
    3. Giáo viên vào vai trò Giáo viên, tạo câu hỏi và phát câu hỏi.
    4. Giáo viên có thể chọn học sinh để UFO gọi lên.
    5. Đáp án đúng được cộng 10 điểm; bảng xếp hạng hiển thị theo điểm.

    **Lưu ý đồng bộ:** Đây là bản chia sẻ dữ liệu qua Supabase; người chơi cần bấm “Làm mới dữ liệu” để cập nhật ngay. Có thể bật tự làm mới từ menu Streamlit nếu muốn; realtime push chưa được cấu hình.
    """)
st.caption("UFO HACK NÃO • Bản phòng chung dùng Supabase")
