import streamlit as st
import random
import time

st.set_page_config(
    page_title="Math Adventure",
    page_icon="🧮",
    layout="centered"
)

st.title("🧮 Math Adventure")
st.write("Jawab sebanyak mungkin soal matematika!")

# Inisialisasi session state
if "score" not in st.session_state:
    st.session_state.score = 0

if "question" not in st.session_state:
    st.session_state.question = None

if "answer" not in st.session_state:
    st.session_state.answer = None

if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

if "questions_answered" not in st.session_state:
    st.session_state.questions_answered = 0

# Pilih level
level = st.selectbox(
    "Pilih Level",
    ["Mudah", "Sedang", "Sulit"]
)

def generate_question(level):

    if level == "Mudah":
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        op = random.choice(["+", "-"])

    elif level == "Sedang":
        a = random.randint(10, 50)
        b = random.randint(1, 20)
        op = random.choice(["+", "-", "*"])

    else:
        a = random.randint(10, 100)
        b = random.randint(1, 20)
        op = random.choice(["+", "-", "*", "/"])

    if op == "+":
        ans = a + b

    elif op == "-":
        ans = a - b

    elif op == "*":
        ans = a * b

    else:
        ans = round(a / b, 1)

    return f"{a} {op} {b}", ans

# Buat soal baru
if st.session_state.question is None:
    st.session_state.question, st.session_state.answer = generate_question(level)

# Sidebar
st.sidebar.header("🏆 Statistik")
st.sidebar.metric("Skor", st.session_state.score)
st.sidebar.metric("Soal Dijawab", st.session_state.questions_answered)

elapsed = int(time.time() - st.session_state.start_time)
st.sidebar.metric("Waktu Bermain", f"{elapsed} detik")

# Soal
st.subheader("Soal")

st.markdown(
    f"""
    <h1 style='text-align:center'>
    {st.session_state.question}
    </h1>
    """,
    unsafe_allow_html=True
)

user_answer = st.number_input(
    "Jawabanmu",
    step=0.1,
    format="%.1f"
)

col1, col2 = st.columns(2)

with col1:
    if st.button("✅ Cek Jawaban"):

        correct = float(st.session_state.answer)

        if abs(user_answer - correct) < 0.1:

            st.success("Hebat! Jawaban benar 🎉")
            st.balloons()
            st.session_state.score += 10

        else:
            st.error(
                f"Belum tepat. Jawaban yang benar adalah {correct}"
            )

        st.session_state.questions_answered += 1

with col2:
    if st.button("➡️ Soal Berikutnya"):

        st.session_state.question, \
        st.session_state.answer = generate_question(level)

        st.rerun()

# Reward
if st.session_state.score >= 100:
    st.success("🏅 Luar biasa! Kamu Math Champion!")

elif st.session_state.score >= 50:
    st.info("⭐ Hebat! Terus berlatih!")

elif st.session_state.score >= 20:
    st.info("👍 Bagus! Kamu makin pintar!")
