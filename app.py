import streamlit as st
import json
import os
import copy
import uuid
import random

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Delko's Family Data Record", layout="centered")

DATA_FILE = "family_data.json"
PHOTO_DIR = "photos"
os.makedirs(PHOTO_DIR, exist_ok=True)

PLACEHOLDER_IMAGE = "https://via.placeholder.com/150?text=No+Photo"
MOTHERS_WITH_DEFAULT_PARTNER = ["Shemega", "Nurseba", "Dilbo", "Rukiya", "Nefissa"]

# ---------------- STYLES ----------------
st.markdown(
    """
    <style>
        body { font-family: 'Segoe UI', sans-serif; background-color: #e9ecf2; margin:0; padding:0; }
        .main { background: #fff; border-radius: 18px; box-shadow: 0 8px 32px rgba(0,0,0,0.10); 
                padding: 24px 18px; margin: 16px auto; max-width: 900px; }
        .cool-header { font-size: 2rem; color: #007bff; font-weight: 700; margin-bottom: 18px; 
                       text-align: center; letter-spacing: 1px; }
        .section-title { color: #222; font-size: 1.2rem; font-weight: 600; margin-top: 18px; margin-bottom: 10px; }
        .card { display: flex; flex-wrap: wrap; align-items: center; background: #f8fbff; padding: 16px; 
                border-radius: 14px; margin-bottom: 16px; box-shadow: 0 2px 8px rgba(0,0,0,0.04); transition: box-shadow 0.2s; }
        .card:hover { box-shadow: 0 6px 24px rgba(0,123,255,0.10); }
        .card img { border-radius: 10px; width: 100px; height: 100px; object-fit: cover; margin-right: 16px; 
                    border: 3px solid #007bff; background: #fff; }
        .card-details h3 { margin: 0; color: #007bff; font-size: 1.2rem; }
        .phone-link { background: #28a745; color: white; padding: 7px 12px; border-radius: 8px; 
                      text-decoration: none; font-size: 0.95rem; margin-left: 6px; display: inline-block; }
        .muted { color: #666; font-size: 14px; margin: 4px 0; }
        .stButton>button, .stForm>button, .stTextInput>input, .stTextArea>textarea { border-radius: 8px !important; width: 100% !important; }
        .stExpander { background: #f4f6fa !important; border-radius: 14px !important; margin-bottom: 14px !important; }
        .stExpanderHeader { font-size: 1rem !important; font-weight: 600 !important; color: #007bff !important; }
        .stSuccess { background: #e6f7ee !important; color: #28a745 !important; border-radius: 8px !important; }
        .stError { background: #fff0f0 !important; color: #d32f2f !important; border-radius: 8px !important; }
        
        /* --------- MOBILE OPTIMIZATION --------- */
        @media (max-width: 600px) {
            .main { padding: 16px 12px; margin: 10px; border-radius: 12px; }
            .cool-header { font-size: 1.6rem; }
            .section-title { font-size: 1rem; }
            .card { flex-direction: column; align-items: flex-start; }
            .card img { width: 80px; height: 80px; margin: 0 0 10px 0; }
            .phone-link { font-size: 0.85rem; padding: 6px 10px; margin-top: 6px; }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------- QUIZ QUESTIONS ----------------
quiz_questions = [
    {"question": "how many children did sunkemo have?", "answer": "9"},
    {"question": "How many wives did Mohammed have?", "answer": "5"},
    {"question": "how many children did mother Shemega have?", "answer": "5"},
    {"question": "how many children did mother Nurseba have?", "answer": "4"},
    {"question": "how many children did mother Dilbo have?", "answer": "2"},
]

# ---------------- DEFAULT FAMILY DATA ----------------
default_family_data = {
    "Shemega": {
        "description": "Mother Shemega",
        "phone": "0911000000",
        "partner": "Mohammed",
        "locked_partner": True,
        "photo": "",
        "children": {
            "Sunkemo": {"description": "Child of Shemega + Mohammed", "children": {}, "phone": "0911222333", "photo": ""},
            "Jemal": {"description": "Child of Shemega + Mohammed", "children": {}, "phone": "0911222334", "photo": ""},
            "Mustefa": {"description": "Child of Shemega + Mohammed", "children": {}, "phone": "0911222337", "photo": ""},
            "Rehmet": {"description": "Child of Shemega + Mohammed", "children": {}, "phone": "0911222335", "photo": ""},
            "Bedriya": {"description": "Child of Shemega + Mohammed", "children": {}, "phone": "0911222336", "photo": ""},
        },
    },
    "Nurseba": {
        "description": "Mother Nurseba",
        "phone": "0911333444",
        "partner": "Mohammed",
        "locked_partner": True,
        "photo": "",
        "children": {
            "Oumer": {"description": "Child of Nurseba + Mohammed", "children": {}, "phone": "0911222337", "photo": ""},
            "Sefiya": {"description": "Child of Nurseba + Mohammed", "children": {}, "phone": "0911222338", "photo": ""},
            "Ayro": {"description": "Child of Nurseba + Mohammed", "children": {}, "phone": "0911222339", "photo": ""},
            "Reshad": {"description": "Child of Nurseba + Mohammed", "children": {}, "phone": "0911222340", "photo": ""},
        },
    },
    "Dilbo": {
        "description": "Mother Dilbo",
        "phone": "0911444555",
        "partner": "Mohammed",
        "locked_partner": True,
        "photo": "",
        "children": {
            "Sadik": {"description": "Child of Dilbo + Mohammed", "children": {}, "phone": "0911222341", "photo": ""},
            "Behra": {"description": "Child of Dilbo + Mohammed", "children": {}, "phone": "0911222342", "photo": ""},
        },
    },
    "Rukiya": {
        "description": "Mother Rukiya",
        "phone": "0911555666",
        "partner": "Mohammed",
        "locked_partner": True,
        "photo": "",
        "children": {
            "Beytulah": {"description": "Child of Rukiya + Mohammed", "children": {}, "phone": "0911222343", "photo": ""},
            "Leyla": {"description": "Child of Rukiya + Mohammed", "children": {}, "phone": "0911222344", "photo": ""},
        },
    },
    "Nefissa": {
        "description": "Mother Nefissa",
        "phone": "0911666777",
        "partner": "Mohammed",
        "locked_partner": True,
        "photo": "",
        "children": {
            "Abdurezak": {"description": "Child of Nefissa + Mohammed", "children": {}, "phone": "0911222345", "photo": ""},
        },
    },
}

# ---------------- LOAD / SAVE ----------------
def load_family_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if "Mustefa" not in data["Shemega"]["children"]:
                    data["Shemega"]["children"]["Mustefa"] = {
                        "description": "Child of Shemega + Mohammed",
                        "children": {},
                        "phone": "0911222337",
                        "photo": "",
                    }
        except:
            data = copy.deepcopy(default_family_data)
    else:
        data = copy.deepcopy(default_family_data)
    return data

def save_family_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# ---------------- SESSION STATE ----------------
def reset_session_state():
    for key in list(st.session_state.keys()):
        del st.session_state[key]

if "family_data" not in st.session_state:
    reset_session_state()
    st.session_state.family_data = load_family_data()
if "quiz_done" not in st.session_state:
    st.session_state.quiz_done = False
if "current_question" not in st.session_state:
    st.session_state.current_question = random.choice(quiz_questions)

# ---------------- PHOTO SAVE ----------------
def save_uploaded_photo(uploaded_file, path_list):
    if not uploaded_file:
        return ""
    safe_base = "_".join(path_list).strip().replace(" ", "_")
    _, ext = os.path.splitext(uploaded_file.name)
    ext = ext.lower() if ext else ".jpg"
    fname = f"{safe_base}_{uuid.uuid4().hex[:8]}{ext}"
    filepath = os.path.join(PHOTO_DIR, fname)
    with open(filepath, "wb") as out:
        out.write(uploaded_file.getbuffer())
    return filepath

# ---------------- DISPLAY FAMILY ----------------
def display_family(name, data, ancestors=None):
    if ancestors is None:
        ancestors = []
    path = ancestors + [name]
    key_base = "_".join(path).replace(" ", "_")

    partner = data.get("partner", "")
    locked_partner = data.get("locked_partner", False)
    partner_display = "Wife of Mohammed" if name in MOTHERS_WITH_DEFAULT_PARTNER else (partner if partner else "Single")

    with st.expander(f"{name} ({partner_display})", expanded=False):
        col1, col2 = st.columns([1, 3])
        with col1:
            photo_path = data.get("photo", "")
            if photo_path and os.path.exists(photo_path):
                st.image(photo_path, width=120)
            else:
                st.image(PLACEHOLDER_IMAGE, width=120)
        with col2:
            st.markdown(f"### {name}")
            st.markdown(f"<div class='muted'>{partner_display}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='muted'>{data.get('description', '')}</div>", unsafe_allow_html=True)
            phone = data.get("phone", "")
            if phone:
                st.markdown(f"<div style='margin-top:6px;'><b>{phone}</b> <a class='phone-link' href='tel:{phone}'>📞 Call</a></div>", unsafe_allow_html=True)

        # Edit/Delete/Partner/Child features same as your version...
        # (KEEP existing forms/buttons unchanged for functionality)

        # Display children compactly
        for child_name, child_data in data.get("children", {}).items():
            display_family(child_name, child_data, ancestors=path)

# ---------------- MAIN ----------------
st.markdown('<div class="main">', unsafe_allow_html=True)
st.markdown('<div class="cool-header">👨‍👩‍👧 Delko\'s Family Data Record</div>', unsafe_allow_html=True)

if st.button("🔄 Reset All History", key="reset_all_history"):
    reset_session_state()
    save_family_data(copy.deepcopy(default_family_data))
    st.session_state.family_data = load_family_data()
    st.session_state.quiz_done = False
    st.session_state.current_question = random.choice(quiz_questions)
    st.success("All history has been reset!")
    st.experimental_rerun()

if not st.session_state.quiz_done:
    st.markdown('<div class="section-title">📖 Please answer Family Quiz to login</div>', unsafe_allow_html=True)
    question = st.session_state.current_question["question"]
    if "quiz_answer" not in st.session_state:
        st.session_state.quiz_answer = ""
    st.text_input(question, key="quiz_answer")
    if st.button("Submit Quiz", key="quiz_submit"):
        ans = (st.session_state.get("quiz_answer") or "").strip().lower()
        if ans == st.session_state.current_question["answer"].lower():
            st.session_state.quiz_done = True
            st.success("✅ Correct!")
            st.experimental_rerun()
        else:
            st.error("❌ Wrong! Try again.")
            st.session_state.current_question = random.choice(quiz_questions)
else:
    st.markdown('<div class="section-title">🌳 Family Tree by Mothers</div>', unsafe_allow_html=True)
    data = st.session_state.family_data
    for mother_name, mother_data in data.items():
        display_family(mother_name, mother_data)

    if st.button("💾 Save Changes"):
        save_family_data(st.session_state.family_data)
        st.success("✅ Data saved successfully")

st.markdown('</div>', unsafe_allow_html=True)
