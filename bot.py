import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import os
import sys

# --- YENİ HEDEF: TRENDYOL ---
# Rastgele bir kulaklık seçtim test için
URL = "https://www.trendyol.com/sony/wh-ch520-kablosuz-kulak-ustu-kulaklik-bej-p-686963999"
HEDEF_FIYAT = 2500 # Şu anki fiyatın biraz altı veya üstü

# Şifreleri Çek
try:
    GONDEREN_MAIL = os.environ["MAIL_ADRESI"]
    GONDEREN_SIFRE = os.environ["MAIL_SIFRESI"]
    ALICI_MAIL = os.environ["MAIL_ADRESI"]
except KeyError:
    print("❌ HATA: Sifreler okunamadi!", flush=True)
    sys.exit(1)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
}

def mail_gonder(fiyat, link):
    konu = f"ALARM: {fiyat} TL"
    mesaj = f"FIYAT DUSTU!\nYeni Fiyat: {fiyat} TL\nLink: {link}"
    
    try:
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
        # Trendyol için timeout 20 saniye
        response = requests.get(URL, headers=headers, timeout=20)
        
        if response.status_code == 200:
            print("2. Baglanti basarili! Veri okunuyor...", flush=True)
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Trendyol'da fiyat genelde 'prc-dsc' class'ındadır
            fiyat_container = soup.find("span", {"class": "prc-dsc"})
            
            # Alternatif class (bazen değişiyor)
            if not fiyat_container:
                 fiyat_container = soup.find("div", {"class": "product-price-container"})

            if fiyat_container:
                fiyat_text = fiyat_container.get_text().replace("TL", "").replace(".", "").replace(",", ".")
                # Bazen '1.200' gelir bazen '1200'. Temizleyelim:
                guncel_fiyat = float(fiyat_text.strip())
                
                print(f"💰 Guncel Fiyat: {guncel_fiyat} TL", flush=True)
                
                # Test amaçlı: Fiyat ne olursa olsun mail atması için mantığı ters çevirdim
                # Normalde küçüktür (<) olmalı. Test için her türlü çalışsın diye print ekledim.
                if guncel_fiyat < HEDEF_FIYAT:
                    print("!!! ALARM TETIKLENDI !!!", flush=True)
                    mail_gonder(guncel_fiyat, URL)
                else:
                    print("Fiyat henüz düşmedi ama sistem çalışıyor.", flush=True)
            else:
                print("⚠️ Fiyat etiketi bulunamadi (Site tasarımı değişmiş olabilir).", flush=True)
                # HTML'in başlığını yazdıralım ki bağlandığımızı kanıtlayalım
                print("Sayfa Başlığı:", soup.title.string, flush=True)
        else:
            print(f"❌ Siteye baglanilamadi. Kod: {response.status_code}", flush=True)
            
    except Exception as e:
        print(f"❌ Genel Hata: {e}", flush=True)

if __name__ == "__main__":
    fiyat_kontrol_et()
