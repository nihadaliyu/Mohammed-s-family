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
        .stButton>button { border-radius: 6px; padding: 4px 10px; font-size: 0.9rem; margin-right: 6px; }
        .edit-btn { background: #007bff !important; color: white !important; }
        .delete-btn { background: #d9534f !important; color: white !important; }
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
        "children": {},
    }
    # ... (keep the rest of your default data as before)
}

# ---------------- LOAD / SAVE ----------------
def load_family_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return copy.deepcopy(default_family_data)
    return copy.deepcopy(default_family_data)

def save_family_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

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
            st.image(photo_path if (photo_path and os.path.exists(photo_path)) else PLACEHOLDER_IMAGE, width=120)
        with col2:
            st.markdown(f"### {name}")
            st.markdown(f"<div class='muted'>{partner_display}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='muted'>{data.get('description', '')}</div>", unsafe_allow_html=True)
            if data.get("phone"):
                st.markdown(
                    f"<b>{data['phone']}</b> <a class='phone-link' href='tel:{data['phone']}'>📞 Call</a>",
                    unsafe_allow_html=True,
                )

            # -------- Action Buttons (Edit + Delete) --------
            c1, c2 = st.columns([1, 1])
            with c1:
                if st.button("📝 Edit Member Name & Info", key=f"edit_{key_base}"):
                    st.session_state[f"editing_{key_base}"] = True
            with c2:
                if st.button("🗑️ Delete", key=f"delete_{key_base}"):
                    st.session_state[f"confirm_delete_{key_base}"] = True

        # -------- Edit Form --------
        if st.session_state.get(f"editing_{key_base}", False):
            with st.form(key=f"edit_form_{key_base}"):
                new_name = st.text_input("Member Name", value=name)
                new_desc = st.text_area("Description", value=data.get("description", ""))
                new_phone = st.text_input("Phone", value=data.get("phone", ""))
                new_partner = st.text_input("Partner", value=partner if not locked_partner else "Mohammed", disabled=locked_partner)
                new_photo = st.file_uploader("Upload new photo", type=["jpg", "jpeg", "png"])

                if st.form_submit_button("Save"):
                    # update
                    if new_name != name:
                        parent = st.session_state.family_data
                        for anc in ancestors[:-1]:
                            parent = parent[anc]["children"]
                        parent.pop(name)
                        parent[new_name] = data
                        name = new_name
                    data["description"] = new_desc
                    data["phone"] = new_phone
                    if not locked_partner:
                        data["partner"] = new_partner
                    if new_photo:
                        data["photo"] = save_uploaded_photo(new_photo, path)
                    save_family_data(st.session_state.family_data)
                    st.success("Updated ✅")
                    st.session_state[f"editing_{key_base}"] = False
                    st.experimental_rerun()

        # -------- Delete Confirm --------
        if st.session_state.get(f"confirm_delete_{key_base}", False):
            st.warning(f"Delete {name}? This cannot be undone.")
            if st.button(f"Yes, delete {name}", key=f"yesdel_{key_base}"):
                parent = st.session_state.family_data
                for anc in ancestors[:-1]:
                    parent = parent[anc]["children"]
                parent.pop(name, None)
                save_family_data(st.session_state.family_data)
                st.success(f"{name} deleted ✅")
                st.session_state[f"confirm_delete_{key_base}"] = False
                st.experimental_rerun()

        # -------- Add Child (if allowed) --------
        if data.get("partner") and not data.get("locked_partner", False) and name not in MOTHERS_WITH_DEFAULT_PARTNER:
            with st.expander(f"➕ Add Child to {name}"):
                with st.form(key=f"child_form_{key_base}"):
                    cname = st.text_input("Child Name")
                    cdesc = st.text_area("Child Description")
                    cphone = st.text_input("Child Phone")
                    cphoto = st.file_uploader("Upload photo", type=["jpg", "jpeg", "png"])
                    if st.form_submit_button("Save Child"):
                        if cname.strip():
                            data.setdefault("children", {})[cname] = {
                                "description": cdesc,
                                "phone": cphone,
                                "photo": save_uploaded_photo(cphoto, [name, cname]) if cphoto else "",
                                "children": {},
                            }
                            save_family_data(st.session_state.family_data)
                            st.success(f"Child {cname} added ✅")
                            st.experimental_rerun()

        # -------- Recurse children --------
        for child_name, child_data in data.get("children", {}).items():
            display_family(child_name, child_data, ancestors + [name])


# ---------------- MAIN ----------------
if "family_data" not in st.session_state:
    st.session_state.family_data = load_family_data()

st.markdown('<div class="main">', unsafe_allow_html=True)
st.markdown('<div class="cool-header">👨‍👩‍👧 Delko\'s Family Data Record</div>', unsafe_allow_html=True)

for mother_name, mother_data in st.session_state.family_data.items():
    display_family(mother_name, mother_data)

if st.button("💾 Save All"):
    save_family_data(st.session_state.family_data)
    st.success("Saved ✅")

st.markdown('</div>', unsafe_allow_html=True)
