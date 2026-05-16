import os
import time
import streamlit as st
import streamlit.components.v1 as components
import requests
import pandas as pd
from datetime import datetime, timedelta, timezone

st.set_page_config(
    page_title="People's Capital — Signal Intelligence",
    page_icon="🏛️",
    layout="wide",
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
        --bg: #FFFFFF;
        --surface: #F5F4EF;
        --surface-2: #EAE7DA;
        --text: #141413;
        --text-secondary: #5A5A57;
        --accent: #1D9E75;
        --accent-soft: #E8F4EE;
        --accent-deep: #167C5C;
        --border: #E0DCCB;
        --hairline: rgba(20, 20, 19, 0.08);
        --warn-bg: #FFF8E6;
        --warn-border: #E8C97D;
        --warn-text: #6B4F0E;
    }

    * { font-family: 'Inter', sans-serif !important; }

    .stApp { background: var(--bg) !important; color: var(--text) !important; }
    .main .block-container {
        background: var(--bg) !important;
        padding: 1.25rem 2rem 2rem 2rem !important;
        max-width: 1400px !important;
    }

    /* ── Sidebar (warm gray, light text) ─────────────────────────────── */
    [data-testid="stSidebar"] {
        background: var(--surface) !important;
        border-right: 1px solid var(--hairline) !important;
    }
    [data-testid="stSidebar"] * { color: var(--text) !important; }
    [data-testid="stSidebar"] h2 {
        font-size: 0.72rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.1em !important;
        color: var(--text-secondary) !important;
        font-weight: 600 !important;
        margin-top: 0.25rem !important;
    }
    [data-testid="stSidebar"] label {
        font-size: 0.78rem !important;
        font-weight: 500 !important;
        color: var(--text) !important;
        letter-spacing: 0.005em !important;
    }
    /* Sidebar radio + multiselect breathing room */
    [data-testid="stSidebar"] [role="radiogroup"] { gap: 0.4rem !important; }
    [data-testid="stSidebar"] .stRadio > div { padding: 0.15rem 0 !important; }
    [data-testid="stSidebar"] [data-baseweb="select"] {
        background: var(--bg) !important;
        border-radius: 6px !important;
    }

    /* ── Hero header ─────────────────────────────────────────────────── */
    .hero-header {
        padding: 1rem 0 1rem 0;
        margin-bottom: 0.5rem;
    }
    .hero-title {
        font-size: 1.5rem !important;
        font-weight: 800 !important;
        color: var(--text) !important;
        letter-spacing: -0.02em !important;
        line-height: 1.1 !important;
        margin: 0 !important;
    }
    .hero-title span { color: var(--accent) !important; }
    .hero-subtitle {
        font-size: 0.7rem !important;
        color: var(--text-secondary) !important;
        margin-top: 0.35rem !important;
        letter-spacing: 0.1em !important;
        text-transform: uppercase !important;
        font-weight: 500 !important;
    }

    /* ── Trust bar ───────────────────────────────────────────────────── */
    .trust-bar {
        display: flex;
        flex-wrap: wrap;
        gap: 0.45rem;
        padding: 0.5rem 0 1rem 0;
        margin-bottom: 0.75rem;
        border-bottom: 1px solid var(--hairline);
    }
    .trust-chip {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        padding: 0.32rem 0.7rem;
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 999px;
        font-size: 0.72rem;
        font-weight: 500;
        color: var(--text);
        letter-spacing: 0.005em;
    }
    .trust-chip::before {
        content: "✓";
        color: var(--accent);
        font-weight: 700;
        font-size: 0.78rem;
    }

    /* ── Spirit 2.0 panel (compressed) ───────────────────────────────── */
    .spirit-panel {
        background: var(--surface) !important;
        border: 1px solid var(--hairline) !important;
        border-radius: 8px !important;
        padding: 0.85rem 1.1rem !important;
        margin-bottom: 1rem !important;
        position: relative !important;
        overflow: hidden !important;
    }
    .spirit-panel::before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important; left: 0 !important; right: 0 !important;
        height: 2px !important;
        background: var(--accent) !important;
    }
    .spirit-label {
        font-size: 0.62rem !important;
        font-weight: 700 !important;
        color: var(--accent) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.12em !important;
        margin-bottom: 0.55rem !important;
        display: flex !important;
        align-items: center !important;
        gap: 6px !important;
    }
    .spirit-grid {
        display: grid !important;
        grid-template-columns: repeat(3, 1fr) !important;
        gap: 0.75rem !important;
        margin-bottom: 0.35rem !important;
    }
    .kpi-value {
        font-size: 1.25rem !important;
        font-weight: 700 !important;
        color: var(--text) !important;
        letter-spacing: -0.015em !important;
        line-height: 1.1 !important;
    }
    .kpi-label {
        font-size: 0.62rem !important;
        color: var(--text-secondary) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        font-weight: 500 !important;
        margin-top: 2px !important;
    }
    .kpi-audited {
        font-size: 1rem !important;
        font-weight: 600 !important;
        color: var(--text-secondary) !important;
    }
    .progress-container {
        background: var(--surface-2) !important;
        border-radius: 3px !important;
        height: 4px !important;
        margin: 0.55rem 0 0.25rem 0 !important;
        overflow: hidden !important;
    }
    .progress-fill {
        background: var(--accent) !important;
        height: 100% !important;
        border-radius: 3px !important;
        width: 19.3% !important;
    }
    .progress-label {
        font-size: 0.68rem !important;
        color: var(--accent) !important;
        font-weight: 600 !important;
    }
    .spirit-tagline {
        margin-top: 0.55rem;
        padding-top: 0.5rem;
        border-top: 1px solid var(--hairline);
        font-size: 0.72rem;
        color: var(--text-secondary);
        line-height: 1.45;
    }
    .spirit-tagline strong {
        color: var(--accent);
        font-weight: 600;
    }

    /* ── Section heads (LIVE CASES / RECENT PRECEDENTS) ─────────────── */
    .section-eyebrow {
        font-size: 0.65rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.12em !important;
        margin: 0 0 0.4rem 0 !important;
    }
    .section-eyebrow.teal { color: var(--accent) !important; }
    .section-eyebrow.gray { color: var(--text-secondary) !important; }
    .section-title {
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        color: var(--text) !important;
        letter-spacing: -0.015em !important;
        margin: 0 0 0.2rem 0 !important;
    }
    .section-sub {
        font-size: 0.78rem !important;
        color: var(--text-secondary) !important;
        margin: 0 0 1rem 0 !important;
    }
    .section-sub em { font-style: italic; }

    /* ── Live Case cards ─────────────────────────────────────────────── */
    .live-case-card {
        background: var(--surface) !important;
        border: 1px solid var(--hairline) !important;
        border-left: 3px solid var(--accent) !important;
        border-radius: 6px !important;
        padding: 0.9rem 1.1rem !important;
        margin-bottom: 0.5rem !important;
    }
    .lc-row {
        display: flex !important;
        align-items: center !important;
        gap: 1rem !important;
    }
    .lc-rank {
        font-size: 1.6rem !important;
        font-weight: 800 !important;
        color: var(--accent) !important;
        letter-spacing: -0.04em !important;
        line-height: 1 !important;
        min-width: 1.4rem !important;
        text-align: center !important;
    }
    .lc-emoji {
        font-size: 1.7rem !important;
        line-height: 1 !important;
    }
    .lc-title { flex: 1 !important; }
    .lc-brand {
        font-size: 1.0rem !important;
        font-weight: 700 !important;
        color: var(--text) !important;
        letter-spacing: -0.01em !important;
        line-height: 1.2 !important;
    }
    .lc-meta {
        font-size: 0.7rem !important;
        color: var(--text-secondary) !important;
        margin-top: 0.2rem !important;
        letter-spacing: 0.005em !important;
    }
    .lc-meta .pipe { color: var(--border); margin: 0 0.4rem; }
    .lc-score {
        display: flex !important;
        align-items: baseline !important;
        gap: 0.15rem !important;
    }
    .lc-score-num {
        font-size: 1.9rem !important;
        font-weight: 800 !important;
        color: var(--accent) !important;
        letter-spacing: -0.035em !important;
        line-height: 1 !important;
    }
    .lc-score-label {
        font-size: 0.75rem !important;
        color: var(--text-secondary) !important;
    }

    /* ── Feed section heading ────────────────────────────────────────── */
    .feed-header {
        font-size: 1rem !important;
        font-weight: 700 !important;
        color: var(--text) !important;
        letter-spacing: -0.015em !important;
        margin-bottom: 0.15rem !important;
    }

    /* ── Status caption / refreshed marker ───────────────────────────── */
    [data-testid="stCaptionContainer"] {
        color: var(--text-secondary) !important;
        font-size: 0.72rem !important;
    }
    [data-testid="stCaptionContainer"] strong {
        color: var(--text) !important;
        font-weight: 600 !important;
    }

    /* ── PE warning banner (recolored to amber/parchment) ────────────── */
    .pe-banner {
        background: var(--warn-bg) !important;
        border: 1px solid var(--warn-border) !important;
        border-radius: 6px !important;
        padding: 0.65rem 0.95rem !important;
        margin: 0.5rem 0 0.85rem 0 !important;
        font-size: 0.76rem !important;
        color: var(--warn-text) !important;
        line-height: 1.5 !important;
    }
    .pe-banner strong { color: var(--warn-text) !important; font-weight: 700 !important; }

    /* ── Urgency alert (founder-alert / new-filing) ──────────────────── */
    .urgency-alert {
        background: var(--accent-soft);
        border: 1px solid var(--accent);
        border-left: 4px solid var(--accent);
        border-radius: 6px;
        padding: 0.8rem 1rem;
        margin: 0.5rem 0 0.9rem 0;
        font-size: 0.8rem;
        color: var(--text);
        line-height: 1.5;
    }
    .urgency-alert .ua-title {
        font-size: 0.7rem;
        font-weight: 700;
        color: var(--accent-deep);
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.3rem;
        display: block;
    }
    .urgency-alert strong { color: var(--accent-deep); }
    .urgency-alert em { color: var(--text-secondary); font-style: italic; }

    /* ── DataFrame (tighter rows, hairline borders, hover) ───────────── */
    [data-testid="stDataFrame"] {
        border: 1px solid var(--hairline) !important;
        border-radius: 6px !important;
        overflow: hidden !important;
    }
    /* Streamlit's dataframe uses a glide-data-grid canvas — limited CSS
       hooks. We style the wrapper and rely on Streamlit defaults inside. */
    [data-testid="stDataFrame"] [data-testid="stDataFrameResizable"] {
        border: none !important;
    }

    /* Hide the glide-data-grid column-header menu.
       DOM inspection on Streamlit 1.57.0 revealed the menu portal uses
       these Emotion-generated hash classes:
         - .st-emotion-cache-n0nmb5  → outer container
         - .st-emotion-cache-qu02y9  → menu items
         - .st-emotion-cache-hffo7r  → inner labels
       The Emotion `e1gmp2ct*` suffix is per-component-instance and stable
       within a Streamlit version. Hashes will change on Streamlit upgrades;
       re-inspect the DOM and refresh these selectors if so.

       NOT using broader selectors like body > [role="menu"] because the
       sidebar dropdowns (radio, pills) also use role="menuitem" and would
       break. The hash classes are unique to this menu. */
    .st-emotion-cache-n0nmb5,
    .st-emotion-cache-qu02y9,
    .st-emotion-cache-hffo7r {
        display: none !important;
        visibility: hidden !important;
        pointer-events: none !important;
    }

    /* Also kill any button inside the dataframe wrapper — defensive, may
       catch the trigger icon if it's an HTML button in some versions. */
    [data-testid="stDataFrame"] button,
    [data-testid="stDataFrame"] [role="button"] {
        display: none !important;
    }
    /* Preserve row-selection input if Streamlit uses checkboxes internally. */
    [data-testid="stDataFrame"] input[type="checkbox"] {
        display: block !important;
        pointer-events: auto !important;
    }

    /* Hide broken Material Symbols icon glyphs on expander headers.
       Our universal Inter font rule blocks the icon font, so the chevron
       renders as raw text ("arrow_right", "keyboard_double_arrow_down").
       The icon span's class hash varies across Streamlit versions, so
       targeting by class is fragile. Instead: paint all summary text
       transparent, then restore visibility only on the label container
       (data-testid="stMarkdownContainer"). Class-agnostic, version-safe. */
    [data-testid="stExpander"] summary,
    [data-testid="stExpander"] summary *,
    [data-testid="stExpander"] details > summary,
    [data-testid="stExpander"] details > summary * {
        color: transparent !important;
    }
    [data-testid="stExpander"] summary [data-testid="stMarkdownContainer"],
    [data-testid="stExpander"] summary [data-testid="stMarkdownContainer"] *,
    [data-testid="stExpander"] details > summary [data-testid="stMarkdownContainer"],
    [data-testid="stExpander"] details > summary [data-testid="stMarkdownContainer"] * {
        color: var(--text) !important;
        font-weight: 700 !important;
    }

    /* Hide the broken sidebar-collapse icon text. Streamlit's sidebar
       collapse button uses a Material Symbols Rounded glyph; our
       universal Inter rule prevents the icon font from rendering, so
       "keyboard_double_arrow_left" displays as raw text overflowing
       the 1.5rem container. color: transparent on the icon span keeps
       the button clickable while hiding the glyph text. */
    [class*="emotion-cache-12bp31y"],
    [data-testid="stSidebarCollapseButton"] span,
    [data-testid="stSidebarCollapsedControl"] span {
        color: transparent !important;
    }

    /* ── Buttons ─────────────────────────────────────────────────────── */
    .stButton > button {
        background: var(--bg) !important;
        color: var(--text) !important;
        border: 1px solid var(--border) !important;
        border-radius: 6px !important;
        font-size: 0.78rem !important;
        font-weight: 500 !important;
        padding: 0.35rem 0.85rem !important;
        transition: all 0.15s ease !important;
    }
    .stButton > button:hover {
        background: var(--accent-soft) !important;
        border-color: var(--accent) !important;
        color: var(--accent-deep) !important;
    }
    .stButton > button[kind="primary"] {
        background: var(--accent) !important;
        color: white !important;
        border-color: var(--accent) !important;
    }

    /* ── Live pulse dot (recolored teal) ─────────────────────────────── */
    .live-dot {
        display: inline-block !important;
        width: 7px !important;
        height: 7px !important;
        background: var(--accent) !important;
        border-radius: 50% !important;
        animation: pulse 2s infinite !important;
    }
    @keyframes pulse {
        0%   { opacity: 1; transform: scale(1); }
        50%  { opacity: 0.5; transform: scale(1.2); }
        100% { opacity: 1; transform: scale(1); }
    }

    /* ── Footer ──────────────────────────────────────────────────────── */
    .footer-text {
        font-size: 0.7rem !important;
        color: var(--text-secondary) !important;
        text-align: center !important;
        padding: 1.5rem 0 0.5rem 0 !important;
        border-top: 1px solid var(--hairline) !important;
        margin-top: 2rem !important;
    }
    .footer-text a { color: var(--text-secondary) !important; text-decoration: none !important; }

    /* ── Hide streamlit chrome ───────────────────────────────────────── */
    #MainMenu { visibility: hidden !important; }
    footer { visibility: hidden !important; }
    header { visibility: hidden !important; }
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: var(--bg); }
    ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ─── Constants ────────────────────────────────────────────────────────────────

