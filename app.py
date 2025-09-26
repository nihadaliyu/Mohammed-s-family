import streamlit as st
import json
import os
import copy
import uuid
import random

st.set_page_config(page_title="Delko's Family Data Record", layout="centered")

DATA_FILE = "family_data.json"
PHOTO_DIR = "photos"
os.makedirs(PHOTO_DIR, exist_ok=True)

PLACEHOLDER_IMAGE = "https://via.placeholder.com/150?text=No+Photo"
MOTHERS_WITH_DEFAULT_PARTNER = ["Shemega", "Nurseba", "Dilbo", "Rukiya", "Nefissa"]

# ---------------- CSS ----------------
st.markdown(
    """
    <style>
        :root { --brand:#0b6cff; --bg:#f5f7fb; --card:#fff; --muted:#667085; --border:#e4e7ec; }
        html,body { background:var(--bg); }
        .main { background:var(--card); border-radius:16px; padding:18px; margin:12px auto; max-width:860px; box-shadow:0 8px 24px rgba(0,0,0,0.06); }
        .cool-header { background:linear-gradient(90deg,#0b6cff,#5b9bff); color:#fff; padding:10px 14px; border-radius:12px; font-weight:700; text-align:center; margin-bottom:12px; position:sticky; top:8px; z-index:10; }
        .muted{ color:var(--muted); font-size:14px; }
        .button-row{ display:flex; gap:8px; flex-wrap:wrap; margin-top:8px; }
        .stButton>button{ border-radius:10px !important; padding:10px 12px; }
        @media(max-width:600px){ .stButton>button{ width:100% !important; } .main{ padding:14px; margin:8px;} .cool-header{ font-size:1rem;} }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------- QUIZ ----------------
quiz_questions = [
    {"question": "How many children did Sunkemo have?", "answer": "9"},
    {"question": "How many wives did Mohammed have?", "answer": "5"},
    {"question": "How many children did mother Shemega have?", "answer": "5"},
    {"question": "How many children did mother Nurseba have?", "answer": "4"},
    {"question": "How many children did mother Dilbo have?", "answer": "2"},
]

# ---------------- DEFAULT DATA ----------------
default_family_data = {
    "Shemega": {
        "description": "Mother Shemega",
        "phone": "0911000000",
        "partner": "Mohammed",
        "locked_partner": True,
        "locked_root": True,
        "photo": "",
        "children": {
            "Sunkemo": {"description": "Child of Shemega + Mohammed", "children": {}, "phone": "0911222333", "photo": "", "fixed_generation": False},
            "Jemal":   {"description": "Child of Shemega + Mohammed", "children": {}, "phone": "0911222334", "photo": "", "fixed_generation": False},
            "Mustefa": {"description": "Child of Shemega + Mohammed", "children": {}, "phone": "0911222337", "photo": "", "fixed_generation": False},
            "Rehmet":  {"description": "Child of Shemega + Mohammed", "children": {}, "phone": "0911222335", "photo": "", "fixed_generation": False},
            "Bedriya": {"description": "Child of Shemega + Mohammed", "children": {}, "phone": "0911222336", "photo": "", "fixed_generation": False},
        },
    },
    "Nurseba": {
        "description": "Mother Nurseba",
        "phone": "0911333444",
        "partner": "Mohammed",
        "locked_partner": True,
        "locked_root": True,
        "photo": "",
        "children": {
            "Oumer": {"description": "Child of Nurseba + Mohammed", "children": {}, "phone": "0911222337", "photo": "", "fixed_generation": False},
            "Sefiya": {"description": "Child of Nurseba + Mohammed", "children": {}, "phone": "0911222338", "photo": "", "fixed_generation": False},
            "Ayro": {"description": "Child of Nurseba + Mohammed", "children": {}, "phone": "0911222339", "photo": "", "fixed_generation": False},
            "Reshad": {"description": "Child of Nurseba + Mohammed", "children": {}, "phone": "0911222340", "photo": "", "fixed_generation": False},
        },
    },
    "Dilbo": {
        "description": "Mother Dilbo",
        "phone": "0911444555",
        "partner": "Mohammed",
        "locked_partner": True,
        "locked_root": True,
        "photo": "",
        "children": {
            "Sadik": {"description": "Child of Dilbo + Mohammed", "children": {}, "phone": "0911222341", "photo": "", "fixed_generation": False},
            "Behra": {"description": "Child of Dilbo + Mohammed", "children": {}, "phone": "0911222342", "photo": "", "fixed_generation": False},
        },
    },
    "Rukiya": {
        "description": "Mother Rukiya",
        "phone": "0911555666",
        "partner": "Mohammed",
        "locked_partner": True,
        "locked_root": True,
        "photo": "",
        "children": {
            "Beytulah": {"description": "Child of Rukiya + Mohammed", "children": {}, "phone": "0911222343", "photo": "", "fixed_generation": False},
            "Leyla": {"description": "Child of Rukiya + Mohammed", "children": {}, "phone": "0911222344", "photo": "", "fixed_generation": False},
        },
    },
    "Nefissa": {
        "description": "Mother Nefissa",
        "phone": "0911666777",
        "partner": "Mohammed",
        "locked_partner": True,
        "locked_root": True,
        "photo": "",
        "children": {
            "Abdurezak": {"description": "Child of Nefissa + Mohammed", "children": {}, "phone": "0911222345", "photo": "", "fixed_generation": False},
        },
    },
}

# ---------------- Load/Save ----------------
def load_family_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return copy.deepcopy(default_family_data)
    return copy.deepcopy(default_family_data)

def save_family_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def save_and_rerun():
    save_family_data(st.session_state.family_data)
    st.rerun()

def save_uploaded_photo(uploaded_file, path_list):
    if not uploaded_file:
        return ""
    safe_base = "_".join(path_list).replace(" ", "_")
    _, ext = os.path.splitext(uploaded_file.name)
    fname = f"{safe_base}_{uuid.uuid4().hex[:6]}{ext or '.jpg'}"
    filepath = os.path.join(PHOTO_DIR, fname)
    with open(filepath, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return filepath

# ---------------- Init ----------------
if "family_data" not in st.session_state:
    st.session_state.family_data = load_family_data()
if "quiz_done" not in st.session_state:
    st.session_state.quiz_done = False
if "current_question" not in st.session_state:
    st.session_state.current_question = random.choice(quiz_questions)

# ---------------- Helpers ----------------
def get_node_and_parent_children(path):
    if not path:
        return None, st.session_state.family_data
    root = st.session_state.family_data
    parent_children = root
    node = None
    for i, part in enumerate(path):
        if i == 0:
            node = root.get(part)
            parent_children = root
        else:
            parent_children = node.get("children", {})
            node = parent_children.get(part)
        if node is None:
            return None, st.session_state.family_data
    return node, parent_children

def get_parent_container(ancestors):
    if not ancestors:
        return st.session_state.family_data
    node, parent_children = get_node_and_parent_children(ancestors)
    if node is None:
        return st.session_state.family_data
    return parent_children

# ---------------- Display ----------------
def display_family(name, data, ancestors=None):
    if ancestors is
