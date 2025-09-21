import streamlit as st
import json
import os
import random

# Custom CSS for styling
st.markdown(
    """
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f0f4f8;
        }
        .expander-header {
            font-weight: bold;
            color: #4a4a4a;
        }
        .button {
            background-color: #007bff;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
        }
        .button:hover {
            background-color: #0056b3;
        }
        .phone-button {
            background-color: #28a745;
            color: white;
            padding: 5px 10px;
            border-radius: 5px;
            text-decoration: none;
        }
        .section-title {
            color: #007bff;
        }
        .header {
            text-align: center;
            margin-bottom: 20px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

DATA_FILE = "family_data.json"

# ---------------- QUIZ SECTION ----------------
quiz_questions = [
    {"question": "Who is the father of kere?", "answer": "Reshad"},
    {"question": "How many wives did Mohammed have?", "answer": "5"},
    {"question": "First child of Nurseba?", "answer": "Oumer"},
    {"question": "Who is the youngest mother?", "answer": "Nefissa"},
    {"question": "Who is the mother of Sadik?", "answer": "Dilbo"},
    {"question": "Who is the first wife of Mohammed?", "answer": "Shemega"},
]

# ---------------- INITIAL FAMILY DATA ----------------
default_family_data = {
    "Shemega": {
        "description": "Mother Shemega",
        "phone": "0911000000",
        "partner": "Mohammed",
        "locked_partner": True,
        "children": {},
        "photo": None
    },
    "Nurseba": {
        "description": "Mother Nurseba",
        "phone": "0911333444",
        "partner": "Mohammed",
        "locked_partner": True,
        "children": {},
        "photo": None
    },
    "Dilbo": {
        "description": "Mother Dilbo",
        "phone": "0911444555",
        "partner": "Mohammed",
        "locked_partner": True,
        "children": {},
        "photo": None
    },
    "Rukiya": {
        "description": "Mother Rukiya",
        "phone": "0911555666",
        "partner": "Mohammed",
        "locked_partner": True,
        "children": {},
        "photo": None
    },
    "Nefissa": {
        "description": "Mother Nefissa",
        "phone": "0911666777",
        "partner": "Mohammed",
        "locked_partner": True,
        "children": {},
        "photo": None
    },
}

# ---------------- DATA HANDLING ----------------
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return default_family_data

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

family_data = load_data()

# ---------------- FAMILY DISPLAY ----------------
def display_family(name, data, parent_key="root"):
    partner = data.get("partner", "")
    locked_partner = data.get("locked_partner", False)

    with st.expander(f"{name} ({partner if partner else 'Single'})", expanded=False):
        st.write(data.get("description", ""))
        
        # Show photo if available
        if data.get("photo"):
            st.image(data["photo"], caption=name, use_column_width=True)

        # Phone button
        if "phone" in data and data["phone"]:
            st.markdown(f"<a href='tel:{data['phone']}' class='phone-button'>📞 Call {name}</a>", unsafe_allow_html=True)

        # CHILDREN display
        if data.get("children"):
            st.subheader(f"Children of {name}")
            for child_name, child_data in data["children"].items():
                display_family(child_name, child_data, parent_key=f"{parent_key}_{child_name}")

        # Adding partner and children logic...

        # DELETE
        if st.button(f"🗑️ Delete {name}", key=f"delete_{parent_key}_{name}"):
            if st.confirm("Are you sure you want to delete this member?"):
                delete_family_member(name)

# ---------------- DELETE HANDLER ----------------
def delete_family_member(name):
    if name in family_data:
        del family_data[name]
        save_data(family_data)
        st.success(f"{name} deleted ✅")
        st.experimental_rerun()

# ---------------- APP ----------------
st.set_page_config(page_title="Delko's Family Data Record", layout="centered")

st.title("👨‍👩‍👧 Delko's Family Data Record")

# Adding photo functionality
for member in family_data.keys():
    uploaded_file = st.file_uploader(f"Upload photo for {member}", type=["jpg", "jpeg", "png"], key=member)
    if uploaded_file is not None:
        family_data[member]["photo"] = uploaded_file.read()  # Store the image data
        save_data(family_data)  # Save the updated data
        st.success(f"Photo uploaded for {member}!")

for mother_name, mother_data in family_data.items():
    display_family(mother_name, mother_data)
