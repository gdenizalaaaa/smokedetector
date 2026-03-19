Elimde ekteki gibi bir kat planı var. Odalar ve odaların kapıları da numaralandırılmış isimlendirilmiş şekilde planda görüntülenebiliyor. Bir duman alarm uygulaması geliştirdim. Bu odaların her birinde birer duman dedektörü var. Herhangi bir odada dedektör aktif hale geldiğinde o odadan exit noktasına ulaşmak için kapıları kullanarak hangi odalardan geçilmesi gerektiğini bulmak istiyorum. Örneğin: 5 numaralı odada dedektör çalışırsa oda geçişleri 5-6-9-19-20-exit şeklinde olmalı. Kapı geçişleri k4-k6-k8-k19-k20 şeklinde olmalı. Bu veri ile iki çıktı üretmeni istiyorum. 1-Bana bu yolları bulabilmemi sağlayacak bir algoritma çıkar, python olsun. Eğer bir veri seti oluşturmak gerekiyorsa onu da bu plana göre oluştur. 2-Python görsel kütüphanesini kullanarak bu path'i çizdirmemi sağlayacak kodu ver. Görseli input olarak vererek üzerinde path olan görseli alabileyim.

venv\Scripts\Activate.ps1

kapsam dışı
1- kat planı girilen bir arayüz yok 
2- kat planı görseli ve kat planı oda-kapı eşleştirmeleri otomatik değil

dedektör
1- threshold geçince supabase'e kayıt gönder

supabase
1- tabloda device-room ilişkisini tutma -eksik
2- alarm kaydetme 
3- alarmın telegram ssubscriberlarına gönderilmesi
4- alarm olan device'ın odasını bulup python webservise gönderip       shortest path'i alma ve path çizimini alma - eksik
5- closed rooms'u gönderebilmek için alarm olan diğer deviceları dda webservise gönderebilmek - eksik
6- telegrama pythondan dönen response'u gönderme - eksik

python - eksik
1- oda-kapı eşleştirmelerine uygun bir isimlenirme şablonu ve bu şablona uygun isimlendirme yapılması (örnek: 1. odadan 2. odaya geçen ilk kapı için 1_2k1, ikinci kapı için 1_2k2 şeklinde) takibi kolaylaştırır
2- çizim yapılabilmessi için room coordları çıkaran kodun iyileştirilmesi lazım (createcoords.py) (burdaki oluşturulan coordlar drawingpath.py için gerekli)
3- room ve closed rooms ile istek yapılığında shortest path'in ve path çizilen dosyanın url'inin ya da base64 halinin supabase'e ya a istek yapılan yere gönderilmesi
