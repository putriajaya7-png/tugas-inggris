import streamlit as st
import google.generativeai as genai
import easyocr
from PIL import Image
import numpy as np


    KUNCI_API = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=KUNCI_API)
    model_ai = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Kunci API tidak terbaca di Secrets! Pastikan namanya GEMINI_API_KEY. Error: {e}")
    st.stop()


@st.cache_resource
def load_reader():
    return easyocr.Reader(['en'])
reader = load_reader()


st.set_page_config(page_title="English Expert Solver", layout="centered")
st.title("🎓 English Expert Solver")
st.write("Aplikasi sudah diperbaiki. Silakan masukkan soal!")

level = st.sidebar.selectbox("Pilih Jenjang:", ["TK", "SD", "SMP", "SMA", "S1", "S2"])
cara_input = st.radio("Metode Input:", ["Ketik Teks", "Upload Foto"])

soal_teks = ""

if cara_input == "Ketik Teks":
    soal_teks = st.text_area("Masukkan soal kamu di sini...")
else:
    unggah_foto = st.file_uploader("Pilih foto soal (JPG/PNG)", type=['jpg', 'jpeg', 'png'])
    if unggah_foto:
        img = Image.open(unggah_foto)
        st.image(img, caption="Foto Soal", width=350)
        with st.spinner("Sedang membaca tulisan di foto..."):
            hasil_scan = reader.readtext(np.array(img), detail=0)
            soal_teks = " ".join(hasil_scan)
            st.info(f"Teks yang terbaca: {soal_teks}")


if st.button("Dapatkan Jawaban ✨"):
    if soal_teks:
        with st.spinner("AI sedang meramu jawaban terbaik..."):
            instruksi = f"Anda adalah guru Bahasa Inggris pakar. Jawablah soal berikut untuk jenjang pendidikan {level}: {soal_teks}"
            try:
                respon = model_ai.generate_content(instruksi)
                st.markdown("---")
                st.success(f"### Jawaban Level {level}:")
                st.write(respon.text)
            except Exception as e:
                
                st.error(f"Gagal koneksi ke Google: {e}")
    else:
        st.warning("Mohon masukkan soal atau upload foto dulu ya!")
