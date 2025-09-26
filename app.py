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

# ---------------- CSS (mobile-friendly) ----------------
st.markdown(
    """
    <style>
        :root {
            --brand:#0b6cff;
            --bg:#f5f7fb;
            --card:#ffffff;
            --text:#222;
            --muted:#667085;
            --border:#e4e7ec;
        }
        html, body { background: var(--bg); }
        .main {
            background: var(--card);
            border-radius: 20px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.08);
            padding: 20px 16px;
            margin: 14px auto;
            max-width: 860px;
        }
        .cool-header {
            position: sticky;
            top: 0;
            z-index: 10;
            background: linear-gradient(90deg, #0b6cff, #5b9bff);
            color: #fff;
            border-radius: 14px;
            padding: 12px 16px;
            font-size: 1.25rem;
            font-weight: 700;
            text-align: center;
            margin-bottom: 16px;
        }
        .section-title {
            font-size: 1rem;
            font-weight: 600;
            margin: 8px 0 12px;
            color: var(--text);
        }
        .muted { color: var(--muted); font-size: 14px; margin: 4px 0; }
        .button-row { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 8px; }
        .stButton>button {
            border-radius: 10px !important;
            padding: 10px 14px;
            font-size: 0.95rem;
            border: 1px solid var(--border);
        }
        .stButton>button:hover { border-color: var(--brand); }
        .stButton>button:focus { outline: none !important; }
        .stTextInput>div>div>input, .stTextArea textarea {
            border-radius: 12px;
        }
        .stFileUploader label { font-size: 0.95rem; }
        .stExpander {
            border: 1px solid var(--border);
            border-radius: 16px !important;
            overflow: hidden;
            margin-bottom: 12px;
        }
        .stExpander > div > div { padding: 8px 12px; }
        @media (max-width: 600px) {
            .main { padding: 16px 12px; margin: 8px; }
            .cool-header { font-size: 1.05rem; padding: 10px; }
            .button-row { gap: 6px; }
            .stButton>button { width: 100% !important; padding: 12px; font-size: 1rem; }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------- QUIZ ----------------
quiz_questions = [
    {"question": "How many children did Sunkemo have?", "answer": "9"},
    {"question": "How many wives did Mohammed have?", "answer": "5"},
    {"question": "How many children did mother Shemega have?", "answer": "5"},
    {"question": "How many children did mother Nurseba have?", "answer": "4"},
    {"question": "How many children did mother Dilbo have?", "answer": "2"},
]

# ---------------- DEFAULT DATA ----------------
default_family_data = {
    "Shemega": {
        "description": "Mother Shemega",
        "phone": "0911000000",
        "partner": "Mohammed",
        "locked_partner": True,
        "locked_root": True,   # fully locked root
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
        "locked_root": True,
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
        "locked_root": True,
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
        "locked_root": True,
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
        "locked_root": True,
        "photo": "",
        "children": {
            "Abdurezak": {"description": "Child of Nefissa + Mohammed", "children": {}, "phone": "0911222345", "photo": "", "fixed_generation": True},
        },
    },
}

# ---------------- Load/Save ----------------
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

def save_and_rerun():
    save_family_data(st.session_state.family_data)
    st.rerun()

def save_uploaded_photo(uploaded_file, path_list):
    if not uploaded_file:
        return ""
    safe_base = "_".join(path_list).replace(" ", "_")
    _, ext = os.path.splitext(uploaded_file.name)
    fname = f"{safe_base}_{uuid.uuid4().hex[:6]}{ext or '.jpg'}"
    filepath = os.path.join(PHOTO_DIR, fname)
    with open(filepath, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return filepath

# ---------------- Init ----------------
if "family_data" not in st.session_state:
    st.session_state.family_data = load_family_data()
if "quiz_done" not in st.session_state:
    st.session_state.quiz_done = False
if "current_question" not in st.session_state:
    st.session_state.current_question = random.choice(quiz_questions)

def get_parent_container(ancestors):
    if not ancestors:
        return st.session_state.family_data
    node = st.session_state.family_data.get(ancestors[0])
    if node is None:
        return st.session_state.family_data
    for anc in ancestors[1:]:
        node = node.get("children", {}).get(anc)
        if node is None:
            return st.session_state.family_data
    return node.setdefault("children", {})

# ---------------- Display ----------------
def display_family(name, data, ancestors=None):
    if ancestors is None:
        ancestors = []
    path = ancestors + [name]
    key_base = "_".join(path).replace(" ", "_")

    partner = data.get("partner", "")
    locked = data.get("locked_partner", False)
    fixed = data.get("fixed_generation", False)
    locked_root = data.get("locked_root", False)
    partner_display = "Wife of Mohammed" if name in MOTHERS_WITH_DEFAULT_PARTNER else (partner or "Single")

    with st.expander(f"{name} ({partner_display})", expanded=False):
        card = st.container()
        with card:
            col1, col2 = st.columns([1, 3])
            with col1:
                img = data.get("photo", "")
                show_img = img if (img and os.path.exists(img)) else PLACEHOLDER_IMAGE
                st.image(show_img, width=100)
            with col2:
                c1, c2 = st.columns([3, 2])
                with c1:
                    st.markdown(f"### {name}")
                    st.markdown(f"<div class='muted'>{data.get('description','')}</div>", unsafe_allow_html=True)
                    if data.get("phone"):
                        st.markdown(f"📞 {data['phone']}", unsafe_allow_html=True)
                with c2:
                    # Only allow edit/delete if not a locked root
                    if not locked_root:
                        if st.button(f"Edit {name}", key=f"edit_{key_base}"):
                            st.session_state[f"edit_mode_{key_base}"] = True
                            st.session_state.pop(f"partner_mode_{key_base}", None)
                            st.session_state.pop(f"child_mode_{key_base}", None)
                        if st.button("❌ Delete", key=f"del_{key_base}"):
                            parent = get_parent_container(ancestors)
                            if name in parent:
                                parent.pop(name, None)
                                save_and_rerun()

                st.markdown('<div class="button-row">', unsafe_allow_html=True)
                # Add Partner (only if not locked root, no partner yet, and not locked)
                if (not partner) and (not locked_root) and (not locked):
                    if st.button("💍 Add Partner", key=f"btn_partner_{key_base}"):
                        st.session_state[f"partner_mode_{key_base}"] = True
                        st.session_state.pop(f"child_mode_{key_base}", None)
                        st.session_state.pop(f"edit_mode_{key_base}", None)

                # Add Child (only if not locked root, partner exists (or is default wife), and not fixed_generation)
                if ((partner or name in MOTHERS_WITH_DEFAULT_PARTNER) and (not fixed) and (not locked_root)):
                    if st.button("➕ Add Child", key=f"btn_child_{key_base}"):
                        st.session_state[f"child_mode_{key_base}"] = True
                        st.session_state.pop(f"partner_mode_{key_base}", None)
                        st.session_state.pop(f"edit_mode_{key_base}", None)
                st.markdown('</div>', unsafe_allow_html=True)

                # Inline forms
                if st.session_state.get(f"partner_mode_{key_base}", False):
                    with st.form(f"form_partner_{key_base}"):
                        pname = st.text_input("Partner name", key=f"pn_{key_base}")
                        colp1, colp2 = st.columns(2)
                        with colp1:
                            save_partner = st.form_submit_button("Save partner")
                        with colp2:
                            cancel_partner = st.form_submit_button("Cancel")
                        if cancel_partner:
                            st.session_state.pop(f"partner_mode_{key_base}", None)
                            st.rerun()
                        if save_partner:
                            if pname.strip():
                                data["partner"] = pname.strip()
                                data.setdefault("children", {})
                                # Close partner form, do NOT auto-open child form
                                st.session_state.pop(f"partner_mode_{key_base}", None)
                                save_and_rerun()
                            else:
                                st.error("Enter partner name.")

                if st.session_state.get(f"child_mode_{key_base}", False):
                    with st.form(f"form_child_{key_base}"):
                        cname = st.text_input("Child name", key=f"cn_{key_base}")
                        cdesc = st.text_area("Description", key=f"cd_{key_base}")
                        cphone = st.text_input("Phone", key=f"cp_{key_base}")
                        cphoto = st.file_uploader("Photo", type=["jpg", "jpeg", "png"], key=f"cph_{key_base}")
                        colc1, colc2 = st.columns(2)
                        with colc1:
                            save_child = st.form_submit_button("Save child")
                        with colc2:
                            cancel_child = st.form_submit_button("Cancel")
                        if cancel_child:
                            st.session_state.pop(f"child_mode_{key_base}", None)
                            st.rerun()
                        if save_child:
                            if not cname.strip():
                                st.error("Name required")
                            else:
                                child = {"description": cdesc, "children": {}, "phone": cphone, "photo": ""}
                                if cphoto:
                                    child["photo"] = save_uploaded_photo(cphoto, path + [cname])
                                data.setdefault("children", {})[cname] = child
                                st.session_state.pop(f"child_mode_{key_base}", None)
                                save_and_rerun()

        # Edit mode (only if not locked root)
        if st.session_state.get(f"edit_mode_{key_base}", False) and not locked_root:
            with st.form(f"form_edit_{key_base}"):
                nname = st.text_input("Name", value=name, key=f"en_{key_base}")
                desc = st.text_area("Description", value=data.get("description", ""), key=f"ed_{key_base}")
                phone = st.text_input("Phone", value=data.get("phone", ""), key=f"ep_{key_base}")
                if locked:
                    st.text_input("Partner", value=partner, disabled=True, key=f"epl_{key_base}")
                    pval = partner
                else:
                    pval = st.text_input("Partner", value=partner, key=f"epv_{key_base}")
                photo = st.file_uploader("New photo", type=["jpg", "jpeg", "png"], key=f"eph_{key_base}")
                cole1, cole2 = st.columns(2)
                with cole1:
                    save_edit = st.form_submit_button("Save")
                with cole2:
                    cancel_edit = st.form_submit_button("Cancel")
                if cancel_edit:
                    st.session_state.pop(f"edit_mode_{key_base}", None)
                    st.rerun()
                if save_edit:
                    parent = get_parent_container(ancestors)
                    if nname.strip() and (nname == name or nname not in parent):
                        data["description"] = desc
                        data["phone"] = phone
                        data["partner"] = pval
                        if photo:
                            data["photo"] = save_uploaded_photo(photo, path)
                        if nname != name:
                            parent.pop(name, None)
                            parent[nname] = data
                        st.session_state.pop(f"edit_mode_{key_base}", None)
                        save_and_rerun()
                    else:
                        st.error("Invalid or duplicate name")

        # Children
        for ch, cd in list(data.get("children", {}).items()):
            display_family(ch, cd, ancestors=path)

# ---------------- MAIN ----------------
st.markdown('<div class="main">', unsafe_allow_html=True)
st.markdown('<div class="cool-header">👨‍👩‍👧 Delko\'s Family Data Record</div>', unsafe_allow_html=True)

if st.button("🔄 Reset All Data", key="reset_all"):
    save_family_data(copy.deepcopy(default_family_data))
    st.session_state.clear()
    st.rerun()

if not st.session_state.quiz_done:
    q = st.session_state.current_question
    st.markdown('<div class="section-title">🔐 Family Quiz</div>', unsafe_allow_html=True)
    ans = st.text_input(q["question"], key="quiz_answer")
    if st.button("Submit", key="quiz_submit"):
        if ans.strip().lower() == q["answer"].lower():
            st.session_state.quiz_done = True
            st.rerun()
        else:
            st.error("Wrong! Try again.")
else:
    st.markdown('<div class="section-title">🌳 Family Tree</div>', unsafe_allow_html=True)
    for mother, md in st.session_state.family_data.items():
        display_family(mother, md)
    if st.button("💾 Save Changes", key="save_changes"):
        save_family_data(st.session_state.family_data)
        st.success("Changes saved.")

st.markdown('</div>', unsafe_allow_html=True)
