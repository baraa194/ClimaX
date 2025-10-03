
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import base64
import mimetypes
import matplotlib.pyplot as plt
import requests
import json


from config import CITIES
from data_fetcher import get_nasa_weather, create_weather_dataframe, NASA_DATA_START_YEAR

st.set_page_config(page_title="ClimaX · Smart Activity Planner", layout="wide", initial_sidebar_state="collapsed")

ROOT = Path(__file__).resolve().parent
ASSETS_DIR = ROOT / ".streamlit" / "assets"


def find_local_asset(name):
    p = ASSETS_DIR / name
    return p if p.exists() else None


def make_data_uri(path: Path):
    b = path.read_bytes()
    mime, _ = mimetypes.guess_type(str(path))
    if not mime:
        mime = "application/octet-stream"
    b64 = base64.b64encode(b).decode("ascii")
    return f"data:{mime};base64,{b64}"



local_logo = None
for cand in ["nasa-1.svg", "nasa.svg", "logo.svg"]:
    p = find_local_asset(cand)
    if p:
        try:
            local_logo = make_data_uri(p)
        except Exception:
            local_logo = str(p.as_uri())
        break

NASA_LOGO = local_logo or "https://raw.githubusercontent.com/baraa194/video-logo-/main/nasa-1.svg"


BACKGROUND_CANDIDATES = [
    "pexels-pixabay-76969.jpg",
    "background.jpg",
    "hero.jpg",
    "pexels-pixabay-76969.jpeg"
]

background_asset = None
for name in BACKGROUND_CANDIDATES:
    p = find_local_asset(name)
    if p:
        background_asset = p
        break

BACKGROUND_DATA_URI = ""
if background_asset:
    try:
        BACKGROUND_DATA_URI = make_data_uri(background_asset)
    except Exception:
        try:
            BACKGROUND_DATA_URI = str(background_asset.as_uri())
        except Exception:
            BACKGROUND_DATA_URI = ""


