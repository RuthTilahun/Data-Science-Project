import pandas as pd
import plotly.express as px

# Load processed data

df = pd.read_csv('../data/processed_data.csv')

# Group by Year and sum the capacity (MWdc)
annual_capacity = df.groupby('Year')['Total NPC MW DC'].sum().reset_index()

# Rename column for clarity
annual_capacity.rename(columns={'Total NPC MW DC': 'Annual Capacity (MWdc)'}, inplace=True)


fig_annual_capacity = px.bar(
    annual_capacity,
    x='Year',
    y='Annual Capacity (MWdc)',
    title="Annual Solar PV Capacity (MWdc) Installed in PA",
    labels={'Annual Capacity (MWdc)': 'Solar Capacity (MWdc)', 'Year': 'Year'}
)
fig_annual_capacity.update_xaxes(tickmode='linear', dtick=1)
fig_annual_capacity.show()

#save figure

# Calculate the cumulative sum of annual capacities
annual_capacity['Cumulative Capacity (MWdc)'] = annual_capacity['Annual Capacity (MWdc)'].cumsum()

fig_cumulative_capacity = px.line(
    annual_capacity,
    x='Year',
    y='Cumulative Capacity (MWdc)',
    title="Cumulative Solar PV Capacity (MWdc) Installed in PA",
    labels={'Cumulative Capacity (MWdc)': 'Cumulative Capacity (MWdc)', 'Year': 'Year'},
    markers=True
)
fig_cumulative_capacity.show()
fig_cumulative_capacity.update_xaxes(tickmode='linear', dtick=1)
#save figure

# Count the number of installations per year
annual_systems = df.groupby('Year').size().reset_index(name='Systems Installed')

fig_annual_systems = px.bar(
    annual_systems,
    x='Year',
    y='Systems Installed',
    title="Annual Number of Solar PV Systems Installed in PA",
    labels={'Systems Installed': 'Number of Systems', 'Year': 'Year'}
)
fig_annual_systems.update_xaxes(tickmode='linear', dtick=1)
fig_annual_systems.show()
#save figure


# Calculate the cumulative sum of systems installed
annual_systems['Cumulative Systems Installed'] = annual_systems['Systems Installed'].cumsum()

fig_cumulative_systems = px.line(
    annual_systems,
    x='Year',
    y='Cumulative Systems Installed',
    title="Cumulative Number of Solar PV Systems Installed in PA",
    labels={'Cumulative Systems Installed': 'Cumulative Number of Systems', 'Year': 'Year'},
    markers=True
)
fig_cumulative_systems.update_xaxes(tickmode='linear', dtick=1)
fig_cumulative_systems.show()
#save figure

