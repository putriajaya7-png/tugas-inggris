import streamlit as st
import google.generativeai as genai

# AMBIL KUNCI DARI SECRETS
try:
    KUNCI = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=KUNCI)
    model_ai = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Gagal baca Secrets: {e}")
    st.stop()

st.title("🎓 English Expert Solver")
level = st.sidebar.selectbox("Pilih Jenjang:", ["TK", "SD", "SMP", "SMA", "S1", "S2"])
soal = st.text_area("Masukkan soal:")

if st.button("Dapatkan Jawaban ✨"):
    if soal:
        with st.spinner("Sedang memproses..."):
            try:
                respon = model_ai.generate_content(f"Jawab soal {level} ini: {soal}")
                st.success(f"### Jawaban ({level}):")
                st.write(respon.text)
            except Exception as e:
                st.error(f"Error Google: {e}")
    else:
        st.warning("Isi soalnya dulu!")
