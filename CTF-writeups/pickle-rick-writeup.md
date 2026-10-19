# TryHackMe: Pickle Rick

**Difficulty:** Easy
**Category:** Web exploitation, command injection, privilege escalation
**Platform:** TryHackMe

## Overview

Pickle Rick is a beginner-friendly, *Rick and Morty*-themed room that centres on web enumeration and web-based exploitation. The scenario: Rick has turned himself into a pickle and needs three secret ingredients to turn back into a human. Each ingredient is a "flag" hidden somewhere on the target machine, and finding all three means working through a realistic chain — enumerate the web app, recover credentials that were left exposed, abuse a command-injection flaw in a login-protected panel, and finally escalate to `root` through a `sudo` misconfiguration.

It's a great room for practising the core web-assessment workflow end to end, and for seeing how a few small, individually "minor" mistakes (a comment here, a `robots.txt` entry there, an over-permissive `sudo` rule) chain together into full system compromise.

> Note: the target IP is shown as `MACHINE_IP` throughout, since TryHackMe assigns a fresh address each session.

---

## 1. Reconnaissance & enumeration

### Port scan

I started with an `nmap` scan to map the attack surface and identify running services:

```bash
nmap -sS -sC -sV MACHINE_IP
```

- `-sS` — stealth (SYN) scan
- `-sC` — run the default NSE script set for extra detail
- `-sV` — probe service/version information

The scan revealed two open ports:

| Port | Service | Notes |
|------|---------|-------|
| 22/tcp | SSH | Remote login — no credentials yet |
| 80/tcp | HTTP | Web server — the obvious starting point |

With only SSH and a web server exposed, and no credentials in hand, the web application on port 80 was clearly the intended way in. SSH is noted for later in case I recover a username/password pair that also works there.

### Inspecting the web application

Browsing to `http://MACHINE_IP/` loaded a themed landing page. Before touching any tooling, I did the simplest and most commonly overlooked step first — **reading the page source** (`Ctrl+U` / "View Source"). Developers frequently leave comments, notes, and debug artefacts in HTML that never render in the browser but are trivially visible in the source.

That paid off immediately: a username had been left behind in an HTML comment.

```
Username: R1ckRul3s
```

> Lesson: always view source before reaching for heavier tools. Credentials, hidden endpoints, and developer notes hide in plain sight.

### Checking `robots.txt`

Next I checked `robots.txt`, a standard file that tells search-engine crawlers which paths to avoid. Because it often *reveals* sensitive paths rather than hiding them, it's always worth a look:

```
http://MACHINE_IP/robots.txt
```

Instead of directory rules, the file contained a single suspicious string:

```
Wubbalubbadubdub
```

At this stage I didn't know what it unlocked, but a lone, unusual string sitting in `robots.txt` is a strong candidate for a password. I noted it alongside the username `R1ckRul3s`.

### Directory brute-forcing

To find endpoints not linked from the homepage, I ran directory enumeration with `dirb` against the default wordlist:

```bash
dirb http://MACHINE_IP/
```

This surfaced several paths, including:

- `/assets` — static content (CSS, images, JS); checked but held nothing useful
- `portal.php` — a login page
- `login.php`, `denied.php`, `index.html`, `robots.txt`

The key discovery was **`portal.php`**, the application's login portal — exactly what I'd want given I now had a candidate username and password.

---

## 2. Gaining access

Using the credentials recovered during enumeration:

- **Username:** `R1ckRul3s`
- **Password:** `Wubbalubbadubdub`

I logged in at `portal.php`, and authentication succeeded.

This is a textbook example of why **exposed credentials** are so dangerous: neither value required any cracking or brute-forcing. The username was sitting in an HTML comment and the password in a world-readable `robots.txt` — the "attack" was simply reading two files.

---

## 3. Exploitation — command injection

After logging in, I landed on a **command panel** — a web form that executes commands on the server and prints the output back to the page. A feature like this, if it passes user input to the operating system without sanitisation, is vulnerable to **command injection**, letting an attacker run arbitrary OS commands in the context of the web-server user.

I confirmed code execution by listing the current directory:

```bash
ls
```

Output:

```
Sup3rS3cretPickl3Ingred.txt
assets
clue.txt
denied.php
index.html
login.php
portal.php
robots.txt
```

Two files stood out: `Sup3rS3cretPickl3Ingred.txt` (almost certainly the first ingredient) and `clue.txt`.

### Ingredient 1 — working around a command filter

I tried to read the first ingredient file with `cat`:

```bash
cat Sup3rS3cretPickl3Ingred.txt
```

But the application had blacklisted `cat`, returning:

```
Command disabled to make it hard for future PICKLEEEE RICCCKKKK.
```

This is a classic — and weak — defensive measure: blacklisting a single command. The problem with blacklists is that there are almost always equivalent commands that achieve the same result. Linux offers plenty of ways to read a file without `cat`, for example:

- `less <file>`
- `more <file>`
- `head <file>` / `tail <file>`
- `strings <file>`
- `nl <file>`
- `grep . <file>`

I used `less`:

```bash
less Sup3rS3cretPickl3Ingred.txt
```

Which revealed the **first ingredient**:

```
mr. meeseek hair
```

> Lesson: blacklisting commands (or characters) is not a real control. Filtering `cat` while leaving `less`, `more`, `head`, and others available stops nobody. Proper mitigation is to never pass user input to a shell at all.

---

## 4. Privilege escalation

With reliable command execution as the web-server user, the next goal was to see how far those privileges could be pushed. The single most valuable check in Linux privilege escalation is to list what the current user is allowed to run via `sudo`:

