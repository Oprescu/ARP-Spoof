import socket
import os
from scapy.all import *

def jobHandler(jobType, jobDesc, jobData, socket):
    if jobType == "check_If_Online":
        print(jobData)
        icmp = IP(dst=jobData)/ICMP()
        resp = sr1(icmp,timeout=10)
        if resp != None:
            print("\nThe destination is online")
            socket.send("ONLINE".encode())
        else:
            print("\nThe destination is unreachable.")
            socket.send("OFFLINE".encode())
    elif jobType == "detect_Port_Status":
        ipAndPort=jobData.split("*")

        pac = sr1(IP(dst=ipAndPort[0])/TCP(dport=int(ipAndPort[1])), timeout=1)
        try:
            pac.show()
            print("The port is open")
            socket.send("PORT OPEN".encode())
        except:
            print("The port is closed")
            socket.send("PORT CLOSED".encode())

        #send(pac)


def Main():
    # add creator host IP's here
    host = ['127.0.0.1', '127.0.0.1']
    port = [5000, 5001]

    i = -1
    while True:
        i += 1
        if i == len(host):
            i = 0
        while True:
            try:
                #print("Asking " + host[i] + ":" + str(port[i]) + " for a job...")
                print("looking for " + host[i] + ":" + str(port[i]))
                mySocket = socket.socket()
                mySocket.connect((host[i], port[i]))
                break
            except:
                break
        data = ""
        mySocket.settimeout(1)
        try:
            data = mySocket.recv(1024).decode()
        except:
            pass
        if data == "":
            pass
        else:
            data = str(data)
            #print("Job found from creater : " + data)
            print("message recieved from creator" + data)
            status = input("Accept job? Y/N: ").upper()

            mySocket.send(status.encode())
            if (status == "Y"):
                mySocket.settimeout(30)
                #try:
                jobRECEIVE = mySocket.recv(1024).decode()
                jobSPLIT = jobRECEIVE.split("$")

                jobHandler(jobSPLIT[0], jobSPLIT[1], jobSPLIT[2], mySocket)
                #except:
                 #   print("Uh oh. The creator was too slow!")
           # data=mySocket.recv(1024).decode()
            #print(f"message is {data}")
            """
            if status == "Y":
                data = data.split(",")
                jobType = data[0]
                description = data[1]
                nrOfSeekers = data[2]
                jobInput = data[3]
                print(jobType)
                if jobType == "revStr":
                    jobInput = jobInput[::-1]
                    mySocket.send(jobInput.encode())
                    print("Job Complete")
                elif jobType == "Addition":
                    numbers = jobInput.split("+")
                    a = int(numbers[0])
                    b = int(numbers[1])
                    c = a + b
                    mySocket.send(str(c).encode())
                    print("Job Complete")
                elif jobType == "Subtraction":
                    numbers = jobInput.split("-")
                    a = int(numbers[0])
                    b = int(numbers[1])
                    c = a - b
                    mySocket.send(str(c).encode())
                    print("Job Complete")
                elif jobType == "Multiplication":
                    numbers = jobInput.split("x")
                    a = int(numbers[0])
                    b = int(numbers[1])
                    c = a * b
                    mySocket.send(str(c).encode())
                    print("Job Complete")
                elif jobType == "RPS":
                    mySocket.send(str(random.randint(1, 3)).encode())
                    print("Job Complete")

            
            else:
                mySocket.send("refuse".encode())
            """
        mySocket.close()


if __name__ == '__main__':
    Main()
