import streamlit as st
import streamlit.components.v1 as components
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

# ---------------- Enhanced CSS ----------------
st.markdown("""
<style>
:root {
  --bg:#f5f7fa;
  --card:#ffffff;
  --accent:#0b6cff;
  --green:#2e7d32;
  --red:#c62828;
  --gray:#666;
  --muted:#667085;
  --border:#e0e4ea;
}
html,body { background:var(--bg); }
.main {
  background:var(--card);
  border-radius:14px;
  box-shadow:0 6px 20px rgba(15,23,42,0.06);
  padding:18px 14px;
  margin:14px auto;
  max-width:920px;
}
.cool-header {
  background:linear-gradient(90deg,#0b6cff,#5b9bff);
  color:#fff;
  padding:10px 14px;
  border-radius:12px;
  font-weight:700;
  font-size:1.3rem;
  text-align:center;
  margin-bottom:12px;
}
.section-title {
  font-size:1.05rem;
  font-weight:600;
  margin:10px 0 6px;
  color:#111827;
}
.stExpander {
  border:1px solid var(--border);
  border-radius:12px !important;
  overflow:hidden;
  margin-bottom:4px;
}
.stExpander > div > div { padding:8px 10px; }
.person-name { font-size:1.02rem; font-weight:650; color:var(--accent); margin-bottom:2px; }
.muted { color:var(--muted); font-size:13px; margin-bottom:2px; }
.phone-link a { color:var(--green); text-decoration:none; font-weight:600; }
.stButton>button {
  border-radius:10px !important;
  padding:10px 14px;
  font-size:0.95rem;
  font-weight:600;
}
button.partner { background:#e6f0ff !important; border:1px solid #0b6cff !important; color:#0b6cff !important; }
button.child { background:#e8f5e9 !important; border:1px solid #2e7d32 !important; color:#2e7d32 !important; }
button.edit { background:#f5f5f5 !important; border:1px solid #666 !important; color:#555 !important; }
button.delete { background:#ffebee !important; border:1px solid #c62828 !important; color:#c62828 !important; }
@media (max-width:600px) {
  .main { padding:14px 10px; margin:8px; }
  .cool-header { font-size:1.05rem; padding:10px; }
  .stButton>button { width:100% !important; font-size:1rem; padding:12px; }
}
</style>
""", unsafe_allow_html=True)

# ---------------- Quiz ----------------
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
        "locked_root": True,
        "photo": "",
        "children": {
            "Sunkemo": {"description": "Child of Shemega + Mohammed", "children": {}, "phone": "0911222333", "photo": "", "fixed_generation": False},
            "Jemal": {"description": "Child of Shemega + Mohammed", "children": {}, "phone": "0911222334", "photo": "", "fixed_generation": False},
            "Mustefa": {"description": "Child of Shemega + Mohammed", "children": {}, "phone": "0911222337", "photo": "", "fixed_generation": False},
            "Rehmet": {"description": "Child of Shemega + Mohammed", "children": {}, "phone": "0911222335", "photo": "", "fixed_generation": False},
            "Bedriya": {"description": "Child of Shemega + Mohammed", "children": {}, "phone": "0911222336", "photo": "", "fixed_generation": False},
        },
    },
    "Nurseba": {"description": "Mother Nurseba", "phone": "0911333444", "partner": "Mohammed", "locked_partner": True, "locked_root": True, "photo": "", "children": {}},
    "Dilbo": {"description": "Mother Dilbo", "phone": "0911444555", "partner": "Mohammed", "locked_partner": True, "locked_root": True, "photo": "", "children": {}},
    "Rukiya": {"description": "Mother Rukiya", "phone": "0911555666", "partner": "Mohammed", "locked_partner": True, "locked_root": True, "photo": "", "children": {}},
    "Nefissa": {"description": "Mother Nefissa", "phone": "0911666777", "partner": "Mohammed", "locked_partner": True, "locked_root": True, "photo": "", "children": {}},
}

# ---------------- Load / Save helpers ----------------
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

# ---------------- Init session state ----------------
if "family_data" not in st.session_state:
    st.session_state.family_data = load_family_data()
if "quiz_done" not in st.session_state:
    st.session_state.quiz_done = False