```bash
sudo -l
```

Output:

```
Matching Defaults entries for www-data on MACHINE_HOST:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin

User www-data may run the following commands on MACHINE_HOST:
    (ALL) NOPASSWD: ALL
```

This is the jackpot. The `www-data` account — the low-privileged user the web server runs as — is permitted to run **any command as any user, with no password** (`(ALL) NOPASSWD: ALL`). In other words, I had effectively unrestricted `root` access through `sudo`, without needing a single credential.

### Ingredient 2 — the `rick` home directory

I began exploring the filesystem with elevated privileges:

```bash
sudo ls /
sudo ls /home
```

`/home` contained two user directories: `rick` and `ubuntu`. Given the theme, `rick` was the obvious place to look:

```bash
sudo ls -la /home/rick
```

Inside was a file named `second ingredients`. Because the filename contains a space, I wrapped it in quotes so the shell treated it as a single argument rather than two:

```bash
sudo less "/home/rick/second ingredients"
```

This revealed the **second ingredient**:

```
1 jerry tear
```

### Ingredient 3 — the `root` directory

Finally, I looked in the one place that normally requires `root` to read — `/root` — using the same `sudo` access:

```bash
sudo ls -la /root
sudo less /root/3rd.txt
```

Which revealed the **third and final ingredient**:

```
3rd ingredients: fleeb juice
```

All three ingredients recovered — room complete.

---

## Ingredients recovered

| # | Ingredient | Location | How it was read |
|---|------------|----------|-----------------|
| 1 | `mr. meeseek hair` | `Sup3rS3cretPickl3Ingred.txt` (web root) | `less` (bypassing the `cat` blacklist) |
| 2 | `1 jerry tear` | `/home/rick/second ingredients` | `sudo less` (quoted path) |
| 3 | `fleeb juice` | `/root/3rd.txt` | `sudo less` |

---

## Attack chain summary

```
Nmap (ports 22, 80)
      │
      ▼
Web enumeration ──> username in page source (R1ckRul3s)
      │            └> password in robots.txt (Wubbalubbadubdub)
      ▼
dirb ──> portal.php (login)
      │
      ▼
Authenticated command panel ──> command injection (RCE as www-data)
      │
      ▼
sudo -l ──> (ALL) NOPASSWD: ALL ──> full root access
      │
      ▼
Three ingredients recovered (web root, /home/rick, /root)
```

---

## Security findings & remediation

### 1. Hardcoded / exposed credentials

**Description:** The username was embedded in the page's HTML source and the password was stored in `robots.txt` — both readable by anyone, with no authentication required.

**Impact:**
- Valid credentials can be obtained trivially, with no brute-forcing.
- Unauthorised users gain direct access to the authenticated portion of the application.

**Remediation:**
- Never place credentials in source code, HTML comments, or public files.
- Treat `robots.txt` as public — never use it to store anything sensitive.
- Enforce strong, unique passwords and a proper authentication mechanism.
- Review code and web roots for leaked secrets before deployment.

### 2. OS command injection

**Description:** The authenticated command panel passed user-supplied input to the operating system and executed it without validation, allowing arbitrary commands to run on the server.

**Impact:**
- Arbitrary command execution in the context of the web-server user.
- Sensitive files can be read or modified.
- Combined with the `sudo` misconfiguration below, it leads directly to full server compromise.

**Remediation:**
- Never pass user input to a system shell. Avoid functions like `system()`, `exec()`, `shell_exec()`, and `passthru()` with user data.
- Where OS interaction is unavoidable, use parameterised APIs and strict input **allow-lists** (not blacklists).
- Blacklisting individual commands (e.g. blocking `cat`) is ineffective — it was bypassed with `less`.

### 3. Over-permissive `sudo` configuration

**Description:** The `www-data` user was granted `(ALL) NOPASSWD: ALL`, allowing it to run any command as `root` without a password.

**Impact:**
- Any code execution as `www-data` (such as the command injection above) escalates instantly to full `root`.
- There is no meaningful privilege boundary between the web application and the operating system.

**Remediation:**
- Apply the principle of least privilege. A web-server account should almost never have `sudo` rights.
- If specific elevated actions are genuinely required, grant only those exact commands, never `ALL`.
- Avoid `NOPASSWD` wherever possible and audit `/etc/sudoers` (and `sudoers.d`) regularly.

---

## Lessons learned

- **Enumerate thoroughly before exploiting.** Everything needed to get in was found by reading the page source and `robots.txt` — no exploitation required.
- **View source first.** The cheapest recon step routinely yields usernames, endpoints, and developer notes.
- **Blacklists are not security.** Blocking `cat` is trivially bypassed with `less`/`more`/`head`/`strings`. Allow-lists and avoiding shell calls entirely are the real fix.
- **`sudo -l` is the first privilege-escalation check.** One command exposed a path straight to `root`.
- **Vulnerabilities chain.** Exposed creds + command injection + a weak `sudo` rule combined into full compromise, even though each issue alone looks small.
- **Mind the shell.** Quoting the `second ingredients` path was necessary because of the space in the filename — a small but important detail when scripting or passing arguments.

## Conclusion

Pickle Rick is a fun, approachable room that walks through a complete web-exploitation chain: enumeration, credential recovery, authenticated command injection for remote code execution, and privilege escalation via a `sudo` misconfiguration. Using `nmap` and `dirb` alongside manual inspection of the source and `robots.txt`, I recovered all three secret ingredients and effectively achieved full control of the host. It's an excellent reinforcement of the fundamental lesson that strong security depends on getting the basics right at every layer — not on hiding a single file or blacklisting a single command.
