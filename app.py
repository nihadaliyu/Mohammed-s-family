#          ONE 11111111
# import random
# import streamlit as st
# import json
# import os
# from PIL import Image
# import io
#
# st.set_page_config(page_title="Delko Family Tree", layout="wide")
# st.title("Delko Family Tree")
#
# DATA_FILE = "family_data.json"
# # ---------------- QUIZ SECTION ----------------
# quiz_questions = [
#     {"question": "who is the youngest child in the mother Nursebe ?", "answer": "Neja"},
#     {"question": "How many wives did Mohammed have?", "answer": "5"},
#     {"question": "how many childs did Nefisa mother have?", "answer": "1"},
#     {"question": "which mother had Sherefa as a child?", "answer": "Nursebe"},
#     {"question": "Which mother has Sadik as a child?", "answer": "Dilbo"},
#     {"question": "who is the elder child in the mother Shemege?", "answer": "Sunkemo"},
# ]
#
# # --- Pick a random question ONCE ---
# if "quiz" not in st.session_state:
#     st.session_state.quiz = random.choice(quiz_questions)
#     st.session_state.quiz_passed = False
#
# # --- Display the random quiz ---
# st.subheader("📝 Quick Quiz")
# question = st.session_state.quiz["question"]
# correct_answer = st.session_state.quiz["answer"]
#
# user_answer = st.text_input(question)
#
# if user_answer:
#     if user_answer.strip().lower() == correct_answer:
#         st.success("✅ Correct! You may now access the family records.")
#         st.session_state.quiz_passed = True
#     else:
#         st.error("❌ Wrong answer. Try again!")
#         st.session_state.quiz_passed = False
#
# # --- Only show family tree if quiz is passed ---
# if st.session_state.quiz_passed:
#     st.header("👨‍👩‍👧 Delko Family Members")
#     st.write("Now you can explore the family records!")

# if "quiz_done" not in st.session_state:
#     st.session_state.quiz_done = False
#
# if not st.session_state.quiz_done:
#     st.header("📖 Quick Family Quiz")
#     # Pick 5 random questions
#     selected_questions =random.sample(quiz_questions, k=5)
#
#     answers = {}
#     score = 0
#
#     with st.form("quiz_form"):
#         for i, q in enumerate(selected_questions):
#             st.write(f"**Q{i+1}: {q['question']}**")
#             answers[i] = st.text_input(f"Your Answer for Q{i+1}", key=f"q_{i}")
#         submitted = st.form_submit_button("Submit Quiz")
#
#     if submitted:
#         for i, q in enumerate(selected_questions):
#             if answers[i].strip().lower() == q["answer"].lower():
#                 score += 1
#         st.success(f"✅ You scored {score} / {len(selected_questions)}")
#         st.session_state.quiz_done = True

# ---------------- FAMILY TREE SECTION ----------------
# if st.session_state.quiz_done:

