import streamlit as st
import google.generativeai as genai
import easyocr
from PIL import Image
import numpy as np

# --- 1. SETTING API KEY ---
# Mengambil kunci otomatis dari menu Secrets Streamlit
try:
    KUNCI_API = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error("Waduh, GEMINI_API_KEY belum diisi di menu Secrets!")
    st.stop()

genai.configure(api_key=KUNCI_API)
model_ai = genai.GenerativeModel('gemini-1.5-flash')

# Fungsi Pembaca Gambar (OCR)
@st.cache_resource
def load_reader():
    return easyocr.Reader(['en'])

reader = load_reader()

# --- 2. TAMPILAN APLIKASI ---
st.set_page_config(page_title="English AI Solver", layout="centered")
st.title("🎓 English Expert Solver")
st.write("Jawab soal Bahasa Inggris dari jenjang TK sampai S2 dengan cerdas!")

# Pilihan Jenjang
level = st.sidebar.selectbox("Pilih Jenjang:", ["TK", "SD", "SMP", "SMA", "S1", "S2"])
cara_input = st.radio("Metode Input:", ["Ketik Teks", "Upload Foto"])

soal_teks = ""

if cara_input == "Ketik Teks":
    soal_teks = st.text_area("Masukkan soal kamu di sini...")
else:
    unggah_foto = st.file_uploader("Pilih foto soal (JPG/PNG)", type=['jpg', 'jpeg', 'png'])
    if unggah_foto:
        img = Image.open(unggah_foto)
        st.image(img, caption="Foto Soal Kamu", width=350)
        with st.spinner("Sedang membaca tulisan di foto..."):
            hasil_scan = reader.readtext(np.array(img), detail=0)
            soal_teks = " ".join(hasil_scan)
            st.info(f"Teks yang terbaca: {soal_teks}")

# --- 3. PROSES JAWABAN ---
if st.button("Dapatkan Jawaban ✨"):
    if soal_teks:
        with st.spinner("AI sedang meramu jawaban terbaik..."):
            instruksi = f"""
            Anda adalah guru Bahasa Inggris pakar. Jawablah soal berikut untuk jenjang pendidikan {level}.
            Berikan jawaban yang akurat, penjelasan tata bahasa yang mudah dimengerti sesuai level tersebut.
            
            Soal: {soal_teks}
            """
            try:
                respon = model_ai.generate_content(instruksi)
                st.markdown("---")
                st.success(f"### Jawaban Level {level}:")
                st.write(respon.text)
            except Exception as e:
                st.error(f"Terjadi kesalahan API: {str(e)}")
    else:
        st.warning("Mohon masukkan soal atau upload foto dulu ya!")
