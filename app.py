import streamlit as st
import json, os, copy, uuid, random

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Delko's Family Data Record", layout="centered")

DATA_FILE = "family_data.json"
PHOTO_DIR = "photos"
os.makedirs(PHOTO_DIR, exist_ok=True)

PLACEHOLDER_IMAGE = "https://via.placeholder.com/150?text=No+Photo"
MOTHERS_WITH_DEFAULT_PARTNER = ["Shemega","Nurseba","Dilbo","Rukiya","Nefissa"]
FIRST_FIXED_CHILDREN = ["Sunkemo","Mustefa","Jemal","Rehmet","Bedriya",
                        "Oumer","Sefiya","Ayro","Reshad",
                        "Sadik","Behra","Beytulah","Leyla","Abdurezak"]

# ---------------- CSS ----------------
st.markdown("""
<style>
.main { background:#fff; border-radius:14px; padding:12px; margin:12px auto; max-width:800px; }
.cool-header { font-size:1.8rem; font-weight:700; text-align:center; color:#007bff; margin-bottom:12px; }
.person-row { display:flex; align-items:center; gap:10px; margin-bottom:6px; flex-wrap:wrap; }
.person-photo img { width:80px; height:80px; border-radius:10px; border:2px solid #007bff; object-fit:cover; }
.person-info { flex:1; display:flex; flex-direction:column; }
.person-actions { display:flex; gap:6px; margin-top:4px; flex-wrap:wrap; }
.stButton>button { border-radius:8px !important; padding:4px 10px; font-size:0.9rem; }
@media(max-width:600px){
  .cool-header { font-size:1.4rem; }
  .person-photo img { width:64px; height:64px; }
  .stButton>button { font-size:0.8rem; padding:4px 8px; }
}
.muted { color:#666; font-size:14px; margin:2px 0; }
</style>
""", unsafe_allow_html=True)

# ---------------- QUIZ ----------------
quiz_questions=[
 {"question":"how many children did sunkemo have?","answer":"9"},
 {"question":"How many wives did Mohammed have?","answer":"5"},
 {"question":"how many children did mother Shemega have?","answer":"5"},
 {"question":"how many children did mother Nurseba have?","answer":"4"},
 {"question":"how many children did mother Dilbo have?","answer":"2"},
]

# ---------------- DEFAULT FAMILY ----------------
default_family_data={
    "Shemega":{"description":"Mother Shemega","phone":"0911000000","partner":"Mohammed","locked_partner":True,"photo":"","children":{
        "Sunkemo":{"description":"Child of Shemega","children":{},"phone":"","photo":"","fixed_generation":True},
        "Jemal":{"description":"Child of Shemega","children":{},"phone":"","photo":"","fixed_generation":True},
        "Mustefa":{"description":"Child of Shemega","children":{},"phone":"","photo":"","fixed_generation":True},
        "Rehmet":{"description":"Child of Shemega","children":{},"phone":"","photo":"","fixed_generation":True},
        "Bedriya":{"description":"Child of Shemega","children":{},"phone":"","photo":"","fixed_generation":True},
    }},
    "Nurseba":{"description":"Mother Nurseba","phone":"0911333444","partner":"Mohammed","locked_partner":True,"photo":"","children":{
        "Oumer":{"description":"Child of Nurseba","children":{},"phone":"","photo":"","fixed_generation":True},
        "Sefiya":{"description":"Child of Nurseba","children":{},"phone":"","photo":"","fixed_generation":True},
        "Ayro":{"description":"Child of Nurseba","children":{},"phone":"","photo":"","fixed_generation":True},
        "Reshad":{"description":"Child of Nurseba","children":{},"phone":"","photo":"","fixed_generation":True},
    }},
    "Dilbo":{"description":"Mother Dilbo","phone":"0911444555","partner":"Mohammed","locked_partner":True,"photo":"","children":{
        "Sadik":{"description":"Child of Dilbo","children":{},"phone":"","photo":"","fixed_generation":True},
        "Behra":{"description":"Child of Dilbo","children":{},"phone":"","photo":"","fixed_generation":True},
    }},
    "Rukiya":{"description":"Mother Rukiya","phone":"0911555666","partner":"Mohammed","locked_partner":True,"photo":"","children":{
        "Beytulah":{"description":"Child of Rukiya","children":{},"phone":"","photo":"","fixed_generation":True},
        "Leyla":{"description":"Child of Rukiya","children":{},"phone":"","photo":"","fixed_generation":True},
    }},
    "Nefissa":{"description":"Mother Nefissa","phone":"0911666777","partner":"Mohammed","locked_partner":True,"photo":"","children":{
        "Abdurezak":{"description":"Child of Nefissa","children":{},"phone":"","photo":"","fixed_generation":True},
    }},
}

# ---------------- HELPER FUNCTIONS ----------------
def load_family_data():
    if os.path.exists(DATA_FILE):
        try: return json.load(open(DATA_FILE,"r",encoding="utf-8"))
        except: return copy.deepcopy(default_family_data)
    return copy.deepcopy(default_family_data)

def save_family_data(data):
    with open(DATA_FILE,"w",encoding="utf-8") as f: json.dump(data,f,indent=2,ensure_ascii=False)

def save_uploaded_photo(file,path):
    if not file: return ""
    name="_".join(path).replace(" ","_")+uuid.uuid4().hex[:5]+os.path.splitext(file.name)[1]
    filepath=os.path.join(PHOTO_DIR,name)
    with open(filepath,"wb") as f: f.write(file.getbuffer())
    return filepath

def save_and_rerun(): save_family_data(st.session_state.family_data); st.experimental_rerun()

def reset_session_state():
    for key in list(st.session_state.keys()): del st.session_state[key]

