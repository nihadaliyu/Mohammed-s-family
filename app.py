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

# ---------------- STYLES (responsive/mobile-friendly) ----------------
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
                # Ensure Mustefa present under Shemega (backwards compatibility)
                if "Shemega" in data and "Mustefa" not in data["Shemega"].get("children", {}):
                    data["Shemega"].setdefault("children", {})["Mustefa"] = {
                        "description": "Child of Shemega + Mohammed",
                        "children": {},
                        "phone": "0911222337",
                        "photo": "",
                    }
        except Exception:
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

# ---------------- PATH HELPERS ----------------
def get_node_by_path(path):
    """
    Given a path list like ['Grandparent', 'Parent'], return the dict for that node.
    If path is empty -> return None (meaning top-level).
    """
    if not path:
        return None
    node = st.session_state.family_data
    # First element is top-level key
    try:
        node = node[path[0]]
    except Exception:
        return None
    for name in path[1:]:
        node = node.get("children", {}).get(name)
        if node is None:
            return None
    return node

def mark_confirm_delete(flag_key):
    st.session_state[flag_key] = True

# ---------------- DISPLAY FAMILY (recursive) ----------------
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
                st.markdown(
                    f"<div style='margin-top:6px;'><b>{phone}</b> <a class='phone-link' href='tel:{phone}'>📞 Call</a></div>",
                    unsafe_allow_html=True,
                )

        # ---------------- Add Partner (show as expander form) ----------------
        # Only show Add Partner if no partner and not locked
        if not partner and not locked_partner:
            with st.expander("➕ Add Partner", expanded=False):
                with st.form(key=f"partner_form_{key_base}"):
                    new_partner_name = st.text_input("Enter partner's name", key=f"partner_input_{key_base}")
                    if st.form_submit_button("Save Partner"):
                        new_name = (new_partner_name or "").strip()
                        if not new_name:
                            st.error("Please enter a partner name.")
                        else:
                            data["partner"] = new_name
                            # ensure children dict exists
                            data.setdefault("children", {})
                            save_family_data(st.session_state.family_data)
                            st.success(f"Partner {new_name} added for {name} ✅")
                            st.experimental_rerun()

        # ---------------- Edit / Delete Partner (if exists and not locked) ----------------
        if partner and not locked_partner:
            with st.expander("✏️ Edit Partner", expanded=False):
                with st.form(key=f"edit_partner_form_{key_base}"):
                    updated_partner = st.text_input("Edit partner's name", value=partner, key=f"edit_partner_input_{key_base}")
                    if st.form_submit_button("Update Partner"):
                        updated = (updated_partner or "").strip()
                        if not updated:
                            st.error("Partner name cannot be empty.")
                        else:
                            data["partner"] = updated
                            save_family_data(st.session_state.family_data)
                            st.success(f"Partner updated for {name} ✅")
                            st.experimental_rerun()
                # Delete Partner (outside the form)
                if st.button(f"Delete Partner for {name}", key=f"delete_partner_{key_base}"):
                    data["partner"] = ""
                    save_family_data(st.session_state.family_data)
                    st.success(f"Partner deleted for {name} ✅")
                    st.experimental_rerun()

        # ---------------- Add Child (appear if person has partner and is NOT one of the default wives) ----------------
        # This ensures that after adding partner, the Add Child expander is available
        if data.get("partner") and not data.get("locked_partner", False) and name not in MOTHERS_WITH_DEFAULT_PARTNER:
            with st.expander(f"➕ Add Child to {name}", expanded=False):
                with st.form(key=f"child_form_{key_base}"):
                    new_child_name = st.text_input("Enter child's name", key=f"child_name_{key_base}")
                    new_child_desc = st.text_area("Enter child's description", key=f"child_desc_{key_base}")
                    new_child_phone = st.text_input("Enter child's phone number", key=f"child_phone_{key_base}")
                    uploaded_photo = st.file_uploader("Upload child's photo", type=["jpg", "jpeg", "png"], key=f"child_photo_{key_base}")
                    if st.form_submit_button("Save Child"):
                        child_name = (new_child_name or "").strip()
                        if not child_name:
                            st.error("Please provide child's name.")
                        else:
                            child_data = {
                                "description": new_child_desc or "",
                                "children": {},
                                "phone": new_child_phone or "",
                                "photo": "",
                            }
                            if uploaded_photo is not None:
                                child_data["photo"] = save_uploaded_photo(uploaded_photo, [name, child_name])
                            data.setdefault("children", {})[child_name] = child_data
                            save_family_data(st.session_state.family_data)
                            st.success(f"Child {child_name} added under {name} ✅")
                            st.experimental_rerun()

        # ---------------- Edit current member (description, phone, photo) ----------------
        with st.expander("✏️ Edit Member", expanded=False):
            with st.form(key=f"edit_form_{key_base}"):
                updated_description = st.text_area("Update description", value=data.get("description", ""), key=f"edit_desc_{key_base}")
                updated_phone = st.text_input("Update phone number", value=data.get("phone", ""), key=f"edit_phone_{key_base}")
                updated_photo = st.file_uploader("Upload new photo (optional)", type=["jpg", "jpeg", "png"], key=f"edit_photo_{key_base}")
                if st.form_submit_button("Save Changes"):
                    data["description"] = updated_description
                    data["phone"] = updated_phone
                    if updated_photo is not None:
                        data["photo"] = save_uploaded_photo(updated_photo, path)
                    save_family_data(st.session_state.family_data)
                    st.success(f"{name} updated successfully ✅")
                    st.experimental_rerun()

        # ---------------- Dangerous: Delete member ----------------
        with st.expander("⚠️ Danger Zone", expanded=False):
            # click once to set a confirmation flag
            confirm_key = f"confirm_delete_{key_base}"
            if st.button(f"🗑️ Delete {name}", key=f"del_btn_{key_base}", on_click=mark_confirm_delete, args=(confirm_key,)):
                pass
            if st.session_state.get(confirm_key, False):
                st.warning(f"Are you sure you want to permanently delete {name}? This will remove them from their parent.")
                if st.button(f"Confirm Delete {name}", key=f"confirm_del_{key_base}"):
                    # find parent by ancestors
                    parent_node = get_node_by_path(ancestors)  # ancestors is list of names of parents (empty->top)
                    if parent_node is None:
                        # top-level deletion
                        st.session_state.family_data.pop(name, None)
                    else:
                        parent_node.get("children", {}).pop(name, None)
                    # clear confirm flag
                    st.session_state.pop(confirm_key, None)
                    save_family_data(st.session_state.family_data)
                    st.success(f"{name} deleted successfully ✅")
                    st.experimental_rerun()

        # ---------------- Recurse children ----------------
        for child_name, child_data in list(data.get("children", {}).items()):
            display_family(child_name, child_data, ancestors=path)


# ---------------- MAIN ----------------
st.markdown('<div class="main">', unsafe_allow_html=True)
st.markdown('<div class="cool-header">👨‍👩‍👧 Delko\'s Family Data Record</div>', unsafe_allow_html=True)

# Reset All History
if st.button("🔄 Reset All History", key="reset_all_history"):
    reset_session_state()
    save_family_data(copy.deepcopy(default_family_data))
    st.session_state.family_data = load_family_data()
    st.session_state.quiz_done = False
    st.session_state.current_question = random.choice(quiz_questions)
    st.success("All history has been reset!")
    st.experimental_rerun()

# Quiz-based simple login
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
    # ensure data present
    if "family_data" not in st.session_state:
        st.session_state.family_data = load_family_data()

    data = st.session_state.family_data
    for mother_name, mother_data in data.items():
        display_family(mother_name, mother_data)

    # Save button
    if st.button("💾 Save Changes"):
        save_family_data(st.session_state.family_data)
        st.success("✅ Data saved successfully")

st.markdown('</div>', unsafe_allow_html=True)
