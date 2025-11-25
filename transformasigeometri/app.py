import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# --- Fungsi-fungsi Transformasi Geometri ---

def translasi(points, tx, ty):
    """Menerapkan Translasi pada sekumpulan titik."""
    # Vektor translasi: [tx, ty]
    return points + np.array([tx, ty])

def rotasi(points, angle_deg, cx=0, cy=0):
    """Menerapkan Rotasi pada sekumpulan titik (berpusat di (cx, cy))."""
    angle_rad = np.radians(angle_deg)
    # Matriks Rotasi: [[cos(a), -sin(a)], [sin(a), cos(a)]]
    cos_a = np.cos(angle_rad)
    sin_a = np.sin(angle_rad)
    
    # Translasi ke pusat (0,0), Rotasi, Translasi kembali
    points_centered = points - np.array([cx, cy])
    points_rotated_centered = np.dot(points_centered, np.array([[cos_a, sin_a], [-sin_a, cos_a]])) # Perhatikan urutan axis untuk Matplotlib
    points_rotated = points_rotated_centered + np.array([cx, cy])
    return points_rotated

def refleksi(points, axis_type):
    """Menerapkan Refleksi pada sekumpulan titik."""
    if axis_type == "Sumbu X (y=0)":
        # Matriks Refleksi terhadap Sumbu X: [[1, 0], [0, -1]]
        return points * np.array([1, -1])
    elif axis_type == "Sumbu Y (x=0)":
        # Matriks Refleksi terhadap Sumbu Y: [[-1, 0], [0, 1]]
        return points * np.array([-1, 1])
    elif axis_type == "Garis y = x":
        # Matriks Refleksi terhadap y=x: [[0, 1], [1, 0]]
        return np.dot(points, np.array([[0, 1], [1, 0]]))
    elif axis_type == "Garis y = -x":
        # Matriks Refleksi terhadap y=-x: [[0, -1], [-1, 0]]
        return np.dot(points, np.array([[0, -1], [-1, 0]]))
    return points

def dilatasi(points, k, cx=0, cy=0):
    """Menerapkan Dilatasi pada sekumpulan titik (berpusat di (cx, cy))."""
    # Faktor skala: k
    # Translasi ke pusat (0,0), Dilatasi, Translasi kembali
    points_centered = points - np.array([cx, cy])
    points_dilated_centered = points_centered * k
    points_dilated = points_dilated_centered + np.array([cx, cy])
    return points_dilated

# --- Antarmuka Streamlit ---

st.set_page_config(layout="wide")
st.title("🔬 Virtual Lab Transformasi Geometri")
st.markdown("Eksplorasi interaktif tentang Rotasi, Dilatasi, Refleksi, dan Translasi.")
st.markdown("---")

# Input Sisi Kiri (Titik Awal)
st.sidebar.header("1. Input Titik Awal")
# Contoh input untuk persegi panjang A(1,1), B(4,1), C(4,3), D(1,3)
initial_points_str = st.sidebar.text_area(
    "Masukkan Koordinat Titik (format: x1,y1; x2,y2; ...):",
    "1,1; 4,1; 4,3; 1,3",
    height=100
)

try:
    # Parsing input string menjadi array NumPy
    points_list = []
    for pair in initial_points_str.strip().split(';'):
        x, y = map(float, pair.split(','))
        points_list.append([x, y])
    initial_points = np.array(points_list)
    
    if initial_points.shape[0] < 2:
         st.error("Input minimal 2 titik.")
         st.stop()
         
except Exception:
    st.error("Format input salah! Gunakan format: x1,y1; x2,y2; ...")
    st.stop()

st.sidebar.header("2. Pilih & Atur Transformasi")
transformation_type = st.sidebar.selectbox(
    "Pilih Jenis Transformasi:",
    ["Translasi (Pergeseran)", "Rotasi (Perputaran)", "Refleksi (Pencerminan)", "Dilatasi (Perkalian)"]
)

