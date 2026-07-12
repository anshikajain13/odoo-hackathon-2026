import streamlit as st
import pandas as pd
from datetime import datetime

# =============================================================================
# PAGE CONFIG
# =============================================================================

st.set_page_config(
    page_title="TransitOps | Fleet Management",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =============================================================================
# CUSTOM CSS — dark, professional, dispatch-console styling
# Native widget colors (buttons, radio, focus rings) come from
# .streamlit/config.toml. This CSS layers on cards, badges, tables & spacing.
# =============================================================================

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600;700&display=swap');

:root {
    --bg: #0B1120;
    --bg-secondary: #0F1729;
    --surface: #131B2E;
    --surface-hover: #1A2438;
    --border: #232D42;
    --text-primary: #E8ECF4;
    --text-secondary: #8B95A8;
    --text-muted: #5B6478;
    --accent: #F5A623;
    --accent-soft: rgba(245, 166, 35, 0.12);
    --success: #22C55E;
    --success-soft: rgba(34, 197, 94, 0.12);
    --danger: #EF4444;
    --danger-soft: rgba(239, 68, 68, 0.12);
    --info: #2DD4BF;
    --info-soft: rgba(45, 212, 191, 0.12);
}

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, sans-serif;
}

.stApp {
    background: radial-gradient(circle at top left, #0F1729 0%, #0B1120 55%);
}

/* Hide default Streamlit chrome clutter */
#MainMenu, footer {visibility: hidden;}

/* ---------- Sidebar ---------- */
[data-testid="stSidebar"] {
    background: var(--bg-secondary);
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.2rem;
}
.sidebar-brand {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 0 0.6rem 1.1rem 0.6rem;
    margin-bottom: 1rem;
    border-bottom: 1px solid var(--border);
}
.sidebar-brand .logo-badge {
    width: 38px; height: 38px;
    background: var(--accent-soft);
    border: 1px solid var(--accent);
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.2rem;
}
.sidebar-brand .brand-text .title {
    font-weight: 800; font-size: 1.05rem; color: var(--text-primary); line-height: 1.1;
}
.sidebar-brand .brand-text .subtitle {
    font-size: 0.72rem; color: var(--text-secondary); letter-spacing: 0.04em; text-transform: uppercase;
}
[data-testid="stSidebar"] .stRadio > div {
    display: flex; flex-direction: column; gap: 3px;
}
[data-testid="stSidebar"] .stRadio > div > label {
    background: transparent;
    border-radius: 10px;
    padding: 9px 12px;
    transition: background 0.15s ease;
    border: 1px solid transparent;
}
[data-testid="stSidebar"] .stRadio > div > label:hover {
    background: var(--surface-hover);
    border-color: var(--border);
}
[data-testid="stSidebar"] .stRadio p {
    font-size: 0.92rem;
    font-weight: 500;
    color: var(--text-primary);
}
.sidebar-footer {
    position: fixed;
    bottom: 1.1rem;
    padding: 0.6rem 0.9rem;
    font-size: 0.7rem;
    color: var(--text-muted);
    border-top: 1px solid var(--border);
    width: 15.5rem;
}

/* ---------- Page header ---------- */
.page-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    padding-bottom: 1rem;
    margin-bottom: 1.4rem;
    border-bottom: 1px solid var(--border);
}
.page-header .title {
    font-size: 1.65rem;
    font-weight: 800;
    color: var(--text-primary);
    margin: 0;
}
.page-header .subtitle {
    font-size: 0.9rem;
    color: var(--text-secondary);
    margin-top: 2px;
}
.page-header .badge {
    background: var(--surface);
    border: 1px solid var(--border);
    color: var(--text-secondary);
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 0.78rem;
    font-family: 'JetBrains Mono', monospace;
}

/* ---------- Metric cards ---------- */
.metric-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 18px 18px;
    display: flex;
    align-items: center;
    gap: 14px;
    transition: transform 0.15s ease, border-color 0.15s ease;
    height: 100%;
}
.metric-card:hover {
    transform: translateY(-2px);
    border-color: var(--accent);
}
.metric-icon {
    width: 42px; height: 42px;
    min-width: 42px;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.25rem;
}
.metric-label {
    font-size: 0.76rem;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.04em;
    font-weight: 600;
}
.metric-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--text-primary);
    line-height: 1.25;
}
.metric-sub {
    font-size: 0.72rem;
    color: var(--text-muted);
    margin-top: 1px;
}

