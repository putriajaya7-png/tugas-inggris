import streamlit as st
import google.generativeai as genai
from PIL import Image
import random

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="English AI Solver", layout="centered")

# --- FUNGSI SMART GENERATE (ANTI-LIMIT) ---
def generate_with_retry(prompt, image=None):
    # Ambil daftar kunci dari secrets
    daftar_kunci = st.secrets["GEMINI_KEYS"]
    
    # Acak urutan kunci agar beban terbagi rata
    kunci_acak = list(daftar_kunci)
    random.shuffle(kunci_acak)

    for kunci in kunci_acak:
        try:
            genai.configure(api_key=kunci)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            if image:
                response = model.generate_content([prompt, image])
            else:
                response = model.generate_content(prompt)
            
            return response.text # Berhasil! Kembalikan teks
            
        except Exception as e:
            if "429" in str(e):
                # Jika limit habis, lanjut ke kunci berikutnya
                continue
            else:
                # Jika error lain (misal koneksi), tampilkan errornya
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
                hasil = generate_with_retry(f"Jawab soal {level} ini: {soal_teks}")
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
                                                            
