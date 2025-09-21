
import streamlit as st
import json
import os
import random

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Delko's Family Data Record", layout="centered")

DATA_FILE = "family_data.json"
PHOTO_DIR = "photos"
os.makedirs(PHOTO_DIR, exist_ok=True)

PLACEHOLDER_IMAGE = "https://via.placeholder.com/150?text=No+Photo"

# Mothers that should always show "Wife of Mohammed"
MOTHERS_WITH_DEFAULT_PARTNER = ["Shemega", "Nurseba", "Dilbo", "Rukiya", "Nefissa"]

# ---------------- STYLES ----------------
st.markdown(
    """
    <style>
        body { font-family: 'Segoe UI', sans-serif; background-color: #f4f6f9; }
        .card {
            display: flex; align-items: center;
            background: #ffffff; padding: 15px; border-radius: 12px;
            margin-bottom: 12px; box-shadow: 0px 6px 18px rgba(0,0,0,0.08);
        }
        .card img {
            border-radius: 8px; width: 120px; height: 120px;
            object-fit: cover; margin-right: 18px; border: 3px solid #007bff;
        }
        .card-details h3 { margin: 0; color: #007bff; }
        .phone-link {
            background: #28a745; color: white; padding: 6px 12px;
            border-radius: 8px; text-decoration: none; font-size: 14px;
        }
        .section-title { color: #444; font-weight: bold; margin-top: 10px; }
        .muted { color: #666; font-size: 13px; margin: 4px 0; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------- QUIZ ----------------
quiz_questions = [
    {"question": "how many childs did sunkemo have?", "answer": "9"},
    {"question": "How many wives did Mohammed have?", "answer": "5"},
    {"question": "how many childs did mother Shemega have ?", "answer": "5"},
    {"question": "how many childs did mother Nurseba have?", "answer": "9"},
    {"question": "how many childs did mother Dilbo have?", "answer": "4"},
]

# ---------------- DEFAULT DATA ----------------
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

# ---------------- DATA HANDLING ----------------
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except Exception:
            save_data(default_family_data)
            return default_family_data
    save_data(default_family_data)
    return default_family_data

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

family_data = load_data()

# Ensure the five mothers always have partner = "Mohammed" and locked_partner True
for mom in MOTHERS_WITH_DEFAULT_PARTNER:
    if mom not in family_data:
        family_data[mom] = default_family_data[mom]
    else:
        family_data[mom]["partner"] = "Mohammed"
        family_data[mom]["locked_partner"] = True
save_data(family_data)

# ---------------- HELPERS ----------------
def save_uploaded_photo(uploaded_file, path_list):
    if not uploaded_file:
        return ""
    safe_name = "_".join(path_list).replace(" ", "_")
    ext = os.path.splitext(uploaded_file.name)[1].lower()
    filename = f"{safe_name}{ext}"
    filepath = os.path.join(PHOTO_DIR, filename)
    with open(filepath, "wb") as out:
        out.write(uploaded_file.getbuffer())
    return filepath

def delete_by_path(data_dict, path):
    if not path:
        return False
    if len(path) == 1:
        key = path[0]
        if key in data_dict:
            del data_dict[key]
            return True
        return False
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

def handle_delete():
    if "delete_target" in st.session_state:
        path_to_delete = st.session_state["delete_target"]
        deleted = delete_by_path(family_data, path_to_delete)
        if deleted:
            save_data(family_data)
            st.success(f"{path_to_delete[-1]} deleted ✅")
        else:
            st.error("Could not delete — path not found.")
        del st.session_state["delete_target"]
        st.rerun()

# ---------------- DISPLAY ----------------
def display_card(name, data):
    photo_path = data.get("photo", "")
    img_display = photo_path if photo_path and os.path.exists(photo_path) else PLACEHOLDER_IMAGE
    partner = data.get("partner", "")
    partner_display = "Wife of Mohammed" if name in MOTHERS_WITH_DEFAULT_PARTNER else (f"Partner: {partner}" if partner else "")
    phone_html = f"<a href='tel:{data.get('phone','')}' class='phone-link'>📞 Call</a>" if data.get("phone") else ""
    st.markdown(
        f"""
        <div class="card">
            <img src="{img_display}" alt="{name}">
            <div class="card-details">
                <h3>{name}</h3>
                <div class="muted">{partner_display}</div>
                <div class="muted">{data.get("description","")}</div>
                <div style="margin-top:6px;"><b>{data.get("phone","")}</b> {phone_html}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def display_family(name, data, ancestors=None):
    if ancestors is None: ancestors = []
    path = ancestors + [name]
    key_base = "_".join(path).replace(" ", "_")
    partner = data.get("partner", "")
    locked_partner = data.get("locked_partner", False)
    partner_display = "Wife of Mohammed" if name in MOTHERS_WITH_DEFAULT_PARTNER else (partner if partner else "Single")

    with st.expander(f"{name} ({partner_display})", expanded=False):
        display_card(name, data)

        if data.get("children"):
            st.markdown(f"<p class='section-title'>👶 Children of {name}</p>", unsafe_allow_html=True)
            for child_name, child_data in data["children"].items():
                display_family(child_name, child_data, ancestors=path)

        # Add Partner
        if not partner and not locked_partner and name not in MOTHERS_WITH_DEFAULT_PARTNER:
            if st.button(f"Add Partner for {name}", key=f"btn_partner_{key_base}"):
                st.session_state[f"adding_partner_{key_base}"] = True
        if st.session_state.get(f"adding_partner_{key_base}", False):
            with st.form(f"partner_form_{key_base}"):
                partner_name = st.text_input("Enter partner's name")
                submit_partner = st.form_submit_button("Save Partner")
                if submit_partner and partner_name:
                    data["partner"] = partner_name
                    save_data(family_data)
                    st.success(f"Partner {partner_name} added for {name} ✅")
                    st.session_state[f"adding_partner_{key_base}"] = False
                    st.rerun()

        # Add Child
        if name not in MOTHERS_WITH_DEFAULT_PARTNER and partner:
            if st.button(f"Add Child to {name}", key=f"btn_child_{key_base}"):
                st.session_state[f"adding_child_{key_base}"] = True
        if st.session_state.get(f"adding_child_{key_base}", False):
            with st.form(f"child_form_{key_base}"):
                new_child_name = st.text_input("Enter child name")
                new_child_desc = st.text_area("Enter child description")
                new_child_phone = st.text_input("Enter phone number")
                new_child_photo = st.file_uploader("Upload photo", type=["jpg", "png", "jpeg"], key=f"uploader_child_{key_base}")
                submit_child = st.form_submit_button("Save Child")
                if submit_child and new_child_name:
                    photo_path = save_uploaded_photo(new_child_photo, path + [new_child_name]) if new_child_photo else ""
                    data.setdefault("children", {})[new_child_name] = {
                        "description": new_child_desc, "children": {}, "phone": new_child_phone, "photo": photo_path,
                    }
                    save_data(family_data)
                    st.success(f"Child {new_child_name} added under {name} ✅")
                    st.session_state[f"adding_child_{key_base}"] = False
                    st.rerun()

        # Edit
        if st.button(f"✏️ Edit {name}", key=f"btn_edit_{key_base}"):
            st.session_state[f"editing_{key_base}"] = True
        if st.session_state.get(f"editing_{key_base}", False):
            with st.form(f"edit_form_{key_base}"):
                new_desc = st.text_area("Update description", value=data.get("description", ""))
                new_phone = st.text_input("Update phone number", value=data.get("phone", ""))
                partner_input = st.text_input("Update partner's name", value=partner)
                new_photo = st.file_uploader("Upload/Replace photo (optional)", type=["jpg", "png", "jpeg"], key=f"uploader_edit_{key_base}")
                submit_edit = st.form_submit_button("Save Changes")
                if submit_edit:
                    data["description"] = new_desc
                    data["phone"] = new_phone
                    data["partner"] = partner_input
                    if new_photo:
                        data["photo"] = save_uploaded_photo(new_photo, path)
                    if name in MOTHERS_WITH_DEFAULT_PARTNER:
                        data["partner"] = "Mohammed"
                        data["locked_partner"] = True
                    save_data(family_data)
                    st.success(f"{name} updated ✅")
                    st.session_state[f"editing_{key_base}"] = False
                    st.rerun()

        # Delete
        delete_btn_key = f"btn_delete_{key_base}"
        delete_state_key = f"confirm_delete_{key_base}"
        if st.button(f"🗑️ Delete {name}", key=delete_btn_key):
            st.session_state[delete_state_key] = True
        if st.session_state.get(delete_state_key, False):
            st.warning(f"Are you sure you want to delete {name}?")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Yes, Delete", key=f"confirm_{key_base}"):
                    st.session_state["delete_target"] = path
                    st.session_state[delete_state_key] = False
                    st.rerun()
            with col2:
                if st.button("Cancel", key=f"cancel_{key_base}"):
                    st.session_state[delete_state_key] = False
                    st.rerun()

# ---------------- APP LAYOUT ----------------
st.title("👨‍👩‍👧 Delko's Family Data Record")

# Quiz flow
if "quiz_done" not in st.session_state:
    st.session_state.quiz_done = False
if "current_question" not in st.session_state:
    st.session_state.current_question = random.choice(quiz_questions)

if not st.session_state.quiz_done:
    st.header("📖 Please answer Family Quiz to login")
    question = st.session_state.current_question["question"]
    ans = st.text_input(question, key="quiz_answer")
    if st.button("Submit Quiz", key="quiz_submit"):
        if ans.strip().lower() == st.session_state.current_question["answer"].lower():
            st.session_state.quiz_done = True
            st.success("✅ Correct!")
            st.rerun()
        else:
            st.error("❌ Wrong! Try again.")
            st.session_state.current_question = random.choice(quiz_questions)
else:
    st.header("🌳 Family Tree by Mothers")
    handle_delete()
    for mother_name, mother_data in family_data.items():
        display_family(mother_name, mother_data)
