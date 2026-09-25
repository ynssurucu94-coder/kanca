import streamlit as st
import pandas as pd
import time

# --- GİZLİLİK VE ŞİFRELEME ---
def check_password():
    def password_entered():
        if st.session_state["password"] == "kanca2024": # BURASI SENİN GİZLİ ŞİFREN
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Kanca Koçluk - Gizli Giriş", type="password", on_change=password_entered, key="password")
        st.info("Lütfen kurumsal erişim şifresini giriniz.")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Hatalı Şifre! Tekrar Deneyin", type="password", on_change=password_entered, key="password")
        return False
    else:
        return True

# --- TASARIM AYARLARI ---
st.set_page_config(page_title="Kanca Koçluk v1.0", page_icon="⚓", layout="wide")

if check_password():
    # --- TASARIM DİLİ (CSS) ---
    st.markdown("""
        <style>
        .main { background-color: #0A0E1A; color: white; }
        .stButton>button { background-color: #FF4B2B; color: white; border-radius: 25px; width: 100%; border:none; height: 50px; font-weight: bold;}
        .kanca-card { background-color: #16213E; padding: 25px; border-radius: 20px; border-left: 5px solid #FF4B2B; margin-bottom: 20px; }
        .ai-box { background-color: #1B262C; border: 1px dashed #FF4B2B; padding: 15px; border-radius: 10px; color: #FFA500; }
        </style>
        """, unsafe_allow_html=True)

    # --- SİSTEM MENÜSÜ ---
    st.sidebar.title("⚓ KANCA v1.0")
    menu = st.sidebar.radio("Menü", ["🚀 Şüheda (Öğrenci)", "🧠 Koç Paneli (Sen)", "🛡️ Veli Portalı"])

    # --- 1. ÖĞRENCİ PANELİ ---
    if menu == "🚀 Şüheda (Öğrenci)":
        st.title("Günün Kancası: Hoş geldin Şüheda!")
        
        st.markdown("<div class='kanca-card'><h4>🎧 Koçundan Mesaj:</h4>'Bugün Matematik-1'deki o zorlandığın konuya beraber kanca atıyoruz. 20 soruyla başlayalım mı?'</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([2,1])
        with col1:
            st.subheader("Günü Kancala")
            soru = st.slider("Bugün kaç soru çözdün?", 0, 300, 50)
            mod = st.select_slider("Şu anki enerjin?", ["Bunalmış", "Yorgun", "Normal", "Enerjik", "Zımba!"])
            if st.button("HEDEFİ KANCALA"):
                with st.spinner('Veriler AI ile analiz ediliyor ve koçuna iletiliyor...'):
                    time.sleep(2)
                st.balloons()
                st.success("Başardın! Kanca yerine oturdu.")
        
        with col2:
            st.subheader("Yol Haritan")
            st.write("🎯 ODTÜ Bilgisayar")
            st.progress(72)
            st.info("Haftalık Hedef: %85 tamamlandı.")

    # --- 2. KOÇ PANELİ ---
    elif menu == "🧠 Koç Paneli (Sen)":
        st.title("Kanca Strateji Merkezi")
        
        col_a, col_b = st.columns([1, 2])
        with col_a:
            st.markdown("<div class='kanca-card'><b>Öğrenci:</b> Şüheda<br><b>Durum:</b> Takip Ediliyor</div>", unsafe_allow_html=True)
            st.write("### 🤖 Kanca AI İçgörüsü")
            st.markdown("<div class='ai-box'>Şüheda son 2 gündür 'Yorgun' girişi yaptı. Sayısal derslerdeki hızında %15 düşüş var. Yarınki programı esnetmenizi öneririm.</div>", unsafe_allow_html=True)
        
        with col_b:
            st.subheader("Gelişim Grafiği")
            chart_data = pd.DataFrame([120, 150, 80, 45, 130], columns=["Soru Sayısı"])
            st.line_chart(chart_data)
            st.write("📌 *Son 5 günlük soru çözüm istatistiği.*")

    # --- 3. VELİ PORTALI ---
    elif menu == "🛡️ Veli Portalı":
        st.title("Veli Huzur Paneli")
        st.markdown("<div class='kanca-card'><h3>Her Şey Kontrol Altında</h3>Şüheda bu hafta disiplinini %20 artırdı. Koç görüşmesi olumlu geçti.</div>", unsafe_allow_html=True)
        st.columns(3)[0].metric("Haftalık Başarı", "%88", "+5%")
