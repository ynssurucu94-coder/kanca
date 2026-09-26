import streamlit as st
import pandas as pd
import os
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# --- GÜVENLİK ---
def check_password():
    def password_entered():
        if st.session_state["password"] == "kanca2024":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False
    if "password_correct" not in st.session_state:
        st.text_input("Kanca Koçluk - Gizli Giriş", type="password", on_change=password_entered, key="password")
        return False
    return st.session_state["password_correct"]

# --- VERİ YÖNETİMİ ---
DATA_FILE = "kanca_veriler.csv"
VAULT_FILE = "kanca_kasa.csv"
DENEME_FILE = "kanca_denemeler.csv"
COACH_NOTE_FILE = "koc_notu.txt"
UPLOAD_DIR = "uploads"

if not os.path.exists(UPLOAD_DIR):
    try: os.makedirs(UPLOAD_DIR)
    except: pass

def save_entry(entry, filename):
    df = pd.read_csv(filename) if os.path.exists(filename) else pd.DataFrame()
    df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
    df.to_csv(filename, index=False)

def get_rank(points):
    if points < 500: return "⚓ Demir Atan"
    if points < 1500: return "🪝 Kancayı Takan"
    if points < 3500: return "🏹 Zıpkın"
    if points < 7000: return "🎓 Üstat"
    return "🔥 Kanca Efsanesi"

# --- TASARIM AYARLARI ---
st.set_page_config(page_title="Kanca Koçluk v1.9", layout="wide")

