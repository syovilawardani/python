import streamlit as st

# Fungsi untuk mencari luas persegi
def luas_persegi(sisi):
    """Menghitung luas persegi."""
    # Pastikan sisi tidak negatif untuk perhitungan luas
    if sisi < 0:
        return 0  
    luas = sisi * sisi
    return luas

st.title("🧮 Kalkulator Luas Persegi")

# --- Input Pengguna ---
# Gunakan number_input untuk sisi, dengan nilai minimum 0
sisi = st.number_input(
    "Masukkan panjang sisi persegi:", 
    min_value=0.0, 
    value=1.0, 
    step=0.1, 
    format="%.2f"
)

# --- Perhitungan dan Output ---
# Hitung luas
luas_hasil = luas_persegi(sisi)

# Tampilkan hasil
st.subheader("Hasil Perhitungan")
st.write(f"**Panjang sisi (s):** {sisi} satuan")

# Gunakan st.metric untuk tampilan hasil yang jelas
st.metric(
    label="Luas Persegi (L)", 
    value=f"{luas_hasil:.2f} satuan persegi"
)

# Catatan tambahan
st.markdown("---")
st.info("💡 Rumus yang digunakan: $L = s \times s$")