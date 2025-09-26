import streamlit as st
import json, os, copy, uuid, random

st.set_page_config(page_title="Delko's Family Tree", layout="centered")

DATA_FILE = "family_data.json"
PHOTO_DIR = "photos"
os.makedirs(PHOTO_DIR, exist_ok=True)
PLACEHOLDER_IMAGE = "https://via.placeholder.com/100?text=No+Photo"
MOTHERS_WITH_DEFAULT_PARTNER = ["Shemega","Nurseba","Dilbo","Rukiya","Nefissa"]

# ---------- CSS ----------
st.markdown("""
<style>
:root { --brand:#0b6cff; --bg:#f5f7fb; --card:#fff; --muted:#667085; --border:#e4e7ec; }
html,body { background:var(--bg); }
.main { background:var(--card); border-radius:16px; padding:18px; margin:12px auto; max-width:860px; box-shadow:0 8px 24px rgba(0,0,0,0.06); }
.cool-header { background:linear-gradient(90deg,#0b6cff,#5b9bff); color:#fff; padding:10px 14px; border-radius:12px; font-weight:700; text-align:center; margin-bottom:12px; }
.person-card { background:#fafcff; border:1px solid var(--border); border-radius:12px; padding:10px; margin:6px 0; }
.person-name { font-weight:600; font-size:1rem; }
.muted{ color:var(--muted); font-size:13px; }
.tree-branch { border-left:2px solid #e0e0e0; margin-left:20px; padding-left:12px; }
.button-row{ display:flex; gap:6px; flex-wrap:wrap; margin-top:6px; }
.stButton>button{ border-radius:8px !important; padding:6px 10px; font-size:0.9rem; }
@media(max-width:600px){ .stButton>button{ width:100% !important; } }
</style>
""", unsafe_allow_html=True)

# ---------- Default Data ----------
default_family_data = {
    "Shemega": {
        "description":"Mother Shemega","phone":"0911000000","partner":"Mohammed",
        "locked_partner":True,"locked_root":True,"photo":"",
        "children":{
            "Sunkemo":{"description":"Child of Shemega","children":{},"phone":"","photo":"","fixed_generation":False},
            "Jemal":{"description":"Child of Shemega","children":{},"phone":"","photo":"","fixed_generation":False},
            "Mustefa":{"description":"Child of Shemega","children":{},"phone":"","photo":"","fixed_generation":False},
            "Rehmet":{"description":"Child of Shemega","children":{},"phone":"","photo":"","fixed_generation":False},
            "Bedriya":{"description":"Child of Shemega","children":{},"phone":"","photo":"","fixed_generation":False},
        }
    },
    "Nurseba": {"description":"Mother Nurseba","phone":"0911333444","partner":"Mohammed","locked_partner":True,"locked_root":True,"photo":"","children":{}},
    "Dilbo":   {"description":"Mother Dilbo","phone":"0911444555","partner":"Mohammed","locked_partner":True,"locked_root":True,"photo":"","children":{}},
    "Rukiya":  {"description":"Mother Rukiya","phone":"0911555666","partner":"Mohammed","locked_partner":True,"locked_root":True,"photo":"","children":{}},
    "Nefissa": {"description":"Mother Nefissa","phone":"0911666777","partner":"Mohammed","locked_partner":True,"locked_root":True,"photo":"","children":{}},
}

# ---------- Load/Save ----------
def load_family_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE,"r",encoding="utf-8") as f: return json.load(f)
        except: return copy.deepcopy(default_family_data)
    return copy.deepcopy(default_family_data)

def save_family_data(data):
    with open(DATA_FILE,"w",encoding="utf-8") as f: json.dump(data,f,indent=4,ensure_ascii=False)

def save_and_rerun():
    save_family_data(st.session_state.family_data); st.rerun()

