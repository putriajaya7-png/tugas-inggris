import streamlit as st
import google.generativeai as genai
from PIL import Image
import random

# --- KONFIGURASI HALAMAN UTAMA ---
st.set_page_config(
    page_title="NEURAL ENGLISH AI - ULTRA CYBER EDITION",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* --- IMPORT GOOGLE FONTS --- */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700;900&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');

    /* --- ROOT VARIABLES --- */
    :root {
        --bg-obsidian: #03050b;
        --navy-dark: #070e1e;
        --navy-accent: #0f1c3f;
        --crimson-neon: #ff003c;
        --crimson-glow: rgba(255, 0, 60, 0.5);
        --crimson-dark: #990024;
        --text-bright: #ffffff;
        --text-dim: #94a3b8;
        --glass-border: rgba(255, 0, 60, 0.3);
    }

    /* --- GLOBAL BACKGROUND & ANIMATED MESH --- */
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        background: radial-gradient(circle at 50% 10%, #150008 0%, #060a17 45%, #020408 100%) !important;
        color: var(--text-bright) !important;
        overflow-x: hidden;
    }

    /* Animated Grid Scanline Background */
    [data-testid="stAppViewContainer"]::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background-image: 
            linear-gradient(rgba(255, 0, 60, 0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(15, 28, 63, 0.15) 1px, transparent 1px);
        background-size: 40px 40px;
        pointer-events: none;
        z-index: 0;
        animation: gridPulse 8s ease-in-out infinite alternate;
    }

    @keyframes gridPulse {
        0% { opacity: 0.6; background-size: 38px 38px; }
        100% { opacity: 1; background-size: 42px 42px; }
    }

    /* --- SIDEBAR GLASSMORPHISM STYLING --- */
    [data-testid="stSidebar"] {
        background: rgba(7, 14, 30, 0.92) !important;
        backdrop-filter: blur(25px) saturate(200%);
        -webkit-backdrop-filter: blur(25px) saturate(200%);
        border-right: 1px solid var(--crimson-neon) !important;
        box-shadow: 10px 0 35px rgba(255, 0, 60, 0.15);
    }

    [data-testid="stSidebar"] * {
        color: #f1f5f9 !important;
    }

    /* --- CYBER HEADER HUD --- */
    .hud-title-container {
        text-align: center;
        padding: 25px 15px;
        margin-bottom: 30px;
        background: rgba(7, 14, 30, 0.7);
        border: 1px solid var(--crimson-neon);
        border-radius: 20px;
        backdrop-filter: blur(15px);
        box-shadow: 0 0 30px rgba(255, 0, 60, 0.2), inset 0 0 15px rgba(255, 0, 60, 0.1);
        position: relative;
        overflow: hidden;
    }

    .hud-title-container::after {
        content: "";
        position: absolute;
        top: 0; left: -100%; width: 100%; height: 2px;
        background: linear-gradient(90deg, transparent, var(--crimson-neon), transparent);
        animation: scanline 3s linear infinite;
    }

    @keyframes scanline {
        0% { left: -100%; }
        100% { left: 100%; }
    }

    .cyber-glitch-title {
        font-family: 'Orbitron', sans-serif !alignment;
        font-size: 2.6rem;
        font-weight: 900;
        letter-spacing: 2px;
        background: linear-gradient(135deg, #ffffff 10%, #ff6b8b 50%, var(--crimson-neon) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 25px var(--crimson-glow);
        margin: 5px 0;
        text-transform: uppercase;
    }

    .cyber-sub {
        font-family: 'JetBrains Mono', monospace;
        color: #94a3b8;
        font-size: 0.88rem;
        letter-spacing: 1px;
    }

    /* --- BADGES & STATUS PILLS --- */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 6px 16px;
        background: rgba(255, 0, 60, 0.1);
        border: 1px solid var(--crimson-neon);
        border-radius: 50px;
        color: #ff809b;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        box-shadow: 0 0 15px var(--crimson-glow);
        margin-bottom: 10px;
    }

    .status-dot {
        width: 8px;
        height: 8px;
        background-color: var(--crimson-neon);
        border-radius: 50%;
        box-shadow: 0 0 10px var(--crimson-neon);
        animation: pulse 1.5s infinite;
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.4; transform: scale(1.3); }
    }

    /* --- INPUT CONTROLS (TEXT AREA & INPUTS) --- */
    .stTextArea textarea, .stTextInput input {
        background: rgba(7, 14, 30, 0.85) !important;
        border: 1px solid rgba(255, 0, 60, 0.35) !important;
        color: #ffffff !important;
        border-radius: 14px !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 1rem !important;
        padding: 16px !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }

    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: var(--crimson-neon) !important;
        box-shadow: 0 0 25px var(--crimson-glow), inset 0 0 10px rgba(255, 0, 60, 0.2) !important;
        background: rgba(10, 20, 45, 0.95) !important;
    }

    /* --- SELECTBOX & DROPDOWN STYLING --- */
    div[data-baseweb="select"] > div {
        background-color: rgba(7, 14, 30, 0.9) !important;
        border: 1px solid rgba(255, 0, 60, 0.4) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        transition: all 0.3s ease;
    }

    div[data-baseweb="select"]:hover > div {
        border-color: var(--crimson-neon) !important;
        box-shadow: 0 0 20px var(--crimson-glow);
    }

    .stRadio label {
        font-family: 'JetBrains Mono', monospace !important;
        color: #e2e8f0 !important;
        font-weight: 600 !important;
        font-size: 0.95rem;
    }

    /* --- HIGH-TECH CYBER BUTTON --- */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #ff003c 0%, #b3002a 50%, #0f1c3f 100%) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        padding: 16px 30px !important;
        font-family: 'Orbitron', sans-serif !important;
        font-size: 1.05rem !important;
        font-weight: 700 !important;
        border-radius: 14px !important;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        box-shadow: 0 4px 30px var(--crimson-glow), inset 0 1px 0 rgba(255, 255, 255, 0.4);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }

    .stButton > button:hover {
        transform: translateY(-3px) scale(1.01);
        box-shadow: 0 10px 45px var(--crimson-neon), 0 0 20px rgba(15, 28, 63, 0.8) !important;
        border-color: #ffffff !important;
        background: linear-gradient(135deg, #ff1e56 0%, #ff003c 50%, #1e3a8a 100%) !important;
    }

    .stButton > button:active {
        transform: translateY(-1px);
    }

    /* --- RESPONSE HUD DISPLAY CARD --- */
    .stSuccess {
        background: rgba(7, 14, 30, 0.95) !important;
        border: 1px solid var(--crimson-neon) !important;
        border-left: 6px solid var(--crimson-neon) !important;
        color: #f8fafc !important;
        border-radius: 16px !important;
        backdrop-filter: blur(20px);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.8), 0 0 20px var(--crimson-glow);
        padding: 24px !important;
    }

    .stWarning {
        background: rgba(15, 28, 63, 0.9) !important;
        border: 1px solid rgba(245, 158, 11, 0.6) !important;
        border-left: 6px solid #f59e0b !important;
        color: #fef3c7 !important;
        border-radius: 14px !important;
    }

    /* FILE UPLOADER CYBER BOX */
    [data-testid="stFileUploader"] {
        background: rgba(7, 14, 30, 0.7) !important;
        border: 2px dashed rgba(255, 0, 60, 0.4) !important;
        border-radius: 18px !important;
        padding: 20px !important;
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: var(--crimson-neon) !important;
        background: rgba(10, 20, 45, 0.9) !important;
        box-shadow: 0 0 25px var(--crimson-glow);
    }
