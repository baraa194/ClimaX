

import os
from pathlib import Path
import base64
import mimetypes
import streamlit as st

st.set_page_config(page_title="ClimaX Landing", layout="wide", initial_sidebar_state="collapsed")

ROOT = Path(__file__).resolve().parent
ASSETS_DIR = ROOT / ".streamlit" / "assets"

LOCAL_IMAGE_NAMES = [
    "pexels-mssoymac-15250518.jpg",
    "pexels-mssoymac-15250518.jpeg",
    "background.jpg",
    "bg.jpg",
    "weather-bg.jpg",
]
LOCAL_LOGO_NAMES = ["nasa-1.svg", "logo.svg", "nasa.svg"]


USER_GITHUB_BLOB = "https://github.com/baraa194/video-logo-/blob/main/pexels-mssoymac-15250518.jpg"
GITHUB_RAW_FALLBACK = USER_GITHUB_BLOB.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")

def find_local_asset(candidates):
    for name in candidates:
        p = ASSETS_DIR / name
        if p.exists():
            return p
    return None

def make_data_uri(path: Path):
    b = path.read_bytes()
    mime, _ = mimetypes.guess_type(str(path))
    if not mime:
        mime = "application/octet-stream"
    b64 = base64.b64encode(b).decode("ascii")
    return f"data:{mime};base64,{b64}"

local_image_file = find_local_asset(LOCAL_IMAGE_NAMES)
local_logo_file = find_local_asset(LOCAL_LOGO_NAMES)

image_env = os.environ.get("CLIMAX_BG_IMAGE", "").strip()
logo_env = os.environ.get("CLIMAX_LOGO", "").strip()
dashboard_env = os.environ.get("CLIMAX_DASHBOARD_URL", "").strip()

if image_env:
    IMAGE_SRC = image_env
    IMAGE_SOURCE_TYPE = "env"
elif local_image_file:
    IMAGE_SRC = make_data_uri(local_image_file)
    IMAGE_SOURCE_TYPE = f"embedded_local:{local_image_file.name}"
else:
    IMAGE_SRC = GITHUB_RAW_FALLBACK
    IMAGE_SOURCE_TYPE = "github_raw_fallback"

if logo_env:
    NASA_LOGO = logo_env
    LOGO_SOURCE_TYPE = "env"
elif local_logo_file:
    try:
        NASA_LOGO = make_data_uri(local_logo_file)
        LOGO_SOURCE_TYPE = f"embedded_local_logo:{local_logo_file.name}"
    except Exception:
        NASA_LOGO = str(local_logo_file.as_uri())
        LOGO_SOURCE_TYPE = "local_uri"
else:
    NASA_LOGO = "https://raw.githubusercontent.com/baraa194/video-logo-/main/nasa-1.svg"
    LOGO_SOURCE_TYPE = "github_raw_fallback"

DASHBOARD_URL = dashboard_env or "http://localhost:8505"

# Debug info in sidebar
st.sidebar.title("Debug / Sources")
st.sidebar.write("IMAGE_SOURCE_TYPE:", IMAGE_SOURCE_TYPE)
st.sidebar.write("NASA_LOGO source:", LOGO_SOURCE_TYPE)
st.sidebar.write("If using local assets and not embedding, run (in .streamlit/assets): python -m http.server 9000")
st.sidebar.write("Embedded image avoids CORS/port issues during dev.")

