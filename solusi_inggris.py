import streamlit as st
import google.generativeai as genai
from PIL import Image
import random

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="English AI Solver", layout="centered")

# --- FUNGSI SMART GENERATE (ANTI-LIMIT & ANTI-ERROR) ---
def generate_with_retry(prompt, image=None):
    if "GEMINI_KEYS" not in st.secrets:
        return "❌ Error: 'GEMINI_KEYS' belum dipasang atau belum tersimpan di menu Secrets Streamlit Cloud!"
        
    daftar_kunci = st.secrets["GEMINI_KEYS"]
    
    # Memastikan format API Keys berupa list
    if isinstance(daftar_kunci, str):
        kunci_acak = [daftar_kunci]
    else:
        kunci_acak = list(daftar_kunci)
        random.shuffle(kunci_acak)

    for kunci in kunci_acak:
        try:
            genai.configure(api_key=kunci)
            
            # Pakai model resmi terbaru yang disarankan API (gemini-3.6-flash)
            model = genai.GenerativeModel('gemini-3.6-flash')
            
            if image:
                response = model.generate_content([prompt, image])
            else:
                response = model.generate_content(prompt)
            
            return response.text
            
        except Exception as e:
            # Jika kuota habis/limit (error 429), ganti ke API Key berikutnya
            if "429" in str(e):
                continue
            else:
                return f"Terjadi kesalahan teknis: {e}"
    
    return "❌ Waduh, semua API Key sedang limit! Coba lagi dalam 1 menit ya."

# --- TAMPILAN APLIKASI ---
st.title("🎓 English Expert Solver")
st.write("Gunakan foto soalmu, dan saya akan menjelaskannya!")

level = st.sidebar.selectbox("Pilih Jenjang:", ["SD", "SMP", "SMA", "Kuliah"])
metode = st.radio("Pilih Cara:", ["Ketik Teks", "Upload Foto Soal"])

# --- LOGIKA JAWABAN ---
if metode == "Ketik Teks":
    soal_teks = st.text_area("Masukkan soal:")
    if st.button("Dapatkan Jawaban ✨"):
        if soal_teks:
            with st.spinner("Sedang mencari jawaban terbaik..."):
                hasil = generate_with_retry(f"Jawab dan jelaskan soal Bahasa Inggris tingkat {level} ini: {soal_teks}")
                st.success("### Jawaban:")
                st.write(hasil)
        else:
            st.warning("Ketik soalnya dulu ya!")

else:
    file_gambar = st.file_uploader("Pilih foto soal", type=['jpg', 'png', 'jpeg'])
    if file_gambar:
        img = Image.open(file_gambar)
        st.image(img, caption="Foto Berhasil Diupload", width=400)
        
        if st.button("Jelaskan Gambar & Jawab ✨"):
            with st.spinner("AI sedang menganalisis gambar..."):
                instruksi = f"Jelaskan secara detail isi gambar ini dan jawab soal Bahasa Inggris tingkat {level} tersebut."
                hasil = generate_with_retry(instruksi, img)
                
                st.markdown("---")
                st.success("### Hasil Analisis & Jawaban:")
                st.write(hasil)
