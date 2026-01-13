import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. SETUP API ---
try:
    kunci = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=kunci)
    # Model flash ini paling hebat untuk menjelaskan isi foto
    model_ai = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Gagal baca Secrets: {e}")
    st.stop()

# --- 2. TAMPILAN ---
st.set_page_config(page_title="English Expert Solver")
st.title("🎓 English Expert Solver")
st.write("Upload foto soalmu, dan AI akan menjelaskannya untukmu!")

level = st.sidebar.selectbox("Pilih Jenjang:", ["SD", "SMP", "SMA", "S1"])
metode = st.radio("Pilih Cara:", ["Ketik Teks", "Upload Foto Soal"])

# --- 3. LOGIKA INPUT ---
if metode == "Ketik Teks":
    soal_teks = st.text_area("Masukkan soal:")
    if st.button("Dapatkan Jawaban ✨"):
        if soal_teks:
            with st.spinner("Berpikir..."):
                respon = model_ai.generate_content(f"Jawab soal {level} ini: {soal_teks}")
                st.success("### Jawaban:")
                st.write(respon.text)
        else:
            st.warning("Isi soalnya dulu!")

else:
    file_gambar = st.file_uploader("Pilih foto soal", type=['jpg', 'png', 'jpeg'])
    if file_gambar:
        img = Image.open(file_gambar)
        st.image(img, caption="Foto yang akan dianalisis", width=400)
        
        # Sesuai maumu: AI menjelaskan gambar di bawahnya
        if st.button("Jelaskan & Jawab ✨"):
            with st.spinner("AI sedang melihat gambarmu..."):
                try:
                    # Prompt khusus agar AI menjelaskan isinya dulu
                    prompt_lengkap = f"Tolong jelaskan apa yang kamu lihat di gambar ini, lalu selesaikan soal Bahasa Inggris tingkat {level} tersebut dengan detail."
                    respon = model_ai.generate_content([prompt_lengkap, img])
                    
                    st.markdown("---")
                    st.success("### Hasil Analisis & Jawaban AI:")
                    st.write(respon.text)
                except Exception as e:
                    st.error(f"Maaf, AI gagal membaca gambar: {e}")
