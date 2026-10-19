# TryHackMe: Hydra

**Difficulty:** Easy
**Category:** Password attacks, brute-forcing, web & SSH authentication
**Platform:** TryHackMe

## Overview

This room is a focused, practical introduction to **Hydra**, one of the most widely used network logon crackers in offensive security. The goal is to learn how Hydra automates online password guessing and then to use it against two different services — a **web login form** and **SSH** — to recover credentials for a user named `molly` and retrieve two flags.

Where an offline attack cracks captured hashes, Hydra performs an **online** attack: it talks to a live service and submits login attempts one after another at high speed, stopping as soon as a guess succeeds. That makes it the right tool when you have a reachable service, a known (or guessable) username, and a wordlist — but no password. It also makes the room a clean demonstration of why weak, common, and reused passwords are such a serious risk.

> Note: the target is shown as `MACHINE_IP` throughout, since TryHackMe assigns a fresh address each session.

---

## What is Hydra?

Hydra is a parallelised brute-forcing tool that automates password guessing against network services. Instead of a person typing passwords in by hand, Hydra takes a wordlist and throws it at the target as fast as the service (and your thread count) allows, reporting any valid credentials it finds.

It supports a broad range of protocols, including:

- **Remote access** — SSH, FTP, Telnet, RDP
- **Web application login forms** — via `http-get-form` / `http-post-form`
- **Mail services** — SMTP, IMAP, POP3
- **Databases** — MySQL, PostgreSQL, MSSQL, and others

The practical takeaway is a core security principle: an internet- or network-facing service that accepts weak, default, or common credentials can often be compromised in minutes. Strong, unique passwords, rate-limiting, and account lockouts are what defeat this class of attack.

---

## Hydra syntax essentials

A Hydra command changes slightly per protocol, but the building blocks are always the same:

