import streamlit as st
import requests  # supabase орнына осыны қолданамыз

# БАПТАУЛАР (Өз мәліметтеріңізді қойыңыз)
URL = "https://iuqdbdvmbewaedgydaah.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml1cWRiZHZtYmV3YWVkZ3lkYWFoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjkzMjE5ODgsImV4cCI6MjA4NDg5Nzk4OH0.a_PPVZWcA3qOfT4cNaXNE_a3xuSv0CHyrY8LbTgjWww" # Скриншоттағы кілт

def post_to_supabase(data):
    # Бұл функция базаға жауапты сақтайды
    headers = {
        "apikey": KEY,
        "Authorization": f"Bearer {KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }
    return requests.post(f"{URL}/rest/v1/bjb_results", json=data, headers=headers)

# --- ИНТЕРФЕЙС ---
st.title("📝 БЖБ: Динамика негіздері")
st.sidebar.header("Оқушы мәліметі")
student_name = st.sidebar.text_input("Аты-жөніңіз:")
student_class = st.sidebar.selectbox("Сыныбыңыз:", ["9 A", "9 Ә", "9 Б", "9 В"])

# Тапсырмалар
student_answers = {}
for i in [1, 2, 3]:
    student_answers[i] = st.text_area(f"{i}-тапсырма жауабы:", key=f"ans_{i}")

if st.button("Жұмысты тапсыру ✅"):
    if not student_name:
        st.error("Аты-жөніңізді жазыңыз!")
    else:
        data = {
            "student_name": student_name,
            "student_class": student_class,
            "answers": student_answers,
            "status": "pending"
        }
        res = post_to_supabase(data)
        if res.status_code in [200, 201]:
            st.success(f"Рахмет, {student_name}! Жұмыс қабылданды.")
        else:
            st.error(f"Қате орын алды: {res.text}")

st.markdown("---")
st.subheader("🔎 Нәтижеңді іздеу")
search = st.text_input("Аты-жөніңді жаз:")
if search:
    headers = {"apikey": KEY, "Authorization": f"Bearer {KEY}"}
    # Базадан іздеу
    res = requests.get(f"{URL}/rest/v1/bjb_results?student_name=eq.{search}&select=*", headers=headers)
    if res.status_code == 200 and res.json():
        job = res.json()[-1]
        st.info(f"Статус: {job['status']}")
        st.markdown(f"**AI Жауабы:**\n\n{job['ai_feedback']}")
    else:
        st.info("Әзірге жұмыс табылмады.")