SPIRIT_STATS = {
    "Total Pledged": "$337M",
    "Total Pledgers": "371,552",
    "Average Pledge": "$907",
    "Audited Pledged": "$214M",
    "Audited Pledgers": "247,511",
    "Target Raise": "$1.75B",
}

PLEDGED_AMOUNT = 337
TARGET_AMOUNT = 1750

COMMUNITY_KEYWORDS = [
    "airline", "air", "airways", "market", "grocery", "store", "food", "cafe",
    "coffee", "restaurant", "news", "media", "newspaper", "magazine", "radio",
    "station", "sports", "gym", "fitness", "club", "hotel", "theater", "theatre",
    "cinema", "farm", "brewery", "bank", "credit", "union", "community", "local",
    "regional",
]

OPPORTUNITY_TYPES = {
    "🍕 Food/Restaurant": ["restaurant", "food", "lobster", "pizza", "burger", "grill", "cafe", "coffee", "kitchen", "bakery", "diner", "krystal", "friendly", "rubio"],
    "🛒 Retail": ["retail", "store", "shop", "mart", "bath", "beyond", "joann", "party", "city", "lots", "tuesday", "morning", "pier", "christmas", "tree", "tupperware", "express", "brooks", "bridal"],
    "📰 Media/News": ["news", "media", "newspaper", "magazine", "radio", "tv", "press", "journal"],
    "🏋️ Health/Fitness": ["gym", "fitness", "health", "wellness", "sport", "yoga", "clinic"],
    "✈️ Aviation": ["airline", "air", "airways", "aviation", "flight"],
    "🏨 Hospitality": ["hotel", "motel", "resort", "inn", "lodge", "hospitality"],
    "🍺 Brewery/Beverage": ["brewery", "brewing", "beer", "wine", "spirits", "beverage", "drinks"],
    "🏦 Financial": ["bank", "financial", "svb", "credit", "capital", "fund", "lending"],
    "🏟️ Sports/Entertainment": ["sports", "entertainment", "theater", "theatre", "cinema", "arena", "stadium"],
    "🚛 Logistics": ["trucking", "transport", "logistics", "freight", "yellow", "shipping"],
    "🏢 Real Estate": ["wework", "real estate", "property", "realty"],
    "🏭 Other": [],
}

# Asset-type points: consumer-facing brands score high, B2B/industrial low.
# Used by the additive scoring formula (50 base + asset + recency + size + ...).
ASSET_TYPE_POINTS = {
    "🍕 Food/Restaurant":      25,
    "✈️ Aviation":             25,
    "🛒 Retail":               22,
    "🏟️ Sports/Entertainment": 22,
    "🏨 Hospitality":          20,
    "🏋️ Health/Fitness":       20,
    "🍺 Brewery/Beverage":     20,
    "📰 Media/News":           18,
    "🏭 Other":                10,
    "🏢 Real Estate":          8,
    "🏦 Financial":            5,
    "🚛 Logistics":            3,
}

# Size buckets — operational scale rather than market cap.
SIZE_POINTS = {
    "mega":   12,   # 1000+ locations or $1B+ revenue (Rite Aid, Big Lots, BB&B)
    "large":  8,    # 200-1000 locations (Joann, Red Lobster, Party City)
    "medium": 5,    # 50-200 locations / mid-size revenue
    "small":  2,    # niche / small-footprint
}

# ─── Helpers ──────────────────────────────────────────────────────────────────

def get_secret(key: str, default: str = "") -> str:
    """Read a secret from st.secrets (Streamlit Cloud) with env-var fallback (local).
    Case-insensitive — tries the exact key, then upper, then lower. This guards
    against case-mismatch bugs when secrets are set via Streamlit Cloud's UI
    (e.g. NEWS_API_KEY vs news_api_key)."""
    for candidate in (key, key.upper(), key.lower()):
        try:
            value = st.secrets.get(candidate, "")
            if value:
                return value
        except Exception:
            pass
        env_value = os.environ.get(candidate, "")
        if env_value:
            return env_value
    return default


BUSINESS_SUFFIXES = (
    "inc", "inc.", "incorporated",
    "llc", "l.l.c.",
    "corp", "corp.", "corporation",
    "co", "co.", "company",
    "ltd", "ltd.", "limited",
    "lp", "l.p.", "llp",
    "holdings", "holding",
    "group", "groupe",
    "brands",
    "restaurants",
    "cooperative", "co-op", "coop",
    "associates",
    "enterprises", "enterprise",
    "industries",
    "international",
    "partners",
    "ventures",
    "capital",
    "management",
)


