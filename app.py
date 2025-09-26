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
        .action-buttons { margin-top: 8px; }
        .stButton>button, .stForm>button, .stTextInput>input, .stTextArea>textarea { border-radius: 8px !important; width: 100% !important; }
        .stExpander { background: #f4f6fa !important; border-radius: 14px !important; margin-bottom: 14px !important; }
        .stExpanderHeader { font-size: 1rem !important; font-weight: 600 !important; color: #007bff !important; }
        .edit-inline { background: #007bff !important; color:#fff !important; border-radius:8px; padding:6px 8px; }
        .delete-inline { background: #d9534f !important; color:#fff !important; border-radius:8px; padding:6px 8px; }
        @media (max-width: 600px) {
            .main { padding: 16px 12px; margin: 10px; border-radius: 12px; }
            .cool-header { font-size: 1.6rem; }
            .section-title { font-size: 1rem; }
            .card { flex-direction: column; align-items: flex-start; }
            .card img { width: 80px; height: 80px; margin: 0 0 10px 0; }
            .phone-link { font-size: 0.85rem; padding: 6px 10px; margin-top: 6px; display:inline-block; }
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
        except Exception:
            data = copy.deepcopy(default_family_data)
    else:
        data = copy.deepcopy(default_family_data)

    # Ensure Mustefa is present under Shemega (backwards compatibility)
    try:
        shem = data.setdefault("Shemega", {})
        shem_children = shem.setdefault("children", {})
        if "Mustefa" not in shem_children:
            shem_children["Mustefa"] = {
                "description": "Child of Shemega + Mohammed",
                "children": {},
                "phone": "0911222337",
                "photo": "",
            }
    except Exception:
        pass

    return data


def save_family_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


# ---------------- SESSION ----------------
def reset_session_state():
    for k in list(st.session_state.keys()):
        del st.session_state[k]


if "family_data" not in st.session_state:
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


# ---------------- HELPERS ----------------
def get_parent_dict(ancestors):
    """
    Given ancestors list (immediate parents from top to immediate parent),
    return the dict that directly holds the current member as keys.
    If ancestors is empty -> returns the top-level family_data dict.
    Ensures intermediate 'children' dicts exist.
    """
    if not ancestors:
        return st.session_state.family_data
    parent = st.session_state.family_data.get(ancestors[0])
    if parent is None:
        return None
    for anc in ancestors[1:]:
        # ensure children dict exists and ancestor node exists inside it
        children = parent.setdefault("children", {})
        parent = children.setdefault(anc, {})
    # return the dict that stores children of the immediate parent
    return parent.setdefault("children", {})


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
                st.markdown(f"<div style='margin-top:6px;'><b>{phone}</b> <a class='phone-link' href='tel:{phone}'>📞 Call</a></div>", unsafe_allow_html=True)

            # Inline action buttons in two narrow columns so they appear next to description
            b1, b2 = st.columns([1, 1])
            with b1:
                # Label should mention the member's name
                if st.button(f"Edit {name}", key=f"edit_btn_{key_base}"):
                    # open edit form for this member
                    st.session_state[f"editing_{key_base}"] = True
            with b2:
                if st.button(f"Delete {name}", key=f"delete_btn_{key_base}"):
                    # immediate single-click delete (per your request)
                    parent_dict = get_parent_dict(ancestors)
                    if parent_dict is not None:
                        parent_dict.pop(name, None)
                        save_family_data(st.session_state.family_data)
                        st.success(f"{name} deleted ✅")
                        st.experimental_rerun()

        # Edit form block (appears immediately after clicking Edit)
        if st.session_state.get(f"editing_{key_base}", False):
            with st.form(key=f"edit_form_{key_base}"):
                new_name = st.text_input("Member name", value=name, key=f"edit_name_{key_base}")
                new_desc = st.text_area("Description", value=data.get("description", ""), key=f"edit_desc_{key_base}")
                new_phone = st.text_input("Phone", value=data.get("phone", ""), key=f"edit_phone_{key_base}")
                if locked_partner:
                    st.text_input("Partner (locked)", value=data.get("partner", ""), disabled=True)
                    new_partner = data.get("partner", "")
                else:
                    new_partner = st.text_input("Partner (add or edit)", value=data.get("partner", ""), key=f"edit_partner_{key_base}")
                new_photo = st.file_uploader("Upload new photo (optional)", type=["jpg", "jpeg", "png"], key=f"edit_photo_{key_base}")

                if st.form_submit_button("Save Changes", key=f"save_edit_{key_base}"):
                    # update fields
                    parent_dict = get_parent_dict(ancestors)
                    if parent_dict is None:
                        st.error("Parent not found. Cannot rename or save.")
                    else:
                        # avoid name collision
                        new_name_clean = (new_name or "").strip()
                        if not new_name_clean:
                            st.error("Member name cannot be empty.")
                        elif new_name_clean != name and new_name_clean in parent_dict:
                            st.error("A sibling with that name already exists. Choose a different name.")
                        else:
                            # perform rename if needed
                            node_data = data
                            node_data["description"] = new_desc or ""
                            node_data["phone"] = new_phone or ""
                            if not locked_partner:
                                node_data["partner"] = new_partner or ""
                            if new_photo is not None:
                                node_data["photo"] = save_uploaded_photo(new_photo, ancestors + [new_name_clean or name])
                            # rename in parent dict if necessary
                            if new_name_clean != name:
                                parent_dict.pop(name, None)
                                parent_dict[new_name_clean] = node_data
                            save_family_data(st.session_state.family_data)
                            st.success(f"{new_name_clean} updated ✅")
                            # close edit form and rerun to refresh UI
                            st.session_state.pop(f"editing_{key_base}", None)
                            st.experimental_rerun()

        # Quick Add Partner inline (if no partner & not locked) - optional quick flow
        if not data.get("partner") and not data.get("locked_partner", False):
            with st.form(key=f"add_partner_form_{key_base}"):
                quick_partner = st.text_input("Add partner (quick)", key=f"quick_partner_{key_base}")
                if st.form_submit_button("Save Partner", key=f"save_quick_partner_{key_base}"):
                    p = (quick_partner or "").strip()
                    if not p:
                        st.error("Partner name required.")
                    else:
                        data["partner"] = p
                        # ensure children dict exists
                        data.setdefault("children", {})
                        save_family_data(st.session_state.family_data)
                        st.success(f"Partner {p} added for {name} ✅")
                        st.experimental_rerun()

        # Add Child (visible when partner exists and not locked and not default wives)
        if data.get("partner") and not data.get("locked_partner", False) and name not in MOTHERS_WITH_DEFAULT_PARTNER:
            with st.expander(f"➕ Add Child to {name}", expanded=False):
                with st.form(key=f"child_form_{key_base}"):
                    new_child_name = st.text_input("Child name", key=f"child_name_{key_base}")
                    new_child_desc = st.text_area("Child description", key=f"child_desc_{key_base}")
                    new_child_phone = st.text_input("Child phone", key=f"child_phone_{key_base}")
                    uploaded_child_photo = st.file_uploader("Upload child's photo", type=["jpg", "jpeg", "png"], key=f"child_photo_{key_base}")
                    if st.form_submit_button("Save Child", key=f"save_child_{key_base}"):
                        cname = (new_child_name or "").strip()
                        if not cname:
                            st.error("Child name required.")
                        else:
                            child_data = {
                                "description": new_child_desc or "",
                                "children": {},
                                "phone": new_child_phone or "",
                                "photo": "",
                            }
                            if uploaded_child_photo is not None:
                                child_data["photo"] = save_uploaded_photo(uploaded_child_photo, ancestors + [name, cname])
                            data.setdefault("children", {})[cname] = child_data
                            save_family_data(st.session_state.family_data)
                            st.success(f"Child {cname} added under {name} ✅")
                            st.experimental_rerun()

        # Recurse into children
        for child_name, child_data in list(data.get("children", {}).items()):
            display_family(child_name, child_data, ancestors=path)


# ---------------- MAIN ----------------
st.markdown('<div class="main">', unsafe_allow_html=True)
st.markdown('<div class="cool-header">👨‍👩‍👧 Delko\'s Family Data Record</div>', unsafe_allow_html=True)

# Reset All History button
if st.button("🔄 Reset All History", key="reset_all"):
    reset_session_state()
    save_family_data(copy.deepcopy(default_family_data))
    st.session_state.family_data = load_family_data()
    st.session_state.quiz_done = False
    st.session_state.current_question = random.choice(quiz_questions)
    st.success("All history has been reset!")
    st.experimental_rerun()

# Quiz gating
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

    # ensure family data in session
    if "family_data" not in st.session_state:
        st.session_state.family_data = load_family_data()

    data = st.session_state.family_data
    for mother_name, mother_data in list(data.items()):
        display_family(mother_name, mother_data)

    # Save button (extra)
    if st.button("💾 Save Changes", key="save_changes"):
        save_family_data(st.session_state.family_data)
        st.success("✅ Data saved successfully")

st.markdown('</div>', unsafe_allow_html=True)