# Output Sisi Kanan (Plot & Kontrol Transformasi)
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader(f"Kontrol: {transformation_type}")
    final_points = initial_points.copy() # Mulai dengan titik awal
    transform_params = {}

    if transformation_type == "Translasi (Pergeseran)":
        tx = st.slider("Vektor Translasi (tx):", -10, 10, 3)
        ty = st.slider("Vektor Translasi (ty):", -10, 10, 2)
        final_points = translasi(initial_points, tx, ty)
        st.info(f"Transformasi: Titik digeser sebesar **({tx}, {ty})**.")

    elif transformation_type == "Rotasi (Perputaran)":
        angle = st.slider("Sudut Rotasi (derajat):", -360, 360, 90)
        center_x = st.number_input("Pusat Rotasi (Cx):", value=0)
        center_y = st.number_input("Pusat Rotasi (Cy):", value=0)
        final_points = rotasi(initial_points, angle, center_x, center_y)
        st.info(f"Transformasi: Titik diputar sebesar **{angle}°** berpusat di **({center_x}, {center_y})**.")

    elif transformation_type == "Refleksi (Pencerminan)":
        axis = st.selectbox(
            "Garis Pencerminan:",
            ["Sumbu X (y=0)", "Sumbu Y (x=0)", "Garis y = x", "Garis y = -x"]
        )
        final_points = refleksi(initial_points, axis)
        st.info(f"Transformasi: Titik dicerminkan terhadap **{axis}**.")

    elif transformation_type == "Dilatasi (Perkalian)":
        k = st.slider("Faktor Skala (k):", 0.1, 5.0, 2.0, 0.1)
        center_x = st.number_input("Pusat Dilatasi (Cx):", value=0, key="dcx")
        center_y = st.number_input("Pusat Dilatasi (Cy):", value=0, key="dcy")
        final_points = dilatasi(initial_points, k, center_x, center_y)
        st.info(f"Transformasi: Titik diperbesar/diperkecil dengan faktor **{k}** berpusat di **({center_x}, {center_y})**.")

with col2:
    st.subheader("Visualisasi Hasil")

    # Plot menggunakan Matplotlib
    fig, ax = plt.subplots(figsize=(8, 8))

    # Tentukan batas plot
    all_points = np.vstack([initial_points, final_points])
    min_x, max_x = np.min(all_points[:, 0]) - 2, np.max(all_points[:, 0]) + 2
    min_y, max_y = np.min(all_points[:, 1]) - 2, np.max(all_points[:, 1]) + 2
    
    # Pastikan plot simetris dan mencakup pusat (0,0)
    limit = max(abs(min_x), abs(max_x), abs(min_y), abs(max_y), 5) * 1.1
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    ax.axhline(0, color='gray', linewidth=0.5)
    ax.axvline(0, color='gray', linewidth=0.5)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlabel("Sumbu X")
    ax.set_ylabel("Sumbu Y")

    # Plot Bangun Awal (Biru)
    # Gunakan np.append untuk menutup poligon
    initial_poly = np.append(initial_points, [initial_points[0]], axis=0)
    ax.plot(initial_poly[:, 0], initial_poly[:, 1], 'b-o', label="Bangun Awal")
    
    # Plot Bangun Hasil Transformasi (Merah)
    final_poly = np.append(final_points, [final_points[0]], axis=0)
    ax.plot(final_poly[:, 0], final_poly[:, 1], 'r--o', label="Bangun Hasil")
    
    # Tambahkan label koordinat
    for i, (x, y) in enumerate(initial_points):
        ax.text(x, y, f'A{i+1}({x:.1f},{y:.1f})', color='blue', fontsize=9, ha='right')
    for i, (x, y) in enumerate(final_points):
        ax.text(x, y, f"A'{i+1}({x:.1f},{y:.1f})", color='red', fontsize=9, ha='left')
        
    ax.legend()
    st.pyplot(fig)

    # Tampilkan Tabel Koordinat
    st.subheader("Tabel Koordinat")
    coord_data = {}
    for i in range(initial_points.shape[0]):
        coord_data[f"Titik Awal A{i+1}"] = f"({initial_points[i, 0]:.2f}, {initial_points[i, 1]:.2f})"
        coord_data[f"Titik Hasil A'{i+1}"] = f"({final_points[i, 0]:.2f}, {final_points[i, 1]:.2f})"
    
    st.dataframe(coord_data, use_container_width=True)
