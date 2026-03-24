import streamlit as st
import random
import urllib.request
import xml.etree.ElementTree as ET

# -------------------------------
# 🎯 INITIAL STATE
# -------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "score" not in st.session_state:
    st.session_state.score = 0

if "asked" not in st.session_state:
    st.session_state.asked = []

if "current_q" not in st.session_state:
    st.session_state.current_q = None

if "last_input" not in st.session_state:
    st.session_state.last_input = ""

# -------------------------------
# 🎯 QUIZ DATA
# -------------------------------
quiz_questions = [
    {"q": "Who appoints the Chief Election Commissioner?",
     "options": ["President", "PM", "Parliament", "Supreme Court"],
     "ans": "President"},

    {"q": "Fundamental Rights are in which articles?",
     "options": ["12-35", "36-51", "51A", "370"],
     "ans": "12-35"},

    {"q": "Capital of India?",
     "options": ["Delhi", "Mumbai", "Chennai", "Kolkata"],
     "ans": "Delhi"},
]

# -------------------------------
# 📰 NEWS FUNCTION
# -------------------------------
def get_news():
    try:
        url = "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en"
        data = urllib.request.urlopen(url)
        root = ET.parse(data).getroot()

        items = root.findall(".//item")
        random.shuffle(items)

        news = "📰 Current Affairs:\n\n"
        for item in items[:5]:
            news += "👉 " + item.find("title").text + "\n"

        return news
    except:
        return "Unable to fetch news."

# -------------------------------
# 🎯 QUIZ FUNCTIONS
# -------------------------------
def start_quiz():
    remaining = [q for q in quiz_questions if q not in st.session_state.asked]

    if not remaining:
        st.session_state.asked = []
        remaining = quiz_questions

    q = random.choice(remaining)
    st.session_state.current_q = q
    st.session_state.asked.append(q)

    messages = ["🧠 Quiz Time!", q["q"]]

    for i, opt in enumerate(q["options"], 1):
        messages.append(f"{i}. {opt}")

    return messages

def check_answer(user_input):
    q = st.session_state.current_q
    if q:
        if user_input.lower() in q["ans"].lower():
            st.session_state.score += 1
            return f"🔥 Correct! Score: {st.session_state.score}"
        else:
            return f"❌ Wrong! Answer: {q['ans']} | Score: {st.session_state.score}"
    return None

# -------------------------------
# 💬 BOT LOGIC
# -------------------------------
def get_response(text):
    t = text.lower()

    ans = check_answer(text)
    if ans:
        return [ans]

    if "menu" in t:
        return ["""📚 MENU:
1. What is UPSC
2. Eligibility
3. Exam Pattern
4. Syllabus
5. Current Affairs
6. Quiz
"""]

    elif "hi" in t or "hello" in t:
        return ["Hi champ 😎 Ready to crack UPSC?"]

    elif "upsc" in t:
        return ["UPSC conducts Civil Services Exam for IAS, IPS, IFS."]

    elif "eligibility" in t:
        return ["Age: 21–32, Degree required, attempts vary by category."]

    elif "pattern" in t:
        return ["Prelims → Mains → Interview (Total 2025 marks)."]

    elif "syllabus" in t:
        return ["""📚 UPSC Syllabus:

1. History (Ancient, Medieval, Modern)
2. Polity (Constitution, Governance)
3. Geography (India & World)
4. Economy (Budget, Banking)
5. Environment (Ecology, Climate)
6. Science & Tech
7. Current Affairs
"""]

    elif "news" in t or "current" in t:
        return [get_news()]

    elif "quiz" in t:
        return start_quiz()

    else:
        return ["Try 'menu' champ 😉"]

# -------------------------------
# 🎨 UI
# -------------------------------
st.set_page_config(page_title="UPSC JARVIS 🤖")

st.title("UPSC JARVIS 🤖")

# Display chat
for msg in st.session_state.messages:
    st.write(msg)

# -------------------------------
# 💬 INPUT FORM (fixes duplicate issue)
# -------------------------------
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Ask something:")
    submit = st.form_submit_button("Send")

if submit and user_input.strip() != "" and user_input != st.session_state.last_input:
    st.session_state.last_input = user_input

    st.session_state.messages.append("🧑 " + user_input)

    responses = get_response(user_input)

    for res in responses:
        st.session_state.messages.append("🤖 " + res)

# -------------------------------
# 🎯 QUICK BUTTONS (no rerun)
# -------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Menu"):
        st.session_state.messages.append("🤖 Type 'menu'")

with col2:
    if st.button("Quiz"):
        for msg in start_quiz():
            st.session_state.messages.append("🤖 " + msg)

with col3:
    if st.button("News"):
        st.session_state.messages.append("🤖 " + get_news())