import streamlit as st
import os
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

# ── Re-use main.py's imports and logic ───────────────────────────────────────
from flight_search import FlightSearch
from data_manager import DataManager
from flight_data import find_cheapest_flight
from notification_manager import NotificationManager

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FlightDeals Dashboard",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;800&display=swap');

:root {
    --bg:        #05060f;
    --surface:   #0d1117;
    --card:      #131822;
    --border:    #1e2636;
    --accent:    #00d4ff;
    --accent2:   #ff6b35;
    --green:     #00ff87;
    --muted:     #4a5568;
    --text:      #e2e8f0;
    --text-dim:  #8892a4;
}

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}
.stApp { background: var(--bg); }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2rem 4rem; }

[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}

.hero {
    background: linear-gradient(135deg, #0a1628 0%, #0d1f3c 50%, #091220 100%);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 250px; height: 250px;
    background: radial-gradient(circle, rgba(0,212,255,.15) 0%, transparent 70%);
    border-radius: 50%;
}
.hero::after {
    content: '';
    position: absolute;
    bottom: -40px; left: -40px;
    width: 180px; height: 180px;
    background: radial-gradient(circle, rgba(255,107,53,.10) 0%, transparent 70%);
    border-radius: 50%;
}
.hero h1 {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 2.4rem;
    background: linear-gradient(90deg, #00d4ff, #ffffff 60%, #ff6b35);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0 0 .4rem;
}
.hero p {
    font-family: 'Space Mono', monospace;
    font-size: .8rem;
    color: var(--text-dim);
    margin: 0;
    letter-spacing: .08em;
}

.metric-grid { display: flex; gap: 1rem; margin-bottom: 2rem; flex-wrap: wrap; }
.metric-card {
    flex: 1; min-width: 160px;
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
}
.metric-card.blue::before   { background: linear-gradient(90deg, var(--accent), transparent); }
.metric-card.orange::before { background: linear-gradient(90deg, var(--accent2), transparent); }
.metric-card.green::before  { background: linear-gradient(90deg, var(--green), transparent); }
.metric-card.purple::before { background: linear-gradient(90deg, #a78bfa, transparent); }
.metric-label {
    font-family: 'Space Mono', monospace;
    font-size: .65rem;
    color: var(--text-dim);
    text-transform: uppercase;
    letter-spacing: .12em;
    margin-bottom: .5rem;
}
.metric-value {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 1.8rem;
    line-height: 1;
}
.metric-value.blue   { color: var(--accent); }
.metric-value.orange { color: var(--accent2); }
.metric-value.green  { color: var(--green); }
.metric-value.purple { color: #a78bfa; }
.metric-sub { font-size: .72rem; color: var(--text-dim); margin-top: .3rem; }

.section-title {
    font-family: 'Space Mono', monospace;
    font-size: .72rem;
    text-transform: uppercase;
    letter-spacing: .18em;
    color: var(--accent);
    margin: 0 0 1rem;
    display: flex; align-items: center; gap: .6rem;
}
.section-title::after {
    content: '';
    flex: 1; height: 1px;
    background: linear-gradient(90deg, var(--border), transparent);
}

.flight-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin-bottom: .8rem;
    display: flex; align-items: center; gap: 1.5rem;
}
.flight-card.deal {
    border-color: rgba(0,255,135,.35);
    background: linear-gradient(135deg, #0a1a12, var(--card));
}
.flight-city {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1.1rem;
    color: var(--text);
}
.flight-iata {
    font-family: 'Space Mono', monospace;
    font-size: .75rem;
    color: var(--text-dim);
}
.flight-price { font-family: 'Syne', sans-serif; font-weight: 800; font-size: 1.4rem; margin-left: auto; }
.flight-price.deal   { color: var(--green); }
.flight-price.normal { color: var(--text); }
.deal-badge {
    background: rgba(0,255,135,.15);
    border: 1px solid rgba(0,255,135,.4);
    color: var(--green);
    font-family: 'Space Mono', monospace;
    font-size: .6rem;
    text-transform: uppercase;
    letter-spacing: .12em;
    padding: .2rem .6rem;
    border-radius: 999px;
}
.stops-badge {
    font-family: 'Space Mono', monospace;
    font-size: .62rem;
    color: var(--accent2);
    background: rgba(255,107,53,.12);
    border: 1px solid rgba(255,107,53,.3);
    padding: .15rem .5rem;
    border-radius: 999px;
}
.dates {
    font-family: 'Space Mono', monospace;
    font-size: .68rem;
    color: var(--text-dim);
    line-height: 1.6;
}
.no-flight {
    font-family: 'Space Mono', monospace;
    font-size: .75rem;
    color: var(--muted);
}

.stButton > button {
    background: linear-gradient(135deg, #0080a0, #00d4ff22) !important;
    border: 1px solid var(--accent) !important;
    color: var(--accent) !important;
    font-family: 'Space Mono', monospace !important;
    font-size: .75rem !important;
    letter-spacing: .08em !important;
    border-radius: 8px !important;
    padding: .6rem 1.4rem !important;
}
.stButton > button:hover {
    background: var(--accent) !important;
    color: #000 !important;
}

.stTextInput input, .stNumberInput input {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
    font-family: 'Space Mono', monospace !important;
    font-size: .8rem !important;
}
label[data-testid="stWidgetLabel"] p {
    font-family: 'Space Mono', monospace !important;
    font-size: .7rem !important;
    text-transform: uppercase;
    letter-spacing: .1em;
    color: var(--text-dim) !important;
}

.log-box {
    background: #080b10;
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    font-family: 'Space Mono', monospace;
    font-size: .72rem;
    color: #4ade80;
    line-height: 1.8;
    max-height: 280px;
    overflow-y: auto;
}
.log-line.info   { color: #4ade80; }
.log-line.warn   { color: var(--accent2); }
.log-line.error  { color: #f87171; }
.log-line.accent { color: var(--accent); }

hr { border-color: var(--border) !important; margin: 1.5rem 0 !important; }

/* Dataframe theming */
[data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; }
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────
def check_env():
    required = ["SHEETY_ENDPOINT", "SHEETY_USERNAME", "SHEETY_PASSWORD",
                "AMADEUS_APIKEY", "AMADEUS_SECRET", "MY_EMAIL", "MY_PASSWORD"]
    return [k for k in required if not os.environ.get(k)]


# ── Session state ─────────────────────────────────────────────────────────────
defaults = {"results": [], "logs": [], "sheet_data": [], "customers": []}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


def add_log(msg, level="info"):
    ts = datetime.now().strftime("%H:%M:%S")
    st.session_state.logs.append({"ts": ts, "msg": msg, "level": level})


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:.8rem 0 1.4rem'>
        <div style='font-family:Syne,sans-serif;font-weight:800;font-size:1.3rem;
                    background:linear-gradient(90deg,#00d4ff,#fff);
                    -webkit-background-clip:text;-webkit-text-fill-color:transparent;'>
            ✈ FlightDeals
        </div>
        <div style='font-family:Space Mono,monospace;font-size:.62rem;
                    color:#4a5568;letter-spacing:.1em;margin-top:.2rem;'>CONTROL PANEL</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**⚙️ Configuration**")
    origin = st.text_input("Origin City (IATA)", value="LON", max_chars=3,
                           help="3-letter IATA code e.g. LON, JFK, DXB")

    st.markdown("**📅 Date Range**")
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        depart_date = st.date_input(
            "From",
            value=datetime.now().date() + timedelta(days=1),
            min_value=datetime.now().date() + timedelta(days=1),
        )
    with col_d2:
        return_date = st.date_input(
            "To",
            value=datetime.now().date() + timedelta(days=180),
            min_value=datetime.now().date() + timedelta(days=2),
        )

    if return_date <= depart_date:
        st.error("'To' date must be after 'From' date.")

    send_emails = st.checkbox("Send email alerts", value=True)

    st.divider()
    st.markdown("**🔑 Environment**")
    missing_env = check_env()
    if missing_env:
        st.error(f"Missing: `{'`, `'.join(missing_env)}`")
    else:
        st.success("All credentials loaded ✓")

    st.divider()
    st.markdown("""
    <div style='font-family:Space Mono,monospace;font-size:.62rem;color:#4a5568;line-height:2;'>
    Amadeus API · Sheety · Gmail SMTP
    </div>
    """, unsafe_allow_html=True)


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>✈ Flight Deals Tracker</h1>
    <p>REAL-TIME FARE MONITORING · AMADEUS API · AUTOMATED ALERTS</p>
    <p style='margin-top:.8rem;font-size:.72rem;color:#ff6b35;letter-spacing:.04em;'>
        ⚠️ Running on Amadeus free test API — results may be limited and searches may take longer than usual.
    </p>
</div>
""", unsafe_allow_html=True)

# ── Buttons ───────────────────────────────────────────────────────────────────
c1, c2, c3, _ = st.columns([1, 1, 1, 4])
run_search = c1.button("🔍 Run Search")
load_sheet = c2.button("📋 Load Sheet")
clear_logs = c3.button("🗑 Clear Logs")

if run_search:
    st.session_state["confirmed_run"] = True

if clear_logs:
    st.session_state.logs = []
    st.rerun()

# ── Load sheet ────────────────────────────────────────────────────────────────
if load_sheet and not missing_env:
    with st.spinner("Loading destinations…"):
        try:
            dm = DataManager()
            st.session_state.sheet_data = dm.get_destination_data()
            st.session_state.customers  = dm.get_customer_details()
            add_log(f"Loaded {len(st.session_state.sheet_data)} destinations", "accent")
            add_log(f"Loaded {len(st.session_state.customers)} subscribers", "info")
        except Exception as e:
            add_log(f"Error: {e}", "error")
            st.error(str(e))
elif load_sheet and missing_env:
    st.error("Missing environment variables — check sidebar.")

# ── Run search  (logic mirrors main.py exactly) ───────────────────────────────
if st.session_state.get("confirmed_run") and not missing_env:
    st.session_state["confirmed_run"] = False
    if return_date <= depart_date:
        st.error("Fix the date range in the sidebar before running.")
    else:
        st.session_state.results = []
        add_log("━━━━ Search started ━━━━", "accent")

        # --- same date range as main.py ---
        tomorrow   = datetime.combine(depart_date, datetime.min.time())
        six_months = datetime.combine(return_date, datetime.min.time())
        progress   = st.progress(0, text="Initialising…")

        try:
            # --- same setup as main.py ---
            flight_search = FlightSearch()
            data_manager  = DataManager()
            notification  = NotificationManager() if send_emails else None
            add_log("Amadeus token obtained", "info")

            # --- get sheet data (main.py: sheet_data = data_manager.get_destination_data()) ---
            sheet_data = st.session_state.sheet_data or data_manager.get_destination_data()

            # --- get customer emails (main.py: customer_data = data_manager.get_customer_details()) ---
            customer_data      = st.session_state.customers or data_manager.get_customer_details()
            customer_email_list = [row["whatIsYourEmail?"] for row in customer_data]

            # --- fill missing IATA codes (main.py loop) ---
            for row in sheet_data:
                if row["iataCode"] == "":
                    row["iataCode"] = flight_search.get_destination_code(row["city"])
                    time.sleep(2)
            data_manager.update_destination_codes(sheet_data)
            st.session_state.sheet_data = sheet_data
            st.session_state.customers  = customer_data

            # --- search flights (main.py loop) ---
            for idx, row in enumerate(sheet_data):
                city = row.get("city", "?")
                iata = row.get("iataCode", "N/A")
                add_log(f"Searching flights to {city}…", "info")
                progress.progress((idx + 1) / len(sheet_data), text=f"Searching {city}…")

                # direct flights first (main.py)
                flights  = flight_search.check_flights(
                    origin.upper(), iata, tomorrow, six_months, is_direct=True
                )
                cheapest = find_cheapest_flight(flights)

                # if no direct flights, check indirect (main.py)
                if cheapest.price == "N/A":
                    add_log(f"  No direct flights. Checking stopover flights…", "warn")
                    flights  = flight_search.check_flights(
                        origin.upper(), iata, tomorrow, six_months, is_direct=False
                    )
                    cheapest = find_cheapest_flight(flights)

                add_log(f"  Cheapest price found: £{cheapest.price}", "info")

                # email trigger (main.py condition)
                is_deal = (
                    cheapest.price != "N/A"
                    and float(row.get("lowestPrice", 99999)) > float(cheapest.price)
                )

                st.session_state.results.append({
                    "city":        city,
                    "iata":        iata,
                    "price":       cheapest.price,
                    "out_date":    cheapest.out_date,
                    "return_date": cheapest.return_date,
                    "stops":       cheapest.stops,
                    "threshold":   row.get("lowestPrice", "N/A"),
                    "is_deal":     is_deal,
                })

                if is_deal:
                    add_log(f"  💚 Price lower than sheet value — sending email!", "info")
                    if notification:
                        notification.notification(
                            price=cheapest.price,
                            origin=origin.upper(),
                            destination=city,
                            from_date=cheapest.out_date,
                            to_date=cheapest.return_date,
                            emails=customer_email_list,
                        )
                        add_log(f"  📧 EMAIL SENT to {len(customer_email_list)} subscriber(s)", "accent")
                else:
                    add_log(f"  No cheaper flight found.", "warn")

            progress.progress(1.0, text="Search complete ✓")
            add_log("━━━━ Search complete ━━━━", "accent")

        except Exception as e:
            add_log(f"ERROR: {e}", "error")
            st.error(str(e))

elif run_search and missing_env:
    st.error("Cannot run — missing environment variables.")


# ── Metric cards ──────────────────────────────────────────────────────────────
results = st.session_state.results
deals   = [r for r in results if r["is_deal"]]
valid_prices = [float(r["price"]) for r in results if r["price"] != "N/A"]
avg_price = sum(valid_prices) / len(valid_prices) if valid_prices else 0

st.markdown(f"""
<div class="metric-grid">
  <div class="metric-card blue">
    <div class="metric-label">Watchlist</div>
    <div class="metric-value blue">{len(st.session_state.sheet_data) or "—"}</div>
    <div class="metric-sub">destinations</div>
  </div>
  <div class="metric-card green">
    <div class="metric-label">Deals Found</div>
    <div class="metric-value green">{len(deals) or "—"}</div>
    <div class="metric-sub">below threshold</div>
  </div>
  <div class="metric-card orange">
    <div class="metric-label">Avg Price</div>
    <div class="metric-value orange">{"£{:.0f}".format(avg_price) if avg_price else "—"}</div>
    <div class="metric-sub">across routes</div>
  </div>
  <div class="metric-card purple">
    <div class="metric-label">Subscribers</div>
    <div class="metric-value purple">{len(st.session_state.customers) or "—"}</div>
    <div class="metric-sub">alert recipients</div>
  </div>
</div>
""", unsafe_allow_html=True)


# ── Results + Log columns ─────────────────────────────────────────────────────
col_main, col_side = st.columns([2, 1])

with col_main:
    st.markdown('<div class="section-title">🛫 Flight Results</div>', unsafe_allow_html=True)

    if not results:
        st.markdown("""
        <div style='text-align:center;padding:3.5rem 2rem;background:#0d1117;
                    border:1px dashed #1e2636;border-radius:12px;
                    font-family:Space Mono,monospace;font-size:.78rem;color:#4a5568;'>
            Run a search to see results here
        </div>
        """, unsafe_allow_html=True)
    else:
        sorted_r = sorted(results, key=lambda r: (not r["is_deal"], float(r["price"]) if r["price"] != "N/A" else 99999))
        for r in sorted_r:
            cc = "flight-card deal" if r["is_deal"] else "flight-card"
            pc = "deal" if r["is_deal"] else "normal"
            ps = f"£{r['price']}" if r["price"] != "N/A" else "N/A"
            deal_b  = '<span class="deal-badge">🔥 DEAL</span>' if r["is_deal"] else ""
            stops   = r["stops"]
            stops_b = (f'<span class="stops-badge">{stops} stop(s)</span>'
                       if stops not in (0, "N/A", "0")
                       else '<span class="stops-badge" style="color:#4a5568;border-color:#1e2636;">direct</span>')
            thresh  = f"Threshold: £{r['threshold']}" if r["threshold"] != "N/A" else ""
            dates   = (f'<div class="dates">Out: {r["out_date"]}<br>Ret: {r["return_date"]}</div>'
                       if r["out_date"] != "N/A" else '<div class="no-flight">No flights</div>')

            st.markdown(f"""
            <div class="{cc}">
                <div style='font-size:1.4rem;flex:0 0 auto'>{"🟢" if r["is_deal"] else "🔵"}</div>
                <div style='flex:1'>
                    <div class="flight-city">{r["city"]}</div>
                    <div class="flight-iata">{r["iata"]} · {thresh}</div>
                </div>
                {dates}
                <div style='display:flex;flex-direction:column;align-items:flex-end;gap:.4rem'>
                    <div class="flight-price {pc}">{ps}</div>
                    <div style='display:flex;gap:.4rem'>{stops_b}{deal_b}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

with col_side:
    st.markdown('<div class="section-title">📟 Activity Log</div>', unsafe_allow_html=True)
    logs_html = "".join(
        f'<div class="log-line {e["level"]}"><span style="color:#4a5568">{e["ts"]}</span>  {e["msg"]}</div>'
        for e in reversed(st.session_state.logs[-60:])
    ) or '<div class="log-line info">Waiting for activity…</div>'
    st.markdown(f'<div class="log-box">{logs_html}</div>', unsafe_allow_html=True)

    if deals:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-title">🏆 Best Deal</div>', unsafe_allow_html=True)
        bd = min(deals, key=lambda r: float(r["price"]))
        st.markdown(f"""
        <div class="flight-card deal" style='flex-direction:column;align-items:flex-start;gap:.5rem'>
            <div style='font-family:Syne,sans-serif;font-weight:800;font-size:1.4rem;color:#00ff87'>
                {bd['city']} — £{bd['price']}
            </div>
            <div style='font-family:Space Mono,monospace;font-size:.68rem;color:#8892a4;line-height:1.8'>
                {bd['iata']} · Out: {bd['out_date']}<br>
                Return: {bd['return_date']}<br>
                Threshold was £{bd['threshold']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    if st.session_state.customers:
        with st.expander(f"👥 Subscribers ({len(st.session_state.customers)})"):
            for c in st.session_state.customers:
                em = c.get("whatIsYourEmail?", "—")
                fn = c.get("whatIsYourFirstName?", "")
                ln = c.get("whatIsYourLastName?", "")
                st.markdown(
                    f"<div style='font-family:Space Mono,monospace;font-size:.7rem;"
                    f"color:#8892a4;padding:.25rem 0'>{fn} {ln} — {em}</div>",
                    unsafe_allow_html=True,
                )

# ── Watchlist table ───────────────────────────────────────────────────────────
if st.session_state.sheet_data:
    st.divider()
    st.markdown('<div class="section-title">📊 Destination Watchlist</div>', unsafe_allow_html=True)
    import pandas as pd
    df = pd.DataFrame(st.session_state.sheet_data)
    cols = [c for c in ["city", "iataCode", "lowestPrice"] if c in df.columns]
    st.dataframe(
        df[cols].rename(columns={"city": "Destination", "iataCode": "IATA", "lowestPrice": "Threshold (£)"}),
        use_container_width=True,
        hide_index=True,
    )
