import streamlit as st
import random
import time

st.set_page_config(
    page_title="3Rs MATH",
    page_icon="🧮",
    layout="wide"
)

st.title("🧮 3Rs MATH")
st.write("Jawab sebanyak mungkin soal matematika!")

# =========================
# SESSION STATE
# =========================

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

if "selected_answer" not in st.session_state:
    st.session_state.selected_answer = None

# untuk Addition Table interaktif
if "selected_row" not in st.session_state:
    st.session_state.selected_row = None

if "selected_col" not in st.session_state:
    st.session_state.selected_col = None

# =========================
# LEVEL
# =========================

level = st.selectbox(
    "Pilih Level",
    ["Rasasti", "Rinjani", "Rajanti"]
)

# =========================
# GENERATE QUESTION
# =========================

def generate_question(level):

    if level == "Rasasti":

        a = random.randint(1, 10)
        b = random.randint(1, 10)
        op = "+"

    elif level == "Rinjani":

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


# =========================
# NEW QUESTION
# =========================

if st.session_state.question is None:
    st.session_state.question, st.session_state.answer = generate_question(level)

# =========================
# SIDEBAR
# =========================

st.sidebar.header("🏆 Statistik")

st.sidebar.metric(
    "Skor",
    st.session_state.score
)

st.sidebar.metric(
    "Soal Dijawab",
    st.session_state.questions_answered
)

elapsed = int(
    time.time() -
    st.session_state.start_time
)

st.sidebar.metric(
    "Waktu Bermain",
    f"{elapsed} detik"
)

# =========================
# RASASTI
# =========================

if level == "Rasasti":

    left, right = st.columns([1, 1.4])

    with left:

        st.subheader("Soal")

        st.markdown(
            f"""
            <h1 style='text-align:center'>
            {st.session_state.question}
            </h1>
            """,
            unsafe_allow_html=True
        )

        st.write("### Pilih Jawaban")

        numbers = list(range(1, 21))

        for row in range(2):

            cols = st.columns(10)

            for col in range(10):

                num = numbers[row * 10 + col]

                with cols[col]:

                    if st.button(
                        str(num),
                        key=f"btn_{num}"
                    ):
                        st.session_state.selected_answer = num

        user_answer = st.session_state.selected_answer

        if user_answer is not None:

            st.success(
                f"Pilihan: {user_answer}"
            )

    with right:

        st.subheader("📘 Tabel Penjumlahan Interaktif")
    
        html = """
        <style>
        table{
            border-collapse:collapse;
            margin:auto;
        }
    
        td{
            border:1px solid #444;
            width:40px;
            height:40px;
            text-align:center;
            font-size:18px;
        }
    
        .head{
            background:#bdf5a7;
            font-weight:bold;
        }
    
        .rowselected{
            background:#7ee081;
            font-weight:bold;
        }
    
        .colselected{
            background:#7ee081;
            font-weight:bold;
        }
    
        .answer{
            background:yellow;
            font-weight:bold;
            font-size:24px;
        }
        </style>
        """
    
        # Header kolom
        cols = st.columns(11)
    
        cols[0].write("➕")
    
        for c in range(1,11):
    
            with cols[c]:
    
                if st.button(
                    str(c),
                    key=f"col_{c}"
                ):
                    st.session_state.selected_col = c
    
        # Baris tabel
    
        for r in range(1,11):
    
            cols = st.columns(11)
    
            with cols[0]:
    
                if st.button(
                    str(r),
                    key=f"row_{r}"
                ):
                    st.session_state.selected_row = r
    
            for c in range(1,11):
    
                value = r + c
    
                cell_style = ""
    
                if (
                    r == st.session_state.selected_row and
                    c == st.session_state.selected_col
                ):
                    cell_style = (
                        "background:yellow;"
                        "font-weight:bold;"
                        "font-size:24px;"
                    )
    
                elif (
                    r == st.session_state.selected_row or
                    c == st.session_state.selected_col
                ):
                    cell_style = (
                        "background:#bdf5a7;"
                    )
    
                cols[c].markdown(
                    f"""
                <div style='
                border:1px solid gray;
                text-align:center;
                padding:8px;
                {cell_style}
                '>
                {value}
                </div>
                """,
                    unsafe_allow_html=True
                )
# =========================
# RINJANI & RAJANTI
# =========================

else:

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

# =========================
# BUTTONS
# =========================

col1, col2 = st.columns(2)

with col1:

    if st.button("✅ Cek Jawaban"):

        correct = float(
            st.session_state.answer
        )

        try:

            if abs(float(user_answer) - correct) < 0.1:

                st.success(
                    "Hebat! Jawaban benar 🎉"
                )

                st.balloons()

                st.session_state.score += 10

            else:

                st.error(
                    f"Belum tepat. Jawaban yang benar adalah {correct}"
                )

        except:
            st.warning(
                "Pilih atau masukkan jawaban terlebih dahulu."
            )

        st.session_state.questions_answered += 1

with col2:

    if st.button("➡️ Soal Berikutnya"):

        st.session_state.question, \
        st.session_state.answer = generate_question(level)

        st.session_state.selected_answer = None

        st.rerun()

# =========================
# REWARD
# =========================

if st.session_state.score >= 100:

    st.success(
        "🏅 Luar biasa! Kamu Math Champion!"
    )

elif st.session_state.score >= 50:

    st.info(
        "⭐ Hebat! Terus berlatih!"
    )

elif st.session_state.score >= 20:

    st.info(
        "👍 Bagus! Kamu makin pintar!"
    )
