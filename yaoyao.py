#! /usr/bin/env python3

from ww import Key, Host, Link
import os

inwall_server_ip = "47.94.166.125"
outwall_server_ip = "104.238.129.4"
client_num=16
client_name=lambda i:"dev{}".format(i+1)
pref = "./data"

def yaoyao():
    os.system("mkdir -p {}".format(pref))
    Key().dump(os.path.join(pref,"bj.key"))
    Key().dump(os.path.join(pref,"lax.key"))
    for i in range(client_num):
        Key().dump(os.path.join(pref,client_name(i)+'.key'))

    lax_key = Key(key_path=os.path.join(pref,"lax.key"))
    bj_key = Key(key_path=os.path.join(pref,"bj.key"))
    dev_keys = []
    for i in range(client_num):
        cur_key=Key(key_path=os.path.join(pref,client_name(i)+'.key'))
        dev_keys.append(cur_key)

    bj = Host("bj", inwall_server_ip, "10.56.100.1", "10.56.233.1", home="/root", key=bj_key)
    lax = Host("lax", outwall_server_ip, "10.56.100.4", "10.56.233.4",home="/root", key=lax_key)
    
    devs = []
    for i in range(client_num):
        cur_dev = Host(client_name(i),None,None,None,key=dev_keys[i])
        devs.append(cur_dev)

    lax_bj = Link(lax, bj, mtu=1360)

    dev_bjs = []
    for i in range(client_num):
        cur_bj = Link(devs[i],bj,mtu=1360)
        dev_bjs.append(cur_bj)

    bj.add_route(["10.56.100.0/24", "10.56.200.0/24", "10.56.233.0/24", "10.56.40.0/24", "1.1.1.1",], via=bj.lo_ns_ip, in_ns=False)
    bj.add_route([inwall_server_ip, outwall_server_ip], via="10.233.233.1", in_ns=True)
    bj.add_route([lax.lo_ip, lax.lo_ns_ip, "1.1.1.1"], link=lax_bj, in_ns=True)

    bj.add_ipset("https://pppublic.oss-cn-beijing.aliyuncs.com/ipsets.txt", in_ns=True)
    bj.add_iptable("mangle", "PREROUTING", "-s 10.56.0.0/16 -m set ! --match-set china_ip dst -m set ! --match-set private_ip dst -j MARK --set-xmark 0x1/0xffffffff", in_ns=True)
    bj.add_cmd(bj.ns_exec + "ip rule add fwmark 0x1 table 100")
    bj.add_cmd(bj.ns_exec + "ip route add default via %s table 100" % lax_bj.left_ip)


    lax.add_route(["10.56.100.0/24", "10.56.200.0/24", "10.56.233.0/24", "10.56.40.0/24"], via=lax.lo_ns_ip, in_ns=False)
    lax.add_route([bj.lo_ip, bj.lo_ns_ip], link=lax_bj, in_ns=True)
    dev_bj_lefts = [t.left_ip for t in dev_bjs]
    lax.add_route(dev_bj_lefts, link=lax_bj, in_ns=True)


    for i in range(client_num):
        dev = devs[i]
        dev.save_cmds_as_bash(os.path.join(pref,client_name(i)+'.sh'))
    bj.save_cmds_as_bash(os.path.join(pref,"bj.sh"))
    lax.save_cmds_as_bash(os.path.join(pref,"lax.sh"))

    for dev in devs:
        dev.save_configs_as_config(os.path.join(pref,"{}.conf".format(dev.hostname)))

if __name__ == "__main__":
    yaoyao()
