import streamlit as st
import pandas as pd

st.set_page_config(page_title="TransitOps", layout="wide")

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

st.sidebar.title("TransitOps")

page = st.sidebar.radio(
    "Navigation",
    [
    "Dashboard",
    "Vehicles",
    "Drivers",
    "Trips",
    "Maintenance",
    "Fuel"
]
)

if page == "Dashboard":

    st.title("Transport Operations Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Vehicles",
            len(st.session_state.vehicles)
        )

    with col2:
        st.metric(
            "Total Drivers",
            len(st.session_state.drivers)
        )
        
    with col3:
       active_trips = len(
          st.session_state.trips[
              st.session_state.trips["Status"] == "Running"
          ]
       )

       st.metric(
           "Active Trips",
          active_trips
        )

    st.subheader("Recent Trips")

    st.dataframe(
   
        st.session_state.trips,
        use_container_width=True
    )
    
    st.subheader("Cost Analytics")

    total_fuel_cost = 0
    if not st.session_state.fuel.empty:
        total_fuel_cost = st.session_state.fuel["Cost"].sum()

    total_maintenance_cost = 0
    if not st.session_state.maintenance.empty:
        total_maintenance_cost = st.session_state.maintenance["Cost"].sum()

    total_cost = total_fuel_cost + total_maintenance_cost

    total_trips = len(st.session_state.trips)

    cost_per_trip = 0
    if total_trips > 0:
        cost_per_trip = total_cost / total_trips

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Fuel Cost", f"₹{total_fuel_cost}")

    with c2:
        st.metric("Maintenance Cost", f"₹{total_maintenance_cost}")

    with c3:
        st.metric("Total Cost", f"₹{total_cost}")

    with c4:
        st.metric("Cost Per Trip", f"₹{cost_per_trip:.2f}")

elif page == "Vehicles":

    st.title("Vehicle Management")

    vehicle_no = st.text_input(
        "Vehicle Number"
    )

    vehicle_type = st.selectbox(
        "Vehicle Type",
        ["Bus", "Truck", "Van"]
    )

    vehicle_status = st.selectbox(
        "Status",
        ["Active", "Maintenance", "Inactive"]
    )

    if st.button("Add Vehicle"):

        if vehicle_no:

            new_vehicle = pd.DataFrame({
                "Vehicle Number": [vehicle_no],
                "Type": [vehicle_type],
                "Status": [vehicle_status]
            })

            st.session_state.vehicles = pd.concat(
                [
                    st.session_state.vehicles,
                    new_vehicle
                ],
                ignore_index=True
            )

            st.success("Vehicle Added Successfully")

    st.subheader("Vehicle Records")

    st.dataframe(
        st.session_state.vehicles,
        use_container_width=True
    )

elif page == "Drivers":

    st.title("Driver Management")

    driver_name = st.text_input(
        "Driver Name"
    )

    license_no = st.text_input(
        "License Number"
    )

    phone = st.text_input(
        "Phone Number"
    )

    if st.button("Add Driver"):

        if driver_name:

            new_driver = pd.DataFrame({
                "Name": [driver_name],
                "License": [license_no],
                "Phone": [phone]
            })

            st.session_state.drivers = pd.concat(
                [
                    st.session_state.drivers,
                    new_driver
                ],
                ignore_index=True
            )

            st.success("Driver Added Successfully")

    st.subheader("Driver Records")

    st.dataframe(
        st.session_state.drivers,
        use_container_width=True
    )

elif page == "Trips":

    st.title("Trip Management")

    source = st.text_input(
        "Source"
    )

    destination = st.text_input(
        "Destination"
    )

    vehicle = st.selectbox(
        "Assign Vehicle",
        st.session_state.vehicles[
            "Vehicle Number"
        ].tolist()
    )

    driver = st.selectbox(
        "Assign Driver",
        st.session_state.drivers[
            "Name"
        ].tolist()
    )

    if st.button("Create Trip"):

        if source and destination:

            new_trip = pd.DataFrame({
                "Source": [source],
                "Destination": [destination],
                "Vehicle": [vehicle],
                "Driver": [driver],
                "Status": ["Running"]
            })

            st.session_state.trips = pd.concat(
                [
                    st.session_state.trips,
                    new_trip
                ],
                ignore_index=True
            )

            st.success("Trip Created Successfully")

    st.subheader("Trip Records")

    st.dataframe(
        st.session_state.trips,
        use_container_width=True
    )
    
elif page == "Maintenance":

    st.title("Maintenance Management")

    vehicle = st.selectbox(
        "Select Vehicle",
        st.session_state.vehicles["Vehicle Number"].tolist()
    )

    issue = st.text_input("Issue")

    cost = st.number_input(
        "Maintenance Cost",
        min_value=0
    )

    if st.button("Add Maintenance Record"):

        new_record = pd.DataFrame({
            "Vehicle Number": [vehicle],
            "Issue": [issue],
            "Cost": [cost],
            "Status": ["Open"]
        })

        st.session_state.maintenance = pd.concat(
            [
                st.session_state.maintenance,
                new_record
            ],
            ignore_index=True
        )

        st.success("Maintenance Record Added")

    st.subheader("Maintenance Records")

    st.dataframe(
        st.session_state.maintenance,
        use_container_width=True
    )
    
elif page == "Fuel":

    st.title("Fuel Management")

    vehicle = st.selectbox(
        "Vehicle",
        st.session_state.vehicles["Vehicle Number"].tolist()
    )

    fuel_liters = st.number_input(
        "Fuel (Liters)",
        min_value=1
    )

    fuel_cost = st.number_input(
        "Fuel Cost",
        min_value=0
    )

    if st.button("Add Fuel Record"):

        new_fuel = pd.DataFrame({
            "Vehicle Number": [vehicle],
            "Fuel (Liters)": [fuel_liters],
            "Cost": [fuel_cost]
        })

        st.session_state.fuel = pd.concat(
            [
                st.session_state.fuel,
                new_fuel
            ],
            ignore_index=True
        )

        st.success("Fuel Record Added")

    st.subheader("Fuel Records")

    st.dataframe(
        st.session_state.fuel,
        use_container_width=True
    )



