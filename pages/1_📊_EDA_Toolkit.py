import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="EDA Toolkit CKD", layout="wide")
st.title("📊 EDA Toolkit - Eksplorasi Dataset CKD")
st.markdown("Dataset **mentah (sebelum preprocessing)**. Gunakan panel kiri untuk mengubah grafik.")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("CKD_NHANES_2021_2023.csv")
    return df

try:
    df = load_data()
    st.success(f"✅ Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
except FileNotFoundError:
    st.error("❌ File 'ckd_dataset.csv' tidak ditemukan. Pastikan file ada di root repositori.")
    st.stop()

# Sidebar
st.sidebar.header("⚙️ Pengaturan")
plot_type = st.sidebar.selectbox("Pilih jenis plot", ["Bar Count", "Box Plot", "Histogram", "Pie Chart"])

# Deteksi kolom numerik dan kategorikal
num_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()

# Pilihan kolom
if plot_type in ["Bar Count", "Pie Chart"]:
    col = st.sidebar.selectbox("Pilih kolom kategorikal", cat_cols) if cat_cols else None
elif plot_type == "Box Plot":
    col = st.sidebar.selectbox("Pilih kolom numerik", num_cols) if num_cols else None
elif plot_type == "Histogram":
    col = st.sidebar.selectbox("Pilih kolom numerik", num_cols) if num_cols else None
    bins = st.sidebar.slider("Jumlah bins", 5, 50, 20) if col else None

# Generate plot
if plot_type == "Bar Count" and col:
    fig = px.bar(df[col].value_counts().reset_index(), x='index', y=col, title=f"Distribusi {col}")
    st.plotly_chart(fig, use_container_width=True)
elif plot_type == "Pie Chart" and col:
    fig = px.pie(df, names=col, title=f"Proporsi {col}")
    st.plotly_chart(fig, use_container_width=True)
elif plot_type == "Box Plot" and col:
    fig = px.box(df, y=col, title=f"Box Plot {col}")
    st.plotly_chart(fig, use_container_width=True)
elif plot_type == "Histogram" and col:
    fig = px.histogram(df, x=col, nbins=bins, title=f"Histogram {col}")
    st.plotly_chart(fig, use_container_width=True)

# Tampilkan data mentah
st.subheader("📋 Data mentah")
st.dataframe(df.head(100))
