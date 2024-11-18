from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
from ttkthemes import ThemedTk  # ttk-themes kütüphanesi

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
            
            print("Tarayıcı açık kalacak. Lütfen giriş işlemini tamamlayın.")
            # Tarayıcıyı kapatma butonu
            confirmation_button = ttk.Button(root, text="Giriş İşlemini Tamamladım", command=lambda: driver.quit())
            confirmation_button.pack(pady=10)

        except Exception as e:
            print("Giriş sırasında hata:", e)

# Koyu temalı bir kullanıcı arayüzü
root = ThemedTk(theme="equilux")
root.title("SENBAY IT AUTO LOGIN TOOL - DijitalVergiDairesi - ATŞ")
root.geometry("600x550")

# Arkaplan rengini koyu yapma
root.configure(bg="#2e2e2e")  # Koyu gri arkaplan rengi

# ttk stil oluşturma
style = ttk.Style()
style.configure('TButton', background="#5c5c5c", foreground="white", font=("Arial", 12))
style.map('TButton', background=[('active', '#7c7c7c')])  # Butonlar aktifken daha açık renk

# Resmi yükle ve göster
img = Image.open("senbay.png")  # Resmin yolu
img = img.resize((600, 300), Image.Resampling.LANCZOS)
photo = ImageTk.PhotoImage(img)
image_label = ttk.Label(root, image=photo, background="#2e2e2e")
image_label.pack(pady=0)

# Excel'den yükleme butonu
load_button = ttk.Button(root, text="Excel'den Yükle", command=load_credentials)
load_button.pack(pady=5)

# Giriş bilgilerini seçmek için dropdown menü
dropdown_label = ttk.Label(root, text="Şirket Seç:", background="#2e2e2e", foreground="white", font=("Arial", 12))
dropdown_label.pack(pady=5)
dropdown = ttk.Combobox(root)
dropdown.pack(pady=5)

# Giriş butonu
login_button = ttk.Button(root, text="Giriş Yap", command=auto_login)
login_button.pack(pady=10)

root.mainloop()