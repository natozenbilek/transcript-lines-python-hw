# Introduction to Python, Ödev 4
# IEEE Hacettepe University Student Branch, Güz 2026
#
# Bu ödevin sonunda list ve tuple'larla veri tutabilecek, iki ismin aynı
# list'i gösterdiği durumu fark edebilecek, hatalı girdide yeniden
# sorabilecek ve kendi function'larınızla bir mesajı şifreleyip
# çözebileceksiniz.
#
# Son teslim: 15 Kasım 2026 Pazar 23.59
# Teslim formu: https://forms.gle/eMHjvPfSRP9cp1JH7
# Ödev reposu: https://github.com/natozenbilek/transcript-lines-python-hw
#
# Ödevi nasıl yapacaksınız
# 1. Bu dosyayı python-kurs klasörünüze kaydedin ve PyCharm'da açın.
# 2. Her görevde "# TODO" satırının yerine kodunuzu yazın.
# 3. Görev 5 ve 6'da test satırları comment olarak duruyor. Function'ı
#    yazdıktan sonra bu satırları seçin ve Ctrl+/ (macOS: Cmd+/) ile açın.
# 4. Dosyayı Run ile çalıştırın. Her görevin başlık satırından sonraki
#    çıktısı, o görevin "Beklenen çıktı" kısmıyla birebir aynı olmalı.
#    Görev 4 klavyeden puan soruyor: görevde yazan değerleri Run
#    penceresine yazıp Enter'a basın.
# 5. Bitince formda "İsim" alanına isminizi yazın, odev4.py'yi "Ödev
#    dosyası" alanına yükleyin ve "Kişisel verileriniz" sorusundaki onay
#    kutusunu işaretleyin. Söylemek istediğiniz bir şey varsa "Açıklama"
#    alanına yazabilirsiniz; bu alan isteğe bağlı.
#
# Dosya bu haliyle de hatasız çalışır. Görev başlıklarını ve Görev 3'te
# verilen kodun çıktısını yazar.
# Yalnızca Ders 1-4'te gördüğümüz yapıları kullanın.

# import satırları dosyanın en üstüne yazılır. Görev 5'in ve Meraklısına'nın
# import'larını buraya ekleyin.
# TODO


print("=== 1. Puan listesi ===")
scores = [70, 45, 85, 90, 30]
# a) 65 puanını append() ile ekleyin. Sonra list'i sort() ile sıralayıp
#    yazdırın.
# b) Sıralı list'in ilk ve son elemanı, en düşük ve en yüksek puandır.
#    İkisini index ile alıp bir f-string ile yazdırın.
# c) Ortalamayı sum() ve len() ile, iki basamakla yazdırın.
# d) Bir for ile 50 ve üstü kaç puan olduğunu sayın.
# TODO
#
# Beklenen çıktı:
# [30, 45, 65, 70, 85, 90]
# En düşük: 30, en yüksek: 90
# Ortalama: 64.17
# 50 ve üstü: 4


print("=== 2. Transkript satırları ===")
lines = ["MAT123;4;C1",
         "FIZ127;3;B2",
         "TKD103;2;A2"]
transcript = []
# Bu kez satırlarda boşluk yerine ; var.
# a) Her satırı split(";") ile parçalayın. Krediyi int() ile çevirin ve
#    (code, credits, letter) tuple'ını transcript'e append edin.
#    Sonra transcript'in ilk elemanını yazdırın.
# b) for code, credits, letter in transcript: ile her dersi bir f-string ile
#    yazdırın ve kredileri toplayın.
# TODO
#
# Beklenen çıktı:
# ('MAT123', 4, 'C1')
# MAT123: 4 kredi, C1
# FIZ127: 3 kredi, B2
# TKD103: 2 kredi, A2
# Toplam kredi: 9


print("=== 3. Haftalık ders listesi ===")
# Aşağıdaki kod gelecek haftanın listesini bu haftanınkinden kurmak istiyor,
# ama şu haliyle this_week de değişiyor. Önce çalıştırıp çıktıya bakın.
# a) Neden böyle olduğunu kodun altına bir comment ile yazın.
# b) Tek bir satırı değiştirerek next_week'i ayrı bir list yapın.
this_week = ["MAT123", "FIZ127"]
next_week = this_week  # TODO: bu satırı değiştirin
next_week.append("BBM101")
next_week.remove("MAT123")
print(this_week)
print(next_week)
print(this_week == next_week, this_week is next_week)
# TODO: açıklamanız
#
# Beklenen çıktı (düzeltince):
# ['MAT123', 'FIZ127']
# ['FIZ127', 'BBM101']
# False False


