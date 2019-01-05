echo "Kuruluma hoþ geldiniz lütfen bekleyiniz..."

cp istemci.service /etc/systemd/system/istemci.service

chmod +x istemci.py

cp istemci.py /root/istemci.py

cp istemci.inf /root/istemci.inf

systemctl enable istemci.service

echo "Kurulum tamamlanmýþtýr..."

systemctl daemon-reload

systemctl start istemci.service