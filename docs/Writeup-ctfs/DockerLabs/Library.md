# Library

Plataforma: Dockerlabs
OS: Linux
Level: Easy
Status: Done
Complete: Yes
EJPT: yes
Created time: 5 de diciembre de 2024 21:23

## Reconeixement

### NMAP

```bash
sudo nmap -p- --open -sS --min-rate 5000 -vvv -Pn -n 172.17.0.2 -oG allports
```

![image.png](<imagenes/image 66.png>)

```bash
sudo nmap -p22,80 -sCV 172.17.0.2 -oN targeted
```

![image.png](<imagenes/image 67.png>)

Fem fuzzing a la web:

Trobem :

![image.png](<imagenes/image 68.png>)

Al codi font de Index.php : J***********D

Trobem

/javascrip/jquery/jquery/

Trobem un script que no sembla que serveixi per res

Provem força bruta amb el possible login de la web index.php

```bash
hydra -L /usr/share/wordlists/rockyou.txt -p J**********D 172.17.0.2 ssh -vV
```

User: c****s

![image.png](<imagenes/image 69.png>)

Conectem per ssh :

Usuari: c****s

Password: J**************D

![image.png](<imagenes/image 70.png>)

### Explotacio

```bash
sudo -l
```

![image.png](<imagenes/image 71.png>)

Veiem que crida al script :

/opt/script.py

[https://exploit-notes.hdks.org/exploit/linux/privilege-escalation/python-privilege-escalation/](https://exploit-notes.hdks.org/exploit/linux/privilege-escalation/python-privilege-escalation/)

Veiem que podem eliminar el script i crear un nou amb la ordre de cridar a una bash:

![image.png](<imagenes/image 72.png>)

Script original:

![image.png](<imagenes/image 73.png>)

creem el [script.py](http://script.py/)

![image.png](<imagenes/image 74.png>)

i executem el scrip amb sudo

![image.png](<imagenes/image 75.png>)