if "current_question" not in st.session_state:
    st.session_state.current_question = random.choice(quiz_questions)

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
def display_family(name, data, ancestors=None, level=0):
    if ancestors is None:
        ancestors = []
    path = ancestors + [name]
    key_base = "_".join(path).replace(" ", "_")

    node, parent_children = get_node_and_parent_children(path)
    if node is None:
        node = data

    partner_live = node.get("partner", "")
    locked = node.get("locked_partner", False)
    fixed = node.get("fixed_generation", False)
    locked_root = node.get("locked_root", False)
    partner_display = "Wife of Mohammed" if name in MOTHERS_WITH_DEFAULT_PARTNER else (partner_live or "Single")

    indent_px = level * 18
    st.markdown(f"<div style='margin-left:{indent_px}px;'>", unsafe_allow_html=True)

    with st.expander(f"👤 {name} — {partner_display}", expanded=False):
        col1, col2 = st.columns([1, 3], gap="small")

        # --- Left column: photo + Add Partner/Child button ---
        with col1:
            img = node.get("photo", "")
            show_img = img if (img and os.path.exists(img)) else PLACEHOLDER_IMAGE
            st.image(show_img, width=140)

            # Wide action button below photo
            if (not locked_root) and (not locked) and (not partner_live):
                if st.button("💍 Add Partner", key=f"btn_partner_{key_base}"):
                    st.session_state[f"partner_mode_{key_base}"] = True
                    st.session_state.pop(f"child_mode_{key_base}", None)
                    st.session_state.pop(f"edit_mode_{key_base}", None)
            elif (not locked_root) and (partner_live) and (not fixed):
                if st.button("➕ Add Child", key=f"btn_child_{key_base}"):
                    st.session_state[f"child_mode_{key_base}"] = True
                    st.session_state.pop(f"partner_mode_{key_base}", None)
                    st.session_state.pop(f"edit_mode_{key_base}", None)

        # --- Right column: info + Edit/Delete inline with description ---
        with col2:
            st.markdown(f"<div class='person-name'>{name}</div>", unsafe_allow_html=True)

            desc_col, btn_col = st.columns([3, 2], gap="small")
            with desc_col:
                st.markdown(f"<div class='muted'>{node.get('description','')}</div>", unsafe_allow_html=True)
                if node.get("phone"):
                    phone = node.get("phone")
                    st.markdown(f"<div class='phone-link'><a href='tel:{phone}'>{phone}</a></div>", unsafe_allow_html=True)

            with btn_col:
                if not locked_root:
                    if st.button("✏️ Edit", key=f"edit_{key_base}"):
                        st.session_state[f"edit_mode_{key_base}"] = True
                        st.session_state.pop(f"partner_mode_{key_base}", None)
                        st.session_state.pop(f"child_mode_{key_base}", None)
                    if st.button("❌ Delete", key=f"del_{key_base}"):
                        if name in parent_children:
                            parent_children.pop(name, None)
                            save_and_rerun()

            # Partner form
            if st.session_state.get(f"partner_mode_{key_base}", False):
                with st.form(f"form_partner_{key_base}"):
                    pname = st.text_input("Partner name", key=f"pn_{key_base}")
                    if st.form_submit_button("Save partner"):
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
                    if st.form_submit_button("Save child"):
                        if not cname.strip():
                            st.error("Name required")
                        else:
                            child = {"description": cdesc, "children": {}, "phone": cphone, "photo": ""}
                            if cphoto:
                                child["photo"] = save_uploaded_photo(cphoto, path + [cname])
                            node.setdefault("children", {})[cname] = child
                            st.session_state.pop(f"child_mode_{key_base}", None)
                            save_and_rerun()

            # Edit form
            if st.session_state.get(f"edit_mode_{key_base}", False) and not locked_root:
                with st.form(f"form_edit_{key_base}"):
                    nname = st.text_input("Name", value=name, key=f"en_{key_base}")
                    desc = st.text_area("Description", value=node.get("description", ""), key=f"ed_{key_base}")
                    phone = st.text_input("Phone", value=node.get("phone", ""), key=f"ep_{key_base}")
                    if locked:
                        st.text_input("Partner", value=node.get("partner", ""), disabled=True, key=f"pp_{key_base}")
                        pval = node.get("partner", "")
                    else:
                        pval = st.text_input("Partner", value=node.get("partner", ""), key=f"epv_{key_base}")
                    photo = st.file_uploader("New photo", type=["jpg", "jpeg", "png"], key=f"eph_{key_base}")
                    save_edit = st.form_submit_button("Save")
                    cancel_edit = st.form_submit_button("Cancel")
                    if cancel_edit:
                        st.session_state.pop(f"edit_mode_{key_base}", None)
                        st.rerun()
                    if save_edit:
                        parent = get_parent_container(ancestors)
                        if nname.strip() and (nname == name or nname not in parent):
                            node["description"] = desc
                            node["phone"] = phone
                            node["partner"] = pval
                            if photo:
                                node["photo"] = save_uploaded_photo(photo, path)
                            if nname != name:
                                parent.pop(name, None)
                                parent[nname] = node
                            st.session_state.pop(f"edit_mode_{key_base}", None)
                            save_and_rerun()
                        else:
                            st.error("Invalid or duplicate name")

        # Recurse into children
        for ch, cd in list(node.get("children", {}).items()):
            display_family(ch, cd, ancestors=path, level=level + 1)

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- MAIN ----------------
st.markdown('<div class="main">', unsafe_allow_html=True)
st.markdown('<div class="cool-header">👨‍👩‍👧 Delko\'s Family Data Record</div>', unsafe_allow_html=True)


#         reset button

# if st.button("🔄 Reset All Data", key="reset_all"):
#     save_family_data(copy.deepcopy(default_family_data))
#     st.session_state.clear()
#     st.rerun()




# Quiz gate — block everything until answered correctly
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
    st.stop()

# Family tree (only shown after quiz passed)
st.markdown('<div class="section-title">🌳 Family Tree</div>', unsafe_allow_html=True)
for mother, md in st.session_state.family_data.items():
    display_family(mother, md, ancestors=[], level=0)


#          save button

# if st.button("💾 Save Changes", key="save_changes"):
#     save_family_data(st.session_state.family_data)
#     st.success("Changes saved.")





st.markdown('</div>', unsafe_allow_html=True)

# ---------------- JS: tag buttons for CSS coloring ----------------
components.html("""
<script>
(function () {
  const map = {
    "💍 Add Partner": "partner",
    "➕ Add Child": "child",
    "❌ Delete": "delete",
    "✏️ Edit": "edit"
  };
  function tagButtons() {
    document.querySelectorAll('button').forEach(btn => {
      const txt = (btn.innerText || '').trim();
      if (map[txt]) btn.classList.add(map[txt]);
    });
  }
  setTimeout(tagButtons, 150);
  const obs = new MutationObserver(() => setTimeout(tagButtons, 50));
  obs.observe(document.body, { childList: true, subtree: true });
})();
</script>
""", height=0, scrolling=False)