print("=== 4. Puanı yeniden sor ===")
# while True içinde "Puan (0-100): " diye bir tam sayı isteyin.
# - Tam sayı yazılmazsa (ValueError) "Tam sayı girin." yazıp yeniden sorun.
# - Sayı 0 ile 100 arasında değilse "0 ile 100 arasında olmalı." yazıp
#   yeniden sorun.
# - Geçerli bir puan gelince loop'tan break ile çıkın ve puanı yazdırın.
# try, except ValueError, continue ve break kullanın.
# Çalıştırınca şunları yazın: seksen, 120, 80
# TODO
#
# Beklenen çıktı:
# Puan (0-100): seksen
# Tam sayı girin.
# Puan (0-100): 120
# 0 ile 100 arasında olmalı.
# Puan (0-100): 80
# Puan: 80


print("=== 5. İlk function'lar ===")
# a) Dosyanın en üstüne import math ekleyin. hypotenuse(a, b) adlı bir
#    function yazın: dik kenarları a ve b olan dik üçgenin hipotenüsünü,
#    yani a * a + b * b'nin karekökünü math.sqrt() ile return etsin.
# b) has_passed(grade_point) adlı bir function yazın: katsayı en az 1.75
#    ise True, değilse False return etsin. İçinde print() olmasın.
# TODO
#
# Test satırları (function'ları yazınca açın):
# print(hypotenuse(3, 4))
# print(hypotenuse(5, 12))
# for gp in [3.25, 1.5]:
#     if has_passed(gp):
#         print(gp, "geçti")
#     else:
#         print(gp, "kaldı")
#
# Beklenen çıktı:
# 5.0
# 13.0
# 3.25 geçti
# 1.5 kaldı


print("=== 6. Sezar şifresi ===")
alphabet = "abcçdefgğhıijklmnoöprsştuüvyz"
# Sezar şifresinde her harf, alfabede birkaç harf ileri kaydırılır.
# a) position(letter) adlı bir function yazın: letter'ın alphabet'teki
#    index'ini return etsin. for ve range(len(alphabet)) ile index'leri
#    dolaşın; alphabet[i] == letter olunca i'yi return edin. Harf alphabet'te
#    yoksa loop biter; o zaman -1 return edin.
# b) caesar(text, shift) adlı bir function yazın. text'i de for ve
#    range(len(text)) ile dolaşın ve her text[i] için position()'ı çağırın:
#    - sonuç -1 ise karakteri olduğu gibi ekleyin;
#    - değilse (index + shift) % len(alphabet) index'indeki harfi ekleyin.
#      % sayesinde z'den sonra yeniden a gelir.
#    Kurduğunuz str'yi return edin.
# shift negatif de olabilir. Python'da (0 - 3) % 29, 26 verir; yani a'dan
# üç harf geri gidince v gelir. Bunun için ayrıca bir şey yazmanız gerekmez.
# TODO
#
# Test satırları (function'ları yazınca açın):
# print(position("a"), position("z"), position("?"))
# print(caesar("merhaba", 1))
# print(caesar("zor", 1))
# secret = "sgğal dlvltglplc, vğdtlnoğt"
# print(caesar(secret, -3))
#
# Beklenen çıktı:
# 0 28 -1
# nfsıbcb
# aös
# ödevi bitirdiniz, tebrikler


print("=== Meraklısına ===")
# Zorunlu değil.
# Dosyanın en üstüne import random ekleyin. counts = [0] * 7 ile başlayın.
# Bir zarı 600 kez random.randint(1, 6) ile atın ve gelen yüzün sayacını
# bir artırın: counts[die] += 1. Sonra toplam atışı ve hiç gelmeyen yüz olup
# olmadığını yazdırın. İsterseniz counts[1:]'i de yazdırın; o satır her
# çalıştırmada değişir.
# TODO
#
# Beklenen çıktı:
# Toplam atış: 600
# Hiç gelmeyen yüz var mı? False