# --- Load or Initialize Data ---
# if os.path.exists(DATA_FILE):
#     with open(DATA_FILE, "r", encoding="utf-8") as f:
#         family_data = json.load(f)
# else:
#     family_data = {
#         "Shemege": {"description": "Mother Shemege", "photo": None, "children": {}},
#         "Nursebe": {"description": "Mother Nursebe", "photo": None, "children": {}},
#         "Dilbo": {"description": "Mother Dilbo", "photo": None, "children": {}},
#         "Rukiya": {"description": "Mother Rukiya", "photo": None, "children": {}},
#         "Nefissa": {"description": "Mother Nefissa", "photo": None, "children": {}}
#     }
#
# # --- Save Data ---
# def save_data():
#     with open(DATA_FILE, "w", encoding="utf-8") as f:
#         json.dump(family_data, f, ensure_ascii=False, indent=4)
#
# # --- Display Member Function ---
# def display_member(name, data, is_mother=False, parent_key=None):
#     if parent_key is None:
#         parent_key = name
#
#     with st.expander(name, expanded=False):
#         st.write(data.get("description", ""))
#         st.write("👨 Father: Mohammed")
#
#         # Show photo if exists
#         if data.get("photo"):
#             try:
#                 img_bytes = bytes.fromhex(data["photo"])
#                 image = Image.open(io.BytesIO(img_bytes))
#                 st.image(image, width=150)
#             except:
#                 pass
#
#         # Display children recursively
#         if data.get("children"):
#             st.subheader(f"Children of {name}:")
#             for child_name, child_data in data["children"].items():
#                 display_member(child_name, child_data, is_mother=False, parent_key=f"{parent_key}_{child_name}")
#
#         # Add Child button and form (skip for mothers)
#         if not is_mother:
#             if f"show_form_{parent_key}" not in st.session_state:
#                 st.session_state[f"show_form_{parent_key}"] = False
#
#             if not st.session_state[f"show_form_{parent_key}"]:
#                 if st.button(f"Add Child to {name}", key=f"button_{parent_key}"):
#                     st.session_state[f"show_form_{parent_key}"] = True
#
#             if st.session_state[f"show_form_{parent_key}"]:
#                 with st.form(f"form_{parent_key}"):
#                     new_name = st.text_input("Child Name")
#                     new_description = st.text_area("Description")
#                     new_photo = st.file_uploader("Upload Photo", type=["png","jpg","jpeg"])
#                     submitted = st.form_submit_button("Submit Child")
#                     if submitted:
#                         if not new_name:
#                             st.warning("Please enter a name.")
#                         elif new_name in data["children"]:
#                             st.warning(f"{new_name} already exists under {name}.")
#                         else:
#                             # Save photo as hex
#                             photo_hex = new_photo.read().hex() if new_photo else None
#                             # Add new child as new generation
#                             data["children"][new_name] = {
#                                 "description": new_description,
#                                 "photo": photo_hex,
#                                 "children": {}
#                             }
#                             save_data()
#                             st.success(f"Child {new_name} added under {name} ✅")
#                             st.session_state[f"show_form_{parent_key}"] = False
#
# # --- Display All Mothers ---
# st.header("Mothers of the Family")
# for mother_name, mother_data in family_data.items():
#     display_member(mother_name, mother_data, is_mother=True)
#
#
# import streamlit as st
# import json
# import os
#
# st.set_page_config(page_title="Delko Family Tree", layout="wide")
# st.title("Delko Family Tree")
#
# # --- JSON FILE PATH ---
# DATA_FILE = "family_data.json"
#
# # --- LOAD DATA OR INITIALIZE ---
# if os.path.exists(DATA_FILE):
#     with open(DATA_FILE, "r", encoding="utf-8") as f:
#         family_data = json.load(f)
# else:
#     # Initialize with mothers and children
#     family_data = {
#         "Shemega": {"description": "Mother Shemega", "photo": None, "children": {
#             "Sunkemo": {"description": "", "photo": None, "children": {}},
#             "Jemal": {"description": "", "photo": None, "children": {}},
#             "Rehmet": {"description": "", "photo": None, "children": {}},
#             "Bedriya": {"description": "", "photo": None, "children": {}}
#         }},
#         "Nurseba": {"description": "Mother Nurseba", "photo": None, "children": {
#             "Oumer": {"description": "", "photo": None, "children": {}},
#             "Sefiya": {"description": "", "photo": None, "children": {}},
#             "Ayro": {"description": "", "photo": None, "children": {}},
#             "Reshad": {"description": "", "photo": None, "children": {}},
#             "Selima": {"description": "", "photo": None, "children": {}},
#             "Fetiya": {"description": "", "photo": None, "children": {}},
#             "Sherefa": {"description": "", "photo": None, "children": {}},
#             "Ali": {"description": "", "photo": None, "children": {}},
#             "Neja": {"description": "", "photo": None, "children": {}}
#         }},
#         "Dilbo": {"description": "Mother Dilbo", "photo": None, "children": {
#             "Sadik": {"description": "", "photo": None, "children": {}},
#             "Behra": {"description": "", "photo": None, "children": {}},
#             "Nasir": {"description": "", "photo": None, "children": {}},
#             "Abdusemed": {"description": "", "photo": None, "children": {}}
#         }},
#         "Rukiya": {"description": "Mother Rukiya", "photo": None, "children": {
#             "Beytulah": {"description": "", "photo": None, "children": {}},
#             "Leyla": {"description": "", "photo": None, "children": {}},
#             "Zulfa": {"description": "", "photo": None, "children": {}},
#             "Ishaq": {"description": "", "photo": None, "children": {}},
#             "Mubarek": {"description": "", "photo": None, "children": {}},
#             "Hayat": {"description": "", "photo": None, "children": {}}
#         }},
#         "Nefissa": {"description": "Mother Nefissa", "photo": None, "children": {
#             "Abdurezak": {"description": "", "photo": None, "children": {}}
#         }}
#     }
#
# # --- HELPER FUNCTION TO SAVE DATA ---
# def save_data():
#     with open(DATA_FILE, "w", encoding="utf-8") as f:
#         json.dump(family_data, f, ensure_ascii=False, indent=4)
#
# # --- DISPLAY FAMILY FUNCTION ---
# def display_family(name, data, father="Mohammed", parent_key=None):
#     """
#     Recursive function to display a member, their children, and dynamic add-child functionality
#     """
#     if parent_key is None:
#         parent_key = name  # top-level key
#
#     with st.expander(name, expanded=False):
#         st.write(data.get("description", ""))
#         st.write(f"👨 Father: {father}")
#
#         # Show photo if exists
#         if data.get("photo"):
#             st.image(data["photo"], width=150)
#
#         # Show existing children
#         if data.get("children"):
#             st.subheader(f"Children of {name}:")
#             for child_name, child_data in data["children"].items():
#                 display_family(child_name, child_data, father="Mohammed", parent_key=f"{parent_key}_{child_name}")
#
#         # --- Add Child Button ---
#         if f"show_form_{parent_key}" not in st.session_state:
#             st.session_state[f"show_form_{parent_key}"] = False
#
#         if not st.session_state[f"show_form_{parent_key}"]:
#             if st.button(f"Add Child to {name}", key=f"button_{parent_key}"):
#                 st.session_state[f"show_form_{parent_key}"] = True
#
#         # --- Add Child Form ---
#         if st.session_state[f"show_form_{parent_key}"]:
#             with st.form(f"form_{parent_key}"):
#                 new_name = st.text_input("Child's Name")
#                 new_description = st.text_area("Child's Description")
#                 new_photo = st.file_uploader("Upload Photo", type=["png","jpg","jpeg"])
#                 submitted = st.form_submit_button("Submit Child")
#                 if submitted:
#                     if not new_name:
#                         st.warning("Please enter the child's name.")
#                     elif new_name in data["children"]:
#                         st.warning(f"{new_name} already exists under {name}.")
#                     else:
#                         # Save child data
#                         if new_photo is not None:
#                             # Convert file to bytes for JSON storage
#                             new_photo_bytes = new_photo.read()
#                             data["children"][new_name] = {
#                                 "description": new_description,
#                                 "photo": new_photo_bytes.hex(),  # store as hex string
#                                 "children": {}
#                             }
#                         else:
#                             data["children"][new_name] = {
#                                 "description": new_description,
#                                 "photo": None,
#                                 "children": {}
#                             }
#                         save_data()  # save to JSON
#                         st.success(f"Child {new_name} added under {name} ✅")
#                         st.session_state[f"show_form_{parent_key}"] = False  # hide form
#
# # --- DISPLAY ALL MOTHERS ---
# st.header("Mothers of the Family")
# for mother_name, mother_data in family_data.items():
#     display_family(mother_name, mother_data)
#
#
# import io
# from PIL import Image
#
# photo_bytes = bytes.fromhex(child["photo"])
# image = Image.open(io.BytesIO(photo_bytes))
# st.image(image)
#
#
# import streamlit as st
# import json
# import os
# from PIL import Image
# import io
#
# st.set_page_config(page_title="Delko Family Tree", layout="wide")
# st.title("Delko Family Tree")
#
# DATA_FILE = "family_data.json"
#
# # --- Load or Initialize Data ---
# if os.path.exists(DATA_FILE):
#     with open(DATA_FILE, "r", encoding="utf-8") as f:
#         family_data = json.load(f)
# else:
#     family_data = {
#         "Shemega": {"description": "Mother Shemega", "photo": None, "children": {}},
#         "Nurseba": {"description": "Mother Nurseba", "photo": None, "children": {}},
#         "Dilbo": {"description": "Mother Dilbo", "photo": None, "children": {}},
#         "Rukiya": {"description": "Mother Rukiya", "photo": None, "children": {}},
#         "Nefissa": {"description": "Mother Nefissa", "photo": None, "children": {}}
#     }
#
# # --- Save to JSON ---
# def save_data():
#     with open(DATA_FILE, "w", encoding="utf-8") as f:
#         json.dump(family_data, f, ensure_ascii=False, indent=4)
#
# # --- Display Family Node ---
# def display_member(name, data, parent_key=None):
#     if parent_key is None:
#         parent_key = name
#
#     with st.expander(name, expanded=False):
#         st.write(data.get("description", ""))
#         st.write("👨 Father: Mohammed")
#
#         # Show photo if exists
#         if data.get("photo"):
#             try:
#                 img_bytes = bytes.fromhex(data["photo"])
#                 image = Image.open(io.BytesIO(img_bytes))
#                 st.image(image, width=150)
#             except:
#                 pass
#
#         # Display children recursively
#         if data.get("children"):
#             st.subheader(f"Children of {name}:")
#             for child_name, child_data in data["children"].items():
#                 display_member(child_name, child_data, parent_key=f"{parent_key}_{child_name}")
#
#         # Add Child button logic
#         if f"show_form_{parent_key}" not in st.session_state:
#             st.session_state[f"show_form_{parent_key}"] = False
#
#         if not st.session_state[f"show_form_{parent_key}"]:
#             if st.button(f"Add Child to {name}", key=f"button_{parent_key}"):
#                 st.session_state[f"show_form_{parent_key}"] = True
#
#         # Add Child Form
#         if st.session_state[f"show_form_{parent_key}"]:
#             with st.form(f"form_{parent_key}"):
#                 new_name = st.text_input("Child Name")
#                 new_description = st.text_area("Description")
#                 new_photo = st.file_uploader("Upload Photo", type=["png","jpg","jpeg"])
#                 submitted = st.form_submit_button("Submit Child")
#                 if submitted:
#                     if not new_name:
#                         st.warning("Please enter a name.")
#                     elif new_name in data["children"]:
#                         st.warning(f"{new_name} already exists under {name}.")
#                     else:
#                         # Save photo as hex
#                         photo_hex = new_photo.read().hex() if new_photo else None
#                         # Add new child as a new generation
#                         data["children"][new_name] = {
#                             "description": new_description,
#                             "photo": photo_hex,
#                             "children": {}  # can have children later
#                         }
#                         save_data()
#                         st.success(f"Child {new_name} added under {name} ✅")
#                         st.session_state[f"show_form_{parent_key}"] = False
#
# # --- Display All Mothers ---
# st.header("Mothers of the Family")
# for mother_name, mother_data in family_data.items():
#     display_member(mother_name, mother_data)
#
# import streamlit as st
# import json
# import os
# from PIL import Image
# import io
#
# st.set_page_config(page_title="Delko Family Tree", layout="wide")
# st.title("Delko Family Tree")
#
# DATA_FILE = "family_data.json"
#
# # --- Load or Initialize Data ---
# if os.path.exists(DATA_FILE):
#     with open(DATA_FILE, "r", encoding="utf-8") as f:
#         family_data = json.load(f)
# else:
#     family_data = {
#         "Shemega": {"description": "Mother Shemega", "photo": None, "children": {}},
#         "Nurseba": {"description": "Mother Nurseba", "photo": None, "children": {}},
#         "Dilbo": {"description": "Mother Dilbo", "photo": None, "children": {}},
#         "Rukiya": {"description": "Mother Rukiya", "photo": None, "children": {}},
#         "Nefissa": {"description": "Mother Nefissa", "photo": None, "children": {}}
#     }
#
# # --- Save Data ---
# def save_data():
#     with open(DATA_FILE, "w", encoding="utf-8") as f:
#         json.dump(family_data, f, ensure_ascii=False, indent=4)
#
# # --- Display Member Function ---
# def display_member(name, data, is_mother=False, parent_key=None):
#     if parent_key is None:
#         parent_key = name
#
#     with st.expander(name, expanded=False):
#         st.write(data.get("description", ""))
#         st.write("👨 Father: Mohammed")
#
#         # Show photo if exists
#         if data.get("photo"):
#             try:
#                 img_bytes = bytes.fromhex(data["photo"])
#                 image = Image.open(io.BytesIO(img_bytes))
#                 st.image(image, width=150)
#             except:
#                 pass
#
#         # Display children recursively
#         if data.get("children"):
#             st.subheader(f"Children of {name}:")
#             for child_name, child_data in data["children"].items():
#                 display_member(child_name, child_data, is_mother=False, parent_key=f"{parent_key}_{child_name}")
#
#         # Add Child button and form (skip for mothers)
#         if not is_mother:
#             if f"show_form_{parent_key}" not in st.session_state:
#                 st.session_state[f"show_form_{parent_key}"] = False
#
#             if not st.session_state[f"show_form_{parent_key}"]:
#                 if st.button(f"Add Child to {name}", key=f"button_{parent_key}"):
#                     st.session_state[f"show_form_{parent_key}"] = True
#
#             if st.session_state[f"show_form_{parent_key}"]:
#                 with st.form(f"form_{parent_key}"):
#                     new_name = st.text_input("Child Name")
#                     new_description = st.text_area("Description")
#                     new_photo = st.file_uploader("Upload Photo", type=["png","jpg","jpeg"])
#                     submitted = st.form_submit_button("Submit Child")
#                     if submitted:
#                         if not new_name:
#                             st.warning("Please enter a name.")
#                         elif new_name in data["children"]:
#                             st.warning(f"{new_name} already exists under {name}.")
#                         else:
#                             # Save photo as hex
#                             photo_hex = new_photo.read().hex() if new_photo else None
#                             # Add new child as new generation
#                             data["children"][new_name] = {
#                                 "description": new_description,
#                                 "photo": photo_hex,
#                                 "children": {}
#                             }
#                             save_data()
#                             st.success(f"Child {new_name} added under {name} ✅")
#                             st.session_state[f"show_form_{parent_key}"] = False
#
# # --- Display All Mothers ---
# st.header("Mothers of the Family")
# for mother_name, mother_data in family_data.items():
#     display_member(mother_name, mother_data, is_mother=True)
# ---------------- FAMILY DISPLAY ----------------
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
    {"question": "first child of Nurseba?", "answer": "Oumer"},
    {"question": "Who is the youngest mother?", "answer": "Nefissa"},
    {"question": "Who mother of sadik?", "answer": "Dilbo"},
    {"question": "Who is the first wife of Mohammed?", "answer": "Shemega"},
]

