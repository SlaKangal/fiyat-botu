import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import sys

# --- AYARLAR ---
# Senin koyduğun iPhone linki veya istediğin herhangi bir link
URL = "https://www.trendyol.com/apple/iphone-13-128gb-yildiz-isigi-p-150244342"
HEDEF_FIYAT = 40000 # Fiyat bunun altına düşerse mail atar

# --- MAİL BİLGİLERİN ---
GONDEREN_MAIL = "sla.kangal0@gmail.com"
GONDEREN_SIFRE = "stezaunuyfnngwrv"
ALICI_MAIL = "sla.kangal0@gmail.com"

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
        response = requests.get(URL, headers=headers, timeout=20)
        
        if response.status_code == 200:
            print("2. Baglanti basarili! Fiyat taraniyor...", flush=True)
            soup = BeautifulSoup(response.content, "html.parser")
            
            # --- ÇOKLU TARAMA SİSTEMİ ---
            # Trendyol'un kullandığı tüm fiyat kutusu isimlerini sırayla deniyoruz
            olasi_classlar = [
                "prc-dsc",                 # Standart indirimli fiyat
                "product-price-container", # Genel kutu
                "prc-box-sllng",           # Elektronik ürünlerde sık çıkar
                "ps-curr",                 # İndirimsiz fiyat
                "featured-prices"          # Kampanyalı fiyat
            ]
            
            guncel_fiyat = None
            
            for class_adi in olasi_classlar:
                kutu = soup.find("span", {"class": class_adi})
                if not kutu:
                    kutu = soup.find("div", {"class": class_adi})
                
                if kutu:
                    try:
                        # Fiyatı temizle (TL yazısını ve noktaları at)
                        text = kutu.get_text().replace("TL", "").replace(".", "").replace(",", ".")
                        guncel_fiyat = float(text.strip())
                        print(f"🎯 Fiyat '{class_adi}' kutusunda bulundu!", flush=True)
                        break # Bulduysan döngüden çık
                    except:
                        continue # Sayı değilse diğer kutuya bak

            if guncel_fiyat:
                print(f"💰 Guncel Fiyat: {guncel_fiyat} TL", flush=True)
                
                if guncel_fiyat < HEDEF_FIYAT:
                    print("!!! FIYAT DUSUK - MAIL ATILIYOR !!!", flush=True)
                    mail_gonder(guncel_fiyat, URL)
                else:
                    print("Fiyat henüz hedeflediğin seviyeye düşmedi.", flush=True)
            else:
                print("⚠️ Fiyat etiketi bulunamadi. HTML yapısı çok farklı olabilir.", flush=True)
        else:
            print(f"❌ Siteye baglanilamadi. Kod: {response.status_code}", flush=True)
            
    except Exception as e:
        print(f"❌ Genel Hata: {e}", flush=True)

if __name__ == "__main__":
    fiyat_kontrol_et()
