import streamlit as st
import google.generativeai as genai
from PIL import Image
import random

st.set_page_config(
    page_title="NEURAL ENGLISH AI - HYPER CYBER EDITION",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* --- IMPORT GOOGLE FONTS FUTURISTIK --- */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700;800;900&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:ital,wght@0,400;0,700;1,400&family=Rajdhani:wght@500;600;700&display=swap');

    /* --- ROOT PALETTE VARIABLES (MERAH + NAVI + UNGU + HITAM) --- */
    :root {
        --bg-black: #020208;
        --bg-navy-dark: #060b1e;
        --navy-accent: #0f172a;
        --purple-core: #7b2cbf;
        --purple-neon: #9d4edd;
        --purple-glow: rgba(157, 78, 221, 0.45);
        --red-crimson: #ff0055;
        --red-neon: #ff003c;
        --red-glow: rgba(255, 0, 60, 0.55);
        --text-pure: #ffffff;
        --text-dim: #94a3b8;
        --glass-bg: rgba(6, 11, 30, 0.75);
    }

    /* --- GLOBAL ANIMATED BACKGROUND --- */
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        background: radial-gradient(circle at 50% 0%, #20002c 0%, #0c0019 30%, #060b1e 60%, #020208 100%) !important;
        color: var(--text-pure) !important;
        overflow-x: hidden;
    }

    /* --- CYBER GRID & NEON MESH OVERLAY --- */
    [data-testid="stAppViewContainer"]::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background-image: 
            linear-gradient(rgba(255, 0, 85, 0.08) 1px, transparent 1px),
            linear-gradient(90deg, rgba(157, 78, 221, 0.08) 1px, transparent 1px),
            radial-gradient(circle at 20% 30%, rgba(255, 0, 60, 0.18) 0%, transparent 40%),
            radial-gradient(circle at 80% 70%, rgba(123, 44, 191, 0.25) 0%, transparent 40%);
        background-size: 36px 36px, 36px 36px, 100% 100%, 100% 100%;
        pointer-events: none;
        z-index: 0;
        animation: gridPulse 10s ease-in-out infinite alternate;
    }

    @keyframes gridPulse {
        0% { opacity: 0.7; transform: scale(1); }
        50% { opacity: 1; transform: scale(1.01); }
        100% { opacity: 0.8; transform: scale(1); }
    }

    /* --- SIDEBAR GLASSMORPHISM ULTRA --- */
    [data-testid="stSidebar"] {
        background: rgba(6, 11, 30, 0.88) !important;
        backdrop-filter: blur(30px) saturate(220%);
        -webkit-backdrop-filter: blur(30px) saturate(220%);
        border-right: 1px solid rgba(157, 78, 221, 0.3) !important;
        box-shadow: 8px 0 35px rgba(255, 0, 85, 0.2), 15px 0 50px rgba(123, 44, 191, 0.2);
    }

    [data-testid="stSidebar"] * {
        color: #f1f5f9 !important;
    }

    /* --- REALISTIC FROSTED GLASS HUD CONTAINER --- */
    .hud-title-container {
        text-align: center;
        padding: 18px 22px;
        margin: 10px auto 18px auto;
        max-width: 550px;
        
        /* FROSTED GLASS EFFECT */
        background: linear-gradient(
            135deg, 
            rgba(255, 255, 255, 0.14) 0%, 
            rgba(15, 23, 42, 0.55) 45%, 
            rgba(123, 44, 191, 0.18) 100%
        ); 
        
        /* MAXIMUM BACKDROP BLUR & SATURATION */
        backdrop-filter: blur(40px) saturate(230%);
        -webkit-backdrop-filter: blur(40px) saturate(230%);
        
        /* GLASS SPECULAR HIGHLIGHT BORDERS */
        border: 1px solid rgba(255, 255, 255, 0.22);
        border-top: 1.8px solid rgba(255, 255, 255, 0.55);
        border-left: 1.8px solid rgba(255, 255, 255, 0.4);
        border-right: 1px solid rgba(255, 255, 255, 0.15);
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        
        border-radius: 26px;
        
        box-shadow: 
            0 20px 45px rgba(0, 0, 0, 0.75),
            0 0 25px rgba(255, 0, 85, 0.2),
            0 0 35px rgba(123, 44, 191, 0.25),
            inset 0 1px 2px rgba(255, 255, 255, 0.5),
            inset 0 -2px 6px rgba(0, 0, 0, 0.6);
            
        position: relative;
        overflow: hidden;
    }

    /* Laser Scanline Bottom Animation */
    .hud-title-container::after {
        content: "";
        position: absolute;
        bottom: 0; left: -100%; width: 100%; height: 2px;
        background: linear-gradient(90deg, transparent, var(--purple-neon), var(--red-neon), transparent);
        animation: scanline 3.5s linear infinite;
    }

    @keyframes scanline {
        0% { left: -100%; }
        100% { left: 100%; }
    }

    .cyber-glitch-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 1.9rem;
        font-weight: 900;
        letter-spacing: 3px;
        background: linear-gradient(135deg, #ffffff 0%, #ff80a0 25%, #d880ff 60%, #ff0055 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 25px var(--red-glow), 0 0 35px var(--purple-glow);
        margin: 4px 0;
        text-transform: uppercase;
        position: relative;
        z-index: 1;
    }

    .cyber-sub {
        font-family: 'JetBrains Mono', monospace;
        color: #cbd5e1;
        font-size: 0.8rem;
        letter-spacing: 1.4px;
        text-transform: uppercase;
        position: relative;
        z-index: 1;
    }

    /* --- STATUS BADGES & LIVE HUD STATS (DIKECILKAN UKURAN KOTAK & TULISANNYA) --- */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 3px 10px; /* Dikecilkan padding kotaknya */
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.25);
        backdrop-filter: blur(15px);
        border-radius: 50px;
        color: #f3e8ff;
        font-family: 'Rajdhani', sans-serif;
        font-size: 0.68rem; /* Dikecilkan ukuran font-nya */
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
        box-shadow: 0 0 10px var(--purple-glow), inset 0 1px 2px rgba(255, 255, 255, 0.3);
        margin-bottom: 4px;
        position: relative;
        z-index: 1;
    }

    .status-dot {
        width: 6px; /* Dikecilkan ukuran titik dot */
        height: 6px;
        background-color: var(--red-neon);
        border-radius: 50%;
        box-shadow: 0 0 8px var(--red-neon);
        animation: pulseNeon 1.2s infinite;
    }

    @keyframes pulseNeon {
        0%, 100% { opacity: 1; transform: scale(1); box-shadow: 0 0 8px var(--red-neon); }
        50% { opacity: 0.3; transform: scale(1.3); box-shadow: 0 0 14px var(--purple-neon); }
    }

    .hud-stats-bar {
        display: flex;
        justify-content: space-around;
        margin-top: 10px;
        padding-top: 10px;
        border-top: 1px solid rgba(255, 255, 255, 0.15);
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        color: #a7f3d0;
        position: relative;
        z-index: 1;
    }

    .hud-stat-item {
        color: #94a3b8;
    }

    .hud-stat-val {
        color: #ff0055;
        font-weight: bold;
    }

    /* --- LAYOUT SPACING FIXES --- */
    .stRadio {
        margin-top: 8px !important;
        margin-bottom: 12px !important;
    }

    .stTextArea, [data-testid="stFileUploader"] {
        margin-top: 6px !important;
        margin-bottom: 14px !important;
    }

    /* --- INPUT CONTROLS (TEXT AREA & INPUTS) --- */
    .stTextArea textarea, .stTextInput input {
        background: rgba(6, 11, 30, 0.88) !important;
        border: 1px solid rgba(157, 78, 221, 0.4) !important;
        color: #ffffff !important;
        border-radius: 16px !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 1rem !important;
        padding: 16px !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6), inset 0 0 15px rgba(123, 44, 191, 0.1);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }

    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: var(--red-neon) !important;
        box-shadow: 0 0 30px var(--red-glow), 0 0 20px var(--purple-glow), inset 0 0 15px rgba(255, 0, 60, 0.2) !important;
        background: rgba(12, 0, 25, 0.95) !important;
    }

    /* --- SELECTBOX & RADIO STYLING --- */
    div[data-baseweb="select"] > div {
        background: rgba(6, 11, 30, 0.92) !important;
        border: 1px solid rgba(255, 0, 85, 0.4) !important;
        border-radius: 14px !important;
        color: #ffffff !important;
        transition: all 0.3s ease;
    }

    div[data-baseweb="select"]:hover > div {
        border-color: var(--purple-neon) !important;
        box-shadow: 0 0 25px var(--purple-glow);
    }

    .stRadio label {
        font-family: 'Orbitron', sans-serif !important;
        color: #e2e8f0 !important;
        font-weight: 600 !important;
        font-size: 0.88rem;
        letter-spacing: 1px;
    }

    /* --- ULTRA HIGH-TECH CYBER BUTTON --- */
    .stButton {
        margin-top: 10px !important;
        margin-bottom: 16px !important;
    }

    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #ff0055 0%, #9d4edd 50%, #060b1e 100%) !important;
        background-size: 200% 200% !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.4) !important;
        padding: 16px 28px !important;
        font-family: 'Orbitron', sans-serif !important;
        font-size: 1.05rem !important;
        font-weight: 800 !important;
        border-radius: 16px !important;
        letter-spacing: 2px;
        text-transform: uppercase;
        box-shadow: 0 6px 35px var(--red-glow), 0 0 30px var(--purple-glow);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }

    .stButton > button:hover {
        background-position: right center !important;
        transform: translateY(-2px) scale(1.01);
        box-shadow: 0 12px 50px var(--red-neon), 0 0 40px var(--purple-neon) !important;
        border-color: #ffffff !important;
    }

    .stButton > button:active {
        transform: translateY(0);
    }

    /* --- RESPONSE HUD DISPLAY CARD --- */
    .stSuccess {
        background: linear-gradient(135deg, rgba(12, 0, 25, 0.95) 0%, rgba(6, 11, 30, 0.95) 100%) !important;
        border: 1px solid var(--purple-neon) !important;
        border-left: 6px solid var(--red-neon) !important;
        color: #f8fafc !important;
        border-radius: 18px !important;
        backdrop-filter: blur(25px);
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.85), 0 0 35px var(--red-glow), 0 0 25px var(--purple-glow);
        padding: 24px !important;
        margin-top: 15px !important;
    }

    .stWarning {
        background: rgba(20, 5, 25, 0.9) !important;
        border: 1px solid rgba(255, 0, 85, 0.6) !important;
        border-left: 6px solid var(--red-neon) !important;
        color: #ffe4e6 !important;
        border-radius: 14px !important;
        margin-top: 12px !important;
    }

    /* FILE UPLOADER CYBER BOX */
    [data-testid="stFileUploader"] {
        background: rgba(6, 11, 30, 0.75) !important;
        border: 2px dashed rgba(157, 78, 221, 0.5) !important;
        border-radius: 18px !important;
        padding: 20px !important;
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: var(--red-neon) !important;
        background: rgba(15, 5, 30, 0.9) !important;
        box-shadow: 0 0 35px var(--red-glow), 0 0 25px var(--purple-glow);
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

st.markdown("""
<div class="hud-title-container">
    <div class="status-badge">
        <span class="status-dot"></span> NEURAL ENGINE 3.6 FLASH • QUANTUM ACTIVE
    </div>
    <div class="cyber-glitch-title">BRAIN SOLVER</div>
    <div class="cyber-sub">SOLUSI CERDAS & ANALISIS TUGAS</div>
    <div class="hud-stats-bar">
        <span class="hud-stat-item">PALETTE: <span class="hud-stat-val">RED • NAVY • PURPLE • OBSIDIAN</span></span>
        <span class="hud-stat-item">LATENCY: <span class="hud-stat-val">&lt; 1.2s</span></span>
        <span class="hud-stat-item">STATUS: <span class="hud-stat-val">ONLINE ⚡</span></span>
    </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("### 🎛️ AI CONTROL CENTER")
level = st.sidebar.selectbox("Pilih Jenjang Sekolah:", ["SD", "SMP", "SMA", "Kuliah"])

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="background: linear-gradient(135deg, rgba(255,0,85,0.1) 0%, rgba(123,44,191,0.15) 100%); padding: 16px; border-radius: 14px; border: 1px solid rgba(157,78,221,0.4); box-shadow: 0 0 20px rgba(123,44,191,0.2);">
    <small style="color: #cbd5e1; font-family: 'JetBrains Mono', monospace; line-height: 1.6;">
        <b style="color: #ff0055;">PALETTE:</b> MERAH, NAVI, UNGU, HITAM<br>
        <b style="color: #9d4edd;">ENGINE:</b> GEMINI MULTI-KEY ROTATION<br>
        <b style="color: #38bdf8;">SECURITY:</b> ENCRYPTED NEURAL SESSION
    </small>
</div>
""", unsafe_allow_html=True)

metode = st.radio("Pilih Metode Input Soal:", ["Ketik Teks", "Upload Foto Soal"])

if metode == "Ketik Teks":
    soal_teks = st.text_area("Masukkan Soal:", placeholder="Ketik soal atau kalimat di sini...", height=150)
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
