import socket
import sys
import random
import threading
from scapy.all import *

def detectPortStatus(csock, address):
    destIP = input("Enter the IP of destination: ")
    destPort= input("Enter the Port Number of the destination: ")

    try:
        csock.send(f"detect_Port_Status$Job creator wants${destIP}*{destPort}".encode())
        data = csock.recv(1024).decode()
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


def newClient(csock, address):
    jobList = ["check_If_Online", "detect_Port_Status"]
    rand = random.randint(0,1)
    #rand = 1
    numOfNodes = ""
    if rand <= 1:
        numOfNodes = "1 person"
    else:
        numOfNodes = "more than 1 person"
    csock.send(f"The job is {jobList[rand]} created for {numOfNodes}. Accept?(Y/N)".encode())
    choice = csock.recv(1024).decode()
    if choice == "Y":
        if (rand == 0):
            checkIfOnline(csock, address)
        if (rand == 1):
            detectPortStatus(csock, address)
    else:
        print("Job refused by seeker")
        csock.close()
        """
            if not data:
                conn.close()
                mySocket.close()

            if data == "refuse":
                print("Job refused by seeker")
                conn.close()
                mySocket.close()
            else:
                print("Data returned from seeker: " + str(data))
                conn.close()
                mySocket.close()
        """

    """    
    csock.send("Hello Client!!!!".encode())
    data = csock.recv(1024).decode()
    print(f"{address} sent: {data}")
       # msg=input("Send a message to the client")
        #csock.send(msg.encode())
    """
    csock.close()
    print("Looking for seekers...")
def Main():
    host = "127.0.0.1"
    #port = int(sys.argv[1])

    port= 5000
    while True:
        mySocket = socket.socket()
        mySocket.bind((host, port))

        # while True:
        mySocket.listen(0)
        #conn, addr = mySocket.accept()
        print("Looking for seekers...")
        while True:

            conn, addr = mySocket.accept()
            print("Connection from seeker: " + str(addr))
            cThread = threading.Thread(target=newClient, args=(conn,addr,))
            cThread.start()
    mySocket.close()


if __name__ == '__main__':
    Main()
