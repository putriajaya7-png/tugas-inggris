import streamlit as st
import google.generativeai as genai
import easyocr
from PIL import Image
import numpy as np

# --- 1. KONFIGURASI API ---
try:
    # Memanggil kunci dari menu Secrets
    KUNCI_API = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=KUNCI_API)
    model_ai = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Kunci API tidak terbaca! Periksa menu Secrets. Error: {e}")
    st.stop()

# Fungsi untuk membaca teks dari gambar
@st.cache_resource
def load_reader():
    return easyocr.Reader(['en'])
reader = load_reader()

# --- 2. TAMPILAN APLIKASI ---
st.set_page_config(page_title="English Expert Solver", layout="centered")
st.title("🎓 English Expert Solver")
st.write("Aplikasi sudah diperbaiki. Silakan masukkan soal!")

# Sidebar untuk pilihan jenjang
level = st.sidebar.selectbox("Pilih Jenjang:", ["TK", "SD", "SMP", "SMA", "S1", "S2"])
metode = st.radio("Pilih Cara Bertanya:", ["Ketik Teks", "Upload Foto Soal"])

soal_siap = ""

if metode == "Ketik Teks":
    soal_siap = st.text_area("Masukkan soal kamu di sini...")
else:
    file_gambar = st.file_uploader("Pilih foto soal (JPG/PNG)", type=['jpg', 'jpeg', 'png'])
    if file_gambar:
        img = Image.open(file_gambar)
        st.image(img, caption="Foto Soal", width=350)
        with st.spinner("Sedang membaca tulisan di foto..."):
            hasil_ocr = reader.readtext(np.array(img), detail=0)
            soal_siap = " ".join(hasil_ocr)
            st.info(f"Teks yang terbaca: {soal_siap}")

# --- 3. PROSES JAWABAN AI ---
if st.button("Dapatkan Jawaban ✨"):
    if soal_siap:
        with st.spinner("AI sedang merumuskan jawaban..."):
            try:
                prompt = f"Anda adalah guru Bahasa Inggris pakar. Jawablah soal tingkat {level} ini dengan penjelasan: {soal_siap}"
                respon = model_ai.generate_content(prompt)
                st.markdown("---")
                st.success(f"### Jawaban ({level}):")
                st.write(respon.text)
            except Exception as e:
                st.error(f"Google bilang: {e}")
    else:
        st.warning("Silakan ketik soal atau unggah foto dulu ya!")
