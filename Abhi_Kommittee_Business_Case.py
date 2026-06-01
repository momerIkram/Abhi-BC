import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import date
from calendar import monthrange
from copy import deepcopy
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="Bachat × ABHI Microfinance Bank — Revenue Model",
    page_icon="🏦", layout="wide", initial_sidebar_state="expanded"
)

# ── ABHI Brand System ──────────────────────────────────────────────────────────
# Primary:  #00833E  (ABHI deep green)
# Accent:   #7DC242  (ABHI lime green)
# Dark:     #005C2B  (dark green)
# Surface:  #F4F9F6  (light green-tinted white)
# Card:     #FFFFFF
# Border:   #D6EAE0
# Text:     #1A2E22  (dark green-black)
# Muted:    #6B8F79
# Gold:     #E8A020  (highlight/alert — used sparingly)
# Red:      #D32F2F  (error/negative)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #F4F9F6;
    color: #1A2E22;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #FFFFFF;
    border-right: 1px solid #D6EAE0;
}
section[data-testid="stSidebar"] * { color: #1A2E22 !important; }
section[data-testid="stSidebar"] h2 { color: #00833E !important; font-weight: 700 !important; }
section[data-testid="stSidebar"] label {
    color: #005C2B !important;
    font-weight: 600 !important;
    font-size: 0.78rem !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
section[data-testid="stSidebar"] .stSlider > div > div > div {
    background: #00833E !important;
}
section[data-testid="stSidebar"] hr { border-color: #D6EAE0 !important; }
section[data-testid="stSidebar"] .stButton button {
    background: #00833E !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}
section[data-testid="stSidebar"] .stButton button:hover {
    background: #005C2B !important;
}

/* ── Main container ── */
.main .block-container {
    padding-top: 0;
    padding-left: 2rem;
    padding-right: 2rem;
    max-width: 1440px;
    background: #F4F9F6;
}

/* ── Header banner ── */
.abhi-header {
    background: linear-gradient(135deg, #00833E 0%, #005C2B 60%, #003D1E 100%);
    padding: 2rem 2.5rem;
    border-radius: 0 0 16px 16px;
    margin: -1rem -2rem 1.5rem -2rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.abhi-header-left h1 {
    color: #FFFFFF;
    font-size: 1.6rem;
    font-weight: 800;
    margin: 0;
    letter-spacing: -0.02em;
}
.abhi-header-left p {
    color: #7DC242;
    font-size: 0.82rem;
    margin: 0.3rem 0 0 0;
    font-weight: 500;
}
.abhi-logo-pill {
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(125,194,66,0.4);
    border-radius: 50px;
    padding: 0.5rem 1.2rem;
    color: white;
    font-size: 0.85rem;
    font-weight: 700;
    letter-spacing: 0.05em;
}
.abhi-logo-pill span { color: #7DC242; }

/* ── Section header ── */
.section-hdr {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin: 1.2rem 0 0.7rem 0;
}
.section-hdr-bar {
    width: 4px; height: 20px;
    background: #00833E;
    border-radius: 4px;
    display: inline-block;
}
.section-hdr-text {
    color: #005C2B;
    font-weight: 700;
    font-size: 0.82rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

/* ── KPI cards ── */
.kpi-card {
    background: #FFFFFF;
    border: 1px solid #D6EAE0;
    border-radius: 12px;
    padding: 1.1rem 1.3rem;
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: #00833E;
}
.kpi-card.gold::before { background: #E8A020; }
.kpi-card.lime::before { background: #7DC242; }
.kpi-card.red::before  { background: #D32F2F; }
.kpi-card .kpi-lbl {
    font-size: 0.68rem;
    color: #6B8F79;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.07em;
}
.kpi-card .kpi-val {
    font-size: 1.5rem;
    font-weight: 800;
    color: #1A2E22;
    margin: 0.2rem 0 0.1rem 0;
    letter-spacing: -0.02em;
}
.kpi-card .kpi-sub {
    font-size: 0.7rem;
    color: #6B8F79;
}

/* ── Milestone cards ── */
.ms-card-unlocked {
    background: #FFFFFF;
    border: 1px solid #7DC242;
    border-left: 4px solid #00833E;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 0.8rem;
}
.ms-card-pending {
    background: #FAFAFA;
    border: 1px solid #E0E0E0;
    border-left: 4px solid #BDBDBD;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 0.8rem;
    opacity: 0.7;
}
.ms-badge-unlocked {
    background: #E8F5EE;
    color: #00833E;
    border: 1px solid #7DC242;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 700;
}
.ms-badge-pending {
    background: #F5F5F5;
    color: #9E9E9E;
    border: 1px solid #E0E0E0;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 700;
}

/* ── Calc breakdown box ── */
.calc-box {
    background: #F4F9F6;
    border: 1px solid #D6EAE0;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    font-size: 0.82rem;
    color: #1A2E22;
    line-height: 1.9;
}
.calc-box .cb-lbl  { color: #6B8F79; font-weight: 600; font-size: 0.72rem; text-transform: uppercase; }
.calc-box .cb-val  { color: #1A2E22; font-weight: 600; }
.calc-box .cb-result { color: #00833E; font-weight: 800; font-size: 1rem; }
.calc-box .cb-release { color: #005C2B; font-weight: 800; font-size: 1.15rem; }
.calc-box .cb-neg  { color: #D32F2F; font-weight: 700; }
.calc-box .cb-pos  { color: #7DC242; font-weight: 700; }

/* ── Legal banner ── */
.legal-banner {
    background: #E8F5EE;
    border: 1px solid #7DC242;
    border-left: 4px solid #00833E;
    border-radius: 10px;
    padding: 0.9rem 1.2rem;
    font-size: 0.81rem;
    color: #1A2E22;
    line-height: 1.7;
    margin: 0.8rem 0;
}
.legal-banner b { color: #00833E; }

/* ── Rate display ── */
.rate-pill {
    background: #00833E;
    color: white;
    padding: 0.4rem 1rem;
    border-radius: 50px;
    font-size: 0.85rem;
    font-weight: 700;
    display: inline-block;
    margin: 0.3rem 0;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: #FFFFFF;
    border-bottom: 2px solid #D6EAE0;
    border-radius: 0;
    gap: 0;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    border-radius: 0;
    color: #6B8F79;
    font-weight: 600;
    font-size: 0.82rem;
    padding: 0.7rem 1.4rem;
    border-bottom: 2px solid transparent;
    margin-bottom: -2px;
}
.stTabs [aria-selected="true"] {
    background: transparent !important;
    color: #00833E !important;
    border-bottom: 2px solid #00833E !important;
}

/* ── Table ── */
.stDataFrame { border-radius: 10px; overflow: hidden; border: 1px solid #D6EAE0; }
.stDataFrame thead tr th {
    background: #E8F5EE !important;
    color: #005C2B !important;
    font-weight: 700 !important;
}

/* ── Inputs ── */
.stNumberInput input, .stTextInput input {
    border-color: #D6EAE0 !important;
    border-radius: 8px !important;
}
.stNumberInput input:focus, .stTextInput input:focus {
    border-color: #00833E !important;
    box-shadow: 0 0 0 2px rgba(0,131,62,0.15) !important;
}

/* ── Success / info ── */
.stSuccess { background: #E8F5EE !important; border-color: #7DC242 !important; color: #005C2B !important; }
.stInfo    { background: #E8F5EE !important; border-color: #00833E !important; }

/* ── Expander ── */
.streamlit-expanderHeader {
    background: #FFFFFF !important;
    border: 1px solid #D6EAE0 !important;
    border-radius: 10px !important;
    color: #1A2E22 !important;
    font-weight: 600 !important;
}
.streamlit-expanderContent {
    border: 1px solid #D6EAE0 !important;
    border-top: none !important;
    border-radius: 0 0 10px 10px !important;
}

/* ── Toggle ── */
.stToggle > label { color: #005C2B !important; }

/* ── Metric ── */
[data-testid="stMetric"] { background: #FFFFFF; border-radius: 10px; padding: 0.8rem; border: 1px solid #D6EAE0; }
[data-testid="stMetricLabel"] { color: #6B8F79 !important; font-size: 0.75rem !important; }
[data-testid="stMetricValue"] { color: #1A2E22 !important; font-weight: 700 !important; }

/* ── Divider ── */
hr { border-color: #D6EAE0 !important; }
</style>
""", unsafe_allow_html=True)

# ── Plotly theme matching ABHI brand ──────────────────────────────────────────
PLOT_BG   = "#FFFFFF"
PLOT_PAPER = "#F4F9F6"
GRID_CLR  = "#E8F0EC"
FONT_CLR  = "#1A2E22"
C_GREEN   = "#00833E"
C_LIME    = "#7DC242"
C_DARK    = "#005C2B"
C_GOLD    = "#E8A020"
C_RED     = "#D32F2F"
C_MUTED   = "#6B8F79"
C_SURFACE = "#F4F9F6"

def abhi_layout(height=380, title=""):
    return dict(
        plot_bgcolor=PLOT_BG, paper_bgcolor=PLOT_PAPER,
        font=dict(color=FONT_CLR, family="Inter", size=11),
        title=dict(text=title, font=dict(color=C_DARK, size=13, weight=700)) if title else {},
        xaxis=dict(gridcolor=GRID_CLR, linecolor="#D6EAE0", tickcolor="#D6EAE0"),
        yaxis=dict(gridcolor=GRID_CLR, linecolor="#D6EAE0", tickcolor="#D6EAE0"),
        height=height,
        margin=dict(l=60, r=40, t=40 if title else 20, b=50),
        legend=dict(orientation="h", yanchor="bottom", y=1.02,
                    xanchor="right", x=1, bgcolor="rgba(0,0,0,0)",
                    font=dict(size=11)),
        hovermode="x unified",
    )

# ── Helpers ────────────────────────────────────────────────────────────────────
def month_index_to_ym(sy, sm, mi):
    t = sm - 1 + mi
    return sy + (t-1)//12, ((t-1)%12)+1

def held_days_exact(dm, pm, dd=1, pd_=15, sy=2024):
    dy,mo = month_index_to_ym(sy,1,dm)
    py,pm_ = month_index_to_ym(sy,1,pm)
    d0 = date(dy,mo,min(dd,monthrange(dy,mo)[1]))
    d1 = date(py,pm_,min(pd_,monthrange(py,pm_)[1]))
    return (d1-d0).days

def fmt_pkr(v):
    if v is None or (isinstance(v,float) and np.isnan(v)): return "—"
    if v>=1_000_000: return f"PKR {v/1_000_000:.2f}M"
    if v>=1_000:     return f"PKR {v/1_000:.1f}K"
    return f"PKR {v:,.0f}"

def fmt_pkr_full(v):
    if v is None or (isinstance(v,float) and np.isnan(v)): return "—"
    return f"PKR {v:,.0f}"

def shdr(icon, text):
    st.markdown(
        f'<div class="section-hdr">'
        f'<span class="section-hdr-bar"></span>'
        f'<span class="section-hdr-text">{icon}&nbsp; {text}</span>'
        f'</div>', unsafe_allow_html=True)

def kpi(label, value, sub="", accent="green"):
    cls = {"green":"","gold":"gold","lime":"lime","red":"red"}.get(accent,"")
    st.markdown(
        f'<div class="kpi-card {cls}">'
        f'<div class="kpi-lbl">{label}</div>'
        f'<div class="kpi-val">{value}</div>'
        f'<div class="kpi-sub">{sub}</div>'
        f'</div>', unsafe_allow_html=True)

# ── Core computation ───────────────────────────────────────────────────────────
def compute_pool_metrics(tmpl):
    s,c = tmpl["slots"], tmpl["contrib"]
    sz  = tmpl["size"]
    paying  = [i for i in range(1,sz+1) if not s[i]["blocked"]]
    blocked = [i for i in range(1,sz+1) if s[i]["blocked"]]
    pv = sz*c
    avg_fee = np.mean([s[i]["fee_pct"]/100 for i in paying]) if paying else 0.0
    return dict(paying_slots=paying, blocked_slots=blocked,
                pool_value=pv, cash_per_month=len(paying)*c, avg_fee=avg_fee)

def compute_forecast(templates, glob, months):
    adj_sign  = 1 if glob["rate_adj_sign"]=="plus" else -1
    net_rate  = glob["sbp_rate"] + adj_sign * glob["rate_adj"]
    abhi_s    = glob["abhi_share"]/100
    bachat_s  = glob["bachat_share"]/100
    def_rate  = glob["default_rate"]/100
    def_pre   = glob["default_pre_pct"]/100
    def_post  = glob["default_post_pct"]/100
    pen_pct   = glob["penalty_pct"]/100
    rec_r     = glob["recovery_rate"]/100
    fee_mode  = glob["fee_mode"]
    dd, pd_   = glob["deposit_day"], glob["payout_day"]
    milestones = sorted(glob["milestones"], key=lambda x: x["pools"])

    active = [t for t in templates if t["active"]]
    cum_by_tmpl = {i:0 for i in range(len(active))}
    ms_unlocked = set()
    cum_bachat  = 0.0
    cg_by_month = {}
    rows, ms_rows = [], []

    for m in range(1, months+1):
        agg = dict(cum_pools=0, paying_members=0, total_float=0,
                   gross_fee=0, base_nii=0, fee_nii=0, pg_nii=0, total_nii=0,
                   total_cg=0, def_loss=0, net_def_loss=0, def_fees=0,
                   total_rev=0, gross_profit=0,
                   abhi_fee=0, bachat_fee=0, abhi_cg=0, bachat_cg=0, total_bachat=0)

        for ti, tmpl in enumerate(active):
            cum_by_tmpl[ti] += tmpl["pools_per_month"]
            cp   = cum_by_tmpl[ti]
            sz   = tmpl["size"]
            con  = tmpl["contrib"]
            slts = tmpl["slots"]
            paying = [s for s in range(1,sz+1) if not slts[s]["blocked"]]
            pv   = sz * con
            total_float_t   = pv * cp
            total_deposits  = len(paying) * con * cp

            # Fee
            if fee_mode == "Upfront":
                gf = sum(slts[s]["fee_pct"]/100 * pv for s in paying) * cp
            else:
                gf = sum(slts[s]["fee_pct"]/100 * con for s in paying) * cp

            # NII — 3 components
            bn = fn = pgn = 0.0
            for s in paying:
                pay_m = m + s
                dp    = cp * con
                fa    = slts[s]["fee_pct"]/100 * pv * cp
                dh    = held_days_exact(m, pay_m, dd, pd_)
                r     = net_rate/100
                bn   += dp   * r * (dh/365)
                fn   += fa   * r * (dh/365)
                pgn  += total_float_t * r * (dh/365)
            total_nii_t = bn + fn + pgn

            # Capital gain — simple monthly accrual on full float
            cg_t = total_float_t * (net_rate/100) / 12

            # Defaults
            tot_def = (total_deposits * def_rate * def_pre +
                       total_deposits * def_rate * def_post)
            rec     = tot_def * rec_r
            net_def = tot_def - rec
            def_f   = tot_def * pen_pct

            # Revenue
            rev_t    = gf + total_nii_t + def_f
            profit_t = rev_t - net_def

            agg["cum_pools"]      += cp
            agg["paying_members"] += cp * len(paying)
            agg["total_float"]    += total_float_t
            agg["gross_fee"]      += gf
            agg["base_nii"]       += bn
            agg["fee_nii"]        += fn
            agg["pg_nii"]         += pgn
            agg["total_nii"]      += total_nii_t
            agg["total_cg"]       += cg_t
            agg["def_loss"]       += tot_def
            agg["net_def_loss"]   += net_def
            agg["def_fees"]       += def_f
            agg["total_rev"]      += rev_t
            agg["gross_profit"]   += profit_t
            agg["abhi_fee"]       += gf   * abhi_s
            agg["bachat_fee"]     += gf   * bachat_s
            agg["abhi_cg"]        += cg_t * abhi_s
            agg["bachat_cg"]      += cg_t * bachat_s
            agg["total_bachat"]   += (gf + cg_t) * bachat_s

        cg_by_month[m] = agg["total_cg"]
        cum_bachat += agg["total_bachat"]

        rows.append({
            "Month":                    m,
            "Cumulative Pools":         agg["cum_pools"],
            "Paying Members":           agg["paying_members"],
            "Total Float (PKR)":        agg["total_float"],
            "Gross Fee Income":         agg["gross_fee"],
            "Base NII":                 agg["base_nii"],
            "Fee NII":                  agg["fee_nii"],
            "Pool Growth NII":          agg["pg_nii"],
            "Total NII":                agg["total_nii"],
            "Monthly Cap Gain (Total)": agg["total_cg"],
            "ABHI Cap Gain (60%)":      agg["abhi_cg"],
            "Bachat Cap Gain (40%)":    agg["bachat_cg"],
            "Net Default Loss":         agg["net_def_loss"],
            "Default Penalty Fees":     agg["def_fees"],
            "Total Revenue":            agg["total_rev"],
            "Gross Profit":             agg["gross_profit"],
            "ABHI Fee Share":           agg["abhi_fee"],
            "Bachat Fee Share":         agg["bachat_fee"],
            "Total Bachat Revenue":     agg["total_bachat"],
            "Cumulative Bachat Revenue":cum_bachat,
        })

    df = pd.DataFrame(rows)

    # Milestone calc — each release = Bachat 40% of cap gain since LAST milestone
    prev_m = 0
    for i, ms in enumerate(milestones):
        tgt   = ms["pools"]
        match = df[df["Cumulative Pools"] >= tgt]
        if match.empty:
            ms_rows.append(dict(ms_num=i+1, pool_target=tgt, status="PENDING",
                unlock_month=None, prev_ms_month=prev_m, float_at_unlock=None,
                months_covered=None, cap_gain_period=None,
                bachat_40pct=None, release_amount=None, delta=None))
            continue
        um  = int(match.iloc[0]["Month"])
        fv  = match.iloc[0]["Total Float (PKR)"]
        period = list(range(prev_m+1, um+1))
        cgp = sum(cg_by_month.get(mm,0) for mm in period)
        b40 = cgp * bachat_s
        usr = ms.get("release", 0)
        rel = usr if usr > 0 else b40
        ms_rows.append(dict(ms_num=i+1, pool_target=tgt, status="UNLOCKED",
            unlock_month=um, prev_ms_month=prev_m, float_at_unlock=fv,
            months_covered=len(period), cap_gain_period=cgp,
            bachat_40pct=b40, release_amount=rel, delta=rel-b40))
        prev_m = um

    return df, pd.DataFrame(ms_rows)

# ── Session state ──────────────────────────────────────────────────────────────
def default_template(name="Pool A", size=10, contrib=10000):
    fr = {1:0,2:0,3:6,4:5,5:4,6:3,7:2,8:1,9:0.5,10:0}
    return {"name":name,"size":size,"contrib":contrib,"pools_per_month":5,
            "slots":{s:{"blocked":s<=2,"fee_pct":fr.get(s,2.0)} for s in range(1,size+1)},
            "active":True}

if "templates" not in st.session_state:
    st.session_state.templates = [default_template("Template A — 10-slot / PKR 10k",10,10000)]

if "global" not in st.session_state:
    st.session_state["global"] = {
        "sbp_rate":22.0,"rate_adj":2.0,"rate_adj_sign":"plus",
        "abhi_share":60.0,"bachat_share":40.0,
        "forecast_months":24,"fee_mode":"Monthly",
        "deposit_day":1,"payout_day":15,
        "default_rate":2.0,"default_pre_pct":30.0,"default_post_pct":70.0,
        "penalty_pct":2.0,"recovery_rate":50.0,"ms_auto":True,
        "milestones":[
            {"pools":50,  "release":0},{"pools":100, "release":0},
            {"pools":150, "release":0},{"pools":250, "release":0},
            {"pools":500, "release":0},{"pools":1000,"release":0},
        ]
    }

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        '<div style="padding:.5rem 0 1rem 0">'
        '<div style="font-size:1.2rem;font-weight:800;color:#00833E">ABHI</div>'
        '<div style="font-size:0.7rem;color:#6B8F79;font-weight:500">× Bachat · Model Parameters</div>'
        '</div>', unsafe_allow_html=True)

    g = st.session_state["global"]

    st.markdown('<p style="color:#005C2B;font-weight:700;font-size:.75rem;text-transform:uppercase;letter-spacing:.06em">📈 Capital Gain Rate</p>', unsafe_allow_html=True)
    g["sbp_rate"] = st.slider("SBP Policy Rate %", 10.0, 35.0, g["sbp_rate"], 0.25)
    c1,c2 = st.columns([1,2])
    with c1:
        g["rate_adj_sign"] = st.radio("±",["plus","minus"],
            format_func=lambda x:"+" if x=="plus" else "−",
            index=0 if g["rate_adj_sign"]=="plus" else 1)
    with c2:
        g["rate_adj"] = st.number_input("Adj %", 0.0, 15.0, g["rate_adj"], 0.25, format="%.2f")
    adj_v  = 1 if g["rate_adj_sign"]=="plus" else -1
    net    = g["sbp_rate"] + adj_v * g["rate_adj"]
    g["_net"] = net
    sign_s = "+" if g["rate_adj_sign"]=="plus" else "−"
    st.markdown(
        f'<div class="rate-pill">SBP {g["sbp_rate"]:.2f}% {sign_s} {g["rate_adj"]:.2f}% = {net:.2f}% p.a.</div>'
        f'<div style="font-size:.68rem;color:#6B8F79;margin-top:.3rem">Per Bachat × ABHI JV agreement</div>',
        unsafe_allow_html=True)

    st.divider()
    st.markdown('<p style="color:#005C2B;font-weight:700;font-size:.75rem;text-transform:uppercase;letter-spacing:.06em">🤝 Revenue Share</p>', unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1: g["abhi_share"] = st.number_input("ABHI %",0,100,int(g["abhi_share"]),5)
    with c2:
        g["bachat_share"] = 100 - g["abhi_share"]
        st.metric("Bachat %",f"{g['bachat_share']}%")

    st.divider()
    st.markdown('<p style="color:#005C2B;font-weight:700;font-size:.75rem;text-transform:uppercase;letter-spacing:.06em">📅 Dates & Fee Mode</p>', unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1: g["deposit_day"] = st.number_input("Deposit Day",1,28,g["deposit_day"])
    with c2: g["payout_day"]  = st.number_input("Payout Day",1,28,g["payout_day"])
    g["fee_mode"] = st.radio("Fee Mode",["Monthly","Upfront"],
        index=0 if g["fee_mode"]=="Monthly" else 1, horizontal=True)

    st.divider()
    st.markdown('<p style="color:#005C2B;font-weight:700;font-size:.75rem;text-transform:uppercase;letter-spacing:.06em">⚠️ Default Parameters</p>', unsafe_allow_html=True)
    g["default_rate"]    = st.slider("Default Rate %",0.0,20.0,g["default_rate"],0.5)
    g["penalty_pct"]     = st.slider("Penalty Fee %",0.0,10.0,g["penalty_pct"],0.5)
    g["recovery_rate"]   = st.slider("Recovery Rate %",0.0,100.0,g["recovery_rate"],5.0)
    c1,c2 = st.columns(2)
    with c1: g["default_pre_pct"]  = st.number_input("Pre-Payout %",0,100,int(g["default_pre_pct"]))
    with c2: g["default_post_pct"] = st.number_input("Post-Payout %",0,100,int(g["default_post_pct"]))

    st.divider()
    g["forecast_months"] = st.slider("Forecast Horizon (months)",6,60,g["forecast_months"],6)

    st.divider()
    st.markdown('<p style="color:#005C2B;font-weight:700;font-size:.75rem;text-transform:uppercase;letter-spacing:.06em">🏆 Milestone Targets</p>', unsafe_allow_html=True)
    g["ms_auto"] = st.toggle("Auto-compute from cap gain",value=g.get("ms_auto",True))
    for i,ms in enumerate(g["milestones"]):
        c1,c2 = st.columns(2)
        with c1: ms["pools"]   = st.number_input(f"MS{i+1} Pools",1,10000,ms["pools"],key=f"msp_{i}")
        with c2:
            if g["ms_auto"]:
                ms["release"] = 0
                st.markdown('<div style="font-size:.68rem;color:#6B8F79;padding-top:.8rem">Auto</div>',
                            unsafe_allow_html=True)
            else:
                ms["release"] = st.number_input(f"PKR",0,50000000,ms["release"],
                                                 100000,key=f"msr_{i}",format="%d")

    st.divider()
    if st.button("➕ Add Pool Template", use_container_width=True):
        ns = list("ABCDEFGHIJ")
        n  = len(st.session_state.templates)
        st.session_state.templates.append(
            default_template(f"Template {ns[min(n,9)]} — New",10,10000))
        st.rerun()

# ── Header ─────────────────────────────────────────────────────────────────────
adj_v2 = 1 if g["rate_adj_sign"]=="plus" else -1
net2   = g["sbp_rate"] + adj_v2 * g["rate_adj"]
sign_s2= "+" if g["rate_adj_sign"]=="plus" else "−"
st.markdown(f"""
<div class="abhi-header">
  <div class="abhi-header-left">
    <h1>Bachat × ABHI Microfinance Bank</h1>
    <p>Capital Gain Milestone Justification Model &nbsp;·&nbsp;
       SBP Policy Rate {g['sbp_rate']:.2f}% {sign_s2} {g['rate_adj']:.2f}% = {net2:.2f}% p.a. &nbsp;·&nbsp;
       {g['abhi_share']:.0f}% / {g['bachat_share']:.0f}% Revenue Share</p>
  </div>
  <div class="abhi-logo-pill">ABHI <span>×</span> BACHAT</div>
</div>
""", unsafe_allow_html=True)

# ── Compute ─────────────────────────────────────────────────────────────────────
df, df_ms = compute_forecast(st.session_state.templates, g, g["forecast_months"])

tab1, tab2, tab3, tab4 = st.tabs([
    "🏆  Milestone Justification",
    "🏗️   Pool Templates",
    "📈  Forecast",
    "📊  NII & Revenue",
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — MILESTONE JUSTIFICATION
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    unlocked = df_ms[df_ms["status"]=="UNLOCKED"]
    total_cg_all  = df["Monthly Cap Gain (Total)"].sum()
    total_b40     = df["Bachat Cap Gain (40%)"].sum()
    total_rel     = unlocked["bachat_40pct"].sum() if not unlocked.empty else 0
    total_fee     = df["Bachat Fee Share"].sum()
    shortfall     = total_b40 - total_rel

    shdr("📌","Capital Gain Release Summary")
    k = st.columns(5)
    with k[0]: kpi("Total Cap Gain (ABHI)", fmt_pkr(total_cg_all), f"{g['forecast_months']}M", "green")
    with k[1]: kpi("Bachat 40% Entitlement", fmt_pkr(total_b40), "theoretical", "lime")
    with k[2]: kpi("Total Milestone Releases", fmt_pkr(total_rel), f"{len(unlocked)} milestones", "green")
    with k[3]: kpi("Remaining Shortfall", fmt_pkr(shortfall), "pending release", "gold")
    with k[4]: kpi("Bachat Fee Revenue", fmt_pkr(total_fee), "direct (SBP allowed)", "lime")

    st.markdown("""
    <div class="legal-banner">
      <b>⚖️ SBP Regulatory Framework</b><br>
      ABHI Microfinance Bank is <b>restricted by SBP from directly sharing capital gains</b> with
      third-party partners. As an agreed alternative, ABHI issues a <b>structured lump-sum milestone
      payment</b> each time the Bachat platform crosses a pool-count threshold. Each payment is
      calibrated to equal Bachat's <b>40% share of capital gain accrued on the float since the
      previous milestone</b>. This is structured as a <b>performance-linked service fee</b>
      tied to platform growth — not a direct profit-share — consistent with SBP guidelines.
    </div>
    """, unsafe_allow_html=True)

    shdr("📋","Milestone Breakdown — ABHI Release Justification")
    net_rate_display = g["_net"] if "_net" in g else net2

    for _, row in df_ms.iterrows():
        ms_num = int(row["ms_num"])
        tgt    = int(row["pool_target"])
        is_u   = row["status"] == "UNLOCKED"
        card   = "ms-card-unlocked" if is_u else "ms-card-pending"
        badge  = "ms-badge-unlocked" if is_u else "ms-badge-pending"
        badge_txt = "✅ UNLOCKED" if is_u else "⏳ PENDING"

        with st.expander(
            f"Milestone {ms_num}  ·  {tgt:,} Pools  "
            f"{'→  Release: ' + fmt_pkr(row['release_amount']) if is_u else '→  Not yet reached'}",
            expanded=(is_u and ms_num <= 3)
        ):
            st.markdown(
                f'<span class="{badge}">{badge_txt}</span>&nbsp;&nbsp;'
                f'<span style="color:#6B8F79;font-size:.8rem">Pool Target: <b style="color:#1A2E22">{tgt:,} active pools</b></span>',
                unsafe_allow_html=True)

            if not is_u:
                st.markdown(
                    f'<div style="color:#9E9E9E;font-size:.82rem;padding:.5rem 0">'
                    f'Target of {tgt:,} pools not reached within {g["forecast_months"]}-month horizon. '
                    f'Increase pools/month or extend forecast period.</div>',
                    unsafe_allow_html=True)
                continue

            prev_m   = int(row["prev_ms_month"])
            unlock_m = int(row["unlock_month"])
            n_months = int(row["months_covered"])
            cgp      = row["cap_gain_period"]
            b40      = row["bachat_40pct"]
            rel      = row["release_amount"]
            delta    = row["delta"]
            fv       = row["float_at_unlock"]

            c_info, c_calc = st.columns(2)

            with c_info:
                st.markdown(f"""
                <div class="calc-box">
                  <div class="cb-lbl">Milestone Details</div>
                  <div style="margin:.6rem 0">
                    <span class="cb-lbl">Pool Target Reached</span><br>
                    <span class="cb-val">Month {unlock_m} &nbsp;({tgt:,} active pools)</span>
                  </div>
                  <div style="margin:.6rem 0">
                    <span class="cb-lbl">Period Covered</span><br>
                    <span class="cb-val">Month {prev_m+1} → Month {unlock_m} ({n_months} month{'s' if n_months!=1 else ''})</span>
                  </div>
                  <div style="margin:.6rem 0">
                    <span class="cb-lbl">Float at Milestone</span><br>
                    <span class="cb-val">{fmt_pkr_full(fv)}</span>
                  </div>
                  <div style="margin:.6rem 0">
                    <span class="cb-lbl">Agreed Capital Gain Rate</span><br>
                    <span class="cb-val">SBP {g['sbp_rate']:.2f}% {sign_s2} {g['rate_adj']:.2f}% = </span>
                    <span class="cb-result">{net_rate_display:.2f}% p.a.</span>
                  </div>
                </div>
                """, unsafe_allow_html=True)

            with c_calc:
                delta_cls = "cb-pos" if delta >= 0 else "cb-neg"
                delta_lbl = "✓ Balanced" if abs(delta) < b40*0.05 else ("▲ Over-release" if delta>0 else "▼ Shortfall")
                st.markdown(f"""
                <div class="calc-box">
                  <div class="cb-lbl">Capital Gain Calculation</div>
                  <div style="margin:.6rem 0">
                    <span class="cb-lbl">Total Cap Gain — ABHI earns (period)</span><br>
                    Σ Float × {net_rate_display:.2f}% ÷ 12 over {n_months} months<br>
                    = <span class="cb-result">{fmt_pkr_full(cgp)}</span>
                  </div>
                  <div style="margin:.6rem 0">
                    <span class="cb-lbl">Bachat's {g['bachat_share']:.0f}% Entitlement</span><br>
                    {fmt_pkr_full(cgp)} × {g['bachat_share']:.0f}%<br>
                    = <span class="cb-result">{fmt_pkr_full(b40)}</span>
                  </div>
                  <div style="margin:.8rem 0 .3rem 0;padding-top:.8rem;border-top:1px solid #D6EAE0">
                    <span class="cb-lbl">ABHI releases to Bachat</span><br>
                    <span class="cb-release">{fmt_pkr_full(rel)}</span>
                  </div>
                  <div>
                    <span class="cb-lbl">Delta</span>&nbsp;
                    <span class="{delta_cls}">PKR {delta:+,.0f} — {delta_lbl}</span>
                  </div>
                </div>
                """, unsafe_allow_html=True)

            # Month-by-month table
            st.markdown('<div style="margin-top:.6rem;font-size:.78rem;font-weight:600;color:#005C2B">Month-by-Month Capital Gain Breakdown</div>', unsafe_allow_html=True)
            period_df = df[(df["Month"]>prev_m)&(df["Month"]<=unlock_m)][
                ["Month","Cumulative Pools","Total Float (PKR)",
                 "Monthly Cap Gain (Total)","Bachat Cap Gain (40%)"]].copy()
            period_df.columns = ["Month","Pools","Float (PKR)","Cap Gain — ABHI Earns","Bachat 40% Owed"]
            period_df["Pools"] = period_df["Pools"].apply(lambda x: f"{int(x):,}")
            for c in ["Float (PKR)","Cap Gain — ABHI Earns","Bachat 40% Owed"]:
                period_df[c] = period_df[c].apply(fmt_pkr_full)
            st.dataframe(period_df, use_container_width=True, hide_index=True)

    # ── Waterfall chart ────────────────────────────────────────────────────────
    if not unlocked.empty:
        st.divider()
        shdr("📊","Release vs Entitlement — Waterfall")

        ms_labels = [f"MS{int(r.ms_num)} · {int(r.pool_target):,} pools"
                     for _,r in unlocked.iterrows()]
        owed     = [r.bachat_40pct   for _,r in unlocked.iterrows()]
        releases = [r.release_amount for _,r in unlocked.iterrows()]

        fig = go.Figure()
        fig.add_trace(go.Bar(
            name=f"Bachat {g['bachat_share']:.0f}% Cap Gain Entitlement",
            x=ms_labels, y=owed,
            marker=dict(color="rgba(0,131,62,0.18)", line=dict(color=C_GREEN, width=2)),
            text=[fmt_pkr(v) for v in owed], textposition="outside",
            textfont=dict(color=C_DARK, size=11)))
        fig.add_trace(go.Bar(
            name="ABHI Release to Bachat",
            x=ms_labels, y=releases,
            marker_color=C_LIME,
            text=[fmt_pkr(v) for v in releases], textposition="inside",
            textfont=dict(color="#FFFFFF", size=11, weight=700)))
        fig.update_layout(**abhi_layout(380), barmode="overlay")
        st.plotly_chart(fig, use_container_width=True)

        # Cumulative position
        shdr("📈","Cumulative Position — Paid vs Owed")
        cum_owed = np.cumsum(owed)
        cum_rel  = np.cumsum(releases)
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=ms_labels, y=cum_owed, name="Cumulative Owed",
            line=dict(color=C_RED, width=2, dash="dash"),
            marker=dict(size=8, color=C_RED)))
        fig2.add_trace(go.Scatter(
            x=ms_labels, y=cum_rel, name="Cumulative Released",
            line=dict(color=C_GREEN, width=2.5),
            marker=dict(size=8, color=C_GREEN),
            fill="tonexty", fillcolor="rgba(0,131,62,0.07)"))
        fig2.update_layout(**abhi_layout(300))
        st.plotly_chart(fig2, use_container_width=True)

    # Summary table
    shdr("📋","Full Milestone Summary")
    ms_tbl = []
    for _,row in df_ms.iterrows():
        is_u = row["status"]=="UNLOCKED"
        ms_tbl.append({
            "MS #":              f"MS{int(row.ms_num)}",
            "Pool Target":       f"{int(row.pool_target):,}",
            "Month Unlocked":    str(int(row.unlock_month)) if is_u else "—",
            "Period (months)":   str(int(row.months_covered)) if is_u else "—",
            "Float at Unlock":   fmt_pkr(row.float_at_unlock) if is_u else "—",
            "Cap Gain (Period)": fmt_pkr(row.cap_gain_period) if is_u else "—",
            "Bachat 40% Owed":   fmt_pkr(row.bachat_40pct)   if is_u else "—",
            "ABHI Release":      fmt_pkr(row.release_amount) if is_u else "—",
            "Delta":             (f"PKR {row.delta:+,.0f}" if is_u else "—"),
            "Status":            "✅ UNLOCKED" if is_u else "⏳ PENDING",
        })
    st.dataframe(pd.DataFrame(ms_tbl), use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — POOL TEMPLATES
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    shdr("🏗️","Pool Templates")
    templates = st.session_state.templates
    to_del = None

    for ti, tmpl in enumerate(templates):
        with st.expander(
            f"{'✅' if tmpl['active'] else '⏸️'}  {tmpl['name']}", expanded=(ti==0)):
            cn,ca,cd = st.columns([4,1,1])
            with cn: tmpl["name"]   = st.text_input("Name",tmpl["name"],key=f"tn_{ti}")
            with ca: tmpl["active"] = st.toggle("Active",tmpl["active"],key=f"ta_{ti}")
            with cd:
                if len(templates)>1 and st.button("🗑️ Remove",key=f"del_{ti}"):
                    to_del = ti

            st.divider()
            c1,c2,c3,c4 = st.columns(4)
            with c1:
                new_sz = st.number_input("Pool Size",4,30,tmpl["size"],1,key=f"sz_{ti}")
                if new_sz != tmpl["size"]:
                    old = tmpl["slots"]
                    fr  = {1:0,2:0,3:6,4:5,5:4,6:3,7:2,8:1,9:0.5}
                    tmpl["size"]  = new_sz
                    tmpl["slots"] = {s: old.get(s,{"blocked":s<=2,"fee_pct":fr.get(s,2.0)})
                                     for s in range(1,new_sz+1)}
            with c2:
                opts = [5000,10000,15000,20000,25000]
                lbls = ["PKR 5,000","PKR 10,000","PKR 15,000","PKR 20,000","PKR 25,000"]
                idx  = opts.index(tmpl["contrib"]) if tmpl["contrib"] in opts else 1
                sel  = st.selectbox("Monthly Contrib / Slot",lbls,index=idx,key=f"ct_{ti}")
                tmpl["contrib"] = opts[lbls.index(sel)]
            with c3:
                tmpl["pools_per_month"] = st.number_input(
                    "New Pools / Month",1,500,tmpl["pools_per_month"],1,key=f"ppm_{ti}")
            with c4:
                db = st.number_input("Default Blocked (first N slots)",0,tmpl["size"],2,1,key=f"db_{ti}")
                if st.button("Apply Default",key=f"ap_{ti}",
                             help="Set first N slots as blocked"):
                    for s in range(1,tmpl["size"]+1):
                        tmpl["slots"][s]["blocked"] = (s<=db)
                    st.rerun()

            shdr("","Slot Configuration")
            slots,size = tmpl["slots"],tmpl["size"]
            per_row = 5
            for ri in range((size+per_row-1)//per_row):
                scols = st.columns(per_row)
                for ci in range(per_row):
                    s = ri*per_row+ci+1
                    if s>size: break
                    with scols[ci]:
                        blk = st.checkbox(
                            f"🔴 Slot {s}" if slots[s]["blocked"] else f"🟢 Slot {s}",
                            value=slots[s]["blocked"],key=f"blk_{ti}_{s}",
                            help="Blocked = platform-held, no cash collected")
                        slots[s]["blocked"] = blk
                        if not blk:
                            slots[s]["fee_pct"] = st.number_input(
                                "Fee %",0.0,20.0,float(slots[s]["fee_pct"]),
                                0.5,key=f"fee_{ti}_{s}",format="%.1f")
                        else:
                            st.caption("No fee")

            st.divider()
            m = compute_pool_metrics(tmpl)
            mc = st.columns(5)
            mc[0].metric("Paying Slots",  len(m["paying_slots"]))
            mc[1].metric("Blocked Slots", len(m["blocked_slots"]))
            mc[2].metric("Pool Value",    fmt_pkr(m["pool_value"]))
            mc[3].metric("Cash / Month",  fmt_pkr(m["cash_per_month"]))
            mc[4].metric("Avg Fee %",     f"{m['avg_fee']*100:.2f}%")

            badges = "".join(
                f'<span style="display:inline-block;'
                f'background:{"#E8F5EE;color:#00833E;border:1px solid #7DC242" if not slots[s]["blocked"] else "#FFEBEE;color:#D32F2F;border:1px solid #EF9A9A"};'
                f'border-radius:50%;width:30px;height:30px;line-height:28px;'
                f'text-align:center;font-size:.72rem;font-weight:700;margin:2px">{s}</span>'
                for s in range(1,size+1))
            st.markdown(f'<div style="margin:.5rem 0">{badges}</div>', unsafe_allow_html=True)
            st.caption("🔴 Blocked — platform-held, no cash collected  ·  🟢 Paying — fee applies")

    if to_del is not None:
        st.session_state.templates.pop(to_del)
        st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — FORECAST
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    last   = df.iloc[-1]
    months = g["forecast_months"]
    net_disp = g.get("_net", net2)

    shdr("📌","Forecast KPIs")
    k = st.columns(5)
    with k[0]: kpi("Active Pools", f"{int(last['Cumulative Pools']):,}", "end of horizon", "green")
    with k[1]: kpi("Float Under ABHI", fmt_pkr(last["Total Float (PKR)"]), "ABHI manages", "green")
    with k[2]: kpi("Monthly Cap Gain", fmt_pkr(last["Monthly Cap Gain (Total)"]),
                    f"@ {net_disp:.2f}% p.a.", "lime")
    with k[3]: kpi("Bachat Rev / Month", fmt_pkr(last["Total Bachat Revenue"]), "fee + cap 40%", "green")
    with k[4]: kpi(f"Cumul Bachat ({months}M)", fmt_pkr(last["Cumulative Bachat Revenue"]), "total", "gold")

    shdr("📈","Monthly Revenue")
    fig = make_subplots(specs=[[{"secondary_y":True}]])
    fig.add_trace(go.Bar(x=df["Month"],y=df["Bachat Fee Share"],
        name="Bachat Fee Share",marker_color=C_GREEN,
        hovertemplate="M%{x}<br>Fee: PKR %{y:,.0f}<extra></extra>"))
    fig.add_trace(go.Bar(x=df["Month"],y=df["Bachat Cap Gain (40%)"],
        name=f"Bachat Cap Gain ({g['bachat_share']:.0f}%)",marker_color=C_LIME,
        hovertemplate="M%{x}<br>Cap Gain: PKR %{y:,.0f}<extra></extra>"))
    fig.add_trace(go.Scatter(x=df["Month"],y=df["Cumulative Bachat Revenue"],
        name="Cumulative",line=dict(color=C_GOLD,width=2,dash="dot"),
        yaxis="y2",hovertemplate="M%{x}<br>Cum: PKR %{y:,.0f}<extra></extra>"))
    for _,row in df_ms[df_ms["status"]=="UNLOCKED"].iterrows():
        fig.add_vline(x=int(row.unlock_month),line_dash="dash",
                      line_color=C_MUTED,line_width=1,
                      annotation_text=f"MS{int(row.ms_num)}",
                      annotation_font_color=C_DARK,annotation_font_size=10)
    layout = abhi_layout(400)
    layout.update(barmode="stack",
                  yaxis2=dict(title="Cumulative PKR",overlaying="y",side="right",
                              gridcolor="rgba(0,0,0,0)"))
    fig.update_layout(**layout)
    st.plotly_chart(fig, use_container_width=True)

    ca,cb = st.columns(2)
    with ca:
        shdr("","Float & Cap Gain Growth")
        fig_f = go.Figure()
        fig_f.add_trace(go.Area(x=df["Month"],y=df["Total Float (PKR)"],
            name="Float",line=dict(color=C_GREEN,width=2),
            fillcolor="rgba(0,131,62,0.08)"))
        fig_f.add_trace(go.Scatter(x=df["Month"],y=df["Monthly Cap Gain (Total)"],
            name="Cap Gain/Month",line=dict(color=C_GOLD,width=2),yaxis="y2"))
        layout_f = abhi_layout(280)
        layout_f.update(yaxis2=dict(title="Cap Gain/Mo",overlaying="y",side="right",
                                    gridcolor="rgba(0,0,0,0)"))
        fig_f.update_layout(**layout_f)
        st.plotly_chart(fig_f, use_container_width=True)

    with cb:
        shdr("","ABHI vs Bachat Capital Gain Split")
        fig_s = go.Figure()
        fig_s.add_trace(go.Bar(x=df["Month"],y=df["ABHI Cap Gain (60%)"],
            name=f"ABHI {g['abhi_share']:.0f}%",marker_color=C_DARK))
        fig_s.add_trace(go.Bar(x=df["Month"],y=df["Bachat Cap Gain (40%)"],
            name=f"Bachat {g['bachat_share']:.0f}%",marker_color=C_LIME))
        layout_s = abhi_layout(280)
        layout_s["barmode"] = "stack"
        fig_s.update_layout(**layout_s)
        st.plotly_chart(fig_s, use_container_width=True)

    shdr("","Monthly Detail Table")
    disp = df[["Month","Cumulative Pools","Total Float (PKR)",
               "Monthly Cap Gain (Total)","Bachat Cap Gain (40%)",
               "Bachat Fee Share","Total Bachat Revenue",
               "Cumulative Bachat Revenue"]].copy()
    for c in disp.columns[2:]:
        disp[c] = disp[c].apply(lambda x: f"PKR {x:,.0f}")
    st.dataframe(disp, use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — NII & REVENUE
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    shdr("📊","NII Breakdown — Base + Fee + Pool Growth")
    st.markdown("""
    <div style="background:#F4F9F6;border:1px solid #D6EAE0;border-radius:10px;
                padding:.8rem 1.2rem;font-size:.81rem;color:#1A2E22;line-height:1.8;margin-bottom:1rem">
      <b style="color:#005C2B">Formula:</b>
      NII = Principal × (SBP Rate ± Adj) × (Days / 365) using exact calendar days<br>
      <b style="color:#005C2B">Base NII</b> — monthly deposits per slot held to payout &nbsp;·&nbsp;
      <b style="color:#005C2B">Fee NII</b> — fees sitting in ABHI account &nbsp;·&nbsp;
      <b style="color:#005C2B">Pool Growth NII</b> — full pool value from month 1
    </div>
    """, unsafe_allow_html=True)

    n1,n2,n3,n4 = st.columns(4)
    n1.metric("Base NII",        fmt_pkr(df["Base NII"].sum()))
    n2.metric("Fee NII",         fmt_pkr(df["Fee NII"].sum()))
    n3.metric("Pool Growth NII", fmt_pkr(df["Pool Growth NII"].sum()))
    n4.metric("Total NII",       fmt_pkr(df["Total NII"].sum()))

    fig_nii = go.Figure()
    for col,clr,nm in [
        ("Base NII",       C_GREEN, "Base NII"),
        ("Fee NII",        C_LIME,  "Fee NII"),
        ("Pool Growth NII",C_GOLD,  "Pool Growth NII"),
        ("Total NII",      C_DARK,  "Total NII"),
    ]:
        fig_nii.add_trace(go.Scatter(x=df["Month"],y=df[col],
            name=nm,line=dict(color=clr,width=2.5 if nm=="Total NII" else 2)))
    fig_nii.update_layout(**abhi_layout(360,"NII Components Over Time"))
    st.plotly_chart(fig_nii, use_container_width=True)

    ca,cb = st.columns(2)
    with ca:
        shdr("","Revenue Components")
        fig_rev = go.Figure()
        fig_rev.add_trace(go.Bar(x=df["Month"],y=df["Gross Fee Income"],
            name="Fee Income",marker_color=C_GREEN))
        fig_rev.add_trace(go.Bar(x=df["Month"],y=df["Total NII"],
            name="NII",marker_color=C_LIME))
        fig_rev.add_trace(go.Bar(x=df["Month"],y=df["Default Penalty Fees"],
            name="Default Penalties",marker_color=C_GOLD))
        layout_rv = abhi_layout(300,"Total Revenue")
        layout_rv["barmode"] = "stack"
        fig_rev.update_layout(**layout_rv)
        st.plotly_chart(fig_rev, use_container_width=True)

    with cb:
        shdr("","Default Impact")
        fig_def = go.Figure()
        fig_def.add_trace(go.Scatter(x=df["Month"],y=df["Net Default Loss"],
            name="Net Default Loss",line=dict(color=C_RED,width=2)))
        fig_def.add_trace(go.Scatter(x=df["Month"],y=df["Gross Profit"],
            name="Gross Profit",line=dict(color=C_GREEN,width=2),
            fill="tozeroy",fillcolor="rgba(0,131,62,0.07)"))
        fig_def.update_layout(**abhi_layout(300,"Gross Profit vs Default Loss"))
        st.plotly_chart(fig_def, use_container_width=True)

    shdr("","Full Monthly Table")
    full = df[["Month","Gross Fee Income","Total NII","Default Penalty Fees",
               "Total Revenue","Net Default Loss","Gross Profit",
               "ABHI Fee Share","Bachat Fee Share",
               "ABHI Cap Gain (60%)","Bachat Cap Gain (40%)"]].copy()
    for c in full.columns[1:]:
        full[c] = full[c].apply(lambda x: f"PKR {x:,.0f}")
    st.dataframe(full, use_container_width=True, hide_index=True)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:#FFFFFF;border-top:1px solid #D6EAE0;margin-top:2rem;
            padding:1rem 2rem;display:flex;justify-content:space-between;
            align-items:center;font-size:.72rem;color:#6B8F79;
            margin-left:-2rem;margin-right:-2rem">
  <span><b style="color:#00833E">ABHI Microfinance Bank</b> × Bachat · Internal Use Only · Otus Apps SMC Pvt. Ltd.</span>
  <span>Milestone Release = Bachat 40% of Cap Gain accrued since previous milestone</span>
</div>
""", unsafe_allow_html=True)
