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
                # Ensure Mustefa is included under Shemega
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

            # ADD PARTNER button
            if not partner and not locked_partner and name not in MOTHERS_WITH_DEFAULT_PARTNER:
                if st.button(f"Add Partner for {name}", key=f"add_partner_{key_base}"):
                    new_partner_name = st.text_input("Enter partner's name", key=f"partner_input_{key_base}")
                    if st.button("Save Partner", key=f"save_partner_{key_base}"):
                        data["partner"] = new_partner_name
                        save_family_data(st.session_state.family_data)
                        st.success(f"Partner {new_partner_name} added for {name} ✅")
                        st.experimental_rerun()

            # ADD CHILD button
            if partner and name not in MOTHERS_WITH_DEFAULT_PARTNER:
                if st.button(f"Add Child to {name}", key=f"add_child_{key_base}"):
                    with st.form(key=f"child_form_{key_base}"):
                        new_child_name = st.text_input("Enter child's name", key=f"child_name_{key_base}")
                        new_child_desc = st.text_area("Enter child's description", key=f"child_desc_{key_base}")
                        new_child_phone = st.text_input("Enter child's phone number", key=f"child_phone_{key_base}")
                        uploaded_photo = st.file_uploader("Upload child's photo", type=["jpg", "jpeg", "png"], key=f"child_photo_{key_base}")

                        if st.form_submit_button("Save Child"):
                            child_data = {
                                "description": new_child_desc,
                                "children": {},
                                "phone": new_child_phone,
                            }
                            if uploaded_photo is not None:
                                child_data["photo"] = save_uploaded_photo(uploaded_photo, [name, new_child_name])
                            data["children"][new_child_name] = child_data
                            save_family_data(st.session_state.family_data)
                            st.success(f"Child {new_child_name} added under {name} ✅")
                            st.experimental_rerun()

            # Edit and Delete buttons for the current member
            if st.button(f"✏️ Edit {name}", key=f"edit_{key_base}"):
                with st.form(key=f"edit_form_{key_base}"):
                    updated_description = st.text_area("Update description", value=data.get("description", ""))
                    updated_phone = st.text_input("Update phone number", value=data.get("phone", ""))
                    if st.form_submit_button("Save Changes"):
                        data["description"] = updated_description
                        data["phone"] = updated_phone
                        save_family_data(st.session_state.family_data)
                        st.success(f"{name} updated successfully ✅")
                        st.experimental_rerun()

            if st.button(f"🗑️ Delete {name}", key=f"delete_{key_base}"):
                if st.button("Confirm Delete"):
                    del st.session_state.family_data[name]
                    save_family_data(st.session_state.family_data)
                    st.success(f"{name} deleted successfully ✅")
                    st.experimental_rerun()

        # Display children recursively
        for child_name, child_data in data.get("children", {}).items():
            display_family(child_name, child_data, ancestors=path)

# ---------------- MAIN ----------------
st.title("👨‍👩‍👧 Delko's Family Data Record")

if not st.session_state.quiz_done:
    st.header("📖 Please answer Family Quiz to login")
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
    st.header("🌳 Family Tree by Mothers")
    data = st.session_state.family_data
    for mother_name, mother_data in data.items():
        display_family(mother_name, mother_data)

    # Save button
    if st.button("💾 Save Changes"):
        save_family_data(st.session_state.family_data)
        st.success("✅ Data saved successfully")
