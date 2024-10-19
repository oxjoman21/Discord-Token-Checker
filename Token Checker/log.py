import time
import sys 
from colorama import Fore 


class Log:

    def fatal(self,message):
        print(f"{Fore.RED}[X]{Fore.RESET} [{message}]")
        time.sleep(5)
        sys.exit()

    def suc(self,message):
        print(f"{Fore.GREEN}[✓]{Fore.RESET} [{message}]")

    def inf(self,message):
        print(f"{Fore.BLUE}[I]{Fore.RESET} [{message}]")

    def error(self,message):
        print(f"{Fore.LIGHTRED_EX}[E]{Fore.RESET} [{message}]")

    