# HTML/CSS template
html_template = """
<style>
/* full-bleed layout */
html, body, .main, .block-container, .stApp {
  height: 100%; margin: 0; padding: 0;
}
.block-container { padding: 0 !important; margin: 0 !important; max-width: 100% !important; }

/* hide streamlit header/footer for clean landing */
header, footer { display: none !important; }

/* make streamlit containers transparent so bg-image shows through */
.stApp, .main, .block-container { background: transparent !important; }

/* background image (cover) with subtle dark overlay */
.bg-image {
  position: fixed; inset: 0; z-index: -9999;
  background: linear-gradient(rgba(0,0,0,0.42), rgba(0,0,0,0.42)), url("__IMAGE_SRC__");
  background-size: cover; background-position: center center; background-repeat: no-repeat;
}

/* fallback <img> (if CSS background blocked) */
#bg-fallback {
  position: fixed; inset: 0; width: 100%; height: 100vh; object-fit: cover; z-index: -9998; display: none;
}

/* overlay content centering */
.landing-overlay { position: relative; z-index: 2; display:flex; align-items:center; justify-content:center; height:100vh; color:#fff; text-align:center; padding: 24px; pointer-events: none; }

/* wider card for larger headline and button */
.card { max-width:1400px; width:100%; pointer-events: auto; padding: 0 24px; box-sizing: border-box; }

/* headline */
.card h1 {
  font-size: clamp(40px, 7vw, 84px);
  margin: 0 0 14px; font-weight:900; line-height:1.02; text-shadow: 0 8px 36px rgba(0,0,0,0.6);
}

/* small subtitle */
.card p.lead { font-size:25px; opacity:0.95; margin-bottom:20px; }

/* CTA - wider, white text, no underline */
.btn-primary {
  display:inline-block;
  background: linear-gradient(180deg, #0b66e0 0%, #084fc1 100%);
  color: #ffffff !important;
  padding: 16px 42px;
  min-width: 320px;           /* ensure wide */
  border-radius: 12px;
  text-decoration: none !important; /* remove underline */
  font-weight:800;
  font-size:22px;
  box-shadow: 0 18px 46px rgba(11,94,215,0.14), 0 6px 22px rgba(8,79,193,0.12) inset;
  border: 0;
  pointer-events: auto;
}

/* remove default focus outline and add custom focus */
.btn-primary:focus { outline: none; box-shadow: 0 0 0 4px rgba(11,94,215,0.12); }

/* hover effect */
.btn-primary:hover { transform: translateY(-3px); box-shadow: 0 26px 56px rgba(11,94,215,0.18); text-decoration:none; color: #fff !important; }

/* round logo + app name top-left */
.logo-container { position: fixed; top: 16px; left: 16px; z-index: 6; display:flex; align-items:center; gap:12px; }
.logo { width:96px; height:96px; border-radius:50%; overflow:hidden; display:flex; align-items:center; justify-content:center; background: rgba(255,255,255,0.06); padding:6px; box-shadow: 0 10px 36px rgba(0,0,0,0.45); border:1px solid rgba(255,255,255,0.04); }
.logo img { display:block; max-width:100%; max-height:100%; object-fit:cover; border-radius:50%; }
.app-name { font-size:28px; font-weight:900; color:#fff; text-shadow:0 4px 12px rgba(0,0,0,0.5); }

/* debugging message in top-right */
#dbg-msg { position: fixed; right: 12px; top: 14px; z-index: 10; background: rgba(0,0,0,0.6); color: #fff; padding:6px 10px; border-radius:6px; font-size:13px; }

/* responsive adjustments */
@media (max-width: 980px) {
  .card h1 { font-size: clamp(28px, 9vw, 48px); }
  .btn-primary { min-width: 220px; padding: 12px 20px; font-size:15px; }
  .logo { width:72px; height:72px; }
  .app-name { font-size:20px; }
}
@media (max-width: 480px) {
  .card { padding: 0 12px; }
  .card h1 { font-size: clamp(22px, 9vw, 36px); }
  .btn-primary { width: 90%; min-width: 0; padding: 12px 12px; }
  .app-name { font-size:16px; }
}
</style>

<div class="bg-image" aria-hidden="true"></div>
<img id="bg-fallback" src="__IMAGE_SRC__" alt="background fallback" />

<div class="logo-container">
  <div class="logo">
    <a href="__DASHBOARD_URL__" target="_self" style="display:block; width:100%; height:100%; text-decoration:none;">
      <img src="__NASA_LOGO__" alt="ClimaX logo" />
    </a>
  </div>
  <div class="app-name">ClimaX App</div>
</div>

<div id="dbg-msg">Loading background...</div>

<div class="landing-overlay">
  <div class="card">
    <h1>Discover the probability of extreme weather</h1>
    <p class="lead">Powered by NASA Data</p>
    <!-- CTA is an anchor styled as a button: white text, no underline, wider -->
    <div>
      <a class="btn-primary" href="__DASHBOARD_URL__" role="button">Go to Dashboard</a>
    </div>
  </div>
</div>

<script>
(function(){
  const url = "__IMAGE_SRC__";
  const dbg = document.getElementById('dbg-msg');
  function setDbg(txt, bg){ dbg.innerText = txt; if (bg) dbg.style.background = bg; }
  const img = new Image();
  img.onload = function(){
    setDbg("Background loaded ✓");
    const fb = document.getElementById('bg-fallback');
    if (fb) fb.style.display = 'none';
    setTimeout(()=> dbg.style.display='none', 900);
  };
  img.onerror = function(e){
    setDbg("Background failed to load — showing fallback", "rgba(180,20,20,0.85)");
    const fb = document.getElementById('bg-fallback');
    if (fb) fb.style.display = 'block';
    console.error("Background image load error for", url, e);
  };
  // prevent stale caching during dev
  img.src = url + (url.includes('?') ? '&_ts=' : '?_ts=') + Date.now();
})();
</script>
"""

html_body = html_template.replace("__IMAGE_SRC__", IMAGE_SRC).replace("__NASA_LOGO__", NASA_LOGO).replace("__DASHBOARD_URL__", DASHBOARD_URL)

st.markdown(html_body, unsafe_allow_html=True)
st.markdown("---")
st.markdown(f"**Or click:** [Go to Dashboard]({DASHBOARD_URL})")

