import streamlit as st
import streamlit.components.v1 as components
import json, os, copy, uuid, random, difflib

# ---------------- SIDEBAR ABOUT ----------------
def display_about():
    st.sidebar.header("About This App")
    st.sidebar.info("""
    This family tree application allows users to visualize and manage their family trees.

    Developed by [Your Name] - a passionate developer dedicated to creating intuitive and engaging applications.

    If you have any questions or feedback, feel free to reach out!
    """)

display_about()

# ---------------- CONFIG & CONSTANTS ----------------
st.set_page_config(page_title="Imam Mohammed's Family Data Center", layout="centered")

DATA_FILE = "family_data.json"
PHOTO_DIR = "photos"
os.makedirs(PHOTO_DIR, exist_ok=True)
PLACEHOLDER_IMAGE = "https://via.placeholder.com/150?text=No+Photo"
MOTHERS_WITH_DEFAULT_PARTNER = ["Shemege", "Nursebe", "Dilbo", "Rukiya", "Nefissa"]

# ---------------- STYLES ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
body { font-family: 'Poppins', sans-serif; background: linear-gradient(to bottom right, #f5f7fa, #c3cfe2); }
.main { background: rgba(255, 255, 255, 0.95); border-radius: 10px; padding: 1rem; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
.cool-header { display:flex; align-items:center; justify-content:space-between; gap:12px; text-align: left; font-size: 1.5rem; color: #3f72af; background-color: #dbe2ef; padding: 0.5rem 0.8rem; border-radius: 10px; margin-bottom: 1rem; }
.header-title { font-weight:600; }
.search-fab { background: linear-gradient(45deg,#3f72af,#112d4e); color: white; border-radius: 999px; padding:8px 14px; border:none; cursor:pointer; box-shadow:0 6px 18px rgba(16,24,40,0.12); }
.section-title { color: #112d4e; border-left: 4px solid #3f72af; padding-left: 8px; font-size: 1.2rem; margin-top: 1rem; }
.person-name { font-weight: 600; font-size: 1rem; color: #112d4e; }
.muted { color: #3f3f3f; font-size: 0.85rem; }
.phone-link a { color: #3f72af; text-decoration: none; font-weight: bold; }
.phone-link a:hover { text-decoration: underline; }
button[data-baseweb="button"] { background: linear-gradient(45deg, #3f72af, #112d4e) !important; color: white !important; border: none !important; border-radius: 8px !important; padding: 0.5rem 1rem; transition: 0.3s; }
button[data-baseweb="button"]:hover { background: linear-gradient(45deg, #112d4e, #3f72af) !important; transform: scale(1.05); }
.stTextInput > div > div > input, .stNumberInput input, .stTextArea textarea { border-radius: 8px; border: 1px solid #ccc; padding: 0.5rem; }
.report-box { border: 1px solid #e6eefc; padding: 10px; border-radius: 8px; background: #f7fbff; margin-top: 10px; }
.report-item { font-weight: 600; color: #0b6cff; margin-bottom: 4px; }
.search-result { border:1px dashed #e6eefc; padding:8px; border-radius:6px; margin-bottom:6px; background:#ffffff; }
</style>
""", unsafe_allow_html=True)

# ---------------- QUIZ ----------------
quiz_questions = [
    {"question": "How many children did Sunkemo have?", "answer": "9"},
    {"question": "How many wives did Mohammed have?", "answer": "5"},
    {"question": "How many children did mother Shemega have?", "answer": "5"},
    {"question": "How many children did mother Nurseba have?", "answer": "9"},
    {"question": "How many children did mother Dilbo have?", "answer": "4"},
]

# ---------------- DEFAULT DATA ----------------
default_family_data = {
    "Shemege": {
        "description": "Mother Shemege", "phone": "may Allah grant her jenahh", "partner": "imam Mohammed",
        "locked_partner": True, "locked_root": True, "photo": "",
        "children": {
            "Sunkemo": {"description": "Child of Shemege + Mohammed", "children": {}, "phone": "0911222333", "photo": "", "fixed_generation": False},
            "Bedriya": {"description": "Child of Shemege + Mohammed", "children": {}, "phone": "0911222334", "photo": "", "fixed_generation": False},
            "Rahmet": {"description": "Child of Shemege + Mohammed", "children": {}, "phone": "0911222337", "photo": "", "fixed_generation": False},
            "Mustefa": {"description": "Child of Shemege + Mohammed", "children": {}, "phone": "0911222335", "photo": "", "fixed_generation": False},
            "Jemal": {"description": "Child of Shemege + Mohammed", "children": {}, "phone": "0911222336", "photo": "", "fixed_generation": False},
        },
    },
    "Nursebe": {
        "description": "Mother Nursebe", "phone": "0911333444", "partner": "imam Mohammed",
        "locked_partner": True, "locked_root": True, "photo": "",
        "children": {
            "Sefiya": {"description": "Child of Nursebe + Mohammed", "children": {}, "phone": "0911555555", "photo": "", "fixed_generation": False},
            "Oumer": {"description": "Child of Nursebe + Mohammed", "children": {}, "phone": "0911555555", "photo": "", "fixed_generation": False},
            "Ayro": {"description": "Child of Nursebe + Mohammed", "children": {}, "phone": "0911555555", "photo": "", "fixed_generation": False},
            "Selima": {"description": "Child of Nursebe + Mohammed", "children": {}, "phone": "0911555555", "photo": "", "fixed_generation": False},
            "Reshad": {"description": "Child of Nursebe + Mohammed", "children": {}, "phone": "0911555555", "photo": "", "fixed_generation": False},
            "Fetiya": {"description": "Child of Nursebe + Mohammed", "children": {}, "phone": "0911555555", "photo": "", "fixed_generation": False},
            "Aliyu": {"description": "Child of Nursebe + Mohammed", "children": {}, "phone": "0911555555", "photo": "", "fixed_generation": False},
            "Neja": {"description": "Child of Nursebe + Mohammed", "children": {}, "phone": "0911555555", "photo": "", "fixed_generation": False},
        },
    },
    "Dilbo": {
        "description": "Mother Dilbo", "phone": "may Allah grant her jennahh", "partner": "imam Mohammed",
        "locked_partner": True, "locked_root": True, "photo": "",
        "children": {
            "Sadik": {"description": "Child of Dilbo + Mohammed", "children": {}, "phone": "0911555555", "photo": "", "fixed_generation": False},
            "Bahredin": {"description": "Child of Dilbo + Mohammed", "children": {}, "phone": "0911555555", "photo": "", "fixed_generation": False},
            "Nasir": {"description": "Child of Dilbo + Mohammed", "children": {}, "phone": "0911555555", "photo": "", "fixed_generation": False},
            "Abdusemed": {"description": "Child of Nurseba + Mohammed", "children": {}, "phone": "0911555555", "photo": "", "fixed_generation": False},
        },
    },
    "Rukiya": {
        "description": "Mother Rukiya", "phone": "0911333444", "partner": "imam Mohammed",
        "locked_partner": True, "locked_root": True, "photo": "",
        "children": {
            "Beytulah": {"description": "Child of Rukiya + Mohammed", "children": {}, "phone": "0911555555", "photo": "", "fixed_generation": False},
            "Leyla": {"description": "Child of Rukiya + Mohammed", "children": {}, "phone": "0911555555", "photo": "", "fixed_generation": False},
            "Zulfa": {"description": "Child of Rukiya + Mohammed", "children": {}, "phone": "0911555555", "photo": "", "fixed_generation": False},
            "Ishak": {"description": "Child of Rukiya + Mohammed", "children": {}, "phone": "0911555555", "photo": "", "fixed_generation": False},
            "Mubarek": {"description": "Child of Rukiya + Mohammed", "children": {}, "phone": "0911555555", "photo": "", "fixed_generation": False},
            "Hayat": {"description": "Child of Rukiya + Mohammed", "children": {}, "phone": "0911555555", "photo": "", "fixed_generation": False},
        },
    },
    "Nefissa": {
        "description": "Mother Nefissa", "phone": "0911333444", "partner": "Imam Mohammed",
        "locked_partner": True, "locked_root": True, "photo": "",
        "children": {
            "Abdurezak": {"description": "Child of Nefissa + Mohammed", "children": {}, "phone": "0911555555", "photo": "", "fixed_generation": False},
        },
    }
}

# ---------------- UTILITIES ----------------
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

# ---------------- SESSION STATE ----------------
if "family_data" not in st.session_state:
    st.session_state.family_data = load_family_data()
if "quiz_done" not in st.session_state:
    st.session_state.quiz_done = False
if "current_question" not in st.session_state:
    st.session_state.current_question = random.choice(quiz_questions)
# search UI state
if "show_search" not in st.session_state:
    st.session_state.show_search = False
if "last_search" not in st.session_state:
    st.session_state.last_search = ""
if "search_results" not in st.session_state:
    st.session_state.search_results = []
# reveal path for "show in tree"
if "reveal_path" not in st.session_state:
    st.session_state.reveal_path = None

# ---------------- COUNTING / REPORT ----------------
def count_levels(node):
    counts = {"gen1": 0, "gen2": 0, "gen3": 0, "gen4": 0}
    def dfs(child_node, depth):
        if not isinstance(child_node, dict): return
        if depth == 1: counts["gen2"] += 1
        elif depth == 2: counts["gen3"] += 1
        elif depth == 3: counts["gen4"] += 1
        if depth < 3:
            for sub in child_node.get("children", {}).values():
                dfs(sub, depth+1)
    is_top = isinstance(node, dict) and any(isinstance(v, dict) and ("description" in v or "children" in v) for v in node.values())
    if is_top:
        roots = [v for v in node.values() if isinstance(v, dict)]
        counts["gen1"] = len(roots)
        for r in roots:
            for ch in r.get("children", {}).values():
                dfs(ch, 1)
    else:
        counts["gen1"] = 1
        for ch in node.get("children", {}).values():
            dfs(ch, 1)
    counts["total_descendants"] = counts["gen2"] + counts["gen3"] + counts["gen4"]
    return counts

# ---------------- SEARCH (fuzzy) ----------------
def fuzzy_score(a, b):
    """Return a normalized similarity score between 0..1 using difflib."""
    if not a or not b:
        return 0.0
    return difflib.SequenceMatcher(None, a, b).ratio()

def find_nodes_by_name_fuzzy(query, max_results=50, threshold=0.45):
    """
    Return list of (score, path_list, node) sorted by descending score.
    threshold: minimal score to include (0..1). lower -> more permissive.
    """
    q = (query or "").strip().lower()
    results = []
    if not q:
        return results

    def _dfs(node, path):
        if not isinstance(node, dict):
            return
        name = path[-1]
        desc = node.get("description", "")
        # compute several heuristics
        score_name = fuzzy_score(q, name.lower())
        score_desc = fuzzy_score(q, desc.lower())
        contains = int(q in name.lower() or q in desc.lower())
        partial_token = 0
        # check tokens (e.g. query 'sunk' should match 'Sunkemo')
        for tok in name.lower().split():
            if tok.startswith(q) or q.startswith(tok):
                partial_token = 0.75
                break
        # final score combines heuristics
        combined = max(score_name, score_desc, contains * 0.9, partial_token)
        if combined >= threshold:
            results.append((combined, path.copy(), node))
        # traverse children
        for child_name, child_node in node.get("children", {}).items():
            _dfs(child_node, path + [child_name])

    for root_name, root_node in st.session_state.family_data.items():
        _dfs(root_node, [root_name])

    # sort and return top N
    results.sort(key=lambda x: x[0], reverse=True)
    return results[:max_results]

def display_search_results(results):
    if not results:
        st.info("No matches found.")
        return
    st.write(f"Found {len(results)} match(es):")
    for i, (score, path, node) in enumerate(results):
        name = path[-1]
        path_str = " → ".join(path)
        rep = count_levels(node)
        st.markdown(f"<div class='search-result'><b>{name}</b> <div style='font-size:0.9rem;color:#555;'>Path: {path_str} — score: {score:.2f}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='margin-top:6px;'>📞 {node.get('phone','-')} &nbsp; | &nbsp; Children: <b>{rep['gen2']}</b> &nbsp; Grandchildren: <b>{rep['gen3']}</b> &nbsp; Great-grandchildren: <b>{rep['gen4']}</b></div>", unsafe_allow_html=True)
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button(f"Show in tree", key=f"show_in_tree_{i}_{'_'.join(path)}"):
                st.session_state.reveal_path = path
                save_and_rerun()
        with col2:
            img = node.get('photo','')
            show_img = img if (img and os.path.exists(img)) else PLACEHOLDER_IMAGE
            st.image(show_img, width=80)
        st.markdown("</div>", unsafe_allow_html=True)

# ---------------- TREE HELPERS / UI ----------------
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

    indent_px = level * 10
    reveal = st.session_state.get('reveal_path')
    should_expand = False
    if reveal and isinstance(reveal, list) and len(reveal) >= 1:
        if path == reveal[:len(path)]:
            should_expand = True
            if path == reveal:
                st.session_state.pop('reveal_path', None)

    st.markdown(f"<div style='margin-left:{indent_px}px; margin-bottom: 8px;'>", unsafe_allow_html=True)
    with st.expander(f"👤 {name} — {partner_display}", expanded=should_expand):
        col1, col2 = st.columns([1, 3], gap="small")
        with col1:
            img = node.get("photo", "")
            show_img = img if (img and os.path.exists(img)) else PLACEHOLDER_IMAGE
            st.image(show_img, width=100)
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

        with col2:
            st.markdown(f"<div class='person-name'>{name}</div>", unsafe_allow_html=True)
            desc_col, btn_col = st.columns([3, 1], gap="small")
            with desc_col:
                st.markdown(f"<div class='muted'>{node.get('description','')}</div>", unsafe_allow_html=True)
                if node.get("phone"):
                    st.markdown(f"<div class='phone-link'>📞 <a href='tel:{node['phone']}'>{node['phone']}</a></div>", unsafe_allow_html=True)

                if st.button("📊 Show Report", key=f"rep_btn_{key_base}"):
                    st.session_state[f"show_report_{key_base}"] = not st.session_state.get(f"show_report_{key_base}", False)

                if st.session_state.get(f"show_report_{key_base}", False):
                    rep = count_levels(node)
                    st.markdown(f"""
                    <div class="report-box" style="margin-top: 5px;">
                        <div style="font-weight:700;color:#0b6cff;">📊 {name}'s Family Summary</div>
                        <div class="report-item">Children: <b>{rep['gen2']}</b></div>
                        <div class="report-item">Grandchildren: <b>{rep['gen3']}</b></div>
                        <div class="report-item">Great-grandchildren: <b>{rep['gen4']}</b></div>
                        <div style="font-weight:700;margin-top: 4px;">Total Descendants: <b>{rep['total_descendants']}</b></div>
                    </div>
                    """, unsafe_allow_html=True)

            with btn_col:
                if not locked_root:
                    if st.button("✏️ Edit", key=f"edit_{key_base}"):
                        st.session_state[f"edit_mode_{key_base}"] = True
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
                            child = {"description": cdesc, "children": {}, "phone": cphone, "photo": "", "fixed_generation": False}
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

        # Recursive display
        for ch, cd in list(node.get("children", {}).items()):
            display_family(ch, cd, ancestors=path, level=level + 1)

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- MAIN APP ----------------
st.markdown('<div class="main">', unsafe_allow_html=True)

# header area with stylish search button on the right
st.markdown(f'''
<div class="cool-header">
  <div class="header-title">👨‍👩‍👧 Imam Mohammed's Family Data Center</div>
  <div>
    <!-- Use a Streamlit button below; CSS class name used to style it visually -->
    <form action="/" method="get" style="display:inline;">
      <!-- placeholder so layout keeps spacing — actual Streamlit button below handles toggling -->
    </form>
  </div>
</div>
''', unsafe_allow_html=True)

# place the search toggle button to the right using columns (only visible after quiz)
hcol1, hcol2 = st.columns([6,1])

# ensure the search form is hidden while quiz not done
if not st.session_state.get("quiz_done", False):
    st.session_state.show_search = False

with hcol2:
    # show the search toggle only after quiz is completed
    if st.session_state.get("quiz_done", False):
        if st.button("🔎 Search", key="toggle_search"):
            st.session_state.show_search = not st.session_state.show_search


# Reset
# if st.button("🔄 Reset All Data", key="reset_all"):
#     save_family_data(copy.deepcopy(default_family_data))
#     st.session_state.clear()
#     st.rerun()

# Quiz gate
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

# --- SEARCH UI: only show when show_search True ---
if st.session_state.show_search:
    st.markdown('<div class="section-title">🔎 Search</div>', unsafe_allow_html=True)
    with st.form("search_form"):
        search_query = st.text_input("Search by name or description (fuzzy)", value=st.session_state.get('last_search', ''))
        search_submit = st.form_submit_button("Search")
        if search_submit:
            st.session_state.last_search = search_query
            st.session_state.search_results = find_nodes_by_name_fuzzy(search_query, threshold=0.45)
            # hide the form after a search (per your requirement)
            st.session_state.show_search = False

# Display search results (they persist until next search)
if st.session_state.get('search_results'):
    st.markdown('<div style="margin-top:8px;margin-bottom:8px;">', unsafe_allow_html=True)
    display_search_results(st.session_state.search_results)
    st.markdown('</div>', unsafe_allow_html=True)

# Family Tree
st.markdown('<div class="section-title">🌳 Family Tree</div>', unsafe_allow_html=True)
for mother, md in st.session_state.family_data.items():
    display_family(mother, md, ancestors=[], level=0)

# ---------------- FAMILY REPORT ----------------
rep = count_levels(st.session_state.family_data)
st.markdown("""
<div class="report-box">
  <div style="font-weight:700; color:#0b6cff; margin-bottom:8px;">📊 Family Report Summary</div>
  <div class="report-item">Wives: <span style="font-weight:800; color:#111;">{m}</span></div>
  <div class="report-item">Children: <span style="font-weight:800; color:#111;">{c}</span></div>
  <div class="report-item">Grandchildren: <span style="font-weight:800; color:#111;">{g}</span></div>
  <div class="report-item">Great-grandchildren: <span style="font-weight:800; color:#111;">{gr}</span></div>
  <hr>
  <div class="report-item">Total descendants: <span style="font-weight:900; color:#111;">{t}</span></div>
</div>
""".format(m=rep["gen1"], c=rep["gen2"], g=rep["gen3"], gr=rep["gen4"], t=rep["total_descendants"]), unsafe_allow_html=True)

# # Save button
# if st.button("💾 Save Changes", key="save_changes"):
#     save_family_data(st.session_state.family_data)
#     st.success("Changes saved successfully!")

st.markdown('</div>', unsafe_allow_html=True)

# Button labeling JS (keeps your class additions)
components.html("""
<script>
(function () {
  const map = {"💍 Add Partner": "partner", "➕ Add Child": "child", "❌ Delete": "delete", "✏️ Edit": "edit"};
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




             # Amharic Version
# import streamlit as st
# import streamlit.components.v1 as components
# import json, os, copy, uuid, random, difflib
#
# # ---------------- VISIBLE NAME MAPPING (only display text changed) ----------------
# # internal keys remain English; this dict maps those keys to Amharic for display only
# DISPLAY_NAME = {
#     "Mohammed": "ሙሀመድ",
#     "Shemege": "ሸመጌ",
#     "Nursebe": "ኑርሰቤ",
#     "Dilbo": "ዲልቦ",
#     "Rukiya": "ሩቂያ",
#     "Nefissa": "ነፊሳ",
#     "Sunkemo": "ሱንከሞ",
#     "Bedriya": "በድሪያ",
#     "Rahmet": "ራሕመት",
#     "Mustefa": "ሙስጠፋ",
#     "Jemal": "ጀማል",
#     "Oumer": "ኡመር",
#     "Sefiya": "ሰፊያ",
#     "Ayro": "አይሮ",
#     "Selima": "ሰሊማ",
#     "Reshad": "ረሻድ",
#     "Fetiya": "ፈቲያ",
#     "Aliyu": "አልዩ",
#     "Neja": "ነጃ",
#     "Sadik": "ሳዲቅ",
#     "Bahredin": "ባሕረዲን",
#     "Nasir": "ናስር",
#     "Abdusemed": "አብዱሰመድ",
#     "Beytulah": "በይቱላህ",
#     "Leyla": "ለይላ",
#     "Zulfa": "ዙልፋ",
#     "Ishak": "ኢስሃቅ",
#     "Mubarek": "ሙባረክ",
#     "Hayat": "ሃያት",
#     "Abdurezak": "አብዱረዛቅ"
# }
#
# # helper to display mapped names
# def disp_name(key):
#     return DISPLAY_NAME.get(key, key)
#
# # ---------------- SIDEBAR ABOUT ----------------
# def display_about():
#     st.sidebar.header("ስለ መተግበሪያው")
#     st.sidebar.info("""
#     ይህ የቤተሰብ መተግበሪያ ተጠቃሚዎችን የቤተሰብ ግንዳቸውን ለማየትና ለማስተካከል ይረዳ ዘንድ የተሰራ ነው፡፡
#     ማንኛውም ጥያቄ ወይም አስተያየት ካለዎት እባኮትን በዚ username  ያግኙን።@nihad_aliyu or @abduselam_abas
#     """)
#
# display_about()
#
# # ---------------- CONFIG & CONSTANTS ----------------
# st.set_page_config(page_title="የኢማም ሙሀመድ የቤተሰብ ዝርዝር", layout="centered")
#
# DATA_FILE = "family_data.json"
# PHOTO_DIR = "photos"
# os.makedirs(PHOTO_DIR, exist_ok=True)
# PLACEHOLDER_IMAGE = "https://via.placeholder.com/150?text=No+Photo"
# MOTHERS_WITH_DEFAULT_PARTNER = ["Shemege", "Nursebe", "Dilbo", "Rukiya", "Nefissa"]
#
# # ---------------- STYLES ----------------
# st.markdown("""
# <style>
# @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
# body { font-family: 'Poppins', sans-serif; background: linear-gradient(to bottom right, #f5f7fa, #c3cfe2); }
# .main { background: rgba(255, 255, 255, 0.95); border-radius: 10px; padding: 1rem; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
# .cool-header { display:flex; align-items:center; justify-content:space-between; gap:12px; text-align: left; font-size: 1.5rem; color: #3f72af; background-color: #dbe2ef; padding: 0.5rem 0.8rem; border-radius: 10px; margin-bottom: 1rem; }
# .header-title { font-weight:600; }
# .search-fab { background: linear-gradient(45deg,#3f72af,#112d4e); color: white; border-radius: 999px; padding:8px 14px; border:none; cursor:pointer; box-shadow:0 6px 18px rgba(16,24,40,0.12); }
# .section-title { color: #112d4e; border-left: 4px solid #3f72af; padding-left: 8px; font-size: 1.2rem; margin-top: 1rem; }
# .person-name { font-weight: 600; font-size: 1rem; color: #112d4e; }
# .muted { color: #3f3f3f; font-size: 0.85rem; }
# .phone-link a { color: #3f72af; text-decoration: none; font-weight: bold; }
# .phone-link a:hover { text-decoration: underline; }
# button[data-baseweb="button"] { background: linear-gradient(45deg, #3f72af, #112d4e) !important; color: white !important; border: none !important; border-radius: 8px !important; padding: 0.5rem 1rem; transition: 0.3s; }
# button[data-baseweb="button"]:hover { background: linear-gradient(45deg, #112d4e, #3f72af) !important; transform: scale(1.05); }
# .stTextInput > div > div > input, .stNumberInput input, .stTextArea textarea { border-radius: 8px; border: 1px solid #ccc; padding: 0.5rem; }
# .report-box { border: 1px solid #e6eefc; padding: 10px; border-radius: 8px; background: #f7fbff; margin-top: 10px; }
# .report-item { font-weight: 600; color: #0b6cff; margin-bottom: 4px; }
# .search-result { border:1px dashed #e6eefc; padding:8px; border-radius:6px; margin-bottom:6px; background:#ffffff; }
# </style>
# """, unsafe_allow_html=True)
#
# # ---------------- QUIZ ----------------
# quiz_questions = [
#     {"question": "ሱንከሞ ስንት ልጆች አሉት?", "answer": "9"},
#     {"question": "እማም ሙሀመድ ስንት ሚስቶች ነበሯችው?", "answer": "5"},
#     {"question": "እናት ሸሜጌ ስንት ልጆች ነበሯት?", "answer": "5"},
#     {"question": "እናት ኑርሴቤ ስንት ልጆች አሏት?", "answer": "9"},
#     {"question": "እናት ዲልቦ ስንት ልጆች ነበሯት?", "answer": "4"},
# ]
#
# # ---------------- DEFAULT DATA (internal keys remain English) ----------------
# default_family_data = {
#     "Shemege": {
#         "description": "እናት Shemege", "phone": "may Allah grant her jenahh", "partner": "Mohammed",
#         "locked_partner": True, "locked_root": True, "photo": "",
#         "children": {
#             "Sunkemo": {"description": "የShemege እና Mohammed ልጅ", "children": {}, "phone": "0911222333", "photo": "", "fixed_generation": False},
#             "Bedriya": {"description": "የShemege እና Mohammed ልጅ", "children": {}, "phone": "0911222334", "photo": "", "fixed_generation": False},
#             "Rahmet": {"description": "የShemege እና Mohammed ልጅ", "children": {}, "phone": "0911222337", "photo": "", "fixed_generation": False},
#             "Mustefa": {"description": "የShemege እና Mohammed ልጅ", "children": {}, "phone": "0911222335", "photo": "", "fixed_generation": False},
#             "Jemal": {"description": "የShemege እና Mohammed ልጅ", "children": {}, "phone": "0911222336", "photo": "", "fixed_generation": False},
#         },
#     },
#     "Nursebe": {
#         "description": "እናት Nursebe", "phone": "0911333444", "partner": "Mohammed",
#         "locked_partner": True, "locked_root": True, "photo": "",
#         "children": {
#             "Sefiya": {"description": "የNursebe እና Mohammed ልጅ", "children": {}, "phone": "0911555555", "photo": "", "fixed_generation": False},
#             "Oumer": {"description": "የNursebe እና Mohammed ልጅ", "children": {}, "phone": "0911555555", "photo": "", "fixed_generation": False},
#             "Ayro": {"description": "የNursebe እና Mohammed ልጅ", "children": {}, "phone": "0911555555", "photo": "", "fixed_generation": False},
#             "Selima": {"description": "የNursebe እና Mohammed ልጅ", "children": {}, "phone": "0911555555", "photo": "", "fixed_generation": False},
#             "Reshad": {"description": "የNursebe እና Mohammed ልጅ", "children": {}, "phone": "0911555555", "photo": "", "fixed_generation": False},
#             "Fetiya": {"description": "የNursebe እና Mohammed ልጅ", "children": {}, "phone": "0911555555", "photo": "", "fixed_generation": False},
#             "Aliyu": {"description": "የNursebe እና Mohammed ልጅ", "children": {}, "phone": "0911555555", "photo": "", "fixed_generation": False},
#             "Neja": {"description": "የNursebe እና Mohammed ልጅ", "children": {}, "phone": "0911555555", "photo": "", "fixed_generation": False},
#         },
#     },
#     "Dilbo": {
#         "description": "እናት Dilbo", "phone": "may Allah grant her jennahh", "partner": "Mohammed",
#         "locked_partner": True, "locked_root": True, "photo": "",
#         "children": {
#             "Sadik": {"description": "የDilbo እና Mohammed ልጅ", "children": {}, "phone": "0911555555", "photo": "", "fixed_generation": False},
#             "Bahredin": {"description": "የDilbo እና Mohammed ልጅ", "children": {}, "phone": "0911555555", "photo": "", "fixed_generation": False},
#             "Nasir": {"description": "የDilbo እና Mohammed ልጅ", "children": {}, "phone": "0911555555", "photo": "", "fixed_generation": False},
#             "Abdusemed": {"description": "የDilbo እና Mohammed ልጅ", "children": {}, "phone": "0911555555", "photo": "", "fixed_generation": False},
#         },
#     },
#     "Rukiya": {
#         "description": "እናት Rukiya", "phone": "0911333444", "partner": "Mohammed",
#         "locked_partner": True, "locked_root": True, "photo": "",
#         "children": {
#             "Beytulah": {"description": "የRukiya እና Mohammed ልጅ", "children": {}, "phone": "0911555555", "photo": "", "fixed_generation": False},
#             "Leyla": {"description": "የRukiya እና Mohammed ልጅ", "children": {}, "phone": "0911555555", "photo": "", "fixed_generation": False},
#             "Zulfa": {"description": "የRukiya እና Mohammed ልጅ", "children": {}, "phone": "0911555555", "photo": "", "fixed_generation": False},
#             "Ishak": {"description": "የRukiya እና Mohammed ልጅ", "children": {}, "phone": "0911555555", "photo": "", "fixed_generation": False},
#             "Mubarek": {"description": "የRukiya እና Mohammed ልጅ", "children": {}, "phone": "0911555555", "photo": "", "fixed_generation": False},
#             "Hayat": {"description": "የRukiya እና Mohammed ልጅ", "children": {}, "phone": "0911555555", "photo": "", "fixed_generation": False},
#         },
#     },
#     "Nefissa": {
#         "description": "እናት Nefissa", "phone": "0911333444", "partner": "Mohammed",
#         "locked_partner": True, "locked_root": True, "photo": "",
#         "children": {
#             "Abdurezak": {"description": "የNefissa እና Mohammed ልጅ", "children": {}, "phone": "0911555555", "photo": "", "fixed_generation": False},
#         },
#     }
# }
#
# # ---------------- UTILITIES ----------------
# def load_family_data():
#     if os.path.exists(DATA_FILE):
#         try:
#             with open(DATA_FILE, "r", encoding="utf-8") as f:
#                 return json.load(f)
#         except Exception:
#             return copy.deepcopy(default_family_data)
#     return copy.deepcopy(default_family_data)
#
# def save_family_data(data):
#     with open(DATA_FILE, "w", encoding="utf-8") as f:
#         json.dump(data, f, indent=4, ensure_ascii=False)
#
# def save_and_rerun():
#     save_family_data(st.session_state.family_data)
#     st.rerun()
#
# def save_uploaded_photo(uploaded_file, path_list):
#     if not uploaded_file:
#         return ""
#     safe_base = "_".join(path_list).replace(" ", "_")
#     _, ext = os.path.splitext(uploaded_file.name)
#     fname = f"{safe_base}_{uuid.uuid4().hex[:6]}{ext or '.jpg'}"
#     filepath = os.path.join(PHOTO_DIR, fname)
#     with open(filepath, "wb") as f:
#         f.write(uploaded_file.getbuffer())
#     return filepath
#
# # ---------------- SESSION STATE ----------------
# if "family_data" not in st.session_state:
#     st.session_state.family_data = load_family_data()
# if "quiz_done" not in st.session_state:
#     st.session_state.quiz_done = False
# if "current_question" not in st.session_state:
#     st.session_state.current_question = random.choice(quiz_questions)
# # search UI state
# if "show_search" not in st.session_state:
#     st.session_state.show_search = False
# if "last_search" not in st.session_state:
#     st.session_state.last_search = ""
# if "search_results" not in st.session_state:
#     st.session_state.search_results = []
# # reveal path for "show in tree"
# if "reveal_path" not in st.session_state:
#     st.session_state.reveal_path = None
#
# # ---------------- COUNTING / REPORT ----------------
# def count_levels(node):
#     counts = {"gen1": 0, "gen2": 0, "gen3": 0, "gen4": 0}
#     def dfs(child_node, depth):
#         if not isinstance(child_node, dict): return
#         if depth == 1: counts["gen2"] += 1
#         elif depth == 2: counts["gen3"] += 1
#         elif depth == 3: counts["gen4"] += 1
#         if depth < 3:
#             for sub in child_node.get("children", {}).values():
#                 dfs(sub, depth+1)
#     is_top = isinstance(node, dict) and any(isinstance(v, dict) and ("description" in v or "children" in v) for v in node.values())
#     if is_top:
#         roots = [v for v in node.values() if isinstance(v, dict)]
#         counts["gen1"] = len(roots)
#         for r in roots:
#             for ch in r.get("children", {}).values():
#                 dfs(ch, 1)
#     else:
#         counts["gen1"] = 1
#         for ch in node.get("children", {}).values():
#             dfs(ch, 1)
#     counts["total_descendants"] = counts["gen2"] + counts["gen3"] + counts["gen4"]
#     return counts
#
# # ---------------- SEARCH (fuzzy) ----------------
# def fuzzy_score(a, b):
#     if not a or not b:
#         return 0.0
#     return difflib.SequenceMatcher(None, a, b).ratio()
#
# def find_nodes_by_name_fuzzy(query, max_results=50, threshold=0.45):
#     q = (query or "").strip().lower()
#     results = []
#     if not q:
#         return results
#
#     def _dfs(node, path):
#         if not isinstance(node, dict):
#             return
#         name = path[-1]
#         desc = node.get("description", "")
#         score_name = fuzzy_score(q, name.lower())
#         score_desc = fuzzy_score(q, desc.lower())
#         contains = int(q in name.lower() or q in desc.lower())
#         partial_token = 0
#         for tok in name.lower().split():
#             if tok.startswith(q) or q.startswith(tok):
#                 partial_token = 0.75
#                 break
#         combined = max(score_name, score_desc, contains * 0.9, partial_token)
#         if combined >= threshold:
#             results.append((combined, path.copy(), node))
#         for child_name, child_node in node.get("children", {}).items():
#             _dfs(child_node, path + [child_name])
#
#     for root_name, root_node in st.session_state.family_data.items():
#         _dfs(root_node, [root_name])
#
#     results.sort(key=lambda x: x[0], reverse=True)
#     return results[:max_results]
#
# def display_search_results(results):
#     if not results:
#         st.info("ምንም ውጤት አልተገኘም።")
#         return
#     st.write(f"ተገኙ {len(results)} ውጤቶች:")
#     for i, (score, path, node) in enumerate(results):
#         # display localized path
#         path_disp = " → ".join(disp_name(p) for p in path)
#         name_disp = disp_name(path[-1])
#         rep = count_levels(node)
#         st.markdown(f"<div class='search-result'><b>{name_disp}</b> <div style='font-size:0.9rem;color:#555;'>መንገድ: {path_disp} — ውጤት ውህድ: {score:.2f}</div>", unsafe_allow_html=True)
#         st.markdown(f"<div style='margin-top:6px;'>📞 {node.get('phone','-')} &nbsp; | &nbsp; ልጆች: <b>{rep['gen2']}</b> &nbsp; የልጆች ልጅ: <b>{rep['gen3']}</b> &nbsp; የልጆች የልጅ ልጅ: <b>{rep['gen4']}</b></div>", unsafe_allow_html=True)
#         col1, col2 = st.columns([1, 4])
#         with col1:
#             if st.button("በዛር ግንድ ያሳዩ", key=f"show_in_tree_{i}_{'_'.join(path)}"):
#                 st.session_state.reveal_path = path
#                 save_and_rerun()
#         with col2:
#             img = node.get('photo','')
#             show_img = img if (img and os.path.exists(img)) else PLACEHOLDER_IMAGE
#             st.image(show_img, width=80)
#         st.markdown("</div>", unsafe_allow_html=True)
#
# # ---------------- TREE HELPERS / UI ----------------
# def get_node_and_parent_children(path):
#     if not path:
#         return None, st.session_state.family_data
#     root = st.session_state.family_data
#     parent_children = root
#     node = None
#     for i, part in enumerate(path):
#         if i == 0:
#             node = root.get(part)
#             parent_children = root
#         else:
#             parent_children = node.get("children", {})
#             node = parent_children.get(part)
#         if node is None:
#             return None, st.session_state.family_data
#     return node, parent_children
#
# def get_parent_container(ancestors):
#     if not ancestors:
#         return st.session_state.family_data
#     node, parent_children = get_node_and_parent_children(ancestors)
#     if node is None:
#         return st.session_state.family_data
#     return parent_children
#
# def display_family(name, data, ancestors=None, level=0):
#     if ancestors is None:
#         ancestors = []
#     path = ancestors + [name]
#     key_base = "_".join(path).replace(" ", "_")
#     node, parent_children = get_node_and_parent_children(path)
#     if node is None:
#         node = data
#     partner_live = node.get("partner", "")
#     locked = node.get("locked_partner", False)
#     fixed = node.get("fixed_generation", False)
#     locked_root = node.get("locked_root", False)
#     partner_display = f"የ {disp_name('Mohammed')}  ሚስት" if name in MOTHERS_WITH_DEFAULT_PARTNER else (disp_name(partner_live) if partner_live else "ነፃ")
#
#     indent_px = level * 10
#     reveal = st.session_state.get('reveal_path')
#     should_expand = False
#     if reveal and isinstance(reveal, list) and len(reveal) >= 1:
#         if path == reveal[:len(path)]:
#             should_expand = True
#             if path == reveal:
#                 st.session_state.pop('reveal_path', None)
#
#     st.markdown(f"<div style='margin-left:{indent_px}px; margin-bottom: 8px;'>", unsafe_allow_html=True)
#     with st.expander(f"👤 {disp_name(name)} — {partner_display}", expanded=should_expand):
#         col1, col2 = st.columns([1, 3], gap="small")
#         with col1:
#             img = node.get("photo", "")
#             show_img = img if (img and os.path.exists(img)) else PLACEHOLDER_IMAGE
#             st.image(show_img, width=100)
#             if (not locked_root) and (not locked) and (not partner_live):
#                 if st.button("👫 የጋብቻ አጋር ያስገቡ", key=f"btn_partner_{key_base}"):
#                     st.session_state[f"partner_mode_{key_base}"] = True
#                     st.session_state.pop(f"child_mode_{key_base}", None)
#                     st.session_state.pop(f"edit_mode_{key_base}", None)
#             elif (not locked_root) and (partner_live) and (not fixed):
#                 if st.button("➕ ልጅ ይመዝግቡ", key=f"btn_child_{key_base}"):
#                     st.session_state[f"child_mode_{key_base}"] = True
#                     st.session_state.pop(f"partner_mode_{key_base}", None)
#                     st.session_state.pop(f"edit_mode_{key_base}", None)
#
#         with col2:
#             st.markdown(f"<div class='person-name'>{disp_name(name)}</div>", unsafe_allow_html=True)
#             desc_col, btn_col = st.columns([3, 1], gap="small")
#             with desc_col:
#                 st.markdown(f"<div class='muted'>{node.get('description','')}</div>", unsafe_allow_html=True)
#                 if node.get("phone"):
#                     st.markdown(f"<div class='phone-link'>📞 <a href='tel:{node['phone']}'>{node['phone']}</a></div>", unsafe_allow_html=True)
#
#                 if st.button("📊 የበተሰብ ብዛት አሳይ", key=f"rep_btn_{key_base}"):
#                     st.session_state[f"show_report_{key_base}"] = not st.session_state.get(f"show_report_{key_base}", False)
#
#                 if st.session_state.get(f"show_report_{key_base}", False):
#                     rep = count_levels(node)
#                     st.markdown(f"""
#                     <div class="report-box" style="margin-top: 5px;">
#                         <div style="font-weight:700;color:#0b6cff;">📊 {disp_name(name)} የቤተሰብ ብዛት</div>
#                         <div class="report-item">ልጆች: <b>{rep['gen2']}</b></div>
#                         <div class="report-item">የልጅ ልጆች: <b>{rep['gen3']}</b></div>
#                         <div class="report-item"> የልጆች የልጅ ልጅ: <b>{rep['gen4']}</b></div>
#                         <div style="font-weight:700;margin-top: 4px;">ጠቅላላ የቤተሰብ ዝርዝር: <b>{rep['total_descendants']}</b></div>
#                     </div>
#                     """, unsafe_allow_html=True)
#
#             with btn_col:
#                 if not locked_root:
#                     if st.button("✏️ አስተካክል", key=f"edit_{key_base}"):
#                         st.session_state[f"edit_mode_{key_base}"] = True
#                     if st.button("❌ ሰርዝ", key=f"del_{key_base}"):
#                         if name in parent_children:
#                             parent_children.pop(name, None)
#                             save_and_rerun()
#
#             # Partner form
#             if st.session_state.get(f"partner_mode_{key_base}", False):
#                 with st.form(f"form_partner_{key_base}"):
#                     pname = st.text_input("የባል/ሚስት ስም", key=f"pn_{key_base}")
#                     if st.form_submit_button("አረጋግጥ"):
#                         if pname.strip():
#                             node["partner"] = pname.strip()
#                             node.setdefault("children", {})
#                             st.session_state.pop(f"partner_mode_{key_base}", None)
#                             save_and_rerun()
#                         else:
#                             st.error("የባል/ሚስት ስም ያስፈልጋል።")
#
#             # Child form
#             if st.session_state.get(f"child_mode_{key_base}", False):
#                 with st.form(f"form_child_{key_base}"):
#                     cname = st.text_input("የልጅ ስም", key=f"cn_{key_base}")
#                     cdesc = st.text_area("መግለጫ", key=f"cd_{key_base}")
#                     cphone = st.text_input("ስልክ", key=f"cp_{key_base}")
#                     cphoto = st.file_uploader("ፎቶ", type=["jpg", "jpeg", "png"], key=f"cph_{key_base}")
#                     if st.form_submit_button("አረጋግጥ"):
#                         if not cname.strip():
#                             st.error("ስም ያስፈልጋል።")
#                         else:
#                             child = {"description": cdesc, "children": {}, "phone": cphone, "photo": "", "fixed_generation": False}
#                             if cphoto:
#                                 child["photo"] = save_uploaded_photo(cphoto, path + [cname])
#                             node.setdefault("children", {})[cname] = child
#                             st.session_state.pop(f"child_mode_{key_base}", None)
#                             save_and_rerun()
#
#             # Edit form
#             if st.session_state.get(f"edit_mode_{key_base}", False) and not locked_root:
#                 with st.form(f"form_edit_{key_base}"):
#                     nname = st.text_input("ስም", value=name, key=f"en_{key_base}")
#                     desc = st.text_area("መግለጫ", value=node.get("description", ""), key=f"ed_{key_base}")
#                     phone = st.text_input("ስልክ", value=node.get("phone", ""), key=f"ep_{key_base}")
#                     if locked:
#                         st.text_input("የባል/ሚስት ስም", value=node.get("partner", ""), disabled=True, key=f"pp_{key_base}")
#                         pval = node.get("partner", "")
#                     else:
#                         pval = st.text_input("የባል/ሚስት ስም", value=node.get("partner", ""), key=f"epv_{key_base}")
#                     photo = st.file_uploader("አዲስ ፎቶ", type=["jpg", "jpeg", "png"], key=f"eph_{key_base}")
#                     save_edit = st.form_submit_button("መዝግብ")
#                     cancel_edit = st.form_submit_button("ይቅር")
#                     if cancel_edit:
#                         st.session_state.pop(f"edit_mode_{key_base}", None)
#                         st.rerun()
#                     if save_edit:
#                         parent = get_parent_container(ancestors)
#                         if nname.strip() and (nname == name or nname not in parent):
#                             node["description"] = desc
#                             node["phone"] = phone
#                             node["partner"] = pval
#                             if photo:
#                                 node["photo"] = save_uploaded_photo(photo, path)
#                             if nname != name:
#                                 parent.pop(name, None)
#                                 parent[nname] = node
#                             st.session_state.pop(f"edit_mode_{key_base}", None)
#                             save_and_rerun()
#                         else:
#                             st.error("የተሳሳተ ወይም የተመዘገባ ስም።")
#
#         # Recursive display
#         for ch, cd in list(node.get("children", {}).items()):
#             display_family(ch, cd, ancestors=path, level=level + 1)
#
#     st.markdown("</div>", unsafe_allow_html=True)
#
# # ---------------- MAIN APP ----------------
# st.markdown('<div class="main">', unsafe_allow_html=True)
#
# # header area with stylish search button on the right (title in Amharic)
# st.markdown(f'''
# <div class="cool-header">
#   <div class="header-title">👨‍👩‍👧 የኢማም ሙሀመድ የቤተሰብ ማዝገብ</div>
#   <div>
#     <form action="/" method="get" style="display:inline;"></form>
#   </div>
# </div>
# ''', unsafe_allow_html=True)
#
# # place the search toggle button to the right using columns (only visible after quiz)
# hcol1, hcol2 = st.columns([6,1])
#
# # ensure the search form is hidden while quiz not done
# if not st.session_state.get("quiz_done", False):
#     st.session_state.show_search = False
#
# with hcol2:
#     if st.session_state.get("quiz_done", False):
#         if st.button("🔎 ፈልግ", key="toggle_search"):
#             st.session_state.show_search = not st.session_state.show_search
#
# # # Reset
# if st.button("🔄 ሁሉንም ሰርዝ", key="reset_all"):
#     save_family_data(copy.deepcopy(default_family_data))
#     st.session_state.clear()
#     st.rerun()
#
# # Quiz gate
# if not st.session_state.quiz_done:
#     q = st.session_state.current_question
#     st.markdown('<div class="section-title">🔐 መግቢያ ጥያቄ</div>', unsafe_allow_html=True)
#     ans = st.text_input(q["question"], key="quiz_answer")
#     if st.button("አስገባ", key="quiz_submit"):
#         if ans.strip().lower() == q["answer"].lower():
#             st.session_state.quiz_done = True
#             st.rerun()
#         else:
#             st.error("የተሳሳተ መልስ ነው! እባክዎ እንደገና ይሞክሩ።")
#     st.stop()
#
# # --- SEARCH UI: only show when show_search True ---
# if st.session_state.show_search:
#     st.markdown('<div class="section-title">🔎 ፈልግ</div>', unsafe_allow_html=True)
#     with st.form("search_form"):
#         search_query = st.text_input("በስም ወይም በመግለጫ ይፈልጉ", value=st.session_state.get('last_search', ''))
#         search_submit = st.form_submit_button("ፈልግ")
#         if search_submit:
#             st.session_state.last_search = search_query
#             st.session_state.search_results = find_nodes_by_name_fuzzy(search_query, threshold=0.45)
#             # hide the form after a search
#             st.session_state.show_search = False
#
# # Display search results (they persist until next search)
# if st.session_state.get('search_results'):
#     st.markdown('<div style="margin-top:8px;margin-bottom:8px;">', unsafe_allow_html=True)
#     display_search_results(st.session_state.search_results)
#     st.markdown('</div>', unsafe_allow_html=True)
#
# # Family Tree
# st.markdown('<div class="section-title">🌳 የቤተሰብ ዝርዝር</div>', unsafe_allow_html=True)
# for mother, md in st.session_state.family_data.items():
#     display_family(mother, md, ancestors=[], level=0)
#
# # ---------------- FAMILY REPORT ----------------
# rep = count_levels(st.session_state.family_data)
# st.markdown(f"""
# <div class="report-box">
#   <div style="font-weight:700; color:#0b6cff; margin-bottom:8px;">📊 የቤተሰብ ጠቅላላ ብዛት</div>
#   <div class="report-item">ሚስቶች: <span style="font-weight:800; color:#111;">{rep["gen1"]}</span></div>
#   <div class="report-item">ልጆች: <span style="font-weight:800; color:#111;">{rep["gen2"]}</span></div>
#   <div class="report-item">የልጅ ልጆች: <span style="font-weight:800; color:#111;">{rep["gen3"]}</span></div>
#   <div class="report-item"> የልጆች የልጅ ልጅ: <span style="font-weight:800; color:#111;">{rep["gen4"]}</span></div>
#   <hr>
#   <div class="report-item">የቤተሰብ ጠቅላላ ብዛት: <span style="font-weight:900; color:#111;">{rep["total_descendants"]}</span></div>
# </div>
# """, unsafe_allow_html=True)
#
# # Save button
# if st.button("💾 ለውጦችን መዝግብ", key="save_changes"):
#     save_family_data(st.session_state.family_data)
#     st.success("ለውጦቹ በትክክል ተቀምጠዋል።")
#
# st.markdown('</div>', unsafe_allow_html=True)
#
# # Button labeling JS (localized labels)
# components.html("""
# <script>
# (function () {
#   const map = {"👫 ያትዳር አጋር ይመዝግቡ": "partner", "➕ ልጅ ያክሉ": "child", "❌ ሰርዝ": "delete", "✏️ አስተካክል": "edit"};
#   function tagButtons() {
#     document.querySelectorAll('button').forEach(btn => {
#       const txt = (btn.innerText || '').trim();
#       if (map[txt]) btn.classList.add(map[txt]);
#     });
#   }
#   setTimeout(tagButtons, 150);
#   const obs = new MutationObserver(() => setTimeout(tagButtons, 50));
#   obs.observe(document.body, { childList: true, subtree: true });
# })();
# </script>
# """, height=0, scrolling=False)