/* ---------- Section cards (forms, tables) ---------- */
.section-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.3rem 1.4rem;
    margin-bottom: 1.2rem;
}
.section-card h4 {
    margin-top: 0;
    color: var(--text-primary);
    font-size: 1.02rem;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 8px;
}
.section-card .desc {
    color: var(--text-secondary);
    font-size: 0.82rem;
    margin-bottom: 1rem;
}

/* Streamlit's own bordered container (st.container(border=True)) */
[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 14px !important;
}

/* ---------- Forms & inputs ---------- */
[data-testid="stForm"] {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.3rem 1.4rem 0.6rem 1.4rem;
}
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input {
    background: var(--bg-secondary) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-primary) !important;
    border-radius: 8px !important;
}
[data-baseweb="select"] > div {
    background: var(--bg-secondary) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
}
label {
    color: var(--text-secondary) !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
}

/* ---------- Buttons ---------- */
.stButton > button, [data-testid="stFormSubmitButton"] button {
    border-radius: 9px !important;
    font-weight: 600 !important;
    padding: 0.5rem 1.3rem !important;
    transition: transform 0.12s ease, box-shadow 0.12s ease !important;
    border: none !important;
}
.stButton > button:hover, [data-testid="stFormSubmitButton"] button:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 16px rgba(245, 166, 35, 0.25);
}

/* ---------- DataFrame / tables ---------- */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border);
    border-radius: 12px;
    overflow: hidden;
}

/* ---------- Alerts ---------- */
[data-testid="stAlert"] {
    border-radius: 10px;
    border: 1px solid var(--border);
}

/* ---------- Activity feed ---------- */
.activity-row {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 10px 4px;
    border-bottom: 1px solid var(--border);
}
.activity-row:last-child { border-bottom: none; }
.activity-icon {
    width: 30px; height: 30px; min-width: 30px;
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.95rem;
    background: var(--surface-hover);
}
.activity-text { font-size: 0.86rem; color: var(--text-primary); }
.activity-time { font-size: 0.72rem; color: var(--text-muted); }

/* ---------- Divider spacing ---------- */
hr { border-color: var(--border) !important; }
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# =============================================================================
# SESSION STATE — same shape/keys as original app, untouched
# =============================================================================

if "vehicles" not in st.session_state:
    st.session_state.vehicles = pd.DataFrame({
        "Vehicle Number": ["MP04AB1234", "MP09XY5678"],
        "Type": ["Bus", "Truck"],
        "Status": ["Active", "Maintenance"]
    })

if "drivers" not in st.session_state:
    st.session_state.drivers = pd.DataFrame({
        "Name": ["Rahul Sharma", "Priya Patel"],
        "License": ["LIC123", "LIC456"],
        "Phone": ["9876543210", "9876501234"]
    })

if "maintenance" not in st.session_state:
    st.session_state.maintenance = pd.DataFrame(
        columns=["Vehicle Number", "Issue", "Cost", "Status"]
    )

if "fuel" not in st.session_state:
    st.session_state.fuel = pd.DataFrame(
        columns=["Vehicle Number", "Fuel (Liters)", "Cost"]
    )

if "trips" not in st.session_state:
    st.session_state.trips = pd.DataFrame({
        "Source": ["Bhopal"],
        "Destination": ["Indore"],
        "Vehicle": ["MP04AB1234"],
        "Driver": ["Rahul Sharma"],
        "Status": ["Running"]
    })


# =============================================================================
# HELPER FUNCTIONS — small, beginner-friendly UI building blocks
# =============================================================================

def page_header(title, subtitle, badge_text=None):
    """Renders a consistent header at the top of every page."""
    badge_html = f'<div class="badge">{badge_text}</div>' if badge_text else ""
    st.markdown(f"""
        <div class="page-header">
            <div>
                <p class="title">{title}</p>
                <p class="subtitle">{subtitle}</p>
            </div>
            {badge_html}
        </div>
    """, unsafe_allow_html=True)


def metric_card(icon, label, value, sublabel="", accent="#F5A623"):
    """Renders one premium metric card. Call inside a column."""
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon" style="background:{accent}22; color:{accent};">{icon}</div>
            <div>
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
                <div class="metric-sub">{sublabel}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)


def section_title(icon, title, desc=""):
    """Small heading used above forms/tables inside a card-like block."""
    st.markdown(f"""
        <h4 style="margin-bottom:2px;">{icon} {title}</h4>
        <p style="color:var(--text-secondary); font-size:0.82rem; margin-top:0; margin-bottom:0.8rem;">{desc}</p>
    """, unsafe_allow_html=True)


STATUS_ICONS = {
    "Active": "🟢", "Running": "🟢", "Closed": "🟢", "Completed": "🟢",
    "Maintenance": "🟡", "Open": "🟡", "Pending": "🟡",
    "Inactive": "⚪", "Cancelled": "🔴",
}