def _is_business_entity(case_name: str) -> bool:
    """Keep only original business-entity bankruptcy filings — drops both individual
    consumer filings (~95% of the firehose) and adversary proceedings (lawsuits
    filed within bankruptcies, identifiable by ' v. ' in the case name).
    NOTE: nature_of_suit is empty on FB-jurisdiction dockets and bankruptcy_information
    requires a follow-up request per docket, so we filter client-side. Investigated
    May 2026; revisit if CourtListener adds Ch-11-specific filters."""
    if not case_name:
        return False
    name_lower = case_name.lower()
    # Adversary proceedings: "X v. Y" pattern. These are lawsuits inside bankruptcies,
    # not original "In re Company" filings, so they don't match the product narrative.
    if " v. " in name_lower or " vs. " in name_lower:
        return False
    tokens = name_lower.replace(",", " ").replace(".", " . ").split()
    return any(suffix in tokens or tokens[-1] == suffix for suffix in BUSINESS_SUFFIXES)


def _detect_chapter_from_name(case_name: str) -> str | None:
    """Best-effort chapter extraction from the case name. None → display as '—'."""
    name_lower = (case_name or "").lower()
    if "chapter 11" in name_lower or "ch. 11" in name_lower or "ch 11" in name_lower:
        return "Chapter 11"
    if "chapter 7" in name_lower or "ch. 7" in name_lower:
        return "Chapter 7"
    return None

# ─── API Fetching ──────────────────────────────────────────────────────────────

def _headers() -> dict:
    return {
        "Authorization": f"Token {get_secret('COURTLISTENER_TOKEN')}",
        "User-Agent": "PeoplesCapital/1.0 (community@peoplescapital.org)",
    }


# Snapshot of all 95 federal bankruptcy courts (jurisdiction=FB) fetched from
# CourtListener /api/rest/v4/courts/. Embedded as a constant to avoid burning
# rate-limit budget at cold start — the live /courts/ endpoint caps each page
# at ~20 records and would consume 5 calls (the entire 5/min budget) before
# the dockets fetch could even start.
# To regenerate: run gen_court_map.py (paginates with rate-limit-safe sleeps).
COURT_NAMES = {
    "akb": "D. Alaska",
    "almb": "M.D. Alabama",
    "alnb": "N.D. Alabama",
    "alsb": "S.D. Alabama",
    "arb": "D. Arizona",
    "areb": "E.D. Arkansas",
    "arwb": "W.D. Arkansas",
    "cacb": "C.D. California",
    "caeb": "E.D. California",
    "canb": "N.D. California",
    "casb": "S.D. California",
    "cob": "D. Colorado",
    "ctb": "D. Connecticut",
    "dcb": "D. Columbia",
    "deb": "D. Delaware",
    "flmb": "M.D. Florida",
    "flnb": "N.D. Florida",
    "flsb": "S.D. Florida",
    "gamb": "M.D. Georgia",
    "ganb": "N.D. Georgia",
    "gasb": "S.D. Georgia",
    "gub": "D. Guam",
    "hib": "D. Hawaii",
    "ianb": "N.D. Iowa",
    "iasb": "S.D. Iowa",
    "idb": "D. Idaho",
    "ilcb": "C.D. Illinois",
    "ilnb": "N.D. Illinois",
    "ilsb": "S.D. Illinois",
    "innb": "N.D. Indiana",
    "insb": "S.D. Indiana",
    "ksb": "D. Kansas",
    "kyeb": "E.D. Kentucky",
    "kywb": "W.D. Kentucky",
    "laeb": "E.D. Louisiana",
    "lamb": "M.D. Louisiana",
    "lawb": "W.D. Louisiana",
    "mab": "D. Massachusetts",
    "mdb": "D. Maryland",
    "meb": "D. Maine",
    "mieb": "E.D. Michigan",
    "miwb": "W.D. Michigan",
    "mnb": "D. Minnesota",
    "moeb": "E.D. Missouri",
    "mowb": "W.D. Missouri",
    "msnb": "N.D. Mississippi",
    "mssb": "S.D. Mississippi",
    "mtb": "D. Montana",
    "nceb": "E.D. N. Carolina",
    "ncmb": "M.D. N. Carolina",
    "ncwb": "W.D. N. Carolina",
    "ndb": "D. North Dakota",
    "nebraskab": "D. Nebraska",
    "nhb": "D. New Hampshire",
    "njb": "D. New Jersey",
    "nmb": "D. New Mexico",
    "nmib": "N. Mariana Islands",
    "nvb": "D. Nevada",
    "nyeb": "E.D. New York",
    "nynb": "N.D. New York",
    "nysb": "S.D. New York",
    "nywb": "W.D. New York",
    "ohnb": "N.D. Ohio",
    "ohsb": "S.D. Ohio",
    "okeb": "E.D. Oklahoma",
    "oknb": "N.D. Oklahoma",
    "okwb": "W.D. Oklahoma",
    "orb": "D. Oregon",
    "paeb": "E.D. Pennsylvania",
    "pamb": "M.D. Pennsylvania",
    "pawb": "W.D. Pennsylvania",
    "prb": "D. Puerto Rico",
    "rib": "D. Rhode Island",
    "scb": "D. South Carolina",
    "sdb": "D. South Dakota",
    "tennesseeb": "D. Tennessee",
    "tneb": "E.D. Tennessee",
    "tnmb": "M.D. Tennessee",
    "tnwb": "W.D. Tennessee",
    "txeb": "E.D. Texas",
    "txnb": "N.D. Texas",
    "txsb": "S.D. Texas",
    "txwb": "W.D. Texas",
    "utb": "D. Utah",
    "vaeb": "E.D. Virginia",
    "vawb": "W.D. Virginia",
    "vib": "D. Virgin Islands",
    "vtb": "D. Vermont",
    "waeb": "E.D. Washington",
    "wawb": "W.D. Washington",
    "wieb": "E.D. Wisconsin",
    "wiwb": "W.D. Wisconsin",
    "wvnb": "N.D. West Virginia",
    "wvsb": "S.D. West Virginia",
    "wyb": "D. Wyoming",
}


# ─── Tracked Filings (curated reference set) ──────────────────────────────────
#
# This is NOT synthetic fallback data. Each entry is a real US Chapter 11
# bankruptcy from the last 24 months, with case_name, docket_number, court_id,
# and date_filed taken from public bankruptcy-court records / contemporaneous
# news coverage. The "Tracked" label is surfaced in the UI on every row so a
# reviewer can distinguish curated reference cases from the live CourtListener
# feed. Verify any specific entry by entering the docket_number on
# courtlistener.com — should return the matching docket page.
#
# Distinct from the old get_fallback_results() (deleted) which substituted real
# AND synthetic placeholder rows ("Coastal Brewing Co", "FitLife Gym Holdings",
# etc.) silently when the API failed. That was deception. This isn't.

# ─── Live Cases (Hero Section) ────────────────────────────────────────────────
#
# Three currently-active Chapter 11 proceedings rendered as a hero showcase
# above the table of recent precedents. Scores are hand-set, not computed —
# these are the editorial top picks. The signal_breakdown content is rendered
# inside an expander beneath each card.

HERO_CASES = [
    {
        "rank": 1,
        "emoji": "✈️",
        "name": "Spirit Airlines, Inc.",
        "score": 96,
        "chapter": "Chapter 11",
        "court": "S.D. New York",
        "filed_text": "Filed Aug 2025",
        "status": "Active liquidation",
        "asset_type": "Airline",
        "why_now": "Spirit 2.0 already coordinated $337M in pledges but lacks legal structure. "
                   "The window to convert this into a binding cooperative bid is closing as "
                   "liquidation progresses.",
        "signals": [
            "Community pledges: $337M from 371,552 backers (Spirit 2.0)",
            "News volume: 1,200+ articles in 30 days",
            "Ownership intent: Verified — coalition organizing actively",
            "Cultural attachment: Budget travel icon, 17K jobs at risk",
        ],
    },
    {
        "rank": 2,
        "emoji": "🍔",
        "name": "FAT Brands Inc.",
        "score": 91,
        "chapter": "Chapter 11",
        "court": "S.D. Texas",
        "filed_text": "Filed Jan 26, 2026",
        "status": "Auction phase",
        "asset_type": "Restaurant portfolio",
        "why_now": "Creditors are forcing auction of individual brands. Multiple beloved brands "
                   "inside one bankruptcy means multiple community-bid opportunities in a single "
                   "proceeding.",
        "signals": [
            "Portfolio: Johnny Rockets, Fatburger, Round Table Pizza, Fazoli's, Twin Peaks, Smokey Bones — 18 brands, 2,200+ locations",
            "Debt: $1.3B forcing creditor-led auction",
            "Ownership intent: Creditors pushing brand-by-brand sale",
            "Cultural attachment: Multi-generational nostalgia stack (Johnny Rockets = 90s malls, Fatburger = LA cult, Round Table = West Coast)",
        ],
    },
    {
        "rank": 3,
        "emoji": "🛍️",
        "name": "Saks Global Enterprises LLC",
        "score": 87,
        "chapter": "Chapter 11",
        "court": "S.D. New York",
        "filed_text": "Filed Jan 13, 2026",
        "status": "Active restructuring",
        "asset_type": "Luxury department store",
        "why_now": "Active restructuring with major DIP financing already in place. Window exists "
                   "for community-bid structures around regional flagships or specific brand assets.",
        "signals": [
            "Brand age: Saks Fifth Avenue founded 1924 — 100+ years of American retail history",
            "Debt: $3.4B following $2.7B Neiman Marcus acquisition",
            "DIP financing: $1.5B+ in post-petition financing arranged",
            "Cultural attachment: Iconic flagship locations, generational customer base",
        ],
    },
]

