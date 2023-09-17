import pandas as pd
import streamlit as st

st.write("# 📊 Simple Interest vs Compound Interest Calculator")

st.sidebar.write("## Parameters")

principal = st.sidebar.number_input("Amount Claimed", value=1000, step=100)
rate = st.sidebar.number_input("Interest Rate in Percent", value=10, step=1)
years = st.sidebar.number_input("Number of Years", value=10, step=1)

# Convert rate from percentage to a proportion
rate = rate / 100

# Create a DataFrame for the years
years_array = pd.DataFrame(index=range(1, years + 1))

# Calculate the values for each year
years_array['Simple Interest'] = principal + years_array.index * principal * rate
years_array['Compound Interest'] = principal * (1 + rate) ** years_array.index

# Calculate the difference between simple and compound interest
years_array['Difference'] = years_array['Compound Interest'] - years_array['Simple Interest']

# Round the entire DataFrame to two decimal places
years_array = years_array.round(2)

# Plot the values
st.line_chart(years_array[['Simple Interest', 'Compound Interest']])

# Display the DataFrame as a table
st.table(years_array)
