import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="EDA Toolkit CKD", layout="wide")
st.title("📊 EDA Toolkit - Eksplorasi Dataset CKD")
st.markdown("Dataset **mentah (sebelum preprocessing)**. Gunakan panel kiri untuk memilih jenis visualisasi.")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("CKD_NHANES_2021_2023")
    return df

try:
    df = load_data()
    st.success(f"✅ Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
except FileNotFoundError:
    st.error("❌ File 'ckd_dataset.csv' tidak ditemukan. Pastikan file ada di root repositori.")
    st.stop()

# Sidebar
st.sidebar.header("⚙️ Pengaturan Visualisasi")
plot_type = st.sidebar.selectbox(
    "Pilih jenis plot",
    ["📊 Bar Count", "📦 Box Plot", "📈 Histogram", "🥧 Pie Chart",
     "🔵 Scatter Plot", "🔥 Correlation Heatmap", "📊 Pair Plot (Terbatas)", "📋 Summary Statistics"]
)

# Deteksi kolom numerik dan kategorikal
num_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
all_cols = df.columns.tolist()

# ------------------------------
# Bar Count (Perbaikan error)
# ------------------------------
if plot_type == "📊 Bar Count":
    if len(cat_cols) == 0:
        st.warning("Tidak ada kolom kategorikal untuk bar count.")
    else:
        col = st.sidebar.selectbox("Pilih kolom kategorikal", cat_cols)
        if col:
            freq = df[col].value_counts().reset_index()
            freq.columns = ['Kategori', 'Frekuensi']
            fig = px.bar(freq, x='Kategori', y='Frekuensi', title=f"Distribusi {col}", text='Frekuensi')
            fig.update_traces(textposition='outside')
            st.plotly_chart(fig, use_container_width=True)

# ------------------------------
# Box Plot
# ------------------------------
elif plot_type == "📦 Box Plot":
    if len(num_cols) == 0:
        st.warning("Tidak ada kolom numerik.")
    else:
        col = st.sidebar.selectbox("Pilih kolom numerik", num_cols)
        if col:
            fig = px.box(df, y=col, title=f"Box Plot {col}", points="all")
            st.plotly_chart(fig, use_container_width=True)

# ------------------------------
# Histogram
# ------------------------------
elif plot_type == "📈 Histogram":
    if len(num_cols) == 0:
        st.warning("Tidak ada kolom numerik.")
    else:
        col = st.sidebar.selectbox("Pilih kolom numerik", num_cols)
        bins = st.sidebar.slider("Jumlah bins", 5, 100, 30)
        if col:
            fig = px.histogram(df, x=col, nbins=bins, title=f"Histogram {col}", marginal="box")
            st.plotly_chart(fig, use_container_width=True)

# ------------------------------
# Pie Chart
# ------------------------------
elif plot_type == "🥧 Pie Chart":
    if len(cat_cols) == 0:
        st.warning("Tidak ada kolom kategorikal.")
    else:
        col = st.sidebar.selectbox("Pilih kolom kategorikal", cat_cols)
        if col:
            top_n = st.sidebar.slider("Jumlah kategori teratas", 3, 15, 10)
            top_categories = df[col].value_counts().nlargest(top_n).index
            df_filtered = df[df[col].isin(top_categories)]
            fig = px.pie(df_filtered, names=col, title=f"Proporsi {col} (Top {top_n})")
            st.plotly_chart(fig, use_container_width=True)

# ------------------------------
# Scatter Plot
# ------------------------------
elif plot_type == "🔵 Scatter Plot":
    if len(num_cols) < 2:
        st.warning("Butuh minimal 2 kolom numerik untuk scatter plot.")
    else:
        x_col = st.sidebar.selectbox("Sumbu X (numerik)", num_cols)
        y_col = st.sidebar.selectbox("Sumbu Y (numerik)", num_cols)
        color_col = st.sidebar.selectbox("Kategori pewarnaan (opsional)", [None] + cat_cols)
        size_col = st.sidebar.selectbox("Ukuran titik (opsional)", [None] + num_cols)
        if x_col and y_col:
            fig = px.scatter(df, x=x_col, y=y_col, color=color_col, size=size_col,
                             title=f"Scatter Plot {x_col} vs {y_col}",
                             hover_data=all_cols, opacity=0.7)
            st.plotly_chart(fig, use_container_width=True)

# ------------------------------
# Correlation Heatmap
# ------------------------------
elif plot_type == "🔥 Correlation Heatmap":
    if len(num_cols) < 2:
        st.warning("Butuh minimal 2 kolom numerik untuk heatmap korelasi.")
    else:
        corr = df[num_cols].corr()
        fig = px.imshow(corr, text_auto=True, aspect="auto", color_continuous_scale="RdBu_r",
                        title="Heatmap Korelasi Antar Fitur Numerik")
        st.plotly_chart(fig, use_container_width=True)

# ------------------------------
# Pair Plot (Terbatas)
# ------------------------------
elif plot_type == "📊 Pair Plot (Terbatas)":
    if len(num_cols) < 2:
        st.warning("Butuh minimal 2 kolom numerik.")
    else:
        max_cols = st.sidebar.slider("Maksimal kolom numerik untuk pair plot (performa)", 2, min(len(num_cols), 6), 4)
        selected_num = num_cols[:max_cols]
        if len(selected_num) >= 2:
            fig = px.scatter_matrix(df, dimensions=selected_num, title="Pair Plot (Scatter Matrix)")
            fig.update_traces(diagonal_visible=False)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Pilih setidaknya 2 kolom.")

# ------------------------------
# Summary Statistics
# ------------------------------
elif plot_type == "📋 Summary Statistics":
    st.subheader("Deskripsi Statistik - Numerik & Kategorikal")
    st.dataframe(df.describe(include='all').T)
    st.subheader("Jumlah Missing Values per Kolom")
    missing = df.isnull().sum().sort_values(ascending=False)
    missing = missing[missing > 0]
    if len(missing) > 0:
        st.bar_chart(missing)
    else:
        st.write("Tidak ada missing values.")

# Tampilkan data mentah opsional
st.sidebar.markdown("---")
if st.sidebar.checkbox("Tampilkan data mentah (100 baris pertama)"):
    st.subheader("📋 Data Mentah (Preview)")
    st.dataframe(df.head(100))
