# 😈 Network Demon

A themed, terminal-based launcher that wraps common Linux network-security and
penetration-testing tools behind a single menu-driven interface. It does **not**
reimplement any attack — it detects whether the real tool is installed, collects
the parameters, and shells out to the genuine utility (`nmap`, `aircrack-ng`,
`bettercap`, `tshark`, `hydra`, `metasploit`, …). Menus that can't be fully
automated (Evil Twin, Rogue DHCP, persistence, etc.) print step-by-step guides
instead.

It's a single self-contained Python script (`NETWORK_DEMON.py`) with a
horror/"demon" aesthetic: animated fire banner, ASCII devils, typewriter text,
and an idle "the demon grows impatient…" nagger.

---

## A note on the theme

The demonic and horror styling of this project is purely an aesthetic choice —
a bit of hacker-culture flavour in the tradition of similarly themed security
tools. It does not reflect my personal beliefs or values, and it is not
intended to endorse, glorify, or promote anything sadistic, occult, or harmful.
No offence is meant to anyone who comes across the project. If the theme isn't
to your taste, the styling is cosmetic only and does not affect how the tool
functions.

---

## ⚠️ Legal & ethical use

This program drives tools that can attack networks, capture traffic, crack
Wi-Fi, and exploit hosts.

**Only use it against systems you own or have explicit, written permission to
test.** Unauthorized scanning, deauthing, credential brute-forcing, traffic
interception, or exploitation is illegal in most jurisdictions. You are solely
responsible for how you use it. Use it for authorized penetration tests, lab
environments, CTFs, and learning — nothing else.

---

## Requirements

- **Linux** (relies on `/sys/class/net`, `hostname -I`, `ip`, `ps`, and the
  `timeout` coreutil). Not for Windows/macOS.
- **Python 3.6+** — standard library only, no `pip install` needed.
- A terminal that supports ANSI colors and the Unicode glyphs used in the UI
  (`⛧`, box-drawing). Most modern terminals are fine.
