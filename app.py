"""TCN Grid Outage Manager — 330kV / 132kV Equipment Outage Analytics.

Rebuilt around TCN_330kV_132kV_Outages_Compiled.xlsx:
Region | SubRegion_ACC | Substation | Equipment | Date_Off | Hour_Off | Minute_Off |
Date_On | Hour_On | Minute_On | Duration | Class | Last_Load_MW | Event_Indication |
Party_Responsible | Weather_Condition | Remarks
"""

import base64
import hashlib
import json
import re
from datetime import timedelta
from io import BytesIO
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ──────────────────────────────────────────────────────────────
# Paths & constants
# ──────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "TCN_330kV_132kV_Outages_Compiled.xlsx"
HIERARCHY_FILE = BASE_DIR / "Complete List of Substation.xlsx"
CATALOG_330_FILE = BASE_DIR / "330kV Transformers and Lines.xlsx"
CATALOG_132_FILE = BASE_DIR / "132kV Transformesr Capacity and 33kV Feeders - Copy.xlsx"
STATION_MAP_FILE = BASE_DIR / "station_region_map.csv"
USERS_FILE = BASE_DIR / "users.json"
LOGIN_BG = BASE_DIR / "login_bg.png"
APP_BG = BASE_DIR / "tcn_background.png"
LOGO = BASE_DIR / "tcn_logo.png"

TCN_RED = "#c81e28"
TCN_BLUE = "#1e3a7a"
TCN_COLORS = [TCN_BLUE, TCN_RED, "#1F6C9F", "#E06E6A", "#7DA3D8", "#956400", "#346538", "#8A8580"]
TCN_RED_SCALE = [[0, "#FBEAEA"], [0.5, "#E06E6A"], [1, TCN_RED]]

CLASS_COLORS = {"Forced": TCN_RED, "Emergency": "#956400", "Planned": TCN_BLUE}
VOLTAGE_COLORS = {"330kV": TCN_RED, "132kV": TCN_BLUE, "Other": "#8A8580"}
PARTY_COLORS = {
    "TCN": TCN_BLUE, "Weather": "#1F6C9F", "Disco": "#956400",
    "Generation Company": "#346538", "Vandalism": TCN_RED,
}
ETYPE_COLORS = {
    "Line": TCN_BLUE, "Transformer": TCN_RED, "Reactor": "#956400",
    "Bus": "#346538", "Feeder": "#1F6C9F", "Grid Event": "#8A8580",
}

TCN_CHART_LAYOUT = dict(
    font=dict(family="Source Sans Pro, sans-serif", size=12, color="#37352F"),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=10, r=10, t=48, b=10),
    title_font=dict(size=14, color="#37352F"),
    bargap=0.25,
    hoverlabel=dict(
        bgcolor="rgba(30, 47, 92, 0.92)",
        bordercolor="rgba(255,255,255,0.15)",
        font=dict(size=12, color="white"),
    ),
)

st.set_page_config(page_title="TCN Grid Outage Manager", page_icon="⚡", layout="wide")


# ──────────────────────────────────────────────────────────────
# Small helpers
# ──────────────────────────────────────────────────────────────
def _b64(path: Path) -> str:
    try:
        return base64.b64encode(path.read_bytes()).decode()
    except Exception:
        return ""