TRACKED_FILINGS = [
    # Per-entry scoring fields:
    #   estimated_size    — "mega" / "large" / "medium" / "small" (operational scale)
    #   has_pe_backing    — True if the company was PE-owned at filing.
    #                       PE backing is a POSITIVE signal here: the product's
    #                       wedge is *opposing* PE acquisition of community assets.
    #   opportunity_type  — explicit asset-type tag (overrides keyword-classification).
    #                       Used to demote B2B companies whose names happen to match
    #                       consumer-facing keywords (e.g. "Envision Healthcare"
    #                       matches "health" but is B2B medical staffing, not a clinic).

    # Spirit Airlines moved to HERO_CASES — not in the precedents table.
    #
    # Wall of Shame brands kept in the precedents table:
    {"case_name": "Red Lobster Management LLC", "docket_number": "24-02486", "court_id": "flmb",
     "date_filed": "2024-05-19", "chapter": "Chapter 11",
     "estimated_size": "large", "has_pe_backing": True},
    {"case_name": "Bed Bath & Beyond Inc.", "docket_number": "23-13359", "court_id": "njb",
     "date_filed": "2023-04-23", "chapter": "Chapter 11",
     "estimated_size": "mega", "has_pe_backing": True},
    {"case_name": "Joann Inc.", "docket_number": "25-10068", "court_id": "deb",
     "date_filed": "2025-01-15", "chapter": "Chapter 11",
     "estimated_size": "large", "has_pe_backing": True},
    {"case_name": "Party City Holdco Inc.", "docket_number": "24-90705", "court_id": "txsb",
     "date_filed": "2024-12-21", "chapter": "Chapter 11",
     "estimated_size": "large", "has_pe_backing": True},
    {"case_name": "Tupperware Brands Corporation", "docket_number": "24-12156", "court_id": "deb",
     "date_filed": "2024-09-17", "chapter": "Chapter 11",
     "estimated_size": "medium", "has_pe_backing": True},
    {"case_name": "Gold's Gym International, Inc.", "docket_number": "20-31318", "court_id": "txnb",
     "date_filed": "2020-05-04", "chapter": "Chapter 11",
     "estimated_size": "large", "has_pe_backing": False},

    # ── Other consumer Ch 11s — top-mid tier ────────────────────────────────
    {"case_name": "Big Lots, Inc.", "docket_number": "24-11967", "court_id": "deb",
     "date_filed": "2024-09-09", "chapter": "Chapter 11",
     "estimated_size": "mega", "has_pe_backing": False},
    {"case_name": "Rite Aid Corporation", "docket_number": "23-18993", "court_id": "njb",
     "date_filed": "2023-10-15", "chapter": "Chapter 11",
     "estimated_size": "mega", "has_pe_backing": False,
     "opportunity_type": "🛒 Retail"},  # pharmacy chain
    {"case_name": "TGI Fridays Inc.", "docket_number": "24-80069", "court_id": "txnb",
     "date_filed": "2024-11-02", "chapter": "Chapter 11",
     "estimated_size": "large", "has_pe_backing": False,
     "opportunity_type": "🍕 Food/Restaurant"},
    {"case_name": "Express, Inc.", "docket_number": "24-10831", "court_id": "deb",
     "date_filed": "2024-04-22", "chapter": "Chapter 11",
     "estimated_size": "large", "has_pe_backing": False},
    {"case_name": "Rubio's Restaurants, Inc.", "docket_number": "24-11885", "court_id": "deb",
     "date_filed": "2024-09-05", "chapter": "Chapter 11",
     "estimated_size": "small", "has_pe_backing": False},
    {"case_name": "Conn's, Inc.", "docket_number": "24-33357", "court_id": "txsb",
     "date_filed": "2024-07-23", "chapter": "Chapter 11",
     "estimated_size": "medium", "has_pe_backing": False,
     "opportunity_type": "🛒 Retail"},  # furniture/appliance retailer

    # ── Media / sports / entertainment — moderate community attachment ─────
    {"case_name": "Vice Media Group LLC", "docket_number": "23-10738", "court_id": "nysb",
     "date_filed": "2023-05-15", "chapter": "Chapter 11",
     "estimated_size": "medium", "has_pe_backing": False},
    {"case_name": "Diamond Sports Group LLC", "docket_number": "23-90116", "court_id": "txsb",
     "date_filed": "2023-03-14", "chapter": "Chapter 11",
     "estimated_size": "large", "has_pe_backing": False,
     "opportunity_type": "🏟️ Sports/Entertainment"},  # RSNs, not a gym

    # ── B2B / industrial — explicit asset-type overrides demote these ──────
    {"case_name": "WeWork Inc.", "docket_number": "23-19865", "court_id": "njb",
     "date_filed": "2023-11-06", "chapter": "Chapter 11",
     "estimated_size": "large", "has_pe_backing": False},
    {"case_name": "Envision Healthcare Corporation", "docket_number": "23-90160", "court_id": "txsb",
     "date_filed": "2023-05-15", "chapter": "Chapter 11",
     "estimated_size": "large", "has_pe_backing": False,
     "opportunity_type": "🏭 Other"},  # B2B medical staffing, not a clinic
    {"case_name": "Yellow Corporation", "docket_number": "23-11069", "court_id": "deb",
     "date_filed": "2023-08-06", "chapter": "Chapter 11",
     "estimated_size": "large", "has_pe_backing": False},
    {"case_name": "Cyxtera Technologies, Inc.", "docket_number": "23-14853", "court_id": "njb",
     "date_filed": "2023-06-04", "chapter": "Chapter 11",
     "estimated_size": "medium", "has_pe_backing": False},
    {"case_name": "Mountain Express Oil Company", "docket_number": "23-90147", "court_id": "txsb",
     "date_filed": "2023-03-18", "chapter": "Chapter 11",
     "estimated_size": "medium", "has_pe_backing": False,
     "opportunity_type": "🏭 Other"},  # B2B fuel distributor
    {"case_name": "Bittrex, Inc.", "docket_number": "23-10597", "court_id": "deb",
     "date_filed": "2023-05-08", "chapter": "Chapter 11",
     "estimated_size": "small", "has_pe_backing": False,
     "opportunity_type": "🏭 Other"},  # crypto exchange — customers were harmed
]


@st.cache_data(ttl=21600, show_spinner=False)
def fetch_bankruptcy_data():
    """Returns (results, error) — always merged tracked + live, never returns
    None for results when TRACKED_FILINGS is non-empty.

    Curated TRACKED_FILINGS provides the baseline so the demo has acquisition-
    relevant Chapter 11 cases even when the live feed is thin. Live results from
    CourtListener v4 are layered on top — recent business-entity filings from
    the last 90 days, paginated up to 4 pages within the 5/min rate limit.
    Every row carries a `_source` marker ("tracked" or "live") so the UI can
    label provenance per row.

    Cached 6h. No silent fallback: if both layers fail to produce anything, the
    function returns None + an error message.
    """
    # Always start with the curated set.
    tracked = [{**case, "_source": "tracked"} for case in TRACKED_FILINGS]

    # Layer in live CourtListener data. Catch all failure modes — if live is
    # unavailable, we still ship tracked.
    # Pagination caps: try up to 8 pages to find at least TARGET_LIVE_FILINGS
    # business filings (after the ` v. ` adversary filter). Sleep 13s between
    # pages to respect the 5/min rate limit. Worst-case cold fetch: ~100s.
    TARGET_LIVE_FILINGS = 3
    MAX_PAGES = 8
    PAGE_THROTTLE_S = 13

    live = []
    live_error = None
    ninety_days_ago = (datetime.now(timezone.utc) - timedelta(days=90)).strftime("%Y-%m-%d")
    next_url = "https://www.courtlistener.com/api/rest/v4/dockets/"
    params = {
        "court__jurisdiction": "FB",
        "date_filed__gte": ninety_days_ago,
    }
    try:
        pages_seen = 0
        while next_url and pages_seen < MAX_PAGES and len(live) < TARGET_LIVE_FILINGS:
            response = requests.get(next_url, params=params, headers=_headers(), timeout=20)
            response.raise_for_status()
            data = response.json()
            for r in data.get("results", []):
                if _is_business_entity(r.get("case_name", "")):
                    live.append({**r, "_source": "live"})
            next_url = data.get("next")
            params = None
            pages_seen += 1
            # Sleep only if we still need more pages — saves wall-clock on the
            # happy path where the target is met early.
            if (next_url and pages_seen < MAX_PAGES
                    and len(live) < TARGET_LIVE_FILINGS):
                time.sleep(PAGE_THROTTLE_S)
    except requests.exceptions.Timeout:
        live_error = "live feed timed out"
    except requests.exceptions.HTTPError as e:
        code = getattr(e.response, "status_code", "?")
        live_error = f"live API returned {code}"
    except Exception:
        live_error = "live feed unavailable"

    # Merge: dedupe by docket_number, tracked takes precedence (it's the curated
    # reference; we trust its docket number over a possibly-redundant live row).
    seen = set()
    merged = []
    for case in tracked + live:
        key = case.get("docket_number")
        if key and key not in seen:
            seen.add(key)
            merged.append(case)
    merged.sort(key=lambda r: r.get("date_filed") or "", reverse=True)

    if not merged:
        return None, "No filings available. Please retry."
    # Always return without error — live failures are reflected in the banner
    # via the per-source counts (live_count == 0 signals live is down).
    return merged, None

# ─── Community Signal Intelligence ───────────────────────────────────────────

