import requests
import re
import smtplib
from email.mime.text import MIMEText
import sys

# --- AYARLAR ---
# Takip ettiğin ürün
URL = "https://www.trendyol.com/apple/iphone-13-128-gb-yildiz-isigi-cep-telefonu-apple-turkiye-garantili-p-150059024"

# BİLDİRİM EŞİĞİ: Fiyat 38.000 TL'nin altına düşerse haber ver
# (Burayı istediğin gibi değiştir)
HEDEF_FIYAT = 38000 

# --- MAİL BİLGİLERİN ---
GONDEREN_MAIL = "sla.kangal0@gmail.com"
GONDEREN_SIFRE = "stezaunuyfnngwrv"
ALICI_MAIL = "sla.kangal0@gmail.com"

headers = {
    "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
}

def mail_gonder(fiyat, link):
    konu = f"ALARM: {fiyat} TL (Indirim Yakalandi!)"
    
    # Buraya ileride kendi Affiliate (Para kazandıran) linkini koyacaksın
    mesaj = f"""
    FIYAT DUSTU! YAKALA!
    --------------------
    Urun Fiyati: {fiyat} TL
    Hedefledigin: {HEDEF_FIYAT} TL
    
    Satin Alma Linki:
    {link}
    """
    
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
            print("2. Baglanti basarili! Fiyat araniyor...", flush=True)
            html_icerigi = response.text
            
            # Script içinden fiyat avlama (Regex)
            match = re.search(r'"sellingPrice":\s*(\d+(\.\d+)?)', html_icerigi)
            if not match:
                match = re.search(r'"sellingPrice":\{"value":\s*(\d+(\.\d+)?)', html_icerigi)

            if match:
                fiyat_text = match.group(1)
                guncel_fiyat = float(fiyat_text)
                
                print(f"💰 Guncel Fiyat: {guncel_fiyat} TL", flush=True)
                
                # --- KARAR ANI ---
                if guncel_fiyat <= HEDEF_FIYAT:
                    print("🚨 FIYAT DUSUK! Mail atiliyor...", flush=True)
                    mail_gonder(guncel_fiyat, URL)
                else:
                    print(f"😴 Fiyat hala yüksek (Hedef: {HEDEF_FIYAT} TL). Mail atılmadı.", flush=True)
                
            else:
                print("⚠️ Fiyat kodu bulunamadi.", flush=True)
        else:
            print(f"❌ Siteye baglanilamadi. Kod: {response.status_code}", flush=True)
            
    except Exception as e:
        print(f"❌ Genel Hata: {e}", flush=True)

if __name__ == "__main__":
    fiyat_kontrol_et()
