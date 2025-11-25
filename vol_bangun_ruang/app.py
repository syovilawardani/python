import streamlit as st
import numpy as np

# Konfigurasi halaman
st.set_page_config(layout="wide")
st.title("🔬 Virtual Lab: Menghitung Volume Bangun Ruang")
st.markdown("Pilih bangun ruang, masukkan dimensinya, dan hitung volumenya secara interaktif.")
st.markdown("---")

# Definisikan nilai Pi
PI = np.pi

## --- Fungsi-fungsi Perhitungan Volume ---

def hitung_kubus(sisi):
    """Volume Kubus: V = s³"""
    return sisi ** 3, "V = s³"

def hitung_balok(panjang, lebar, tinggi):
    """Volume Balok: V = p × l × t"""
    return panjang * lebar * tinggi, "V = p × l × t"

def hitung_tabung(jari_jari, tinggi):
    """Volume Tabung: V = π × r² × t"""
    volume = PI * (jari_jari ** 2) * tinggi
    return volume, "V = π × r² × t"

def hitung_bola(jari_jari):
    """Volume Bola: V = (4/3) × π × r³"""
    volume = (4/3) * PI * (jari_jari ** 3)
    return volume, "V = (4/3) × π × r³"

def hitung_limas_segiempat(panjang_alas, lebar_alas, tinggi):
    """Volume Limas Segiempat: V = (1/3) × Luas Alas × t"""
    luas_alas = panjang_alas * lebar_alas
    volume = (1/3) * luas_alas * tinggi
    return volume, "V = (1/3) × p × l × t"

def hitung_kerucut(jari_jari, tinggi):
    """Volume Kerucut: V = (1/3) × π × r² × t"""
    volume = (1/3) * PI * (jari_jari ** 2) * tinggi
    return volume, "V = (1/3) × π × r² × t"

## --- Antarmuka Streamlit ---

# Sidebar untuk pemilihan bangun
st.sidebar.header("Pilih Bangun Ruang")
shape_options = [
    "Kubus", 
    "Balok", 
    "Tabung (Silinder)", 
    "Bola", 
    "Limas Segiempat", 
    "Kerucut"
]
selected_shape = st.sidebar.selectbox("Pilih:", shape_options)

# Konten Utama
st.header(f"🧮 Perhitungan Volume {selected_shape}")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("1. Input Dimensi (Satuan cm)")
    volume = 0
    formula_text = ""
    is_valid = True

    # --- Input Sesuai Bangun Ruang ---
    if selected_shape == "Kubus":
        s = st.number_input("Panjang Sisi (s):", min_value=0.1, value=5.0, step=0.5)
        if s > 0:
            volume, formula_text = hitung_kubus(s)
        else:
            is_valid = False
            st.warning("Sisi harus lebih besar dari 0.")

    elif selected_shape == "Balok":
        p = st.number_input("Panjang (p):", min_value=0.1, value=6.0, step=0.5)
        l = st.number_input("Lebar (l):", min_value=0.1, value=4.0, step=0.5)
        t = st.number_input("Tinggi (t):", min_value=0.1, value=3.0, step=0.5)
        if p > 0 and l > 0 and t > 0:
            volume, formula_text = hitung_balok(p, l, t)
        else:
            is_valid = False
            st.warning("Panjang, lebar, dan tinggi harus lebih besar dari 0.")

    elif selected_shape == "Tabung (Silinder)":
        r = st.number_input("Jari-jari Alas (r):", min_value=0.1, value=3.0, step=0.1)
        t = st.number_input("Tinggi (t):", min_value=0.1, value=7.0, step=0.1)
        if r > 0 and t > 0:
            volume, formula_text = hitung_tabung(r, t)
        else:
            is_valid = False
            st.warning("Jari-jari dan tinggi harus lebih besar dari 0.")

    elif selected_shape == "Bola":
        r = st.number_input("Jari-jari (r):", min_value=0.1, value=4.0, step=0.1)
        if r > 0:
            volume, formula_text = hitung_bola(r)
        else:
            is_valid = False
            st.warning("Jari-jari harus lebih besar dari 0.")
            
    elif selected_shape == "Limas Segiempat":
        p = st.number_input("Panjang Alas (p):", min_value=0.1, value=5.0, step=0.5, key="lp")
        l = st.number_input("Lebar Alas (l):", min_value=0.1, value=5.0, step=0.5, key="ll")
        t = st.number_input("Tinggi Limas (t):", min_value=0.1, value=6.0, step=0.5, key="lt")
        if p > 0 and l > 0 and t > 0:
            volume, formula_text = hitung_limas_segiempat(p, l, t)
        else:
            is_valid = False
            st.warning("Dimensi harus lebih besar dari 0.")

    elif selected_shape == "Kerucut":
        r = st.number_input("Jari-jari Alas (r):", min_value=0.1, value=3.0, step=0.1, key="kr")
        t = st.number_input("Tinggi (t):", min_value=0.1, value=6.0, step=0.1, key="kt")
        if r > 0 and t > 0:
            volume, formula_text = hitung_kerucut(r, t)
        else:
            is_valid = False
            st.warning("Jari-jari dan tinggi harus lebih besar dari 0.")
            
with col2:
    st.subheader("2. Hasil Perhitungan")
    
    # Menampilkan rumus
    st.code(f"Rumus Volume {selected_shape}: {formula_text}")
    
    if is_valid:
        # Tampilkan volume
        st.metric(
            label=f"Volume {selected_shape}",
            value=f"{volume:,.2f} cm³"
        )
        
        st.info("Nilai $\pi$ yang digunakan adalah $\pi \\approx 3.14159$")

    st.markdown("---")
    st.subheader("3. Pemahaman Konsep")
    
    # Penjelasan singkat
    if selected_shape == "Kubus":
        st.markdown(f"Volume **Kubus** adalah ukuran ruang yang dibatasi oleh enam bidang persegi yang sama besar. Karena semua sisinya sama (**s**), volume dihitung dengan mengalikan sisi sebanyak tiga kali.")
    elif selected_shape == "Balok":
        st.markdown(f"Volume **Balok** dihitung dengan mengalikan luas alas (panjang $\\times$ lebar) dengan tingginya.")
    elif selected_shape == "Tabung (Silinder)":
        st.markdown(f"Volume **Tabung** adalah luas alas (lingkaran, $\\pi r^2$) dikalikan dengan tingginya.")
    elif selected_shape == "Bola":
        st.markdown(f"Volume **Bola** bergantung pada jari-jari ($r$). Rumus volumenya adalah $\\frac{4}{3} \\pi r^3$.")
    elif selected_shape == "Limas Segiempat":
        st.markdown(f"Volume **Limas** adalah sepertiga dari volume prisma yang memiliki alas dan tinggi yang sama. Limas segiempat memiliki alas berbentuk persegi atau persegi panjang.")
    elif selected_shape == "Kerucut":
        st.markdown(f"Volume **Kerucut** adalah sepertiga dari volume tabung yang memiliki alas dan tinggi yang sama.")
