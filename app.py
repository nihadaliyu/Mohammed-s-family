# app.py - Mobile-optimized final version
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

# ---------------- CSS ----------------
st.markdown(
    """
    <style>
        body { font-family: 'Segoe UI', sans-serif; background:#f1f3f6; margin:0; padding:0; }
        .main { background:#fff; border-radius:16px; box-shadow:0 4px 12px rgba(0,0,0,0.08);
                padding:18px 14px; margin:14px auto; max-width:800px; }
        .cool-header { font-size:1.8rem; color:#007bff; font-weight:700; text-align:center; margin-bottom:16px; }
        .section-title { font-size:1.1rem; font-weight:600; margin:10px 0; color:#222; }
        .card img { width:90px; height:90px; border-radius:10px; border:2px solid #007bff; object-fit:cover; }
        .muted { color:#555; font-size:14px; margin:2px 0; }
        .button-row { display:flex; gap:8px; flex-wrap:wrap; margin-top:8px; }
        .stButton>button { border-radius:8px !important; padding:6px 12px; font-size:0.9rem; width:auto !important; }
        @media (max-width:600px){
            .main { padding:14px 10px; margin:8px; }
            .cool-header { font-size:1.4rem; }
            .card img { width:72px; height:72px; }
            .stButton>button { font-size:0.85rem; padding:6px 10px; }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------- QUIZ ----------------
quiz_questions = [
    {"question": "how many children did sunkemo have?", "answer": "9"},
    {"question": "How many wives did Mohammed have?", "answer": "5"},
    {"question": "how many children did mother Shemega have?", "answer": "5"},
    {"question": "how many children did mother Nurseba have?", "answer": "4"},
    {"question": "how many children did mother Dilbo have?", "answer": "2"},
]

# ---------------- DEFAULT DATA ----------------
default_family_data = {
    "Shemega": {
        "description": "Mother Shemega",
        "phone": "0911000000",
        "partner": "Mohammed",
        "locked_partner": True,
        "photo": "",
        "children": {
            "Sunkemo": {"description":"Child of Shemega + Mohammed","children":{},"phone":"0911222333","photo":"","fixed_generation":True},
            "Jemal":   {"description":"Child of Shemega + Mohammed","children":{},"phone":"0911222334","photo":"","fixed_generation":True},
            "Mustefa": {"description":"Child of Shemega + Mohammed","children":{},"phone":"0911222337","photo":"","fixed_generation":True},
            "Rehmet":  {"description":"Child of Shemega + Mohammed","children":{},"phone":"0911222335","photo":"","fixed_generation":True},
            "Bedriya": {"description":"Child of Shemega + Mohammed","children":{},"phone":"0911222336","photo":"","fixed_generation":True},
        },
    },
    "Nurseba": {
        "description": "Mother Nurseba",
        "phone": "0911333444",
        "partner": "Mohammed","locked_partner":True,"photo":"",
        "children": {
            "Oumer": {"description":"Child of Nurseba + Mohammed","children":{},"phone":"0911222337","photo":"","fixed_generation":True},
            "Sefiya":{"description":"Child of Nurseba + Mohammed","children":{},"phone":"0911222338","photo":"","fixed_generation":True},
            "Ayro":  {"description":"Child of Nurseba + Mohammed","children":{},"phone":"0911222339","photo":"","fixed_generation":True},
            "Reshad":{"description":"Child of Nurseba + Mohammed","children":{},"phone":"0911222340","photo":"","fixed_generation":True},
        },
    },
    "Dilbo": {
        "description": "Mother Dilbo",
        "phone": "0911444555",
        "partner": "Mohammed","locked_partner":True,"photo":"",
        "children": {
            "Sadik":{"description":"Child of Dilbo + Mohammed","children":{},"phone":"0911222341","photo":"","fixed_generation":True},
            "Behra":{"description":"Child of Dilbo + Mohammed","children":{},"phone":"0911222342","photo":"","fixed_generation":True},
        },
    },
    "Rukiya": {
        "description": "Mother Rukiya",
        "phone": "0911555666",
        "partner": "Mohammed","locked_partner":True,"photo":"",
        "children": {
            "Beytulah":{"description":"Child of Rukiya + Mohammed","children":{},"phone":"0911222343","photo":"","fixed_generation":True},
            "Leyla":  {"description":"Child of Rukiya + Mohammed","children":{},"phone":"0911222344","photo":"","fixed_generation":True},
        },
    },
    "Nefissa": {
        "description": "Mother Nefissa",
        "phone": "0911666777",
        "partner": "Mohammed","locked_partner":True,"photo":"",
        "children": {
            "Abdurezak":{"description":"Child of Nefissa + Mohammed","children":{},"phone":"0911222345","photo":"","fixed_generation":True},
        },
    },
}

# ---------------- Load/Save ----------------
def load_family_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE,"r",encoding="utf-8") as f:
                return json.load(f)
        except: return copy.deepcopy(default_family_data)
    return copy.deepcopy(default_family_data)

def save_family_data(data):
    with open(DATA_FILE,"w",encoding="utf-8") as f:
        json.dump(data,f,indent=4,ensure_ascii=False)

def save_and_rerun():
    save_family_data(st.session_state.family_data)
    st.experimental_rerun()

def save_uploaded_photo(uploaded_file, path_list):
    if not uploaded_file: return ""
    safe_base = "_".join(path_list).replace(" ","_")
    _,ext=os.path.splitext(uploaded_file.name)
    fname=f"{safe_base}_{uuid.uuid4().hex[:6]}{ext or '.jpg'}"
    filepath=os.path.join(PHOTO_DIR,fname)
    with open(filepath,"wb") as f: f.write(uploaded_file.getbuffer())
    return filepath

# ---------------- Init ----------------
if "family_data" not in st.session_state:
    st.session_state.family_data = load_family_data()
if "quiz_done" not in st.session_state:
    st.session_state.quiz_done=False
if "current_question" not in st.session_state:
    st.session_state.current_question=random.choice(quiz_questions)

def get_parent_container(ancestors):
    if not ancestors: return st.session_state.family_data
    node=st.session_state.family_data.get(ancestors[0])
    for anc in ancestors[1:]:
        node=node.get("children",{}).get(anc)
    return node.setdefault("children",{})

# ---------------- Display ----------------
def display_family(name,data,ancestors=None):
    if ancestors is None: ancestors=[]
    path=ancestors+[name]
    key_base="_".join(path).replace(" ","_")

    partner=data.get("partner","")
    locked=data.get("locked_partner",False)
    fixed=data.get("fixed_generation",False)
    partner_display="Wife of Mohammed" if name in MOTHERS_WITH_DEFAULT_PARTNER else (partner or "Single")

    with st.expander(f"{name} ({partner_display})",expanded=False):
        col1,col2=st.columns([1,3])
        with col1:
            img=data.get("photo","")
            st.image(img if img and os.path.exists(img) else PLACEHOLDER_IMAGE,width=100)
        with col2:
            # Name with inline buttons
            c1,c2=st.columns([3,2])
            with c1: st.markdown(f"### {name}")
            with c2:
                if st.button(f"Edit {name}",key=f"edit_{key_base}"):
                    st.session_state[f"edit_mode_{key_base}"]=True
                if st.button("❌ Delete",key=f"del_{key_base}"):
                    parent=get_parent_container(ancestors)
                    parent.pop(name,None)
                    save_and_rerun()
            st.markdown(f"<div class='muted'>{partner_display}</div>",unsafe_allow_html=True)
            st.markdown(f"<div class='muted'>{data.get('description','')}</div>",unsafe_allow_html=True)
            if data.get("phone"): st.markdown(f"📞 {data['phone']}",unsafe_allow_html=True)

            # --- Partner / Child buttons ---
            st.markdown('<div class="button-row">',unsafe_allow_html=True)
            # Add Partner (if not default wives, no partner yet)
            if (not partner) and (name not in MOTHERS_WITH_DEFAULT_PARTNER) and not locked:
                if st.button("💍 Add Partner",key=f"btn_partner_{key_base}"):
                    st.session_state[f"partner_mode_{key_base}"]=True
            # Add Child (only if partner exists and not fixed_generation)
            if ((partner or name in MOTHERS_WITH_DEFAULT_PARTNER) and not fixed):
                if st.button("➕ Add Child",key=f"btn_child_{key_base}"):
                    st.session_state[f"child_mode_{key_base}"]=True
            st.markdown('</div>',unsafe_allow_html=True)

            # Inline forms
            if st.session_state.get(f"partner_mode_{key_base}",False):
                with st.form(f"form_partner_{key_base}"):
                    pname=st.text_input("Partner name",key=f"pn_{key_base}")
                    if st.form_submit_button("Save Partner"):
                        if pname.strip():
                            data["partner"]=pname.strip()
                            data.setdefault("children",{})
                            st.session_state.pop(f"partner_mode_{key_base}",None)
                            save_and_rerun()
                        else: st.error("Enter partner name.")
            if st.session_state.get(f"child_mode_{key_base}",False):
                with st.form(f"form_child_{key_base}"):
                    cname=st.text_input("Child name")
                    cdesc=st.text_area("Description")
                    cphone=st.text_input("Phone")
                    cphoto=st.file_uploader("Photo",type=["jpg","jpeg","png"])
                    if st.form_submit_button("Save Child"):
                        if not cname.strip(): st.error("Name required")
                        else:
                            child={"description":cdesc,"children":{},"phone":cphone,"photo":""}
                            if cphoto: child["photo"]=save_uploaded_photo(cphoto,path+[cname])
                            data.setdefault("children",{})[cname]=child
                            st.session_state.pop(f"child_mode_{key_base}",None)
                            save_and_rerun()

        # Edit mode
        if st.session_state.get(f"edit_mode_{key_base}",False):
            with st.form(f"form_edit_{key_base}"):
                nname=st.text_input("Name",value=name)
                desc=st.text_area("Description",value=data.get("description",""))
                phone=st.text_input("Phone",value=data.get("phone",""))
                if locked: 
                    st.text_input("Partner",value=partner,disabled=True)
                    pval=partner
                else: pval=st.text_input("Partner",value=partner)
                photo=st.file_uploader("New photo",type=["jpg","jpeg","png"])
                if st.form_submit_button("Save"):
                    parent=get_parent_container(ancestors)
                    if nname.strip() and (nname==name or nname not in parent):
                        data["description"]=desc; data["phone"]=phone; data["partner"]=pval
                        if photo: data["photo"]=save_uploaded_photo(photo,path)
                        if nname!=name:
                            parent.pop(name); parent[nname]=data
                        save_and_rerun()
                    else: st.error("Invalid or duplicate name")

        # Children
        for ch,cd in list(data.get("children",{}).items()):
            display_family(ch,cd,ancestors=path)

# ---------------- MAIN ----------------
st.markdown('<div class="main">',unsafe_allow_html=True)
st.markdown('<div class="cool-header">👨‍👩‍👧 Delko\'s Family Data Record</div>',unsafe_allow_html=True)

if st.button("🔄 Reset All Data"): 
    save_family_data(copy.deepcopy(default_family_data)); st.session_state.clear(); st.experimental_rerun()

if not st.session_state.quiz_done:
    q=st.session_state.current_question
    st.markdown('<div class="section-title">🔐 Family Quiz</div>',unsafe_allow_html=True)
    ans=st.text_input(q["question"])
    if st.button("Submit"):
        if ans.strip().lower()==q["answer"].lower():
            st.session_state.quiz_done=True; st.experimental_rerun()
        else: st.error("Wrong! Try again.")
else:
    st.markdown('<div class="section-title">🌳 Family Tree</div>',unsafe_allow_html=True)
    for mother,md in st.session_state.family_data.items():
        display_family(mother,md)
    if st.button("💾 Save Changes"): save_family_data(st.session_state.family_data)
st.markdown('</div>',unsafe_allow_html=True)
