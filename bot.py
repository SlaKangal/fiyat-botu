import requests
from bs4 import BeautifulSoup
import time
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

# --- KULLANICI AYARLARI ---
URL = "https://www.amazon.com.tr/dp/B07GDR2LYK"
HEDEF_FIYAT = 15000 
KONTROL_SURESI = 3600 

# Mail Ayarları
GONDEREN_MAIL = "sla.kangal0@gmail.com"
GONDEREN_SIFRE = "stezaunuyfnngwrv"
ALICI_MAIL = "sla.kangal0@gmail.com"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Accept-Language": "tr-TR"
}

def mail_gonder(fiyat, link):
    konu = f"ALARM: {fiyat} TL"
    
    mesaj = f"""
    FIYAT DUSTU! YAKALA!
    --------------------
    Yeni Fiyat: {fiyat} TL
    
    Linke Tikla ve Al:
    {link}
    """
    
    try:
        # --- DÜZELTİLEN KISIM BURASI ---
        # local_hostname='localhost' ekledik ki senin bilgisayar adındaki 'ı' harfini kullanmasın.
        server = smtplib.SMTP('smtp.gmail.com', 587, local_hostname='localhost')
        server.starttls()
        server.login(GONDEREN_MAIL, GONDEREN_SIFRE)
        
        msg = MIMEText(mesaj, 'plain', 'utf-8')
        msg['Subject'] = konu
        msg['From'] = GONDEREN_MAIL
        msg['To'] = ALICI_MAIL
        
        server.sendmail(GONDEREN_MAIL, ALICI_MAIL, msg.as_string())
        server.quit()
        print("✅ Mail basariyla gonderildi! (Telefonunu kontrol et)")
        
    except Exception as e:
        print(f"❌ Mail gonderme hatasi: {e}")

def fiyat_kontrol_et():
    print(f"[{datetime.now().strftime('%H:%M')}] Kontrol ediliyor...")
    try:
        response = requests.get(URL, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            
            try:
                fiyat_span = soup.find("span", {"class": "a-price-whole"})
                if fiyat_span:
                    fiyat_text = fiyat_span.get_text().replace(".", "").replace(",", ".")
                    guncel_fiyat = float(fiyat_text)
                    
                    print(f"   Fiyat: {guncel_fiyat} TL")
                    
                    if guncel_fiyat < HEDEF_FIYAT:
                        print("   !!! FİYAT DÜŞTÜ - MAİL ATILIYOR !!!")
                        mail_gonder(guncel_fiyat, URL)
                        return True 
                else:
                    print("   Fiyat alanı bulunamadı.")
            except Exception as e:
                print(f"   Veri işleme hatası: {e}")
        else:
            print("   Siteye bağlanılamadı.")
            
    except Exception as e:
        print(f"   Bağlantı hatası: {e}")
    return False

print("Bot Başlatıldı (PC Ismi Hatası Düzeltildi)...")
while True:
    mail_atti_mi = fiyat_kontrol_et()
    
    if mail_atti_mi:
        time.sleep(14400) 
    else:
        time.sleep(KONTROL_SURESI)