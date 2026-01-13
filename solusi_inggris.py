import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. SETUP API & MODEL
try:
    kunci = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=kunci)
    # Menggunakan model 1.5-flash karena paling pintar baca gambar
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Kunci API bermasalah: {e}")
    st.stop()

# 2. TAMPILAN
st.set_page_config(page_title="English Expert Solver")
st.title("🎓 English Expert Solver")
st.subheader("Solusi Cerdas Soal Bahasa Inggris")

level = st.sidebar.selectbox("Pilih Jenjang:", ["SD", "SMP", "SMA", "Kuliah"])
metode = st.radio("Pilih Cara:", ["Ketik Teks", "Upload Foto Soal"])

# 3. PROSES INPUT
if metode == "Ketik Teks":
    soal_teks = st.text_area("Masukkan soal kamu di sini:")
    if st.button("Dapatkan Jawaban ✨"):
        if soal_teks:
            with st.spinner("Sedang berpikir..."):
                respon = model.generate_content(f"Jawab soal {level} ini: {soal_teks}")
                st.success("### Penjelasan & Jawaban:")
                st.write(respon.text)
        else:
            st.warning("Ketik soalnya dulu ya!")

else:
    file_gambar = st.file_uploader("Pilih foto soal (JPG/PNG)", type=['jpg', 'jpeg', 'png'])
    if file_gambar:
        gambar = Image.open(file_gambar)
        st.image(gambar, caption="Foto yang kamu upload", width=400)
        
        if st.button("Analisis Gambar & Jawab ✨"):
            with st.spinner("AI sedang membaca dan menjelaskan gambar..."):
                try:
                    # AI langsung membaca gambar dan teks secara bersamaan
                    prompt = f"Tolong jelaskan apa yang ada di gambar ini dan jawab soal Bahasa Inggris tingkat {level} tersebut dengan detail."
                    respon = model.generate_content([prompt, gambar])
                    
                    st.markdown("---")
                    st.success("### Hasil Analisis Gambar:")
                    st.write(respon.text)
                except Exception as e:
                    st.error(f"Gagal memproses gambar: {e}")import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. SETUP API & MODEL
try:
    kunci = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=kunci)
    # Menggunakan model 1.5-flash karena paling pintar baca gambar
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Kunci API bermasalah: {e}")
    st.stop()

# 2. TAMPILAN
st.set_page_config(page_title="English Expert Solver")
st.title("🎓 English Expert Solver")
st.subheader("Solusi Cerdas Soal Bahasa Inggris")

level = st.sidebar.selectbox("Pilih Jenjang:", ["SD", "SMP", "SMA", "Kuliah"])
metode = st.radio("Pilih Cara:", ["Ketik Teks", "Upload Foto Soal"])

# 3. PROSES INPUT
if metode == "Ketik Teks":
    soal_teks = st.text_area("Masukkan soal kamu di sini:")
    if st.button("Dapatkan Jawaban ✨"):
        if soal_teks:
            with st.spinner("Sedang berpikir..."):
                respon = model.generate_content(f"Jawab soal {level} ini: {soal_teks}")
                st.success("### Penjelasan & Jawaban:")
                st.write(respon.text)
        else:
            st.warning("Ketik soalnya dulu ya!")

else:
    file_gambar = st.file_uploader("Pilih foto soal (JPG/PNG)", type=['jpg', 'jpeg', 'png'])
    if file_gambar:
        gambar = Image.open(file_gambar)
        st.image(gambar, caption="Foto yang kamu upload", width=400)
        
        if st.button("Analisis Gambar & Jawab ✨"):
            with st.spinner("AI sedang membaca dan menjelaskan gambar..."):
                try:
                    # AI langsung membaca gambar dan teks secara bersamaan
                    prompt = f"Tolong jelaskan apa yang ada di gambar ini dan jawab soal Bahasa Inggris tingkat {level} tersebut dengan detail."
                    respon = model.generate_content([prompt, gambar])
                    
                    st.markdown("---")
                    st.success("### Hasil Analisis Gambar:")
                    st.write(respon.text)
                except Exception as e:
                    st.error(f"Gagal memproses gambar: {e}")
