from tkinter import *
import socket
from threading import Thread
import sys
from time import sleep
import configparser
from PIL import ImageTk,Image

global sock_liste
sock_liste = []

class Istemci():#Gelen bağlantıları sınıf olarak bir listeye atıyoruz
    def __init__(self,sock,ip):
        self.sock = sock
        self.ip = ip
def elemanlar():
    eleman = []
    for i in sock_liste:
        eleman.append(i.ip[0])
    return eleman

def IPal(parser):
    parser.read("sunucu.inf")
    return parser['IP']['ip']

def socket_olustur():##Socket oluşturmak için gerekli fonksiyon
    
    global s
    global PORT
    global HOST
    PORT = 5545
    parser = configparser.ConfigParser()
    HOST = IPal(parser) ##ayar dosyamızdan gerekli bağlnatıları alıyoruz
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)##socket nesnemizi oluşturuyoruz
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)##Socket kapanmasın diye gerekli ayarı yapıyoruz
    s.bind((HOST,PORT))##dinlemeye başlıyoruz
    s.listen(400)##max kullanıcı sayısını belirliyoruz
    while True:
        clis , addr = s.accept()
        a = elemanlar()
        print(a)
        print(addr[0])
        if addr[0] in a:
            msg = "Bu makine zaten bağlı... {}".format(addr)
            allentry.insert(END,msg)
            continue
        else:    ##Bağlantıları kabul ediyoruz
            sock_liste.append(Istemci(clis,addr))##gelen socket nesnelerini bir listeye atıyoruz 
            sr = "Bağlandı : ", addr ,"\n"##Ve bağlandıklarına dair mesajı ekrana basıyoruz
            allentry.insert(END,sr)
            continue

def listele():
    global sock_liste##Bağlantıları listelemek için bir fonksiyon
    if sock_liste == []:##Eğer boş ise gerekli mesajı yazıyoruz
        allentry.insert(END,"Henüz bağlantı kurulamadı...")
    for i,j in enumerate(sock_liste):#listede bulunan bağlı elemanları ekrana basıyoruz
        c = "Bağlandı {} : {} \n".format(i,j.ip)
        allentry.insert(END,c)

def yolla_tam():##Bütün kullanıcılara mesaj göndermek için fonksiyon
    global sock_liste
    if sock_liste == []:#Eğer boş ise hata almamak için ekrana mesaj basıyoruz
        allentry.insert(END,"Henüz bağlantı kurulamadı...\n")
    else:
        kom = sendal_ent.get(1.0,END)##Değilse gerekli text'den mesajı alıyor ve herkese iletiyoruz 
        if kom != None:
            if ('reboot' or 'poweroff' or 'init' )in kom:##Eğer sunucu kapatma girişiminde bulunursa geri bilgi almamak için
                kapat()
                sock_liste = []               
            elif "apt" in kom:
                for i in sock_liste:
                    try:
                        i.sock.send(kom.encode('utf-8'))
                    except Exception as e:
                        print(e)
                        allentry.insert(END,"Bağlantı kayboldu...\n")
                        del sock_liste[sock_liste.index(i)]
                        
            else:
                for i in sock_liste:
                    try:
                        i.sock.send(kom.encode('utf-8'))
                    except Exception as e:
                        print(e)
                        allentry.insert(END,"Bağlantı kayboldu...\n")
                    

def kapat():
    global sock_liste
    if sock_liste == []:
        allentry.insert(END,"Henüz bağlantı kurulamadı...\n")
    else:     
        for i in sock_liste:
            i.sock.close()
        sock_liste = []



