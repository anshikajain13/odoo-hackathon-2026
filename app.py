import streamlit as st

st.set_page_config(page_title="TransitOps", layout="wide")

st.sidebar.title("TransitOps")

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Vehicles", "Drivers", "Trips"]
)

if page == "Dashboard":
    st.title("Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Vehicles", "10")

    with col2:
        st.metric("Total Drivers", "8")

    with col3:
        st.metric("Active Trips", "5")

    st.subheader("Recent Activity")

    st.table({
        "Trip": ["Bhopal-Indore", "Indore-Ujjain"],
        "Status": ["Running", "Completed"]
    })

elif page == "Vehicles":
    st.title("Vehicle Management")

    vehicle_no = st.text_input("Vehicle Number")
    vehicle_type = st.selectbox(
        "Vehicle Type",
        ["Bus", "Truck", "Van"]
    )
    
    vehicle_status = st.selectbox(
    "Status",
    ["Active", "Maintenance", "Inactive"]
    )

    if st.button("Add Vehicle"):
        st.success("Vehicle Added Successfully")

    st.subheader("Vehicle List")

    st.table({
        "Vehicle No": ["MP04AB1234", "MP09XY5678"],
        "Type": ["Bus", "Truck"],
        "Status": ["Active", "Maintenance"]
    })

elif page == "Drivers":
    st.title("Driver Management")

    driver_name = st.text_input("Driver Name")
    license_no = st.text_input("License Number")
    phone = st.text_input("Phone Number")

    if st.button("Add Driver"):
        st.success("Driver Added Successfully")

    st.subheader("Driver List")

    st.table({
        "Name": ["Rahul", "Priya"],
        "License": ["LIC123", "LIC456"]
    })

elif page == "Trips":
    st.title("Trip Management")

    source = st.text_input("Source")
    destination = st.text_input("Destination")
    
    vehicle = st.selectbox(
        "Assign Vehicle",
        ["MP04AB1234", "MP09XY5678"]
    )

    driver = st.selectbox(
        "Assign Driver",
        ["Rahul", "Priya"]
    )

    if st.button("Create Trip"):
        st.success("Trip Created Successfully")

    st.subheader("Trips")

    st.table({
        "Source": ["Bhopal"],
        "Destination": ["Indore"],
        "Status": ["Running"]
    })
