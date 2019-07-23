#! /bin/bash
sudo iptables -t nat -D PREROUTING -s 10.233.233.2/32 -p tcp -j REDIRECT --to-ports 3140
sudo iptables -t filter -D INPUT -i eth0 -p tcp -m tcp --dport 3140 -j DROP

sudo iptables -t nat -A PREROUTING -s 10.233.233.2/32 -p tcp -j REDIRECT --to-ports 3140
sudo iptables -t filter -A INPUT -i eth0 -p tcp -m tcp --dport 3140 -j DROP

ulimit -n 65535
./any_proxy -l=:3140
