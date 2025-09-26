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
        .button-row { display: flex; gap: 6px; margin-top: 6px; flex-wrap: wrap; }
        .stButton>button { border-radius: 8px !important; padding: 0.3em 0.8em; font-size: 0.9rem; }
        .edit-btn { background: #ffc107 !important; color: black !important; }
        .delete-btn { background: #dc3545 !important; color: white !important; }
        .add-btn { background: #28a745 !important; color: white !important; }
        
        /* MOBILE OPTIMIZATION */
        @media (max-width: 600px) {
            .main { padding: 16px 12px; margin: 10px; border-radius: 12px; }
            .cool-header { font-size: 1.6rem; }
            .section-title { font-size: 1rem; }
            .card { flex-direction: column; align-items: flex-start; }
            .card img { width: 80px; height: 80px; margin: 0 0 10px 0; }
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
    "Mohammed": {
        "id": "root",
        "name": "Mohammed",
        "photo": PLACEHOLDER_IMAGE,
        "partner": None,
        "children": {
            "Shemega": {
                "id": str(uuid.uuid4()),
                "name": "Shemega",
                "partner": "Mohammed",
                "children": {
                    "Mustefa": {
                        "id": str(uuid.uuid4()),
                        "name": "Mustefa",
                        "partner": None,
                        "children": {}
                    }
                },
                "photo": PLACEHOLDER_IMAGE
            },
            "Nurseba": {
                "id": str(uuid.uuid4()),
                "name": "Nurseba",
                "partner": "Mohammed",
                "children": {},
                "photo": PLACEHOLDER_IMAGE
            },
            "Dilbo": {
                "id": str(uuid.uuid4()),
                "name": "Dilbo",
                "partner": "Mohammed",
                "children": {},
                "photo": PLACEHOLDER_IMAGE
            },
            "Rukiya": {
                "id": str(uuid.uuid4()),
                "name": "Rukiya",
                "partner": "Mohammed",
                "children": {},
                "photo": PLACEHOLDER_IMAGE
            },
            "Nefissa": {
                "id": str(uuid.uuid4()),
                "name": "Nefissa",
                "partner": "Mohammed",
                "children": {},
                "photo": PLACEHOLDER_IMAGE
            },
        },
    }
}

# ---------------- SAVE/LOAD ----------------
def load_family_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return copy.deepcopy(default_family_data)

def save_family_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ---------------- DISPLAY FAMILY ----------------
def display_family(member, member_key, parent=None):
    with st.expander(member["name"], expanded=False):
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image(member.get("photo", PLACEHOLDER_IMAGE), use_container_width=True)
        with col2:
            st.markdown(f"**Name:** {member['name']}")
            if member.get("partner"):
                st.markdown(f"**Partner:** {member['partner']}")
        
        # --- Action Buttons (Edit/Delete) ---
        st.markdown('<div class="button-row">', unsafe_allow_html=True)
        edit_clicked = st.button(f"✏️ Edit {member['name']}", key=f"edit_{member_key}")
        delete_clicked = st.button("🗑️ Delete", key=f"delete_{member_key}")
        st.markdown('</div>', unsafe_allow_html=True)

        if edit_clicked:
            new_name = st.text_input("Edit Name", value=member["name"], key=f"edit_name_{member_key}")
            new_partner = st.text_input("Edit Partner", value=member.get("partner", ""), key=f"edit_partner_{member_key}")
            if st.button("Save Changes", key=f"save_{member_key}"):
                member["name"] = new_name
                member["partner"] = new_partner if new_partner else None
                save_family_data(family_data)
                st.rerun()

        if delete_clicked and parent is not None:
            parent.pop(member_key)
            save_family_data(family_data)
            st.rerun()

        # --- Partner/Child Buttons ---
        if member["name"] in MOTHERS_WITH_DEFAULT_PARTNER:
            st.button("➕ Add Child", key=f"add_child_{member_key}", on_click=add_child, args=(member,))
        else:
            if not member.get("partner"):
                st.button("💍 Add Partner", key=f"add_partner_{member_key}", on_click=add_partner, args=(member,))
            else:
                st.button("➕ Add Child", key=f"add_child_{member_key}", on_click=add_child, args=(member,))

        # --- Children Recursion ---
        for child_key, child in member.get("children", {}).items():
            display_family(child, child_key, member["children"])

# ---------------- ADD FUNCTIONS ----------------
def add_partner(member):
    with st.form(key=f"form_partner_{member['id']}"):
        partner_name = st.text_input("Partner Name")
        submitted = st.form_submit_button("Save Partner")
        if submitted and partner_name:
            member["partner"] = partner_name
            save_family_data(family_data)
            st.rerun()

def add_child(member):
    with st.form(key=f"form_child_{member['id']}"):
        child_name = st.text_input("Child Name")
        submitted = st.form_submit_button("Save Child")
        if submitted and child_name:
            child_id = str(uuid.uuid4())
            member["children"][child_name] = {
                "id": child_id,
                "name": child_name,
                "partner": None,
                "children": {},
                "photo": PLACEHOLDER_IMAGE
            }
            save_family_data(family_data)
            st.rerun()

# ---------------- MAIN ----------------
st.markdown('<div class="main">', unsafe_allow_html=True)
st.markdown('<div class="cool-header">👨‍👩‍👧‍👦 Delko\'s Family Tree</div>', unsafe_allow_html=True)

family_data = load_family_data()

# Quiz
st.subheader("🎯 Family Quiz")
q = random.choice(quiz_questions)
ans = st.text_input(q["question"], key="quiz_input")
if st.button("Submit Answer"):
    if ans.strip().lower() == q["answer"].lower():
        st.success("✅ Correct!")
    else:
        st.error(f"❌ Wrong! The correct answer is {q['answer']}.")

# Family tree
st.subheader("🌳 Family Tree")
for key, member in family_data.items():
    display_family(member, key)

# Save data
if st.button("💾 Save Family Data"):
    save_family_data(family_data)
    st.success("Family data saved!")

st.markdown('</div>', unsafe_allow_html=True)
