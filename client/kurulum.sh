echo "Kuruluma ho� geldiniz l�tfen bekleyiniz..."

cp istemci.service /etc/systemd/system/istemci.service

chmod +x istemci.py

cp istemci.py /root/istemci.py

cp istemci.inf /root/istemci.inf

systemctl enable istemci.service

echo "Kurulum tamamlanm��t�r..."

systemctl daemon-reload

systemctl start istemci.service