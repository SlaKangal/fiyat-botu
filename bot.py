import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import os
import sys # İşlemi zorla bitirmek için

# --- AYARLAR ---
URL = "https://www.amazon.com.tr/dp/B07GDR2LYK"
HEDEF_FIYAT = 15000 

# Şifreleri GitHub Secrets'tan alıyoruz
try:
    GONDEREN_MAIL = os.environ["MAIL_ADRESI"]
    GONDEREN_SIFRE = os.environ["MAIL_SIFRESI"]
    ALICI_MAIL = os.environ["MAIL_ADRESI"]
except KeyError:
    print("❌ HATA: GitHub Secrets (Sifreler) okunamadi! Ayarlari kontrol et.")
    sys.exit(1)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Accept-Language": "tr-TR"
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
        print("✅ Mail basariyla gonderildi!")
    except Exception as e:
        print(f"❌ Mail Hatasi: {e}")

def fiyat_kontrol_et():
    print("Kontrol ediliyor...")
    try:
        # TIMEOUT EKLENDİ: 15 saniye cevap gelmezse hata verip kapatır.
        response = requests.get(URL, headers=headers, timeout=15)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Fiyatı bul
            fiyat_span = soup.find("span", {"class": "a-price-whole"})
            if fiyat_span:
                guncel_fiyat = float(fiyat_span.get_text().replace(".", "").replace(",", "."))
                print(f"Guncel Fiyat: {guncel_fiyat} TL")
                
                if guncel_fiyat < HEDEF_FIYAT:
                    print("!!! FIYAT DUSUK - MAIL ATILIYOR !!!")
                    mail_gonder(guncel_fiyat, URL)
                else:
                    print("Fiyat henüz düşmedi.")
            else:
                print("Fiyat alani bulunamadi (Amazon HTML degistirmis olabilir).")
        else:
            print(f"Siteye baglanilamadi. Kod: {response.status_code}")
            
    except requests.exceptions.Timeout:
        print("❌ HATA: Amazon çok yavaş cevap verdi (Zaman Aşımı).")
    except Exception as e:
        print(f"❌ Genel Hata: {e}")

# SADECE 1 KERE ÇALIŞIR
if __name__ == "__main__":
    fiyat_kontrol_et()
    print("İşlem bitti, bot kapatılıyor.")
