import streamlit as st
import google.generativeai as genai
import easyocr
from PIL import Image
import numpy as np

# --- 1. SETUP API YANG ANTI-ERROR ---
try:
    kunci = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=kunci)
    
    # Mencari model yang tersedia secara otomatis agar tidak 404
    models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    nama_model = models[0] if models else 'gemini-1.5-flash'
    model_ai = genai.GenerativeModel(nama_model)
except Exception as e:
    st.error(f"Masalah Kunci API: {e}")
    st.stop()

# --- 2. SETUP PEMBACA FOTO (OCR) ---
@st.cache_resource
def ambil_pembaca():
    return easyocr.Reader(['en'])
pembaca = ambil_pembaca()

# --- 3. TAMPILAN ---
st.title("🎓 English Expert Solver")
level = st.sidebar.selectbox("Pilih Jenjang:", ["SD", "SMP", "SMA", "S1"])
cara = st.radio("Pilih Metode:", ["Ketik Teks", "Upload Foto Soal"])

soal_final = ""

if cara == "Ketik Teks":
    soal_final = st.text_area("Masukkan soal:")
else:
    file = st.file_uploader("Upload Foto (Pastikan Jelas)", type=['jpg', 'png', 'jpeg'])
    if file:
        img = Image.open(file)
        st.image(img, width=300)
        with st.spinner("Sabar ya, AI lagi baca tulisan di fotonya..."):
            hasil = pembaca.readtext(np.array(img), detail=0)
            soal_final = " ".join(hasil)
            if soal_final:
                st.info(f"Teks terbaca: {soal_final}")

# --- 4. TOMBOL JAWAB ---
if st.button("Dapatkan Jawaban ✨"):
    if soal_final:
        with st.spinner(f"Menghubungi AI ({nama_model})..."):
            try:
                prompt = f"Tolong jawab soal Bahasa Inggris level {level} ini: {soal_final}"
                respon = model_ai.generate_content(prompt)
                st.success("### Jawaban:")
                st.write(respon.text)
            except Exception as e:
                st.error(f"Gagal dapat jawaban: {e}")
    else:
        st.warning("Belum ada soal yang terbaca!")
