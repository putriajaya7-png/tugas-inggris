import streamlit as st
import google.generativeai as genai
from PIL import Image
import random

st.set_page_config(
    page_title="English AI Solver - Cyber Edition",
    page_icon="⚡",
    layout="centered"
)

st.markdown("""
<style>
    /* --- GOOGLE FONTS --- */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&family=JetBrains+Mono:wght@400;600&display=swap');

    /* --- GLOBAL THEME & BACKGROUND --- */
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background: radial-gradient(circle at 80% 20%, #1e0813 0%, #060913 45%, #020307 100%) !important;
        color: #f1f5f9 !important;
    }

    /* Subtle grid animation effect */
    [data-testid="stAppViewContainer"]::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background-image: linear-gradient(rgba(239, 68, 68, 0.03) 1px, transparent 1px),
                          linear-gradient(90deg, rgba(30, 58, 138, 0.05) 1px, transparent 1px);
        background-size: 35px 35px;
        pointer-events: none;
        z-index: 0;
    }

    /* --- SIDEBAR STYLING --- */
    [data-testid="stSidebar"] {
        background: rgba(8, 13, 26, 0.85) !important;
        backdrop-filter: blur(15px);
        border-right: 1px solid rgba(239, 68, 68, 0.2) !important;
    }
    
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] label {
        color: #f8fafc !important;
        letter-spacing: 0.5px;
    }

    /* --- HEADER & TITLE STYLING --- */
    .main-title {
        background: linear-gradient(135deg, #ffffff 0%, #94a3b8 50%, #ef4444 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.5rem;
        text-align: center;
        letter-spacing: -1px;
        margin-bottom: 5px;
        text-shadow: 0 0 35px rgba(239, 68, 68, 0.3);
    }
    
    .sub-title {
        color: #94a3b8;
        text-align: center;
        font-size: 0.95rem;
        margin-bottom: 25px;
        font-weight: 400;
    }

    /* --- INPUT FIELDS & TEXTAREA --- */
    .stTextArea textarea, .stTextInput input {
        background-color: rgba(15, 23, 42, 0.75) !important;
        border: 1px solid rgba(239, 68, 68, 0.3) !important;
        color: #f8fafc !important;
        border-radius: 12px !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
        transition: all 0.3s ease;
    }

    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #ef4444 !important;
        box-shadow: 0 0 15px rgba(239, 68, 68, 0.4) !important;
    }

    /* --- RADIO BUTTONS & SELECTBOX --- */
    div[data-baseweb="select"] > div {
        background-color: rgba(15, 23, 42, 0.8) !important;
        border: 1px solid rgba(239, 68, 68, 0.3) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
    }

    .stRadio label {
        color: #cbd5e1 !important;
        font-weight: 500;
    }

    /* --- BUTTON STYLING (GLOW RED & NAVY) --- */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #dc2626 0%, #991b1b 50%, #1e1b4b 100%) !important;
        color: #ffffff !important;
        border: 1px solid rgba(248, 113, 113, 0.4) !important;
        padding: 12px 24px !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 25px rgba(220, 38, 38, 0.35);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        cursor: pointer;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(239, 68, 68, 0.6) !important;
        border-color: #fca5a5 !important;
        background: linear-gradient(135deg, #ef4444 0%, #b91c1c 50%, #312e81 100%) !important;
    }

    .stButton > button:active {
        transform: translateY(0);
    }

    /* --- CARD CONTAINERS & ALERT BOXES --- */
    .stSuccess {
        background: rgba(15, 23, 42, 0.85) !important;
        border: 1px solid rgba(239, 68, 68, 0.4) !important;
        border-left: 5px solid #ef4444 !important;
        color: #f8fafc !important;
        border-radius: 12px !important;
        backdrop-filter: blur(10px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
    }

    .stWarning {
        background: rgba(30, 27, 75, 0.75) !important;
        border: 1px solid rgba(245, 158, 11, 0.4) !important;
        color: #fef3c7 !important;
        border-radius: 12px !important;
    }

    /* File uploader custom style */
    [data-testid="stFileUploader"] {
        background: rgba(15, 23, 42, 0.6) !important;
        border: 2px dashed rgba(239, 68, 68, 0.3) !important;
        border-radius: 16px !important;
        padding: 10px !important;
        transition: border-color 0.3s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #ef4444 !important;
    }

    /* --- BADGE DEKORASI FUTURISTIK --- */
    .cyber-badge {
        display: inline-block;
        padding: 4px 12px;
        background: rgba(239, 68, 68, 0.15);
        border: 1px solid rgba(239, 68, 68, 0.4);
        color: #fca5a5;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        border-radius: 20px;
        margin-bottom: 12px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
</style>
""", unsafe_allow_html=True)

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
            
            # Model resmi rekomendasi Google terbaru
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

st.markdown("<div style='text-align: center;'><span class='cyber-badge'>⚡ Powered by Gemini 3.6 Flash</span></div>", unsafe_allow_html=True)
st.markdown("<h1 class='main-title'>English Expert AI</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Solusi Cerdas & Analisis Tugas Bahasa Inggris Berbasis AI</p>", unsafe_allow_html=True)

# --- SIDEBAR CONTROL ---
st.sidebar.markdown("### 🎛️ AI Settings")
level = st.sidebar.selectbox("Pilih Jenjang Sekolah:", ["SD", "SMP", "SMA", "Kuliah"])
st.sidebar.markdown("---")
st.sidebar.markdown("<small style='color: #64748b;'>Theme: <b>Cyber Crimson & Navy</b><br>Engine: <b>Gemini Multi-Key Active</b></small>", unsafe_allow_html=True)

metode = st.radio("Pilih Metode Input Soal:", ["Ketik Teks", "Upload Foto Soal"])

if metode == "Ketik Teks":
    soal_teks = st.text_area("Masukkan Soal Bahasa Inggris:", placeholder="Ketik soal atau kalimat di sini...", height=150)
    if st.button("Dapatkan Jawaban ✨"):
        if soal_teks:
            with st.spinner("⚡ AI sedang memproses & menganalisis jawaban..."):
                hasil = generate_with_retry(f"Jawab dan jelaskan soal Bahasa Inggris tingkat {level} ini: {soal_teks}")
                st.markdown("---")
                st.success("### 💡 Hasil Jawaban & Penjelasan:")
                st.write(hasil)
        else:
            st.warning("⚠️ Tolong ketik soalnya terlebih dahulu!")

else:
    file_gambar = st.file_uploader("Upload Foto Soal (JPG, PNG, JPEG):", type=['jpg', 'png', 'jpeg'])
    if file_gambar:
        img = Image.open(file_gambar)
        st.image(img, caption="📷 Foto Soal Terdeteksi", use_container_width=True)
        
        if st.button("Jelaskan Gambar & Jawab ✨"):
            with st.spinner("⚡ AI sedang memindai foto & mencari jawaban..."):
                instruksi = f"Jelaskan secara detail isi gambar ini dan jawab soal Bahasa Inggris tingkat {level} tersebut."
                hasil = generate_with_retry(instruksi, img)
                
                st.markdown("---")
                st.success("### 💡 Hasil Analisis Foto & Jawaban:")
                st.write(hasil)
