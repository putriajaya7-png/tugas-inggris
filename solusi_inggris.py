import streamlit as st
import google.generativeai as genai
import easyocr
from PIL import Image
import numpy as np

# --- 1. KONEKSI KE API ---
try:
    # Memanggil kunci dari menu Secrets Streamlit
    KUNCI = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=KUNCI)
    model_ai = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Kunci API tidak terbaca: {e}")
    st.stop()

# --- 2. OCR ---
@st.cache_resource
def load_reader():
    return easyocr.Reader(['en'])
reader = load_reader()

# --- 3. TAMPILAN ---
st.title("🎓 English Expert Solver")
level = st.sidebar.selectbox("Pilih Jenjang:", ["TK", "SD", "SMP", "SMA", "S1", "S2"])
soal_teks = st.text_area("Masukkan soal kamu di sini...")

# --- 4. PROSES ---
if st.button("Dapatkan Jawaban ✨"):
    if soal_teks:
        with st.spinner("Sedang berpikir..."):
            try:
                respon = model_ai.generate_content(f"Jawab soal {level} ini: {soal_teks}")
                st.success("### Jawaban:")
                st.write(respon.text)
            except Exception as e:
                # Ini akan memunculkan pesan error asli dari Google
                st.error(f"Error dari Google: {e}")
    else:
        st.warning("Isi soalnya dulu ya!")