if check_password():
    st.sidebar.title("⚓ KANCA v1.9")
    menu = st.sidebar.radio("Menü", ["🚀 Öğrenci Paneli", "📦 Kanca Kasası", "📝 Deneme Analizi", "🏆 Kanca Ligi", "🧠 Koç Paneli"])

    # --- 1. ÖĞRENCİ PANELİ ---
    if menu == "🚀 Öğrenci Paneli":
        st.title("Günün Kancası, Şüheda!")
        if os.path.exists(COACH_NOTE_FILE):
            with open(COACH_NOTE_FILE, "r", encoding="utf-8") as f: koc_notu = f.read()
            st.info(f"🎧 Koçunun Mesajı: {koc_notu}")

        tab1, tab2 = st.tabs(["📊 Günlük Takip", "📸 Hata Yükle"])
        with tab1:
            with st.form("gunluk_form"):
                soru = st.number_input("Bugün kaç soru çözdün?", min_value=0, value=100)
                saat = st.number_input("Kaç saat odaklandın?", min_value=0, value=4)
                mod = st.select_slider("Enerjin?", ["Bunalmış", "Yorgun", "Normal", "Enerjik", "Zımba!"])
                if st.form_submit_button("HEDEFİ KANCALA"):
                    puan = soru + (saat * 10)
                    if mod in ["Yorgun", "Bunalmış", "Kaygılı"]: puan += 50
                    save_entry({"Tarih": datetime.now().strftime("%Y-%m-%d %H:%M"), "Soru": soru, "Saat": saat, "Mod": mod, "Puan": puan}, DATA_FILE)
                    st.balloons(); st.success(f"Tebrikler! {int(puan)} KP kazandın.")
        with tab2:
            st.subheader("Hata Teşhis ve Yükleme")
            uploaded_file = st.file_uploader("Soru Fotoğrafı Seç", type=['png', 'jpg', 'jpeg'])
            ders = st.selectbox("Ders", ["Matematik", "Fizik", "Kimya", "Biyoloji", "Türkçe"])
            neden = st.selectbox("Neden Yapamadın?", ["Bilgi Eksikliği", "İşlem Hatası", "Soru Tipi", "Süre Yetmedi", "Dikkatsizlik"])
            if st.button("KASAYA MÜHÜRLE"):
                if uploaded_file:
                    fname = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                    file_path = os.path.join(UPLOAD_DIR, fname)
                    with open(file_path, "wb") as f: f.write(uploaded_file.getbuffer())
                    save_entry({"Tarih": datetime.now().strftime("%Y-%m-%d %H:%M"), "Ders": ders, "Neden": neden, "Dosya": file_path, "Durum": "Çözülmedi"}, VAULT_FILE)
                    st.success("Hata kasaya mühürlendi!")

    # --- 2. KANCA KASASI ---
    elif menu == "📦 Kanca Kasası":
        st.title("📦 Kanca Kasası")
        if os.path.exists(VAULT_FILE):
            kasa_df = pd.read_csv(VAULT_FILE)
            for index, row in kasa_df.iterrows():
                durum_r = "🔴" if row['Durum'] == "Çözülmedi" else "🟢"
                with st.expander(f"{durum_r} {row['Ders']} - {row['Neden']}"):
                    if os.path.exists(str(row['Dosya'])): st.image(str(row['Dosya']), use_container_width=True)
                    if row['Durum'] == "Çözülmedi":
                        if st.button("Çözüldü!", key=f"k_{index}"):
                            kasa_df.at[index, 'Durum'] = "Çözüldü"
                            kasa_df.to_csv(VAULT_FILE, index=False)
                            st.rerun()
        else: st.info("Kasa boş.")

    # --- 3. DENEME ANALİZİ ---
    elif menu == "📝 Deneme Analizi":
        st.title("📝 Detaylı Deneme Analizör")
        with st.form("detayli_deneme"):
            sinav_ad = st.text_input("Sınav Adı")
            c1, c2, c3, c4 = st.columns(4)
            ders_sec = c1.selectbox("Ders", ["Matematik", "Türkçe", "Fizik", "Kimya", "Biyoloji"])
            d = c2.number_input("Doğru", min_value=0, value=0)
            y = c3.number_input("Yanlış", min_value=0, value=0)
            kritik_konu = c4.text_input("Eksik Konu?")
            if st.form_submit_button("NETİ EKLE"):
                save_entry({"Tarih": datetime.now().strftime("%Y-%m-%d"), "Sınav": sinav_ad, "Ders": ders_sec, "Net": d-(y*0.25), "Eksik": kritik_konu}, DENEME_FILE)
                st.success("Kaydedildi.")

    # --- 4. KANCA LİGİ ---
    elif menu == "🏆 Kanca Ligi":
        st.title("🏆 Kanca Ligi")
        pts = pd.read_csv(DATA_FILE)["Puan"].sum() if os.path.exists(DATA_FILE) else 0
        lig_data = pd.DataFrame([
            {"Öğrenci": "🚀 ParagrafAvcısı", "Puan": 4200, "Rütbe": get_rank(4200)},
            {"Öğrenci": "⚓ Şüheda (Sen)", "Puan": pts, "Rütbe": get_rank(pts)},
            {"Öğrenci": "📐 GeoMaster", "Puan": 1200, "Rütbe": get_rank(1200)}
        ]).sort_values(by="Puan", ascending=False).reset_index(drop=True)
        st.table(lig_data)

    # --- 5. KOÇ PANELİ (ZİRVE SÜRÜM) ---
    elif menu == "🧠 Koç Paneli":
        st.title("🧠 Stratejik Komuta Merkezi")
        
        if os.path.exists(DATA_FILE):
            df_k = pd.read_csv(DATA_FILE)
            
            # --- KANCA BAŞARI İNDEKSİ (HSI) HESAPLAMA ---
            # Basit Formül: İstikrar + Verimlilik + Psikoloji
            istikrar = min(len(df_k) * 10, 40)
            verimlilik = min(df_k["Soru"].mean() / 2, 40)
            hsi_score = istikrar + verimlilik + 20 # 20 taban puan
            
            st.write(f"### ⚓ Kanca Başarı İndeksi: {int(hsi_score)} / 100")
            st.progress(hsi_score / 100)
            
            # --- AI ANALİZ VE VELİ RAPORU ---
            col_ai, col_rep = st.columns(2)
            
            with col_ai:
                st.subheader("🤖 Kanca AI İçgörüsü")
                st.info(f"Şüheda'nın istikrarı %{int(istikrar*2.5)}. Hata kasasında çözüm bekleyen konulara odaklanması HSI skorunu artıracaktır.")
            
            with col_rep:
                st.subheader("📊 Otomatik Veli Bülteni")
                toplam = int(df_k["Soru"].sum())
                rapor = f"Sayın Veli, Şüheda bu hafta {toplam} soru çözerek kancayı sıkıladı. Başarı İndeksi {int(hsi_score)} seviyesine yükseldi. Süreç planlı ilerliyor."
                st.text_area("WhatsApp için kopyala:", rapor)

            # --- GRAFİKLER ---
            c1, c2 = st.columns(2)
            if os.path.exists(VAULT_FILE):
                fig = px.pie(pd.read_csv(VAULT_FILE), names='Neden', hole=0.5, title="Hata Karakteri")
                c1.plotly_chart(fig)
            
            if os.path.exists(DENEME_FILE):
                fig_d = px.bar(pd.read_csv(DENEME_FILE), x="Ders", y="Net", color="Ders", title="Branş Başarısı")
                c2.plotly_chart(fig_d)
        
        st.text_area("Şüheda'ya Yeni Mesaj:", key="msg_v9")
        if st.button("Gönder"):
            with open(COACH_NOTE_FILE, "w", encoding="utf-8") as f: f.write(st.session_state.msg_v9)
            st.success("İletildi.")