def _hash(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()


def _style_chart(fig):
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(gridcolor="rgba(55,53,47,0.08)", zeroline=False)
    return fig


def _eyebrow(text, bg="#E8EEF7", fg=TCN_BLUE):
    st.markdown(
        f'<span style="display:inline-block;font-size:0.68rem;font-weight:700;'
        f'letter-spacing:0.08em;text-transform:uppercase;padding:3px 10px;'
        f'border-radius:5px;background:{bg};color:{fg};">{text}</span>',
        unsafe_allow_html=True,
    )


ICONS = {
    "bolt": '<path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
    "power": '<path d="M18.36 6.64a9 9 0 1 1-12.73 0"/><line x1="12" y1="2" x2="12" y2="12"/>',
    "building": '<rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>',
    "pulse": '<path d="M22 12h-4l-3 9L9 3l-3 9H2"/>',
    "alert": '<path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>',
    "tower": '<path d="M12 2v20"/><path d="M6 22l6-14 6 14"/><path d="M8 12h8"/>',
    "chart": '<line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/>',
}


def kpi_card(label, value, unit="", icon="bolt", color=TCN_BLUE):
    unit_html = (
        f'<span style="font-size:0.7rem;color:var(--text-tertiary);margin-left:3px;">{unit}</span>'
        if unit else ""
    )
    r, g, b = tuple(int(color.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
    return f"""<div class="kpi-card"><div class="kpi-card-inner">
        <div class="kpi-left">
            <div class="kpi-icon" style="background:linear-gradient(135deg,rgba({r},{g},{b},0.12),rgba({r},{g},{b},0.05));">
                <svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{ICONS[icon]}</svg>
            </div>
            <div><div class="kpi-label">{label}</div><div class="kpi-value">{value}{unit_html}</div></div>
        </div>
    </div></div>"""


def kpi_grid(cards):
    n = len(cards)
    st.markdown(
        f'<div class="kpi-grid" style="grid-template-columns: repeat({n}, 1fr);">{"".join(cards)}</div>',
        unsafe_allow_html=True,
    )


# ──────────────────────────────────────────────────────────────
# CSS
# ──────────────────────────────────────────────────────────────
def inject_css():
    bg64 = _b64(APP_BG)
    bg_rule = (
        f'.stApp {{ background: linear-gradient(rgba(248,249,252,0.94), rgba(248,249,252,0.94)), '
        f'url("data:image/png;base64,{bg64}") center/cover fixed; }}'
        if bg64 else ".stApp { background: #f8f9fc; }"
    )
    st.markdown(f"""<style>
    @import url('https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@400;600;700&family=JetBrains+Mono:wght@500;600&display=swap');
    :root {{
        --text-primary: #37352F;
        --text-secondary: #787774;
        --text-tertiary: #9B9A97;
        --tcn-red: {TCN_RED};
        --tcn-blue: {TCN_BLUE};
        --surface: #FFFFFF;
        --border: rgba(55,53,47,0.09);
        --ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1);
    }}
    {bg_rule}
    html, body, [class*="css"] {{ font-family: 'Source Sans Pro', sans-serif; }}

    /* Sidebar */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #0a1630 0%, #0e1c3d 45%, {TCN_BLUE} 140%);
        border-right: 1px solid rgba(255,255,255,0.06);
    }}
    [data-testid="stSidebar"] * {{ color: #E8ECF5 !important; }}
    [data-testid="stSidebar"] hr {{ border-color: rgba(255,255,255,0.15); }}

    /* Filters header */
    .flt-header {{
        display: flex; align-items: center; gap: 0.7rem;
        margin: 1.1rem 0 0.9rem 0; padding: 0.85rem 0.9rem;
        background: linear-gradient(135deg, rgba(200,30,40,0.22), rgba(255,255,255,0.05) 65%);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 14px;
    }}
    .flt-icon {{
        width: 34px; height: 34px; border-radius: 9px; flex-shrink: 0;
        display: flex; align-items: center; justify-content: center;
        background: linear-gradient(135deg, {TCN_RED}, #8f1620);
        box-shadow: 0 2px 8px rgba(200,30,40,0.4);
    }}
    .flt-icon svg {{ width: 17px; height: 17px; }}
    .flt-title {{ font-size: 1.02rem; font-weight: 700; line-height: 1.2; }}
    .flt-sub {{ font-size: 0.68rem; color: #9FB0D6 !important; letter-spacing: 0.04em; }}

    /* Filter widget labels */
    [data-testid="stSidebar"] .stMultiSelect label p,
    [data-testid="stSidebar"] .stDateInput label p {{
        font-size: 0.7rem !important; font-weight: 700 !important;
        text-transform: uppercase; letter-spacing: 0.09em;
        color: #9FB0D6 !important;
    }}

    /* Glassy inputs */
    [data-testid="stSidebar"] .stMultiSelect [data-baseweb="select"] > div,
    [data-testid="stSidebar"] .stDateInput [data-baseweb="input"] {{
        background: rgba(255,255,255,0.07) !important;
        border: 1px solid rgba(255,255,255,0.16) !important;
        border-radius: 12px !important;
        transition: border-color 0.25s ease, background 0.25s ease, box-shadow 0.25s ease;
    }}
    [data-testid="stSidebar"] .stDateInput input {{ background: transparent !important; }}
    [data-testid="stSidebar"] .stMultiSelect [data-baseweb="select"] > div:hover,
    [data-testid="stSidebar"] .stDateInput [data-baseweb="input"]:hover {{
        border-color: rgba(255,255,255,0.38) !important;
        background: rgba(255,255,255,0.11) !important;
        box-shadow: 0 0 0 3px rgba(255,255,255,0.05);
    }}

    /* Tag pills — color-coded per filter */
    [data-testid="stSidebar"] span[data-baseweb="tag"] {{
        border-radius: 8px !important; font-weight: 600;
        border: none !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.15);
        transition: transform 0.2s var(--ease-spring);
    }}
    [data-testid="stSidebar"] span[data-baseweb="tag"]:hover {{ transform: translateY(-1px); }}
    .st-key-flt_region span[data-baseweb="tag"] {{
        background: linear-gradient(135deg, #2a4a94, {TCN_BLUE}) !important;
    }}
    .st-key-flt_voltage span[data-baseweb="tag"] {{
        background: linear-gradient(135deg, #d43a44, #9c1620) !important;
    }}
    .st-key-flt_class span[data-baseweb="tag"] {{
        background: linear-gradient(135deg, #b07a10, #7d5606) !important;
    }}
    .st-key-flt_etype span[data-baseweb="tag"] {{
        background: linear-gradient(135deg, #3f7a45, #2a5230) !important;
    }}

    /* Record count badge */
    .flt-count {{
        margin-top: 1.2rem; padding: 0.9rem 1rem;
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 14px;
    }}
    .flt-count-num {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.45rem; font-weight: 600; line-height: 1.1;
    }}
    .flt-count-label {{
        font-size: 0.68rem; color: #9FB0D6 !important;
        letter-spacing: 0.04em; margin: 2px 0 8px 0;
    }}
    .flt-count-bar {{
        height: 5px; border-radius: 99px; overflow: hidden;
        background: rgba(255,255,255,0.1);
    }}
    .flt-count-fill {{
        height: 100%; border-radius: 99px;
        background: linear-gradient(90deg, {TCN_RED}, #ff7a6b);
        transition: width 0.6s ease;
    }}

    /* KPI cards */
    .kpi-grid {{ display: grid; gap: 0.8rem; margin: 0.6rem 0 1.1rem 0; }}
    .kpi-card {{
        position: relative; background: var(--surface); border-radius: 14px;
        border: 1px solid var(--border);
        box-shadow: 0 1px 2px rgba(16,24,40,0.04), 0 4px 12px rgba(16,24,40,0.04);
        overflow: hidden;
        transition: transform 0.35s var(--ease-spring), box-shadow 0.35s ease;
    }}
    .kpi-card::before {{
        content: ""; position: absolute; inset: 0; border-radius: 14px; padding: 1px;
        background: linear-gradient(135deg, rgba(30,58,122,0.25), rgba(200,30,40,0.12), transparent 60%);
        -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        -webkit-mask-composite: xor; mask-composite: exclude;
        pointer-events: none;
    }}
    .kpi-card:hover {{ transform: translateY(-2px); box-shadow: 0 4px 8px rgba(16,24,40,0.06), 0 12px 24px rgba(16,24,40,0.08); }}
    .kpi-card-inner {{ display: flex; align-items: center; justify-content: space-between; padding: 1rem 1.1rem; }}
    .kpi-left {{ display: flex; align-items: center; gap: 0.75rem; }}
    .kpi-icon {{
        width: 40px; height: 40px; border-radius: 10px; flex-shrink: 0;
        display: flex; align-items: center; justify-content: center;
    }}
    .kpi-icon svg {{ width: 20px; height: 20px; }}
    .kpi-label {{
        font-size: 0.66rem; font-weight: 700; letter-spacing: 0.07em;
        text-transform: uppercase; color: var(--text-tertiary); margin-bottom: 2px;
    }}
    .kpi-value {{
        font-family: 'JetBrains Mono', monospace; font-size: 1.35rem;
        font-weight: 600; color: var(--text-primary); line-height: 1.15;
    }}

    /* Dashboard header */
    .dash-header {{ display: flex; align-items: center; justify-content: space-between; margin: 0.4rem 0 0.2rem 0; }}
    .dash-title {{ font-size: 1.9rem; font-weight: 700; color: var(--text-primary); margin: 0; }}
    .dash-sub {{ font-size: 0.85rem; color: var(--text-secondary); }}
    .live-badge {{
        display: inline-flex; align-items: center; gap: 6px; font-size: 0.72rem; font-weight: 600;
        color: #346538; background: #EDF3EC; padding: 4px 11px; border-radius: 999px;
    }}
    .live-dot {{
        width: 7px; height: 7px; border-radius: 50%; background: #4CAF50;
        animation: pulse 1.8s infinite;
    }}
    @keyframes pulse {{ 0%,100% {{ opacity: 1; }} 50% {{ opacity: 0.35; }} }}

    /* Tabs — bold pill navigation */
    .stTabs [data-baseweb="tab-list"] {{
        background: var(--surface);
        border-radius: 16px;
        padding: 6px;
        border: 1px solid var(--border);
        box-shadow: 0 1px 2px rgba(16,24,40,0.05), 0 4px 14px rgba(16,24,40,0.05);
        gap: 4px;
        flex-wrap: wrap;
    }}
    .stTabs [data-baseweb="tab"] {{
        border-radius: 11px;
        padding: 0.55rem 1.15rem;
        height: auto;
        background: transparent;
        transition: background 0.25s ease, box-shadow 0.25s ease,
                    transform 0.3s var(--ease-spring);
    }}
    .stTabs [data-baseweb="tab"] p {{
        font-weight: 700 !important;
        font-size: 0.88rem !important;
        letter-spacing: 0.015em;
        color: var(--text-secondary);
        transition: color 0.25s ease;
        white-space: nowrap;
    }}
    .stTabs [data-baseweb="tab"]:hover {{
        background: #F1F4FA;
        transform: translateY(-1px);
    }}
    .stTabs [data-baseweb="tab"]:hover p {{ color: var(--tcn-blue); }}
    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, {TCN_BLUE} 0%, #142a5c 100%) !important;
        box-shadow: 0 2px 10px rgba(30,58,122,0.35), inset 0 1px 0 rgba(255,255,255,0.12);
    }}
    .stTabs [aria-selected="true"]:hover {{ transform: none; }}
    .stTabs [aria-selected="true"] p {{ color: #FFFFFF !important; }}
    .stTabs [data-baseweb="tab-highlight"] {{ display: none; }}
    .stTabs [data-baseweb="tab-border"] {{ display: none; }}

    /* Buttons */
    .stButton > button[kind="primary"] {{
        background: {TCN_RED}; border: none; border-radius: 9px; font-weight: 600;
    }}
    header[data-testid="stHeader"] {{ background: transparent; }}
    </style>""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────
# Auth
# ──────────────────────────────────────────────────────────────
def load_users():
    if USERS_FILE.exists():
        return json.loads(USERS_FILE.read_text())
    users = {"admin": {"password": _hash("admin123"), "role": "admin",
                       "name": "Administrator", "region": None}}
    USERS_FILE.write_text(json.dumps(users, indent=2))
    return users


def save_users(users):
    USERS_FILE.write_text(json.dumps(users, indent=2))


def login_page():
    bg64 = _b64(LOGIN_BG)
    logo64 = _b64(LOGO)
    bg_css = (
        f'background: linear-gradient(rgba(6,12,30,0.60), rgba(6,12,30,0.72)), '
        f'url("data:image/png;base64,{bg64}") center/cover fixed !important;'
        if bg64 else
        "background: linear-gradient(160deg, #0a1630, #1e3a7a) !important;"
    )
    st.markdown(f"""<style>
    .stApp {{ {bg_css} }}
    header[data-testid="stHeader"] {{ background: transparent; }}

    /* Logo ring */
    .login-logo {{
        width: 96px; height: 96px; margin: 1.6rem auto 0 auto;
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        background: rgba(255,255,255,0.94);
        border: 1px solid rgba(255,255,255,0.35);
        box-shadow:
            0 0 0 8px rgba(255,255,255,0.07),
            0 0 0 16px rgba(255,255,255,0.035),
            0 8px 32px rgba(200,30,40,0.35);
        animation: logo-glow 3.5s ease-in-out infinite;
    }}
    @keyframes logo-glow {{
        0%, 100% {{ box-shadow: 0 0 0 8px rgba(255,255,255,0.07), 0 0 0 16px rgba(255,255,255,0.035), 0 8px 32px rgba(200,30,40,0.35); }}
        50% {{ box-shadow: 0 0 0 8px rgba(255,255,255,0.10), 0 0 0 16px rgba(255,255,255,0.05), 0 8px 44px rgba(200,30,40,0.55); }}
    }}
    .login-logo img {{ width: 64px; }}

    .login-title {{
        text-align: center; color: white; font-size: 2.1rem; font-weight: 700;
        margin: 0.9rem 0 0.1rem 0; letter-spacing: -0.01em;
        text-shadow: 0 2px 18px rgba(0,0,0,0.45);
    }}
    .login-sub {{
        text-align: center; color: rgba(255,255,255,0.72); font-size: 0.72rem;
        font-weight: 600; letter-spacing: 0.22em; text-transform: uppercase;
        margin-bottom: 1.1rem;
    }}
    .login-sub .dot {{ color: {TCN_RED}; font-weight: 700; }}

    /* Glass card with gradient border */
    [data-testid="stForm"] {{
        position: relative;
        background: linear-gradient(160deg, rgba(22,35,70,0.62), rgba(14,24,50,0.55));
        backdrop-filter: blur(18px); -webkit-backdrop-filter: blur(18px);
        border: 1px solid rgba(255,255,255,0.16);
        border-radius: 22px;
        padding: 1.9rem 1.8rem 1.6rem 1.8rem;
        box-shadow: 0 24px 64px rgba(0,0,0,0.45), inset 0 1px 0 rgba(255,255,255,0.12);
    }}
    [data-testid="stForm"] label p {{
        color: #C9D4EE !important; font-size: 0.7rem !important; font-weight: 700 !important;
        text-transform: uppercase; letter-spacing: 0.1em;
    }}
    [data-testid="stForm"] [data-baseweb="input"] {{
        background: rgba(255,255,255,0.09) !important;
        border: 1px solid rgba(255,255,255,0.18) !important;
        border-radius: 12px !important;
        transition: border-color 0.25s ease, background 0.25s ease, box-shadow 0.25s ease;
    }}
    [data-testid="stForm"] [data-baseweb="input"]:hover {{
        border-color: rgba(255,255,255,0.4) !important;
        background: rgba(255,255,255,0.13) !important;
    }}
    [data-testid="stForm"] [data-baseweb="input"]:focus-within {{
        border-color: rgba(224,110,106,0.85) !important;
        box-shadow: 0 0 0 3px rgba(200,30,40,0.25) !important;
    }}
    [data-testid="stForm"] [data-baseweb="base-input"] {{ background: transparent !important; }}
    [data-testid="stForm"] input {{ background: transparent !important; color: white !important; }}
    [data-testid="stForm"] input::placeholder {{ color: rgba(255,255,255,0.45) !important; }}

    /* Password reveal (eye) button — keep it subtle */
    [data-testid="stForm"] [data-baseweb="input"] button {{
        background: transparent !important; border: none !important;
        box-shadow: none !important;
    }}
    [data-testid="stForm"] [data-baseweb="input"] button svg {{ fill: rgba(255,255,255,0.6); }}

    /* Sign-in button */
    [data-testid="stForm"] [data-testid="stFormSubmitButton"] button {{
        background: linear-gradient(135deg, {TCN_RED} 0%, #8f1620 100%) !important;
        border: none !important; border-radius: 12px !important;
        padding: 0.62rem 1rem !important; margin-top: 0.5rem;
        box-shadow: 0 4px 18px rgba(200,30,40,0.45), inset 0 1px 0 rgba(255,255,255,0.22);
        transition: transform 0.3s var(--ease-spring), box-shadow 0.3s ease, filter 0.25s ease;
    }}
    [data-testid="stForm"] [data-testid="stFormSubmitButton"] button p {{
        color: white !important; font-weight: 700 !important;
        letter-spacing: 0.06em; text-transform: uppercase; font-size: 0.82rem !important;
    }}
    [data-testid="stForm"] [data-testid="stFormSubmitButton"] button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 26px rgba(200,30,40,0.6), inset 0 1px 0 rgba(255,255,255,0.25);
        filter: brightness(1.06);
    }}
    [data-testid="stForm"] [data-testid="stFormSubmitButton"] button:active {{ transform: translateY(0); }}

    .login-footer {{
        text-align: center; margin-top: 1.1rem;
        color: rgba(255,255,255,0.45); font-size: 0.7rem; letter-spacing: 0.08em;
    }}
    .login-footer b {{ color: rgba(255,255,255,0.65); }}
    </style>""", unsafe_allow_html=True)

    _, mid, _ = st.columns([1, 1.15, 1])
    with mid:
        if logo64:
            st.markdown(
                f'<div class="login-logo"><img src="data:image/png;base64,{logo64}"></div>',
                unsafe_allow_html=True,
            )
        st.markdown('<p class="login-title">TCN Grid Outage Manager</p>', unsafe_allow_html=True)
        st.markdown(
            '<p class="login-sub">330kV <span class="dot">·</span> 132kV Equipment Outages</p>',
            unsafe_allow_html=True,
        )
        with st.form("login"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            if st.form_submit_button("Sign In", use_container_width=True):
                users = load_users()
                u = users.get(username.strip())
                if u and u["password"] == _hash(password):
                    st.session_state.user = {"username": username.strip(), **{k: v for k, v in u.items() if k != "password"}}
                    st.rerun()
                else:
                    st.error("Invalid username or password")
        st.markdown(
            '<div class="login-footer"><b>TRANSMISSION COMPANY OF NIGERIA</b><br>'
            'Grid Operations · Secure Access</div>',
            unsafe_allow_html=True,
        )


# ──────────────────────────────────────────────────────────────
# Canonical station-name normalization (station_region_map.csv)
# ──────────────────────────────────────────────────────────────
_ST_STOP = {"t/s", "s/s", "ts", "ss", "t", "s", "substation", "substaion", "station",
            "switching", "gis", "mobile", "phase", "new"}

_ST_ALIASES = {
    "ajah": "aja", "amuwo": "amuwo odofin", "awka": "nibo awka",
    "dangora": "kwana dangora", "danagundi": "dan agundi", "fakun": "fakum",
    "gwarinpa": "gwarimpa", "ile ife": "ife", "ilesa": "ilesha", "offa": "ofa",
    "old abeokuta": "abeokuta", "olorunshogo": "olorunsogo", "ota": "otta",
    "oworo": "oworosoki", "oworonshoki": "oworosoki",
    "ph main": "port harcourt main", "ph mains": "port harcourt main",
    "ph town": "port harcourt town", "rumousi": "rumuosi",
    "tamburawa": "tambarawa", "ugwuaiji": "ugwuaji",
    "university of ibadan": "ui", "adiabo": "adiabor", "elelenwo": "elelenwon",
}

_ST_OVERRIDES = {
    "Adiabo 330kV": "Adiabor 330KV T/S",
    "Dadinkowa GS 132kV": "Dadinkowa GS",
}

# Cosmetic clean-ups applied AFTER canonical matching (typos in the map itself,
# combined multi-station names collapsed to the primary station)
_CANON_FIXUPS = {
    "Agu Awka132/33kV S/S": "Agu Awka 132/33kV S/S",
    "Nibo Awka` 132/33kV S/S": "Nibo Awka 132/33kV S/S",
    "katampe-1 132/33kV S/S": "Katampe-1 132/33kV S/S",
    "katampe-2 132/33kV S/S": "Katampe-2 132/33kV S/S",
    "Delta 330/132KV T/S Aladja Steel 330/132KV T/S": "Delta 330/132KV T/S",
    "Ihovbor 330/132kV TS Ihovbor NIPP 330/132kV TS Ihovbor Azura 330/132kV TS": "Ihovbor 330/132kV T/S",
    "Omotosho phase 1 330/132/33KV T/S Omotosho phase 2 330/132/33KV T/S": "Omotosho 330/132/33KV T/S",
    "New Abeokuta 132/3kV Substaion": "New Abeokuta 132/33kV Substation",
    "Sapade 132kv S/S": "Sapade 132kV S/S",
}

_SR_STOP = {"sub", "region", "sub-region", "subregion", "works", "work", "centre",
            "center", "w/c", "wc", "w", "c", "proposed", "axis"}


def _sr_key(name):
    s = str(name).lower().strip()
    s = re.sub(r"\(.*?\)", " ", s)
    s = s.replace("-", " ").replace("/", " ")
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    return " ".join(t for t in s.split() if t not in _SR_STOP).strip()


def _st_key(name):
    s = str(name).lower().strip()
    s = re.sub(r"\(.*?\)", " ", s)
    s = s.replace("`", "").replace("'", "").replace("-", " ")
    s = re.sub(r"\d{2,3}\s*/\s*\d{2,3}(\s*/\s*\d{2,3})?\s*kv", " ", s)
    s = re.sub(r"\d{2,3}\s*kv", " ", s)
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    return " ".join(t for t in s.split() if t not in _ST_STOP).strip()


@st.cache_data
def _station_lookup():
    if not STATION_MAP_FILE.exists():
        return None
    m = pd.read_csv(STATION_MAP_FILE).dropna(how="all")
    m = m[m["Region"].notna()]
    ts_map, ss_map, ts_first, ss_first = {}, {}, {}, {}
    station_subregion, sr_canon = {}, {}
    for _, r in m.iterrows():
        subregion = re.sub(r"\s+", " ", str(r["Sub-Region"]).strip())
        if subregion and subregion.lower() != "nan":
            srk = _sr_key(subregion)
            if srk and srk not in sr_canon:
                sr_canon[srk] = subregion
        ts = re.sub(r"\s+", " ", str(r["Transmission Station"]).strip())
        ss = re.sub(r"\s+", " ", str(r["Sub-Station"]).strip().replace("\n", " "))
        if ts and ts.lower() != "nan":
            k = _st_key(ts)
            if k and k not in ts_map:
                ts_map[k] = ts
            f = k.split()[0] if k else ""
            if f and f not in ts_first:
                ts_first[f] = ts
            final = _CANON_FIXUPS.get(ts, ts)
            if subregion and subregion.lower() != "nan":
                station_subregion.setdefault(final, subregion)
        if ss and ss.lower() != "nan":
            k = _st_key(ss)
            ss_clean = re.sub(
                r"\s*\((Under [Cc]onstruction|only fence|Only fence|Only plot of land|"
                r"Awaiting Mobitra|completed without lines|No transmission line)\)\s*$", "", ss)
            if k and k not in ss_map:
                ss_map[k] = ss_clean
            f = k.split()[0] if k else ""
            if f and f not in ss_first:
                ss_first[f] = ss_clean
            final = _CANON_FIXUPS.get(ss_clean, ss_clean)
            if subregion and subregion.lower() != "nan":
                station_subregion.setdefault(final, subregion)
    # stations absent from the map but with known sub-regions
    station_subregion.setdefault("Billiri 132kV", "Gombe Sub-Region")
    station_subregion.setdefault("Dadinkowa GS", "Gombe Sub-Region")
    station_subregion.setdefault("132KV DAWAKI T/S", "Abuja Sub-region")
    return ts_map, ss_map, ts_first, ss_first, station_subregion, sr_canon


def _st_lookup_level(k, m, mf):
    alias = _ST_ALIASES.get(k)
    if alias is None:
        toks = k.split()
        for n in range(len(toks), 0, -1):
            kk = " ".join(toks[:n])
            if kk in _ST_ALIASES:
                alias = _ST_ALIASES[kk]
                break
    for key in (k, alias):
        if not key:
            continue
        if key in m:
            return m[key]
        toks = key.split()
        for n in range(len(toks) - 1, 0, -1):
            kk = " ".join(toks[:n])
            if kk in m:
                return m[kk]
        f = key.split()[0] if key else ""
        if f in mf:
            return mf[f]
    return None


def normalize_station(raw):
    """Map a free-form substation name to its canonical name; return input if unmatched."""
    lookup = _station_lookup()
    raw = str(raw).strip()
    if lookup is None or not raw or raw.lower() == "nan":
        return raw
    if raw in _ST_OVERRIDES:
        return _ST_OVERRIDES[raw]
    if raw in _CANON_FIXUPS:
        return _CANON_FIXUPS[raw]
    ts_map, ss_map, ts_first, ss_first, _, _ = lookup
    k = _st_key(raw)
    if not k:
        return raw
    levels = [(ts_map, ts_first), (ss_map, ss_first)]
    if "330" not in raw:
        levels.reverse()
    for m, mf in levels:
        res = _st_lookup_level(k, m, mf)
        if res:
            return _CANON_FIXUPS.get(res, res)
    return raw


def normalize_subregion(station, raw_sr):
    """Canonical sub-region: prefer map lookup by station, else normalize the text."""
    lookup = _station_lookup()
    raw_sr = str(raw_sr).strip()
    if lookup is None or raw_sr.lower() == "nan":
        return raw_sr
    _, _, _, _, station_subregion, sr_canon = lookup
    target = station_subregion.get(str(station).strip())
    if target:
        return target
    return sr_canon.get(_sr_key(raw_sr), raw_sr)


# ──────────────────────────────────────────────────────────────
# Data loading & derivation
# ──────────────────────────────────────────────────────────────
def _parse_duration(v):
    if pd.isna(v):
        return np.nan
    s = str(v).strip()
    m = re.match(r"^(\d+):(\d{1,2})(?::(\d{1,2}))?$", s)
    if m:
        return int(m.group(1)) + int(m.group(2)) / 60 + (int(m.group(3) or 0)) / 3600
    try:
        return float(s)
    except ValueError:
        return np.nan


def _voltage(row):
    for field in (row["Equipment"], row["Substation"]):
        s = str(field)
        if "330" in s:
            return "330kV"
        if "132" in s:
            return "132kV"
    return "Other"


def _equip_type(e):
    s = str(e).lower()
    if "transformer" in s or re.search(r"\btr\d", s) or "mva" in s:
        return "Transformer"
    if "reactor" in s:
        return "Reactor"
    if "bus" in s:
        return "Bus"
    if "feeder" in s or "fdr" in s:
        return "Feeder"
    if "line" in s:
        return "Line"
    return "Grid Event"


@st.cache_data(show_spinner="Loading outage data…")
def load_data():
    df = pd.read_excel(DATA_FILE, sheet_name=0)
    df.columns = [c.strip() for c in df.columns]

    df["Duration_Hours"] = df["Duration"].map(_parse_duration)
    df["Datetime_Off"] = (
        pd.to_datetime(df["Date_Off"], dayfirst=True, errors="coerce")
        + pd.to_timedelta(pd.to_numeric(df["Hour_Off"], errors="coerce").fillna(0), unit="h")
        + pd.to_timedelta(pd.to_numeric(df["Minute_Off"], errors="coerce").fillna(0), unit="m")
    )
    df["Datetime_On"] = (
        pd.to_datetime(df["Date_On"], dayfirst=True, errors="coerce")
        + pd.to_timedelta(pd.to_numeric(df["Hour_On"], errors="coerce").fillna(0), unit="h")
        + pd.to_timedelta(pd.to_numeric(df["Minute_On"], errors="coerce").fillna(0), unit="m")
    )
    df["Status"] = np.where(df["Datetime_On"].isna(), "Ongoing", "Restored")
    df["Voltage_Level"] = df.apply(_voltage, axis=1)  # uses raw names before normalization
    df["Equipment_Type"] = df["Equipment"].map(_equip_type)
    # Canonical station & sub-region names from station_region_map.csv (fixes typos &
    # duplicates, including rows arriving via Upload Data and Report Outage)
    _canon_cache = {s: normalize_station(s) for s in df["Substation"].dropna().astype(str).str.strip().unique()}
    df["Substation"] = df["Substation"].astype(str).str.strip().map(lambda s: _canon_cache.get(s, s))
    _sr_cache = {}
    for st, sr in df[["Substation", "SubRegion_ACC"]].drop_duplicates().itertuples(index=False):
        _sr_cache[(st, str(sr).strip())] = normalize_subregion(st, sr)
    df["SubRegion_ACC"] = [
        _sr_cache.get((st, str(sr).strip()), sr)
        for st, sr in zip(df["Substation"], df["SubRegion_ACC"])
    ]
    df["Last_Load_MW"] = pd.to_numeric(df["Last_Load_MW"], errors="coerce")

    # Officer fields (added later — backfill for older workbooks that lack them)
    for col in ("Officer_Interruption", "Officer_Restoration"):
        if col not in df.columns:
            df[col] = None
        df[col] = df[col].astype(str).str.strip().replace(
            {"nan": None, "None": None, "": None, "NaT": None})

    for col in ("Class", "Weather_Condition", "Party_Responsible", "Region"):
        df[col] = df[col].astype(str).str.strip().replace({"nan": "Unspecified", "None": "Unspecified", "": "Unspecified"})
    return df


def _norm_region_name(r):
    r = str(r).strip().title()
    if "Harcourt" in r or "Harcout" in r:
        return "Port-Harcourt"
    return r


def _clean_cell(s):
    if pd.isna(s):
        return None
    s = " ".join(str(s).split())
    return s or None


@st.cache_data(show_spinner="Loading equipment catalog…")
def load_catalog():
    """Canonical equipment register from the 330kV and 132kV reference workbooks.

    Includes region, sub-region, station, line names/nomenclature and
    transformer names/nomenclature. 33kV feeder names and peak load are
    intentionally excluded.
    """
    rows = []

    # ── 330kV Transformers and Lines ──
    if CATALOG_330_FILE.exists():
        xl = pd.ExcelFile(CATALOG_330_FILE)
        skip = {"dashboard", "station summary"}
        for sheet in [s for s in xl.sheet_names if s.strip().lower() not in skip]:
            raw = pd.read_excel(xl, sheet_name=sheet, header=None)
            hdr = None
            for i in range(min(15, len(raw))):
                if str(raw.iat[i, 0]).strip() == "Region":
                    hdr = i
                    break
            if hdr is None:
                continue
            df = raw.iloc[hdr + 1:].copy()
            df.columns = [str(c).replace("\n", " ").strip() for c in raw.iloc[hdr]]
            for col in ("Region", "Subregion", "Substation"):
                if col in df.columns:
                    df[col] = df[col].ffill()
            for _, r in df.iterrows():
                station = _clean_cell(r.get("Substation"))
                if not station:
                    continue
                region = _norm_region_name(r.get("Region"))
                sub = _clean_cell(r.get("Subregion"))
                tn = _clean_cell(r.get("Transformer Naming"))
                tnom = _clean_cell(r.get("Transformer Nomenclature"))
                if tn or tnom:
                    name = tn or "330/132kV Transformer"
                    if tnom and tnom not in name:
                        name = f"{name} ({tnom})"
                    rows.append((region, sub, station, "Transformer", "330kV", name))
                ln = _clean_cell(r.get("330/132kV Line Naming"))
                lnom = _clean_cell(r.get("330kV Line Nomenclature"))
                if ln or lnom:
                    name = ln or "330kV Line"
                    if lnom and lnom not in name:
                        name = f"{name} ({lnom})"
                    rows.append((region, sub, station, "Line", "330kV", name))

    # ── 132kV Transformers (feeders & peak load excluded) ──
    if CATALOG_132_FILE.exists():
        raw = pd.read_excel(CATALOG_132_FILE, sheet_name="ALL REGIONS", header=None)
        hdr = None
        for i in range(min(15, len(raw))):
            if str(raw.iat[i, 0]).strip() == "S/N":
                hdr = i
                break
        if hdr is not None:
            df = raw.iloc[hdr + 1:].copy()
            cols = [str(c).replace("\n", " ").strip() for c in raw.iloc[hdr]]
            df.columns = cols
            desig_c = next((c for c in cols if c.startswith("Transformer Designation")), None)
            nom_c = next((c for c in cols if c.startswith("Transformer Nomenclature")), None)
            rat_c = next((c for c in cols if c.startswith("Transformer Rating")), None)
            for col in ("Region", "Sub-Region", "Substation"):
                df[col] = df[col].ffill()
            for _, r in df.iterrows():
                desig = _clean_cell(r.get(desig_c)) if desig_c else None
                nom = _clean_cell(r.get(nom_c)) if nom_c else None
                if not (desig or nom):
                    continue
                station = _clean_cell(r.get("Substation"))
                region = _norm_region_name(r.get("Region"))
                if not station or region in ("Nan", "None"):
                    continue
                try:
                    rating = float(r.get(rat_c))
                except (TypeError, ValueError):
                    rating = None
                base = f"{rating:g}MVA 132/33kV Transformer" if rating else "132/33kV Transformer"
                name = f"{base} {desig}" if desig else base
                if nom and nom not in name:
                    name = f"{name} ({nom})"
                rows.append((region, _clean_cell(r.get("Sub-Region")), station, "Transformer", "132kV", name))

    cat = pd.DataFrame(rows, columns=["Region", "SubRegion", "Substation",
                                      "Equipment_Type", "Voltage_Level", "Equipment"])

    # Canonical station & sub-region names (station_region_map.csv) so the two
    # reference workbooks resolve to the SAME station entry — e.g. "AJAOKUTA TS
    # (2AJA)" and "132KV AJAOKUTA TS" no longer appear as separate stations.
    def _canon_cat_station(name, vl):
        n = str(name).strip()
        hint = n if ("330" in n or "132" in n) else f"{n} {vl}"
        res = normalize_station(hint)
        return n if res == hint else res

    _st_cache = {
        (n, v): _canon_cat_station(n, v)
        for n, v in cat[["Substation", "Voltage_Level"]].drop_duplicates().itertuples(index=False)
    }
    cat["Substation"] = [_st_cache[(n, v)] for n, v in zip(cat["Substation"], cat["Voltage_Level"])]
    _sr_cat_cache = {
        (st, str(sr)): normalize_subregion(st, sr)
        for st, sr in cat[["Substation", "SubRegion"]].drop_duplicates().itertuples(index=False)
    }
    cat["SubRegion"] = [_sr_cat_cache[(st, str(sr))] for st, sr in zip(cat["Substation"], cat["SubRegion"])]
    return cat.drop_duplicates(subset=["Substation", "Equipment"]).reset_index(drop=True)


@st.cache_data
def load_hierarchy():
    try:
        h = pd.read_excel(HIERARCHY_FILE, sheet_name="Sheet1")
        h.columns = [c.strip() for c in h.columns]
        for c in h.columns:
            if h[c].dtype == object:
                h[c] = h[c].astype(str).str.strip()
        h["Region"] = h["Region"].str.title().replace({"Port Harcourt": "Port-Harcourt", "Port-Harcourt ": "Port-Harcourt"})
        return h.dropna(subset=["Region"])
    except Exception:
        return pd.DataFrame()


# ──────────────────────────────────────────────────────────────
# Sidebar filters
# ──────────────────────────────────────────────────────────────
def sidebar_filters(df, user):
    with st.sidebar:
        role_badge = "Admin" if user["role"] == "admin" else "Operator"
        scope = user["region"] or "All Regions"
        st.markdown(
            f"**{user['name']}** ({user['username']})<br>"
            f'<span style="font-size:0.72rem;background:rgba(255,255,255,0.14);padding:2px 8px;'
            f'border-radius:5px;font-family:monospace;">{role_badge}</span> · {scope}',
            unsafe_allow_html=True,
        )
        if st.button("Logout", type="primary"):
            st.session_state.pop("user", None)
            st.rerun()

        st.markdown("""
        <div class="flt-header">
            <div class="flt-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="#EDF1FA" stroke-width="2"
                     stroke-linecap="round" stroke-linejoin="round">
                    <polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/>
                </svg>
            </div>
            <div>
                <div class="flt-title">Filters</div>
                <div class="flt-sub">Refine the grid view</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        dmin = df["Datetime_Off"].min()
        dmax = df["Datetime_Off"].max()
        date_range = st.date_input(
            "📅 Date Range",
            value=(dmin.date(), dmax.date()) if pd.notna(dmin) else (),
            key="flt_date",
        )

        regions_all = sorted(df["Region"].dropna().unique())
        if user["region"]:
            regions = [user["region"]]
            st.multiselect("🌍 Region", regions_all, default=regions, disabled=True, key="flt_region")
        else:
            regions = st.multiselect("🌍 Region", regions_all, default=regions_all, key="flt_region")

        voltages = st.multiselect("⚡ Voltage Level", ["330kV", "132kV", "Other"],
                                  default=["330kV", "132kV", "Other"], key="flt_voltage")
        classes = st.multiselect("🚨 Outage Class", sorted(df["Class"].unique()),
                                 default=sorted(df["Class"].unique()), key="flt_class")
        etypes = st.multiselect("🔧 Equipment Type", sorted(df["Equipment_Type"].unique()),
                                default=sorted(df["Equipment_Type"].unique()), key="flt_etype")

    filtered = df[
        df["Region"].isin(regions)
        & df["Voltage_Level"].isin(voltages)
        & df["Class"].isin(classes)
        & df["Equipment_Type"].isin(etypes)
    ]
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start, end = date_range
        filtered = filtered[
            (filtered["Datetime_Off"] >= pd.Timestamp(start))
            & (filtered["Datetime_Off"] < pd.Timestamp(end) + timedelta(days=1))
        ]

    with st.sidebar:
        pct = (len(filtered) / len(df) * 100) if len(df) else 0
        st.markdown(f"""
        <div class="flt-count">
            <div class="flt-count-num">{len(filtered):,}</div>
            <div class="flt-count-label">records in view · {pct:.0f}% of data</div>
            <div class="flt-count-bar"><div class="flt-count-fill" style="width:{pct:.0f}%;"></div></div>
        </div>
        """, unsafe_allow_html=True)
    return filtered


# ──────────────────────────────────────────────────────────────
# Pages
# ──────────────────────────────────────────────────────────────
def show_dashboard(df, user):
    st.markdown(f"""
    <div class="dash-header">
        <div>
            <p class="dash-sub" style="margin-bottom:0;">Welcome back, <b>{user['name']}</b></p>
            <h1 class="dash-title">Grid Operations Dashboard</h1>
            <p class="dash-sub">{df['Region'].nunique()} regions · {len(df):,} outage records · 330kV / 132kV network</p>
        </div>
        <span class="live-badge"><span class="live-dot"></span>Live</span>
    </div>
    """, unsafe_allow_html=True)

    if df.empty:
        st.info("No records match the current filters.")
        return

    ongoing = int((df["Status"] == "Ongoing").sum())
    kpi_grid([
        kpi_card("Total Outages", f"{len(df):,}", icon="bolt", color=TCN_BLUE),
        kpi_card("Total Duration", f"{df['Duration_Hours'].sum():,.1f}", "hrs", icon="clock", color=TCN_RED),
        kpi_card("Load Lost", f"{df['Last_Load_MW'].sum():,.1f}", "MW", icon="power", color="#956400"),
        kpi_card("Ongoing", f"{ongoing:,}", icon="alert", color="#E06E6A" if ongoing else "#346538"),
        kpi_card("Substations", f"{df['Substation'].nunique()}", icon="building", color="#1F6C9F"),
    ])

    # Voltage split mini row
    v330 = df[df["Voltage_Level"] == "330kV"]
    v132 = df[df["Voltage_Level"] == "132kV"]
    kpi_grid([
        kpi_card("330kV Outages", f"{len(v330):,}", f"· {v330['Duration_Hours'].sum():,.0f} hrs", icon="tower", color=TCN_RED),
        kpi_card("132kV Outages", f"{len(v132):,}", f"· {v132['Duration_Hours'].sum():,.0f} hrs", icon="tower", color=TCN_BLUE),
        kpi_card("Equipment Affected", f"{df['Equipment'].nunique():,}", icon="pulse", color="#346538"),
        kpi_card("Avg Duration", f"{df['Duration_Hours'].mean():.2f}" if df['Duration_Hours'].notna().any() else "—", "hrs", icon="chart", color="#1F6C9F"),
    ])

    # Row 1: region bar + daily trend
    c1, c2 = st.columns(2)
    with c1:
        by_region = df.groupby(["Region", "Voltage_Level"]).size().reset_index(name="Outages")
        fig = px.bar(by_region, x="Region", y="Outages", color="Voltage_Level",
                     title="Outages by Region & Voltage Level",
                     color_discrete_map=VOLTAGE_COLORS, barmode="stack")
        fig.update_layout(height=380, **TCN_CHART_LAYOUT)
        fig.update_traces(marker_line_width=0, marker_cornerradius=4)
        _style_chart(fig)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        daily = df.dropna(subset=["Datetime_Off"]).copy()
        daily["Day"] = daily["Datetime_Off"].dt.floor("D")
        trend = daily.groupby("Day").agg(Outages=("Day", "size"), Load=("Last_Load_MW", "sum")).reset_index()
        trend["Day"] = pd.to_datetime(trend["Day"])
        monthly = trend.set_index("Day").resample("MS").agg(
            Outages=("Outages", "sum"), Load=("Load", "sum"),
        ).reset_index()
        monthly["Label"] = monthly["Day"].dt.strftime("%b '%y")
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=monthly["Label"], y=monthly["Outages"], name="Outages",
            marker_color=TCN_BLUE, marker_line_width=0, marker_cornerradius=4, opacity=0.85,
        ))
        fig.add_trace(go.Scatter(
            x=monthly["Label"], y=monthly["Load"], name="Load Lost (MW)", yaxis="y2",
            mode="lines+markers",
            line=dict(color=TCN_RED, width=2.5, shape="spline"),
            marker=dict(size=6, color=TCN_RED, line=dict(width=1.5, color="white")),
        ))
        fig.update_layout(
            title="Monthly Outages & Load Lost",
            yaxis=dict(title="Outages"),
            yaxis2=dict(title="MW", overlaying="y", side="right", showgrid=False),
            xaxis=dict(tickangle=-45),
            legend=dict(x=0, y=1.14, orientation="h", font=dict(size=11), bgcolor="rgba(0,0,0,0)"),
            height=380, **{**TCN_CHART_LAYOUT, "bargap": 0.35},
        )
        _style_chart(fig)
        st.plotly_chart(fig, use_container_width=True)

    # Row 2: class pie + equipment type + party responsible
    c3, c4, c5 = st.columns(3)
    with c3:
        by_class = df["Class"].value_counts().reset_index()
        by_class.columns = ["Class", "Count"]
        fig = px.pie(by_class, names="Class", values="Count", hole=0.45,
                     title="Outage Classification", color="Class", color_discrete_map=CLASS_COLORS)
        fig.update_layout(height=360, **TCN_CHART_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)
    with c4:
        by_et = df["Equipment_Type"].value_counts().reset_index()
        by_et.columns = ["Type", "Count"]
        fig = px.pie(by_et, names="Type", values="Count", hole=0.45,
                     title="Equipment Type", color="Type", color_discrete_map=ETYPE_COLORS)
        fig.update_layout(height=360, **TCN_CHART_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)
    with c5:
        by_party = df["Party_Responsible"].value_counts().reset_index()
        by_party.columns = ["Party", "Count"]
        fig = px.pie(by_party, names="Party", values="Count", hole=0.45,
                     title="Party Responsible", color="Party", color_discrete_map=PARTY_COLORS)
        fig.update_layout(height=360, **TCN_CHART_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)

    # Row 3: duration by region + weather + top events
    c6, c7 = st.columns(2)
    with c6:
        dur = df.groupby("Region")["Duration_Hours"].sum().sort_values().reset_index()
        fig = px.bar(dur, x="Duration_Hours", y="Region", orientation="h",
                     title="Total Outage Duration by Region (hrs)",
                     color="Duration_Hours", color_continuous_scale=TCN_RED_SCALE)
        fig.update_layout(height=380, coloraxis_showscale=False, **TCN_CHART_LAYOUT)
        fig.update_traces(marker_line_width=0, marker_cornerradius=4)
        _style_chart(fig)
        st.plotly_chart(fig, use_container_width=True)
    with c7:
        events = df["Event_Indication"].astype(str).str.strip().value_counts().head(10).reset_index()
        events.columns = ["Event", "Count"]
        fig = px.bar(events, x="Count", y="Event", orientation="h", title="Top 10 Event Indications",
                     color_discrete_sequence=[TCN_BLUE])
        fig.update_layout(height=380, yaxis=dict(autorange="reversed"), **TCN_CHART_LAYOUT)
        fig.update_traces(marker_line_width=0, marker_cornerradius=4)
        _style_chart(fig)
        st.plotly_chart(fig, use_container_width=True)


def show_records(df):
    _eyebrow("Data", "#E8EEF7", TCN_BLUE)
    st.header("Outage Records")
    search = st.text_input("Search records", placeholder="Search equipment, substation, remarks…")
    view = df
    if search:
        mask = pd.Series(False, index=df.index)
        for col in ("Equipment", "Substation", "Remarks", "Event_Indication", "Region"):
            mask |= df[col].astype(str).str.contains(search, case=False, na=False)
        view = df[mask]
    st.caption(f"{len(view):,} records")
    cols = ["Region", "SubRegion_ACC", "Substation", "Equipment", "Voltage_Level",
            "Equipment_Type", "Datetime_Off", "Datetime_On", "Duration_Hours", "Status",
            "Class", "Last_Load_MW", "Event_Indication", "Officer_Interruption", "Officer_Restoration", "Party_Responsible",
            "Weather_Condition", "Remarks"]
    st.dataframe(view[cols], use_container_width=True, height=520)


def show_region_analysis(df):
    _eyebrow("Analysis", "#EDF3EC", "#346538")
    st.header("Region Analysis")

    r1, r2, r3 = st.columns(3)
    with r1:
        region = st.selectbox("Region", sorted(df["Region"].dropna().unique()), key="ra_region")
    rdf = df[df["Region"] == region]
    with r2:
        subregion = st.selectbox(
            "Sub-Region / ACC", ["All Sub-Regions"] + sorted(rdf["SubRegion_ACC"].dropna().unique().tolist()),
            key="ra_subregion")
    if subregion != "All Sub-Regions":
        rdf = rdf[rdf["SubRegion_ACC"] == subregion]
    with r3:
        station = st.selectbox(
            "Station *(optional)*", ["All Stations"] + sorted(rdf["Substation"].dropna().unique().tolist()),
            key="ra_station")
    if station != "All Stations":
        rdf = rdf[rdf["Substation"] == station]
    scope = f"{station} ({region})" if station != "All Stations" else (
        f"{subregion} ({region})" if subregion != "All Sub-Regions" else region)

    if rdf.empty:
        st.info("No records for this selection.")
        return

    last_label = "Equipment" if station != "All Stations" else "Substations"
    last_value = rdf["Equipment"].nunique() if station != "All Stations" else rdf["Substation"].nunique()
    kpi_grid([
        kpi_card("Outages", f"{len(rdf):,}", icon="bolt", color=TCN_BLUE),
        kpi_card("Total Duration", f"{rdf['Duration_Hours'].sum():,.1f}", "hrs", icon="clock", color=TCN_RED),
        kpi_card("Load Lost", f"{rdf['Last_Load_MW'].sum():,.1f}", "MW", icon="power", color="#956400"),
        kpi_card(last_label, f"{last_value}", icon="building", color="#1F6C9F"),
    ])

    c1, c2 = st.columns(2)
    with c1:
        if station != "All Stations":
            top = rdf.groupby("Equipment").agg(Outages=("Equipment", "size"), Load=("Last_Load_MW", "sum")).reset_index()
            top = top.sort_values("Outages", ascending=False).head(15)
            fig = px.bar(top, x="Outages", y="Equipment", orientation="h",
                         title=f"Equipment Outages: {scope}", color="Load",
                         color_continuous_scale=TCN_RED_SCALE)
            fig.update_layout(height=420, yaxis=dict(autorange="reversed"), coloraxis_showscale=False, **TCN_CHART_LAYOUT)
        else:
            top = rdf.groupby("Substation").agg(Outages=("Substation", "size"), Load=("Last_Load_MW", "sum")).reset_index()
            top = top.sort_values("Outages", ascending=False).head(15)
            fig = px.bar(top, x="Substation", y="Outages", color="Load",
                         title=f"Top Substations: {scope}", color_continuous_scale=TCN_RED_SCALE)
            fig.update_layout(height=420, xaxis_tickangle=-45, coloraxis_showscale=False, **TCN_CHART_LAYOUT)
        fig.update_traces(marker_line_width=0, marker_cornerradius=4)
        _style_chart(fig)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        top_dur = rdf.groupby("Equipment")["Duration_Hours"].sum().sort_values(ascending=False).head(15).reset_index()
        fig = px.bar(top_dur, x="Duration_Hours", y="Equipment", orientation="h",
                     title=f"Longest Equipment Downtime: {scope}",
                     color_discrete_sequence=[TCN_BLUE])
        fig.update_layout(height=420, yaxis=dict(autorange="reversed"), **TCN_CHART_LAYOUT)
        fig.update_traces(marker_line_width=0, marker_cornerradius=4)
        _style_chart(fig)
        st.plotly_chart(fig, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        by_class = rdf["Class"].value_counts().reset_index()
        by_class.columns = ["Class", "Count"]
        fig = px.pie(by_class, names="Class", values="Count", hole=0.45,
                     title=f"Outage Classification: {scope}", color="Class", color_discrete_map=CLASS_COLORS)
        fig.update_layout(height=380, **TCN_CHART_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)
    with c4:
        by_weather = rdf["Weather_Condition"].value_counts().reset_index()
        by_weather.columns = ["Weather", "Count"]
        fig = px.pie(by_weather, names="Weather", values="Count", hole=0.45,
                     title=f"Weather During Outages: {scope}",
                     color_discrete_sequence=TCN_COLORS)
        fig.update_layout(height=380, **TCN_CHART_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)

    st.subheader(f"Records: {scope}")
    cols = ["Substation", "Equipment", "Voltage_Level", "Equipment_Type", "Datetime_Off",
            "Datetime_On", "Duration_Hours", "Status", "Class", "Last_Load_MW",
            "Event_Indication", "Officer_Interruption", "Officer_Restoration", "Party_Responsible", "Weather_Condition", "Remarks"]
    st.dataframe(rdf[cols], use_container_width=True, height=380)

    # ── Generate Analysis panel ──
    scope_chips = ""
    for label, val in [("Region", region), ("Sub-Region", subregion), ("Station", station)]:
        active = not val.startswith("All")
        chip_bg = "rgba(200,30,40,0.14)" if active else "rgba(255,255,255,0.10)"
        chip_bd = "rgba(224,110,106,0.45)" if active else "rgba(255,255,255,0.16)"
        chip_fg = "#FFD9D6" if active else "#B9C4E0"
        display = val if len(val) <= 42 else val[:40] + "…"
        scope_chips += (
            f'<span style="display:inline-flex;align-items:center;gap:5px;font-size:0.68rem;'
            f'font-weight:600;padding:4px 10px;border-radius:999px;margin:0 6px 6px 0;'
            f'background:{chip_bg};border:1px solid {chip_bd};color:{chip_fg};">'
            f'<span style="opacity:0.6;">{label}</span> {display}</span>'
        )

    st.markdown(f"""
    <div style="position:relative;margin-top:1.6rem;padding:1.5rem 1.6rem 1.2rem 1.6rem;
                border-radius:18px;overflow:hidden;
                background:linear-gradient(135deg, #12224a 0%, #1e3a7a 55%, #35204a 130%);
                box-shadow:0 12px 36px rgba(14,28,61,0.35), inset 0 1px 0 rgba(255,255,255,0.10);">
        <div style="position:absolute;top:-60px;right:-40px;width:220px;height:220px;border-radius:50%;
                    background:radial-gradient(circle, rgba(200,30,40,0.35), transparent 70%);"></div>
        <div style="display:flex;align-items:center;gap:0.9rem;margin-bottom:0.8rem;">
            <div style="width:42px;height:42px;border-radius:11px;display:flex;align-items:center;
                        justify-content:center;background:linear-gradient(135deg,{TCN_RED},#8f1620);
                        box-shadow:0 4px 14px rgba(200,30,40,0.5);">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"
                     stroke-linecap="round" stroke-linejoin="round">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                    <polyline points="14 2 14 8 20 8"/>
                    <line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/>
                </svg>
            </div>
            <div>
                <div style="font-size:1.15rem;font-weight:700;color:white;line-height:1.2;">Generate Analysis</div>
                <div style="font-size:0.72rem;color:#B9C4E0;letter-spacing:0.05em;">
                    Export a full report for {scope} — {len(rdf):,} outage records
                </div>
            </div>
        </div>
        <div style="margin-bottom:0.2rem;">{scope_chips}</div>
    </div>
    """, unsafe_allow_html=True)

    rep_cols = ["Region", "SubRegion_ACC", "Substation", "Equipment", "Voltage_Level",
                "Equipment_Type", "Datetime_Off", "Datetime_On", "Duration_Hours", "Status",
                "Class", "Last_Load_MW", "Event_Indication", "Officer_Interruption", "Officer_Restoration", "Party_Responsible",
                "Weather_Condition", "Remarks"]
    overview = pd.DataFrame({
        "Metric": ["Scope", "Total Outages", "Substations Affected", "Unique Equipment",
                   "Total Duration (hrs)", "Avg Duration (hrs)", "Load Lost (MW)",
                   "Ongoing Outages", "Forced", "Planned", "Emergency"],
        "Value": [
            scope, len(rdf), rdf["Substation"].nunique(), rdf["Equipment"].nunique(),
            round(rdf["Duration_Hours"].sum(), 1),
            round(rdf["Duration_Hours"].mean(), 2) if rdf["Duration_Hours"].notna().any() else 0,
            round(rdf["Last_Load_MW"].sum(), 1), int((rdf["Status"] == "Ongoing").sum()),
            int((rdf["Class"] == "Forced").sum()), int((rdf["Class"] == "Planned").sum()),
            int((rdf["Class"] == "Emergency").sum()),
        ],
    })
    sub_summary = rdf.groupby(["SubRegion_ACC", "Substation"]).agg(
        Outages=("Substation", "size"),
        Total_Hours=("Duration_Hours", "sum"),
        Avg_Hours=("Duration_Hours", "mean"),
        Load_Lost_MW=("Last_Load_MW", "sum"),
        Unique_Equipment=("Equipment", "nunique"),
    ).round(2).reset_index().sort_values("Outages", ascending=False)

    buf = BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        overview.to_excel(writer, sheet_name="Overview", index=False)
        sub_summary.to_excel(writer, sheet_name="Substation Summary", index=False)
        rdf[rep_cols].to_excel(writer, sheet_name="Outage Records", index=False)

    g1, g2, _ = st.columns([1, 1, 2])
    with g1:
        st.download_button(
            "⚡ Generate Excel Report", buf.getvalue(),
            f"TCN_Region_Analysis_{region.replace(' ', '_')}.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            type="primary", use_container_width=True, key="ra_gen_xlsx",
        )
    with g2:
        st.download_button(
            "📄 Download CSV", rdf[rep_cols].to_csv(index=False).encode(),
            f"TCN_Region_Analysis_{region.replace(' ', '_')}.csv", "text/csv",
            use_container_width=True, key="ra_gen_csv",
        )


def show_equipment_analysis(df):
    _eyebrow("Equipment", "#FBEAEA", TCN_RED)
    st.header("Equipment Analysis")

    # ── Drill-down selectors: Region → Sub-Region → Station → Type → Equipment ──
    s1, s2, s3 = st.columns(3)
    with s1:
        region = st.selectbox(
            "Region", ["All Regions"] + sorted(df["Region"].dropna().unique().tolist()),
            key="ea_region")
    edf = df if region == "All Regions" else df[df["Region"] == region]
    with s2:
        subregion = st.selectbox(
            "Sub-Region / ACC", ["All Sub-Regions"] + sorted(edf["SubRegion_ACC"].dropna().unique().tolist()),
            key="ea_subregion")
    if subregion != "All Sub-Regions":
        edf = edf[edf["SubRegion_ACC"] == subregion]
    with s3:
        station = st.selectbox(
            "Station", ["All Stations"] + sorted(edf["Substation"].dropna().unique().tolist()),
            key="ea_station")
    if station != "All Stations":
        edf = edf[edf["Substation"] == station]

    s4, s5 = st.columns(2)
    with s4:
        etype = st.selectbox(
            "Equipment Type", ["All Types"] + sorted(edf["Equipment_Type"].dropna().unique().tolist()),
            key="ea_etype")
    if etype != "All Types":
        edf = edf[edf["Equipment_Type"] == etype]
    with s5:
        equipment = st.selectbox(
            "Equipment", ["All Equipment"] + sorted(edf["Equipment"].dropna().unique().tolist()),
            key="ea_equipment")
    if equipment != "All Equipment":
        edf = edf[edf["Equipment"] == equipment]

    if edf.empty:
        st.info("No records for this selection.")
        return

    kpi_grid([
        kpi_card("Outages", f"{len(edf):,}", icon="bolt", color=TCN_BLUE),
        kpi_card("Unique Equipment", f"{edf['Equipment'].nunique():,}", icon="pulse", color="#346538"),
        kpi_card("Total Downtime", f"{edf['Duration_Hours'].sum():,.1f}", "hrs", icon="clock", color=TCN_RED),
        kpi_card("Load Lost", f"{edf['Last_Load_MW'].sum():,.1f}", "MW", icon="power", color="#956400"),
    ])

    c1, c2 = st.columns(2)
    with c1:
        top = edf.groupby("Equipment").size().sort_values(ascending=False).head(15).reset_index(name="Outages")
        fig = px.bar(top, x="Outages", y="Equipment", orientation="h",
                     title="Most Frequent Equipment Outages",
                     color_discrete_sequence=[TCN_RED])
        fig.update_layout(height=440, yaxis=dict(autorange="reversed"), **TCN_CHART_LAYOUT)
        fig.update_traces(marker_line_width=0, marker_cornerradius=4)
        _style_chart(fig)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        top_dur = edf.groupby("Equipment")["Duration_Hours"].sum().sort_values(ascending=False).head(15).reset_index()
        fig = px.bar(top_dur, x="Duration_Hours", y="Equipment", orientation="h",
                     title="Longest Cumulative Downtime (hrs)",
                     color_discrete_sequence=[TCN_BLUE])
        fig.update_layout(height=440, yaxis=dict(autorange="reversed"), **TCN_CHART_LAYOUT)
        fig.update_traces(marker_line_width=0, marker_cornerradius=4)
        _style_chart(fig)
        st.plotly_chart(fig, use_container_width=True)

    # Repeat offenders
    st.subheader("Repeat Offenders (3+ outages)")
    rep = edf.groupby(["Region", "Substation", "Equipment", "Voltage_Level"]).agg(
        Outages=("Equipment", "size"),
        Total_Hours=("Duration_Hours", "sum"),
        Load_MW=("Last_Load_MW", "sum"),
    ).reset_index()
    rep = rep[rep["Outages"] >= 3].sort_values("Outages", ascending=False)
    if rep.empty:
        st.caption("No equipment with 3 or more outages in the current filter window.")
    else:
        st.dataframe(rep, use_container_width=True, height=320)

    c3, c4, c5 = st.columns(3)
    with c3:
        by_class = edf["Class"].value_counts().reset_index()
        by_class.columns = ["Class", "Count"]
        fig = px.pie(by_class, names="Class", values="Count", hole=0.45,
                     title="Outage Classification", color="Class",
                     color_discrete_map=CLASS_COLORS)
        fig.update_layout(height=380, **TCN_CHART_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)
    with c4:
        by_v = edf.groupby(["Voltage_Level", "Class"]).size().reset_index(name="Count")
        fig = px.bar(by_v, x="Voltage_Level", y="Count", color="Class", barmode="group",
                     title="Voltage Level vs Outage Class", color_discrete_map=CLASS_COLORS)
        fig.update_layout(height=380, **TCN_CHART_LAYOUT)
        fig.update_traces(marker_line_width=0, marker_cornerradius=4)
        _style_chart(fig)
        st.plotly_chart(fig, use_container_width=True)
    with c5:
        hourly = edf.dropna(subset=["Datetime_Off"]).copy()
        hourly["Hour"] = hourly["Datetime_Off"].dt.hour
        by_h = hourly.groupby("Hour").size().reset_index(name="Outages")
        fig = px.bar(by_h, x="Hour", y="Outages", title="Outages by Hour of Day",
                     color_discrete_sequence=[TCN_BLUE])
        fig.update_layout(height=380, **TCN_CHART_LAYOUT)
        fig.update_traces(marker_line_width=0, marker_cornerradius=4)
        _style_chart(fig)
        st.plotly_chart(fig, use_container_width=True)

    if equipment != "All Equipment":
        st.subheader(f"Outage History: {equipment}")
        hist_cols = ["Datetime_Off", "Datetime_On", "Duration_Hours", "Status", "Class",
                     "Last_Load_MW", "Event_Indication", "Officer_Interruption", "Officer_Restoration", "Party_Responsible",
                     "Weather_Condition", "Remarks"]
        st.dataframe(edf.sort_values("Datetime_Off")[hist_cols],
                     use_container_width=True, height=320)

    # ── Generate Analysis panel ──
    scope_chips = ""
    for label, val in [("Region", region), ("Sub-Region", subregion), ("Station", station),
                       ("Type", etype), ("Equipment", equipment)]:
        active = not val.startswith("All")
        chip_bg = "rgba(200,30,40,0.14)" if active else "rgba(255,255,255,0.10)"
        chip_bd = "rgba(224,110,106,0.45)" if active else "rgba(255,255,255,0.16)"
        chip_fg = "#FFD9D6" if active else "#B9C4E0"
        display = val if len(val) <= 42 else val[:40] + "…"
        scope_chips += (
            f'<span style="display:inline-flex;align-items:center;gap:5px;font-size:0.68rem;'
            f'font-weight:600;padding:4px 10px;border-radius:999px;margin:0 6px 6px 0;'
            f'background:{chip_bg};border:1px solid {chip_bd};color:{chip_fg};">'
            f'<span style="opacity:0.6;">{label}</span> {display}</span>'
        )

    st.markdown(f"""
    <div style="position:relative;margin-top:1.6rem;padding:1.5rem 1.6rem 1.2rem 1.6rem;
                border-radius:18px;overflow:hidden;
                background:linear-gradient(135deg, #12224a 0%, #1e3a7a 55%, #35204a 130%);
                box-shadow:0 12px 36px rgba(14,28,61,0.35), inset 0 1px 0 rgba(255,255,255,0.10);">
        <div style="position:absolute;top:-60px;right:-40px;width:220px;height:220px;border-radius:50%;
                    background:radial-gradient(circle, rgba(200,30,40,0.35), transparent 70%);"></div>
        <div style="display:flex;align-items:center;gap:0.9rem;margin-bottom:0.8rem;">
            <div style="width:42px;height:42px;border-radius:11px;display:flex;align-items:center;
                        justify-content:center;background:linear-gradient(135deg,{TCN_RED},#8f1620);
                        box-shadow:0 4px 14px rgba(200,30,40,0.5);">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"
                     stroke-linecap="round" stroke-linejoin="round">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                    <polyline points="14 2 14 8 20 8"/>
                    <line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/>
                </svg>
            </div>
            <div>
                <div style="font-size:1.15rem;font-weight:700;color:white;line-height:1.2;">Generate Analysis</div>
                <div style="font-size:0.72rem;color:#B9C4E0;letter-spacing:0.05em;">
                    Export a full report for the current selection — {len(edf):,} outage records
                </div>
            </div>
        </div>
        <div style="margin-bottom:0.2rem;">{scope_chips}</div>
    </div>
    """, unsafe_allow_html=True)

    # Build the report workbook in memory
    rep_cols = ["Region", "SubRegion_ACC", "Substation", "Equipment", "Voltage_Level",
                "Equipment_Type", "Datetime_Off", "Datetime_On", "Duration_Hours", "Status",
                "Class", "Last_Load_MW", "Event_Indication", "Officer_Interruption", "Officer_Restoration", "Party_Responsible",
                "Weather_Condition", "Remarks"]
    overview = pd.DataFrame({
        "Metric": ["Scope", "Total Outages", "Unique Equipment", "Total Downtime (hrs)",
                   "Avg Duration (hrs)", "Load Lost (MW)", "Ongoing Outages",
                   "Forced", "Planned", "Emergency"],
        "Value": [
            " / ".join(v for v in [region, subregion, station, etype, equipment] if not v.startswith("All")) or "All data",
            len(edf), edf["Equipment"].nunique(), round(edf["Duration_Hours"].sum(), 1),
            round(edf["Duration_Hours"].mean(), 2) if edf["Duration_Hours"].notna().any() else 0,
            round(edf["Last_Load_MW"].sum(), 1), int((edf["Status"] == "Ongoing").sum()),
            int((edf["Class"] == "Forced").sum()), int((edf["Class"] == "Planned").sum()),
            int((edf["Class"] == "Emergency").sum()),
        ],
    })
    eq_summary = edf.groupby(["Region", "Substation", "Equipment", "Voltage_Level", "Equipment_Type"]).agg(
        Outages=("Equipment", "size"),
        Total_Hours=("Duration_Hours", "sum"),
        Avg_Hours=("Duration_Hours", "mean"),
        Load_Lost_MW=("Last_Load_MW", "sum"),
    ).round(2).reset_index().sort_values("Outages", ascending=False)

    buf = BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        overview.to_excel(writer, sheet_name="Overview", index=False)
        eq_summary.to_excel(writer, sheet_name="Equipment Summary", index=False)
        edf[rep_cols].to_excel(writer, sheet_name="Outage Records", index=False)

    g1, g2, _ = st.columns([1, 1, 2])
    with g1:
        st.download_button(
            "⚡ Generate Excel Report", buf.getvalue(),
            "TCN_Equipment_Analysis.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            type="primary", use_container_width=True, key="ea_gen_xlsx",
        )
    with g2:
        st.download_button(
            "📄 Download CSV", edf[rep_cols].to_csv(index=False).encode(),
            "TCN_Equipment_Analysis.csv", "text/csv",
            use_container_width=True, key="ea_gen_csv",
        )


def show_hierarchy(df):
    _eyebrow("Network", "#F3EDE1", "#956400")
    st.header("Network Hierarchy")
    h = load_hierarchy()
    if h.empty:
        st.warning("Hierarchy file not available.")
        return

    region = st.selectbox("Region", sorted(h["Region"].dropna().unique()))
    hr = h[h["Region"] == region]

    counts = df[df["Region"].str.title() == region.title()]
    outage_by_sub = counts.groupby("Substation").size()

    kpi_grid([
        kpi_card("Sub-Regions", f"{hr['Sub-Region'].nunique()}", icon="chart", color=TCN_BLUE),
        kpi_card("Transmission Stations", f"{hr['Transmission Station'].nunique()}", icon="tower", color=TCN_RED),
        kpi_card("Sub-Stations", f"{hr['Sub-Station'].nunique()}", icon="building", color="#346538"),
        kpi_card("Outages in Region", f"{len(counts):,}", icon="bolt", color="#956400"),
    ])

    for subregion in sorted(hr["Sub-Region"].dropna().unique()):
        sr = hr[hr["Sub-Region"] == subregion]
        with st.expander(f"**{subregion}** — {sr['Transmission Station'].nunique()} stations, {sr['Sub-Station'].nunique()} substations"):
            for ts in sorted(sr["Transmission Station"].dropna().unique()):
                subs = sr[sr["Transmission Station"] == ts]["Sub-Station"].dropna().tolist()
                n_out = int(outage_by_sub.filter(like=ts.split()[0]).sum()) if len(ts.split()) else 0
                st.markdown(f"**⚡ {ts}**" + (f" · `{n_out} outages`" if n_out else ""))
                for s in subs:
                    if s and s.lower() != "nan":
                        st.markdown(f"&nbsp;&nbsp;&nbsp;└ {s}")


def show_report_outage(user):
    _eyebrow("Entry", "#E8EEF7", TCN_BLUE)
    st.header("Report Outage")
    st.caption("Log a new 330kV / 132kV equipment outage. It is appended to the compiled dataset immediately.")

    full = load_data()
    catalog = load_catalog()
    use_catalog = not catalog.empty
    regions = sorted(catalog["Region"].unique()) if use_catalog else sorted(full["Region"].dropna().unique())

    # ── Location & equipment selectors (reactive, cascading, catalog-driven) ──
    c1, c2, c3 = st.columns(3)
    with c1:
        if user.get("region"):
            region = st.selectbox("Region", [user["region"]], disabled=True)
        else:
            region = st.selectbox("Region", regions)
        rcat = catalog[catalog["Region"] == region] if use_catalog else pd.DataFrame()
        if not rcat.empty:
            subregions = sorted(rcat["SubRegion"].dropna().unique())
        else:
            subregions = sorted(full.loc[full["Region"] == region, "SubRegion_ACC"].dropna().unique())
        subregion = st.selectbox("Sub-Region / ACC", subregions + ["Other…"])
        subregion_other = ""
        if subregion == "Other…":
            subregion_other = st.text_input("Specify Sub-Region *")
    with c2:
        if not rcat.empty:
            if subregion != "Other…":
                known_subs = sorted(rcat.loc[rcat["SubRegion"] == subregion, "Substation"].unique())
            else:
                known_subs = sorted(rcat["Substation"].unique())
        else:
            known_subs = sorted(full.loc[full["Region"] == region, "Substation"].dropna().unique())
        substation = st.selectbox("Substation", known_subs + ["Other…"])
        substation_other = ""
        if substation == "Other…":
            substation_other = st.text_input("Specify Substation *")
    with c3:
        equip_type = st.selectbox(
            "Equipment Type",
            ["Line", "Transformer", "Feeder", "Reactor", "Bus", "Other"],
        )

    # Equipment options: catalog first (station → region), then history, else manual
    equip_options, scope_note = [], ""
    if substation != "Other…" and equip_type != "Other":
        if use_catalog and equip_type in ("Line", "Transformer"):
            scope = catalog[(catalog["Substation"] == substation) & (catalog["Equipment_Type"] == equip_type)]
            if not scope.empty:
                scope_note = f"{equip_type}s registered at {substation}."
            else:
                scope = catalog[(catalog["Region"] == region) & (catalog["Equipment_Type"] == equip_type)]
                if not scope.empty:
                    scope_note = f"No {equip_type.lower()}s registered at {substation} — showing all {equip_type.lower()}s in {region}."
            equip_options = sorted(scope["Equipment"].unique().tolist())
        if not equip_options:
            hist = full[(full["Region"] == region) & (full["Equipment_Type"] == equip_type)]
            if not hist.empty:
                equip_options = sorted(hist["Equipment"].dropna().unique().tolist())
                scope_note = f"{equip_type}s previously recorded in {region} outage history."

    equipment_choice = st.selectbox(
        "Equipment *",
        equip_options + ["Other (type manually)…"],
        help=scope_note or None,
    )
    if scope_note:
        st.caption(scope_note)
    equipment_other = ""
    if equipment_choice == "Other (type manually)…":
        equipment_other = st.text_input(
            "Specify Equipment *",
            placeholder="e.g. 60MVA 132/33kV Transformer TR1 (3KNE-TR1)",
        )
    equipment = equipment_other.strip() if equipment_choice == "Other (type manually)…" else equipment_choice

    st.divider()

    # ── Remaining details ──
    c4, c5, c6 = st.columns(3)
    with c4:
        outage_class = st.selectbox("Class", ["Forced", "Emergency", "Planned"])
    with c5:
        load_mw = st.number_input("Last Load (MW)", min_value=0.0, step=0.1, format="%.1f")
    with c6:
        weather = st.selectbox("Weather Condition", ["Clear", "Rainy", "Windy", "Drizzling", "Cloudy"])

    c7, c8 = st.columns(2)
    with c7:
        st.markdown("**Time Off**")
        date_off = st.date_input("Date Off")
        t1, t2 = st.columns(2)
        hour_off = t1.number_input("Hour Off", 0, 23, 0)
        minute_off = t2.number_input("Minute Off", 0, 59, 0)
        officer_off = st.text_input("Officer (Interruption)",
                                    placeholder="Officer on duty at interruption")
    with c8:
        st.markdown("**Time On** *(leave unchecked if still out)*")
        restored = st.checkbox("Equipment restored")
        date_on = st.date_input("Date On", disabled=not restored)
        t3, t4 = st.columns(2)
        hour_on = t3.number_input("Hour On", 0, 23, 0, disabled=not restored)
        minute_on = t4.number_input("Minute On", 0, 59, 0, disabled=not restored)
        officer_on = st.text_input("Officer (Restoration)",
                                   placeholder="Officer on duty at restoration",
                                   disabled=not restored)

    c9, c10 = st.columns(2)
    with c9:
        event = st.text_input("Event Indication", placeholder="e.g. Distance Protection, Frequency Control")
    with c10:
        party = st.selectbox("Party Responsible", ["TCN", "Disco", "Generation Company", "Weather", "Vandalism"])
    remarks = st.text_area("Remarks", placeholder="Describe the event, protection operations, restoration steps…")

    if st.button("Submit Outage Report", type="primary"):
        if not equipment:
            st.error("Equipment is required — pick one from the list or type it under 'Other'.")
        elif subregion == "Other…" and not subregion_other.strip():
            st.error("Please specify the Sub-Region.")
        elif substation == "Other…" and not substation_other.strip():
            st.error("Please specify the Substation.")
        else:
            duration = None
            d_on = h_on = m_on = None
            if restored:
                dt_off = pd.Timestamp(date_off) + timedelta(hours=int(hour_off), minutes=int(minute_off))
                dt_on = pd.Timestamp(date_on) + timedelta(hours=int(hour_on), minutes=int(minute_on))
                if dt_on < dt_off:
                    st.error("Restoration time is before the outage time.")
                    return
                mins = int((dt_on - dt_off).total_seconds() // 60)
                duration = f"{mins // 60}:{mins % 60:02d}"
                d_on = date_on.strftime("%d/%m/%Y")
                h_on, m_on = int(hour_on), int(minute_on)
            row = {
                "Region": region,
                "SubRegion_ACC": subregion_other.strip() if subregion == "Other…" else subregion,
                "Substation": substation_other.strip() if substation == "Other…" else substation,
                "Equipment": equipment.strip(),
                "Date_Off": date_off.strftime("%d/%m/%Y"),
                "Hour_Off": int(hour_off),
                "Minute_Off": int(minute_off),
                "Date_On": d_on,
                "Hour_On": h_on,
                "Minute_On": m_on,
                "Duration": duration,
                "Class": outage_class,
                "Last_Load_MW": load_mw if load_mw > 0 else None,
                "Event_Indication": event.strip() or None,
                "Officer_Interruption": officer_off.strip() or None,
                "Officer_Restoration": officer_on.strip() if restored else None,
                "Party_Responsible": party,
                "Weather_Condition": weather,
                "Remarks": remarks.strip() or None,
            }
            try:
                existing = pd.read_excel(DATA_FILE, sheet_name=0)
                combined = pd.concat([existing, pd.DataFrame([row])], ignore_index=True)
                with pd.ExcelWriter(DATA_FILE, engine="openpyxl") as writer:
                    combined.to_excel(writer, sheet_name="Outages", index=False)
                load_data.clear()
                st.success(f"Outage recorded for {row['Equipment']} at {row['Substation']} ({region}).")
            except PermissionError:
                st.error("Data file is open in Excel — close it and submit again.")
            except Exception as exc:
                st.error(f"Could not save record: {exc}")


def show_export(df):
    _eyebrow("Export", "#F3EDE1", "#956400")
    st.header("Export Reports")

    e1, e2 = st.columns([1.2, 1])
    with e1:
        dmin = df["Datetime_Off"].min()
        dmax = df["Datetime_Off"].max()
        export_range = st.date_input(
            "📅 Export Date Range",
            value=(dmin.date(), dmax.date()) if pd.notna(dmin) else (),
            key="exp_date",
        )
    with e2:
        fmt = st.radio("Export Format", ["Excel (.xlsx)", "CSV (.csv)"], horizontal=True)

    if isinstance(export_range, tuple) and len(export_range) == 2:
        e_start, e_end = export_range
        df = df[
            (df["Datetime_Off"] >= pd.Timestamp(e_start))
            & (df["Datetime_Off"] < pd.Timestamp(e_end) + timedelta(days=1))
        ]
    st.caption(f"{len(df):,} records in the selected period")
    if df.empty:
        st.info("No records in the selected date range.")
        return
    cols = ["Region", "SubRegion_ACC", "Substation", "Equipment", "Voltage_Level",
            "Equipment_Type", "Datetime_Off", "Datetime_On", "Duration_Hours", "Status",
            "Class", "Last_Load_MW", "Event_Indication", "Officer_Interruption", "Officer_Restoration", "Party_Responsible",
            "Weather_Condition", "Remarks"]
    out = df[cols]

    if fmt.startswith("Excel"):
        buf = BytesIO()
        with pd.ExcelWriter(buf, engine="openpyxl") as writer:
            out.to_excel(writer, sheet_name="Outages", index=False)
            summary = df.groupby("Region").agg(
                Total_Outages=("Region", "size"),
                Total_Duration_Hrs=("Duration_Hours", "sum"),
                Avg_Duration_Hrs=("Duration_Hours", "mean"),
                Total_Load_Lost_MW=("Last_Load_MW", "sum"),
                Unique_Substations=("Substation", "nunique"),
                Unique_Equipment=("Equipment", "nunique"),
            ).round(2).reset_index()
            summary.to_excel(writer, sheet_name="Summary", index=False)
        st.download_button("Download Excel Report", buf.getvalue(),
                           "TCN_Outage_Report.xlsx",
                           "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                           type="primary")
    else:
        st.download_button("Download CSV", out.to_csv(index=False).encode(),
                           "TCN_Outage_Report.csv", "text/csv", type="primary")

    st.subheader("Summary Statistics")
    summary = df.groupby("Region").agg(
        Total_Outages=("Region", "size"),
        Total_Duration_Hrs=("Duration_Hours", "sum"),
        Avg_Duration_Hrs=("Duration_Hours", "mean"),
        Total_Load_Lost_MW=("Last_Load_MW", "sum"),
        Unique_Substations=("Substation", "nunique"),
        Unique_Equipment=("Equipment", "nunique"),
    ).round(2).sort_values("Total_Outages", ascending=False)
    st.dataframe(summary, use_container_width=True)


def show_upload():
    _eyebrow("Admin", "#FBEAEA", TCN_RED)
    st.header("Upload Data")
    st.caption(
        "Replace the compiled outage dataset. The file must contain the standard columns: "
        "Region, SubRegion_ACC, Substation, Equipment, Date_Off, Hour_Off, Minute_Off, "
        "Date_On, Hour_On, Minute_On, Duration, Class, Last_Load_MW, Event_Indication, "
        "Party_Responsible, Weather_Condition, Remarks"
    )
    up = st.file_uploader("Upload compiled outages workbook (.xlsx)", type=["xlsx"])
    if up is not None:
        try:
            new = pd.read_excel(up, sheet_name=0)
            new.columns = [c.strip() for c in new.columns]
            required = {"Region", "Substation", "Equipment", "Date_Off", "Class"}
            missing = required - set(new.columns)
            if missing:
                st.error(f"Missing required columns: {', '.join(sorted(missing))}")
                return
            st.dataframe(new.head(10), use_container_width=True)
            st.caption(f"{len(new):,} rows detected")
            mode = st.radio("Import mode", ["Replace existing data", "Append to existing data"], horizontal=True)
            if st.button("Confirm Import", type="primary"):
                if mode.startswith("Append"):
                    existing = pd.read_excel(DATA_FILE, sheet_name=0)
                    combined = pd.concat([existing, new], ignore_index=True)
                else:
                    combined = new
                with pd.ExcelWriter(DATA_FILE, engine="openpyxl") as writer:
                    combined.to_excel(writer, sheet_name="Outages", index=False)
                load_data.clear()
                st.success(f"Imported {len(new):,} rows ({mode.split()[0].lower()}). Data reloaded.")
                st.rerun()
        except Exception as exc:
            st.error(f"Could not read workbook: {exc}")


def show_users(user):
    _eyebrow("Admin", "#FBEAEA", TCN_RED)
    st.header("User Management")
    users = load_users()

    rows = [{"Username": k, "Name": v["name"], "Role": v["role"], "Region": v["region"] or "All"}
            for k, v in users.items()]
    st.dataframe(pd.DataFrame(rows), use_container_width=True)

    st.subheader("Add User")
    with st.form("add_user"):
        c1, c2 = st.columns(2)
        with c1:
            uname = st.text_input("Username")
            pw = st.text_input("Password", type="password")
        with c2:
            name = st.text_input("Full Name")
            role = st.selectbox("Role", ["operator", "admin"])
        region = st.selectbox("Region scope (operators)", ["All"] + sorted(load_data()["Region"].dropna().unique().tolist()))
        if st.form_submit_button("Create User", type="primary"):
            if not uname or not pw:
                st.error("Username and password are required.")
            elif uname in users:
                st.error("Username already exists.")
            else:
                users[uname.strip()] = {
                    "password": _hash(pw), "role": role, "name": name or uname,
                    "region": None if region == "All" or role == "admin" else region,
                }
                save_users(users)
                st.success(f"User '{uname}' created.")
                st.rerun()

    st.subheader("Delete User")
    deletable = [u for u in users if u != user["username"]]
    if deletable:
        target = st.selectbox("Select user", deletable)
        if st.button("Delete User"):
            users.pop(target, None)
            save_users(users)
            st.success(f"User '{target}' deleted.")
            st.rerun()


# ──────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────
def main():
    inject_css()

    if "user" not in st.session_state:
        login_page()
        return

    user = st.session_state.user
    logo64 = _b64(LOGO)
    logo_html = (
        f'<div style="width:52px;height:52px;border-radius:13px;display:flex;align-items:center;'
        f'justify-content:center;background:linear-gradient(135deg,#E8EEF7,#FBEAEA);'
        f'border:1px solid rgba(55,53,47,0.08);">'
        f'<img src="data:image/png;base64,{logo64}" width="36"></div>'
        if logo64 else ""
    )
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:0.9rem;margin-bottom:0.4rem;">
        {logo_html}
        <div>
            <div style="font-size:1.35rem;font-weight:700;color:var(--text-primary);">TCN Grid Outage Manager</div>
            <div style="font-size:0.68rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:var(--text-tertiary);">
                330kV · 132kV Equipment Outages · Analytics · Reporting
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not DATA_FILE.exists():
        st.error(f"Data file not found: {DATA_FILE.name}. Upload it via the admin Upload tab or place it in the app folder.")
        return

    df = load_data()
    if user.get("region"):
        df = df[df["Region"] == user["region"]]

    filtered = sidebar_filters(df, user)

    tab_names = ["⚡ Dashboard", "🗂️ Records", "🌍 Region Analysis", "🔧 Equipment Analysis",
                 "📝 Report Outage", "🗼 Network Hierarchy", "📤 Export"]
    if user["role"] == "admin":
        tab_names += ["📁 Upload Data", "👥 Users"]
    tabs = st.tabs(tab_names)

    with tabs[0]:
        show_dashboard(filtered, user)
    with tabs[1]:
        show_records(filtered)
    with tabs[2]:
        show_region_analysis(filtered)
    with tabs[3]:
        show_equipment_analysis(filtered)
    with tabs[4]:
        show_report_outage(user)
    with tabs[5]:
        show_hierarchy(filtered)
    with tabs[6]:
        show_export(filtered)
    if user["role"] == "admin":
        with tabs[7]:
            show_upload()
        with tabs[8]:
            show_users(user)


if __name__ == "__main__":
    main()
