import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. KONFIGURASI AI
try:
    kunci = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=kunci)
    # Model 1.5-flash adalah yang terbaik untuk menjelaskan gambar
    model_ai = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Kunci API bermasalah. Cek menu Secrets! Error: {e}")
    st.stop()

# 2. TAMPILAN APLIKASI
st.set_page_config(page_title="English AI Solver", layout="centered")
st.title("🎓 English Expert Solver")
st.write("Gunakan foto soalmu, dan saya akan menjelaskannya!")

level = st.sidebar.selectbox("Pilih Jenjang:", ["SD", "SMP", "SMA", "Kuliah"])
metode = st.radio("Pilih Cara:", ["Ketik Teks", "Upload Foto Soal"])

# 3. LOGIKA JAWABAN
if metode == "Ketik Teks":
    soal_teks = st.text_area("Masukkan soal:")
    if st.button("Dapatkan Jawaban ✨"):
        if soal_teks:
            with st.spinner("Berpikir..."):
                respon = model_ai.generate_content(f"Jawab soal {level} ini: {soal_teks}")
                st.success("### Jawaban:")
                st.write(respon.text)
        else:
            st.warning("Ketik soalnya dulu ya!")

else:
    file_gambar = st.file_uploader("Pilih foto soal", type=['jpg', 'png', 'jpeg'])
    if file_gambar:
        img = Image.open(file_gambar)
        st.image(img, caption="Foto Berhasil Diupload", width=400)
        
        # FITUR KHUSUS: Penjelasan Gambar
        if st.button("Jelaskan Gambar & Jawab ✨"):
            with st.spinner("AI sedang melihat dan menganalisis gambarmu..."):
                try:
                    # AI langsung membaca gambar dan memberikan penjelasan
                    instruksi = f"Jelaskan secara detail apa yang ada di gambar ini, lalu berikan jawaban yang tepat untuk soal Bahasa Inggris tingkat {level} tersebut."
                    respon = model_ai.generate_content([instruksi, img])
                    
                    st.markdown("---")
                    st.success("### Hasil Analisis & Jawaban:")
                    st.write(respon.text)
                except Exception as e:
                    st.error(f"AI gagal memproses gambar. Pastikan gambar jelas! Error: {e}")
