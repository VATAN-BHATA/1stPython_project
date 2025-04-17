import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image, ImageDraw, ImageFont

# Set up the Streamlit page
st.set_page_config(page_title="🌦️ Weather Insights", layout="wide")
st.title("🌍 Weather Insights Dashboard")

# Load the dataset
@st.cache_data
def load_data():
    return pd.read_csv(r"D:\Advanced Python\Advanced Python\Dataset\csv\weather_dataset.csv")

df = load_data()

# Sidebar Navigation
st.sidebar.title("🔎 Explore")
menu = st.sidebar.radio("Go to", ["Dataset Overview", "Visual Insights", "City Weather Summary"])

# 1. Dataset Overview
if menu == "Dataset Overview":
    st.subheader("📄 Dataset Preview")
    st.dataframe(df)

    st.subheader("📊 Descriptive Statistics")
    st.write(df.describe())

# 2. Visual Insights
elif menu == "Visual Insights":
    st.subheader("📈 Factor Comparison Between Cities")

    options = ["Temperature (°C)", "Humidity (%)", "Wind Speed (km/h)", "Air Quality Index (AQI)", "Rainfall (mm)"]
    selected = st.multiselect("Select one or more factors", options, default=["Temperature (°C)"])

    for factor in selected:
        fig, ax = plt.subplots(figsize=(10, 4))
        sns.barplot(data=df, x="City", y=factor, palette="coolwarm", ax=ax)
        ax.set_title(f"{factor} by City")
        st.pyplot(fig)

    st.subheader("🔗 Correlation Heatmap")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(df.drop(columns=["City"]).corr(), annot=True, cmap="YlGnBu", linewidths=0.5, ax=ax)
    st.pyplot(fig)

# 3. Weather Summary with PIL
elif menu == "City Weather Summary":
    st.subheader("🖼️ Generate Summary Image")

    selected_city = st.selectbox("Select a city", df["City"].unique())
    city_data = df[df["City"] == selected_city].squeeze()

    # Create image using PIL
    img = Image.new("RGB", (500, 300), color="#003366")
    draw = ImageDraw.Draw(img)

    try:
        font_title = ImageFont.truetype("arial.ttf", 24)
        font_text = ImageFont.truetype("arial.ttf", 18)
    except:
        font_title = font_text = None  # fallback if fonts not found

    draw.text((20, 20), f"Weather Summary - {selected_city}", fill="white", font=font_title)
    draw.text((20, 70), f"Temperature: {city_data['Temperature (°C)']} °C", fill="lightblue", font=font_text)
    draw.text((20, 100), f"Humidity: {city_data['Humidity (%)']}%", fill="lightblue", font=font_text)
    draw.text((20, 130), f"Wind Speed: {city_data['Wind Speed (km/h)']} km/h", fill="lightblue", font=font_text)
    draw.text((20, 160), f"AQI: {city_data['Air Quality Index (AQI)']}", fill="lightblue", font=font_text)
    draw.text((20, 190), f"Rainfall: {city_data['Rainfall (mm)']} mm", fill="lightblue", font=font_text)

    st.image(img, caption=f"{selected_city} Weather Summary (Generated with PIL)", use_container_width=False)
