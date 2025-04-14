# Chocolate

Plataforma: Dockerlabs
OS: Linux
Level: Easy
Status: Done
Complete: Yes
EJPT: yes
Created time: 5 de diciembre de 2024 21:03

Reconeixement

```bash
sudo nmap -p- --open -sS --min-rate 5000 -vvv  -n 172.17.0.2 -oG allports
```

![image.png](<imagenes/image 81.png>)

Mirem codi font i apareix;

![image.png](<imagenes/image 82.png>)

Entrem a :

[http://172.17.0.2/nibbleblog/](http://172.17.0.2/nibbleblog/)

![image.png](<imagenes/image 83.png>)

Trobem panell d'autenticació:

![image.png](<imagenes/image 84.png>)

Credencials per defecte : admin/admin
Trobem versió :

![image.png](<imagenes/image 85.png>)

Busquem exploit
Provem a metasploit

![image.png](<imagenes/image 86.png>)

Configurem parametres:

Usuari: admin
Pass: admin
RHOST: 172.17.0.2

Falla
Veiem que al scrip utilitza la ruta del Plugin "My_image"
Instale el plugin a la web
executem exploit

Entrem i tractem tty:

![image.png](<imagenes/image 87.png>)

Som usuari www-data

```bash
sudo -l :
```

![image.png](<imagenes/image 88.png>)

L'usuari "chocolate" pot utilitzar php

Busquem a GTOBins i torbem:

![image.png](<imagenes/image 89.png>)

Per poder fer-ho amb l'usuari chocolate i que no demani password:

![image.png](<imagenes/image 90.png>)

Som usuari chocolate

Veiem amb ps -faux que corre un script php com a root

![image.png](<imagenes/image 91.png>)

/opt/script.php

Modifiquem el fitxer :

echo '<?php exec("chmod u+s /bin/bash"); ?>' > /opt/script.php

Comprovem que ha canviat la bash :

![image.png](<imagenes/image 92.png>)

amb el permis sudoer

![image.png](<imagenes/image 93.png>)

Ja amb la bash modificada fem

bash -p
root

![image.png](<imagenes/image 94.png>)