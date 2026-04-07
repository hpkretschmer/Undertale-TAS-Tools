while True:
    try:
        dir = input("Please input the file path to your list of random(1)s ")
        rnglist = open(dir, "r")
        #print(pathlib.Path("listofrands.txt"))
        break
    except FileNotFoundError:
        afdsafdsafdsdasf = input("File not found... ")
rng30 = []
rng18 = []
for i in rnglist:
    rng30.append(round(30*float(i)))
    rng18.append(round(18*float(i)))
xlist = [0, 4, 10, 18, 28, 40, 54, 70, 88, 108, 130, 154, 180, 208, 238, 270, 304, 340, 378, 418]
phone = [26, 12, None] # last one depends on toriel
droplist = [82, 122, 136, 56, 58, 58, 58, 58, 58, 58, 58, 58, 58, 58, 58, 58, 58, 58, 58]
uselist = [104, 116]

seenoffsets0 = []
seenoffsets30 = []
valid0s = []
valid30s = []

sdheader = "      x1  z1        x2  z2   offset"
cellheader = " x1  z1  x2  z2  x3  z3   offset"


def phonemanip():
    global seendoffsets0
    global seendoffsets30
    global valid0s
    global valid30s
    for frames in range(20):
        for x1 in range(frames+1):
            for z1 in range(frames+1-x1):
                for x2 in range(frames+1-x1-z1):
                    for z2 in range(frames+1-x1-z1-x2):
                        for x3 in range(frames+1-x1-z1-x2-z2):
                            for z3 in range(frames+1-x1-z1-x2-z2-x3):
                                offset = xlist[x1] + phone[0]*(z1+1) + xlist[x2] + phone[1]*(z2+1) + xlist[x3] + phone[2]*(z3+1) + 4
                                if((not (offset in seenoffsets0)) and (rng30[offset] == 0)):
                                    valid0s.append([x1, z1, x2, z2, x3, z3, offset])
                                    seenoffsets0.append(offset)

    sort0s()

    for manip0 in valid0s:
        offset0 = manip0[-1]
        for frames in range(14):
            for x1 in range(frames+1):
                for z1 in range(0, frames+1-x1):
                    for x2 in range(frames+1-x1-z1):
                        for z2 in range(frames+1-x1-z1-x2):
                            for x3 in range(frames+1-x1-z1-x2-z2):
                                for z3 in range(frames+1-x1-z1-x2-z2-x3):
                                    offset = xlist[x1] + phone[0]*(z1+1) + xlist[x2] + phone[1]*(z2+1) + xlist[x3] + phone[2]*(z3+1) + 44 + offset0 + papoffset
                                    if((not (offset in seenoffsets30)) and (rng30[offset] == 30)):
                                        valid30s.append([x1, z1, x2, z2, x3, z3, offset0, offset])
                                        seenoffsets30.append(offset)

def stickdropmanip():
    global seenoffsets0
    global seenoffsets30
    global valid0s
    global valid30s
    for frames in range(14):
        for u1 in range(2):
            for x1 in range(frames+1):
                for z1 in range(frames+1-x1):
                    for u2 in range(u1+1):
                        for x2 in range(frames+1-x1-z1):
                            for z2 in range(frames+1-x1-x2-z1):
                                offset = xlist[x1] + xlist[x2] + uselist[u1]*(z1+1) + uselist[u2]*(z2+1)
                                if((not offset in seenoffsets0) and (rng30[offset] == 0)):
                                    valid0s.append([u1, x1, z1, u2, x2, z2, offset])
                                    seenoffsets0.append(offset)

    sort0s()

    for manip0 in valid0s:
        offset0 = manip0[-1]
        for frames in range(10):
            for u1 in range(2):
                for x1 in range(frames+1):
                    for z1 in range(frames+1-x1):
                        dropoffset = xlist[x1] + uselist[u1]*(z1+1) + 5 + offset0
                        for x2 in range(frames+1-x1-z1):
                            for z2 in range(frames+1-x1-z1-x2):
                                offset = dropoffset + xlist[x2] + droplist[rng18[dropoffset]]*(z2+1) + 36 + papoffset
                                if((not offset in seenoffsets30) and (rng30[offset] == 30)):
                                    valid30s.append([u1, x1, z1, 0, x2, z2, offset0, offset])
                                    seenoffsets30.append(offset)

def sort0s():
    global seendoffsets0
    global seendoffsets30
    global valid0s
    global valid30s
    while True:
        swaps = 0
        for i in range(len(valid0s) - 1):
            if(valid0s[i][-1] > valid0s[i+1][-1]):
                temp = valid0s[i]
                valid0s[i] = valid0s[i+1]
                valid0s[i+1] = temp
                swaps += 1
        if(swaps == 0):
    #################################
            break

def sort30s():
    global seendoffsets0
    global seendoffsets30
    global valid0s
    global valid30s
    while True:
        swaps = 0
        for i in range(len(valid30s) - 1):
            if(valid30s[i][-1] > valid30s[i+1][-1]):
                temp = valid30s[i]
                valid30s[i] = valid30s[i+1]
                valid30s[i+1] = temp
                swaps += 1
        if(swaps == 0):
    #################################
            break

def printmanips():
    for m0 in valid0s:
        current30s = []
        for m30 in valid30s:
            if(m30[-2] == m0[-1]):
                current30s.append(m30)
        if(len(current30s) > 0):
            if(stickdrop):
                print(sdheader)
                print(readablestick(m0, False))
                print("  " + sdheader)
                for m30 in current30s:
                    print("  " + readablestick(m30, True))
                print("\n---------------------------")
            else:
                print(cellheader)
                print(readablecell(m0))
                print("  " + cellheader)
                for m30 in current30s:
                    print("  " + readablecell(m30))
                print("\n---------------------------")

def readablestick(manip, drop):
    if(manip[0] == 0):
        u1 = "use "
    else:
        u1 = "info"
    if(drop):
        u2 = "drop"
    elif(manip[3] == 0):
        u2 = "use "
    else:
        u2 = "info"

    return f" {u1} {manip[1]}   {manip[2]}   {u2}  {manip[4]}   {manip[5]}    {manip[-1]}"

def readablecell(manip):
    return f" {manip[0]}   {manip[1]}   {manip[2]}   {manip[3]}   {manip[4]}   {manip[5]}    {manip[-1]}"


while True:
    stickcellstr = input("Do you have the stick? y/n\n")
    if(stickcellstr.lower() == "y"):
        stickdrop = True
        print("\n\n---------------------------")
        break
    elif(stickcellstr.lower() == "n"):
        stickdrop = False
        print("\n\n---------------------------")
        break
while True:
    papcall = input("Is Papyrus alive? y/n\n")
    if(papcall.lower() == "y"):
        papoffset = 1376
        print("\n\n---------------------------")
        break
    elif(papcall.lower() == "n"):
        papoffset = 0
        print("\n\n---------------------------")
        break
while True:
    toriel = input("Is Toriel alive? y/n\n")
    if(toriel.lower() == "y"):
        phone[2] = 38
        print("\n\n---------------------------")
        break
    elif(toriel.lower() == "n"):
        phone[2] = 36
        print("\n\n---------------------------")
        break

if(stickdrop):
    stickdropmanip()
else:
    phonemanip()
sort30s()
printmanips()
