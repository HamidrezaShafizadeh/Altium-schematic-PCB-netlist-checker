import re, sys

##########################################################################
def show_exception_and_exit(exc_type, exc_value, tb):
    import traceback
    traceback.print_exception(exc_type, exc_value, tb)
    input("Press key to exit.")
    sys.exit(-1)

sys.excepthook = show_exception_and_exit
##########################################################################
def is_number(string):
    for character in string:
        if not character.isdigit():
            return False
    return True

Calay_dic = {}
PCB_dic = {}
Calay_netlist_address = input("Calay netlist document file: ")
exported_PCB_netlist_address = input("Exported PCB netlist document file: ")
with open(Calay_netlist_address, 'r') as Calay_netlist_document:
    Calay = Calay_netlist_document.readlines()
line = 0

if len(Calay) == 0:
    print("Calay Netlist is empty")
    exit(1)
for i in Calay:
    line += 1
    words = re.split(r"\s+", i)
    words = list(filter(lambda x: x != '' and x != ' ', words))
    if len(words) > 0:
        if len(words) == 1:
            print("Missed Net name or component names in Calay Netlist. Line: {line}->{i}")
            exit(1)
        if words[0][0] != '/':
            print("Missed '/' in Calay Netlist. Line: {line}->{i}")
            exit(1)
        if words[-1][-1] != ';':
            print("Missed ';' in Calay Netlist. Line: {line}->{i}")
            exit(1)
        words[-1] = words[-1][:-1]
        for j in range(1, len(words[1:])+1):
            begin = words[j].rfind('(')
            if begin != -1 and words[j][-1] == ')':
                words[j] = words[j][:begin]+'-'+words[j][begin+1:-1]
        t = words[0][1:].rfind('_')
        if t != -1 and is_number(words[0][t+1:]):
            words[0] = f"{words[0][:t]}-{words[0][t+1:]}"
        Calay_dic[words[0][1:]] = set(words[1:])

#print(Calay_dic)

with open(exported_PCB_netlist_address, 'r') as exported_PCB_netlist_document:
    PCB = exported_PCB_netlist_document.read().split(')\n(\n')

if len(PCB) == 0:
    print("PCB Netlist is empty")
    exit(1)
ind = -1
while (PCB[-1][ind] == ' ' or PCB[-1][ind] == '\n' or PCB[-1][ind] == '\t') and ind != -len(PCB[-1]):
    ind -= 1
if PCB[-1][ind] != ')':
    print("Last character of PCB Netlist should be ')'.")
    exit(1)
PCB[-1] = PCB[-1][:ind]
if PCB[0].find("]\n(\n") == -1:
    print("Invalid PCB Netlist Format.")
    exit(1)
PCB[0] = PCB[0][PCB[0].find("]\n(\n")+4:-1]
for i in PCB:
    temp = i.split('\n')
    temp = list(filter(lambda x: x != '' and x != ' ', temp))
    if len(temp) == 0:
        print(f"Excepted more parameters ->{i}")
        exit(1)
    t = temp[0].rfind('_')
    if t != -1 and is_number(temp[0][t+1:]):
        temp[0] = f"{temp[0][:t]}-{temp[0][t+1:]}"
    PCB_dic[temp[0]] = set(temp[1:])


if(PCB_dic == Calay_dic):
    print("Netlists are identical")
    input("Press Enter to exit...")
else:
    print("Netlists are not identical\n")
    for i in PCB_dic:
        if i not in Calay_dic:
            print(f"{i} is not in Calay Netlist")
            input()
        elif PCB_dic[i] != Calay_dic[i]:
            print(f"PCB_dic[{i}] = {PCB_dic[i]} != Calay_dic[{i}] = {Calay_dic[i]}")
            print("\n\n")
            PCB_Calay = PCB_dic[i].difference(Calay_dic[i])
            Calay_PCB = Calay_dic[i].difference(PCB_dic[i])
            if len(PCB_Calay):
                if len(PCB_Calay) == 1:
                    print(f"{PCB_Calay} is in PCB but not in Calay Netlist")
                else:
                    print(f"{PCB_Calay} are in PCB but not in Calay Netlist")
            if len(Calay_PCB):
                if len(Calay_PCB) == 1:
                    print(f"{Calay_PCB} is in Calay Netlist but not in PCB")
                else:
                    print(f"{Calay_PCB} are in Calay Netlist but not in PCB")
            input("press Enter to continue...")
    for i in Calay_dic:
        if i not in PCB_dic:
            print(f"{i} is not in PCB Netlist")
            input()