def save_uploaded_photo(uploaded_file,path_list):
    if not uploaded_file: return ""
    safe_base="_".join(path_list).replace(" ","_")
    _,ext=os.path.splitext(uploaded_file.name)
    fname=f"{safe_base}_{uuid.uuid4().hex[:6]}{ext or '.jpg'}"
    filepath=os.path.join(PHOTO_DIR,fname)
    with open(filepath,"wb") as f: f.write(uploaded_file.getbuffer())
    return filepath

# ---------- Init ----------
if "family_data" not in st.session_state: st.session_state.family_data=load_family_data()

# ---------- Helpers ----------
def get_node(path):
    node=st.session_state.family_data
    for p in path: node=node["children"][p] if "children" in node and p in node["children"] else node[p]
    return node

# ---------- Display ----------
def display_family(name,data,ancestors=None,level=0):
    if ancestors is None: ancestors=[]
    path=ancestors+[name]; key_base="_".join(path).replace(" ","_")
    node=get_node(path)
    partner=node.get("partner",""); locked_root=node.get("locked_root",False)
    partner_display="Wife of Mohammed" if name in MOTHERS_WITH_DEFAULT_PARTNER else (partner or "Single")

    # Person card
    indent_class="tree-branch" if level>0 else ""
    st.markdown(f"<div class='{indent_class}'><div class='person-card'>",unsafe_allow_html=True)
    col1,col2=st.columns([1,4])
    with col1:
        img=node.get("photo",""); show_img=img if (img and os.path.exists(img)) else PLACEHOLDER_IMAGE
        st.image(show_img,width=70)
    with col2:
        st.markdown(f"<div class='person-name'>{name}</div>",unsafe_allow_html=True)
        st.markdown(f"<span class='muted'>{partner_display}</span>",unsafe_allow_html=True)
        if node.get("phone"): st.markdown(f"📞 {node['phone']}")
        st.markdown(f"<div class='muted'>{node.get('description','')}</div>",unsafe_allow_html=True)

    # Action buttons
    if not locked_root:
        st.markdown('<div class="button-row">',unsafe_allow_html=True)
        if not partner:
            if st.button("💍 Add partner",key=f"btn_partner_{key_base}"): st.session_state[f"partner_mode_{key_base}"]=True
        else:
            if st.button("➕ Add child",key=f"btn_child_{key_base}"): st.session_state[f"child_mode_{key_base}"]=True
        st.markdown('</div>',unsafe_allow_html=True)

    # Partner form
    if st.session_state.get(f"partner_mode_{key_base}",False):
        with st.form(f"form_partner_{key_base}"):
            pname=st.text_input("Partner name",key=f"pn_{key_base}")
            if st.form_submit_button("Save partner"):
                node["partner"]=pname.strip(); node.setdefault("children",{})
                st.session_state.pop(f"partner_mode_{key_base}",None); save_and_rerun()

    # Child form
    if st.session_state.get(f"child_mode_{key_base}",False):
        with st.form(f"form_child_{key_base}"):
            cname=st.text_input("Child name",key=f"cn_{key_base}")
            if st.form_submit_button("Save child"):
                node.setdefault("children",{})[cname]={"description":"","children":{},"phone":"","photo":""}
                st.session_state.pop(f"child_mode_{key_base}",None); save_and_rerun()

    st.markdown("</div></div>",unsafe_allow_html=True)

    # Recurse children
    for ch,cd in node.get("children",{}).items():
        display_family(ch,cd,ancestors=path,level=level+1)

# ---------- MAIN ----------
st.markdown('<div class="main">',unsafe_allow_html=True)
st.markdown('<div class="cool-header">🌳 Delko\'s Family Tree</div>',unsafe_allow_html=True)

if st.button("🔄 Reset All Data"): save_family_data(copy.deepcopy(default_family_data)); st.session_state.clear(); st.rerun()

st.markdown("### Family Tree")
for mother,md in st.session_state.family_data.items():
    display_family(mother,md)

if st.button("💾 Save Changes"): save
