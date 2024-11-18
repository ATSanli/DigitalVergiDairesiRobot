from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk

# Giriş bilgilerinin saklanacağı global liste
credentials_list = []

# Kullanıcı bilgilerini Excel'den yükleyen fonksiyon
def load_credentials():
    global credentials_list
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    if file_path:
        df = pd.read_excel(file_path, usecols=["isim", "kullanıcı adı", "şifre"])
        credentials_list = df.to_dict('records')
        update_dropdown()

# Dropdown menüyü güncelleyen fonksiyon
def update_dropdown():
    credential_names = [item['isim'] for item in credentials_list]
    dropdown['values'] = credential_names

# Otomatik giriş fonksiyonu
def auto_login():
    selected_name = dropdown.get()
    selected_cred = next((item for item in credentials_list if item['isim'] == selected_name), None)
    
    if selected_cred:
        username = selected_cred['kullanıcı adı']
        password = selected_cred['şifre']
        
        # Chrome seçenekleri ve driver başlatma
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        
        # Siteye giriş
        driver.get("https://dijital.gib.gov.tr/portal/login")
        
        try:
            # Kullanıcı adı alanını bekleme ve kullanıcı adını girme
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='userid']"))
            ).send_keys(username)
            
            # Şifre alanını bekleme ve şifreyi girme
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']"))
            ).send_keys(password)
            
            # Kullanıcı manuel olarak giriş yapabilmesi için bekle
            print("Tarayıcı açık kalacak. Lütfen giriş işlemini tamamlayın.")
            input("Devam etmek için Enter tuşuna basın...")  # Giriş işlemini tamamlamak için bekle
        
        except Exception as e:
            print("Giriş sırasında hata:", e)
            

         

# Basit bir kullanıcı arayüzü
root = tk.Tk()
root.title("SENBAY IT AUTO LOGIN TOOL - DijitalVergiDairesi - ATŞ")
root.geometry("600x500") 
root.configure(bg="#f0f0f0")  # Arka plan rengi

# Resmi yükle ve göster
img = Image.open("senbay.png")  # Resmin yolu
img = img.resize((600, 300), Image.Resampling.LANCZOS)
photo = ImageTk.PhotoImage(img)
image_label = tk.Label(root, image=photo, bg="#f0f0f0")  # Resim için bir label
image_label.pack(pady=10)

# Excel'den yükleme butonu
load_button = tk.Button(root, text="Excel'den Yükle", command=load_credentials, bg="#007BFF", fg="white", font=("Arial", 12))
load_button.pack(pady=5)

# Giriş bilgilerini seçmek için dropdown menü
dropdown_label = tk.Label(root, text="Kullanıcı Seç:", bg="#f0f0f0", font=("Arial", 12))
dropdown_label.pack(pady=5)
dropdown = ttk.Combobox(root)
dropdown.pack(pady=5)

# Giriş butonu
login_button = tk.Button(root, text="Giriş Yap", command=auto_login, bg="#28A745", fg="white", font=("Arial", 12))
login_button.pack(pady=10)

root.mainloop()