GLOBAL_CSS = """
<style>
/* Defensive chrome hiding */
#MainMenu, footer, header[role="banner"], div[data-testid="stToolbar"], section[data-testid="stSidebar"], aside[role="complementary"] {
  display: none;
  visibility: hidden;
}

.cairo-override, .cairo-override * {
  color: #0b2a4a !important;    
  opacity: 1 !important;
}

.cairo-override input::placeholder {
  color: #0b2a4a !important;
  opacity: 1 !important;
}



/* palette */
:root{
  --climax-navy: #ffffff; 
  --input-text: #0b2a4a;  
  --climax-beige: #f5efe6;
  --btn-green-a: #43c06f;
  --btn-green-b: #28a745;
  --input-border: #e6e9ec;
}


body, .stApp, .main {
  background: linear-gradient(rgba(0,0,0,0.48), rgba(0,0,0,0.48)), url('ASSET_URL_PLACEHOLDER') center/cover fixed no-repeat;
  background-attachment: fixed;
  margin: 0;
  font-size: 36px; 
  line-height: 1.45;
  color: var(--climax-navy); 
}


.app-navbar {
  position: fixed !important;
  top: 48px !important;
  left: 12px !important;
  right: 12px !important;
  height: 100px !important;

  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 36px;
  z-index: 99999 !important;
  box-shadow: 0 8px 22px rgba(0,0,0,0.06);
  border-bottom: 1px solid rgba(0,0,0,0.04);
  border-radius: 12px;

}

/* brand */
.app-navbar .brand {
  display: flex;
  align-items: center;
  gap: 14px;
  white-space: nowrap;
}
.app-navbar .brand img {
  width:72px;
  height:72px;
  border-radius:50%;
  object-fit:cover;
  background:#fff;
  padding:6px;
  box-shadow:0 6px 18px rgba(0,0,0,0.12);
}

.app-navbar .brand .title {
  font-size: 28px;
  font-weight:900;
  color: var(--climax-navy);
  margin: 0;
}
.app-navbar .nav-actions a {
  color: var(--climax-navy);
  text-decoration: none;
  font-weight:700;
  font-size:22px;
  padding:6px 10px;
}


.block-container {
  max-width:1280px;
  margin-left:32px;
  margin-right:auto;
  padding-top:120px;
  box-sizing:border-box;
  background: transparent;
  color: var(--climax-navy);
}


h1, .stHeader {
  font-size: 56px;
  font-weight: 900;
  color: var(--climax-navy);
  text-shadow: 0 2px 8px rgba(0,0,0,0.45);
  margin-top: 20px;
}
h2 {
  font-size: 40px;
  font-weight: 800;
  color: var(--climax-navy);
  text-shadow: 0 1px 6px rgba(0,0,0,0.35);
}


.stMarkdown p:first-of-type, .stMarkdown div p:first-child {
  font-size: 30px;
  color: var(--climax-navy);
  margin-top: 6px;
  margin-bottom: 14px;
  font-weight: 600;
  text-shadow: 0 1px 4px rgba(0,0,0,0.25);
}


 block-container (labels, p, small, radio/checkbox labels, help text, etc.)
 
.block-container label,
.block-container p,
.block-container small,
.block-container .stMarkdown,
.block-container .streamlit-expanderHeader,
.block-container .stMetric,
.block-container .stMetricValue,
.block-container .stMetricLabel,
.block-container .stInfo,
.block-container .stText,
.block-container .stCaption,
.block-container .stRadio,
.block-container .stRadio label,
.block-container .stCheckbox,
.block-container .stCheckbox label,
.block-container .stSelectbox > label,
.block-container .css-1oe6wy1 /* generic streamlit text containers */ {
  font-size: 26px !important;
  color: var(--climax-navy) !important;
}
.stSelectbox:nth-of-type(1) div[role="combobox"] > div[tabindex] {
  color: #0b2a4a !important;  
  opacity: 1 !important;
}

.stSelectbox div[role="combobox"][aria-label*="Select your city"] > div[tabindex] {
  color: #0b2a4a !important;   
  opacity: 1 !important;
}


.stSelectbox input[placeholder="Cairo"],
.stSelectbox div[role="combobox"] input[placeholder="Cairo"] {
  color: #0b2a4a !important;
  opacity: 1 !important;
}


.stSelectbox:nth-of-type(1) div[role="combobox"] > div[tabindex] {
  color: #0b2a4a !important;
  opacity: 1 !important;
}



.block-container div[class*="st-"], 
.block-container span[class*="st-"],
.block-container .css-1l02zno, 
.block-container .css-1v3fvcr  {
  color: var(--climax-navy) !important;
    font-size: 26px !important;
}


input[type="text"], input[type="search"], textarea, select, .stTextInput>div>input {
  background: #ffffff !important;
  color: var(--input-text) !important; 
  font-size: 28px !important;
  padding: 12px 14px !important;
  border-radius: 10px !important;
  border: 1px solid var(--input-border) !important;
  min-height: 52px !important;
  box-shadow: 0 1px 0 rgba(0,0,0,0.02) !important;
}
.stTextArea>div>textarea {
  min-height: 300px !important;
  font-size: 28px !important;
  padding: 12px !important;
  border-radius: 10px !important;
  background: #ffffff !important;
  border: 1px solid var(--input-border) !important;
  color: var(--input-text) !important;
}


.stSelectbox div[role="combobox"] > div[tabindex] {
  padding: 14px 16px !important;
  font-size: 34px !important;
  min-height: 64px !important;
  border-radius: 10px !important;
  border: 1px solid var(--input-border) !important;
  background: #ffffff !important;
  color: var(--input-text) !important;
}


div[role="listbox"] li, ul[role="listbox"] li, div[role="menu"] li {
  font-size: 30px !important;
  padding: 10px 14px !important;
  color: var(--input-text) !important;
  min-height: 48px !important;
}
ul[role="listbox"], div[role="listbox"], div[role="menu"] {
  max-height: 420px !important;
  overflow: auto !important;
}


div.stButton > button, div.stDownloadButton > button {
  color: #ffffff !important;
  background: linear-gradient(180deg, var(--btn-green-a), var(--btn-green-b)) !important;
  border: none !important;
  font-weight: 900 !important;
  font-size: 30px !important;
  padding: 12px 28px !important;
  border-radius: 12px !important;
  box-shadow: 0 12px 28px rgba(40,167,69,0.12) !important;
}


.stDataFrame, .stTable {
  font-size: 28px !important;
  color: var(--input-text) !important;
}
.stDataFrame table, .stTable table {
  font-size: 26px !important;
}
.stDataFrame table th, .stTable table th,
.stDataFrame table td, .stTable table td {
  color: var(--input-text) !important;
  font-weight: 600 !important;
    font-size: 26px !important;
}

/* defensive */
div[title*="API Key"], div[aria-label*="API Key"] {
  display:none !important;
}

/* responsive tweaks */
@media (max-width: 900px) {
  .block-container { padding-top: 160px; margin-left: 18px; margin-right: 18px; }
  body, .stApp, .main { font-size: 27px; }
  input, textarea, select { font-size: 18px !important; padding: 10px !important; }
  .app-navbar { padding: 12px 18px; height: 86px; }
  .app-navbar .brand .title { font-size: 27px; }
}
</style>
"""


