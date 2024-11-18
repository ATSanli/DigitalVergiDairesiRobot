from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from ttkthemes import ThemedTk

loaded_label = None
credentials_list = []
driver = None  # Store driver globally to access it across functions

# Load credentials function
def load_credentials():
    global credentials_list, loaded_label
    try:
        df = pd.read_excel("sifreler.xlsx", usecols=["isim", "kullanıcı adı", "şifre"])
        credentials_list = df.to_dict('records')
        update_dropdown()
        if credentials_list:
            dropdown.set(credentials_list[0]['isim'])

        if not loaded_label:
            loaded_label = ttk.Label(root, text="'sifreler' isimli Excel başarıyla yüklendi...", background="#2e2e2e", foreground="orange", font=("Arial", 10))
            loaded_label.grid(row=3, column=1, sticky="e", padx=10, pady=5)

    except FileNotFoundError:
        messagebox.showerror("Excel Yükleme Hatası", "sifreler Excel dosyası bulunamadı.")

# Update dropdown menu
def update_dropdown():
    credential_names = [item['isim'] for item in credentials_list]
    dropdown['values'] = credential_names

# Auto-login function
def auto_login():
    global driver
    selected_name = dropdown.get()
    selected_cred = next((item for item in credentials_list if item['isim'] == selected_name), None)
    
    if selected_cred:
        username = selected_cred['kullanıcı adı']
        password = selected_cred['şifre']
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        
        driver.get("https://dijital.gib.gov.tr/portal/login")
        
        try:
            # Step 1: Log in with credentials
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='userid']"))
            ).send_keys(username)
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']"))
            ).send_keys(password)
            
            messagebox.showinfo("Başarılı", "Giriş yapıldı. Şimdi 'Borcu Yoktur Yazısı Al' butonuna tıklayın.")

        except Exception as e:
            messagebox.showerror("Hata", f"Giriş sırasında hata oluştu: {e}")

# Run "Borcu Yoktur Yazısı Al" steps after login
def run_borcu_yoktur_steps():
    global driver
    if driver:
        try:
            # Step 2: Close the tour modal
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".reactour__close-button"))
            ).click()

            # Step 3: Click "İnternet Vergi Dairesi" button and confirm
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#internetVergiDairesi"))
            ).click()
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "button[title='ONAYLA']"))
            ).click()

            # Switch to the new tab
            WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)
            driver.switch_to.window(driver.window_handles[1])  # Switch to the new tab

            # Step 4: Click "Borcu yoktur / Mükellefiyet Yazısı"
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Borcu yoktur / Mükellefiyet Yazısı')]"))
            ).click()

            # Step 6: Click on the tab button panel and then the nested item
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "span.csc-tab-buton-panel-btn"))
            ).click()

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#H9c90a361ab086-5746832e911746"))
            ).click()



        except Exception as e:
            messagebox.showerror("Hata", f"İşlem sırasında hata oluştu: {e}")
        finally:
            driver.quit()  # Close driver after the steps are completed
            driver = None  # Reset driver to prevent re-use


# Setting up the UI
root = ThemedTk(theme="equilux")
root.title("SENBAY IT AUTO LOGIN TOOL - By ATŞ")
root.configure(bg="#2e2e2e")

style = ttk.Style()
style.configure('TButton', background="#1c1c1c", foreground="white", font=("Times 22", 12))
style.map('TButton', background=[('active', '#7c7c7c')])

img = Image.open("senbay.png").resize((600, 300), Image.Resampling.LANCZOS)
photo = ImageTk.PhotoImage(img)
image_label = ttk.Label(root, image=photo, background="#2e2e2e")
image_label.grid(row=0, column=0, columnspan=2, pady=0)

load_button = ttk.Button(root, text="Şirketler yüklenmediyse dosya seç", command=load_credentials)
load_button.grid(row=1, column=1, padx=10, pady=5, sticky="we")

dropdown_label = ttk.Label(root, text="Excel yükle:", background="#2e2e2e", foreground="white", font=("Times 22", 12))
dropdown_label.grid(row=1, column=0, sticky="e", padx=10, pady=5)

dropdown_label = ttk.Label(root, text="Şirket Seç:", background="#2e2e2e", foreground="white", font=("Times 22", 12))
dropdown_label.grid(row=2, column=0, sticky="e", padx=10, pady=5)

root.grid_columnconfigure(1, weight=1)

dropdown = ttk.Combobox(root)
dropdown.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

login_button = ttk.Button(root, text="Dijital Vergi Dairesi Giriş", command=auto_login)
login_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

# Adding "Borcu Yoktur Yazısı Al" button
borcu_yoktur_button = ttk.Button(root, text="Borcu Yoktur Yazısı Al", command=run_borcu_yoktur_steps)
borcu_yoktur_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

# Load initial credentials if available
load_credentials()

root.mainloop()