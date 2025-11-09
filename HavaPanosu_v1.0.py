import customtkinter as ctk
import requests
import datetime

# Tema ayarları
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class HavaPanosu(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🌤️ Hava Panosu 🇹🇷 v1.0")
        self.geometry("420x500")
        self.resizable(False, False)

        # Saat ve tarih
        self.saat_label = ctk.CTkLabel(self, text="", font=("Segoe UI", 30, "bold"))
        self.saat_label.pack(pady=(25, 8))

        self.tarih_label = ctk.CTkLabel(self, text="", font=("Segoe UI", 16))
        self.tarih_label.pack(pady=(0, 20))

        # Şehir girişi
        self.sehir_frame = ctk.CTkFrame(self)
        self.sehir_frame.pack(pady=(10, 20), padx=20, fill="x")

        self.sehir_entry = ctk.CTkEntry(self.sehir_frame, placeholder_text="Türkiye'deki bir şehir giriniz...", font=("Segoe UI", 14))
        self.sehir_entry.pack(side="left", padx=(10, 5), expand=True, fill="x")

        self.getir_button = ctk.CTkButton(self.sehir_frame, text="Göster", width=70, command=self.getir)
        self.getir_button.pack(side="right", padx=(5, 10))

        # Hava bilgisi paneli
        self.hava_frame = ctk.CTkFrame(self, corner_radius=15)
        self.hava_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.sehir_label = ctk.CTkLabel(self.hava_frame, text="📍 İstanbul", font=("Segoe UI", 20, "bold"))
        self.sehir_label.pack(pady=(20, 10))

        self.sicaklik_label = ctk.CTkLabel(self.hava_frame, text="🌡️ - °C", font=("Segoe UI", 18))
        self.sicaklik_label.pack(pady=5)

        self.durum_label = ctk.CTkLabel(self.hava_frame, text="☁️ -", font=("Segoe UI", 16))
        self.durum_label.pack(pady=5)

        self.detay_label = ctk.CTkLabel(self.hava_frame, text="💧 Nem: -  |  💨 Rüzgar: -", font=("Segoe UI", 14))
        self.detay_label.pack(pady=10)

        self.hata_label = ctk.CTkLabel(self.hava_frame, text="", text_color="red", font=("Segoe UI", 13))
        self.hata_label.pack(pady=(5, 0))

        # ✨ Sağ altta imza
        self.imza_label = ctk.CTkLabel(self, text="Powered by Ferit Oflaz", text_color="#777", font=("Segoe UI", 12, "italic"))
        self.imza_label.pack(side="bottom", pady=5, anchor="se")

        # Saat güncelleme
        self.guncelle_saat()

        # İlk açılışta otomatik İstanbul verisini göster
        self.getir("İstanbul")

    def guncelle_saat(self):
        simdi = datetime.datetime.now()
        aylar = {
            "January": "Ocak", "February": "Şubat", "March": "Mart", "April": "Nisan",
            "May": "Mayıs", "June": "Haziran", "July": "Temmuz", "August": "Ağustos",
            "September": "Eylül", "October": "Ekim", "November": "Kasım", "December": "Aralık"
        }
        gunler = {
            "Monday": "Pazartesi", "Tuesday": "Salı", "Wednesday": "Çarşamba",
            "Thursday": "Perşembe", "Friday": "Cuma", "Saturday": "Cumartesi", "Sunday": "Pazar"
        }

        gun_adi = gunler[simdi.strftime("%A")]
        ay_adi = aylar[simdi.strftime("%B")]
        tarih = f"{gun_adi}, {simdi.day} {ay_adi} {simdi.year}"

        self.saat_label.configure(text=simdi.strftime("%H:%M:%S"))
        self.tarih_label.configure(text=tarih)
        self.after(1000, self.guncelle_saat)

    def getir(self, sehir=None):
        if sehir is None:
            sehir = self.sehir_entry.get().strip().capitalize()

        if not sehir:
            self.hata_label.configure(text="Lütfen bir şehir adı girin.")
            return

        url = f"https://wttr.in/{sehir}?format=j1"

        try:
            res = requests.get(url)
            data = res.json()

            if "current_condition" not in data:
                self.hata_label.configure(text=f"Şehir bulunamadı: {sehir}")
                return

            self.hata_label.configure(text="")
            hava = data["current_condition"][0]
            temp = hava["temp_C"]
            durum_ing = hava["weatherDesc"][0]["value"]
            nem = hava["humidity"]
            ruzgar = hava["windspeedKmph"]

            durum_map = {
                "Sunny": "Güneşli",
                "Partly cloudy": "Parçalı bulutlu",
                "Cloudy": "Bulutlu",
                "Overcast": "Kapalı",
                "Mist": "Sisli",
                "Patchy rain possible": "Yer yer yağmurlu",
                "Light rain": "Hafif yağmurlu",
                "Moderate rain": "Yağmurlu",
                "Heavy rain": "Şiddetli yağmurlu",
                "Snow": "Karlı",
                "Clear": "Açık",
            }
            durum = durum_map.get(durum_ing, durum_ing)

            self.sehir_label.configure(text=f"📍 {sehir}")
            self.sicaklik_label.configure(text=f"🌡️ {temp}°C")
            self.durum_label.configure(text=f"☁️ {durum}")
            self.detay_label.configure(text=f"💧 Nem: %{nem}  |  💨 Rüzgar: {ruzgar} km/s")

        except Exception as e:
            self.hata_label.configure(text=f"Hata oluştu: {e}")

if __name__ == "__main__":
    app = HavaPanosu()
    app.mainloop()
