# app.py - Final corrected version for Delko's Family Data Record
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
        .button-row { display: flex; gap: 6px; margin-top: 6px; flex-wrap: wrap; }
        .stButton>button { border-radius: 8px !important; padding: 0.3em 0.8em; font-size: 0.9rem; }
        .edit-btn { background: #ffc107 !important; color: black !important; }
        .delete-btn { background: #dc3545 !important; color: white !important; }
        .add-btn { background: #28a745 !important; color: white !important; }
        .danger { color: #d9534f; font-weight:700; }
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

    # ensure Mustefa under Shemega for backward compatibility
    try:
        shem = data.setdefault("Shemega", {})
        children = shem.setdefault("children", {})
        if "Mustefa" not in children:
            children["Mustefa"] = {
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

# ---------------- SESSION STATE HELPERS ----------------
if "family_data" not in st.session_state:
    st.session_state.family_data = load_family_data()
if "quiz_done" not in st.session_state:
    st.session_state.quiz_done = False
if "current_question" not in st.session_state:
    st.session_state.current_question = random.choice(quiz_questions)

def reset_session_state_and_data():
    # clear session state keys but preserve what we need to reinitialize
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.session_state.family_data = load_family_data()
    st.session_state.quiz_done = False
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

# ---------------- PATH / PARENT HELPERS ----------------
def get_parent_container(ancestors):
    """
    Return the dict object which directly contains the current member as keys.
    If ancestors is empty -> top-level family_data dict.
    """
    if not ancestors:
        return st.session_state.family_data
    node = st.session_state.family_data
    # walk until immediate parent
    for name in ancestors[:-1]:
        node = node[name]["children"]
    # if there's only one ancestor then parent container is top-level children under that ancestor
    parent_name = ancestors[-1]
    parent_node = node[parent_name]
    return parent_node.setdefault("children", {})

def get_node_by_path(path):
    """
    Given path list (ancestors + [name]) return the node dict, or None
    """
    if not path:
        return None
    node = st.session_state.family_data.get(path[0])
    if node is None:
        return None
    for p in path[1:]:
        node = node.get("children", {}).get(p)
        if node is None:
            return None
    return node

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

            # inline action buttons row
            st.markdown('<div class="button-row">', unsafe_allow_html=True)
            # Edit button shows edit form below
            if st.button(f"Edit {name}", key=f"edit_btn_{key_base}"):
                st.session_state[f"editing_{key_base}"] = True
            # Delete button sets confirm flag
            if st.button(f"Delete {name}", key=f"delete_btn_{key_base}"):
                st.session_state[f"confirm_delete_{key_base}"] = True
            st.markdown('</div>', unsafe_allow_html=True)

        # Edit form visible when editing flag set
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
                    parent_container = get_parent_container(ancestors)
                    if parent_container is None:
                        st.error("Parent not found; cannot save.")
                    else:
                        new_name_clean = (new_name or "").strip()
                        if not new_name_clean:
                            st.error("Member name cannot be empty.")
                        elif new_name_clean != name and new_name_clean in parent_container:
                            st.error("Sibling with this name already exists. Choose a different name.")
                        else:
                            # update fields
                            data["description"] = new_desc or ""
                            data["phone"] = new_phone or ""
                            if not locked_partner:
                                data["partner"] = new_partner or ""
                            # save new photo if provided
                            if new_photo is not None:
                                data["photo"] = save_uploaded_photo(new_photo, ancestors + [new_name_clean or name])
                            # handle rename: pop old key, insert new
                            if new_name_clean != name:
                                parent_container.pop(name, None)
                                parent_container[new_name_clean] = data
                            save_family_data(st.session_state.family_data)
                            st.success(f"{new_name_clean} updated ✅")
                            # close editing and refresh
                            st.session_state.pop(f"editing_{key_base}", None)
                            st.experimental_rerun()

        # Delete confirm UI
        if st.session_state.get(f"confirm_delete_{key_base}", False):
            st.warning(f"Are you sure you want to permanently delete {name}?")
            if st.button(f"Confirm Delete {name}", key=f"confirm_delete_btn_{key_base}"):
                # find parent container
                if ancestors:
                    parent_container = get_parent_container(ancestors)
                    parent_container.pop(name, None)
                else:
                    # top-level deletion
                    st.session_state.family_data.pop(name, None)
                save_family_data(st.session_state.family_data)
                st.success(f"{name} deleted ✅")
                st.session_state.pop(f"confirm_delete_{key_base}", None)
                st.experimental_rerun()

        # Show Add Partner if no partner and not locked and NOT default wives
        if (not data.get("partner")) and (not data.get("locked_partner", False)) and (name not in MOTHERS_WITH_DEFAULT_PARTNER):
            with st.form(key=f"add_partner_form_{key_base}"):
                partner_name = st.text_input("Add Partner (required to add children)", key=f"partner_input_{key_base}")
                if st.form_submit_button("Save Partner", key=f"save_partner_{key_base}"):
                    p = (partner_name or "").strip()
                    if not p:
                        st.error("Partner name required.")
                    else:
                        data["partner"] = p
                        data.setdefault("children", {})
                        save_family_data(st.session_state.family_data)
                        st.success(f"Partner {p} added for {name} ✅")
                        st.experimental_rerun()

        # If partner exists OR member is one of default wives -> show Add Child
        if (data.get("partner") or name in MOTHERS_WITH_DEFAULT_PARTNER):
            # but prevent Add Child for people with locked_partner==True? default wives are allowed
            if not data.get("locked_partner", False) or name in MOTHERS_WITH_DEFAULT_PARTNER:
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

# Reset All History
if st.button("🔄 Reset All History", key="reset_all_history"):
    save_family_data(copy.deepcopy(default_family_data))
    reset_session_state_and_data()
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
    # Ensure data present
    if "family_data" not in st.session_state:
        st.session_state.family_data = load_family_data()

    data = st.session_state.family_data
    # display each top-level mother
    for mother_name, mother_data in list(data.items()):
        display_family(mother_name, mother_data)

    # Save button
    if st.button("💾 Save Changes", key="save_changes"):
        save_family_data(st.session_state.family_data)
        st.success("✅ Data saved successfully")

st.markdown('</div>', unsafe_allow_html=True)
