# GoodGames

Plataforma: HackTheBox
OS: Linux
Level: Easy
Status: Not started
Complete: No
Created time: 23 de enero de 2025 20:22

## Recopilación de información

<aside>
💡 Reconocimiento general

</aside>

Whichsystem

```bash
whichSystem.py 10.10.11.130

	10.10.11.130 (ttl -> 63): 
```

### **Escaneo de puertos**

Comenzamos con un escaneo para identificar que puertos están abiertos.

---

```bash
sudo nmap -p- --open -T5 -sS --min-rate 5000 -n -Pn -vvv 10.10.11.130 -oG targeted

PORT   STATE SERVICE REASON
80/tcp open  http    syn-ack ttl 63
```

### **Enumeración de servicios**

Una vez listado los puertos accesibles, procederemos a realizar la enumeración de servicios para su posterior identificación de vulnerabilidades.

---

```bash
sudo nmap -sCV -p80 10.10.11.130 -oN targeted

ORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.51
|_http-title: GoodGames | Community and Store
|_http-server-header: Werkzeug/2.0.2 Python/3.9.2
Service Info: Host: goodgames.htb
```

- **Identificación de vulnerabilidades**
    - 80/tcp open  http    Apache httpd 2.4.51

Whatweb

```bash
whatweb 10.10.11.130
http://10.10.11.130 [200 OK] Bootstrap, Country[RESERVED][ZZ], Frame, HTML5, HTTPServer[Werkzeug/2.0.2 Python/3.9.2], IP[10.10.11.130], JQuery, Meta-Author[_nK], PasswordField[password], Python[3.9.2], Script, Title[GoodGames | Community and Store], Werkzeug[2.0.2], X-UA-Compatible[IE=edge]

```

- **Enumación web**
    
    ```bash
    ❯ gobuster dir -u http://goodgames.htb -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt --exclude-length 9265
    ```
    
    ![image.png](<imagenes/image 109.png>)
    

Buscamos subdominios

```bash
❯ ffuf -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-110000.txt -t 50 -u http://goodgames.htb -H "HOST:FUZZ.goodgames.htb" -fs 85107
```

## Explotación

<aside>
💡 Probamos diferentes accesos

</aside>

### Explotación 1

```bash

```

### Explotación 2

```bash

```

### Explotación posterior

<aside>
💡 Accedemos con las credenciales encontradas

</aside>

### Escalada de privilegios

```bash
 
```

## Conclusión

<aside>
💡 En esta sección, debes proporcionar un resumen de la máquina para cuando tengas que volver a ella, puedas saber conocer de forma rápida de que se trataba

</aside>