</style>
""", unsafe_allow_html=True)

def generate_with_retry(prompt, image=None):
    """
    Fungsi utama pengolah AI dengan fitur rotasi multi-API key otomatis.
    Logika tetap 100% persis tanpa perubahan alur.
    """
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
            
            # Model resmi rekomendasi Google Gemini terbaru
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

# --- HEADER HUD LAYOUT ---
st.markdown("""
<div class="hud-title-container">
    <div class="status-badge">
        <span class="status-dot"></span> NEURAL ENGINE 3.6 FLASH ONLINE
    </div>
    <div class="cyber-glitch-title">ENGLISH EXPERT AI</div>
    <div class="cyber-sub">SOLUSI CERDAS & ANALISIS TUGAS BAHASA INGGRIS FUTURISTIK</div>
</div>
""", unsafe_allow_html=True)

# --- SIDEBAR STYLING & CONFIG ---
st.sidebar.markdown("### 🎛️ AI CONTROL CENTER")
level = st.sidebar.selectbox("Pilih Jenjang Sekolah:", ["SD", "SMP", "SMA", "Kuliah"])

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="background: rgba(255,0,60,0.05); padding: 12px; border-radius: 10px; border: 1px solid rgba(255,0,60,0.2);">
    <small style="color: #94a3b8; font-family: 'JetBrains Mono', monospace;">
        <b>THEME:</b> CYBER CRIMSON & NAVY<br>
        <b>ENGINE:</b> GEMINI MULTI-KEY ROTATION<br>
        <b>SECURITY:</b> ENCRYPTED SESSION
    </small>
</div>
""", unsafe_allow_html=True)

metode = st.radio("Pilih Metode Input Soal:", ["Ketik Teks", "Upload Foto Soal"])

# --- LOGIKA JAWABAN & INTERAKSI USER ---
if metode == "Ketik Teks":
    soal_teks = st.text_area("Masukkan Soal Bahasa Inggris:", placeholder="Ketik soal atau kalimat di sini...", height=150)
    if st.button("Dapatkan Jawaban ✨"):
        if soal_teks:
            with st.spinner("⚡ NEURAL AI sedang menganalisis & memproses jawaban..."):
                hasil = generate_with_retry(f"Jawab dan jelaskan soal Bahasa Inggris tingkat {level} ini: {soal_teks}")
                st.markdown("---")
                st.success("### 💡 HASIL ANALISIS & JAWABAN:")
                st.write(hasil)
        else:
            st.warning("⚠️ Tolong ketik soalnya terlebih dahulu!")

else:
    file_gambar = st.file_uploader("Upload Foto Soal (JPG, PNG, JPEG):", type=['jpg', 'png', 'jpeg'])
    if file_gambar:
        img = Image.open(file_gambar)
        st.image(img, caption="📷 FOTO SOAL TERDETEKSI OLEH SYSTEM", use_container_width=True)
        
        if st.button("Jelaskan Gambar & Jawab ✨"):
            with st.spinner("⚡ NEURAL AI sedang memindai foto & mencari jawaban..."):
                instruksi = f"Jelaskan secara detail isi gambar ini dan jawab soal Bahasa Inggris tingkat {level} tersebut."
                hasil = generate_with_retry(instruksi, img)
                
                st.markdown("---")
                st.success("### 💡 HASIL ANALISIS FOTO & JAWABAN:")
                st.write(hasil)