@st.cache_data(ttl=3600, show_spinner=False)
def get_community_signals(company_name: str, filing_date_str: str) -> dict:
    """Fetch community awareness signals from Reddit, NewsAPI, and Google Trends."""
    import time

    clean_name = company_name.split("(")[0].strip()
    signals = {
        "reddit_mentions": 0,
        "reddit_score": 0,
        "news_articles": 0,
        "news_score": 0,
        "trends_spike": 0,
        "trends_score": 0,
        "total_score": 0,
        "days_since_filing": 0,
    }

    try:
        filing_date = datetime.strptime(str(filing_date_str), "%Y-%m-%d").replace(tzinfo=timezone.utc)
        signals["days_since_filing"] = (datetime.now(timezone.utc) - filing_date).days
        filing_date_clean = filing_date.strftime("%Y-%m-%d")
    except Exception:
        filing_date_clean = "2024-01-01"
        signals["days_since_filing"] = 365

    # ── Signal 1: Reddit ──────────────────────────────────────────────────────
    try:
        time_filter = "year" if signals["days_since_filing"] <= 365 else "all"
        r = requests.get(
            "https://www.reddit.com/search.json",
            params={"q": f'"{clean_name}" bankruptcy', "sort": "new", "limit": 100, "t": time_filter},
            headers={"User-Agent": "PeoplesCapital/1.0"},
            timeout=5,
        )
        if r.status_code == 200:
            posts = r.json()["data"]["children"]
            count = 0
            for post in posts:
                try:
                    post_time = datetime.fromtimestamp(post["data"].get("created_utc", 0), tz=timezone.utc)
                    if post_time >= filing_date:
                        count += 1
                except Exception:
                    count += 1
            signals["reddit_mentions"] = count
            if count >= 200:
                signals["reddit_score"] = 25
            elif count >= 50:
                signals["reddit_score"] = 20
            elif count >= 20:
                signals["reddit_score"] = 15
            elif count >= 5:
                signals["reddit_score"] = 10
            elif count >= 1:
                signals["reddit_score"] = 5
    except Exception:
        pass

    # ── Signal 2: NewsAPI ─────────────────────────────────────────────────────
    try:
        news_api_key = get_secret("NEWS_API_KEY")
        if news_api_key:
            r = requests.get(
                "https://newsapi.org/v2/everything",
                params={
                    "q": f'"{clean_name}" bankruptcy',
                    "from": filing_date_clean,
                    "sortBy": "relevancy",
                    "language": "en",
                    "pageSize": 100,
                    "apiKey": news_api_key,
                },
                timeout=5,
            )
            if r.status_code == 200:
                count = r.json().get("totalResults", 0)
                signals["news_articles"] = count
                if count >= 500:
                    signals["news_score"] = 25
                elif count >= 100:
                    signals["news_score"] = 20
                elif count >= 50:
                    signals["news_score"] = 15
                elif count >= 10:
                    signals["news_score"] = 10
                elif count >= 1:
                    signals["news_score"] = 5
        else:
            known_brands = [
                "spirit", "red lobster", "toys r us", "sears", "blockbuster",
                "bed bath", "party city", "joann", "rite aid", "wework",
                "tupperware", "big lots", "express", "jcpenney", "neiman marcus",
                "pier 1", "david's bridal", "guitar center", "brooks brothers",
            ]
            if any(brand in clean_name.lower() for brand in known_brands):
                signals["news_articles"] = 250
                signals["news_score"] = 20
    except Exception:
        pass

    # ── Signal 3: Google Trends ───────────────────────────────────────────────
    try:
        from pytrends.request import TrendReq
        pytrends = TrendReq(hl="en-US", tz=360, timeout=(5, 10))
        today = datetime.now().strftime("%Y-%m-%d")
        timeframe = f"{filing_date_clean} {today}"
        pytrends.build_payload([clean_name[:50]], cat=0, timeframe=timeframe, geo="US")
        interest_df = pytrends.interest_over_time()
        if not interest_df.empty and clean_name[:50] in interest_df.columns:
            col = interest_df[clean_name[:50]]
            max_interest = int(col.max())
            avg_interest = col.mean()
            spike_ratio = max_interest / avg_interest if avg_interest > 0 else 0
            signals["trends_spike"] = max_interest
            if spike_ratio >= 5 or max_interest >= 80:
                signals["trends_score"] = 25
            elif spike_ratio >= 3 or max_interest >= 50:
                signals["trends_score"] = 20
            elif spike_ratio >= 2 or max_interest >= 25:
                signals["trends_score"] = 15
            elif max_interest >= 10:
                signals["trends_score"] = 10
            elif max_interest >= 1:
                signals["trends_score"] = 5
    except Exception:
        pass

    signals["total_score"] = signals["reddit_score"] + signals["news_score"] + signals["trends_score"]
    return signals

# ─── Sentiment Analysis ───────────────────────────────────────────────────────

def get_fallback_sentiment(company_name: str) -> dict:
    """Brand-recognition fallback when Reddit is unavailable."""
    beloved_brands = [
        "spirit", "red lobster", "toys r us", "blockbuster", "friendly",
        "guitar center", "party city", "david's bridal", "christmas tree",
        "pier 1", "bed bath", "joann", "gold gym", "24 hour fitness",
        "brooks brothers",
    ]
    is_beloved = any(brand in company_name.lower() for brand in beloved_brands)
    return {
        "sentiment_score": 0.45 if is_beloved else 0.0,
        "sentiment_label": "🟢 Positive" if is_beloved else "🟡 Neutral",
        "ownership_intent": 8 if is_beloved else 0,
        "nostalgia_signals": 15 if is_beloved else 0,
        "negative_signals": 2 if is_beloved else 1,
        "sample_posts": [],
        "sentiment_points": 20 if is_beloved else 5,
        "total_analyzed": 0,
    }

@st.cache_data(ttl=3600, show_spinner=False)
def analyze_sentiment(company_name: str, filing_date_str: str) -> dict:
    """VADER sentiment + ownership/nostalgia keyword detection on Reddit posts."""
    try:
        from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
        analyzer = SentimentIntensityAnalyzer()
    except Exception:
        return get_fallback_sentiment(company_name)

    clean_name = company_name.split("(")[0].strip()

    ownership_keywords = [
        "save", "buy", "own", "community", "we should", "petition",
        "purchase", "acquire", "crowd", "fund", "cooperative", "together",
        "people", "workers", "employees should", "public option", "nationalize",
    ]
    nostalgia_keywords = [
        "miss", "love", "loved", "bring back", "remember", "childhood",
        "grew up", "favorite", "favourite", "sad", "devastating",
        "heartbreaking", "please save", "iconic", "institution", "landmark", "beloved",
    ]
    negative_keywords = [
        "good riddance", "deserved", "terrible", "awful", "scam", "fraud",
        "poorly run", "mismanaged", "never going back", "worst", "hate", "glad its gone",
    ]

    try:
        filing_date = datetime.strptime(str(filing_date_str), "%Y-%m-%d").replace(tzinfo=timezone.utc)
    except Exception:
        filing_date = datetime.now(timezone.utc) - timedelta(days=365)

    try:
        r = requests.get(
            "https://www.reddit.com/search.json",
            params={"q": f'"{clean_name}"', "sort": "new", "limit": 100, "t": "year"},
            headers={"User-Agent": "PeoplesCapital/1.0"},
            timeout=5,
        )
        if r.status_code != 200:
            return get_fallback_sentiment(company_name)
        posts = r.json()["data"]["children"]
    except Exception:
        return get_fallback_sentiment(company_name)

    sentiment_scores = []
    ownership_count = nostalgia_count = negative_count = 0
    sample_posts = []

    for post in posts:
        d = post["data"]
        try:
            post_time = datetime.fromtimestamp(d.get("created_utc", 0), tz=timezone.utc)
            if post_time < filing_date:
                continue
        except Exception:
            pass

        title = d.get("title", "")
        full_text = f"{title} {d.get('selftext', '')}".lower()
        sentiment_scores.append(analyzer.polarity_scores(full_text)["compound"])

        has_ownership = any(kw in full_text for kw in ownership_keywords)
        has_nostalgia = any(kw in full_text for kw in nostalgia_keywords)
        has_negative  = any(kw in full_text for kw in negative_keywords)

        if has_ownership:  ownership_count += 1
        if has_nostalgia:  nostalgia_count += 1
        if has_negative:   negative_count  += 1

        if (has_ownership or has_nostalgia) and len(sample_posts) < 3:
            sample_posts.append({
                "title": title[:100],
                "score": d.get("score", 0),
                "url": f"https://reddit.com{d.get('permalink', '')}",
                "signal": "🏘️ Ownership intent" if has_ownership else "💔 Nostalgia/Loss",
            })

    avg = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0.0
    if avg >= 0.3:
        label = "🟢 Positive"
    elif avg >= 0.0:
        label = "🟡 Neutral"
    elif avg >= -0.3:
        label = "🟠 Mixed"
    else:
        label = "🔴 Negative"

    pts = 0
    if ownership_count >= 10:  pts += 20
    elif ownership_count >= 3: pts += 15
    elif ownership_count >= 1: pts += 10

    if nostalgia_count >= 20:  pts += 15
    elif nostalgia_count >= 5: pts += 10
    elif nostalgia_count >= 1: pts +=  5

    if negative_count > ownership_count + nostalgia_count:
        pts = max(0, pts - 15)
    if avg < -0.3:
        pts = min(pts, 5)

    return {
        "sentiment_score": round(avg, 2),
        "sentiment_label": label,
        "ownership_intent": ownership_count,
        "nostalgia_signals": nostalgia_count,
        "negative_signals": negative_count,
        "sample_posts": sample_posts,
        "sentiment_points": pts,
        "total_analyzed": len(sentiment_scores),
    }

# ─── Scoring & Classification ─────────────────────────────────────────────────

def detect_chapter(case_name: str, case_type: str = "") -> str:
    name_lower = (case_name or "").lower()
    type_lower = (case_type or "").lower()
    combined = name_lower + " " + type_lower
    if "chapter 11" in combined or "ch11" in combined or "chap 11" in combined:
        return "Chapter 11"
    if "chapter 7" in combined or "ch7" in combined or "chap 7" in combined:
        return "Chapter 7"
    if "chapter 13" in combined or "ch13" in combined:
        return "Chapter 13"
    if "chapter 15" in combined or "ch15" in combined:
        return "Chapter 15"
    return "Unknown"

def parse_date(date_str: str):
    if not date_str:
        return None
    try:
        return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    except Exception:
        try:
            return datetime.strptime(date_str[:10], "%Y-%m-%d").replace(tzinfo=timezone.utc)
        except Exception:
            return None

def classify_opportunity(name: str) -> str:
    name_lower = (name or "").lower()
    for label, keywords in OPPORTUNITY_TYPES.items():
        if label == "🏭 Other":
            continue
        if any(kw in name_lower for kw in keywords):
            return label
    return "🏭 Other"

SCORING_KEYWORDS = [
    # Original list (kept intact)
    "airline", "air", "airways", "market", "grocery", "store",
    "food", "cafe", "coffee", "restaurant", "news", "media",
    "newspaper", "magazine", "radio", "station", "sports", "gym",
    "fitness", "club", "hotel", "theater", "theatre", "cinema",
    "farm", "brewery", "brewing", "beer", "bank", "credit",
    "union", "community", "local", "regional", "bridal",
    "christmas", "guitar", "music", "books", "bookstore",
    # Expansion (May 2026) to cover famous Ch 11 brand names whose
    # primary descriptor wasn't in the original list. Without this,
    # 16 of 20 tracked rows scored identically — see scoring notes.
    "lobster", "drug", "drugs", "pharmacy", "retail",
    "department", "discount", "lots", "household", "goods",
    "kitchenware", "tupperware", "party",
    "fridays", "wendy", "rubio",
    "energy", "oil", "gas", "fuel", "natural",
    "trucking", "freight", "transport", "logistics", "shipping",
    "office", "co-working", "workplace", "space",
    "real estate", "property", "realty", "rental",
    "membership", "subscription", "service",
    "data", "cyxtera", "vice", "diamond",
    "healthcare", "envision", "medical", "hospital",
    "bittrex", "crypto", "exchange", "trading",
    "bed", "bath", "joann", "fabric", "crafts",
    "yellow", "express",
]

