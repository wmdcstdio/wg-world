#! /usr/bin/env python3

from ww import Key, Host, Link
import os

inwall_server_ip = "47.94.166.125"
outwall_server_ip = "149.28.60.68"
pref = "./data"

def yaoyao():
    os.system("mkdir -p {}".format(pref))
    Key().dump(os.path.join(pref,"bj.key"))
    Key().dump(os.path.join(pref,"lax.key"))
    Key().dump(os.path.join(pref,"dev1.key"))
    Key().dump(os.path.join(pref,"dev2.key"))
    Key().dump(os.path.join(pref,"dev3.key"))
    Key().dump(os.path.join(pref,"dev4.key"))
    Key().dump(os.path.join(pref,"dev5.key"))
    Key().dump(os.path.join(pref,"dev6.key"))
    Key().dump(os.path.join(pref,"dev7.key"))
    Key().dump(os.path.join(pref,"dev8.key"))

    lax_key = Key(key_path=os.path.join(pref,"lax.key"))
    bj_key = Key(key_path=os.path.join(pref,"bj.key"))
    dev1_key = Key(key_path=os.path.join(pref,"dev1.key"))
    dev2_key = Key(key_path=os.path.join(pref,"dev2.key"))
    dev3_key = Key(key_path=os.path.join(pref,"dev3.key"))
    dev4_key = Key(key_path=os.path.join(pref,"dev4.key"))
    dev5_key = Key(key_path=os.path.join(pref,"dev5.key"))
    dev6_key = Key(key_path=os.path.join(pref,"dev6.key"))
    dev7_key = Key(key_path=os.path.join(pref,"dev7.key"))
    dev8_key = Key(key_path=os.path.join(pref,"dev8.key"))

    bj = Host("bj", inwall_server_ip, "10.56.100.1", "10.56.233.1", home="/root", key=bj_key)
    lax = Host("lax", outwall_server_ip, "10.56.100.4", "10.56.233.4",home="/root", key=lax_key)

    dev1 = Host("dev1", None, None, None, key=dev1_key)
    dev2 = Host("dev2", None, None, None, key=dev2_key)
    dev3 = Host("dev3",None,None,None,key=dev3_key)
    dev4 = Host("dev4",None,None,None,key=dev4_key)
    dev5 = Host("dev5",None,None,None,key=dev5_key)
    dev6 = Host("dev6",None,None,None,key=dev6_key)
    dev7 = Host("dev7",None,None,None,key=dev7_key)
    dev8 = Host("dev8",None,None,None,key=dev8_key)
    devs = [dev1,dev2,dev3,dev4,dev5,dev6,dev7,dev8]

    lax_bj = Link(lax, bj, mtu=1360)

    dev1_bj = Link(dev1, bj, mtu=1360)
    dev2_bj = Link(dev2, bj, mtu=1360)
    dev3_bj = Link(dev3,bj,mtu=1360)
    dev4_bj = Link(dev4,bj,mtu=1360)
    dev5_bj = Link(dev5,bj,mtu=1360)
    dev6_bj = Link(dev6,bj,mtu=1360)
    dev7_bj = Link(dev7,bj,mtu=1360)
    dev8_bj = Link(dev8,bj,mtu=1360)

    bj.add_route(["10.56.100.0/24", "10.56.200.0/24", "10.56.233.0/24", "10.56.40.0/24", "1.1.1.1",], via=bj.lo_ns_ip, in_ns=False)
    bj.add_route([inwall_server_ip, outwall_server_ip], via="10.233.233.1", in_ns=True)
    bj.add_route([lax.lo_ip, lax.lo_ns_ip, "1.1.1.1"], link=lax_bj, in_ns=True)

    bj.add_ipset("https://pppublic.oss-cn-beijing.aliyuncs.com/ipsets.txt", in_ns=True)
    bj.add_iptable("mangle", "PREROUTING", "-s 10.56.0.0/16 -m set ! --match-set china_ip dst -m set ! --match-set private_ip dst -j MARK --set-xmark 0x1/0xffffffff", in_ns=True)
    bj.add_cmd(bj.ns_exec + "ip rule add fwmark 0x1 table 100")
    bj.add_cmd(bj.ns_exec + "ip route add default via %s table 100" % lax_bj.left_ip)


    lax.add_route(["10.56.100.0/24", "10.56.200.0/24", "10.56.233.0/24", "10.56.40.0/24"], via=lax.lo_ns_ip, in_ns=False)
    lax.add_route([bj.lo_ip, bj.lo_ns_ip], link=lax_bj, in_ns=True)
    lax.add_route([dev1_bj.left_ip, dev2_bj.left_ip], link=lax_bj, in_ns=True)
    lax.add_route([dev3_bj.left_ip,dev4_bj.left_ip,dev5_bj.left_ip,dev6_bj.left_ip,dev7_bj.left_ip,dev8_bj.left_ip], link=lax_bj, in_ns=True)

    dev1.save_cmds_as_bash(os.path.join(pref,"dev1.sh"))
    dev2.save_cmds_as_bash(os.path.join(pref,"dev2.sh"))
    dev3.save_cmds_as_bash(os.path.join(pref,"dev3.sh"))
    dev4.save_cmds_as_bash(os.path.join(pref,"dev4.sh"))
    dev5.save_cmds_as_bash(os.path.join(pref,"dev5.sh"))
    dev6.save_cmds_as_bash(os.path.join(pref,"dev6.sh"))
    dev7.save_cmds_as_bash(os.path.join(pref,"dev7.sh"))
    dev8.save_cmds_as_bash(os.path.join(pref,"dev8.sh"))
    bj.save_cmds_as_bash(os.path.join(pref,"bj.sh"))
    lax.save_cmds_as_bash(os.path.join(pref,"lax.sh"))

    for dev in devs:
        dev.save_configs_as_config(os.path.join(pref,"{}.conf".format(dev.hostname)))

if __name__ == "__main__":
    yaoyao()