ASSET_URL_IN_CSS = BACKGROUND_DATA_URI if BACKGROUND_DATA_URI else ""
GLOBAL_CSS = GLOBAL_CSS.replace("ASSET_URL_PLACEHOLDER", ASSET_URL_IN_CSS)


NAVBAR_HTML = f"""
<div class="app-navbar">
  <div class="brand">
    <img src="{NASA_LOGO}" alt="logo" />
    <div>
      <div class="title">Dashboard</div>
    </div>
  </div>
  <div class="nav-actions">
    <a href="/" class="">Home</a>
  </div>
</div>
"""


st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
st.markdown(NAVBAR_HTML, unsafe_allow_html=True)


st.markdown("##")
st.markdown("<div style='padding:10px 0 18px 0'></div>", unsafe_allow_html=True)

st.title(" Smart Activity Planner")
st.markdown("Plan activities with weather-aware recommendations ")
st.markdown("---")


st.header("Select options")

selected_city = st.selectbox("Select your city:", list(CITIES.keys()))
plan_type = st.radio("Plan type:", ["Daily Plan", "Weekly Plan"], horizontal=False)

if plan_type == "Daily Plan":
    selected_date = st.date_input("Select date:", datetime.now().date())
    activities = st.text_area("Enter your daily activities (one per line):",
                              height=260,
                              placeholder="Morning jog\nGrocery shopping\nPicnic in the park\nGardening\nEvening walk")
else:
    start_date = st.date_input("Start date:", datetime.now().date())
    end_date = start_date + timedelta(days=6)
    activities = st.text_area("Enter your weekly activities (one per line ):",
                              height=260,
                              placeholder="Monday: Team meeting\nTuesday: Outdoor photoshoot\n...")

create_button = st.button("🧠 Create Smart Schedule")


OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "qwen2.5:3b-instruct"


def ollama_generate(prompt: str, model: str = OLLAMA_MODEL, timeout: int =300, temperature: float = 0.4) -> str:

    try:
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,           
            "options": {"temperature": temperature}
        }
        resp = requests.post(OLLAMA_URL, json=payload, timeout=timeout)
        resp.raise_for_status()
        data = resp.json()
        text = (data.get("response") or "").strip()
        return text if text else "⚠️ No response from the local model."
    except requests.exceptions.RequestException as e:
        return f"⚠️ Ollama error: {e}"
    except ValueError:
        return "⚠️ Failed to parse response from Ollama."


def _serialize_weather_keys(d: dict) -> dict:
    out = {}
    for k, v in d.items():
        if hasattr(k, "strftime"):
            out[k.strftime("%Y-%m-%d")] = v
        else:
            out[str(k)] = v
    return out

