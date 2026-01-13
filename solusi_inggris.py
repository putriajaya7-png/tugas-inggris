import streamlit as st
import google.generativeai as genai
import easyocr
from PIL import Image
import numpy as np

# --- 1. SETUP API ---
try:
    kunci = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=kunci)
    # Kita pakai gemini-pro agar lebih stabil dan tidak 404
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error(f"Gagal baca Secrets: {e}")
    st.stop()

# --- 2. SETUP OCR ---
@st.cache_resource
def load_reader():
    return easyocr.Reader(['en'])
reader = load_reader()

# --- 3. TAMPILAN ---
st.title("🎓 English Expert Solver")
level = st.sidebar.selectbox("Pilih Jenjang:", ["TK", "SD", "SMP", "SMA", "S1", "S2"])
cara = st.radio("Metode:", ["Ketik Teks", "Upload Foto Soal"])

soal_teks = ""
if cara == "Ketik Teks":
    soal_teks = st.text_area("Masukkan soal kamu di sini...")
else:
    file = st.file_uploader("Pilih foto soal", type=['jpg', 'png', 'jpeg'])
    if file:
        img = Image.open(file)
        st.image(img, width=300)
        with st.spinner("Membaca foto..."):
            hasil = reader.readtext(np.array(img), detail=0)
            soal_teks = " ".join(hasil)

# --- 4. TOMBOL JAWAB ---
if st.button("Dapatkan Jawaban ✨"):
    if soal_teks:
        with st.spinner("Sedang berpikir..."):
            try:
                respon = model.generate_content(f"Jawab soal {level} ini: {soal_teks}")
                st.success(f"### Jawaban ({level}):")
                st.write(respon.text)
            except Exception as e:
                st.error(f"Pesan Google: {e}")
    else:
        st.warning("Isi soal dulu ya!")
