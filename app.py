import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------
# Page Configuration
# -----------------------
st.set_page_config(
    page_title="NFHS India Dashboard",
    layout="wide"
)

st.title("📊 National Family Health Survey (NFHS) Dashboard")
st.caption("Source: Ministry of Health & Family Welfare, Government of India")

# -----------------------
# Load Data
# -----------------------
@st.cache_data
def load_data():
    df = pd.read_csv("All India National Family Health Survey.csv")
    return df

df = load_data()

# -----------------------
# Sidebar Filters
# -----------------------
st.sidebar.header("🔎 Filters")

state = st.sidebar.selectbox(
    "Select State / UT",
    sorted(df["India/States/UTs"].unique())
)

survey = st.sidebar.selectbox(
    "Select Survey",
    sorted(df["Survey"].unique())
)

area = st.sidebar.selectbox(
    "Select Area",
    sorted(df["Area"].unique())
)

filtered_df = df[
    (df["India/States/UTs"] == state) &
    (df["Survey"] == survey) &
    (df["Area"] == area)
]

# -----------------------
# Key Indicators (KPIs)
# -----------------------
st.subheader("📌 Key Indicators")

col1, col2, col3, col4 = st.columns(4)

def get_value(column):
    try:
        return round(filtered_df[column].values[0], 1)
    except:
        return "NA"

with col1:
    st.metric(
        "Female Literacy (%)",
        get_value("Population and Household Profile - Population (female) age 6 years and above who ever attended school (%)")
    )

with col2:
    st.metric(
        "Sex Ratio",
        get_value("Population and Household Profile - Sex ratio of the total population (females per 1000 males)")
    )

with col3:
    st.metric(
        "Electricity (%)",
        get_value("Population and Household Profile - Households with electricity (%)")
    )

with col4:
    st.metric(
        "Improved Water (%)",
        get_value("Population and Household Profile - Households with an improved drinking-water source (%)")
    )

# -----------------------
# Comparative Chart
# -----------------------
st.subheader("📈 State-wise Comparison")

indicator = st.selectbox(
    "Select Indicator",
    [
        "Population and Household Profile - Population (female) age 6 years and above who ever attended school (%)",
        "Population and Household Profile - Households with electricity (%)",
        "Population and Household Profile - Sex ratio of the total population (females per 1000 males)",
        "Population and Household Profile - Children under age 5 years whose birth was registered (%)"
    ]
)

compare_df = df[
    (df["Survey"] == survey) &
    (df["Area"] == area)
][["India/States/UTs", indicator]].dropna()

fig = px.bar(
    compare_df,
    x="India/States/UTs",
    y=indicator,
    title=f"{indicator} ({survey} – {area})",
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------
# Data Table
# -----------------------
st.subheader("📋 Filtered Data (Preview)")

st.dataframe(filtered_df, use_container_width=True)

# -----------------------
# Footer
# -----------------------
st.markdown("---")
st.caption("Designed for policy analysis, UPSC preparation & public health review")
