# TryHackMe — Pre Security Learning Path

**Status:** ✅ Completed — 24th August 2026
**Duration:** 19 hours 10 minutes
**Type:** Learning path (foundational theory + practical rooms)

## Overview

The Pre Security path is TryHackMe's entry point into cyber security, aimed at building the foundational knowledge needed before tackling offensive/defensive security properly. It's split into cyber security fundamentals, networking, web, and both major operating systems (Linux and Windows). This writeup summarises the key concepts from each section rather than walking through a single machine, since the path is theory + guided practicals rather than one CTF box.

---

## 1. Introduction to Cyber Security

- Covered the difference between **offensive security** (red team — attacking systems to find weaknesses) and **defensive security** (blue team — detecting, responding to, and preventing attacks).
- Learned the basic structure of the security industry: pentesting, SOC analysis, threat intelligence, digital forensics, and governance/compliance roles.
- Got introduced to the **CIA triad** (Confidentiality, Integrity, Availability) as the core model for thinking about what security is actually protecting.

## 2. Network Fundamentals

- This overlaps with notes already written up separately in `networking.md` — OSI model, TCP vs UDP, subnetting, common ports, DNS.
- New from this path specifically: how data physically/logically moves across a network (switches vs routers), MAC vs IP addressing, and basic packet structure.
- Reinforced why understanding networking is a prerequisite for basically everything else in security — you can't attack or defend what you don't understand the plumbing of.

## 3. How the Web Works

- HTTP request/response cycle: methods (GET, POST, PUT, DELETE), status codes (2xx/3xx/4xx/5xx), headers, and cookies.
- Client-server model, and how a browser turns a URL into a rendered page (DNS lookup → TCP handshake → HTTP request → response → render).
- Basics of HTML/CSS/JS from a security-relevant angle — enough to recognise how a page is structured, not full web dev.
- Introduced to browser dev tools (Inspect Element / Network tab) as a way to see requests/responses directly, which is the starting point for a lot of web app testing later on.

## 4. Linux Fundamentals

- Filesystem hierarchy (`/etc`, `/var`, `/home`, `/bin`, etc.) and what lives where.
- Core commands: `ls`, `cd`, `pwd`, `cat`, `grep`, `find`, `chmod`, `chown`, `ps`, `top`, `man`.
- File permissions model (`rwx` for owner/group/other) and how to read/change them with `chmod`.
- Package management basics (`apt`) and process management.
- This directly reinforced stuff I'd already been doing hands-on in the home lab (Kali laptop, Debian server), so it was more consolidation than brand new material.

## 5. Windows Fundamentals

- Windows filesystem structure and the registry as the equivalent of Linux's config files.
- User accounts and permissions model (Administrator vs standard user, UAC).
- Basic use of the command line (`cmd`) and PowerShell for navigation and simple tasks.
- Windows-specific concepts that come up a lot in security contexts: services, Task Manager/Event Viewer, and how Windows handles processes differently from Linux.

---

## Key Takeaways

- This path is intentionally broad rather than deep — the goal is having *just enough* context in networking, web, Linux, and Windows to not be lost when starting Security+ theory or the first real CTF rooms.
- Confirmed a lot of what I already knew from the home lab and Kenobi, which was reassuring — the hands-on approach is clearly sticking.
- Biggest gap filled was **Windows fundamentals** — most of my practical time so far has been Linux-heavy (Kali, Debian server), so having a baseline on the Windows side matters for when Windows-based rooms/CTFs show up.

## Next Steps

- Move into the next stage of the roadmap: Security+ (SY0-701) theory alongside continuing CTF rooms.
- Apply Windows fundamentals in a practical room soon to cement it (rather than just reading).
