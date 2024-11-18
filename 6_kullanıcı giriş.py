import tkinter as tk
from tkinter import messagebox

# Kullanıcı giriş fonksiyonu
def login():
    username = entry_username.get()
    password = entry_password.get()
    remember = var_remember.get()
    
    # Basit kullanıcı doğrulama (örnek)
    if username == "admin" and password == "1234":
        messagebox.showinfo("Giriş Başarılı", "Hoş geldiniz!")
        # Kullanıcıyı hatırlama işlemi
        if remember:
            with open("user.txt", "w") as f:
                f.write(username)
    else:
        messagebox.showerror("Hata", "Kullanıcı adı veya şifre yanlış.")

# Tkinter penceresi
root = tk.Tk()
root.title("Kullanıcı Giriş")

# Kullanıcı adı etiketi ve giriş kutusu
label_username = tk.Label(root, text="Kullanıcı Adı:")
label_username.pack(pady=5)
entry_username = tk.Entry(root)
entry_username.pack(pady=5)

# Şifre etiketi ve giriş kutusu
label_password = tk.Label(root, text="Şifre:")
label_password.pack(pady=5)
entry_password = tk.Entry(root, show="*")
entry_password.pack(pady=5)

# Beni Hatırla seçeneği
var_remember = tk.BooleanVar()
checkbox_remember = tk.Checkbutton(root, text="Beni Hatırla", variable=var_remember)
checkbox_remember.pack(pady=5)

# Giriş butonu
button_login = tk.Button(root, text="Giriş", command=login)
button_login.pack(pady=20)

# Pencereyi çalıştır
root.mainloop()
