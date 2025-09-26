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
        :root { --brand:#0b6cff; --bg:#f5f7fb; --card:#fff; --muted:#667085; --border:#e4e7ec; }
        html,body { background:var(--bg); }
        .main { background:var(--card); border-radius:16px; padding:18px; margin:12px auto; max-width:860px; box-shadow:0 8px 24px rgba(0,0,0,0.06); }
        .cool-header { background:linear-gradient(90deg,#0b6cff,#5b9bff); color:#fff; padding:10px 14px; border-radius:12px; font-weight:700; text-align:center; margin-bottom:12px; position:sticky; top:8px; z-index:10; }
        .muted{ color:var(--muted); font-size:14px; }
        .button-row{ display:flex; gap:8px; flex-wrap:wrap; margin-top:8px; }
        .stButton>button{ border-radius:10px !important; padding:10px 12px; }
        @media(max-width:600px){ .stButton>button{ width:100% !important; } .main{ padding:14px; margin:8px;} .cool-header{ font-size:1rem;} }
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

# ---------------- DEFAULT DATA (Mustefa included; children unfixed) ----------------
default_family_data = {
    "Shemega": {
        "description": "Mother Shemega",
        "phone": "0911000000",
        "partner": "Mohammed",
        "locked_partner": True,
        "locked_root": True,
        "photo": "",
        "children": {
            "Sunkemo": {"description": "Child of Shemega + Mohammed", "children": {}, "phone": "0911222333", "photo": "", "fixed_generation": False},
            "Jemal":   {"description": "Child of Shemega + Mohammed", "children": {}, "phone": "0911222334", "photo": "", "fixed_generation": False},
            "Mustefa": {"description": "Child of Shemega + Mohammed", "children": {}, "phone": "0911222337", "photo": "", "fixed_generation": False},
            "Rehmet":  {"description": "Child of Shemega + Mohammed", "children": {}, "phone": "0911222335", "photo": "", "fixed_generation": False},
            "Bedriya": {"description": "Child of Shemega + Mohammed", "children": {}, "phone": "0911222336", "photo": "", "fixed_generation": False},
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
            "Oumer": {"description": "Child of Nurseba + Mohammed", "children": {}, "phone": "0911222337", "photo": "", "fixed_generation": False},
            "Sefiya": {"description": "Child of Nurseba + Mohammed", "children": {}, "phone": "0911222338", "photo": "", "fixed_generation": False},
            "Ayro": {"description": "Child of Nurseba + Mohammed", "children": {}, "phone": "0911222339", "photo": "", "fixed_generation": False},
            "Reshad": {"description": "Child of Nurseba + Mohammed", "children": {}, "phone": "0911222340", "photo": "", "fixed_generation": False},
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
            "Sadik": {"description": "Child of Dilbo + Mohammed", "children": {}, "phone": "0911222341", "photo": "", "fixed_generation": False},
            "Behra": {"description": "Child of Dilbo + Mohammed", "children": {}, "phone": "0911222342", "photo": "", "fixed_generation": False},
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
            "Beytulah": {"description": "Child of Rukiya + Mohammed", "children": {}, "phone": "0911222343", "photo": "", "fixed_generation": False},
            "Leyla": {"description": "Child of Rukiya + Mohammed", "children": {}, "phone": "0911222344", "photo": "", "fixed_generation": False},
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
            "Abdurezak": {"description": "Child of Nefissa + Mohammed", "children": {}, "phone": "0911222345", "photo": "", "fixed_generation": False},
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

# Helper: walk path and return the exact dict reference for the node and its parent children dict
def get_node_and_parent_children(path):
    if not path:
        return None, st.session_state.family_data
    root = st.session_state.family_data
    parent_children = root
    node = None
    for i, part in enumerate(path):
        if i == 0:
            node = root.get(part)
            parent_children = root
        else:
            parent_children = node.get("children", {})
            node = parent_children.get(part)
        if node is None:
            return None, st.session_state.family_data
    return node, parent_children

def get_parent_container(ancestors):
    if not ancestors:
        return st.session_state.family_data
    node, parent_children = get_node_and_parent_children(ancestors)
    if node is None:
        return st.session_state.family_data
    return parent_children

# ---------------- Display ----------------
def display_family(name, data, ancestors=None):
    if ancestors is None:
        ancestors = []
    path = ancestors + [name]
    key_base = "_".join(path).replace(" ", "_")

    node, _ = get_node_and_parent_children(path)
    if node is None:
        node = data

    partner_live = node.get("partner", "")
    locked = node.get("locked_partner", False)
    fixed = node.get("fixed_generation", False)
    locked_root = node.get("locked_root", False)
    partner_display = "Wife of Mohammed" if name in MOTHERS_WITH_DEFAULT_PARTNER else (partner_live or "Single")

    with st.expander(f"{name} ({partner_display})", expanded=False):
        col1, col2 = st.columns([1, 3])
        with col1:
            img = node.get("photo", "")
            show_img = img if (img and os.path.exists(img)) else PLACEHOLDER_IMAGE
            st.image(show_img, width=100)
        with col2:
            c1, c2 = st.columns([3, 2])
            with c1:
                st.markdown(f"### {name}")
                st.markdown(f"<div class='muted'>{node.get('description','')}</div>", unsafe_allow_html=True)
                if node.get("phone"):
                    st.markdown(f"📞 {node['phone']}", unsafe_allow_html=True)
            with c2:
                if not locked_root:
                    if st.button(f"Edit {name}", key=f"edit_{key_base}"):
                        st.session_state[f"edit_mode_{key_base}"] = True
                        st.session_state.pop(f"partner_mode_{key_base}", None)
                        st.session_state.pop(f"child_mode_{key_base}", None)
                    if st.button("❌ Delete", key=f"del_{key_base}"):
                        _, parent_children = get_node_and_parent_children(path)
                        if name in parent_children:
                            parent_children.pop(name, None)
                            save_and_rerun()

            # Single action spot: either Add Partner (no partner) OR Add Child (partner exists)
            st.markdown('<div class="button-row">', unsafe_allow_html=True)
            show_add_partner = (not locked_root) and (not locked) and (not partner_live)
            show_add_child = (not locked_root) and (partner_live) and (not fixed)

            if show_add_partner:
                if st.button("💍 Add partner", key=f"btn_partner_{key_base}"):
                    st.session_state[f"partner_mode_{key_base}"] = True
                    st.session_state.pop(f"child_mode_{key_base}", None)
                    st.session_state.pop(f"edit_mode_{key_base}", None)
            elif show_add_child:
                if st.button("➕ Add child", key=f"btn_child_{key_base}"):
                    st.session_state[f"child_mode_{key_base}"] = True
                    st.session_state.pop(f"partner_mode_{key_base}", None)
                    st.session_state.pop(f"edit_mode_{key_base}", None)
            st.markdown('</div>', unsafe_allow_html=True)

            # Partner form
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
                            live_node, _ = get_node_and_parent_children(path)
                            if live_node is not None:
                                live_node["partner"] = pname.strip()
                                live_node.setdefault("children", {})
                            else:
                                data["partner"] = pname.strip()
                                data.setdefault("children", {})
                            st.session_state.pop(f"partner_mode_{key_base}", None)
                            save_and_rerun()
                        else:
                            st.error("Enter partner name.")

            # Child form
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
                            live_node, _ = get_node_and_parent_children(path)
                            if live_node is None:
                                live_node = data
                            child = {"description": cdesc, "children": {}, "phone": cphone, "photo": ""}
                            if cphoto:
                                child["photo"] = save_uploaded_photo(cphoto, path + [cname])
                            live_node.setdefault("children", {})[cname] = child
                            st.session_state.pop(f"child_mode_{key_base}", None)
                            save_and_rerun()

    # Edit mode (only if not locked root)
    if st.session_state.get(f"edit_mode_{key_base}", False) and not node.get("locked_root", False):
        with st.form(f"form_edit_{key_base}"):
            nname = st.text_input("Name", value=name, key=f"en_{key_base}")
            desc = st.text_area("Description", value=data.get("description", ""), key=f"ed_{key_base}")
            phone = st.text_input("Phone", value=data.get("phone", ""), key=f"ep_{key_base}")
            if node.get("locked_partner", False):
                st.text_input("Partner", value=node.get("partner", ""), disabled=True, key=f"epl_{key_base}")
                pval = node.get("partner", "")
            else:
                pval = st.text_input("Partner", value=node.get("partner", ""), key=f"epv_{key_base}")
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
                parent_children = get_parent_container(ancestors)
                if nname.strip() and (nname == name or nname not in parent_children):
                    node["description"] = desc
                    node["phone"] = phone
                    node["partner"] = pval
                    if photo:
                        node["photo"] = save_uploaded_photo(photo, path)
                    if nname != name:
                        parent_children.pop(name, None)
                        parent_children[nname] = node
                    st.session_state.pop(f"edit_mode_{key_base}", None)
                    save_and_rerun()
                else:
                    st.error("Invalid or duplicate name")

    # Children recursion
    for ch, cd in list(node.get("children", {}).items()):
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