def decorate_status(df, column):
    """Returns a display-only copy of df with an icon prefixed to the
    status column, so the table reads at a glance. Original session_state
    data is never modified."""
    if df.empty or column not in df.columns:
        return df
    display_df = df.copy()
    display_df[column] = display_df[column].apply(
        lambda s: f"{STATUS_ICONS.get(s, '⚪')} {s}"
    )
    return display_df


def empty_state(message):
    st.markdown(f"""
        <div style="text-align:center; padding: 2rem 1rem; color: var(--text-muted);
                    border: 1px dashed var(--border); border-radius: 12px;">
            {message}
        </div>
    """, unsafe_allow_html=True)


# =============================================================================
# SIDEBAR NAVIGATION
# =============================================================================

with st.sidebar:
    st.markdown("""
        <div class="sidebar-brand">
            <div class="logo-badge">🚦</div>
            <div class="brand-text">
                <div class="title">TransitOps</div>
                <div class="subtitle">Fleet Management</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        [
            "📊  Dashboard",
            "🚌  Vehicles",
            "👤  Drivers",
            "🗺️  Trips",
            "🔧  Maintenance",
            "⛽  Fuel",
        ],
        label_visibility="collapsed"
    )
    # strip the icon back off so the rest of the logic stays unchanged
    page = page.split("  ")[1]

    st.markdown("""
        <div class="sidebar-footer">
            Built for Odoo Hackathon 2026<br>Frontend by the UI team
        </div>
    """, unsafe_allow_html=True)


# =============================================================================
# PAGE: DASHBOARD
# =============================================================================

if page == "Dashboard":

    page_header(
        "Transport Operations Dashboard",
        "Live overview of your fleet, drivers and trips",
        datetime.now().strftime("%d %b %Y")
    )

    active_trips = len(st.session_state.trips[st.session_state.trips["Status"] == "Running"])
    fuel_cost = st.session_state.fuel["Cost"].sum() if not st.session_state.fuel.empty else 0
    maintenance_cost = st.session_state.maintenance["Cost"].sum() if not st.session_state.maintenance.empty else 0

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        metric_card("🚌", "Total Vehicles", len(st.session_state.vehicles), accent="#F5A623")
    with c2:
        metric_card("👤", "Total Drivers", len(st.session_state.drivers), accent="#2DD4BF")
    with c3:
        metric_card("🗺️", "Active Trips", active_trips, accent="#22C55E")
    with c4:
        metric_card("🔧", "Maintenance Records", len(st.session_state.maintenance), accent="#EF4444")
    with c5:
        metric_card("⛽", "Fuel Expense", f"₹{fuel_cost:,.0f}", accent="#F5A623")

    st.write("")
    left, right = st.columns([1.6, 1])

    with left:
        with st.container(border=True):
            section_title("🗺️", "Recent Trips", "Latest journeys across your fleet")
            if st.session_state.trips.empty:
                empty_state("No trips recorded yet.")
            else:
                st.dataframe(
                    decorate_status(st.session_state.trips, "Status"),
                    use_container_width=True,
                    hide_index=True
                )

        with st.container(border=True):
            section_title("💰", "Cost Analytics", "Fuel vs. maintenance spend")
            cc1, cc2 = st.columns(2)
            with cc1:
                metric_card("⛽", "Fuel Cost", f"₹{fuel_cost:,.0f}", accent="#F5A623")
            with cc2:
                metric_card("🔧", "Maintenance Cost", f"₹{maintenance_cost:,.0f}", accent="#EF4444")

    with right:
        with st.container(border=True):
            section_title("🕒", "Recent Activity", "Latest entries across modules")

            activities = []
            for _, row in st.session_state.trips.tail(3).iterrows():
                activities.append(("🗺️", f"Trip created: {row['Source']} → {row['Destination']} "
                                          f"({row['Vehicle']}, {row['Driver']})"))
            for _, row in st.session_state.maintenance.tail(2).iterrows():
                activities.append(("🔧", f"Maintenance logged for {row['Vehicle Number']}: {row['Issue']}"))
            for _, row in st.session_state.fuel.tail(2).iterrows():
                activities.append(("⛽", f"Fuel refill for {row['Vehicle Number']}: "
                                          f"{row['Fuel (Liters)']} L (₹{row['Cost']})"))

            if not activities:
                empty_state("No activity yet — add a vehicle, driver or trip to get started.")
            else:
                rows_html = ""
                for icon, text in activities[-6:][::-1]:
                    rows_html += f"""
                        <div class="activity-row">
                            <div class="activity-icon">{icon}</div>
                            <div class="activity-text">{text}</div>
                        </div>
                    """
                st.markdown(rows_html, unsafe_allow_html=True)


# =============================================================================
# PAGE: VEHICLES
# =============================================================================

elif page == "Vehicles":

    page_header("Vehicle Management", "Add and track vehicles in your fleet")

    with st.form("add_vehicle_form", clear_on_submit=True):
        section_title("➕", "Add Vehicle", "Register a new vehicle to the fleet")

        col1, col2, col3 = st.columns(3)
        with col1:
            vehicle_no = st.text_input("Vehicle Number", placeholder="e.g. MP04AB1234")
        with col2:
            vehicle_type = st.selectbox("Vehicle Type", ["Bus", "Truck", "Van"])
        with col3:
            vehicle_status = st.selectbox("Status", ["Active", "Maintenance", "Inactive"])

        submitted = st.form_submit_button("Add Vehicle", use_container_width=True)

        if submitted:
            if vehicle_no.strip() == "":
                st.warning("Enter vehicle number")
            elif vehicle_no in st.session_state.vehicles["Vehicle Number"].values:
                st.error("Vehicle already exists")
            else:
                new_vehicle = pd.DataFrame({
                    "Vehicle Number": [vehicle_no],
                    "Type": [vehicle_type],
                    "Status": [vehicle_status]
                })
                st.session_state.vehicles = pd.concat(
                    [st.session_state.vehicles, new_vehicle], ignore_index=True
                )
                st.success("Vehicle added successfully")

    st.write("")

    with st.container(border=True):
        section_title("🚌", "Vehicle Records", f"{len(st.session_state.vehicles)} vehicles on record")

        fcol1, fcol2 = st.columns([2, 1])
        with fcol1:
            search_term = st.text_input("Search by vehicle number", placeholder="Type to search...")
        with fcol2:
            status_filter = st.selectbox("Filter by status", ["All", "Active", "Maintenance", "Inactive"])

        filtered = st.session_state.vehicles.copy()
        if search_term:
            filtered = filtered[
                filtered["Vehicle Number"].str.contains(search_term, case=False, na=False)
            ]
        if status_filter != "All":
            filtered = filtered[filtered["Status"] == status_filter]

        if filtered.empty:
            empty_state("No vehicles match your search/filter.")
        else:
            st.dataframe(
                decorate_status(filtered, "Status"),
                use_container_width=True,
                hide_index=True
            )


# =============================================================================
# PAGE: DRIVERS
# =============================================================================

elif page == "Drivers":

    page_header("Driver Management", "Maintain your roster of drivers")

    with st.form("add_driver_form", clear_on_submit=True):
        section_title("➕", "Add Driver", "Register a new driver")

        col1, col2, col3 = st.columns(3)
        with col1:
            driver_name = st.text_input("Driver Name", placeholder="e.g. Rahul Sharma")
        with col2:
            license_no = st.text_input("License Number", placeholder="e.g. LIC123")
        with col3:
            phone = st.text_input("Phone Number", placeholder="e.g. 9876543210")

        submitted = st.form_submit_button("Add Driver", use_container_width=True)

        if submitted:
            if driver_name.strip() == "":
                st.warning("Enter driver name")
            else:
                new_driver = pd.DataFrame({
                    "Name": [driver_name],
                    "License": [license_no],
                    "Phone": [phone]
                })
                st.session_state.drivers = pd.concat(
                    [st.session_state.drivers, new_driver], ignore_index=True
                )
                st.success("Driver added successfully")

    st.write("")

    with st.container(border=True):
        section_title("👤", "Driver Records", f"{len(st.session_state.drivers)} drivers on record")
        if st.session_state.drivers.empty:
            empty_state("No drivers added yet.")
        else:
            st.dataframe(st.session_state.drivers, use_container_width=True, hide_index=True)


# =============================================================================
# PAGE: TRIPS
# =============================================================================

elif page == "Trips":

    page_header("Trip Management", "Plan and track trips across your fleet")

    vehicle_list = st.session_state.vehicles["Vehicle Number"].tolist()
    driver_list = st.session_state.drivers["Name"].tolist()

    with st.container(border=True):
        section_title("➕", "Create Trip", "Assign a vehicle and driver to a new trip")

        if vehicle_list and driver_list:
            with st.form("create_trip_form", clear_on_submit=True):
                col1, col2 = st.columns(2)
                with col1:
                    source = st.text_input("Source", placeholder="e.g. Bhopal")
                with col2:
                    destination = st.text_input("Destination", placeholder="e.g. Indore")

                col3, col4 = st.columns(2)
                with col3:
                    vehicle = st.selectbox("Assign Vehicle", vehicle_list)
                with col4:
                    driver = st.selectbox("Assign Driver", driver_list)

                submitted = st.form_submit_button("Create Trip", use_container_width=True)

                if submitted:
                    if source.strip() and destination.strip():
                        new_trip = pd.DataFrame({
                            "Source": [source],
                            "Destination": [destination],
                            "Vehicle": [vehicle],
                            "Driver": [driver],
                            "Status": ["Running"]
                        })
                        st.session_state.trips = pd.concat(
                            [st.session_state.trips, new_trip], ignore_index=True
                        )
                        st.success("Trip created successfully")
                    else:
                        st.warning("Enter source and destination")
        else:
            empty_state("Add at least one vehicle and one driver before creating a trip.")

    st.write("")

    with st.container(border=True):
        section_title("🗺️", "Trip History", f"{len(st.session_state.trips)} trips recorded")
        if st.session_state.trips.empty:
            empty_state("No trips recorded yet.")
        else:
            st.dataframe(
                decorate_status(st.session_state.trips, "Status"),
                use_container_width=True,
                hide_index=True
            )


# =============================================================================
# PAGE: MAINTENANCE
# =============================================================================

elif page == "Maintenance":

    page_header("Maintenance Management", "Log and monitor vehicle maintenance")

    vehicle_list = st.session_state.vehicles["Vehicle Number"].tolist()

    with st.container(border=True):
        section_title("➕", "Add Maintenance Record", "Log an issue and its repair cost")

        if vehicle_list:
            with st.form("add_maintenance_form", clear_on_submit=True):
                col1, col2, col3 = st.columns(3)
                with col1:
                    vehicle = st.selectbox("Select Vehicle", vehicle_list)
                with col2:
                    issue = st.text_input("Issue", placeholder="e.g. Brake pad replacement")
                with col3:
                    cost = st.number_input("Maintenance Cost (₹)", min_value=0)

                submitted = st.form_submit_button("Add Maintenance Record", use_container_width=True)

                if submitted:
                    new_record = pd.DataFrame({
                        "Vehicle Number": [vehicle],
                        "Issue": [issue],
                        "Cost": [cost],
                        "Status": ["Open"]
                    })
                    st.session_state.maintenance = pd.concat(
                        [st.session_state.maintenance, new_record], ignore_index=True
                    )
                    st.success("Maintenance record added")
        else:
            empty_state("Add a vehicle first before logging maintenance.")

    st.write("")

    with st.container(border=True):
        section_title("🔧", "Maintenance Records", f"{len(st.session_state.maintenance)} records on file")
        if st.session_state.maintenance.empty:
            empty_state("No maintenance records yet.")
        else:
            st.dataframe(
                decorate_status(st.session_state.maintenance, "Status"),
                use_container_width=True,
                hide_index=True
            )


# =============================================================================
# PAGE: FUEL
# =============================================================================

elif page == "Fuel":

    page_header("Fuel Management", "Track fuel usage and cost per vehicle")

    vehicle_list = st.session_state.vehicles["Vehicle Number"].tolist()

    with st.container(border=True):
        section_title("➕", "Add Fuel Record", "Log a refill for a vehicle")

        if vehicle_list:
            with st.form("add_fuel_form", clear_on_submit=True):
                col1, col2, col3 = st.columns(3)
                with col1:
                    vehicle = st.selectbox("Select Vehicle", vehicle_list)
                with col2:
                    fuel_liters = st.number_input("Fuel (Liters)", min_value=1)
                with col3:
                    fuel_cost = st.number_input("Fuel Cost (₹)", min_value=0)

                submitted = st.form_submit_button("Add Fuel Record", use_container_width=True)

                if submitted:
                    new_fuel = pd.DataFrame({
                        "Vehicle Number": [vehicle],
                        "Fuel (Liters)": [fuel_liters],
                        "Cost": [fuel_cost]
                    })
                    st.session_state.fuel = pd.concat(
                        [st.session_state.fuel, new_fuel], ignore_index=True
                    )
                    st.success("Fuel record added")
        else:
            empty_state("Add a vehicle first before logging fuel.")

    st.write("")

    with st.container(border=True):
        total_fuel_cost = st.session_state.fuel["Cost"].sum() if not st.session_state.fuel.empty else 0
        section_title("⛽", "Fuel Records", f"{len(st.session_state.fuel)} records • ₹{total_fuel_cost:,.0f} total")
        if st.session_state.fuel.empty:
            empty_state("No fuel records yet.")
        else:
            st.dataframe(st.session_state.fuel, use_container_width=True, hide_index=True)