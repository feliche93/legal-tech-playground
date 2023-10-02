import os
import streamlit as st
from pathlib import Path
from bar_chart_races import get_df
import plotly.express as px


def get_video_path(column: str):
    # Get the absolute path of the current script file
    script_location = Path(os.path.abspath(__file__)).resolve()

    # Get the parent directory of the script file
    parent_directory = script_location.parent

    # Construct the path to the video file
    video_path = parent_directory / f"{column}_bar_chart_race.mp4"

    return video_path


# Get the paths to the videos
video_path_revenue = get_video_path("Revenue")
video_path_headcount = get_video_path("Headcount")

# Read the videos
video_revenue = open(video_path_revenue, "rb").read()
video_headcount = open(video_path_headcount, "rb").read()

st.write("## Law Firm Revenue and Headcount Over Time")
# Display the videos
st.video(video_revenue)
st.video(video_headcount)


# Plotly Charts
df = get_df("SELECT * FROM law_firm_data WHERE Revenue != 0")


st.write("## Law Firm Revenue and Headcount Over Time")

# Get unique firms
firms = df["firm"].unique()

# Get top 5 firms based on Revenue
top_5_firms = df.groupby("firm")["Revenue"].sum().nlargest(5).index.tolist()

# Create a multiselect widget for firms
selected_firms = st.multiselect("Select firms", options=firms, default=top_5_firms)

# Filter the dataframe based on the selected firms
filtered_df = df[df["firm"].isin(selected_firms)]

# Create a line chart for Revenue
fig_revenue = px.line(filtered_df, x="Year", y="Revenue", color="firm")
fig_revenue.update_layout(title="Revenue Over Time")

# Display the Revenue chart in Streamlit
st.plotly_chart(fig_revenue)

# Create a line chart for Headcount
fig_headcount = px.line(filtered_df, x="Year", y="Headcount", color="firm")
fig_headcount.update_layout(title="Headcount Over Time")

# Display the Headcount chart in Streamlit
st.plotly_chart(fig_headcount)


# Add a header
st.write("## Total Revenue and Headcount Over Time")

# Calculate total Revenue and Headcount over time
total_revenue = df.groupby("Year")["Revenue"].sum().reset_index()
total_headcount = df.groupby("Year")["Headcount"].sum().reset_index()

# Adjust Revenue to be in billions
total_revenue["Revenue"] = total_revenue["Revenue"] / 1e9

# Create a bar chart for total Revenue
fig_total_revenue = px.bar(total_revenue, x="Year", y="Revenue")
fig_total_revenue.update_layout(title="Total Revenue Over Time (in billions)", yaxis=dict(tickformat=".2f"))
st.plotly_chart(fig_total_revenue)

# Create a bar chart for total Headcount
fig_total_headcount = px.bar(total_headcount, x="Year", y="Headcount")
fig_total_headcount.update_layout(title="Total Headcount Over Time", yaxis=dict(tickformat=","))
st.plotly_chart(fig_total_headcount)


# Add a header
# Add a header
# Add a header
# Add a header
st.write("## Revenue Rank Over Time")

# Get unique firms
firms = df["firm"].unique()

# Calculate Revenue Rank for all firms
df["Revenue Rank"] = df.groupby("Year")["Revenue"].rank(ascending=False)

# Create a multiselect widget for firms
selected_firms = st.multiselect("Select firms", options=firms)

# Filter the dataframe based on the selected firms
filtered_df = df[df["firm"].isin(selected_firms)].copy()  # Use copy to avoid SettingWithCopyWarning

# Create a bubble chart for Revenue Rank
fig_revenue_rank = px.scatter(filtered_df, x="Year", y="Revenue Rank", size="Revenue", color="firm")
fig_revenue_rank.update_layout(title="Revenue Rank Over Time")
fig_revenue_rank.update_yaxes(autorange="reversed")  # Invert y-axis

# Display the chart in Streamlit
st.plotly_chart(fig_revenue_rank)
