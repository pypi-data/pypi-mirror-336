import requests
import time

ESP_IP = "192.168.1.50"  # ESP8266'nın IP adresi
URL = f"http://{ESP_IP}"  # Bağlantı adresi
DATA_FILE = "data.txt"  # Kaydedilecek dosya

def fetch_data():
    try:
        response = requests.get(URL, timeout=5)  # ESP8266'ya GET isteği gönder
        if response.status_code == 200:
            data = response.text.strip()  # Gelen veriyi al ve boşlukları temizle
            print("Data received:", data)
            
            with open(DATA_FILE, "a") as file:  # Veriyi dosyaya ekle
                file.write(data + "\n")
        else:
            print("❌ Connection failed:", response.status_code)
    except requests.exceptions.RequestException:
        print("❌ ESP8266 could not be reached !")


while True:
    fetch_data()  
    time.sleep(3) 
