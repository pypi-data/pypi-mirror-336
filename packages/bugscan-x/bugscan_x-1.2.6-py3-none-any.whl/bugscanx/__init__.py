import threading
from rich import print
from pyfiglet import Figlet

def import_modules():
    def task():
        try:
            from bugscanx.modules.scanners_pro import host_scanner_pro
            from bugscanx.modules.scrapers.subfinder import subfinder
        except Exception:
            pass
    
    threading.Thread(target=task, daemon=True).start()

figlet = Figlet(font="calvin_s")

def banner():
    print("""
    [bold red]╔╗[/bold red] [turquoise2]╦ ╦╔═╗╔═╗╔═╗╔═╗╔╗╔═╗ ╦[/turquoise2]
    [bold red]╠╩╗[/bold red][turquoise2]║ ║║ ╦╚═╗║  ╠═╣║║║╔╩╦╝[/turquoise2]
    [bold red]╚═╝[/bold red][turquoise2]╚═╝╚═╝╚═╝╚═╝╩ ╩╝╚╝╩ ╚═[/turquoise2]
     [bold magenta]Dᴇᴠᴇʟᴏᴘᴇʀ: Aʏᴀɴ Rᴀᴊᴘᴏᴏᴛ
      Tᴇʟᴇɢʀᴀᴍ: @BᴜɢSᴄᴀɴX[/bold magenta]
    """)

def text_ascii(text, color="white", indentation=2):
    ascii_banner = figlet.renderText(text)
    shifted_banner = "\n".join((" " * indentation) + line for line in ascii_banner.splitlines())
    print(f"[{color}]{shifted_banner}[/{color}]")
    print()

def clear_screen():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

import_modules()
