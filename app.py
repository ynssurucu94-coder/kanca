import streamlit as st
import pandas as pd
import os
from datetime import datetime

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
COACH_NOTE_FILE = "koc_notu.txt"
UPLOAD_DIR = "uploads"

if not os.path.exists(UPLOAD_DIR):
    try: os.makedirs(UPLOAD_DIR)
    except: pass

def save_entry(entry, filename):
    if os.path.exists(filename):
        df = pd.read_csv(filename)
    else:
        df = pd.DataFrame()
    df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
    df.to_csv(filename, index=False)

# --- LİG VE PUAN HESAPLAMA ---
def get_rank(points):
    if points < 500: return "⚓ Demir Atan"
    if points < 1500: return "🪝 Kancayı Takan"
    if points < 3500: return "🏹 Zıpkın"
    if points < 7000: return "🎓 Üstat"
    return "🔥 Kanca Efsanesi"

# --- TASARIM ---
st.set_page_config(page_title="Kanca Koçluk v1.4", layout="wide")

if check_password():
    st.sidebar.title("⚓ KANCA v1.4")
    menu = st.sidebar.radio("Menü", ["🚀 Öğrenci Paneli", "📦 Kanca Kasası", "🏆 Kanca Ligi", "🧠 Koç Paneli"])

    # --- 1. ÖĞRENCİ PANELİ ---
    if menu == "🚀 Öğrenci Paneli":
        st.title("Günü Kancala, Şüheda!")
        
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
                    if mod in ["Yorgun", "Bunalmış"]: puan += 50
                    
                    save_entry({
                        "Tarih": datetime.now().strftime("%Y-%m-%d %H:%M"), 
                        "Soru": soru, 
                        "Saat": saat,
                        "Mod": mod,
                        "Puan": puan
                    }, DATA_FILE)
                    st.balloons()
                    st.success(f"Tebrikler! Bugün {int(puan)} Kanca Puanı kazandın.")

        with tab2:
            uploaded_file = st.file_uploader("Soru Fotoğrafı Seç", type=['png', 'jpg', 'jpeg'])
            ders = st.selectbox("Ders", ["Matematik", "Fizik", "Kimya", "Biyoloji", "Türkçe"])
            if st.button("KASAYA KİLİTLE"):
                if uploaded_file:
                    fname = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                    file_path = os.path.join(UPLOAD_DIR, fname)
                    with open(file_path, "wb") as f: f.write(uploaded_file.getbuffer())
                    save_entry({"Tarih": datetime.now().strftime("%Y-%m-%d %H:%M"), "Ders": ders, "Dosya": file_path, "Durum": "Çözülmedi"}, VAULT_FILE)
                    st.success("Soru kasaya eklendi!")

    # --- 2. KANCA KASASI ---
    elif menu == "📦 Kanca Kasası":
        st.title("📦 Kanca Kasası")
        if os.path.exists(VAULT_FILE):
            kasa_df = pd.read_csv(VAULT_FILE)
            for index, row in kasa_df.iterrows():
                with st.expander(f"{row['Tarih']} - {row['Ders']} ({row['Durum']})"):
                    if os.path.exists(str(row['Dosya'])):
                        st.image(str(row['Dosya']), use_container_width=True)
                    if row['Durum'] == "Çözülmedi":
                        if st.button("Çözüldü İşaretle", key=f"kasa_{index}"):
                            kasa_df.at[index, 'Durum'] = "Çözüldü"
                            kasa_df.to_csv(VAULT_FILE, index=False)
                            st.rerun()
        else: st.info("Kasa henüz boş.")

    # --- 3. KANCA LİGİ ---
    elif menu == "🏆 Kanca Ligi":
        st.title("🏆 Kanca Ligi")
        suheda_points = 0
        if os.path.exists(DATA_FILE):
            df = pd.read_csv(DATA_FILE)
            if "Puan" in df.columns:
                suheda_points = df["Puan"].sum()
        
        lig_data = pd.DataFrame([
            {"Öğrenci": "🚀 ParagrafAvcısı", "Puan": 4200, "Rütbe": get_rank(4200)},
            {"Öğrenci": "🧪 KimyaBükücü", "Puan": 3850, "Rütbe": get_rank(3850)},
            {"Öğrenci": "⚓ Şüheda (Sen)", "Puan": suheda_points, "Rütbe": get_rank(suheda_points)},
            {"Öğrenci": "📐 GeoMaster", "Puan": 1200, "Rütbe": get_rank(1200)},
            {"Öğrenci": "⚡ VoltMetre", "Puan": 450, "Rütbe": get_rank(450)}
        ]).sort_values(by="Puan", ascending=False).reset_index(drop=True)
        
        st.table(lig_data)
        st.metric("Senin Toplam Puanın", f"{int(suheda_points)} KP", get_rank(suheda_points))

    # --- 4. KOÇ PANELİ ---
    elif menu == "🧠 Koç Paneli":
        st.title("Strateji Merkezi")
        st.subheader("✍️ Şüheda'ya Mesaj Gönder")
        mevcut_not = ""
        if os.path.exists(COACH_NOTE_FILE):
            with open(COACH_NOTE_FILE, "r", encoding="utf-8") as f: mevcut_not = f.read()
        yeni_not = st.text_area("Öğrenci ekranında görünecek not:", value=mevcut_not)
        if st.button("Notu Güncelle"):
            with open(COACH_NOTE_FILE, "w", encoding="utf-8") as f: f.write(yeni_not)
            st.success("Not güncellendi!")
        
        if os.path.exists(DATA_FILE):
            st.write("### Gelişim Grafiği")
            df_koc = pd.read_csv(DATA_FILE)
            st.line_chart(df_koc.set_index("Tarih")["Soru"])
