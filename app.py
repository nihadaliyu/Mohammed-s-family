import streamlit as st
import os
import random

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Delko's Family Data Record", layout="centered")

PHOTO_DIR = "photos"
os.makedirs(PHOTO_DIR, exist_ok=True)

PLACEHOLDER_IMAGE = "https://via.placeholder.com/150?text=No+Photo"

MOTHERS_WITH_DEFAULT_PARTNER = ["Shemega", "Nurseba", "Dilbo", "Rukiya", "Nefissa"]

# ---------------- QUIZ ----------------
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

# ---------------- SESSION STATE ----------------
if "family_data" not in st.session_state:
    st.session_state.family_data = default_family_data
if "quiz_done" not in st.session_state:
    st.session_state.quiz_done = False
if "current_question" not in st.session_state:
    st.session_state.current_question = random.choice(quiz_questions)

family_data = st.session_state.family_data


# ---------------- HELPERS ----------------
def show_member(name, data, level=0):
    indent = "&nbsp;" * 4 * level
    photo = data.get("photo") if data.get("photo") else PLACEHOLDER_IMAGE
    st.markdown(f"{indent}👤 **{name}** - {data.get('description','')}")
    st.image(photo, width=100)
    st.write(f"📞 {data.get('phone', 'N/A')}")
    for child_name, child_data in data.get("children", {}).items():
        show_member(child_name, child_data, level + 1)


def delete_member(parent, member_name):
    if member_name in family_data[parent]["children"]:
        del family_data[parent]["children"][member_name]
        st.success(f"🗑️ {member_name} deleted from {parent}")


# ---------------- QUIZ ----------------
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

# ---------------- MAIN APP ----------------
else:
    st.header("🌳 Family Tree by Mothers")

    for mother_name, mother_data in family_data.items():
        with st.expander(mother_name, expanded=False):
            st.subheader(mother_name)
            st.write(f"📞 {mother_data['phone']}")
            if mother_data.get("photo"):
                st.image(mother_data["photo"], width=150)
            for child_name, child_data in mother_data["children"].items():
                show_member(child_name, child_data, level=1)

    # Add/Edit
    st.subheader("➕ Add or Edit Family Member")
    parent_name = st.selectbox("Select Parent", [""] + list(family_data.keys()))
    if parent_name:
        member_name = st.text_input("Member Name")
        description = st.text_area("Description")
        phone = st.text_input("Phone Number")
        uploaded_photo = st.file_uploader("Upload Photo", type=["jpg", "png"])

        if st.button("Save Member"):
            if member_name:
                photo_path = ""
                if uploaded_photo:
                    photo_path = os.path.join(PHOTO_DIR, uploaded_photo.name)
                    with open(photo_path, "wb") as f:
                        f.write(uploaded_photo.getbuffer())

                family_data[parent_name]["children"][member_name] = {
                    "description": description,
                    "phone": phone,
                    "photo": photo_path if photo_path else "",
                    "children": {},
                }
                st.success(f"✅ {member_name} added/updated under {parent_name}")
                st.rerun()
            else:
                st.error("⚠️ Please enter a member name.")

    # Delete
    st.subheader("🗑️ Delete Family Member")
    del_parent = st.selectbox("Select Mother for Delete", [""] + list(family_data.keys()))
    if del_parent:
        del_member = st.selectbox("Select Child to Delete", [""] + list(family_data[del_parent]["children"].keys()))
        if st.button("Delete Member"):
            if del_member:
                delete_member(del_parent, del_member)
                st.rerun()