def generate_schedule_with_ollama(
    weather_data: dict,
    activities: str,
    plan_type: str,
    city: str,
    day: datetime | None,
    start_date=None,
    end_date=None
):

    if plan_type == "Daily Plan":
        date_str = day.strftime("%Y-%m-%d") if day else ""
        prompt = f"""
You are ClimaX's planner. Create a concise smart schedule.

City: {city}
Plan type: {plan_type}
Date: {date_str}
Activities:
{activities}

Weather data:
{weather_data}

Instructions:
- Group activities by morning/afternoon/evening.
- Consider temperature, precipitation, wind, humidity, solar radiation.
- If outdoor risky (hot >32°C, rain >1mm, wind >15 m/s), suggest alternative or shift.
- Keep short and practical. English only.
"""
    else:
        prompt = f"""
You are ClimaX's planner. Create a 7-day smart weekly plan.

City: {city}
Plan type: {plan_type}
Date Range: {start_date} to {end_date}
Activities (list):
{activities}

Weather data (by date):
{weather_data}

Instructions:
- Assign each activity to the best day depending on weather.
- Spread activities logically across the week.
- If outdoor activities clash with bad weather, move them to better days.
- Present as a bullet-point plan, **day by day (Mon-Sun)**.
- Use clear, concise English.
"""
    return ollama_generate(prompt)



def get_ai_recommendations_with_ollama(weather_data: dict, activities_list: list[str]) -> str:

    prompt = f"""
You recommend activity-specific tips based on weather.

Weather(JSON):
{weather_data}

Activities:
{activities_list}

For each activity, return 2-4 short bullet points (not tables), considering the weather risks and best timing.
Language: English.
"""
    return ollama_generate(prompt)



if create_button:
    if not activities or (plan_type == "Daily Plan" and not selected_date):
        st.warning("Please enter activities and select a date.")
    else:
        with st.spinner("📈 Analyzing decades of historical data to predict weather patterns..."):
            target_date = selected_date if plan_type == "Daily Plan" else start_date
            st.info(
                f"Analyzing historical data for {target_date.strftime('%Y-%m-%d')} based on trends from {NASA_DATA_START_YEAR} onwards.")

            weather_data = {}
            historical_data_for_plot = {}
            trend_data_for_plot = {}
            city_coords = CITIES[selected_city]

            if plan_type == "Daily Plan":
                pred, hist, trend = get_nasa_weather(city_coords, selected_date)
                if pred:
                    weather_data[selected_date] = pred
                    historical_data_for_plot[selected_date] = hist
                    trend_data_for_plot[selected_date] = trend
                else:
                    st.error("Could not retrieve enough historical data to make a prediction.")
                    st.stop()
            else:
                current_date = start_date
                while current_date <= end_date:
                    pred, hist, trend = get_nasa_weather(city_coords, current_date)
                    if pred:
                        weather_data[current_date] = pred
                        historical_data_for_plot[current_date] = hist
                        trend_data_for_plot[current_date] = trend
                    current_date += timedelta(days=1)
                if not weather_data:
                    st.error("Could not retrieve weather forecast for any of the selected days.")
                    st.stop()

            st.session_state['weather_data'] = weather_data
            st.session_state['historical_data'] = historical_data_for_plot
            st.session_state['trend_data'] = trend_data_for_plot
            st.session_state['activities'] = activities
            st.session_state['plan_type'] = plan_type
            st.session_state['selected_city'] = selected_city
            if plan_type == "Weekly Plan":
                st.session_state['start_date'] = start_date
                st.session_state['end_date'] = end_date

            ai_schedule = generate_schedule_with_ollama(
                weather_data=weather_data,
                activities=activities,
                plan_type=plan_type,
                city=selected_city,
                day=(selected_date if plan_type == "Daily Plan" else None),
                start_date=(start_date if plan_type == "Weekly Plan" else None),
                end_date=(end_date if plan_type == "Weekly Plan" else None)
            )

            st.session_state['ai_schedule'] = ai_schedule
            st.success("Smart schedule created successfully!")


