📸 Modern QR Kod Oluşturucu ve Okuyucu

Bu Python uygulaması, CustomTkinter kütüphanesi kullanılarak modern ve kullanıcı dostu bir grafik arayüz (GUI) ile geliştirilmiştir. Kullanıcıların metin veya URL'leri kolayca QR koda dönüştürmesine ve mevcut resim dosyalarındaki QR kodlarını 
okuyup çözümlemesine olanak tanır.

![Logo](logo.png)

Özellikler

Modern Arayüz: CustomTkinter ile koyu ve açık tema destekli profesyonel tasarım.

QR Oluşturma: Metin ve URL verilerini PNG formatında QR koda çevirir.

QR Okuma: Harici bir resim dosyasındaki QR kodunu okur ve içerdiği veriyi çözer (OpenCV kullanılarak).

Çapraz Platform: Python'ın desteklediği herhangi bir işletim sisteminde çalışabilir.

![Uygulama Görüntüsü](screenshot.png)

Kurulum

Projenin çalışması için gerekli kütüphaneleri kurmanız gerekmektedir:

pip install -r requirements.txt


Çalıştırma

Tüm bağımlılıklar yüklendikten sonra, uygulamayı aşağıdaki komutla başlatabilirsiniz:

python qr_app.py


EXE Olarak Derleme (Windows Görev Çubuğu İkonu için Önerilir)

Uygulamanın Windows'ta kendi ikonunuzla ve Python logosu olmadan görev çubuğunda görünmesi için PyInstaller ile derlenmesi önerilir.

PyInstaller'ı kurun:

pip install pyinstaller


Uygulamayı derleyin:

pyinstaller --noconsole --onefile --windowed --icon=logo.ico qr_app.py


Derlenen yürütülebilir dosya (qr_app.exe) projenizin dist klasöründe bulunacaktır.
