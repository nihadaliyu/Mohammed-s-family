# app.py - Final / corrected for requested behaviors
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

# ---------------- CSS (responsive + keeps your previous look) ----------------
st.markdown(
    """
    <style>
        body { font-family: 'Segoe UI', sans-serif; background-color: #e9ecf2; margin:0; padding:0; }
        .main { background: #fff; border-radius: 18px; box-shadow: 0 8px 32px rgba(0,0,0,0.10);
                padding: 24px 18px; margin: 16px auto; max-width: 900px; }
        .cool-header { font-size: 2.2rem; color: #007bff; font-weight: 700; margin-bottom: 18px; text-align: center; }
        .section-title { color: #222; font-size: 1.2rem; font-weight: 600; margin-top: 18px; margin-bottom: 10px; }
        .card { display:flex; gap:12px; align-items:center; background:#f8fbff; padding:12px; border-radius:12px; margin-bottom:12px; }
        .card img { width:96px; height:96px; object-fit:cover; border-radius:10px; border:3px solid #007bff; }
        .muted { color:#666; font-size:14px; margin:4px 0; }
        .button-row { display:flex; gap:8px; margin-top:6px; flex-wrap:wrap; }
        .stButton>button { border-radius:8px !important; }
        @media (max-width:600px){
            .main { padding:16px; margin:10px; }
            .cool-header { font-size:1.6rem; }
            .card { flex-direction:column; align-items:flex-start; }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------- QUIZ ----------------
quiz_questions = [
    {"question": "how many children did sunkemo have?", "answer": "9"},
    {"question": "How many wives did Mohammed have?", "answer": "5"},
    {"question": "how many children did mother Shemega have?", "answer": "5"},
    {"question": "how many children did mother Nurseba have?", "answer": "4"},
    {"question": "how many children did mother Dilbo have?", "answer": "2"},
]

# ---------------- DEFAULT DATA (with fixed_generation flags for initial first-children) ----------------
default_family_data = {
    "Shemega": {
        "description": "Mother Shemega",
        "phone": "0911000000",
        "partner": "Mohammed",
        "locked_partner": True,
        "photo": "",
        "children": {
            "Sunkemo": {"description": "Child of Shemega + Mohammed", "children": {}, "phone": "0911222333", "photo": "", "fixed_generation": True},
            "Jemal": {"description": "Child of Shemega + Mohammed", "children": {}, "phone": "0911222334", "photo": "", "fixed_generation": True},
            "Mustefa": {"description": "Child of Shemega + Mohammed", "children": {}, "phone": "0911222337", "photo": "", "fixed_generation": True},
            "Rehmet": {"description": "Child of Shemega + Mohammed", "children": {}, "phone": "0911222335", "photo": "", "fixed_generation": True},
            "Bedriya": {"description": "Child of Shemega + Mohammed", "children": {}, "phone": "0911222336", "photo": "", "fixed_generation": True},
        },
    },
    "Nurseba": {
        "description": "Mother Nurseba",
        "phone": "0911333444",
        "partner": "Mohammed",
        "locked_partner": True,
        "photo": "",
        "children": {
            "Oumer": {"description": "Child of Nurseba + Mohammed", "children": {}, "phone": "0911222337", "photo": "", "fixed_generation": True},
            "Sefiya": {"description": "Child of Nurseba + Mohammed", "children": {}, "phone": "0911222338", "photo": "", "fixed_generation": True},
            "Ayro": {"description": "Child of Nurseba + Mohammed", "children": {}, "phone": "0911222339", "photo": "", "fixed_generation": True},
            "Reshad": {"description": "Child of Nurseba + Mohammed", "children": {}, "phone": "0911222340", "photo": "", "fixed_generation": True},
        },
    },
    "Dilbo": {
        "description": "Mother Dilbo",
        "phone": "0911444555",
        "partner": "Mohammed",
        "locked_partner": True,
        "photo": "",
        "children": {
            "Sadik": {"description": "Child of Dilbo + Mohammed", "children": {}, "phone": "0911222341", "photo": "", "fixed_generation": True},
            "Behra": {"description": "Child of Dilbo + Mohammed", "children": {}, "phone": "0911222342", "photo": "", "fixed_generation": True},
        },
    },
    "Rukiya": {
        "description": "Mother Rukiya",
        "phone": "0911555666",
        "partner": "Mohammed",
        "locked_partner": True,
        "photo": "",
        "children": {
            "Beytulah": {"description": "Child of Rukiya + Mohammed", "children": {}, "phone": "0911222343", "photo": "", "fixed_generation": True},
            "Leyla": {"description": "Child of Rukiya + Mohammed", "children": {}, "phone": "0911222344", "photo": "", "fixed_generation": True},
        },
    },
    "Nefissa": {
        "description": "Mother Nefissa",
        "phone": "0911666777",
        "partner": "Mohammed",
        "locked_partner": True,
        "photo": "",
        "children": {
            "Abdurezak": {"description": "Child of Nefissa + Mohammed", "children": {}, "phone": "0911222345", "photo": "", "fixed_generation": True},
        },
    },
}

# ---------------- load/save ----------------
def load_family_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = copy.deepcopy(default_family_data)
    else:
        data = copy.deepcopy(default_family_data)

    # ensure Mustefa exists (backwards compatibility)
    try:
        shem = data.setdefault("Shemega", {})
        children = shem.setdefault("children", {})
        if "Mustefa" not in children:
            children["Mustefa"] = {
                "description": "Child of Shemega + Mohammed",
                "children": {},
                "phone": "0911222337",
                "photo": "",
                "fixed_generation": True,
            }
    except Exception:
        pass

    return data

def save_family_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# ---------------- session init ----------------
if "family_data" not in st.session_state:
    st.session_state.family_data = load_family_data()
if "quiz_done" not in st.session_state:
    st.session_state.quiz_done = False
if "current_question" not in st.session_state:
    st.session_state.current_question = random.choice(quiz_questions)

# small helper that returns the container (dict) which holds the node as keys
def get_parent_container(ancestors):
    """
    ancestors: list of ancestor names (from top to immediate parent)
    returns: dict that maps child_name -> child_data (the container where the current node sits)
    """
    if not ancestors:
        return st.session_state.family_data
    node = st.session_state.family_data.get(ancestors[0])
    if node is None:
        return None
    # walk down to immediate parent
    for anc in ancestors[1:]:
        node = node.get("children", {}).get(anc)
        if node is None:
            return None
    return node.setdefault("children", {})

def save_and_rerun():
    save_family_data(st.session_state.family_data)
    st.experimental_rerun()

# ---------------- photo saving ----------------
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

# ---------------- display (recursive) ----------------
def display_family(name, data, ancestors=None):
    if ancestors is None:
        ancestors = []
    path = ancestors + [name]
    key_base = "_".join(path).replace(" ", "_")

    partner = data.get("partner", "")
    locked_partner = data.get("locked_partner", False)
    fixed_gen = data.get("fixed_generation", False)

    partner_display = "Wife of Mohammed" if name in MOTHERS_WITH_DEFAULT_PARTNER else (partner if partner else "Single")

    # expander for member
    with st.expander(f"{name} ({partner_display})", expanded=False):
        # layout: photo on left, details + buttons on right
        col1, col2 = st.columns([1, 3])
        with col1:
            photo_path = data.get("photo", "")
            if photo_path and os.path.exists(photo_path):
                st.image(photo_path, width=120)
            else:
                st.image(PLACEHOLDER_IMAGE, width=120)

        with col2:
            # Name + inline buttons at front of description area
            r1, r2 = st.columns([3, 1])
            with r1:
                st.markdown(f"### {name}")
            with r2:
                # Edit button (label includes member name)
                if st.button(f"Edit {name}", key=f"edit_btn_{key_base}"):
                    st.session_state[f"editing_{key_base}"] = True
                # Delete button - immediate delete (your requested layout)
                if st.button(f"Delete {name}", key=f"delete_btn_{key_base}"):
                    parent_container = get_parent_container(ancestors)
                    if parent_container is not None:
                        parent_container.pop(name, None)
                    else:
                        # top-level
                        st.session_state.family_data.pop(name, None)
                    save_and_rerun()

            # After buttons, show partner/description/phone
            st.markdown(f"<div class='muted'>{partner_display}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='muted'>{data.get('description','')}</div>", unsafe_allow_html=True)
            phone = data.get("phone", "")
            if phone:
                st.markdown(f"<div style='margin-top:6px;'><b>{phone}</b> <a class='phone-link' href='tel:{phone}'>📞 Call</a></div>", unsafe_allow_html=True)

            # Spacer buttons row: Add Partner or Add Child (button opens an inline form)
            # RULES:
            #  - For default wives (MOTHERS_WITH_DEFAULT_PARTNER) they already have partner -> show Add Child
            #  - For others:
            #      - if no partner: show "Add Partner" button (toggles inline form)
            #      - if partner exists: show "Add Child" button unless fixed_generation == True
            #  - fixed_generation members NEVER show Add Child (even if they have partner)
            # Use toggles in st.session_state to open inline forms (one-click to open)
            st.markdown('<div class="button-row">', unsafe_allow_html=True)

            # show Add Partner (if applicable)
            show_add_partner_flag = f"show_add_partner_{key_base}"
            if (not data.get("partner")) and (not locked_partner) and (name not in MOTHERS_WITH_DEFAULT_PARTNER):
                if st.button("💍 Add Partner", key=f"show_add_partner_btn_{key_base}"):
                    st.session_state[show_add_partner_flag] = True

            # show Add Child (if applicable)
            show_add_child_flag = f"show_add_child_{key_base}"
            can_show_child = (data.get("partner") or name in MOTHERS_WITH_DEFAULT_PARTNER) and (not fixed_gen)
            if can_show_child:
                if st.button("➕ Add Child", key=f"show_add_child_btn_{key_base}"):
                    st.session_state[show_add_child_flag] = True

            st.markdown('</div>', unsafe_allow_html=True)

            # If Add Partner form toggled -> show inline form
            if st.session_state.get(show_add_partner_flag, False):
                with st.form(key=f"add_partner_form_{key_base}"):
                    partner_name = st.text_input("Partner name", key=f"partner_input_{key_base}")
                    if st.form_submit_button("Save Partner", key=f"save_partner_{key_base}"):
                        pn = (partner_name or "").strip()
                        if pn:
                            data["partner"] = pn
                            data.setdefault("children", {})
                            # Close the form toggle and persist
                            st.session_state.pop(show_add_partner_flag, None)
                            save_and_rerun()
                        else:
                            st.error("Enter a partner name.")

            # If Add Child form toggled -> show inline form
            if st.session_state.get(show_add_child_flag, False):
                with st.form(key=f"add_child_form_{key_base}"):
                    child_name = st.text_input("Child name", key=f"child_name_{key_base}")
                    child_desc = st.text_area("Child description", key=f"child_desc_{key_base}")
                    child_phone = st.text_input("Child phone", key=f"child_phone_{key_base}")
                    child_photo = st.file_uploader("Child photo", type=["jpg","jpeg","png"], key=f"child_photo_{key_base}")
                    if st.form_submit_button("Save Child", key=f"save_child_{key_base}"):
                        cn = (child_name or "").strip()
                        if not cn:
                            st.error("Child name required.")
                        else:
                            # create child (not fixed_generation by default)
                            child_data = {
                                "description": child_desc or "",
                                "children": {},
                                "phone": child_phone or "",
                                "photo": "",
                            }
                            if child_photo is not None:
                                child_data["photo"] = save_uploaded_photo(child_photo, ancestors + [name, cn])
                            data.setdefault("children", {})[cn] = child_data
                            # close toggle and save
                            st.session_state.pop(show_add_child_flag, None)
                            save_and_rerun()

        # EDIT form (if editing flag set)
        if st.session_state.get(f"editing_{key_base}", False):
            with st.form(key=f"edit_form_{key_base}"):
                new_name = st.text_input("Member name", value=name, key=f"edit_name_{key_base}")
                new_desc = st.text_area("Description", value=data.get("description", ""), key=f"edit_desc_{key_base}")
                new_phone = st.text_input("Phone", value=data.get("phone",""), key=f"edit_phone_{key_base}")
                if locked_partner:
                    st.text_input("Partner (locked)", value=data.get("partner",""), disabled=True)
                    new_partner_value = data.get("partner","")
                else:
                    new_partner_value = st.text_input("Partner (add or edit)", value=data.get("partner",""), key=f"edit_partner_{key_base}")
                new_photo = st.file_uploader("Upload new photo (optional)", type=["jpg","jpeg","png"], key=f"edit_photo_{key_base}")

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
                            # update data fields
                            data["description"] = new_desc or ""
                            data["phone"] = new_phone or ""
                            if not locked_partner:
                                data["partner"] = new_partner_value or ""
                            if new_photo is not None:
                                data["photo"] = save_uploaded_photo(new_photo, ancestors + [new_name_clean or name])
                            # handle rename in parent container
                            if new_name_clean != name:
                                parent_container.pop(name, None)
                                parent_container[new_name_clean] = data
                            save_and_rerun()

        # Recurse for children
        for child_name, child_data in list(data.get("children", {}).items()):
            display_family(child_name, child_data, ancestors=path)


# ---------------- MAIN ----------------
st.markdown('<div class="main">', unsafe_allow_html=True)
st.markdown('<div class="cool-header">👨‍👩‍👧 Delko\'s Family Data Record</div>', unsafe_allow_html=True)

# Reset All History
if st.button("🔄 Reset All History", key="reset_all_history"):
    save_family_data(copy.deepcopy(default_family_data))
    # reinitialize session state keys
    for k in list(st.session_state.keys()):
        del st.session_state[k]
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
            st.success("✅ Correct! You can now see and edit the family tree.")
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
    # display each top-level mother
    for mother_name, mother_data in list(data.items()):
        display_family(mother_name, mother_data)

    # Save button
    if st.button("💾 Save Changes", key="save_changes"):
        save_family_data(st.session_state.family_data)
        st.success("✅ Data saved successfully")

st.markdown('</div>', unsafe_allow_html=True)
