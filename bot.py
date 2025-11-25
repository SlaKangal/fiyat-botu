import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import sys

# --- AYARLAR ---
URL = "https://www.trendyol.com/sony/wh-ch520-kablosuz-kulak-ustu-kulaklik-bej-p-686963999"

# --- SENİN BİLGİLERİNİ ELLE GİRDİM ---
GONDEREN_MAIL = "sla.kangal0@gmail.com"
GONDEREN_SIFRE = "stezaunuyfnngwrv"  # Senin verdiğin 16 haneli kod
ALICI_MAIL = "sla.kangal0@gmail.com"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
}

def mail_gonder(fiyat, link):
    konu = f"TEST ALARMI: {fiyat} TL"
    mesaj = f"Sistem Calisiyor!\nSu anki Fiyat: {fiyat} TL\nLink: {link}"
    
    try:
        # local_hostname hatayı önler
        server = smtplib.SMTP('smtp.gmail.com', 587, local_hostname='localhost')
        server.starttls()
        server.login(GONDEREN_MAIL, GONDEREN_SIFRE)
        
        msg = MIMEText(mesaj, 'plain', 'utf-8')
        msg['Subject'] = konu
        msg['From'] = GONDEREN_MAIL
        msg['To'] = ALICI_MAIL
        
        server.sendmail(GONDEREN_MAIL, ALICI_MAIL, msg.as_string())
        server.quit()
        print("✅ Mail basariyla gonderildi!", flush=True)
    except Exception as e:
        print(f"❌ Mail Hatasi: {e}", flush=True)

def fiyat_kontrol_et():
    print("1. Siteye baglaniliyor...", flush=True)
    try:
        response = requests.get(URL, headers=headers, timeout=20)
        
        if response.status_code == 200:
            print("2. Baglanti basarili! Fiyat okunuyor...", flush=True)
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Trendyol fiyat alanı
            fiyat_container = soup.find("span", {"class": "prc-dsc"})
            if not fiyat_container:
                 fiyat_container = soup.find("div", {"class": "product-price-container"})

            if fiyat_container:
                fiyat_text = fiyat_container.get_text().replace("TL", "").replace(".", "").replace(",", ".")
                guncel_fiyat = float(fiyat_text.strip())
                print(f"💰 Guncel Fiyat: {guncel_fiyat} TL", flush=True)
                
                # --- ZORLA MAIL TESTİ ---
                print("🧪 TEST MODU: Mail atiliyor...", flush=True)
                mail_gonder(guncel_fiyat, URL)
                
            else:
                print("⚠️ Fiyat etiketi bulunamadi. Yine de mail testi yapılıyor.", flush=True)
                mail_gonder(0, URL)
        else:
            print(f"❌ Siteye baglanilamadi. Kod: {response.status_code}", flush=True)
            
    except Exception as e:
        print(f"❌ Genel Hata: {e}", flush=True)

if __name__ == "__main__":
    fiyat_kontrol_et()