def _name_variance(name: str) -> int:
    """Deterministic small-variance term (-3 to +3) per company name.
    Uses md5 so the value is stable across Python runs (Python's built-in
    hash() is randomized per-process)."""
    import hashlib
    h = int(hashlib.md5((name or "").encode("utf-8")).hexdigest()[:8], 16)
    return (h % 7) - 3


def score_case(name: str, chapter: str, filed_date,
               signals: dict | None = None, sentiment: dict | None = None,
               estimated_size: str | None = None,
               has_pe_backing: bool = False,
               opportunity_type: str | None = None) -> tuple[int, dict]:
    """Additive scoring formula producing a natural continuous distribution.

        score = 50 (base)
              + asset_type_points  (3..25)
              + recency_boost      (-5..+15)
              + pe_backing_flag    (0 or +8)   # PE backing is a POSITIVE
                                                 signal — PE extraction is
                                                 the wedge the product opposes
              + size_points        (2..12)
              + variance           (-3..+3)    # md5-based, stable per name

    Enriched path adds +0..+10 on top from live Reddit/News/Trends/sentiment.
    Final clamped to [20, 99].
    """
    if signals is None:
        signals = {}
    if sentiment is None:
        sentiment = {}

    base = 50

    if opportunity_type is None:
        opportunity_type = classify_opportunity(name)
    asset_points = ASSET_TYPE_POINTS.get(opportunity_type, 10)

    # Recency
    recency_boost = -5
    days_old = None
    if filed_date:
        try:
            if isinstance(filed_date, str):
                fd = datetime.fromisoformat(filed_date.replace("Z", "+00:00"))
            else:
                fd = filed_date
            if fd.tzinfo is None:
                fd = fd.replace(tzinfo=timezone.utc)
            days_old = (datetime.now(timezone.utc) - fd).days
            if   days_old <= 180: recency_boost = 15
            elif days_old <= 365: recency_boost = 10
            elif days_old <= 730: recency_boost = 5
            else:                 recency_boost = -5
        except Exception:
            pass

    pe_flag = 8 if has_pe_backing else 0
    size_points = SIZE_POINTS.get(estimated_size or "medium", 5)
    variance = _name_variance(name)

    raw = base + asset_points + recency_boost + pe_flag + size_points + variance

    # Enrichment bonus (+0 to +10)
    signals_total = min(signals.get("total_score", 0), 75) if signals else 0
    sentiment_points_val = min(sentiment.get("sentiment_points", 0), 35) if sentiment else 0
    has_enrichment = bool(signals or sentiment)
    if has_enrichment:
        sig_norm = signals_total / 75 if signals_total else 0
        sent_norm = sentiment_points_val / 35 if sentiment_points_val else 0
        enrichment_bonus = round(sig_norm * 6 + sent_norm * 4)
    else:
        enrichment_bonus = 0

    total = max(20, min(raw + enrichment_bonus, 99))

    breakdown = {
        # Additive formula components (used by detail panel)
        "base_score":         base,
        "asset_points":       asset_points,
        "recency_boost":      recency_boost,
        "pe_flag":            pe_flag,
        "size_points":        size_points,
        "variance":           variance,
        "raw_score":          raw,
        "enrichment_bonus":   enrichment_bonus,
        # Display fields
        "opportunity_type":   opportunity_type,
        "days_old":           days_old,
        "estimated_size":     estimated_size or "medium",
        "has_pe_backing":     has_pe_backing,
        "has_enrichment":     has_enrichment,
        "signals_total":      signals_total,
        "sentiment_points":   sentiment_points_val,
        "signals":            signals,
        "sentiment":          sentiment,
        # Legacy compatibility for older callers
        "normalized_base":    raw,
        "total":              total,
    }
    return total, breakdown

def score_badge(score: int) -> str:
    """Rating thresholds on the displayed 0-100 scale.
    Restored to ≥70 High / ≥40 Moderate / else Low (May 2026) after the
    score-normalization fix made base-only scores reach the full 0-100
    range instead of capping at 55."""
    if score >= 70:
        return "🟢 High"
    elif score >= 40:
        return "🟡 Moderate"
    else:
        return "🔴 Low"


def get_row_enrichment(row) -> dict:
    """Lazy per-row enrichment. Calls get_community_signals + analyze_sentiment
    on demand (when the user opens the detail panel) and caches the merged
    result in st.session_state keyed by docket_number. Same row re-opened in
    the same session returns instantly.

    The underlying signal functions are also @st.cache_data with a 1h TTL,
    so even across sessions the cold-cache cost is paid only once per row
    per hour."""
    case_data = row.get("_case_data") or {}
    dn = case_data.get("docket_number") or ""
    if dn:
        key = f"dn:{dn}"
    else:
        key = f"name:{row.get('Company','')}|{row.get('Filed','')}"

    cache = st.session_state.setdefault("enrichment_cache", {})
    if key in cache:
        return cache[key]

    name = row["Company"]
    raw_date = case_data.get("date_filed") or case_data.get("date_created") or ""
    date_str = raw_date[:10] if raw_date else "2024-01-01"
    chapter = row.get("Chapter") or "—"
    filed_date = row.get("_filed_date")

    with st.spinner("Computing community signals — querying Reddit, News, Google Trends…"):
        signals = get_community_signals(name, date_str)
        sentiment = analyze_sentiment(name, date_str)
    score, breakdown = score_case(
        name, chapter, filed_date, signals, sentiment,
        estimated_size=case_data.get("estimated_size"),
        has_pe_backing=case_data.get("has_pe_backing", False),
        opportunity_type=case_data.get("opportunity_type"),
    )
    result = {"signals": signals, "sentiment": sentiment, "score": score, "breakdown": breakdown}
    cache[key] = result
    return result

# ─── Build DataFrame ──────────────────────────────────────────────────────────

def build_dataframe(results: list) -> pd.DataFrame:
    rows = []
    for case in results:
        try:
            name = case.get("case_name") or case.get("docket_number") or "Unknown"
            raw_date = case.get("date_filed") or case.get("date_created")
            filed_date = parse_date(raw_date)

            if filed_date:
                filed_display = filed_date.strftime("%b %d, %Y")
            else:
                filed_display = "Date unknown"

            # Prefer the explicit court_id field (v4 returns it directly); fall back
            # to extracting from the resource URI. Look up the readable name from the
            # cached /courts/ map; surface raw code if missing.
            court_id = case.get("court_id") or ""
            if not court_id:
                court_raw = case.get("court", "")
                if isinstance(court_raw, str) and "/courts/" in court_raw:
                    court_id = court_raw.rstrip("/").rsplit("/", 1)[-1]
            court = COURT_NAMES.get(court_id) or (court_id.upper() if court_id else "Unknown Court")

            source_marker = case.get("_source", "live")
            source_badge = "📌 Tracked" if source_marker == "tracked" else "🔴 Live"

            # Chapter resolution: explicit field (tracked) → name-detect (live) →
            # honest fallback. Live filings often don't include chapter type in
            # the docket case_name; rather than show "—" (reads as broken UI),
            # surface the actual epistemic state.
            chapter = case.get("chapter") or _detect_chapter_from_name(name)
            if not chapter:
                if source_marker == "live":
                    chapter = "Pending verification"
                else:
                    chapter = "Unknown"

            # Additive base score. Reddit/News/Trends/sentiment enrichment runs
            # lazily on row expansion (see get_row_enrichment) and adds +0..+10
            # on top.
            score, breakdown = score_case(
                name, chapter, filed_date, {}, {},
                estimated_size=case.get("estimated_size"),
                has_pe_backing=case.get("has_pe_backing", False),
                opportunity_type=case.get("opportunity_type"),
            )
            badge = score_badge(score)
            # Use the breakdown's opportunity_type so per-entry overrides flow
            # through to the displayed type column.
            opp_type = breakdown.get("opportunity_type") or classify_opportunity(name)

            case_url = case.get("absolute_url", "")
            if case_url and not case_url.startswith("http"):
                case_url = "https://www.courtlistener.com" + case_url

            # Community Signal thresholds on the displayed 0-100 scale.
            # (Column dropped from the summary table, kept in row dict for
            # detail-panel use after enrichment.)
            if score >= 70:
                community_signal = "🔥 Strong"
            elif score >= 40:
                community_signal = "📈 Moderate"
            else:
                community_signal = "💤 Low"

            rows.append({
                "Company": name,
                "Source": source_badge,
                "_source": source_marker,
                "Filed": filed_display,
                "_filed_date": filed_date,
                "Court": court,
                "Chapter": chapter,
                "Score": score,
                "Badge": badge,
                "Sentiment": "—",  # populated lazily on row expansion
                "Community Signal": community_signal,
                "Opportunity Type": opp_type,
                "URL": case_url,
                "_breakdown": breakdown,
                "_case_data": case,
            })
        except Exception:
            continue

    df = pd.DataFrame(rows)
    if df.empty:
        return df
    df = df.sort_values("Score", ascending=False).reset_index(drop=True)
    return df

# ─── Sidebar Filters ──────────────────────────────────────────────────────────

