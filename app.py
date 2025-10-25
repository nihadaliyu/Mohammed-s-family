# app.py
import streamlit as st
import streamlit.components.v1 as components
import json
import os
import copy
import uuid
import random
import difflib
import hashlib
from io import BytesIO

# PDF libs
try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.utils import ImageReader
    from PIL import Image
    REPORTLAB_AVAILABLE = True
except Exception:
    REPORTLAB_AVAILABLE = False

# ---------------- VISIBLE NAME MAPPING (only display text changed) ----------------
DISPLAY_NAME = {
    "Mohammed": "ሙሀመድ",
    "Shemege": "ሸመጌ",
    "Nursebe": "ኑርሰቤ",
    "Dilbo": "ዲልቦ",
    "Rukiya": "ሩቂያ",
    "Nefissa": "ነፊሳ",
    "Sunkemo": "ሱንከሞ",
    "Bedriya": "በድሪያ",
    "Rahmet": "ራሕመት",
    "Mustefa": "ሙስጠፋ",
    "Jemal": "ጀማል",
    "Oumer": "ኡመር",
    "Sefiya": "ሰፊያ",
    "Ayro": "አይሮ",
    "Selima": "ሰሊማ",
    "Reshad": "ረሻድ",
    "Fetiya": "ፈቲያ",
    "Aliyu": "አልዩ",
    "Neja": "ነጃ",
    "Sadik": "ሳዲቅ",
    "Bahredin": "ባሕረዲን",
    "Nasir": "ናሲር",
    "Abdusemed": "አብዱሰመድ",
    "Beytulah": "ቤይቱላህ",
    "Leyla": "ለይላ",
    "Zulfa": "ዙልፋ",
    "Ishak": "ኢስሃቅ",
    "Mubarek": "ሙባሪክ",
    "Hayat": "ሃያት",
    "Abdurezak": "አብዱረዛቅ"
}
def disp_name(key):
    return DISPLAY_NAME.get(key, key)

# ---------------- CONFIG & FILES ----------------
st.set_page_config(page_title="የኢማም ሙሀመድ የቤተሰብ ማዕከል", layout="centered")

DATA_FILE = "family_data.json"
AUTH_FILE = "admin_auth.json"
PHOTO_DIR = "photos"
os.makedirs(PHOTO_DIR, exist_ok=True)
PLACEHOLDER_IMAGE = "https://via.placeholder.com/150?text=No+Photo"

