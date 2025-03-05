import streamlit as st
import pandas as pd

# --------------------------------------------------
# 1. Load the Data
# --------------------------------------------------
df = pd.read_csv("../data/processed_data.csv")

# --------------------------------------------------
# 2. Define Capacity Ranges (in MW) and Labels
# --------------------------------------------------
# The bin edges are in MW. For example:
#   0.015 MW = 15 kW
#   0.25 MW = 250 kW
#   1 MW = 1 MW, etc.
bins = [0, 0.015, 0.25, 1, 3, 5, 10, float('inf')]
labels = [
    "≤ 15 kW",
    "> 15 kW to ≤ 250 kW",
    "> 250 kW to ≤ 1 MW",
    "> 1 MW to ≤ 3 MW",
    "> 3 MW to ≤ 5 MW",
    "> 5 MW to ≤ 10 MW",
    "> 10 MW"
]

# Create a new column categorizing each row by the capacity bin
df["Capacity Range"] = pd.cut(
    df["Total NPC MW DC"],
    bins=bins,
    labels=labels,
    right=True  # means the bin edge is inclusive on the right side
)
#print if the capacity range is greater than 10 MW
#st.dataframe(df[df['Capacity Range'] == "> 10 MW"])

# --------------------------------------------------
# 3. Group by Capacity Range
# --------------------------------------------------
# - "# of Systems" = count of rows (assuming each row = 1 system)
# - "Total MW" = sum of 'Total NPC MW DC'
grouped = df.groupby("Capacity Range", as_index=True).agg(
    Systems=("PA Certification #", "count"),
    Total_MW=("Total NPC MW DC", lambda x: int(round(x.sum())))
)

# Ensure all bins appear, even if they have zero systems
# (in case some bins have no data)
table_df = grouped.reindex(labels, fill_value=0).reset_index()

#rename the last column to "Total MW"
table_df.rename(columns={'Total_MW': 'Total MW'}, inplace=True)

# --------------------------------------------------
# 4. Add a "Total" Row
# --------------------------------------------------
systems_sum = table_df["Systems"].sum()
mw_sum = table_df["Total MW"].sum()

# Append the total row at the bottom
total_row = pd.DataFrame([["Total", systems_sum, mw_sum]], columns=table_df.columns)
table_df = pd.concat([table_df, total_row])

# Reset the index to ensure it's unique
table_df = table_df.reset_index(drop=True)
                                
# --------------------------------------------------
# Custom Styling Function to Add Row-Specific Borders
# --------------------------------------------------
def border_style(row):
    # Start with no style for all cells in this row.
    styles = ["" for _ in row.index]
    
    # Add a bold bottom border after the "≤ 15 kW" row.
    if row["Capacity Range"] == "≤ 15 kW":
        styles = ["border-bottom: 1.5px solid black" for _ in row.index]
    
    # Add a bold bottom border after the "> 1 MW to ≤ 3 MW" row.
    elif row["Capacity Range"] == "> 1 MW to ≤ 3 MW":
        styles = ["border-bottom: 1.5px solid black" for _ in row.index]
    
    # Add a bold top border on the "Total" row.
    elif row["Capacity Range"] == "Total":
        styles = ["border-top: 1.5px solid black" for _ in row.index]
    
    return styles

# Define custom style dictionaries
headers = {
    'selector': 'th',
    'props': [('background-color', '#3c598eff'), ('color', 'white')]
}
cell_hover = {
    'selector': 'tr:hover',
    'props': [('background-color', '#fcfcd7')]
}
cell = {
    'selector': 'td',
    'props': [('text-align', 'center')]
}
# style to make last row bold
last_row = {
    'selector': 'tr:last-child',
    'props': [('font-weight', 'bold')]
}
# style to make first column left aligned
first_col = {
    'selector': 'th:first-child, td:first-child',
    'props': [('text-align', 'left')]
}


# --------------------------------------------------
# Apply Overall Table Styles and the Custom Row Styles
# --------------------------------------------------
table_styled = (
    table_df.style
    # Set an overall border around the table and ensure cells have a border.
    .set_table_styles([
        {"selector": "table", "props": [("border", "2px solid black"), ("border-collapse", "collapse")]},
        {"selector": "th", "props": [("border-bottom", "2px solid black"), ("padding", "8px")]},
        headers,
        cell_hover,
        cell,
        last_row,
        first_col
    ])
    # Set a default padding and a cell border for all cells.
    .set_properties(**{"padding": "8px", "border" : "None"})
    # Apply the custom border styles for specific rows.
    .apply(border_style, axis=1)
    .hide()  # Hide the default index
)

# get the 'Certification Start Date' for the latest entry
date = df.iloc[1]['Certification Start Date'] 
st.write(date)
# --------------------------------------------------
# Display the Styled Table in Streamlit Without the Default Index
# --------------------------------------------------
st.subheader("Cumulative PV Installed in PA (DC)")
st.markdown(table_styled.to_html(), unsafe_allow_html=True)
st.caption("*As of "+ date + " (source: PA AEPS / PUC)")


st.download_button(
    label="Download Table as HTML",
    data=table_styled.to_html(),
    file_name="styled_table.html",
    mime="text/html"
)
# --------------------------------------------------
# 5. Display the Table in Streamlit
# --------------------------------------------------
#st.title("Cumulative PV Installed in PA (DC)")
#st.table(table_df.set_index("Capacity Range"))

#st.caption("* As of 2/12/2025 (source: PA AEPS / PUC)")
