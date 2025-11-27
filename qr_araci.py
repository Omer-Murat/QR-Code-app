import customtkinter as ctk
import qrcode
import cv2
import os
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox
import uuid # Rastgele dosya adı oluşturmak için eklendi

# Sistem renk modunu ve varsayılan temayı ayarla
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class QRCodeApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("QR Kod Aracı")
        self.geometry("750x600") 
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 1. Ikonları Ayarla (Pencere ve Görev Çubuğu)
        # Ikonu PNG ve ICO kullanarak yüklemeyi deneriz.
        
        # İkon yüklemeden önce PNG görselini ImageTk için yükleyelim
        self.app_icon_photo = None
        try:
            icon_image_for_photo = Image.open("logo.png")
            self.app_icon_photo = ImageTk.PhotoImage(icon_image_for_photo)

            if self.app_icon_photo:
                self.iconphoto(True, self.app_icon_photo)

        except FileNotFoundError:
            print("Uyarı: 'logo.png' dosyası bulunamadı. Uygulama ve pencere ikonları yüklenemeyecek.")
            pass
        except Exception as e:
            print(f"Uyarı: İkon PNG yüklenirken hata oluştu: {e}")
            pass

        # ICO yüklemeyi dene (Windows Görev Çubuğu ve Pencere İkonu için birincil yöntemdir.)
        try:
            self.iconbitmap("logo.ico")
        except Exception:
            pass # ICO yoksa veya başarısız olursa, iconphoto devrede kalır.
            
        # --- Kenar Çubuğu Navigasyonu ---
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)
        
        # 2. Uygulama İçi Logo Yükleme ve Boyutlandırma
        self.logo_photo = None
        
        if self.app_icon_photo:
            try:
                logo_image = Image.open("logo.png")
                logo_image = logo_image.resize((75, 75), Image.LANCZOS)
                self.logo_photo = ImageTk.PhotoImage(logo_image)
            except Exception:
                pass
        
        self.navigation_frame_label = ctk.CTkLabel(self.navigation_frame,
                                                   text="",
                                                   image=self.logo_photo, 
                                                   compound="center", 
                                                   font=ctk.CTkFont(size=20, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.create_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10,
                                           text="QR Oluştur", fg_color="transparent", text_color=("gray10", "gray90"),
                                           hover_color=("gray70", "gray30"), anchor="w",
                                           command=self.select_create_frame)
        self.create_button.grid(row=1, column=0, sticky="ew", pady=(0,5))

        self.read_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10,
                                         text="QR Oku", fg_color="transparent", text_color=("gray10", "gray90"),
                                           hover_color=("gray70", "gray30"), anchor="w",
                                         command=self.select_read_frame)
        self.read_button.grid(row=2, column=0, sticky="ew", pady=(0,5))

        # Tema Seçim Menüsü
        self.appearance_mode_label = ctk.CTkLabel(self.navigation_frame, text="Tema:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.navigation_frame,
                                                               values=["System", "Light", "Dark"],
                                                               command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=10, sticky="ew")

        # --- Oluşturma Çerçevesi ---
        self.create_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.create_frame.grid_columnconfigure(0, weight=1)
        
        self.create_label = ctk.CTkLabel(self.create_frame, text="QR Kod Oluşturucu", font=ctk.CTkFont(size=24, weight="bold"))
        self.create_label.grid(row=0, column=0, pady=20, padx=20, sticky="n")

        self.data_entry_label = ctk.CTkLabel(self.create_frame, text="Metin veya URL Girin:")
        self.data_entry_label.grid(row=1, column=0, pady=(10,0), padx=20, sticky="w")
        self.data_entry = ctk.CTkEntry(self.create_frame, width=400, height=30, placeholder_text="Örn: Merhaba Dünya! veya https://example.com")
        self.data_entry.grid(row=2, column=0, pady=(5, 10), padx=20, sticky="ew")

        # Kullanıcıdan Dosya Adı Girişi Kaldırıldı, Kayıt Butonu Kullanılacak
        self.filename_entry_label = ctk.CTkLabel(self.create_frame, text="Kayıt konumu, QR kodu oluşturduktan sonra seçilecektir.", text_color=("gray50", "gray60"))
        self.filename_entry_label.grid(row=3, column=0, pady=(10, 20), padx=20, sticky="w")
        
        # Eski filename entry kaldırıldı

        self.generate_button = ctk.CTkButton(self.create_frame, text="QR Kodu Oluştur ve Kayıt Konumu Seç", command=self.generate_qr)
        self.generate_button.grid(row=5, column=0, pady=10, padx=20)
        
        self.qr_image_label = ctk.CTkLabel(self.create_frame, text="Oluşturulan kod buraya gelecek", width=200, height=200, 
                                            fg_color=("gray85", "gray25"))
        self.qr_image_label.grid(row=6, column=0, pady=20, padx=20)


        # --- Okuma Çerçevesi ---
        self.read_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.read_frame.grid_columnconfigure(0, weight=1)

        self.read_label = ctk.CTkLabel(self.read_frame, text="QR Kod Okuyucu", font=ctk.CTkFont(size=24, weight="bold"))
        self.read_label.grid(row=0, column=0, pady=20, padx=20, sticky="n")

        self.read_file_button = ctk.CTkButton(self.read_frame, text="QR Kodu Resim Dosyasından Oku", command=self.read_qr_from_file)
        self.read_file_button.grid(row=1, column=0, pady=10, padx=20)
        
        self.read_result_label = ctk.CTkLabel(self.read_frame, text="Okunan içerik ve dosya bilgisi burada görünecektir.", wraplength=400, justify="left",
                                               font=ctk.CTkFont(size=14))
        self.read_result_label.grid(row=2, column=0, pady=20, padx=20, sticky="ew")

        self.read_image_display = ctk.CTkLabel(self.read_frame, text="Okunacak resim önizlemesi", width=250, height=250,
                                                fg_color=("gray85", "gray25"))
        self.read_image_display.grid(row=3, column=0, pady=10, padx=20)


        # Varsayılan çerçeveyi seç
        self.select_create_frame()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def select_frame_by_name(self, name):
        self.create_frame.grid_forget()
        self.read_frame.grid_forget()
        
        if name == "create":
            self.create_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        elif name == "read":
            self.read_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        self.create_button.configure(fg_color=("gray75", "gray25") if name == "create" else "transparent")
        self.read_button.configure(fg_color=("gray75", "gray25") if name == "read" else "transparent")

    def select_create_frame(self):
        self.select_frame_by_name("create")

    def select_read_frame(self):
        self.select_frame_by_name("read")

    def generate_qr(self):
        data = self.data_entry.get()

        if not data:
            messagebox.showerror("Hata", "Lütfen QR koda dönüştürülecek bir metin veya URL girin.")
            return

        try:
            # 1. QR kodunu oluştur
            qr = qrcode.QRCode(
                version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
            qr.add_data(data)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            
            # YENİ: Rastgele dosya adı oluştur (Örn: QR_a1b2c3d4.png)
            random_filename = f"QR_{uuid.uuid4().hex[:8]}.png"

            # 2. Kullanıcının kayıt yerini seçmesini sağla (asksaveasfilename)
            filepath = filedialog.asksaveasfilename(
                defaultextension=".png", # Varsayılan uzantı
                filetypes=[("PNG dosyaları", "*.png")], # Dosya tipi filtresi
                initialfile=random_filename, # Rastgele oluşturulan dosya adı kullanılıyor
                title="QR Kodunu Kaydet"
            )

            # Kullanıcı iptal ederse, kaydetme işlemini durdur
            if not filepath:
                return
            
            # 3. QR kodunu seçilen yola kaydet
            img.save(filepath)
            
            messagebox.showinfo("Başarılı", f"QR kod başarıyla oluşturuldu ve '{os.path.basename(filepath)}' olarak kaydedildi.")
            
            # 4. Oluşturulan QR kodunu arayüzde göster
            qr_display_image = Image.open(filepath)
            qr_display_image = qr_display_image.resize((200, 200), Image.LANCZOS)
            qr_photo = ImageTk.PhotoImage(qr_display_image)
            self.qr_image_label.configure(image=qr_photo, text="")
            self.qr_image_label.image = qr_photo

        except Exception as e:
            messagebox.showerror("Hata", f"QR kodu oluşturulurken bir hata oluştu: {e}")

    def read_qr_from_file(self):
        file_path = filedialog.askopenfilename(
            title="QR Kodu İçeren Resim Dosyası Seçin",
            filetypes=[("Resim Dosyaları", "*.png *.jpg *.jpeg *.gif *.bmp")],
            initialdir=os.getcwd()
        )

        if not file_path:
            return

        try:
            img = cv2.imread(file_path)
            if img is None:
                messagebox.showerror("Hata", "Seçilen resim dosyası yüklenemedi.")
                return

            detektor = cv2.QRCodeDetector()
            data, bbox, straight_qrcode = detektor.detectAndDecode(img)

            if data:
                is_url = data.startswith(('http://', 'https://', 'www.'))
                tip = 'URL/Bağlantı' if is_url else 'Metin'
                result_text = f"Okunan Dosya: {os.path.basename(file_path)}\n" \
                              f"İçerik Tipi: **{tip}**\n" \
                              f"İçerik: {data}"
                self.read_result_label.configure(text=result_text)
                
                # Okunan resmi arayüzde göster
                display_image = Image.open(file_path)
                display_image = display_image.resize((250, 250), Image.LANCZOS)
                photo = ImageTk.PhotoImage(display_image)
                self.read_image_display.configure(image=photo, text="")
                self.read_image_display.image = photo

            else:
                self.read_result_label.configure(text="Görüntüde bir QR kod bulunamadı veya okunamadı.")
                self.read_image_display.configure(image=None, text="QR Kod Bulunamadı")

        except Exception as e:
            messagebox.showerror("Hata", f"QR kodu okunurken bir hata oluştu: {e}")
            self.read_result_label.configure(text=f"Okuma Hatası: {e}")
            self.read_image_display.configure(image=None, text="Hata")

if __name__ == "__main__":
    app = QRCodeApp()
    app.mainloop()