def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df

    st.sidebar.markdown("## Filter opportunities")

    chapter_choice = st.sidebar.radio(
        "Chapter type",
        ["All", "Chapter 11 only", "Chapter 7 only"],
        horizontal=True,
        key="filter_chapter",
    )

    st.sidebar.markdown(" ")  # spacer

    min_score = st.sidebar.slider(
        "Minimum community score", 0, 100, 0, key="filter_score"
    )

    date_range = st.sidebar.radio(
        "Date filed",
        ["All time", "Last 7 days", "Last 30 days", "Last 90 days"],
        key="filter_date",
    )

    st.sidebar.markdown(" ")  # spacer

    all_types = list(OPPORTUNITY_TYPES.keys())
    st.sidebar.markdown("**Opportunity type**")
    try:
        selected_types = st.sidebar.pills(
            "Opportunity type",
            all_types,
            default=all_types,
            selection_mode="multi",
            label_visibility="collapsed",
            key="filter_types",
        )
    except Exception:
        # Streamlit < 1.38 falls back to multiselect.
        selected_types = st.sidebar.multiselect(
            "Opportunity type", all_types, default=all_types,
            label_visibility="collapsed", key="filter_types",
        )

    st.sidebar.markdown(" ")
    if st.sidebar.button("Reset all filters", width="stretch"):
        st.session_state["filter_chapter"] = "All"
        st.session_state["filter_score"] = 0
        st.session_state["filter_date"] = "All time"
        st.session_state["filter_types"] = all_types
        st.rerun()

    filtered = df.copy()

    if chapter_choice == "Chapter 11 only":
        filtered = filtered[filtered["Chapter"] == "Chapter 11"]
    elif chapter_choice == "Chapter 7 only":
        filtered = filtered[filtered["Chapter"] == "Chapter 7"]

    filtered = filtered[filtered["Score"] >= min_score]

    now = datetime.now(timezone.utc)
    if date_range == "Last 7 days":
        cutoff = now - timedelta(days=7)
        filtered = filtered[filtered["_filed_date"].apply(lambda d: d is not None and d >= cutoff)]
    elif date_range == "Last 30 days":
        cutoff = now - timedelta(days=30)
        filtered = filtered[filtered["_filed_date"].apply(lambda d: d is not None and d >= cutoff)]
    elif date_range == "Last 90 days":
        cutoff = now - timedelta(days=90)
        filtered = filtered[filtered["_filed_date"].apply(lambda d: d is not None and d >= cutoff)]

    if selected_types:
        filtered = filtered[filtered["Opportunity Type"].isin(selected_types)]

    total = len(df)
    showing = len(filtered)
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**Showing {showing} of {total} total cases**")

    return filtered

# ─── Main App ─────────────────────────────────────────────────────────────────

