import os
import sys
pref = "./data"

if __name__=="__main__":
    name = sys.argv[1]
    cmd1 = "content=$(cat {}.conf)".format(os.path.join(pref,name))
    cmd2 = "echo \"${content}\" | qrencode -o - -t UTF8"
    cmd = cmd1 + "&&" + cmd2
    print(cmd)
    os.system(cmd)
