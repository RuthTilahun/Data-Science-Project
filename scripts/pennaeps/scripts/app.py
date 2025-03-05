import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------
# Load the Processed Data
# -------------------------------
df = pd.read_csv('../data/processed_data.csv')

# -------------------------------
# Annual Solar PV Capacity (MWdc)
# -------------------------------
# Group by Year and sum the capacity (MWdc)
annual_capacity = df.groupby('Year')['Total NPC MW DC'].sum().reset_index()

# Rename column for clarity
annual_capacity.rename(columns={'Total NPC MW DC': 'Annual Capacity (MWdc)'}, inplace=True)

# Create a bar chart for annual capacity
fig_annual_capacity = px.bar(
    annual_capacity,
    x='Year',
    y='Annual Capacity (MWdc)',
    title="Annual Solar PV Capacity (MWdc) Installed in PA",
    labels={'Annual Capacity (MWdc)': 'Solar Capacity (MWdc)', 'Year': 'Year'}
)

# -------------------------------
# Cumulative Solar PV Capacity (MWdc)
# -------------------------------
# Calculate the cumulative sum of annual capacities
annual_capacity['Cumulative Capacity (MWdc)'] = annual_capacity['Annual Capacity (MWdc)'].cumsum()

# Create a line chart for cumulative capacity
fig_cumulative_capacity = px.line(
    annual_capacity,
    x='Year',
    y='Cumulative Capacity (MWdc)',
    title="Cumulative Solar PV Capacity (MWdc) Installed in PA",
    labels={'Cumulative Capacity (MWdc)': 'Cumulative Capacity (MWdc)', 'Year': 'Year'},
    markers=True
)

# -------------------------------
# Annual Number of Solar PV Systems Installed
# -------------------------------
# Count the number of installations per year
annual_systems = df.groupby('Year').size().reset_index(name='Systems Installed')

# Create a bar chart for the annual system count
fig_annual_systems = px.bar(
    annual_systems,
    x='Year',
    y='Systems Installed',
    title="Annual Number of Solar PV Systems Installed in PA",
    labels={'Systems Installed': 'Number of Systems', 'Year': 'Year'}
)

# -------------------------------
# Cumulative Number of Solar PV Systems Installed
# -------------------------------
# Calculate the cumulative sum of systems installed
annual_systems['Cumulative Systems Installed'] = annual_systems['Systems Installed'].cumsum()

# Create a line chart for cumulative system count
fig_cumulative_systems = px.line(
    annual_systems,
    x='Year',
    y='Cumulative Systems Installed',
    title="Cumulative Number of Solar PV Systems Installed in PA",
    labels={'Cumulative Systems Installed': 'Cumulative Number of Systems', 'Year': 'Year'},
    markers=True
)

# -------------------------------
# Build the Streamlit Dashboard Layout
# -------------------------------
st.title("PSEA Solar PV Data Dashboard")
st.header("Visualizations for Solar PV Installations in PA")

st.subheader("Annual Solar PV Capacity (MWdc)")
st.plotly_chart(fig_annual_capacity, use_container_width=True)

st.subheader("Cumulative Solar PV Capacity (MWdc)")
st.plotly_chart(fig_cumulative_capacity, use_container_width=True)

st.subheader("Annual Number of Solar PV Systems Installed")
st.plotly_chart(fig_annual_systems, use_container_width=True)

st.subheader("Cumulative Number of Solar PV Systems Installed")
st.plotly_chart(fig_cumulative_systems, use_container_width=True)
