from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

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
        
        service = Service("C:/Users/ATS/Desktop/Muhasebe oto giriş/chrome.exe")  # ChromeDriver yolunu burada belirtin
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

        # Siteye giriş
        driver.get("https://dijital.gib.gov.tr/portal/login")
        
        try:
            # Kullanıcı adı ve şifreyi girmek
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username"))).send_keys(username)
            driver.find_element(By.ID, "password").send_keys(password)
            
            # Giriş butonuna tıklama
            driver.find_element(By.ID, "loginButton").click()
        
        except Exception as e:
            print("Giriş sırasında hata:", e)
        finally:
            driver.quit()

# Basit bir kullanıcı arayüzü
root = tk.Tk()
root.title("Oto Login Aracı")

# Excel'den yükleme butonu
load_button = tk.Button(root, text="Excel'den Yükle", command=load_credentials)
load_button.pack(pady=5)

# Giriş bilgilerini seçmek için dropdown menü
dropdown_label = tk.Label(root, text="Kullanıcı Seç:")
dropdown_label.pack(pady=5)
dropdown = ttk.Combobox(root)
dropdown.pack(pady=5)

# Giriş butonu
login_button = tk.Button(root, text="Giriş Yap", command=auto_login)
login_button.pack(pady=10)

root.mainloop()
