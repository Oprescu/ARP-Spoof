from scapy.all import *
import getmac

#This is a dictionary that saves validated hosts
known_hosts = {}

#Function that uses arp request to get the real MAC of an IP
def get_mac(ip):
    request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip)
    ans, unans = srp(request, timeout=1, verbose=False)
    for sent, received in ans:
        return received.hwsrc



def checkPacket(packet):
    global known_hosts
    #IF the packet is an ARP Reply and is not in the list of trusted hosts then verify it
    if packet.haslayer(ARP) and packet[ARP].op == 2 and known_hosts.get(packet[ARP].psrc) != packet[ARP].hwsrc:
        try:
            #This file says program output
            o = open("output.txt", "a")

            #Get the REAL mac of the suspected IP
            mac = get_mac(packet[ARP].psrc)
            
            #Check if the REAL mac matches the one sent in the ARP Reply
            if mac != packet[ARP].hwsrc and mac != None: 
                    print(f"*** Your ARP Table is being spoofed by: {packet[ARP].psrc}, with a spoofed MAC of: {packet[ARP].hwsrc} ***")
                    o.write("!!! Spoofed by " + packet[ARP].psrc + " with a spoofed mac of " + packet[ARP].hwsrc + "\n")
            else:
                #If they do match, we know the host can be trusted, and their IP + MAC combo is added to the list
                # of trusted hosts
                print(f"[-] Reply from : {packet[ARP].hwsrc} {packet[ARP].psrc}")
                o.write("[-] Reply from " + packet[ARP].psrc + " " + packet[ARP].hwsrc + "\n")
                print("[+] Host validated, adding to trusted list")
                o.write("[+] Host validated, adding to trusted list \n")
                known_hosts[packet[ARP].psrc] = packet[ARP].hwsrc

                #This file saves the found trusted hosts of every session
                f = open("trusted_hosts.ini", "w")
                f.write(str(known_hosts))
                f.close()
                o.close()
        except IndexError:
            pass


def Main():
    global known_hosts

    #Add the user to trusted hosts
    known_hosts[get_if_addr(conf.iface)]=getmac.get_mac_address()

    print("[.] Waiting for packets...")
    
    #Start sniffing
    sniff(store=False, prn=checkPacket)

if __name__ == '__main__':
    Main()