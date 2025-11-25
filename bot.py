import requests
import re # Düzenli ifadeler (Metin içinde avlanmak için)
import smtplib
from email.mime.text import MIMEText
import sys

# --- AYARLAR ---
URL = "https://www.trendyol.com/apple/iphone-13-128gb-yildiz-isigi-p-150244342"
HEDEF_FIYAT = 40000 

# --- BİLGİLERİN ---
GONDEREN_MAIL = "sla.kangal0@gmail.com"
GONDEREN_SIFRE = "stezaunuyfnngwrv"
ALICI_MAIL = "sla.kangal0@gmail.com"

headers = {
    # Google Bot taklidi yapıyoruz ki Trendyol bizi engellemesin
    "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
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
            print("2. Baglanti basarili! Kodlar taraniyor...", flush=True)
            html_icerigi = response.text
            
            # YÖNTEM 1: "sellingPrice" değerini ara (En garantisi)
            # Trendyol'un arka plan verisinde fiyat genelde şöyle durur: "sellingPrice":35000
            match = re.search(r'"sellingPrice":\s*(\d+(\.\d+)?)', html_icerigi)
            
            if not match:
                # YÖNTEM 2: Alternatif yazım şekli "sellingPrice":{"value":35000
                match = re.search(r'"sellingPrice":\{"value":\s*(\d+(\.\d+)?)', html_icerigi)

            if match:
                # Bulunan fiyatı al
                fiyat_text = match.group(1)
                guncel_fiyat = float(fiyat_text)
                
                print(f"💰 Guncel Fiyat (Scriptten Bulundu): {guncel_fiyat} TL", flush=True)
                
                # Test için mail atalım
                print("🧪 TEST MODU: Fiyat bulundu, mail atiliyor...", flush=True)
                mail_gonder(guncel_fiyat, URL)
                
            else:
                print("⚠️ Fiyat kodların içinde de bulunamadi.", flush=True)
                # Sayfa başlığını yazdıralım, belki 'Robot Doğrulama' sayfasına düşüyoruzdur
                baslik_match = re.search(r'<title>(.*?)</title>', html_icerigi)
                if baslik_match:
                    print(f"Sayfa Başlığı: {baslik_match.group(1)}", flush=True)
                else:
                    print("Sayfa başlığı okunamadı.", flush=True)
                    
        else:
            print(f"❌ Siteye baglanilamadi. Kod: {response.status_code}", flush=True)
            
    except Exception as e:
        print(f"❌ Genel Hata: {e}", flush=True)

if __name__ == "__main__":
    fiyat_kontrol_et()