# ---------------- STYLES ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
body { font-family: 'Poppins', sans-serif; background: linear-gradient(to bottom right, #f5f7fa, #c3cfe2); padding-bottom: 120px; }
.main { background: rgba(255, 255, 255, 0.95); border-radius: 10px; padding: 1rem; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
.cool-header { display:flex; align-items:center; justify-content:space-between; gap:12px; text-align: left; font-size: 1.5rem; color: #3f72af; background-color: #dbe2ef; padding: 0.5rem 0.8rem; border-radius: 10px; margin-bottom: 1rem; }
.header-title { font-weight:600; }
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

/* Bottom admin bar */
.fixed-bottom-bar {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(90deg,#ffffffee,#f2f8ff);
  border-top: 1px solid #e6eefc;
  padding: 10px 12px;
  display:flex;
  justify-content:center;
  z-index:9999;
  box-shadow: 0 -2px 8px rgba(0,0,0,0.06);
}
.fixed-bottom-inner {
  width:100%;
  max-width:960px;
  display:flex;
  gap:8px;
  justify-content:space-between;
  align-items:center;
}
.btn-bottom {
  flex:1;
  margin:0 6px;
  padding:10px 8px;
  border-radius:10px;
  text-align:center;
  cursor:pointer;
}
@media (max-width:600px){
  .fixed-bottom-inner { gap:6px; padding:0 6px; }
  .btn-bottom { padding:8px 6px; font-size:0.92rem; }
}

/* Centered card for change-password */
.change-card {
  max-width:480px;
  margin-left:auto;
  margin-right:auto;
  background: #fff;
  padding: 16px;
  border-radius: 10px;
  box-shadow: 0 6px 20px rgba(17,45,78,0.08);
  border: 1px solid #e6eefc;
}
</style>
""", unsafe_allow_html=True)

# ---------------- QUIZ ----------------
quiz_questions = [
    {"question": "ሱንከሞ ስንት ልጆች አሉት?", "answer": "9"},
    {"question": "ሙሀመድ ስንት ሚስቶች ነበሩት?", "answer": "5"},
    {"question": "እናት ሸመጌ ስንት ልጆች ነበራት?", "answer": "5"},
    {"question": "እናት ኑርሰቤ ስንት ልጆች ነበሩ?", "answer": "9"},
    {"question": "እናት ዲልቦ ስንት ልጆች ነበሩ?", "answer": "4"},
]

# ---------------- DEFAULT DATA ----------------
default_family_data = {
    "Shemege": {
        "description": "እናት ሸመጌ", "phone": "አላህ ጀነት-አል ፊርደውስ ይወፍቃት", "partner": "Mohammed",
        "locked_partner": True, "locked_root": True, "photo": "",
        "children": {
            "Sunkemo": {"description": "የ የ ሸመጌ የመጀመሪያ ልጅ", "children": {}, "phone": "0920138830", "photo": "", "fixed_generation": False},
            "Bedriya": {"description": "የ ሸመጌ ሁለተኛ ልጅ", "children": {}, "phone": "0913558013", "photo": "", "fixed_generation": False},
            "Rahmet": {"description": "የ ሸመጌ ሶስተኛ ልጅ", "children": {}, "phone": "0921610321", "photo": "", "fixed_generation": False},
            "Mustefa": {"description": "የ ሸመጌ አራተኛ ልጅ", "children": {}, "phone": "0911626138", "photo": "", "fixed_generation": False},
            "Jemal": {"description": "የ ሸመጌ የመጨረሻ ልጅ", "children": {}, "phone": "0977922700", "photo": "", "fixed_generation": False},
        },
    },
    "Nursebe": {
        "description": "እናት ኑርሰቤ", "phone": "0941832034", "partner": "Mohammed",
        "locked_partner": True, "locked_root": True, "photo": "",
        "children": {
            "Sefiya": {"description": "የ ኑርሰቤ የመጀመሪያ ልጅ", "children": {}, "phone": "አላህ ጀነት-አል ፊርደውስ ይወፍቃት", "photo": "", "fixed_generation": False},
            "Oumer": {"description": "የ ኑርሰቤ ሁለተኛ ልጅ", "children": {}, "phone": "አላህ ጀነት-አል ፊርደውስ ይወፍቀው", "photo": "", "fixed_generation": False},
            "Ayro": {"description": "የ ኑርሰቤ ሶስተኛ ልጅ", "children": {}, "phone": "0912854001", "photo": "", "fixed_generation": False},
            "Selima": {"description": "የ ኑርሰቤ አራተኛ ልጅ", "children": {}, "phone": "0963835660", "photo": "", "fixed_generation": False},
            "Reshad": {"description": "የ ኑርሰቤ አምስተኛ ልጅ", "children": {}, "phone": "0911154225", "photo": "", "fixed_generation": False},
            "Fetiya": {"description": "የ ኑርሰቤ ስድስተኛ ልጅ", "children": {}, "phone": "0966046176", "photo": "", "fixed_generation": False},
            "Aliyu": {"description": "የ ኑርሰቤ ሰባተኛ ልጅ", "children": {}, "phone": "0911287428", "photo": "", "fixed_generation": False},
            "Neja": {"description": "የ ኑርሰቤ የመጨረሻ ልጅ", "children": {}, "phone": "0911441196", "photo": "", "fixed_generation": False},
        },
    },
    "Dilbo": {
        "description": "እናት ዲልቦ", "phone": "አላህ ጀነት-አል ፊርደውስ ይወፍቃት", "partner": "Mohammed",
        "locked_partner": True, "locked_root": True, "photo": "",
        "children": {
            "Sadik": {"description": "የ የመጀመሪያ ልጅ", "children": {}, "phone": "0953098207", "photo": "", "fixed_generation": False},
            "Bahredin": {"description": "የ ዲልቦ ሁለተኛ ልጅ", "children": {}, "phone": "0913064107", "photo": "", "fixed_generation": False},
            "Nasir": {"description": "የ ዲልቦ ሶስተኛ ልጅ", "children": {}, "phone": "0913956015", "photo": "", "fixed_generation": False},
            "Abdusemed": {"description": "የ ዲልቦ የመጨረሻ ልጅ", "children": {}, "phone": "0912765901", "photo": "", "fixed_generation": False},
        },
    },
    "Rukiya": {
        "description": "እናት ሩቂያ", "phone": "0911333444", "partner": "Mohammed",
        "locked_partner": True, "locked_root": True, "photo": "",
        "children": {
            "Beytulah": {"description": "የ ሩቂያ አንደኛ ልጅ", "children": {}, "phone": "0919062619", "photo": "", "fixed_generation": False},
            "Leyla": {"description": "የ ሩቂያ ሁለተኛ ልጅ", "children": {}, "phone": "0939145817", "photo": "", "fixed_generation": False},
            "Zulfa": {"description": "የ ሩቂያ ሶስተኛ ልጅ", "children": {}, "phone": "0937100577", "photo": "", "fixed_generation": False},
            "Ishak": {"description": "የ ሩቂያ አራትኛ ልጅ", "children": {}, "phone": "0927983682", "photo": "", "fixed_generation": False},
            "Mubarek": {"description": "የ ሩቂያ አምስተኛ ልጅ", "children": {}, "phone": "0923547118", "photo": "", "fixed_generation": False},
            "Hayat": {"description": "የ ሩቂያ የመጨረሻ ልጅ", "children": {}, "phone": "0988088017", "photo": "", "fixed_generation": False},
        },
    },
    "Nefissa": {
        "description": "እናት ነፊሳ", "phone": "0911333444", "partner": "Mohammed",
        "locked_partner": True, "locked_root": True, "photo": "",
        "children": {
            "Abdurezak": {"description": "የ ነፊሳ የመጀመሪያ ልጅ", "children": {}, "phone": "0912868786", "photo": "", "fixed_generation": False},
        },
    }
}
MOTHERS_WITH_DEFAULT_PARTNER = ["Shemege", "Nursebe", "Dilbo", "Rukiya", "Nefissa"]
# ---------------- UTILS: atomic save/load ----------------
def load_json_file(path, fallback=None):
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print("Error reading", path, e)
    return copy.deepcopy(fallback) if fallback is not None else {}

def atomic_save_json(path, data):
    tmp = path + ".tmp"
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        os.replace(tmp, path)
    except Exception as e:
        print("Error saving", path, e)

def load_family_data():
    d = load_json_file(DATA_FILE, fallback=default_family_data)
    # ensure correct structure fallback
    if not isinstance(d, dict):
        return copy.deepcopy(default_family_data)
    return d

def save_family_data(data):
    atomic_save_json(DATA_FILE, data)

# ---------------- AUTH (hashed passwords) ----------------
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def check_password(stored_hash: str, entered_password: str) -> bool:
    if not stored_hash:
        return False
    return stored_hash == hash_password(entered_password)

def load_auth_data():
    d = load_json_file(AUTH_FILE, fallback={})
    if not isinstance(d, dict):
        return {}
    return d

def save_auth_data(d):
    if not isinstance(d, dict):
        return
    atomic_save_json(AUTH_FILE, d)

# ---------------- SESSION STATE ----------------
if "family_data" not in st.session_state:
    st.session_state.family_data = load_family_data()
if "quiz_done" not in st.session_state:
    st.session_state.quiz_done = False
if "current_question" not in st.session_state:
    st.session_state.current_question = random.choice(quiz_questions)
if "show_search" not in st.session_state:
    st.session_state.show_search = False
if "last_search" not in st.session_state:
    st.session_state.last_search = ""
if "search_results" not in st.session_state:
    st.session_state.search_results = []
if "reveal_path" not in st.session_state:
    st.session_state.reveal_path = None

# Auth state
if "login_role" not in st.session_state:
    st.session_state.login_role = None  # None / "Guest" / "Admin"
if "email" not in st.session_state:
    st.session_state.email = ""
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False
if "auth_data" not in st.session_state:
    st.session_state.auth_data = load_auth_data()
if "tried_local_email_detect" not in st.session_state:
    st.session_state.tried_local_email_detect = False

# Allowed admin emails (from you)
ALLOWED_ADMIN_EMAILS = {"abdilselamabas@gmail.com", "nihadaliyu@gmail.com"}

# ---------------- Initialize auth_data with unique default passwords if empty ----------------
def _localpart_default(email):
    local = email.split("@")[0] if "@" in email else email
    return f"{local}123"

# If no auth data, create defaults for allowed admin emails
_initial_auth = load_auth_data()
if not _initial_auth:
    new_auth = {}
    for em in ALLOWED_ADMIN_EMAILS:
        default_pw = _localpart_default(em)
        new_auth[em.lower()] = {
            "password_hash": hash_password(default_pw),
            "is_admin": True,
            "must_change": True,
            "default_plain": default_pw  # kept briefly for convenience (not required); won't be displayed
        }
    save_auth_data(new_auth)
    st.session_state.auth_data = new_auth
else:
    st.session_state.auth_data = _initial_auth

# ---------------- SMART LOCAL DETECTION using query param (one-shot) ----------------
qp = st.query_params
detected_email = None
if "detected_email" in qp:
    val = qp.get("detected_email")
    if isinstance(val, list) and val:
        detected_email = val[0].strip()
    elif isinstance(val, str):
        detected_email = val.strip()
    # clear query params to avoid re-trigger
    try:
        st.query_params.clear()
    except Exception:
        try:
            st.query_params = {}
        except Exception:
            pass
if detected_email:
    st.session_state.email = detected_email
    if detected_email.lower() in {e.lower() for e in ALLOWED_ADMIN_EMAILS}:
        st.session_state.is_admin = True
        st.session_state.login_role = "Admin"
        st.session_state.quiz_done = True

# ---------------- SIDEBAR: role selection and login ----------------
# ------------------- SIDEBAR + LOGIN SYSTEM -------------------

# Sidebar menu (click ☰ to open)
with st.sidebar:
    st.markdown("## 📋 መግቢያ")

    menu_choice = st.radio("Navigate to:", ["🏠 መግቢያ", "🔐 አገባብ ይለዩ", "ℹ️ እርዳታ ይጠይቁ", "👨‍👩‍👦 ስለ እኛ ያንብቡ"], index=0)

    if menu_choice == "ℹ️ እርዳታ ይጠይቁ":
        st.info("""
        **የእርዳታ መመሪያ**

በዚህ መተግበሪያ ውስጥ፣ ቤተሰባችን ሁሉ በአንድ ቦታ ተያይዞ መቀመጥ ይችላል። እያንዳንዱ አባል ያለውን መረጃ በቀላሉ ማየትና ማካፈል ይችላል።

* 👑 **አድሚኖች** የቤተሰብ መረጃ መጨመር፣ ማስተካከል ወይም ማጥፋት ይችላሉ። ቤተሰቡን በተደራጀ መንገድ ለማስተዳደር እነርሱ ዋና ኃላፊዎች ናቸው።
* 👨‍👩‍👧‍👦 **እንግዶች** የቤተሰብ መረጃን ማየትና የትዳር አጋር እና የልጆች መረጃ መጨመር ይችላሉ።
* 🔐 እንደ **አድሚን** ለመግባት፣ *Login* የሚለውን ይንኩ እና መለያ መረጃዎን ያስገቡ።

መተግበሪያውን ሲጠቀሙ ምንም አይነት ችግር ካገጠሞት አልያም አስተያያት ካሎት ከታች ባለው መስፈንጠሪያ አድሚኖችን ያነጋግሩ፦
👉 [@ibn_abas](https://t.me/ibn_abas) እና [@nihad_aliyu](https://t.me/nihad_aliyu)
 """)

    elif menu_choice == "👨‍👩‍👦 ስለ እኛ ያንብቡ":
        st.success("""
        **የኢማም መሐመድ የቤተሰብ መረጃ መዝገብ**

ይህ የመረጃ መዝገብ የኢማም መሐመድ ቤተሰብን የትውልድ ትውልድ ታሪክና ዘር በመጠበቅ እና በዘመናዊ መንገድ ለማቅረብ የተቋቋመ ነው።
በዚህ መድረክ ላይ የቤተሰቡ አባላት የተለያዩ የዘር ግንኙነቶችን ማየት፣ የታሪክ መረጃ ማካፈል እና በቀላሉ እርስ በእርሳቸው መገናኘት ይችላሉ።
ይህ ፕሮጀክት የቤተሰብ መረጃ እንዳይጠፋ እና ለወደፊት ትውልድ እንዲቀጥል በመሰረታዊ መንገድ ተሠርቷል።

በዚህ ስራ ላይ በትልቅ ድጋፍና በመንፈስ እንዲሁም በሃላፊነት ሲያግዘኝ ለነበረው የ አክስቴ ልጅ አቡዱሰላም ታላቅ ክብር እና ምስጋና ማቅረብ እውዳለው። የቤተሰቡን ሥራ በተዋህዶ መንፈስ የሚያበረታታ የእርሱን ድጋፍ እንከብራለን።

💬 ስለ ቤተሰቡ ወቅታዊ መረጃ ለማግኘት እባክዎን በዚህ የተለግራም ሊንክ ያግኙን፦ [@imam_mohammed_delko](https://t.me/imam_mohammed_delko)
 """)

# -------------- LOGIN PANEL (Enhanced with Default Password + Change Flow) --------------
if menu_choice == "🔐 አገባብ ይለዩ":
    st.markdown("### 🔐 የአገባብ መምረጫ")

    # Already logged in (Admin or Guest)
    if st.session_state.get("is_admin", False) and st.session_state.get("email"):
        st.success(f"✅ Logged in as Admin: {st.session_state.get('email', '')}")
        if st.button("🚪 Logout"):
            for key in ["is_admin", "login_role", "email", "must_change_password"]:
                st.session_state.pop(key, None)
            st.success("Logged out successfully.")
            st.rerun()
    elif st.session_state.get("login_role") == "Guest":
        st.info("🟢 እንደ ቤተሰብ አባል ገብተዋል")
        if st.button("🚪 Logout"):
            for key in ["is_admin", "login_role", "email", "must_change_password"]:
                st.session_state.pop(key, None)
            st.success("logged out succesfully.")
            st.rerun()
    else:
        st.write("እባኮትን መግብያ ይምረጡ:")
        role = st.radio("አንዱን በመምረጥ ይቀጥሉ:", ["Guest", "Admin"], horizontal=True)

        if role == "Guest":
            if st.button("እንደ ቤተሰብ አባል ይቀጥሉ"):
                st.session_state.login_role = "Guest"
                st.session_state.is_admin = False
                st.session_state.email = ""
                st.success("እንደ እንግዳ ገብተዋል.")
                st.rerun()

        elif role == "Admin":
            st.markdown("#### Admin Login")

            # Load auth data (email, hashed passwords, defaults)
            auth_data = st.session_state.get("auth_data", {})
            email = st.text_input("📧 Email Address")
            password = st.text_input("🔑 Password", type="password")

            if st.button("Login"):
                allowed_emails = {e.lower() for e in ALLOWED_ADMIN_EMAILS}
                if not email:
                    st.warning("Please enter your email.")
                elif email.lower() not in allowed_emails:
                    st.error("This email is not authorized for admin access.")
                else:
                    record = auth_data.get(email.lower())

                    # If no record exists yet, create one with default password
                    if not record:
                        record = {
                            "password_hash": None,
                            "default_plain": "imam123",  # Default password
                            "must_change": False
                        }
                        auth_data[email.lower()] = record
                        save_auth_data(auth_data)

                    # Check login credentials
                    stored_hash = record.get("password_hash")
                    default_plain = record.get("default_plain")
                    must_change = record.get("must_change", False)

                    # Case 1: login with default password
                    if default_plain and password == default_plain:
                        record["must_change"] = True
                        save_auth_data(auth_data)
                        st.session_state.email = email.lower()
                        st.session_state.is_admin = True
                        st.session_state.login_role = "Admin"
                        st.session_state.must_change_password = True
                        st.session_state.auth_data = auth_data
                        st.success("Logged in with default password. Please change it below.")
                        st.rerun()

                    # Case 2: login with saved hash
                    elif stored_hash and check_password(stored_hash, password):
                        st.session_state.email = email.lower()
                        st.session_state.is_admin = True
                        st.session_state.login_role = "Admin"
                        st.session_state.must_change_password = must_change
                        st.session_state.auth_data = auth_data
                        st.success(f"Welcome back, {email}!")
                        st.rerun()
                    else:
                        st.error("Invalid password.")


# Sidebar role badges
if st.session_state.get("is_admin", False):
    st.sidebar.success(f"Signed in as Admin: {st.session_state.get('email','')}")
elif st.session_state.get("login_role") == "Guest":
    st.sidebar.info("Signed in as Guest () — quiz required")
else:
    st.sidebar.info("Please choose role")

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
    if not a or not b:
        return 0.0
    return difflib.SequenceMatcher(None, a, b).ratio()

def find_nodes_by_name_fuzzy(query, max_results=50, threshold=0.45):
    q = (query or "").strip().lower()
    results = []
    if not q:
        return results
    def _dfs(node, path):
        if not isinstance(node, dict):
            return
        name = path[-1]
        desc = node.get("description", "")
        score_name = fuzzy_score(q, name.lower())
        score_desc = fuzzy_score(q, desc.lower())
        contains = int(q in name.lower() or q in desc.lower())
        partial_token = 0
        for tok in name.lower().split():
            if tok.startswith(q) or q.startswith(tok):
                partial_token = 0.75
                break
        combined = max(score_name, score_desc, contains * 0.9, partial_token)
        if combined >= threshold:
            results.append((combined, path.copy(), node))
        for child_name, child_node in node.get("children", {}).items():
            _dfs(child_node, path + [child_name])
    for root_name, root_node in st.session_state.family_data.items():
        _dfs(root_node, [root_name])
    results.sort(key=lambda x: x[0], reverse=True)
    return results[:max_results]

def display_search_results(results):
    if not results:
        st.info("ምንም ውጤት አልተገኘም።")
        return
    st.write(f"የተገኙ {len(results)} ውጤቶች:")
    for i, (score, path, node) in enumerate(results):
        path_disp = " → ".join(disp_name(p) for p in path)
        name_disp = disp_name(path[-1])
        rep = count_levels(node)
        st.markdown(f"<div class='search-result'><b>{name_disp}</b> <div style='font-size:0.9rem;color:#555;'>መንገድ: {path_disp} — ውጤት ውህድ: {score:.2f}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='margin-top:6px;'>📞 {node.get('phone','-')} &nbsp; | &nbsp; ልጆች: <b>{rep['gen2']}</b> &nbsp; የልጆች ልጆች: <b>{rep['gen3']}</b> &nbsp; ታላቅ የልጆች ልጆች: <b>{rep['gen4']}</b></div>", unsafe_allow_html=True)
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("በዝርር አሳይ", key=f"show_in_tree_{i}_{'_'.join(path)}"):
                st.session_state.reveal_path = path
                save_family_data(st.session_state.family_data)
                st.rerun()
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
    """Display node with inline add buttons; guest-safe; no add-child for default wives."""
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

    # Determine partner display
    if partner_live and str(partner_live).strip():
        if str(partner_live).strip().lower() == "mohammed":
            partner_display = f"{disp_name('Mohammed')} ሚስት"
        else:
            partner_display = disp_name(partner_live)
    else:
        partner_display = "ያላገባ/ያላገባች"

    indent_px = level * 10
    reveal = st.session_state.get("reveal_path")
    should_expand = False
    if reveal and isinstance(reveal, list) and len(reveal) >= 1:
        if path == reveal[:len(path)]:
            should_expand = True
            if path == reveal:
                st.session_state.pop("reveal_path", None)

    st.markdown(f"<div style='margin-left:{indent_px}px; margin-bottom:8px;'>", unsafe_allow_html=True)
    with st.expander(f"👤 {disp_name(name)} — {partner_display}", expanded=should_expand):
        col1, col2 = st.columns([1, 5], gap="small")
        with col1:
            img = node.get("photo", "")
            show_img = img if (img and os.path.exists(img)) else PLACEHOLDER_IMAGE
            st.image(show_img, width=100)

        with col2:
            # Inline row: name/desc on left, action buttons on right
            ncol, bcol = st.columns([3, 2])
            with ncol:
                st.markdown(f"**{disp_name(name)}**", unsafe_allow_html=True)
                if node.get("description"):
                    st.markdown(f"<div class='muted'>{node['description']}</div>", unsafe_allow_html=True)
                if node.get("phone"):
                    st.markdown(f"📞 <a href='tel:{node['phone']}'>{node['phone']}</a>", unsafe_allow_html=True)

            with bcol:
                allow_guest_add = True
                is_admin = st.session_state.get("is_admin", False)

                # Add Partner button (shown to guests too)
                if not node.get("locked_partner", False) and not node.get("partner", ""):
                    if is_admin or allow_guest_add:
                        if st.button("➕ ባል/ሚስት", key=f"btn_partner_{key_base}"):
                            st.session_state[f"partner_mode_{key_base}"] = True
                            st.session_state.pop(f"child_mode_{key_base}", None)
                            st.session_state.pop(f"edit_mode_{key_base}", None)

                # Add Child button (skip for default wives)
                if name not in MOTHERS_WITH_DEFAULT_PARTNER and node.get("partner", "") and not node.get("fixed_generation", False):
                    if is_admin or allow_guest_add:
                        if st.button("👶 ልጅ", key=f"btn_child_{key_base}"):
                            st.session_state[f"child_mode_{key_base}"] = True
                            st.session_state.pop(f"partner_mode_{key_base}", None)
                            st.session_state.pop(f"edit_mode_{key_base}", None)

                # Admin-only buttons (edit/delete)
                if is_admin and not locked_root:
                    if st.button("✏️ አስተካክል", key=f"edit_{key_base}"):
                        st.session_state[f"edit_mode_{key_base}"] = True
                    if st.button("❌ ሰርዝ", key=f"del_{key_base}"):
                        if name in parent_children:
                            parent_children.pop(name, None)
                            save_family_data(st.session_state.family_data)
                            st.rerun()

            # Partner form
            if st.session_state.get(f"partner_mode_{key_base}", False):
                with st.form(f"form_partner_{key_base}"):
                    pname = st.text_input("የባል/ሚስት ስም", key=f"pn_{key_base}")
                    if st.form_submit_button("አስቀምጥ"):
                        if pname.strip():
                            node["partner"] = pname.strip()
                            node.setdefault("children", {})
                            st.session_state.pop(f"partner_mode_{key_base}", None)
                            save_family_data(st.session_state.family_data)
                            st.success("✅ Partner added.")
                            st.rerun()
                        else:
                            st.error("የባል/ሚስት ስም ያስፈልጋል።")

            # Child form
            if st.session_state.get(f"child_mode_{key_base}", False):
                with st.form(f"form_child_{key_base}"):
                    cname = st.text_input("የልጅ ስም", key=f"cn_{key_base}")
                    cdesc = st.text_area("መግለጫ", key=f"cd_{key_base}")
                    cphone = st.text_input("ስልክ", key=f"cp_{key_base}")
                    cphoto = st.file_uploader("ፎቶ", type=["jpg", "jpeg", "png"], key=f"cph_{key_base}")
                    if st.form_submit_button("አስቀምጥ"):
                        if not cname.strip():
                            st.error("ስም ያስፈልጋል።")
                        else:
                            child = {"description": cdesc, "children": {}, "phone": cphone, "photo": "", "fixed_generation": False}
                            if cphoto:
                                safe_base = "_".join(path + [cname]).replace(" ", "_")
                                _, ext = os.path.splitext(cphoto.name)
                                fname = f"{safe_base}_{uuid.uuid4().hex[:6]}{ext or '.jpg'}"
                                filepath = os.path.join(PHOTO_DIR, fname)
                                with open(filepath, "wb") as f:
                                    f.write(cphoto.getbuffer())
                                child["photo"] = filepath
                            node.setdefault("children", {})[cname] = child
                            st.session_state.pop(f"child_mode_{key_base}", None)
                            save_family_data(st.session_state.family_data)
                            st.success(f"✅ {cname} added under {disp_name(name)}.")
                            st.rerun()

            # Edit form (admin-only)
            if st.session_state.get(f"edit_mode_{key_base}", False) and not locked_root and is_admin:
                with st.form(f"form_edit_{key_base}"):
                    nname = st.text_input("ስም", value=name)
                    desc = st.text_area("መግለጫ", value=node.get("description", ""))
                    phone = st.text_input("ስልክ", value=node.get("phone", ""))
                    if locked:
                        st.text_input("የባል/ሚስት", value=node.get("partner", ""), disabled=True)
                        pval = node.get("partner", "")
                    else:
                        pval = st.text_input("የባል/ሚስት", value=node.get("partner", ""))
                    photo = st.file_uploader("አዲስ ፎቶ", type=["jpg", "jpeg", "png"])
                    if st.form_submit_button("አስቀምጥ"):
                        parent = get_parent_container(ancestors)
                        if nname.strip() and (nname == name or nname not in parent):
                            node.update({"description": desc, "phone": phone, "partner": pval})
                            if photo:
                                safe_base = "_".join(path).replace(" ", "_")
                                _, ext = os.path.splitext(photo.name)
                                fname = f"{safe_base}_{uuid.uuid4().hex[:6]}{ext or '.jpg'}"
                                filepath = os.path.join(PHOTO_DIR, fname)
                                with open(filepath, "wb") as f:
                                    f.write(photo.getbuffer())
                                node["photo"] = filepath
                            if nname != name:
                                parent.pop(name, None)
                                parent[nname] = node
                            st.session_state.pop(f"edit_mode_{key_base}", None)
                            save_family_data(st.session_state.family_data)
                            st.rerun()

        for ch, cd in list(node.get("children", {}).items()):
            display_family(ch, cd, ancestors=path, level=level + 1)

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- MAIN APP ----------------
st.markdown('<div class="main">', unsafe_allow_html=True)

# header area with stylish search button on the right (title in Amharic)
st.markdown(f'''
    <div class="cool-header">
      <div class="header-title">👨‍👩‍👧 የኢማም ሙሀመድ የቤተሰብ ማዕከል</div>
      <div></div>
    </div>
    ''', unsafe_allow_html=True)

# ensure the search form is hidden while quiz not done (guests)
if not st.session_state.get("quiz_done", False) and not st.session_state.get("is_admin", False):
    st.session_state.show_search = False

hcol1, hcol2 = st.columns([6, 1])
with hcol2:
    if st.session_state.get("quiz_done", False) or st.session_state.get("is_admin", False):
        if st.button("🔎 ፈልግ", key="toggle_search"):
            st.session_state.show_search = not st.session_state.show_search

# ---------------- ADMIN CONTROLS (moved to bottom) ----------------
# We removed the earlier duplicate export sections and instead add a pinned bottom bar
# which renders at the bottom of the page (admin-only controls appear there).

# Quiz gate (admin bypasses)
if not st.session_state.get("is_admin", False):
    if not st.session_state.quiz_done:
        q = st.session_state.current_question
        st.markdown('<div class="section-title">🔐 የቤተሰብ ሙከራ</div>', unsafe_allow_html=True)
        ans = st.text_input(q["question"], key="quiz_answer")
        if st.button("አስገባ", key="quiz_submit"):
            if ans.strip().lower() == q["answer"].lower():
                st.session_state.quiz_done = True
                st.rerun()
            else:
                st.error("የተሳሳተ ነው! እባክዎ እንደገና ይሞክሩ።")
        st.stop()
else:
    st.session_state.quiz_done = True

# --- SEARCH UI: only show when show_search True ---
if st.session_state.show_search:
    st.markdown('<div class="section-title">🔎 ፈልግ</div>', unsafe_allow_html=True)
    with st.form("search_form"):
        search_query = st.text_input("የ እንግሊዘኛ ፊደላትን በመጥቀም በስም ወይም በመግለጫ ይፈልጉ ",
                                     value=st.session_state.get('last_search', ''))
        search_submit = st.form_submit_button("ፈልግ")
        if search_submit:
            st.session_state.last_search = search_query
            st.session_state.search_results = find_nodes_by_name_fuzzy(search_query, threshold=0.45)
            st.session_state.show_search = False

# Display search results (they persist until next search)
if st.session_state.get('search_results'):
    st.markdown('<div style="margin-top:8px;margin-bottom:8px;">', unsafe_allow_html=True)
    display_search_results(st.session_state.search_results)
    st.markdown('</div>', unsafe_allow_html=True)

# Family Tree
st.markdown('<div class="section-title">🌳 የቤተሰብ ዝርዝር</div>', unsafe_allow_html=True)
for mother, md in st.session_state.family_data.items():
    display_family(mother, md, ancestors=[], level=0)

# ---------------- FAMILY REPORT ----------------
rep = count_levels(st.session_state.family_data)
st.markdown(f"""
    <div class="report-box">
      <div style="font-weight:700; color:#0b6cff; margin-bottom:8px;">📊 የቤተሰብ ጠቅላላ ሪፖርት</div>
      <div class="report-item">ሚስቶች: <span style="font-weight:800; color:#111;">{rep["gen1"]}</span></div>
      <div class="report-item">ልጆች: <span style="font-weight:800; color:#111;">{rep["gen2"]}</span></div>
      <div class="report-item">የልጆች ልጆች: <span style="font-weight:800; color:#111;">{rep["gen3"]}</span></div>
      <div class="report-item">የልጅ ልጅ ልጆች: <span style="font-weight:800; color:#111;">{rep["gen4"]}</span></div>
      <hr>
      <div class="report-item">ጠቅላላ ብዛት: <span style="font-weight:900; color:#111;">{rep["total_descendants"]}</span></div>
    </div>
    """, unsafe_allow_html=True)

# ---------------- PDF GENERATION (Summary + Full Tree, include photos where available) ----------------
def build_tree_lines(data, indent=0, lines=None, parent_name=None):
    if lines is None:
        lines = []
    for name, node in data.items():
        prefix = "  " * indent + ("- " if indent >=0 else "")
        partner = node.get("partner", "")
        partner_disp = f" ({disp_name(partner)})" if partner else ""
        lines.append(f"{prefix}{disp_name(name)}{partner_disp} — {node.get('description','')}")
        # include phone if available
        if node.get("phone"):
            lines.append("  " * (indent+1) + f"📞 {node.get('phone')}")
        # process children
        children = node.get("children", {})
        if children:
            build_tree_lines(children, indent+1, lines, parent_name=name)
    return lines

def generate_pdf_bytes(family_data):
    """Return bytes of a PDF containing summary report + full family tree and photos where available."""
    buf = BytesIO()
    if not REPORTLAB_AVAILABLE:
        # fallback: simple text-based PDF via plain BytesIO (not ideal)
        buf.write("PDF generation libs not available on server.\n".encode("utf-8"))
        return buf.getvalue()

    PAGE_WIDTH, PAGE_HEIGHT = A4
    pdf_canvas = canvas.Canvas(buf, pagesize=A4)
    margin = 40
    y = PAGE_HEIGHT - margin

    # Title
    pdf_canvas.setFont("Helvetica-Bold", 16)
    pdf_canvas.drawString(margin, y, "የጠቅላላ ቤተሰብ ብዛት - Imam Mohammed Family Report")
    y -= 28

    # Summary
    pdf_canvas.setFont("Helvetica-Bold", 12)
    pdf_canvas.drawString(margin, y, "📊 ጠቅላላ ብዛት ")
    y -= 18
    pdf_canvas.setFont("Helvetica", 11)
    counts = count_levels(family_data)
    summary_items = [
        ("ሚስቶች (Mothers)", counts["gen1"]),
        ("ልጆች (Children)", counts["gen2"]),
        ("የልጆች ልጆች (Grandchildren)", counts["gen3"]),
        ("ታላቅ የልጆች ልጆች (Great-grandchildren)", counts["gen4"]),
        ("ጠቅላላ የወረዱ ልጆች (Total descendants)", counts["total_descendants"]),
    ]
    for label, value in summary_items:
        pdf_canvas.drawString(margin, y, f"{label}: {value}")
        y -= 14
        if y < margin + 120:
            pdf_canvas.showPage()
            y = PAGE_HEIGHT - margin
            pdf_canvas.setFont("Helvetica", 11)

    # Horizontal rule
    y -= 6
    pdf_canvas.line(margin, y, PAGE_WIDTH - margin, y)
    y -= 18

    # Full family tree (text)
    pdf_canvas.setFont("Helvetica-Bold", 12)
    pdf_canvas.drawString(margin, y, "🌳 Full Family Tree")
    y -= 18
    pdf_canvas.setFont("Helvetica", 10)

    lines = build_tree_lines(family_data)
    for line in lines:
        # Wrap long lines
        max_width = PAGE_WIDTH - 2 * margin
        # simple wrap
        if pdf_canvas.stringWidth(line, "Helvetica", 10) <= max_width:
            pdf_canvas.drawString(margin, y, line)
            y -= 12
        else:
            # naive wrap by words
            words = line.split()
            cur = ""
            for w in words:
                test = cur + " " + w if cur else w
                if pdf_canvas.stringWidth(test, "Helvetica", 10) <= max_width:
                    cur = test
                else:
                    pdf_canvas.drawString(margin, y, cur)
                    y -= 12
                    cur = w
            if cur:
                pdf_canvas.drawString(margin, y, cur)
                y -= 12
        if y < margin + 80:
            pdf_canvas.showPage()
            y = PAGE_HEIGHT - margin
            pdf_canvas.setFont("Helvetica", 10)

    # Add a new page for photos + compact tree with images
    pdf_canvas.showPage()
    y = PAGE_HEIGHT - margin
    pdf_canvas.setFont("Helvetica-Bold", 12)
    pdf_canvas.drawString(margin, y, "📸 Photos (where available) — members")
    y -= 18
    pdf_canvas.setFont("Helvetica", 10)

    def draw_member_with_photo(name, node, cur_y):
        # draw image (if available) and text beside it
        img_path = node.get("photo", "")
        text = f"{disp_name(name)} — {node.get('description','')} ({node.get('phone','-')})"
        img_w = 70
        img_h = 70
        if img_path and os.path.exists(img_path):
            try:
                im = Image.open(img_path)
                im.thumbnail((img_w, img_h))
                ir = ImageReader(im)
                pdf_canvas.drawImage(ir, margin, cur_y - img_h, width=img_w, height=img_h)
                pdf_canvas.drawString(margin + img_w + 8, cur_y - 14, text)
            except Exception:
                # if image loading fails, just draw text
                pdf_canvas.drawString(margin, cur_y - 14, text)
        else:
            pdf_canvas.drawString(margin, cur_y - 14, text)
        return cur_y - max(img_h + 10, 20)

    # traverse tree and draw photos with spacing
    for mother_name, mother_node in family_data.items():
        y = draw_member_with_photo(mother_name, mother_node, y)
        # children
        for child_name, child_node in mother_node.get("children", {}).items():
            if y < margin + 100:
                pdf_canvas.showPage()
                y = PAGE_HEIGHT - margin
            y = draw_member_with_photo(child_name, child_node, y)
            # grandchildren
            for gc_name, gc_node in child_node.get("children", {}).items():
                if y < margin + 100:
                    pdf_canvas.showPage()
                    y = PAGE_HEIGHT - margin
                y = draw_member_with_photo(gc_name, gc_node, y)
                # Great-grandchildren
                for ggc_name, ggc_node in gc_node.get("children", {}).items():
                    if y < margin + 100:
                        pdf_canvas.showPage()
                        y = PAGE_HEIGHT - margin
                    y = draw_member_with_photo(ggc_name, ggc_node, y)

    pdf_canvas.save()
    buf.seek(0)
    return buf.getvalue()

# ---------------- MAIN: Admin bottom bar rendering and actions ----------------
def admin_bottom_bar():
    # Only render for admins
    if not st.session_state.get("is_admin", False):
        return None

    # Buttons via columns inside a container; CSS will pin the wrapper to bottom
    st.markdown('<div class="fixed-bottom-bar"><div class="fixed-bottom-inner">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        if st.button("🔄 ሁሉንም አጥፋ", key="reset_all_bottom"):
            admin_email = st.session_state.get("email", "")
            st.session_state.family_data = copy.deepcopy(default_family_data)
            save_family_data(st.session_state.family_data)
            st.session_state.email = admin_email
            st.success("ለውጦቹ ወደ መጀመሪያው ተመልሶዋል ")
            st.rerun()
    with col2:
        if st.button("💾 ሁሉንም መዝግብ", key="save_changes_bottom"):
            save_family_data(st.session_state.family_data)
            st.success("ለውጦቹ በትክክል ተመዝግቦዋል።")
            st.rerun()
    with col3:
        # Generate PDF bytes on demand and provide download button
        pdf_bytes = None
        pdf_ready = False
        if st.button("📤 export pdf", key="export_pdf_bottom"):
            try:
                pdf_bytes = generate_pdf_bytes(st.session_state.family_data)
                pdf_ready = True
            except Exception as e:
                st.error(f"PDF generation failed: {e}")
                pdf_ready = False
        # If pdf_bytes ready, show download
        if pdf_ready and pdf_bytes:
            st.download_button(
                label="⬇️ download pdf",
                data=pdf_bytes,
                file_name="family_report.pdf",
                mime="application/pdf",
                key=f"download_pdf_{uuid.uuid4().hex}"
            )
    st.markdown('</div></div>', unsafe_allow_html=True)

# render bottom admin bar (pinned)
admin_bottom_bar()

# ---------------- Change-password flow (when admin uses default password) ----------------
# This is shown in main area when admin logged in and must change password
if st.session_state.get("is_admin", False) and st.session_state.get("email"):
    auth_data = st.session_state.get("auth_data", {})
    rec = auth_data.get(st.session_state["email"].lower())
    if rec and rec.get("must_change", False):
        st.markdown("<div class='section-title'>🔐 Change Your Password</div>", unsafe_allow_html=True)
        st.markdown("<div class='change-card'>", unsafe_allow_html=True)
        st.markdown(f"<p>👋 Hello <b>{st.session_state['email']}</b>. You are using a default password — please pick a new password now.</p>", unsafe_allow_html=True)
        new_pw = st.text_input("New password", type="password", key="new_password")
        confirm_pw = st.text_input("Confirm new password", type="password", key="confirm_password")
        if st.button("Update password", key="update_pwd_btn"):
            if not new_pw:
                st.error("Please enter a new password.")
            elif new_pw != confirm_pw:
                st.error("Passwords do not match.")
            else:
                # update persisted auth data
                auth_data[st.session_state["email"].lower()]["password_hash"] = hash_password(new_pw)
                auth_data[st.session_state["email"].lower()]["must_change"] = False
                # remove plain default if present
                if "default_plain" in auth_data[st.session_state["email"].lower()]:
                    auth_data[st.session_state["email"].lower()].pop("default_plain", None)
                save_auth_data(auth_data)
                st.session_state.auth_data = auth_data
                st.success("Password changed successfully. Please log out and log in with your new password.")
                st.session_state.is_admin = False
                st.session_state.login_role = None
                st.session_state.email = ""
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# Button labeling JS (keeps original enhancement)
components.html("""
    <script>
    (function () {
      const map = {"👫 ባል / ሚስት ይመዝግቡ": "partner", "➕ ልጅ ይመዝግቡ": "child", "❌ ሰርዝ": "delete", "✏️ አስተካክል": "edit"};
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