- The actual security tools you intend to launch (all optional — the script
  checks for each one and tells you the install command if it's missing).

> Many actions need **root** (packet capture, `nmap -O`, monitor-mode Wi-Fi
> attacks, clearing `/var/log/auth.log`). Run with `sudo` when a tool requires
> it. The script itself does not require root to start.

### Installing the wrapped tools (Debian/Kali/Ubuntu)

Use the built-in **Tool Checker** (main menu → `10`) to see what's present and
get the exact `apt` command for anything missing. Common ones:

```bash
sudo apt install nmap aircrack-ng reaver bettercap wifite \
                 tshark tcpdump hydra exploitdb metasploit-framework \
                 dsniff bluez macchanger dnsutils whois iw wireless-tools
```

---

## Running

```bash
python3 NETWORK_DEMON.py
```

You'll get the animated banner, then a "ritual login" that asks your name and
whether you're *"ready to dance with the devil?"* — answer `yes` to reach the
main menu (answering anything else triggers a dramatic fiery exit).

---

## Menu map

```
RED TEAM
  1  Network Attacks ─ ARP Poisoning · DNS Spoofing · MITM (bettercap) ·
                       Rogue DHCP (guide) · Traffic Analyser (tshark)
  2  Wireless Hacking ─ WiFi Scanner · Deauth · WPA Handshake Capture ·
                        Evil Twin (guide) · WPS (reaver) · Bluetooth ·
                        Wifite · Bettercap
  3  Device Discovery ─ OS Fingerprinting · Service Enumeration ·
                        Vulnerability Scan · Default-Creds reference
  4  Router Attacks ─ Login Brute Forcer (hydra) · WPS · Router Vuln Scan ·
                      Default Credential Checker
  5  Traffic Analysis ─ Packet Capture · Live Monitor · HTTP Inspector ·
                        DNS Query Monitor
  6  Exploitation ─ Metasploit · Searchsploit · CVE Lookup ·
                    Reverse Shell Generator · Msfvenom Payload
  7  Post Exploitation ─ PrivEsc (linpeas) · Cover Tracks · Persistence ·
                         Lateral Movement · Data Exfiltration guides

TOOLS
  8  Notes          Save / view / delete personal notes
  9  VPN Checker    Shows public IP + detects VPN processes / tunnel interfaces
  10 Tool Checker   Reports which wrapped tools are installed
  11 Exit
```

### Where things are stored

| File | Purpose |
|------|---------|
| `~/.networkdemon_notes.txt` | Saved notes (`title\|note` per line) |
| `~/.networkdemon_log.txt`   | Timestamped log of every tool launched |
| `~/demon_capture_<ts>.pcap` | Packet-capture output (you're asked keep/delete) |

---

## How the tools are wired

Every launcher follows the same safe pattern:

1. Log the action to `~/.networkdemon_log.txt`.
2. Check the real binary exists with `shutil.which(...)`; if not, print the
   `apt` install hint and bail.
3. Prompt for required parameters and refuse to run on missing input.
4. Shell out via `subprocess.run([...], check=False)` with the correct flags.

Verified invocations (syntax matches each tool's real CLI):
`arpspoof -i -t <gw>`, `aireplay-ng --deauth 0 -a <bssid> [ -c <client> ]`,
`airodump-ng [ -c ] [ --bssid ] -w -`, `reaver -i -b -vv`,
`iwlist <if> scan`, `nmap -O/-sV/--script vuln/http-*`,
`tshark -i [ -f ] [ -Y ]`, `tcpdump -i -w`, `hydra -l -P <target> http-get /`,
`msfvenom -p <payload> LHOST= LPORT= -f -o`, `msfconsole`, `searchsploit <term>`.

---

## Known caveats (by design, not bugs)

- **Router brute-force / default-cred check (Hydra)** use Hydra's `http-get`
  module, which only tests HTTP Basic/Digest auth pop-ups. Most consumer routers
  use a **form-based** web login, which this will *not* detect even with the
  correct password. The script warns you about this at runtime; for form logins
  use Hydra's `http-post-form` with that router's exact field names.
- **CVE Lookup** queries NIST's official **NVD 2.0** API
  (`services.nvd.nist.gov`). It needs internet access and is rate-limited
  (~5 requests / 30s without an API key), so rapid repeat lookups may briefly
  fail; it degrades to a clear message rather than crashing.
- **Cover Tracks** only truncates the bash-history *file*; a still-running shell
  keeps its history in memory and can rewrite the file on exit (the script notes
  this). Clearing `/var/log/auth.log` needs root.
- Wi-Fi attacks (deauth, WPA capture, WPS) require an adapter in **monitor
  mode** and usually **root**.

---

## Changelog (debug pass)

Fixes applied while reviewing the code:

- **Checker output no longer vanishes.** VPN Checker and Tool Checker (and in
  fact every menu) printed their results and then immediately redrew the menu,
  scrolling the output off-screen — this was the "they don't really work"
  symptom. Added a `pause()` ("Press Enter to continue") so results stay on
  screen until acknowledged; wired into every submenu loop and after the two
  one-shot checkers.
- **Fixed wrong-note deletion.** `delete_note()` read the notes file without
  filtering blank lines while `view_notes()` filtered them, so the displayed
  number could map to the wrong entry. Both now filter identically.
- **WPA Handshake Capture** no longer passes empty `-c ""` / `--bssid ""` to
  `airodump-ng` when those fields are left blank.
- Added an `if __name__ == "__main__":` guard plus a clean **Ctrl+C** handler
  (previously it dumped a traceback and left the idle-timer thread alive).
- Removed an unused loop variable.

Second pass (hardening before release):

- **CVE Lookup** moved off CIRCL's deprecated endpoint to the official NVD 2.0
  API, with proper parsing of description, published date, and CVSS score
  (v3.1/v3.0/v2 fallback). Verified against live data.
- **Router Default Credential Checker** now detects a hit from Hydra's actual
  credential-report line (`host: … login: … password: …`) instead of a loose
  substring match that produced false positives.
- **Idle messages** no longer orphan your input line — the prompt is redrawn
  after the nag (via a small `demon_input()` helper that also de-duplicates the
  timer bookkeeping).
- Added an MIT `LICENSE`.

The script compiles cleanly (`python3 -m py_compile`) with no linter
diagnostics, and the logic fixes were unit-verified.
