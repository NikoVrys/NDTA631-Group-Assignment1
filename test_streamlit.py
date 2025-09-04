# test_streamlit.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Basic Streamlit commands to test everything
st.title("🚀 Streamlit Installation Test")
st.success("If you can see this message, Streamlit is working!")

# Test pandas
data = pd.DataFrame({
    'Year': [2017, 2018, 2019, 2020, 2021, 2022, 2023],
    'CO2_Emissions': [439.996, 434.581, 464.114, 434.067, 425.918, 405.312, 401.893],
    'Diet_Unaffordability': [60.8, 60.2, 60.2, 61.8, 61.1, 61.0, 61.7]
})

st.write("### Sample Data (Testing pandas):")
st.dataframe(data)

# Test numpy
st.write("### Basic Statistics (Testing numpy):")
st.write(f"Mean CO2: {np.mean(data['CO2_Emissions']):.2f}")
st.write(f"Mean Diet Unaffordability: {np.mean(data['Diet_Unaffordability']):.2f}%")

# Test matplotlib
st.write("### Simple Plot (Testing matplotlib):")
fig, ax = plt.subplots()
ax.plot(data['Year'], data['CO2_Emissions'], marker='o')
ax.set_xlabel('Year')
ax.set_ylabel('CO2 Emissions')
ax.set_title('Test Plot')
st.pyplot(fig)

st.info("🎉 All tests passed! Your Streamlit environment is ready.")