# ---------------- SESSION STATE ----------------
if "family_data" not in st.session_state: st.session_state.family_data = load_family_data()
if "quiz_done" not in st.session_state: st.session_state.quiz_done = False
if "current_question" not in st.session_state: st.session_state.current_question=random.choice(quiz_questions)

# ---------------- DISPLAY FAMILY ----------------
def display_family(name,data,ancestors=[]):
    path=ancestors+[name]
    key="_".join(path).replace(" ","_")
    partner=data.get("partner","")
    locked=data.get("locked_partner",False)
    fixed=data.get("fixed_generation",False)
    partner_display="Wife of Mohammed" if name in MOTHERS_WITH_DEFAULT_PARTNER else (partner or "Single")
    
    with st.expander(f"{name} ({partner_display})",expanded=False):
        col1,col2=st.columns([1,3])
        with col1:
            st.image(data.get("photo") if data.get("photo") and os.path.exists(data.get("photo")) else PLACEHOLDER_IMAGE,width=80)
        with col2:
            st.markdown(f"**{data.get('description','')}**")
            st.markdown(f"<div class='muted'>{partner_display}</div>",unsafe_allow_html=True)
            if data.get("phone"): st.markdown(f"<div class='muted'>📞 {data['phone']}</div>",unsafe_allow_html=True)
            st.markdown('<div class="person-actions">',unsafe_allow_html=True)
            if st.button(f"Edit {name}",key=f"edit_{key}"): st.session_state[f"edit_{key}"]=True
            if st.button("❌ Delete",key=f"del_{key}"):
                parent=st.session_state.family_data
                for anc in ancestors: parent=parent[anc]["children"]
                parent.pop(name,None); save_and_rerun()
            if name not in FIRST_FIXED_CHILDREN and not partner:
                if st.button("💍 Add Partner",key=f"partner_{key}"): st.session_state[f"partner_{key}"]=True
            if (partner or name in MOTHERS_WITH_DEFAULT_PARTNER) and name not in FIRST_FIXED_CHILDREN:
                if st.button("➕ Add Child",key=f"child_{key}"): st.session_state[f"child_{key}"]=True
            st.markdown('</div>',unsafe_allow_html=True)
            # Forms
            if st.session_state.get(f"partner_{key}",False):
                with st.form(f"form_partner_{key}"):
                    pname=st.text_input("Partner name")
                    if st.form_submit_button("Save Partner"):
                        if pname.strip(): data["partner"]=pname.strip(); st.session_state.pop(f"partner_{key}"); save_and_rerun()
            if st.session_state.get(f"child_{key}",False):
                with st.form(f"form_child_{key}"):
                    cname=st.text_input("Child name")
                    cdesc=st.text_area("Description")
                    cphone=st.text_input("Phone")
                    cphoto=st.file_uploader("Photo",type=["jpg","jpeg","png"])
                    if st.form_submit_button("Save Child"):
                        if cname.strip():
                            child={"description":cdesc,"children":{},"phone":cphone,"photo":""}
                            if cphoto: child["photo"]=save_uploaded_photo(cphoto,path+[cname])
                            data.setdefault("children",{})[cname]=child
                            st.session_state.pop(f"child_{key}"); save_and_rerun()
        # Edit mode
        if st.session_state.get(f"edit_{key}",False):
            with st.form(f"form_edit_{key}"):
                desc=st.text_area("Description",value=data.get("description",""))
                phone=st.text_input("Phone",value=data.get("phone",""))
                partner_val=partner if locked else st.text_input("Partner",value=partner)
                photo=st.file_uploader("New photo",type=["jpg","jpeg","png"])
                if st.form_submit_button("Save"):
                    data["description"]=desc; data["phone"]=phone; data["partner"]=partner_val
                    if photo: data["photo"]=save_uploaded_photo(photo,path)
                    st.session_state.pop(f"edit_{key}"); save_and_rerun()
        # Recurse children
        for ch,cd in list(data.get("children",{}).items()): display_family(ch,cd,path)

# ---------------- MAIN ----------------
st.markdown('<div class="main">', unsafe_allow_html=True)
st.markdown('<div class="cool-header">👨‍👩‍👧 Delko\'s Family Data Record</div>', unsafe_allow_html=True)

if st.button("🔄 Reset All History"):
    reset_session_state()
    save_family_data(copy.deepcopy(default_family_data))
    st.session_state.family_data = load_family_data()
    st.session_state.quiz_done = False
    st.session_state.current_question = random.choice(quiz_questions)
    st.success("All history has been reset!")
    st.experimental_rerun()

if not st.session_state.quiz_done:
    st.markdown('<div class="muted">📖 Please answer Family Quiz to login</div>', unsafe_allow_html=True)
    question = st.session_state.current_question["question"]
    if "quiz_answer" not in st.session_state: st.session_state.quiz_answer=""
    st.text_input(question,key="quiz_answer")
    if st.button("Submit Quiz"):
        ans = (st.session_state.get("quiz_answer") or "").strip().lower()
        if ans == st.session_state.current_question["answer"].lower():
            st.session_state.quiz_done=True
            st.success("✅ Correct!")
            st.experimental_rerun()
        else:
            st.error("❌ Wrong! Try again.")
            st.session_state.current_question=random.choice(quiz_questions)
else:
    st.markdown('<div class="muted">🌳 Family Tree by Mothers</div>', unsafe_allow_html=True)
    for mother_name, mother_data in st.session_state.family_data.items():
        display_family(mother_name,mother_data)
    if st.button("💾 Save Changes"):
        save_family_data(st.session_state.family_data)
        st.success("✅ Data saved successfully")

st.markdown('</div>', unsafe_allow_html=True)
