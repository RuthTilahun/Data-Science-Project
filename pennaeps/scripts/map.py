
import streamlit as st
import pandas as pd
import plotly.express as px
import json

st.title("PA Solar PV Data Maps as of 2025")

# -------------------------------
# Load Processed Data
# -------------------------------
df = pd.read_csv('../data/processed_data.csv')

# Standardize the county names to uppercase
df['County'] = df['County'].str.upper()

# -------------------------------
# Aggregate Data by County
# -------------------------------
# Map 1: Cumulative Solar PV Capacity (MW in DC) by County using "Total NPC MW DC"
county_capacity = (
    df.groupby('County')['Total NPC MW DC']
    .sum()
    .reset_index()
    .rename(columns={'Total NPC MW DC': 'Solar PV Capacity (MW in DC)'})
)

# Map 2: Cumulative Number of Solar PV Systems Installed by County
# Here we assume each row is one installation.
county_systems = df.groupby('County').size().reset_index(name='Total PV Systems Installed (MW in DC)')


# -------------------------------
# Load GeoJSON for PA Counties
# -------------------------------
try:
    with open('../data/pa_counties.geojson') as f:
        pa_geo = json.load(f)
    st.write("county GeoJSON loaded successfully.")
except Exception as e:
    st.error(f"Error loading county GeoJSON: {e}")


# -------------------------------
# Create Choropleth Maps with Plotly Express
# -------------------------------

# Map 1: Cumulative Solar PV Capacity (MWdc)
fig_capacity = px.choropleth(
    county_capacity,
    geojson=pa_geo,
    locations='County',             # County names in your aggregated DataFrame
    featureidkey="properties.COUNTY_NAM", # Key in GeoJSON features that contains county name
    color='Solar PV Capacity (MW in DC)',
    color_continuous_scale="Blues",
    scope="usa"
)
fig_capacity.update_geos(fitbounds="locations", visible=False)
fig_capacity.update_layout(width=1000, height=500)
fig_capacity.update_layout(
    title={
        'text': "Total Solar PV Capacity (MW in DC) by County in PA",
        'x': 0.5,           # 0.5 centers the title horizontally
        'y': 0.9,          # 0.95 places the title at the top of the plot
        'xanchor': 'center' # anchors the title in the center
    }
)
fig_capacity.write_html("Map1.html")

# Map 2: Cumulative Number of Solar PV Systems Installed
fig_systems = px.choropleth(
    county_systems,
    geojson=pa_geo,
    locations='County',
    featureidkey="properties.COUNTY_NAM",
    color='Total PV Systems Installed (MW in DC)',
    color_continuous_scale="Purples",
    scope="usa"
)
fig_systems.update_geos(fitbounds="locations", visible=False)
fig_systems.update_layout(width=1000, height=500)
fig_systems.update_layout(
    title={
        'text': "Total Number of Solar PV Systems Installed by County in PA",
        'x': 0.5,           # 0.5 centers the title horizontally
        'y': 0.9,          # 0.9 places the title at the top of the plot
        'xanchor': 'center' # anchors the title in the center
    }
)
fig_systems.write_html("Map2.html")


# -------------------------------
# Display the Maps in the Dashboard
# -------------------------------
st.subheader("Map 1: Total Solar PV Capacity (MW$_{DC}$)")
st.plotly_chart(
    fig_capacity,
    use_container_width=False, width=2000, height=2000, config={
        "modeBarButtonsToRemove": ["zoom2d", "pan2d", "zoomIn2d", "zoomOut2d"],
        "displayModeBar": False
    }
)

st.subheader("Map 2: Total Number of Solar PV Systems Installed by County")
st.plotly_chart(
    fig_systems,
    use_container_width=False, width=2000, height=2000, config={
        "modeBarButtonsToRemove": ["zoom2d", "pan2d", "zoomIn2d", "zoomOut2d"],
        "displayModeBar": False
    }
)