# ---------------- INITIAL FAMILY DATA ----------------
default_family_data = {
    "Shemega": {
        "description": "Mother Shemega",
        "phone": "0911000000",
        "partner": "Mohammed",
        "locked_partner": True,
        "children": {
            "Sunkemo": {"description": "Child of Shemega + Mohammed", "children": {}, "phone": "0911222333"},
            "Jemal": {"description": "Child of Shemega + Mohammed", "children": {}, "phone": "0911222334"},
            "Rehmet": {"description": "Child of Shemega + Mohammed", "children": {}, "phone": "0911222335"},
            "Bedriya": {"description": "Child of Shemega + Mohammed", "children": {}, "phone": "0911222336"},
        },
    },
    "Nurseba": {
        "description": "Mother Nurseba",
        "phone": "0911333444",
        "partner": "Mohammed",
        "locked_partner": True,
        "children": {
            "Oumer": {"description": "Child of Nurseba + Mohammed", "children": {}, "phone": "0911222337"},
            "Sefiya": {"description": "Child of Nurseba + Mohammed", "children": {}, "phone": "0911222338"},
            "Ayro": {"description": "Child of Nurseba + Mohammed", "children": {}, "phone": "0911222339"},
            "Reshad": {"description": "Child of Nurseba + Mohammed", "children": {}, "phone": "0911222340"},
        },
    },
    "Dilbo": {
        "description": "Mother Dilbo",
        "phone": "0911444555",
        "partner": "Mohammed",
        "locked_partner": True,
        "children": {
            "Sadik": {"description": "Child of Dilbo + Mohammed", "children": {}, "phone": "0911222341"},
            "Behra": {"description": "Child of Dilbo + Mohammed", "children": {}, "phone": "0911222342"},
        },
    },
    "Rukiya": {
        "description": "Mother Rukiya",
        "phone": "0911555666",
        "partner": "Mohammed",
        "locked_partner": True,
        "children": {
            "Beytulah": {"description": "Child of Rukiya + Mohammed", "children": {}, "phone": "0911222343"},
            "Leyla": {"description": "Child of Rukiya + Mohammed", "children": {}, "phone": "0911222344"},
        },
    },
    "Nefissa": {
        "description": "Mother Nefissa",
        "phone": "0911666777",
        "partner": "Mohammed",
        "locked_partner": True,
        "children": {
            "Abdurezak": {"description": "Child of Nefissa + Mohammed", "children": {}, "phone": "0911222345"},
        },
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

    # Show in an expander
    if name in ["Shemega", "Nurseba", "Dilbo", "Rukiya", "Nefissa"]:
        partner_display = "Wife of Mohammed"
    else:
        partner_display = partner if partner else "Single"

    with st.expander(f"{name} ({partner_display})", expanded=False):
        st.write(data.get("description", ""))

        # Phone button
        if "phone" in data and data["phone"]:
            st.markdown(f"<a href='tel:{data['phone']}' class='phone-button'>📞 Call {name}</a>", unsafe_allow_html=True)

        # CHILDREN display
        if data.get("children"):
            header = f"Children of {name}" if not partner else f"Children of {name} + {partner}"
            st.subheader(header)
            for child_name, child_data in data["children"].items():
                display_family(child_name, child_data, parent_key=f"{parent_key}_{child_name}")

        # ADD PARTNER (only if no partner & not locked & not one of the specified mothers)
        if not partner and not locked_partner and name not in ["Shemega", "Nurseba", "Dilbo", "Rukiya", "Nefissa"]:
            if st.button(f"Add Partner for {name}", key=f"partner_{parent_key}_{name}"):
                st.session_state[f"adding_partner_{parent_key}_{name}"] = True

            if st.session_state.get(f"adding_partner_{parent_key}_{name}", False):
                with st.form(f"partner_form_{parent_key}_{name}"):
                    partner_name = st.text_input("Enter partner's name")
                    submit_partner = st.form_submit_button("Save Partner")

                    if submit_partner and partner_name:
                        data["partner"] = partner_name
                        save_data(family_data)
                        st.success(f"Partner {partner_name} added for {name} ✅")
                        st.session_state[f"adding_partner_{parent_key}_{name}"] = False
                        st.rerun()

        # REMOVE ADD CHILD BUTTON for specified mothers
        if name not in ["Shemega", "Nurseba", "Dilbo", "Rukiya", "Nefissa"] and partner:
            if st.button(f"Add Child to {name}", key=f"child_{parent_key}_{name}"):
                st.session_state[f"adding_child_{parent_key}_{name}"] = True

            if st.session_state.get(f"adding_child_{parent_key}_{name}", False):
                with st.form(f"child_form_{parent_key}_{name}"):
                    new_child_name = st.text_input("Enter child name")
                    new_child_desc = st.text_area("Enter child description")
                    new_child_phone = st.text_input("Enter phone number")
                    submit_child = st.form_submit_button("Save Child")

                    if submit_child and new_child_name:
                        data["children"][new_child_name] = {
                            "description": new_child_desc,
                            "children": {},
                            "phone": new_child_phone,
                        }
                        save_data(family_data)
                        st.success(f"Child {new_child_name} added under {name} ✅")
                        st.session_state[f"adding_child_{parent_key}_{name}"] = False
                        st.rerun()

        # EDIT
        if st.button(f"✏️ Edit {name}", key=f"edit_{parent_key}_{name}"):
            st.session_state[f"editing_{parent_key}_{name}"] = True

        if st.session_state.get(f"editing_{parent_key}_{name}", False):
            with st.form(f"edit_form_{parent_key}_{name}"):
                new_desc = st.text_area("Update description", value=data.get("description", ""))
                new_phone = st.text_input("Update phone number", value=data.get("phone", ""))
                partner_input = st.text_input("Update partner's name", value=partner)
                submit_edit = st.form_submit_button("Save Changes")

                if submit_edit:
                    data["description"] = new_desc
                    data["phone"] = new_phone
                    data["partner"] = partner_input  # Update partner's name
                    save_data(family_data)
                    st.success(f"{name} updated ✅")
                    st.session_state[f"editing_{parent_key}_{name}"] = False
                    st.rerun()

        # DELETE
        if st.button(f"🗑️ Delete {name}", key=f"delete_{parent_key}_{name}"):
            st.session_state[f"delete_{parent_key}_{name}"] = True

        if st.session_state.get(f"delete_{parent_key}_{name}", False):
            st.warning(f"Are you sure you want to delete {name}?")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Yes, Delete", key=f"confirm_delete_{parent_key}_{name}"):
                    st.session_state["delete_target"] = (parent_key, name)
                    st.session_state[f"delete_{parent_key}_{name}"] = False
                    st.rerun()
            with col2:
                if st.button("Cancel", key=f"cancel_delete_{parent_key}_{name}"):
                    st.session_state[f"delete_{parent_key}_{name}"] = False
                    st.rerun()

# ---------------- DELETE HANDLER ----------------
def handle_delete():
    if "delete_target" in st.session_state:
        parent_key, name = st.session_state["delete_target"]

        def recursive_delete(data_dict, target):
            if target in data_dict:
                del data_dict[target]
                return True
            for _, v in data_dict.items():
                if recursive_delete(v.get("children", {}), target):
                    return True
            return False

        recursive_delete(family_data, name)
        save_data(family_data)
        st.success(f"{name} deleted ✅")
        del st.session_state["delete_target"]
        st.rerun()

# ---------------- APP ----------------
st.set_page_config(page_title="Delko's Family Data Record", layout="centered")

st.title("👨‍👩‍👧 Delko's Family Data Record")

# Quiz logic
if "quiz_done" not in st.session_state:
    st.session_state.quiz_done = False
    st.session_state.current_question = random.choice(quiz_questions)

if not st.session_state.quiz_done:
    st.header("📖 Family Quiz")
    question = st.session_state.current_question["question"]

    ans = st.text_input(question)
    if st.button("Submit Quiz"):
        if ans.strip().lower() == st.session_state.current_question["answer"].lower():
            st.success("✅ Correct!")
            st.session_state.quiz_done = True  # Mark quiz as done
        else:
            st.error("❌ Wrong! Try again.")
            # Pick a new question if the answer is wrong
            st.session_state.current_question = random.choice(quiz_questions)

else:
    st.header("Family Tree by Mothers")
    handle_delete()
    for mother_name, mother_data in family_data.items():
        display_family(mother_name, mother_data)