import streamlit as st
import google.generativeai as genai
from PIL import Image
import random

st.set_page_config(
    page_title="English Expert AI - Cyber Edition",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* --- GOOGLE FONTS IMPORT --- */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');

    /* --- ROOT VARIABLES & COLOR PALETTE --- */
    :root {
        --bg-dark: #030712;
        --bg-card: rgba(15, 23, 42, 0.75);
        --accent-crimson: #ef4444;
        --accent-crimson-glow: rgba(239, 68, 68, 0.4);
        --accent-navy: #1e3a8a;
        --accent-navy-dark: #0f172a;
        --text-primary: #f8fafc;
        --text-secondary: #94a3b8;
        --border-color: rgba(239, 68, 68, 0.25);
    }

    /* --- GLOBAL BACKGROUND & MESH GRADIENT --- */
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        background: radial-gradient(circle at 15% 15%, #1e050f 0%, #060913 50%, #020307 100%) !important;
        color: var(--text-primary) !important;
    }

    /* Ambient Cyber Mesh Grid Background Overlay */
    [data-testid="stAppViewContainer"]::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background-image: 
            linear-gradient(rgba(239, 68, 68, 0.04) 1px, transparent 1px),
            linear-gradient(90deg, rgba(30, 58, 138, 0.06) 1px, transparent 1px);
        background-size: 32px 32px;
        pointer-events: none;
        z-index: 0;
    }

    /* --- SIDEBAR STYLING (NAVY GLASSMORPHISM) --- */
    [data-testid="stSidebar"] {
        background: rgba(10, 16, 30, 0.88) !important;
        backdrop-filter: blur(20px) saturate(180%);
        -webkit-backdrop-filter: blur(20px) saturate(180%);
        border-right: 1px solid rgba(239, 68, 68, 0.3) !important;
        box-shadow: 5px 0 25px rgba(0, 0, 0, 0.5);
    }
    
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] label {
        color: #f1f5f9 !important;
        font-weight: 600;
        letter-spacing: 0.5px;
    }

    /* --- TYPOGRAPHY & HEADER STYLING --- */
    .hero-container {
        text-align: center;
        padding: 20px 0 10px 0;
        margin-bottom: 25px;
        position: relative;
    }

    .main-title {
        background: linear-gradient(135deg, #ffffff 0%, #fca5a5 40%, #ef4444 80%, #991b1b 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.8rem;
        letter-spacing: -1.5px;
        margin-bottom: 8px;
        filter: drop-shadow(0 0 20px rgba(239, 68, 68, 0.35));
    }
    
    .sub-title {
        color: #94a3b8;
        font-size: 1rem;
        font-weight: 400;
        letter-spacing: 0.2px;
        margin-bottom: 20px;
    }

    /* --- INPUT FIELDS & TEXTAREAS --- */
    .stTextArea textarea, .stTextInput input {
        background-color: rgba(15, 23, 42, 0.85) !important;
        border: 1px solid rgba(239, 68, 68, 0.35) !important;
        color: #f8fafc !important;
        border-radius: 14px !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 1rem !important;
        padding: 14px !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #ef4444 !important;
        box-shadow: 0 0 20px rgba(239, 68, 68, 0.5), 0 0 5px rgba(30, 58, 138, 0.8) !important;
        background-color: rgba(15, 23, 42, 0.95) !important;
    }

    /* --- SELECTBOX & DROPDOWN --- */
    div[data-baseweb="select"] > div {
        background-color: rgba(15, 23, 42, 0.85) !important;
        border: 1px solid rgba(239, 68, 68, 0.35) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        transition: all 0.3s ease;
    }

    div[data-baseweb="select"]:hover > div {
        border-color: #ef4444 !important;
        box-shadow: 0 0 15px rgba(239, 68, 68, 0.3);
    }

    .stRadio label {
        color: #cbd5e1 !important;
        font-weight: 600 !important;
        font-size: 0.95rem;
    }

    /* --- ACTION BUTTONS (CYBER CRIMSON GLOW) --- */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #dc2626 0%, #b91c1c 45%, #1e1b4b 100%) !important;
        color: #ffffff !important;
        border: 1px solid rgba(248, 113, 113, 0.5) !important;
        padding: 14px 28px !important;
        font-size: 1.05rem !important;
        font-weight: 700 !important;
        border-radius: 14px !important;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 25px rgba(220, 38, 38, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.2);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }

    .stButton > button:hover {
        transform: translateY(-3px) scale(1.01);
        box-shadow: 0 10px 35px rgba(239, 68, 68, 0.75), 0 0 15px rgba(30, 58, 138, 0.6) !important;
        border-color: #fca5a5 !important;
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 45%, #312e81 100%) !important;
    }

    .stButton > button:active {
        transform: translateY(-1px);
    }

    /* --- ALERT & SUCCESS BOXES --- */
    .stSuccess {
        background: rgba(15, 23, 42, 0.9) !important;
        border: 1px solid rgba(239, 68, 68, 0.45) !important;
        border-left: 6px solid #ef4444 !important;
        color: #f8fafc !important;
        border-radius: 14px !important;
        backdrop-filter: blur(12px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.7);
        padding: 20px !important;
    }

    .stWarning {
        background: rgba(30, 27, 75, 0.85) !important;
        border: 1px solid rgba(245, 158, 11, 0.5) !important;
        border-left: 6px solid #f59e0b !important;
        color: #fef3c7 !important;
        border-radius: 14px !important;
    }

    /* FILE UPLOADER CUSTOM STYLE */
    [data-testid="stFileUploader"] {
        background: rgba(15, 23, 42, 0.65) !important;
        border: 2px dashed rgba(239, 68, 68, 0.35) !important;
        border-radius: 16px !important;
        padding: 16px !important;
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #ef4444 !important;
        background: rgba(15, 23, 42, 0.85) !important;
        box-shadow: 0 0 20px rgba(239, 68, 68, 0.25);
    }

    /* --- CYBER BADGE DEKORASI --- */
    .cyber-badge {
        display: inline-block;
        padding: 6px 16px;
        background: rgba(239, 68, 68, 0.12);
        border: 1px solid rgba(239, 68, 68, 0.4);
        color: #fca5a5;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.78rem;
        font-weight: 600;
        border-radius: 30px;
        margin-bottom: 14px;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        box-shadow: 0 0 15px rgba(239, 68, 68, 0.2);
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
