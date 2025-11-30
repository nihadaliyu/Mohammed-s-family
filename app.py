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
    "Mohammed": "ኢማም ሙሀመድ",
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

# ---------------- GLOBAL STYLES (responsive + mobile-first improvements) ----------------
# Put core app styles here so layout + small-screen behavior improves.
st.markdown("""
<style>
/* Import friendly font */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

:root{
  --accent: #ff6b6b;        /* warm coral accent */
  --accent-2: #0b6cff;     /* blue accent for other elements */
  --card-bg: rgba(255,255,255,0.96);
  --muted: #556;
  --surface: #f6fbff;
}

/* Base body adjustments */
body, .main, .block-container {
  font-family: 'Inter', system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
  color: #0e2533;
}

/* Main card */
.main {
  background: linear-gradient(180deg,#ffffff, #fbfdff);
  border-radius: 12px;
  padding: 14px;
  box-shadow: 0 12px 30px rgba(2,6,23,0.06);
  margin-top: 8px;
}

/* Sticky header inside the main card */
.cool-header {
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:12px;
  padding: 12px 14px;
  border-radius: 10px;
  background: linear-gradient(90deg, rgba(255,255,255,0.6), rgba(240,247,255,0.6));
  box-shadow: 0 4px 12px rgba(2,6,23,0.03);
}
.header-title { font-weight:700; font-size:1.15rem; color: #123a57; }

/* Small helper blocks */
.section-title {
  display:flex;
  align-items:center;
  gap:10px;
  color: #123a57;
  font-weight:700;
  margin-top: 18px;
  padding-left: 8px;
  border-left: 4px solid var(--accent-2);
  font-size: 1.02rem;
}

/* Cards and report boxes */
.report-box, .family-card {
  background: var(--card-bg);
  border-radius: 12px;
  padding: 12px;
  border: 1px solid rgba(11,108,255,0.05);
  box-shadow: 0 8px 20px rgba(17,45,78,0.04);
}

/* Search result */
.search-result { border-radius:10px; padding:8px; margin-bottom:10px; }

/* Image responsiveness */
img, .stImage img {
  max-width:100%;
  height:auto;
  border-radius:8px;
}

/* Buttons: larger targets for touch */
button[data-baseweb="button"], button {
  padding: 10px 14px !important;
  border-radius: 10px !important;
  font-weight:600;
}

/* Bottom admin bar improvements */
.fixed-bottom-bar {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(90deg,#ffffffee,#f0f7ffcc);
  border-top: 1px solid rgba(11,108,255,0.06);
  padding: 10px 8px;
  display:flex;
  justify-content:center;
  z-index:9999;
  box-shadow: 0 -6px 24px rgba(2,6,23,0.06);
}
.fixed-bottom-inner {
  width:100%;
  max-width:980px;
  display:flex;
  gap:8px;
  justify-content:space-between;
  align-items:center;
}

/* Make expanders and internal forms fit */
[data-testid="stExpander"] > div {
  box-shadow: none !important;
}
.stTextInput, .stNumberInput, .stTextArea { width: 100% !important; }

/* Mobile-first: narrow viewport adjustments */
@media (max-width: 880px) {
  .cool-header { padding:10px; gap:8px; }
  .header-title { font-size: 1.05rem; }
  .main { padding: 10px; }
  .fixed-bottom-inner { gap:6px; padding: 6px; }
  .section-title { font-size: 1rem; }
  /* Make sidebar less intrusive on mobile — collapse it visually */
  /* Hide the sidebar column (Streamlit wraps it; using typical class used by Streamlit) */
  .css-1d391kg .css-1v3fvcr { display: none !important; } /* best-effort; streamlit classnames vary */
  /* Ensure main container uses full width */
  .block-container { padding-left: 12px !important; padding-right: 12px !important; max-width: 100% !important; }
}

/* Extra-large screens */
@media (min-width: 1200px){
  .header-title { font-size: 1.35rem; }
}
</style>
""", unsafe_allow_html=True)

