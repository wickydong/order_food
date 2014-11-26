#!/bin/bash
# delete any existing chains
/sbin/iptables -F INPUT
/sbin/iptables -F FORWARD
/sbin/iptables -F OUTPUT
/sbin/iptables -Z INPUT
/sbin/iptables -Z FORWARD
/sbin/iptables -Z OUTPUT

# setting up default policies
/sbin/iptables -P INPUT DROP
/sbin/iptables -P FORWARD DROP
/sbin/iptables -P OUTPUT ACCEPT

# trust port for eth0,may closed
#for PORT in 80; do
#        /sbin/iptables -A INPUT -i eth0 -p tcp --dport $PORT -j ACCEPT
#done


for i in 53 
do
       iptables -I INPUT -p udp --sport $i -j ACCEPT
done

for i in 25 80 587 3306 
do
	iptables -I INPUT -p tcp --sport $i -j ACCEPT
done



# enable local traffic
/sbin/iptables -A INPUT -i eth1 -j ACCEPT
/sbin/iptables -A INPUT -i eth2 -j ACCEPT
/sbin/iptables -A INPUT -i lo -j ACCEPT

# allow ping for check net status
/sbin/iptables -A OUTPUT -p icmp -j ACCEPT
/sbin/iptables -A INPUT -p icmp -j ACCEPT

# trust IP for eth0
/sbin/iptables -A INPUT -i eth0 -p 41 -j ACCEPT
/sbin/iptables -A INPUT -i eth0 -p 89 -j ACCEPT
/sbin/iptables -A INPUT -i eth0 -p tcp --dport 53 -j ACCEPT
/sbin/iptables -A INPUT -i eth0 -p udp --dport 53 -j ACCEPT
/sbin/iptables -A INPUT -i eth0 -p tcp --dport 6010 -s 60.212.40.45 -j ACCEPT
/sbin/iptables -A INPUT -i eth0 -p tcp --dport 6010 -s 122.5.32.226 -j ACCEPT
