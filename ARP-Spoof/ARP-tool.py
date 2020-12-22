import Detect
import Spoof

def printLogo():
    print("""                                                                                               
           _____  _____     _______ ____   ____  _      
     /\   |  __ \|  __ \   |__   __/ __ \ / __ \| |     
    /  \  | |__) | |__) |_____| | | |  | | |  | | |     
   / /\ \ |  _  /|  ___/______| | | |  | | |  | | |     
  / ____ \| | \ \| |          | | | |__| | |__| | |____ 
 /_/    \_\_|  \_\_|          |_|  \____/ \____/|______|
                                                        
                                                        
                """)

def printMenu():
    print("""******************* MENU *******************

    -    1. Spoof ARP
    -    2. Detect ARP Spoof


********************************************  """)

def Main():
    printLogo()
    printMenu()
    choice = input("Choose : ")
    print(choice)
    if choice == "1" :
        Spoof.Main()
    else:
        Detect.Main()
if __name__ == '__main__':
    Main()