# ---------------- QUIZ ----------------
quiz_questions = [
    {"question": "ሱንከሞ ስንት ልጆች አሉት?", "answer": "9"},
    {"question": "ኢማም ሙሀመድ ስንት ሚስቶች ነበሯቸው?", "answer": "5"},
    {"question": "እናት ሸመጌ ስንት ልጆች ነበራት?", "answer": "5"},
    {"question": "እናት ኑርሰቤ ስንት ልጆች አላት?", "answer": "8"},
    {"question": "እናት ዲልቦ ስንት ልጆች ነበራት?", "answer": "4"},
]

# ---------------- DEFAULT DATA (unchanged) ----------------
default_family_data = {
    "Shemege": {
        "description": "እናት ሸመጌ",
        "phone": "አላህ ጀነት-አል ፊርደውስ ይወፍቃት",
        "partner": "Mohammed",
        "locked_partner": True,
        "locked_root": True,
        "photo": "",
        "children": {
            "Sunkemo": {"description": "የ የ ሸመጌ የመጀመሪያ ልጅ", "children": {}, "phone": "0920138830", "photo": "", "fixed_generation": False},
            "Bedriya": {"description": "የ ሸመጌ ሁለተኛ ልጅ", "children": {}, "phone": "0913558013", "photo": "", "fixed_generation": False},
            "Rahmet": {"description": "የ ሸመጌ ሶስተኛ ልጅ", "children": {}, "phone": "0921610321", "photo": "", "fixed_generation": False},
            "Mustefa": {"description": "የ ሸመጌ አራተኛ ልጅ", "children": {}, "phone": "0911626138", "photo": "", "fixed_generation": False},
            "Jemal": {"description": "የ ሸመጌ የመጨረሻ ልጅ", "children": {}, "phone": "0977922700", "photo": "", "fixed_generation": False},
        },
    },
    "Nursebe": {
        "description": "እናት ኑርሰቤ",
        "phone": "0941832034",
        "partner": "Mohammed",
        "locked_partner": True,
        "locked_root": True,
        "photo": "",
        "children": {
            "Sefiya": {"description": "የ ኑርሰቤ የመጀመሪያ ልጅ", "children": {}, "phone": "0910000000", "photo": "", "fixed_generation": False},
            "Oumer": {"description": "የ ኑርሰቤ ሁለተኛ ልጅ", "children": {}, "phone": "0910000001", "photo": "", "fixed_generation": False},
            "Ayro": {"description": "የ ኑርሰቤ ሶስተኛ ልጅ", "children": {}, "phone": "0912854001", "photo": "", "fixed_generation": False},
            "Selima": {"description": "የ ኑርሰቤ አራተኛ ልጅ", "children": {}, "phone": "0963835660", "photo": "", "fixed_generation": False},
            "Reshad": {"description": "የ ኑርሰቤ አምስተኛ ልጅ", "children": {}, "phone": "0911154225", "photo": "", "fixed_generation": False},
            "Fetiya": {"description": "የ ኑርሰቤ ስድስተኛ ልጅ", "children": {}, "phone": "0966046176", "photo": "", "fixed_generation": False},
            "Aliyu": {"description": "የ ኑርሰቤ ሰባተኛ ልጅ", "children": {}, "phone": "0911287428", "photo": "", "fixed_generation": False},
            "Neja": {"description": "የ ኑርሰቤ የመጨረሻ ልጅ", "children": {}, "phone": "0911441196", "photo": "", "fixed_generation": False},
        },
    },
    "Dilbo": {
        "description": "እናት ዲልቦ",
        "phone": "አላህ ጀነት-አል ፊርደውስ ይወፍቃት",
        "partner": "Mohammed",
        "locked_partner": True,
        "locked_root": True,
        "photo": "",
        "children": {
            "Sadik": {"description": "የ የመጀመሪያ ልጅ", "children": {}, "phone": "0953098207", "photo": "", "fixed_generation": False},
            "Bahredin": {"description": "የ ዲልቦ ሁለተኛ ልጅ", "children": {}, "phone": "0913064107", "photo": "", "fixed_generation": False},
            "Nasir": {"description": "የ ዲልቦ ሶስተኛ ልጅ", "children": {}, "phone": "0913956015", "photo": "", "fixed_generation": False},
            "Abdusemed": {"description": "የ ዲልቦ የመጨረሻ ልጅ", "children": {}, "phone": "0912765901", "photo": "", "fixed_generation": False},
        },
    },
    "Rukiya": {
        "description": "እናት ሩቂያ",
        "phone": "0911333444",
        "partner": "Mohammed",
        "locked_partner": True,
        "locked_root": True,
        "photo": "",
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
        "description": "እናት ነፊሳ",
        "phone": "091040404",
        "partner": "Mohammed",
        "locked_partner": True,
        "locked_root": True,
        "photo": "",
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
    if not isinstance(d, dict):
        return copy.deepcopy(default_family_data)
    return d

def save_family_data(data):
    """
    Persist family data to DATA_FILE. Returns True on success, False on failure.
    Performs an atomic write (write to .tmp then replace).
    """
    tmp = DATA_FILE + ".tmp"
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        os.replace(tmp, DATA_FILE)
        return True
    except Exception as e:
        # cleanup and log error for debugging
        try:
            if os.path.exists(tmp):
                os.remove(tmp)
        except Exception:
            pass
        print("Error saving", DATA_FILE, e)
        return False

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

_initial_auth = load_auth_data()
if not _initial_auth:
    new_auth = {}
    for em in ALLOWED_ADMIN_EMAILS:
        default_pw = _localpart_default(em)
        new_auth[em.lower()] = {
            "password_hash": hash_password(default_pw),
            "is_admin": True,
            "must_change": True,
            "default_plain": default_pw
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
with st.sidebar:
    st.markdown("## 📋 መግቢያ")

    menu_choice = st.radio("Navigate to:", ["🏠 መግቢያ", "🔐 አገባብ ይለዩ", "ℹ️ እርዳታ ይጠይቁ", "👨‍👩‍👦 ስለ እኛ ያንብቡ"], index=0)

    if menu_choice == "ℹ️ እርዳታ ይጠይቁ":
        st.info("""
        **የእርዳታ መመሪያ**

በዚህ መተግበሪያ ውስጥ፣ ቤተሰባችን ሁሉ በአንድ ቦታ ተያይዞ መቀመጥ ይችላል። እያንዳንዱ አባል ያለውን መረጃ በቀላሉ [...]

* 👑 **አድሚኖች** የቤተሰብ መረጃ መጨመር፣ ማስተካከል ወይም ማጥፋት ይችላሉ።
* 👨‍👩‍👧‍👦 **እንግዶች** የቤተሰብ መረጃን ማየትና የትዳር አጋር እና የልጆች መረጃ መጨመር ይችላሉ።
* 🔐 እንደ **አድሚን** ለመግባት፣ Login የሚለውን ይጫኑ እና መለያ መረጃዎን ያስገቡ።

👉 @ibn_abas እና @nihad_aliyu
        """)

    elif menu_choice == "👨‍👩‍👦 ስለ እኛ ያንብቡ":
        st.success("""
       **የኢማም መሐመድ የቤተሰብ መረጃ መዝገብ**

ይህ የመረጃ መዝገብ የኢማም መሐመድ ቤተሰብን የትውልድ ትውልድ ታሪክና ዘር በመጠበቅ እና በዘመናዊ መንገድ ለማቅረብ የ[...]
በዚህ መድረክ ላይ የቤተሰቡ አባላት የተለያዩ የዘር ግንኙነቶችን ማየት፣ የታሪክ መረጃ ማካፈል እና በቀላሉ እርስ በእር[...]
ይህ ፕሮጀክት የቤተሰብ መረጃ እንዳይጠፋ እና ለወደፊት ትውልድ እንዲቀጥል በመሰረታዊ መንገድ ተሠርቷል።

በዚህ ስራ ላይ በትልቅ ድጋፍና በመንፈስ እንዲሁም በሃላፊነት ሲያግዘኝ ለነበረው የ አክስቴ ልጅ አቡዱሰላም ታላቅ ክብር[...]


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

                    # If no record exists yet, create one with default password placeholder
                    if not record:
                        record = {
                            "password_hash": None,
                            "default_plain": "imam123",
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
        if not isinstance(child_node, dict):
            return
        if depth == 1:
            counts["gen2"] += 1
        elif depth == 2:
            counts["gen3"] += 1
        elif depth == 3:
            counts["gen4"] += 1
        if depth < 3:
            for sub in child_node.get("children", {}).values():
                dfs(sub, depth+1)
    # Determine if the node is the top-level family_data dict
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
        st.markdown(
            f"<div class='search-result'><b>{name_disp}</b>"
            f"<div style='font-size:0.9rem;color:#555;'>መንገድ: {path_disp} — ውጤት ውህድ: {score:.2f}</div>",
            unsafe_allow_html=True
        )
        st.markdown(f"<div style='margin-top:6px;'>📞 {node.get('phone','-')} &nbsp; | &nbsp; ልጆች: <b>{rep['gen2']}</b> &nbsp; የልጆች ልጆች: <b>{rep['gen3']}</b></div>", unsafe_allow_html=True)
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
            partner_display = f"የ {disp_name('Mohammed')} ሚስት"
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
                st.markdown(f"<div class='family-card'><b style='font-size:1.03rem'>{disp_name(name)}</b><div style='color:#556;margin-top:6px'>{node.get('description','')}</div></div>", unsafe_allow_html=True)
                if node.get("phone"):
                    st.markdown(f"📞 <a href='tel:{node['phone']}' style='color:var(--accent-2);font-weight:600;text-decoration:none'>{node['phone']}</a>", unsafe_allow_html=True)

            with bcol:
                allow_guest_add = True
                is_admin = st.session_state.get("is_admin", False)

                # Add Partner button (shown to guests too)
                if not node.get("locked_partner", False) and not node.get("partner", ""):
                    if is_admin or allow_guest_add:
                        if st.button("➕ ባል/ሚስት መዝግብ", key=f"btn_partner_{key_base}"):
                            st.session_state[f"partner_mode_{key_base}"] = True
                            st.session_state.pop(f"child_mode_{key_base}", None)
                            st.session_state.pop(f"edit_mode_{key_base}", None)

                # Add Child button (skip for default wives)
                if name not in MOTHERS_WITH_DEFAULT_PARTNER and node.get("partner", "") and not node.get("fixed_generation", False):
                    if is_admin or allow_guest_add:
                        if st.button("👶 ልጅ መዝግብ", key=f"btn_child_{key_base}"):
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

                # Report toggle button (visible to guests and admins)
                if is_admin or allow_guest_add:
                    if st.button("📊 ሪፖርት", key=f"report_{key_base}"):
                        cur = st.session_state.get(f"report_mode_{key_base}", False)
                        st.session_state[f"report_mode_{key_base}"] = not cur
                        # session-only toggle; persisting family data isn't necessary, but harmless
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
                            st.success("✅ ባረከላሁ አለይኩማ ወጀማ በነኩማ ፊል ኽይር.")
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

            # Per-node report display (toggleable)
            if st.session_state.get(f"report_mode_{key_base}", False):
                rep_node = count_levels(node)
                st.markdown("<div class='report-box' style='margin-top:8px;'>", unsafe_allow_html=True)
                st.markdown(f"<div style='font-weight:700; color:var(--accent-2); margin-bottom:6px;'>📊 {disp_name(name)} የንዑስ ሪፖርት</div>", unsafe_allow_html=True)
                st.markdown(f"<div style='font-weight:600'>ልጆች: <span style='font-weight:800; color:#111;'>{rep_node['gen2']}</span></div>", unsafe_allow_html=True)
                st.markdown(f"<div style='font-weight:600'>የልጆች ልጆች: <span style='font-weight:800; color:#111;'>{rep_node['gen3']}</span></div>", unsafe_allow_html=True)
                st.markdown(f"<div style='font-weight:600'>የልጅ ልጅ ልጆች: <span style='font-weight:800; color:#111;'>{rep_node['gen4']}</span></div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

        # recurse into children
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

# ---------------- Enhanced Sliding Carousel (already mobile-friendly) ----------------
carousel_html = r"""
<style>
:root{ --accent: #ff6b6b; --muted: #556; --bg: linear-gradient(90deg,#ffffffee,#f0f7ff); }
#family-carousel-container{
  width:100%; max-width:980px; margin: 18px auto; border-radius: 14px;
  background: var(--bg); box-shadow: 0 14px 36px rgba(11,108,255,0.04); position: relative; height: 220px;
}
#family-carousel-viewport{ width:100%; height:100%; overflow:hidden; border-radius:12px; padding:8px; box-sizing:border-box; }
#family-carousel-track{ display:flex; height:100%; transition: transform 1200ms cubic-bezier(.2,.9,.28,1); will-change:transform; }
.family-carousel-slide{ flex:0 0 100%; display:flex; align-items:center; justify-content:center; padding: 10px; box-sizing:border-box; }
.family-carousel-card{ width:100%; max-width:860px; background: linear-gradient(180deg, rgba(255,255,255,0.98), rgba(255,255,255,0.95)); border-radius:12px; padding:16px; box-shadow: 0 10px 30px rgba(17,45,78,0.05); text-align:center; transform: scale(.98); opacity:.94; transition: transform 700ms, opacity 700ms; border-left:6px solid rgba(255,255,255,0); }
.family-carousel-card.active{ transform: scale(1); opacity:1; border-left-color:var(--accent); box-shadow: 0 16px 40px rgba(255,107,107,0.12); }
.family-carousel-title{ font-size:1.25rem; color:var(--accent); font-weight:700; margin-bottom:6px; }
.family-carousel-quote{ font-size:1.02rem; color:#0e2738; line-height:1.45; }
.family-carousel-footer{ margin-top:10px; color:var(--muted); font-size:0.92rem; }

/* controls and dots */
.carousel-arrow{ position:absolute; top:50%; transform:translateY(-50%); background:rgba(255,255,255,0.95); border:none; width:40px;height:40px;border-radius:50%; box-shadow:0 6px 18px rgba(17,45,78,0.08); cursor:pointer; z-index:9; color:#123a57; font-weight:700; }
#carousel-prev{ left:12px; } #carousel-next{ right:12px; }
.family-carousel-dots{ position:absolute; bottom:12px; left:50%; transform:translateX(-50%); display:flex; gap:8px; z-index:9; }
.family-carousel-dot{ width:12px;height:12px;border-radius:50%; background: rgba(11,108,255,0.12); border:none; cursor:pointer; transition:all 260ms; }
.family-carousel-dot.active{ background:var(--accent); transform:scale(1.12); box-shadow: 0 6px 18px rgba(255,107,107,0.18); }

/* reduce motion */
@media (prefers-reduced-motion: reduce){ #family-carousel-track { transition:none !important; } .family-carousel-card { transition:none !important; } }
@media (max-width:760px){ #family-carousel-container{ height:170px; } .family-carousel-title{ font-size:1.05rem; } .family-carousel-quote{ font-size:0.98rem; } }
</style>

<div id="family-carousel-container" role="region" aria-label="Welcome carousel">
  <div id="family-carousel-viewport" tabindex="0">
    <div id="family-carousel-track" aria-live="polite"></div>
  </div>

  <button class="carousel-arrow" id="carousel-prev" aria-label="Previous slide">‹</button>
  <button class="carousel-arrow" id="carousel-next" aria-label="Next slide">›</button>

  <div class="family-carousel-dots" id="family-carousel-dots" role="tablist" aria-hidden="false"></div>
</div>

<script>
(function(){
  const slides = [
    { title: "እንኳን ደህና መጡ", text: "Welcome to Imam Mohammed family hub" },
    { title: "ልምድ አንድ", text: "Family is the compass that guides us." },
    { title: "ልምድ ሁለት", text: "Roots run deep — remember your elders." },
    { title: "ልምድ ሶስት", text: "Share stories — keep memories alive." },
    { title: "አመሰግናለሁ", text: "Thank you — እናመሰግናለን" }
  ];

  const track = document.getElementById('family-carousel-track');
  const dotsContainer = document.getElementById('family-carousel-dots');
  const prevBtn = document.getElementById('carousel-prev');
  const nextBtn = document.getElementById('carousel-next');
  const viewport = document.getElementById('family-carousel-viewport');
  if(!track) return;

  let index = 0;
  const total = slides.length;
  const intervalMs = 10000; // 10s
  let autoplay = true;
  let timer = null;

  slides.forEach((s, i) => {
    const slide = document.createElement('div');
    slide.className = 'family-carousel-slide';
    slide.id = 'slide-' + i;
    slide.innerHTML = '<div class="family-carousel-card"><div class="family-carousel-title">' + s.title + '</div>'
                    + '<div class="family-carousel-quote">' + s.text + '</div>'
                    + '<div class="family-carousel-footer">ይቆዩ — Sit and read</div></div>';
    track.appendChild(slide);

    const dot = document.createElement('button');
    dot.className = 'family-carousel-dot';
    dot.setAttribute('aria-label','Go to slide ' + (i+1));
    dot.onclick = () => { goTo(i, true); };
    dotsContainer.appendChild(dot);
  });

  function setActiveCard(){
    for(let i=0;i<total;i++){
      const card = document.querySelector('#slide-' + i + ' .family-carousel-card');
      if(card) card.classList.toggle('active', i === index);
    }
  }

  function updateDots(){
    const dots = dotsContainer.querySelectorAll('.family-carousel-dot');
    dots.forEach((d, i) => d.classList.toggle('active', i === index));
  }

  function refreshTransform(animate=true){
    track.style.transition = animate ? 'transform 1200ms cubic-bezier(.2,.9,.28,1)' : 'none';
    track.style.transform = 'translateX(' + (-index * 100) + '%)';
    updateDots();
    setActiveCard();
  }

  function next(){ index = (index + 1) % total; refreshTransform(true); }
  function prev(){ index = (index - 1 + total) % total; refreshTransform(true); }
  function goTo(i, userTriggered){
    index = ((i % total) + total) % total;
    refreshTransform(true);
    if(userTriggered) restartTimer();
  }

  function restartTimer(){
    if(timer) clearInterval(timer);
    if(autoplay) timer = setInterval(next, intervalMs);
  }

  prevBtn.addEventListener('click', () => { prev(); restartTimer(); });
  nextBtn.addEventListener('click', () => { next(); restartTimer(); });

  const container = document.getElementById('family-carousel-container');
  container.addEventListener('mouseenter', () => { if(timer) clearInterval(timer); });
  container.addEventListener('mouseleave', () => { restartTimer(); });
  viewport.addEventListener('focus', () => { if(timer) clearInterval(timer); }, true);
  viewport.addEventListener('blur', () => { restartTimer(); }, true);

  viewport.addEventListener('keydown', (e) => {
    if(e.key === 'ArrowLeft'){ prev(); restartTimer(); }
    if(e.key === 'ArrowRight'){ next(); restartTimer(); }
  });

  // swipe support
  let startX=0, deltaX=0, touching=false;
  viewport.addEventListener('touchstart', (e)=>{ touching=true; if(timer) clearInterval(timer); startX = e.touches[0].clientX; track.style.transition='none'; }, {passive:true});
  viewport.addEventListener('touchmove', (e)=>{ if(!touching) return; deltaX = e.touches[0].clientX - startX; const percent = (deltaX / viewport.clientWidth) * 100; track.style.transform = 'translateX(' + ((-index*100) + percent) + '%)'; }, {passive:true});
  viewport.addEventListener('touchend', ()=>{ touching=false; if(Math.abs(deltaX) > (viewport.clientWidth * 0.12)){ if(deltaX>0) prev(); else next(); } else { refreshTransform(true); } deltaX=0; restartTimer(); });

  // init
  refreshTransform(false);
  setActiveCard();
  restartTimer();
})();
</script>
"""
components.html(carousel_html, height=260, scrolling=False)

# ensure the search form is hidden while quiz not done (guests)
if not st.session_state.get("quiz_done", False) and not st.session_state.get("is_admin", False):
    st.session_state.show_search = False

hcol1, hcol2 = st.columns([6, 1])
with hcol2:
    if st.session_state.get("quiz_done", False) or st.session_state.get("is_admin", False):
        if st.button("🔎 ፈልግ", key="toggle_search"):
            st.session_state.show_search = not st.session_state.show_search

# ---------------- ADMIN CONTROLS (moved to bottom) ----------------
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
        search_query = st.text_input(
            "የ እንግሊዘኛ ፊደላትን በመጥቀም በስም ወይም በመግለጫ ይፈልጉ ",
            value=st.session_state.get('last_search', '')
        )
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

# ---------------- FAMILY REPORT (overall) ----------------
rep = count_levels(st.session_state.family_data)
st.markdown(f"""
    <div class="report-box" style="margin-top:12px;">
      <div style="font-weight:700; color:var(--accent-2); margin-bottom:8px;">📊 የቤተሰብ ጠቅላላ ሪፖርት</div>
      <div style="font-weight:600">ሚስቶች: <span style='font-weight:800;'>{rep["gen1"]}</span></div>
      <div style="font-weight:600">ልጆች: <span style='font-weight:800;'>{rep["gen2"]}</span></div>
      <div style="font-weight:600">የልጆች ልጆች: <span style='font-weight:800;'>{rep["gen3"]}</span></div>
      <div style="font-weight:600">የልጅ ልጅ ልጆች: <span style='font-weight:800;'>{rep["gen4"]}</span></div>
      <hr>
      <div style="font-weight:700">ጠቅላላ ብዛት: <span style='font-weight:900;'>{rep["total_descendants"]}</span></div>
    </div>
    """, unsafe_allow_html=True)

# ---------------- PDF GENERATION (Summary + Full Tree, include photos where available) ----------------
def build_tree_lines(data, indent=0, lines=None):
    if lines is None:
        lines = []
    for name, node in data.items():
        prefix = "  " * indent + "- "
        partner = node.get("partner", "")
        partner_disp = f" ({disp_name(partner)})" if partner else ""
        lines.append(f"{prefix}{disp_name(name)}{partner_disp} — {node.get('description','')}")
        if node.get("phone"):
            lines.append("  " * (indent+1) + f"📞 {node.get('phone')}")
        children = node.get("children", {})
        if children:
            build_tree_lines(children, indent+1, lines)
    return lines

def generate_pdf_bytes(family_data):
    """Return bytes of a PDF containing summary report + full family tree and photos where available."""
    buf = BytesIO()
    if not REPORTLAB_AVAILABLE:
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
        max_width = PAGE_WIDTH - 2 * margin
        if pdf_canvas.stringWidth(line, "Helvetica", 10) <= max_width:
            pdf_canvas.drawString(margin, y, line)
            y -= 12
        else:
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
                pdf_canvas.drawString(margin, cur_y - 14, text)
        else:
            pdf_canvas.drawString(margin, cur_y - 14, text)
        return cur_y - max(img_h + 10, 20)

    for mother_name, mother_node in family_data.items():
        y = draw_member_with_photo(mother_name, mother_node, y)
        for child_name, child_node in mother_node.get("children", {}).items():
            if y < margin + 100:
                pdf_canvas.showPage()
                y = PAGE_HEIGHT - margin
            y = draw_member_with_photo(child_name, child_node, y)
            for gc_name, gc_node in child_node.get("children", {}).items():
                if y < margin + 100:
                    pdf_canvas.showPage()
                    y = PAGE_HEIGHT - margin
                y = draw_member_with_photo(gc_name, gc_node, y)
                for ggc_name, ggc_node in gc_node.get("children", {}).items():
                    if y < margin + 100:
                        pdf_canvas.showPage()
                        y = PAGE_HEIGHT - margin
                    y = draw_member_with_photo(ggc_name, ggc_node, y)

    pdf_canvas.save()
    buf.seek(0)
    return buf.getvalue()
    
def admin_bottom_bar():
    """
    Bottom admin bar — only visible to admins.
    Save/Reset/Export visible only when st.session_state['is_admin'] is True.
    """
    is_admin = st.session_state.get("is_admin", False)

    # Only render the pinned bottom bar for admins
    if not is_admin:
        return

    st.markdown('<div class="fixed-bottom-bar"><div class="fixed-bottom-inner">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])

    # Reset (admins only)
    with col1:
        if st.button("🔄 Reset All Data (for recovery)", key="reset_all_bottom"):
            try:
                st.session_state.family_data = copy.deepcopy(default_family_data)
                ok = save_family_data(st.session_state.family_data)
                # also reset auth file
                if os.path.exists(AUTH_FILE):
                    try:
                        os.remove(AUTH_FILE)
                    except Exception as e:
                        st.error(f"Could not remove auth file: {e}")
                if ok:
                    st.success("✅ App reset to defaults and persisted to disk. Signing out...")
                else:
                    st.error("❌ Reset applied in session but failed to persist to disk.")
            except Exception as e:
                st.error(f"Error during reset: {e}")
                print("Reset error:", e)
            # clear admin session and rerun to apply defaults
            st.session_state.is_admin = False
            st.session_state.login_role = None
            st.session_state.email = ""
            st.rerun()

    # Save changes (admins only)
    with col2:
        if st.button("💾 Save Changes", key="save_changes_bottom"):
            try:
                ok = save_family_data(st.session_state.family_data)
                if ok:
                    st.success(f"✅ Changes saved to {DATA_FILE}")
                    # store a last-saved timestamp in session so UI can show it
                    st.session_state["last_saved"] = str(round(random.random(), 6))  # cheap change to session; could be timestamp
                else:
                    st.error("❌ Failed to save changes. Check server logs or file permissions.")
                    print("save_family_data returned False.")
            except Exception as e:
                st.error(f"❌ Exception while saving: {e}")
                print("Exception saving data:", e)

    # Export PDF (admins only)
    with col3:
        if st.button("📤 Export PDF", key="export_pdf_bottom"):
            try:
                pdf_bytes = generate_pdf_bytes(st.session_state.family_data)
                if isinstance(pdf_bytes, (bytes, bytearray)):
                    st.download_button(
                        label="⬇️ Download PDF",
                        data=pdf_bytes,
                        file_name="family_report.pdf",
                        mime="application/pdf"
                    )
                else:
                    # generate_pdf_bytes may return an error message string when reportlab not installed
                    st.error("Could not generate PDF: PDF libs not available on server.")
            except Exception as e:
                st.error(f"Error generating PDF: {e}")
                print("PDF generation error:", e)

    st.markdown('</div></div>', unsafe_allow_html=True)

# render bottom admin bar (pinned)
admin_bottom_bar()

# ---------------- Change-password flow (when admin uses default password) ----------------
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
                auth_data[st.session_state["email"].lower()]["password_hash"] = hash_password(new_pw)
                auth_data[st.session_state["email"].lower()]["must_change"] = False
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