if 'weather_data' in st.session_state:
    weather_data = st.session_state['weather_data']
    historical_data = st.session_state.get('historical_data', {})
    trend_data = st.session_state.get('trend_data', {})

    st.subheader("🌤️ Predicted Weather Data (Based on Historical Trends)")
    try:
        weather_df = create_weather_dataframe(weather_data)
        st.dataframe(weather_df, use_container_width=True)
    except Exception:
        pass

    st.subheader("🌤️ Detailed Weather Information & Trend Analysis")
    for date, data in weather_data.items():
        if data:
            with st.expander(f"Weather Details for {date.strftime('%A, %B %d')}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Temperature", f"{data['temperature']:.1f}°C")
                    st.metric("Humidity", f"{data['humidity']:.1f}%")
                with col2:
                    st.metric("Wind Speed", f"{data['wind_speed']:.1f} m/s")
                    st.metric("Precipitation", f"{data['precipitation']:.1f} mm")
                with col3:
                    st.metric("Pressure", f"{data['pressure']:.1f} hPa")
                    st.metric("Solar Radiation", f"{data.get('solar_radiation', 0):.1f} W/m²")

                hist = historical_data.get(date)
                trend = trend_data.get(date)
                if hist and trend and not np.isnan(trend['temperature']['slope']):
                    try:
                        years = list(hist.keys())
                        temps = [hist[y]['temperature'] for y in years]
                        slope = trend['temperature']['slope']
                        intercept = trend['temperature']['intercept']
                        predicted_temp = data['temperature']

                        fig, ax = plt.subplots(figsize=(10, 6))
                        ax.scatter(years, temps, label='Historical Data Points')
                        trend_line_x = np.array([min(years), max(years), date.year])
                        trend_line_y = slope * trend_line_x + intercept
                        ax.plot(trend_line_x, trend_line_y, linestyle='--', linewidth=2, label='Trend Line')
                        ax.scatter(date.year, predicted_temp, s=120, zorder=5, label=f'Predicted ({date.year})')
                        ax.set_xlabel("Year", fontsize=18, color="#0b2a4a")
                        ax.set_ylabel("Temperature (°C)", fontsize=18, color="#0b2a4a")
                        ax.set_title(
                            f"Temperature Trend for {date.strftime('%B %d')} in {st.session_state['selected_city']}",
                            fontsize=20, color="#0b2a4a")
                        ax.legend()
                        ax.grid(True, linestyle=':', alpha=0.6)
                        st.pyplot(fig)
                    except Exception as e:
                        st.write("Plot error:", e)
                else:
                    st.info("Not enough historical data to generate a reliable trend analysis.")

    st.subheader("💡 Smart Recommendations")

    activities_list = [act.strip() for act in st.session_state.get('activities', '').split('\n') if act.strip()]

    if not activities_list:
        st.info("Enter activities and press 'Create Smart Schedule' to get recommendations.")
    else:
        try:
            weather_for_llm = _serialize_weather_keys(weather_data)

            prompt = f"""
    You are ClimaX AI assistant.

    Weather data (JSON):
    {weather_for_llm}

    Activities:
    {activities_list}

    Task: Provide 3-5 concise, practical recommendations for the whole plan.
    - If Daily Plan → group them into Morning / Afternoon / Evening.
    - If Weekly Plan → assign activities day by day (Mon–Sun) depending on the weather.
    - Consider temperature, precipitation, wind, humidity, solar radiation.
    - Short, actionable, English only. No tables.
    """

            ai_text = ollama_generate(prompt)

            # عرض واضح حتى لو فيه تحذير
            if not ai_text or not ai_text.strip() or ai_text.strip().lower() in {"no response.", "no response"}:
                st.warning("⚠️ No Smart Recommendations generated.")
            elif ai_text.startswith("⚠️"):
                st.error(ai_text)
            else:
                st.markdown(ai_text)

        except Exception as e:
            st.error(f"Ollama error: {e}")
