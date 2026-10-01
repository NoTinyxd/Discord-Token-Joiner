from datetime import datetime
from colorama import Fore, Style

def timestamp():
    return f"{Fore.LIGHTBLACK_EX}[{datetime.now().strftime('%H:%M:%S')}]"

def success(message):
    print(f"{timestamp()} - {Fore.GREEN}(+){Style.RESET_ALL} {message}")

def error(message):
    print(f"{timestamp()} - {Fore.RED}(-){Style.RESET_ALL} {message}")

def warning(message):
    print(f"{timestamp()} - {Fore.YELLOW}(!){Style.RESET_ALL} {message}")

def info(message):
    print(f"{timestamp()} - {Fore.CYAN}(*){Style.RESET_ALL} {message}") #from my previous repos ik
def inputt(message):
    return input(f"{timestamp()} - {Fore.CYAN}(*){Style.RESET_ALL} {message}")