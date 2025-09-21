import streamlit as st
import json
import os
import copy
import uuid
import random
import traceback

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Delko's Family Data Record", layout="centered")

DATA_FILE = "family_data.json"  # optional local load/save (useful for local dev)
PHOTO_DIR = "photos"
os.makedirs(PHOTO_DIR, exist_ok=True)

PLACEHOLDER_IMAGE = "https://via.placeholder.com/150?text=No+Photo"

# These mothers must always show Wife of Mohammed and have locked_partner True
MOTHERS_WITH_DEFAULT_PARTNER = ["Shemega", "Nurseba", "Dilbo", "Rukiya", "Nefissa"]

# ---------------- STYLES ----------------
st.markdown(
    """
    <style>
        body { font-family: 'Segoe UI', sans-serif; background-color: #f4f6f9; }
        .card {
            display:flex; align-items:center; background:#fff; padding:12px;
            border-radius:12px; margin-bottom:10px; box-shadow:0 6px 18px rgba(0,0,0,0.06);
        }
        .card img { border-radius:8px; width:120px; height:120px; object-fit:cover; margin-right:14px; border:3px solid #007bff; }
        .card-details h3 { margin:0; color:#007bff; }
        .phone-link { background:#28a745; color:white; padding:6px 10px; border-radius:8px; text-decoration:none; }
        .muted { color:#666; font-size:13px; margin:4px 0; }
        .section-title { color:#444; font-weight:bold; margin-top:10px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------- QUIZ QUESTIONS ----------------
quiz_questions = [
    {"question": "how many childs did sunkemo have?", "answer": "9"},
    {"question": "How many wives did Mohammed have?", "answer": "5"},
    {"question": "how many childs did mother Shemega have ?", "answer": "5"},
    {"question": "how many childs did mother Nurseba have?", "answer": "4"},
    {"question": "how many childs did mother Dilbo have?", "answer": "2"},
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

# ---------------- HELPERS: load/merge session & file ----------------
def merge_defaults_into(data, defaults):
    """Add missing mothers/children from defaults without overwriting existing data."""
    for mom, mom_val in defaults.items():
        if mom not in data:
            data[mom] = copy.deepcopy(mom_val)
        else:
            # ensure keys exist
            data[mom].setdefault("description", mom_val.get("description", ""))
            data[mom].setdefault("phone", mom_val.get("phone", ""))
            data[mom].setdefault("photo", mom_val.get("photo", ""))
            data[mom].setdefault("children", {})
            # add missing default children
            for child_name, child_val in mom_val.get("children", {}).items():
                if child_name not in data[mom]["children"]:
                    data[mom]["children"][child_name] = copy.deepcopy(child_val)
    # enforce locked partner for special mothers
    for mom in MOTHERS_WITH_DEFAULT_PARTNER:
        if mom in data:
            data[mom]["partner"] = "Mohammed"
            data[mom]["locked_partner"] = True


def load_initial_data():
    """
    Try loading from local file (useful in local dev). Then merge defaults and return data copy.
    For deployed apps the local file might not exist; defaults ensure all children (Mustefa) exist.
    """
    data = {}
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = {}
    if not data:
        data = copy.deepcopy(default_family_data)
    else:
        # merge defaults if file existed but new defaults were added later
        merge_defaults_into(data, default_family_data)
    # ensure required mothers are locked to Mohammed
    for mom in MOTHERS_WITH_DEFAULT_PARTNER:
        data.setdefault(mom, copy.deepcopy(default_family_data[mom]))
        data[mom]["partner"] = "Mohammed"
        data[mom]["locked_partner"] = True
    return data


def save_local_file(data):
    """Optional: save to local JSON file (works for local dev)."""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        st.error(f"Unable to write local file: {e}")
        return False


# Initialize session_state.family_data on first run
if "family_data" not in st.session_state:
    st.session_state.family_data = load_initial_data()

# convenience local reference (always point to session_state)
def get_data():
    return st.session_state.family_data


def set_data(d):
    st.session_state.family_data = d


# ---------------- PHOTO SAVE ----------------
def save_uploaded_photo(uploaded_file, path_list):
    """Save uploaded photo to photos dir and return path; create a unique filename."""
    if not uploaded_file:
        return ""
    safe_base = "_".join(path_list).strip().replace(" ", "_")
    _, ext = os.path.splitext(uploaded_file.name)
    ext = ext.lower() if ext else ".jpg"
    fname = f"{safe_base}_{uuid.uuid4().hex[:8]}{ext}"
    filepath = os.path.join(PHOTO_DIR, fname)
    try:
        with open(filepath, "wb") as out:
            out.write(uploaded_file.getbuffer())
        return filepath
    except Exception as e:
        st.error(f"Failed to save photo: {e}")
        return ""


# ---------------- DELETE HELPER ----------------
def delete_by_path(data_dict, path):
    """
    Delete the node at path (list) from the nested data structure.
    Example path: ['Shemega', 'Sunkemo', 'Ammar']
    Returns True if deleted.
    """
    if not path:
        return False
    # top-level deletion
    if len(path) == 1:
        key = path[0]
        if key in data_dict:
            del data_dict[key]
            return True
        return False
    # traverse to parent children dict
    cur = data_dict
    for p in path[:-1]:
        if p in cur:
            cur = cur[p].get("children", {})
        else:
            return False
    target = path[-1]
    if target in cur:
        del cur[target]
        return True
    return False


# ---------------- DISPLAY HELPERS ----------------
def display_card(name, data):
    """Visual card with image and details (uses Streamlit columns)."""
    col1, col2 = st.columns([1, 3])
    with col1:
        photo_path = data.get("photo", "")
        if photo_path and os.path.exists(photo_path):
            st.image(photo_path, width=120)
        else:
            st.image(PLACEHOLDER_IMAGE, width=120)
    with col2:
        st.markdown(f"### {name}")
        partner = data.get("partner", "")
        partner_display = "Wife of Mohammed" if name in MOTHERS_WITH_DEFAULT_PARTNER else (f"Partner: {partner}" if partner else "Single")
        st.markdown(f"<div class='muted'>{partner_display}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='muted'>{data.get('description','')}</div>", unsafe_allow_html=True)
        phone = data.get("phone", "")
        if phone:
            st.markdown(f"<div style='margin-top:6px;'><b>{phone}</b> <a class='phone-link' href='tel:{phone}'>📞 Call</a></div>", unsafe_allow_html=True)


def display_family(name, data, ancestors=None):
    """
    Recursively show member and provide add/edit/delete controls.
    ancestors: list of ancestor names (excluding current name)
    """
    if ancestors is None:
        ancestors = []
    path = ancestors + [name]
    key_base = "_".join(path).replace(" ", "_")

    partner = data.get("partner", "")
    locked_partner = data.get("locked_partner", False)
    partner_display = "Wife of Mohammed" if name in MOTHERS_WITH_DEFAULT_PARTNER else (partner if partner else "Single")

    with st.expander(f"{name} ({partner_display})", expanded=False):
        display_card(name, data)

        # children list
        children = data.get("children", {})
        if children:
            st.markdown(f"<p class='section-title'>👶 Children of {name}</p>", unsafe_allow_html=True)
            for child_name, child_data in list(children.items()):
                display_family(child_name, child_data, ancestors=path)

        # ADD PARTNER (only if no partner, not locked, and not one of specified mothers)
        if not partner and not locked_partner and name not in MOTHERS_WITH_DEFAULT_PARTNER:
            if st.button(f"Add Partner for {name}", key=f"btn_partner_{key_base}"):
                st.session_state[f"adding_partner_{key_base}"] = True

        if st.session_state.get(f"adding_partner_{key_base}", False):
            with st.form(f"partner_form_{key_base}", clear_on_submit=False):
                partner_name = st.text_input("Enter partner's name", key=f"input_partner_{key_base}")
                submit_partner = st.form_submit_button("Save Partner")
                if submit_partner and partner_name:
                    # set and persist
                    d = get_data()
                    # traverse to node by path
                    node = d
                    for p in path:
                        if p == name:
                            node = d[name] if len(path) == 1 else None
                    # easier: direct reference
                    cur = d
                    for p in path[:-1]:
                        cur = cur[p]["children"]
                    # cur is parent's children dict if adding partner to an existing person; but simpler: we already have reference 'data'
                    data["partner"] = partner_name
                    set_data(d)
                    st.success(f"Partner {partner_name} added for {name} ✅")
                    st.session_state[f"adding_partner_{key_base}"] = False
                    st.rerun()

        # ADD CHILD (only for non-specified mothers and only if they have a partner)
        if name not in MOTHERS_WITH_DEFAULT_PARTNER and partner:
            if st.button(f"Add Child to {name}", key=f"btn_child_{key_base}"):
                st.session_state[f"adding_child_{key_base}"] = True

        if st.session_state.get(f"adding_child_{key_base}", False):
            with st.form(f"child_form_{key_base}", clear_on_submit=False):
                new_child_name = st.text_input("Enter child name", key=f"child_name_{key_base}")
                new_child_desc = st.text_area("Enter child description", key=f"child_desc_{key_base}")
                new_child_phone = st.text_input("Enter phone number", key=f"child_phone_{key_base}")
                new_child_photo = st.file_uploader("Upload photo", type=["jpg", "png", "jpeg"], key=f"uploader_child_{key_base}")
                submit_child = st.form_submit_button("Save Child")
                if submit_child and new_child_name:
                    photo_path = ""
                    if new_child_photo:
                        photo_path = save_uploaded_photo(new_child_photo, path + [new_child_name])
                    d = get_data()
                    parent_node = d
                    # traverse to this person's dict using path
                    for p in path[:-1]:
                        parent_node = parent_node[p]["children"]
                    # parent_node is children dict of parent (if length>1) or top-level dict if parent is top-level
                    # easier: just use direct reference to 'data' passed to function
                    data.setdefault("children", {})[new_child_name] = {
                        "description": new_child_desc,
                        "children": {},
                        "phone": new_child_phone,
                        "photo": photo_path,
                    }
                    set_data(d)
                    st.success(f"Child {new_child_name} added under {name} ✅")
                    st.session_state[f"adding_child_{key_base}"] = False
                    st.rerun()

        # EDIT
        if st.button(f"✏️ Edit {name}", key=f"btn_edit_{key_base}"):
            st.session_state[f"editing_{key_base}"] = True

        if st.session_state.get(f"editing_{key_base}", False):
            with st.form(f"edit_form_{key_base}", clear_on_submit=False):
                new_desc = st.text_area("Update description", value=data.get("description", ""), key=f"edit_desc_{key_base}")
                new_phone = st.text_input("Update phone number", value=data.get("phone", ""), key=f"edit_phone_{key_base}")
                partner_input = st.text_input("Update partner's name", value=partner, key=f"edit_partner_{key_base}")
                new_photo = st.file_uploader("Upload/Replace photo (optional)", type=["jpg", "png", "jpeg"], key=f"uploader_edit_{key_base}")
                submit_edit = st.form_submit_button("Save Changes")
                if submit_edit:
                    d = get_data()
                    data["description"] = new_desc
                    data["phone"] = new_phone
                    # enforce locked mother partner if applicable
                    if name in MOTHERS_WITH_DEFAULT_PARTNER:
                        data["partner"] = "Mohammed"
                        data["locked_partner"] = True
                    else:
                        data["partner"] = partner_input
                    if new_photo:
                        data["photo"] = save_uploaded_photo(new_photo, path)
                    set_data(d)
                    st.success(f"{name} updated ✅")
                    st.session_state[f"editing_{key_base}"] = False
                    st.rerun()

        # DELETE
        delete_state_key = f"confirm_delete_{key_base}"
        if st.button(f"🗑️ Delete {name}", key=f"btn_delete_{key_base}"):
            st.session_state[delete_state_key] = True

        if st.session_state.get(delete_state_key, False):
            st.warning(f"Are you sure you want to delete {name}?")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Yes, Delete", key=f"confirm_{key_base}"):
                    d = get_data()
                    ok = delete_by_path(d, path)
                    if ok:
                        set_data(d)
                        st.success(f"{name} deleted ✅")
                    else:
                        st.error("Could not delete — path not found.")
                    st.session_state[delete_state_key] = False
                    st.rerun()
            with col2:
                if st.button("Cancel", key=f"cancel_{key_base}"):
                    st.session_state[delete_state_key] = False
                    st.rerun()


# ---------------- APP LAYOUT ----------------
def main():
    st.title("👨‍👩‍👧 Delko's Family Data Record")

    # Show a small hint about persistence
    st.info("Data is stored in-session while the app runs. Use Export/Import to persist between app restarts or set up an external DB for permanent storage.")

    # QUIZ state initialization (works on first click)
    if "quiz_done" not in st.session_state:
        st.session_state.quiz_done = False
    if "current_question" not in st.session_state or not st.session_state.current_question:
        st.session_state.current_question = random.choice(quiz_questions)

    if not st.session_state.quiz_done:
        st.header("📖 Please answer Family Quiz to login")
        question = st.session_state.current_question["question"]
        # Keep quiz input persistent in session to avoid needing double-click
        if "quiz_answer" not in st.session_state:
            st.session_state.quiz_answer = ""
        st.text_input(question, key="quiz_answer")
        if st.button("Submit Quiz", key="quiz_submit"):
            ans = (st.session_state.get("quiz_answer") or "").strip().lower()
            if ans and ans == st.session_state.current_question["answer"].lower():
                st.session_state.quiz_done = True  # set before rerun
                st.success("✅ Correct!")
                st.rerun()
            else:
                st.error("❌ Wrong! Try again.")
                st.session_state.current_question = random.choice(quiz_questions)
    else:
        # Controls: Export / Import / Reset / Save local (dev)
        colA, colB, colC, colD = st.columns([2, 2, 2, 2])
        with colA:
            # Export JSON
            json_bytes = json.dumps(get_data(), indent=4, ensure_ascii=False).encode("utf-8")
            st.download_button("⬇️ Export JSON", data=json_bytes, file_name="family_data_export.json", mime="application/json")
        with colB:
            uploaded = st.file_uploader("⬆️ Import JSON (replace data)", type=["json"], key="import_json")
            if uploaded:
                try:
                    new_data = json.load(uploaded)
                    # merge defaults to avoid accidental removal of required structure
                    merge_defaults_into(new_data, default_family_data)
                    set_data(new_data)
                    st.success("Imported data set as current family data ✅")
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to import JSON: {e}")
        with colC:
            if st.button("🔁 Reset to defaults"):
                st.session_state.family_data = copy.deepcopy(default_family_data)
                st.success("Data reset to defaults ✅")
                st.rerun()
        with colD:
            if st.button("💾 Save local file (dev only)"):
                ok = save_local_file(get_data())
                if ok:
                    st.success("Saved to local file (DATA_FILE).")

        st.header("🌳 Family Tree by Mothers")
        try:
            # display in insertion order
            data = get_data()
            for mother_name, mother_data in data.items():
                display_family(mother_name, mother_data)
        except Exception:
            st.error("An unexpected error occurred while rendering the tree. See details below.")
            st.exception(traceback.format_exc())


if __name__ == "__main__":
    main()