def secGonder(sock,ip,num,com):##Özel olarak komut gönderme fonksiyonu
    while True:
        if ('reboot' or 'poweroff' or 'init') in com:##eğer sunucu bilgisayarı kapatmak istiyorsa veri yollanıyor ve listemizden socket nesnesi siliniyor
            sock.send(data)
            del sock_liste[num]
            break
        elif "apt" in com:
            try:
                sock.send(com.encode('utf-8'))##Eğer kurulum yapılmak isteniyorsa geri veri alınmıyor hata il karşılaşınca da listeden siliniyor
                cli_recv = sock.recv(1024).decode('ISO-8859-1')
                f = "{}> {}\n".format(ip[0],cli_recv)
                allentry.insert(END,f)
                break
            except:
                del sock_liste[num]
                break
        else:
            try:##eğer yukarıdaki gibi bir komut değilse de normal olarak komut gönderiliyor
                sock.send(com.encode("utf-8"))
                cli_recv = sock.recv(10024).decode('ISO-8859-1')
                f = "{}> {}\n".format(ip[0],cli_recv)
                allentry.insert(END,f)
                break
            except Exception as e:
                print(e)
                allentry.insert(END,"Bağlantı kayboldu..\n")##sorunlarla karşılaşınca da  bağlantı listeden siliniyor
                del sock_liste[num]
                break
   
def ana_menu():##ana_menu fonksiyonu
    data = send_ent.get(1.0,END)#veri alınıyor
    if "cikis" in data:##pencereyi kapatma
        pencere.destroy()

    elif  "liste" in data:##baplantıları listeleme
        listele()

    elif data[:6] == "selend":#bireysel komut gönderme örnek: selend@0@ls -l : 0.indisdeki bilgisayara ls -l komutunu gönder gibi
        data = data.split('@')     
        target = int(data[1])
        target_sock = sock_liste[target].sock
        target_ip = sock_liste[target].ip
        t3 = Thread(target = secGonder,args=(target_sock,target_ip,target,data[2]))
        t3.start()
    
        
    else:#hiç bir şey değilse uyarı mesajı gidiyor.
        allentry.insert(END,"Başka bir şey deneyin...\n")
    

            

##Window conf.
pencere= Tk()

pencere.resizable(width=False, height=False)

arka_res = ImageTk.PhotoImage(Image.open("arkapl.jpg"))

arka = Label(image=arka_res)

arka.pack()


gen = pencere.winfo_reqwidth()

yuk = pencere.winfo_reqheight()

sagPoz = int(pencere.winfo_screenwidth()/3 - gen/2)

solPoz = int(pencere.winfo_screenheight()/3 - yuk/2)

pencere.geometry("900x450+{}+{}".format(sagPoz, solPoz))

pencere.title("Sınıf Yönetim Yazılımı v0.1")



t = Thread(target=socket_olustur,args=())##dinlemeye başlıyoruz 
t.daemon = True
t.start()

##Butonlar oluşturluyor

sendall1 = Button(pencere,text="Toplu Yolla",bg="black",fg="white",width = 10,height=1,command=yolla_tam)
sendall1.configure(font=("Calibri", 12, "bold"))
sendall1.place(relx=0.65,rely=0.17)

toplu_kapa = Button(pencere,text="Toplu Kapa",bg="black",fg="white",width = 10,height=1,command=kapat)
toplu_kapa.configure(font=("Calibri", 12, "bold"))
toplu_kapa.place(relx=0.65,rely=0.35)

selend1 = Button(pencere,text="Seç ve yolla",bg="black",fg="white",width = 10,height=1,command=ana_menu)
selend1.configure(font=("Calibri", 12, "bold"))
selend1.place(relx=0.09,rely=0.66)


##Metin alanları oluşturuluyor
allentry = Text(pencere,bg="white",fg="black",width=50, height = 10)
allentry.configure(font=("Calibri", 12, "bold"))
allentry.place(relx=0.05,rely=0.12)

send_ent = Text(pencere,bg="white",fg="black",width=20,height=0.5)
send_ent.configure(font=("Calibri", 12, "bold"))
send_ent.place(relx=0.09,rely=0.75)

sendal_ent= Text(pencere,bg="white",fg="black",width=20,height=0.5)
sendal_ent.configure(font=("Calibri", 12, "bold"))
sendal_ent.place(relx=0.65,rely=0.27)

pencere.mainloop()