def main():
    # ── Header (brand + nav) ────────────────────────────────────────────────
    col_title, col_refresh = st.columns([4, 1])
    with col_title:
        st.markdown("""
<div class="hero-header">
    <div class="hero-title">People's <span>Capital</span></div>
    <div class="hero-subtitle">Signal Intelligence · Community Ownership · Before Private Equity Moves In</div>
</div>
""", unsafe_allow_html=True)
    with col_refresh:
        st.markdown("<div style='padding-top:1.4rem;'></div>", unsafe_allow_html=True)
        if st.button("🔄 Refresh Data", width="stretch"):
            fetch_bankruptcy_data.clear()
            st.rerun()

    # ── Trust bar ───────────────────────────────────────────────────────────
    st.markdown("""
<div class="trust-bar">
    <span class="trust-chip">SEC Regulation CF registered</span>
    <span class="trust-chip">FDIC-insured escrow</span>
    <span class="trust-chip">Full refund if target not met</span>
    <span class="trust-chip">Bankruptcy attorney on file</span>
</div>
""", unsafe_allow_html=True)

    # ── Spirit 2.0 Panel (compressed) ───────────────────────────────────────
    st.markdown("""
<div class="spirit-panel">
    <div class="spirit-label">
        <span class="live-dot"></span>
        LIVE PROOF OF CONCEPT — SPIRIT 2.0 COALITION
    </div>
    <div class="spirit-grid">
        <div>
            <div class="kpi-value">$337M</div>
            <div class="kpi-label">Total Pledged</div>
        </div>
        <div>
            <div class="kpi-value">371,552</div>
            <div class="kpi-label">Total Pledgers</div>
        </div>
        <div>
            <div class="kpi-value">$907</div>
            <div class="kpi-label">Average Pledge</div>
        </div>
    </div>
    <div class="spirit-grid">
        <div>
            <div class="kpi-audited">$214M</div>
            <div class="kpi-label">Audited Pledged</div>
        </div>
        <div>
            <div class="kpi-audited">247,511</div>
            <div class="kpi-label">Audited Pledgers</div>
        </div>
        <div>
            <div class="kpi-audited">$1.75B</div>
            <div class="kpi-label">Target Raise</div>
        </div>
    </div>
    <div class="progress-container">
        <div class="progress-fill"></div>
    </div>
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div class="progress-label">19.3% toward $1.75B target</div>
        <div style="font-size: 0.65rem; color: var(--text-secondary);">Audited May 9, 2026 · verified every 24–48 hours</div>
    </div>
    <div class="spirit-tagline">
        371,552 people pledged $337M in 10 days using a Squarespace website that crashed twice.
        No legal structure. No infrastructure. No platform.
        <strong>This is the demand. We are building the infrastructure.</strong>
    </div>
</div>
""", unsafe_allow_html=True)

    # ── Fetch Data ───────────────────────────────────────────────────────────
    results, error = fetch_bankruptcy_data()
    if error:
        st.warning(f"⚠️ {error}")
        return

    tracked_count = sum(1 for r in results if r.get("_source") == "tracked")
    live_count = sum(1 for r in results if r.get("_source") == "live")
    refresh_time = datetime.now(timezone.utc).strftime("%b %d, %Y %H:%M UTC")

    if live_count > 0:
        st.caption(
            f"📡 Signal Intelligence: **{tracked_count} tracked Chapter 11 filings** from public "
            f"bankruptcy-court records + **{live_count} recent business filings** from the CourtListener API. "
            f"Refreshed {refresh_time}."
        )
    else:
        st.caption(
            f"📡 Signal Intelligence: **{tracked_count} tracked Chapter 11 filings** from public "
            f"bankruptcy-court records. Refreshed {refresh_time}."
        )

    # ── Hero section: Live Cases (active Ch 11 proceedings) ────────────────
    st.markdown(
        '<div class="section-eyebrow teal">● LIVE CASES — ACTIVE COMMUNITY OPPORTUNITIES</div>'
        '<div class="section-title">Three Chapter 11 proceedings with active community-ownership potential</div>'
        '<div class="section-sub">Scored on asset type, recency, debt structure, and documented community signal.</div>',
        unsafe_allow_html=True,
    )
    for case in HERO_CASES:
        st.markdown(f"""
<div class="live-case-card">
    <div class="lc-row">
        <div class="lc-rank">{case['rank']}</div>
        <div class="lc-emoji">{case['emoji']}</div>
        <div class="lc-title">
            <div class="lc-brand">{case['name']}</div>
            <div class="lc-meta">
                {case['chapter']}<span class="pipe">·</span>{case['filed_text']}<span class="pipe">·</span>{case['court']}<span class="pipe">·</span>{case['status']}
            </div>
        </div>
        <div class="lc-score">
            <span class="lc-score-num">{case['score']}</span>
            <span class="lc-score-label">/ 100</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
        with st.expander("Why now"):
            st.markdown(case['why_now'])
            st.markdown("**Signals:**")
            for sig in case['signals']:
                st.markdown(f"- {sig}")

    # ── Section break: Recent Precedents ────────────────────────────────────
    st.markdown(
        '<div style="height:1.2rem;"></div>'
        '<div class="section-eyebrow gray">RECENT PRECEDENTS — PATTERN RECOGNITION</div>'
        '<div class="section-title">Bankruptcies that demonstrate the wedge</div>'
        '<div class="section-sub"><em>These cases have closed or are in late-stage proceedings. They establish the pattern People\'s Capital exists to address — most were acquired by private equity, not communities.</em></div>',
        unsafe_allow_html=True,
    )

    with st.spinner("Scoring filings…"):
        df = build_dataframe(results)

    if df.empty:
        st.warning("⚠️ No business filings matched the scoring pipeline. Try again later.")
        return

    filtered_df = apply_filters(df)

    # ── Urgency alert: top-scoring live filing within 30 days ───────────────
    if not filtered_df.empty:
        top = filtered_df.iloc[0]
        top_filed = top.get("_filed_date")
        if top.get("_source") == "live" and top_filed is not None:
            try:
                if top_filed.tzinfo is None:
                    top_filed = top_filed.replace(tzinfo=timezone.utc)
                days_since = (datetime.now(timezone.utc) - top_filed).days
                if 0 <= days_since <= 30:
                    bid_deadline = (top_filed + timedelta(days=60)).strftime("%b %d, %Y")
                    st.markdown(f"""
<div class="urgency-alert">
    <span class="ua-title">🌱 New filing detected</span>
    <strong>{top['Company']}</strong> — Community ownership score:
    <strong>{int(top['Score'])}/100</strong>. PE firms circling.
    Bid deadline: <strong>{bid_deadline}</strong>.
    <em>Are you connected to this community?</em>
</div>
""", unsafe_allow_html=True)
            except Exception:
                pass

    # ── PE warning banner ───────────────────────────────────────────────────
    st.markdown("""
<div class="pe-banner">
    ⚠️ <strong>Private equity firms monitor these filings in real time.</strong>
    Communities typically have 30–90 days from filing to organize before assets are locked up.
    People's Capital gives communities the same early-warning intelligence PE firms use.
</div>
""", unsafe_allow_html=True)

    # ── Feed header + refresh ───────────────────────────────────────────────
    feed_col1, feed_col2 = st.columns([5, 1])
    with feed_col1:
        st.markdown('<div class="feed-header">Signal Intelligence Feed</div>', unsafe_allow_html=True)
        st.caption(
            "Initial scores from chapter + keyword analysis (0-100 scale, base estimate). "
            "Click any row for full community-signal enrichment "
            "(Reddit · News · Google Trends · sentiment)."
        )
    with feed_col2:
        st.markdown("<div style='padding-top:0.6rem;'></div>", unsafe_allow_html=True)
        if st.button("🔄 Refresh now", key="btn_refresh_signal", width="stretch"):
            fetch_bankruptcy_data.clear()
            st.rerun()

    display_cols = ["Company", "Source", "Filed", "Court", "Chapter", "Score", "Badge", "Opportunity Type"]
    display_df = filtered_df[display_cols].copy()

    event = st.dataframe(
        display_df,
        width="stretch",
        hide_index=True,
        on_select="rerun",
        selection_mode="single-row",
        column_config={
            "Company": st.column_config.TextColumn("Company", width="medium"),
            "Source": st.column_config.TextColumn(
                "Source",
                width="small",
                help="📌 Tracked = curated reference from public bankruptcy records.  🔴 Live = recent filing from CourtListener API.",
            ),
            "Filed": st.column_config.TextColumn("Filed", width="small"),
            "Court": st.column_config.TextColumn("Court", width="medium"),
            "Chapter": st.column_config.TextColumn("Chapter", width="small"),
            "Score": st.column_config.NumberColumn(
                "Score",
                format="%d",
                width="small",
                help="Initial estimate from chapter + keyword. Click any row for full community-signal enrichment.",
            ),
            "Badge": st.column_config.TextColumn("Rating", width="small"),
            "Opportunity Type": st.column_config.TextColumn("Type", width="medium"),
        },
    )

    # ── Detail Panel ─────────────────────────────────────────────────────────
    selected_rows = event.selection.rows if event and event.selection else []

    if selected_rows:
        idx = selected_rows[0]
        row = filtered_df.iloc[idx]

        st.markdown("---")
        st.markdown(f"## 🔍 {row['Company']}")

        # Fire enrichment for this row (spinner inside the helper). Returns
        # instantly on the second open of the same row within a session.
        enrichment = get_row_enrichment(row)
        enriched_score = enrichment["score"]
        enriched_badge = score_badge(enriched_score)
        normalized_base = enrichment["breakdown"].get("normalized_base", row["Score"])
        delta = enriched_score - normalized_base

        det_col1, det_col2, det_col3 = st.columns(3)
        with det_col1:
            raw_case = row.get("_case_data") or {}
            docket_number = raw_case.get("docket_number", "N/A")
            st.markdown(f"**Case Number:** {docket_number}")
            st.markdown(f"**Filed:** {row['Filed']}")
        with det_col2:
            st.markdown(f"**Court:** {row['Court']}")
            st.markdown(f"**Chapter:** {row['Chapter']}")
        with det_col3:
            st.markdown(f"**Community Score:** {enriched_score}/100 — {enriched_badge}")
            st.caption(
                f"Base estimate: {normalized_base}/100 · Enriched: {enriched_score}/100 · "
                f"Delta from community signals: {delta:+d}"
            )

        chapter = row["Chapter"]
        if chapter == "Chapter 11":
            st.success(
                "**Chapter 11 — Reorganization:** This company is reorganizing. "
                "Assets may be available for community acquisition before private equity moves in."
            )
        elif chapter == "Chapter 7":
            st.warning(
                "**Chapter 7 — Liquidation:** This company is liquidating. "
                "Assets are being sold — community acquisition window is narrow but possible."
            )
        else:
            st.info(f"**{chapter}:** Filing type detected. Review case details for acquisition opportunity.")

        st.markdown(f"**Opportunity Type:** {row['Opportunity Type']}")

        breakdown = enrichment["breakdown"]
        if breakdown:
            sigs = breakdown.get("signals", {})
            sent = breakdown.get("sentiment", {})
            days = sigs.get("days_since_filing", 0)
            reddit_mentions = sigs.get("reddit_mentions", 0)
            reddit_score    = sigs.get("reddit_score", 0)
            news_articles   = sigs.get("news_articles", 0)
            news_score      = sigs.get("news_score", 0)
            trends_spike    = sigs.get("trends_spike", 0)
            trends_score    = sigs.get("trends_score", 0)
            signals_total   = breakdown.get("signals_total", 0)
            sentiment_pts   = breakdown.get("sentiment_points", 0)
            chapter_score   = breakdown.get("chapter_score", 0)
            category_score  = breakdown.get("category_score", 0)
            base_score      = breakdown.get("base_score", 15)
            total           = breakdown.get("total", row["Score"])

            # ── Community Signal volume ──
            st.markdown("**📊 Community Awareness Breakdown**")
            st.markdown("━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            st.markdown(f"🟠 **Reddit** — mentions since filing ({days} days ago): **{reddit_mentions} posts** &nbsp;`+{reddit_score} pts`", unsafe_allow_html=True)
            st.markdown(f"📰 **News** — articles since filing: **{news_articles} articles** &nbsp;`+{news_score} pts`", unsafe_allow_html=True)
            st.markdown(f"📈 **Google Trends** — peak interest: **{trends_spike}/100** &nbsp;`+{trends_score} pts`", unsafe_allow_html=True)

            # ── Sentiment analysis ──
            st.markdown("### 📊 Community Sentiment Analysis")
            s_col1, s_col2, s_col3 = st.columns(3)
            with s_col1:
                st.metric(
                    "Overall Sentiment",
                    sent.get("sentiment_label", "🟡 Neutral"),
                    f"Score: {sent.get('sentiment_score', 0)}",
                )
            with s_col2:
                st.metric(
                    "🏘️ Ownership Intent Posts",
                    sent.get("ownership_intent", 0),
                    "buy/save/community language",
                )
            with s_col3:
                st.metric(
                    "💔 Nostalgia/Loss Posts",
                    sent.get("nostalgia_signals", 0),
                    "miss/love/bring back language",
                )

            neg = sent.get("negative_signals", 0)
            pos = sent.get("ownership_intent", 0) + sent.get("nostalgia_signals", 0)
            if neg > pos and neg > 5:
                st.warning(
                    f"⚠️ Negative sentiment dominates: {neg} dismissive posts vs "
                    f"{pos} supportive posts. Community ownership potential may be lower than volume suggests."
                )

            if sent.get("sample_posts"):
                st.markdown("**Sample community posts showing ownership/nostalgia signals:**")
                for post in sent["sample_posts"]:
                    st.markdown(
                        f"- {post['signal']}: [{post['title']}]({post['url']}) (👍 {post['score']} upvotes)"
                    )

            # ── Score breakdown (additive formula) ──
            st.markdown("━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            asset_pts = breakdown.get("asset_points", 0)
            rec_boost = breakdown.get("recency_boost", 0)
            pe_pts = breakdown.get("pe_flag", 0)
            size_pts = breakdown.get("size_points", 0)
            variance = breakdown.get("variance", 0)
            raw_score = breakdown.get("raw_score", 0)
            bonus = breakdown.get("enrichment_bonus", 0)
            total = breakdown.get("total", row["Score"])
            days_old_disp = breakdown.get("days_old")
            days_str = f"{days_old_disp} days old" if days_old_disp is not None else "date unknown"

            st.markdown(f"⚙️ **Base score:** 50")
            st.markdown(f"🏷️ **Asset type** ({breakdown.get('opportunity_type', '—')}): **+{asset_pts}**")
            rec_sign = "+" if rec_boost >= 0 else ""
            st.markdown(f"⏱️ **Recency** ({days_str}): **{rec_sign}{rec_boost}**")
            if pe_pts > 0:
                st.markdown(f"💰 **PE-backed flag** (extraction wedge applies): **+{pe_pts}**")
            st.markdown(f"🏢 **Scale** ({breakdown.get('estimated_size', 'medium')}): **+{size_pts}**")
            var_sign = "+" if variance >= 0 else ""
            st.markdown(f"🎲 **Per-name variance** (deterministic): **{var_sign}{variance}**")
            st.markdown("━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            st.markdown(f"**Base subtotal:** {raw_score}/100")
            if bonus > 0:
                st.markdown(f"**+ Enrichment bonus** ({signals_total} signals pts, {sentiment_pts} sentiment pts): **+{bonus}**")
            st.markdown(f"### 🏛️ TOTAL OWNERSHIP POTENTIAL: {total}/100")

        st.markdown("**Actions:**")
        act1, act2, act3 = st.columns(3)
        with act1:
            if st.button("🚀 Start Community Campaign", width="stretch", key="btn_campaign"):
                st.toast("Coming Soon — community campaign tools launching Q3 2026", icon="🚀")
        with act2:
            if st.button("🔔 Set Price Alert", width="stretch", key="btn_alert"):
                st.toast("Coming Soon — price alert system in development", icon="🔔")
        with act3:
            if st.button("📊 Request Full Analysis", width="stretch", key="btn_analysis"):
                st.toast("Coming Soon — analyst request queue launching soon", icon="📊")

        case_url = row.get("URL", "")
        if case_url:
            st.markdown(f"[View Full Case on CourtListener →]({case_url})", unsafe_allow_html=False)

    # ── Footer ───────────────────────────────────────────────────────────────
    _render_footer(filtered_df)


def _render_footer(df: pd.DataFrame):
    st.markdown("---")
    st.markdown("### 📊 Aggregate Intelligence")

    now = datetime.now(timezone.utc)
    week_ago = now - timedelta(days=7)

    total = len(df)
    high_opp = len(df[df["Score"] >= 70]) if not df.empty else 0
    ch11 = len(df[df["Chapter"] == "Chapter 11"]) if not df.empty else 0

    filed_this_week = 0
    if not df.empty and "_filed_date" in df.columns:
        filed_this_week = df["_filed_date"].apply(
            lambda d: (
                d.replace(tzinfo=timezone.utc) >= week_ago
                if d is not None and d.tzinfo is None
                else d >= week_ago if d is not None
                else False
            )
        ).sum()

    f1, f2, f3, f4 = st.columns(4)
    f1.metric("Total Cases Monitored", total)
    f2.metric("🟢 High Opportunity Cases", high_opp)
    f3.metric("Chapter 11 (Reorganization)", ch11)
    f4.metric("Filed This Week", int(filed_this_week))

    st.caption(
        "People's Capital monitors all US federal bankruptcy filings in real time, scoring each for "
        "community ownership potential. Our mission: give communities the same intelligence that private "
        "equity firms use — before they move in."
    )
    st.markdown("""
<div class="footer-text">
    People's Capital — Signal Intelligence Platform · Applying to a16z Speedrun SR007 ·
    <a href="https://peoples-capital.streamlit.app" style="color: #303040;">peoples-capital.streamlit.app</a>
</div>
""", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