| Component | Flag / position | Purpose |
|-----------|-----------------|---------|
| Target | `<ip>` / `<hostname>` | The host running the service |
| Username | `-l <user>` (single) or `-L <file>` (list) | The account to attack |
| Password list | `-P <wordlist>` | File of candidate passwords |
| Service | e.g. `ssh`, `ftp`, `http-post-form` | Protocol/module to attack |
| Threads | `-t <n>` | Parallel tasks — faster, but too many can break fragile services |
| Verbose | `-V` | Print every attempt (useful for confirming it's working) |

### Attacking SSH

```bash
hydra -l <username> -P <wordlist> <target_ip> ssh -t 4
```

- `-l <username>` — the single account to test
- `-P <wordlist>` — the password file
- `ssh` — the target protocol module
- `-t 4` — four parallel tasks (SSH can be sensitive to high thread counts, so a modest value is safer)

### Attacking a web login form (HTTP POST)

Web forms are more involved, because Hydra has to build the POST request itself and be told how to recognise a failed attempt:

```bash
hydra -l <username> -P <wordlist> <target_ip> http-post-form "<login_path>:<request_body>:<failure_string>"
```

- `http-post-form` — the attack module for form-based POST logins
- `<login_path>` — the path the form submits to (e.g. `/login`)
- `<request_body>` — the POST parameters, with `^USER^` and `^PASS^` as placeholders Hydra substitutes each attempt (e.g. `username=^USER^&password=^PASS^`)
- `<failure_string>` — text present in the response on a **failed** login. Hydra treats the absence of this string as success, so choosing it correctly is critical.

Finding the right parameter names and failure string means inspecting the login page first (view source / browser dev tools / intercepting the request in a proxy), rather than guessing.

---

## Challenge 1 — web form brute-force (flag 1)

The first task was to recover the web password for the user `molly`. I inspected the login page to confirm the form submitted a POST to `/login` with `username` and `password` fields, and that a failed attempt returned the string `incorrect`. With those three pieces, I built the command and used `rockyou.txt` as the wordlist:

```bash
hydra -l molly -P /usr/share/wordlists/rockyou.txt MACHINE_IP http-post-form "/login:username=^USER^&password=^PASS^:F=incorrect" -V
```

Breaking down the module string:
- `/login` — the form's submission path
- `username=^USER^&password=^PASS^` — the POST body, with Hydra filling in `molly` and each candidate password
- `F=incorrect` — the failure condition: any response containing `incorrect` is a failed login, so a response **without** it marks a hit

Hydra quickly recovered the password:

```
molly : sunshine
```

Logging into the web portal as `molly` / `sunshine` revealed the first flag:

- **Flag 1:** `THM{2673a7dd116de68e85c48ec0b1f2612e}`

---

## Challenge 2 — SSH brute-force (flag 2)

The second task was to find `molly`'s SSH password. SSH is simpler for Hydra than a web form — no module string to craft — so the command is compact:

```bash
hydra -l molly -P /usr/share/wordlists/rockyou.txt MACHINE_IP ssh -t 4
```

Hydra identified the credentials:

```
molly : butterfly
```

I then connected to the target over SSH with the recovered password:

```bash
ssh molly@MACHINE_IP
```

After authenticating as `molly` with `butterfly`, I had an interactive shell on the host. I located and read the `flag2` file to get the final flag:

```bash
cat flag2
```

- **Flag 2:** `THM{c8eeb0468febbadea859baeb33b2541b}`

---

## Results summary

| # | Service | Username | Password | Flag |
|---|---------|----------|----------|------|
| 1 | Web login form (`http-post-form`) | `molly` | `sunshine` | `THM{2673a7dd116de68e85c48ec0b1f2612e}` |
| 2 | SSH | `molly` | `butterfly` | `THM{c8eeb0468febbadea859baeb33b2541b}` |

Both passwords (`sunshine`, `butterfly`) are common dictionary words that appear in `rockyou.txt` — which is exactly why Hydra found them so quickly.

---

## Security findings & remediation

### 1. Weak, guessable passwords

**Description:** Both accounts used common single-word passwords present in the `rockyou.txt` wordlist, so an online dictionary attack succeeded almost immediately.

**Impact:**
- Credentials can be recovered in minutes with no prior access.
- The same weakness typically affects any other service the user can log into.

**Remediation:**
- Enforce strong password policies (length and complexity) and screen against known-breached/common-password lists.
- Encourage passphrases and a password manager so unique passwords are practical.

### 2. No brute-force protection on authentication

**Description:** The services accepted a high volume of rapid login attempts without throttling or locking out, allowing Hydra to run unimpeded.

**Impact:**
- Unlimited guesses make online brute-forcing viable.
- Attacks are faster and harder to notice when nothing slows them down.

**Remediation:**
- Implement rate-limiting and progressive delays on failed logins.
- Apply account lockout or temporary bans after repeated failures (e.g. Fail2ban for SSH).
- Add CAPTCHA or step-up challenges on web login forms after a few failed attempts.
- Monitor and alert on bursts of failed authentications.

### 3. Single-factor authentication

**Description:** Access to both the web portal and SSH depended on a password alone.

**Impact:**
- A single recovered password grants full access.
- There is no second barrier once the password is guessed.

**Remediation:**
- Enable multi-factor authentication (MFA) wherever possible.
- For SSH specifically, prefer **key-based authentication** and disable password logins (`PasswordAuthentication no`), which defeats online password brute-forcing outright.

---

## Lessons learned

- **Hydra is an online attack.** Its speed is bounded by the service and your thread count — not a weakness in cryptography, but in password choice and missing rate-limits.
- **The failure string is everything for `http-post-form`.** Pick the wrong `F=` value and Hydra reports either every attempt or none as a success. Inspect the real login response first.
- **Tune threads to the service.** `-t 4` is a sensible default for SSH; cranking threads too high can crash fragile services or trip defences, costing you the attack.
- **`rockyou.txt` is the go-to first wordlist** for CTF-style boxes — if a password is a common word, it's almost certainly in there.
- **Defence is about process, not just password strength.** Rate-limiting, lockouts, SSH keys, and MFA each break this attack even when a weak password slips through.

## Conclusion

The Hydra room is a clean, practical primer on online brute-forcing. Working through it, I used Hydra against two very different services — crafting an `http-post-form` module string to attack a web login, then running a straightforward SSH attack — to recover `molly`'s credentials and both flags. More importantly, it reinforces *why* the attack works: weak passwords combined with authentication endpoints that allow unlimited, unmonitored attempts. Fixing either side of that equation — stronger credentials, or rate-limiting/lockouts/MFA/SSH keys — is what shuts tools like Hydra down.
