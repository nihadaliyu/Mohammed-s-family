import streamlit as st
import json
import os
import copy
import uuid
import random

st.set_page_config(page_title="Delko's Family Tree", layout="centered")

DATA_FILE = "family_data.json"
PHOTO_DIR = "photos"
os.makedirs(PHOTO_DIR, exist_ok=True)

PLACEHOLDER_IMAGE = "https://via.placeholder.com/150?text=No+Photo"
MOTHERS_WITH_DEFAULT_PARTNER = ["Shemega", "Nurseba", "Dilbo", "Rukiya", "Nefissa"]

# ---------------- CSS (mobile + tree styling) ----------------
st.markdown(
    """
    <style>
        :root { --brand:#0b6cff; --bg:#f5f7fb; --card:#ffffff; --muted:#667085; --border:#e4e7ec; }
        html, body { background: var(--bg); }
        .main {
            background: var(--card);
            border-radius: 16px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.06);
            padding: 18px;
            margin: 12px auto;
            max-width: 880px;
        }
        .cool-header {
            background: linear-gradient(90deg, #0b6cff, #5b9bff);
            color: #fff;
            padding: 12px 16px;
            border-radius: 12px;
            font-weight: 700;
            text-align: center;
            margin-bottom: 14px;
            position: sticky;
            top: 8px;
            z-index: 10;
        }
        .section-title { font-size: 1rem; font-weight: 600; margin: 10px 0; color: #222; }
        .muted { color: var(--muted); font-size: 13px; }
        .button-row { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 8px; }
        .stButton>button { border-radius: 10px !important; padding: 10px 14px; font-size: 0.95rem; }
        .tree-wrap { position: relative; margin-top: 6px; }
        .tree-line { border-left: 2px solid #e0e0e0; padding-left: 12px; }
        .tree-dot { width: 8px; height: 8px; background: #e0e0e0; border-radius: 50%; position: absolute; left: -4px; top: 12px; }
        .person-card {
            background: #fafcff;
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 10px;
            margin: 6px 0;
        }
        @media (max-width: 600px) {
            .main { padding: 14px; margin: 8px; }
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
            "Sunkemo": {"description": "Child of Shemega + Mohammed", "children": {}, "phone": "", "photo": "", "fixed_generation": False},
            "Jemal":   {"description": "Child of Shemega + Mohammed", "children": {}, "phone": "", "photo": "", "fixed_generation": False},
            "Mustefa": {"description": "Child of Shemega + Mohammed", "children": {}, "phone": "", "photo": "", "fixed_generation": False},
            "Rehmet":  {"description": "Child of Shemega + Mohammed", "children": {}, "phone": "", "photo": "", "fixed_generation": False},
            "Bedriya": {"description": "Child of Shemega + Mohammed", "children": {}, "phone": "", "photo": "", "fixed_generation": False},
        },
    },
    "Nurseba": {"description":"Mother Nurseba","phone":"0911333444","partner":"Mohammed","locked_partner":True,"locked_root":True,"photo":"","children":{}},
    "Dilbo":   {"description":"Mother Dilbo","phone":"0911444555","partner":"Mohammed","locked_partner":True,"locked_root":True,"photo":"","children":{}},
    "Rukiya":  {"description":"Mother Rukiya","phone":"0911555666","partner":"Mohammed","locked_partner":True,"locked_root":True,"photo":"","children":{}},
    "Nefissa": {"description":"Mother Nefissa","phone":"0911666777","partner":"Mohammed","locked_partner":True,"locked_root":True,"photo":"","children":{}},
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

# ---------------- Helpers ----------------
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

# ---------------- Display (tree + full features) ----------------
def display_family(name, data, ancestors=None, level=0):
    if ancestors is None:
        ancestors = []
    path = ancestors + [name]
    key_base = "_".join(path).replace(" ", "_")

    # live node
    node, parent_children = get_node_and_parent_children(path)
    if node is None:
        node = data

    partner_live = node.get("partner", "")
    locked = node.get("locked_partner", False)
    fixed = node.get("fixed_generation", False)
    locked_root = node.get("locked_root", False)
    partner_display = "Wife of Mohammed" if name in MOTHERS_WITH_DEFAULT_PARTNER else (partner_live or "Single")

    # Tree wrapper with indentation
    indent_px = level * 20
    st.markdown(f"<div class='tree-wrap' style='margin-left:{indent_px}px;'>", unsafe_allow_html=True)
    if level > 0:
        st.markdown("<div class='tree-dot'></div>", unsafe_allow_html=True)
        st.markdown("<div class='tree-line'>", unsafe_allow_html=True)

    # Person card header + info
    with st.container():
        col1, col2 = st.columns([1, 3])
        with col1:
            img = node.get("photo", "")
            show_img = img if (img and os.path.exists(img)) else PLACEHOLDER_IMAGE
            st.image(show_img, width=80)
        with col2:
            st.markdown(f"<div class='person-card'>", unsafe_allow_html=True)
            c1, c2 = st.columns([3, 2])
            with c1:
                st.markdown(f"**{name}**")
                st.markdown(f"<span class='muted'>{partner_display}</span>", unsafe_allow_html=True)
                if node.get("phone"):
                    st.markdown(f"📞 {node['phone']}")
                st.markdown(f"<div class='muted'>{node.get('description','')}</div>", unsafe_allow_html=True)
            with c2:
                if not locked_root:
                    if st.button(f"Edit {name}", key=f"edit_{key_base}"):
                        st.session_state[f"edit_mode_{key_base}"] = True
                        st.session_state.pop(f"partner_mode_{key_base}", None)
                        st.session_state.pop(f"child_mode_{key_base}", None)
                    if st.button("❌ Delete", key=f"del_{key_base}"):
                        if name in parent_children:
                            parent_children.pop(name, None)
                            save_and_rerun()

            # Single action spot (same place): Add partner OR Add child
            if not locked_root:
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
            st.markdown(f"</div>", unsafe_allow_html=True)  # close person-card

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
                    node["partner"] = pname.strip()
                    node.setdefault("children", {})
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
                    child = {"description": cdesc, "children": {}, "phone": cphone, "photo": ""}
                    if cphoto:
                        child["photo"] = save_uploaded_photo(cphoto, path + [cname])
                    node.setdefault("children", {})[cname] = child
                    st.session_state.pop(f"child_mode_{key_base}", None)
                    save_and_rerun()

    # Edit mode (non-root only)
    if st.session_state.get(f"edit_mode_{key_base}", False) and not locked_root:
        with st.form(f"form_edit_{key_base}"):
            nname = st.text_input("Name", value=name, key=f"en_{key_base}")
            desc = st.text_area("Description", value=node.get("description", ""), key=f"ed_{key_base}")
            phone = st.text_input("Phone", value=node.get("phone", ""), key=f"ep_{key_base}")
            if locked:
                st.text_input("Partner", value=partner_live, disabled=True, key=f"epl_{key_base}")
                pval = partner_live
            else:
                pval = st.text_input("Partner", value=partner_live, key=f"epv_{key_base}")
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

    # Close tree wrappers for children indentation
    if level > 0:
        st.markdown("</div>", unsafe_allow_html=True)  # close tree-line
    st.markdown("</div>", unsafe_allow_html=True)      # close tree-wrap

    # Recurse children
    for ch, cd in list(node.get("children", {}).items()):
        display_family(ch, cd, ancestors=path, level=level + 1)

# ---------------- MAIN ----------------
st.markdown('<div class="main">', unsafe_allow_html=True)
st.markdown("<div class='cool-header'>🌳 Delko's Family Tree</div>", unsafe_allow_html=True)

# Reset button
if st.button("🔄 Reset All Data", key="reset_all"):
    save_family_data(copy.deepcopy(default_family_data))
    st.session_state.clear()
    st.rerun()

# Quiz + gate
if not st.session_state.quiz_done:
    q = st.session_state.current_question
    st.markdown("<div class='section-title'>🔐 Family Quiz</div>", unsafe_allow_html=True)
    ans = st.text_input(q["question"], key="quiz_answer")
    if st.button("Submit", key="quiz_submit"):
        if ans.strip().lower() == q["answer"].lower():
            st.session_state.quiz_done = True
            st.rerun()
        else:
            st.error("Wrong! Try again.")
else:
    st.markdown("<div class='section-title'>🌿 Tree view</div>", unsafe_allow_html=True)
    # Top-level mothers
    for mother, md in st.session_state.family_data.items():
        display_family(mother, md, ancestors=[], level=0)
    # Save changes
    if st.button("💾 Save Changes", key="save_changes"):
        save_family_data(st.session_state.family_data)
        st.success("Changes saved.")

st.markdown("</div>", unsafe_allow_html=True)
