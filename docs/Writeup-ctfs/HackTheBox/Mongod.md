# Mongod

Plataforma: HackTheBox
OS: Linux
Level: Very Easy
Status: Done
Complete: Yes
Created time: 4 de enero de 2025 16:02
IP: 10.129.83.144

## Recopilación de información

<aside>
💡 Maquina very easy del Trier 0 de HTB

</aside>

### **Escaneo de puertos**

Comenzamos con un escaneo para identificar que puertos están abiertos.

---

```bash
sudo nmap -p- --open --min-rate 5000 -sS -n -Pn -www 10.129.83.144 -oG allports

PORT      STATE SERVICE REASON
22/tcp    open  ssh     syn-ack ttl 63
27017/tcp open  mongod  syn-ack ttl 63
```

![image.png](<imagenes/image 68.png>)

### **Enumeración de servicios**

Una vez listado los puertos accesibles, procederemos a realizar la enumeración de servicios para su posterior identificación de vulnerabilidades.

---

```bash
sudo nmap -sCV -p22,27017 10.129.83.144 -oN targeted

PORT      STATE SERVICE VERSION
22/tcp    open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.5 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 48:ad:d5:b8:3a:9f:bc:be:f7:e8:20:1e:f6:bf:de:ae (RSA)
|   256 b7:89:6c:0b:20:ed:49:b2:c1:86:7c:29:92:74:1c:1f (ECDSA)
|_  256 18:cd:9d:08:a6:21:a8:b8:b6:f7:9f:8d:40:51:54:fb (ED25519)
27017/tcp open  mongodb MongoDB 3.6.8 3.6.8
```

- **Identificación de vulnerabilidades**
    - 22/tcp    open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.5 (Ubuntu Linux; protocol 2.0)
    - 27017/tcp open  mongodb MongoDB 3.6.8 3.6.8

Vemos que con el script de nmap nos ha enumerado toda la BD de Mongo

```bash
db.flag.find().documents
db.coll.find().pretty()27017
```

Nos conectamos con

```bash
mongo 10.129.83.144:27010

test> show dbs
admin                  32.00 KiB
config                 72.00 KiB
local                  72.00 KiB
sensitive_information  32.00 KiB
users                  32.00 KiB
db> use admin
switched to db admin
admin> show collections
system.version
admin> use sensitive_information
switched to db sensitive_information
sensitive_information> show collections
flag
sensitive_information> db.flag.find()
[
  {
    _id: ObjectId("630e3dbcb82540ebbd1748c5"),
    flag: '1b6e6fb359e7c40241b6d431427ba6ea'
  }
]
sensitive_information> 

```

Flag: 1b6e6fb359e7c40241b6d431427ba6ea

## Explotación

<aside>
💡 No hay explotación

</aside>

## Conclusión

<aside>
💡 Maquina muy facil, sin explotación

</aside>