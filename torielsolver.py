import math, sys, os, copy, pathlib
while True:
    try:
        dir = input("Please input the file path to your list of random(100s) or round(random(100))s ")
        rnglist = open(dir, "r")
        #print(pathlib.Path("listofrands.txt"))
        break
    except FileNotFoundError:
        afdsafdsafdsdasf = input("No listofrands.txt detected. Please generate a list of at least 6000 random(100)s between the end of toriel's pre-battle text and before entering the battle, and paste the file in the same folder as this program. Press enter to retry.")
while True:
    PI = input("Do you have the pie? y/n\n").lower()
    if (PI == "y" or PI == "yes"):
        PIE_OFFSET = 22
        break
    elif (PI == "n" or PI == "no"):
        PIE_OFFSET = 0
        break

rngraw = rnglist.readlines()
rng = []
for i in rngraw:
    rng.append(round(float(i)))
rnglist.close()
stack = []
LTSsize = 0

FRAMES = 0
CURRENT_OFFSET = 1
BOTTOMS = 2
CONVERSATION = 3
HP = 4
PREVIOUS_ATK = 5
HISTORY = 6

#potentialManipAction = offsetAdjustment
#negative = variable offset calculated when used
ZZ = 0
DZZ = -1
XZZ = -2
SZZ = -3
ZSZ = 38
DDZZ = -4
DXZZ = -5
DSZZ = -6
DZSZ = -7
SXZZ = -8
SSZZ = -9
SZSZ = -10
XSZZ = -11
XZSZ = -12
ZSSZ = 76
ZXZZ = 82

ZZXZ = -100
DZZXZ = -13
XZZXZ = -14
SZZXZ = -106
ZSZXZ = 96 + PIE_OFFSET
ZZSXZ = 4
ZZXSZ = 102
DDZZXZ = -15
DXZZXZ = -16
DSZZXZ = -17
DZSZXZ = -18
DZZSXZ = -19
DZZXSZ = -20
SXZZXZ = -21
SSZZXZ = -114
SZSZXZ = 102 + PIE_OFFSET
SZZSXZ = 10
SZZXSZ = 108
ZSSZXZ = 192 + (2*PIE_OFFSET)
ZSZSXZ = 100 + PIE_OFFSET
ZSZXSZ = 198 + PIE_OFFSET
ZZSXSZ = 106
ZZXSSZ = 204
XSZZXZ = -22
XZSZXZ = -23
XZZXSZ = -24
LZXZZXZ = 198 + (2*PIE_OFFSET)
ZXLZZXZ = -182

mcs = [[DDZZXZ, 2], [DXZZXZ, 2], [DSZZXZ, 2], [DZSZXZ, 2], [DZZSXZ, 2], [DZZXSZ, 2], [SXZZXZ, 2], [SSZZXZ, 2], [SZSZXZ, 2], [SZZSXZ, 2], [SZZXSZ, 2], [ZSSZXZ, 2], [ZSZSXZ, 2], [ZSZXSZ, 2], [ZZSXSZ, 2], [ZZXSSZ, 2], [XSZZXZ, 2], [XZSZXZ, 2], [XZZXSZ, 2], [ZXLZZXZ, 2], [LZXZZXZ, 2], [DZZXZ, 1], [XZZXZ, 1], [SZZXZ, 1], [ZSZXZ, 1], [ZZSXZ, 1], [ZZXSZ, 1], [ZZXZ, 0]]
norms = [[DDZZ, 2], [DXZZ, 2], [DSZZ, 2], [DZSZ, 2], [SXZZ, 2], [SSZZ, 2], [SZSZ, 2], [XSZZ, 2], [XZSZ, 2], [ZSSZ, 2], [ZXZZ, 2], [DZZ, 1], [XZZ, 1], [SZZ, 1], [ZSZ, 1], [ZZ, 0]]


offsets = [94, 233, 311, 323, 213, 323, 323, 323, 323, 281, 323, 281]
ds = [0, 12, 24, 32, 10, 32, 32, 32, 32, 18, 32, 18]
dds = [0, 24, 48, 66, 20, 66, 66, 66, 66, 36, 66, 36, 16]
xs = [88, 96, 104, 112]


def getRealAdj(adj, conversation, prevcom):
    #gets adjustment values for manips with variable effects
    d = ds[conversation - 1]      #get values for D, DD, and X for this turn
    dd = dds[conversation - 1]
    smod = 0
    if (conversation == 1):
        #print(adj, conversation)
        x = xs[0]
        smod = 4
    elif (prevcom >= 90):
        x = xs[3]
    elif (prevcom >= 70):
        x = xs[1]
    elif (prevcom >= 30):
        x = xs[2]

    if (adj == DZZ):     #I'm so sorry
        adj = d
    elif (adj == XZZ):
        adj = x
    elif (adj == SZZ):
        adj = 6 + smod
    elif (adj == DDZZ):
        adj = dd
    elif (adj == DXZZ):
        adj = d + x
    elif (adj == DSZZ):
        adj = d + 6 + smod
    elif (adj == DZSZ):
        adj = d + 38
    elif (adj == SXZZ):
        adj = x + 4 + smod
    elif (adj == SSZZ):
        adj = 14 + 2*smod
    elif (adj == SZSZ):
        adj = 44 + smod
    elif (adj == XSZZ):
        adj = int(1.5*x + 2)
    elif (adj == XZSZ):
        adj = x + 38
    elif (adj == DZZXZ):
        adj = d
    elif (adj == XZZXZ):
        adj = x
    elif (adj == DDZZXZ):
        adj = dd
    elif (adj == DXZZXZ):
        adj = d + x
    elif (adj == DSZZXZ):
        adj = d + 6
    elif (adj == DZSZXZ):
        adj = d + 96 + 118
    elif (adj == DZZSXZ):
        adj = d + 4
    elif (adj == DZZXSZ):
        adj = d + 102
    elif (adj == SXZZXZ):
        adj = x + 4
    elif (adj == XSZZXZ):
        adj = int(1.5*x + 2)
    elif (adj == XZSZXZ):
        adj = x + 96 + PIE_OFFSET
    elif (adj == XZZXSZ):
        adj = x + 102
    elif (adj <= -100):
        adj *= -1
        adj -= 100

    #print(adj)
    return(adj)

def verifySequence(branch):
    #given completed branch, determines if the branch is a valid toriel manip
    try:
        seq = branch[6:]
        offset = offsets[0]   #initial offset
        conversation = 1      #tracks fight progression
        prevcom = 0           #result of previous turn (tracked to find x for some manips)
        hp = 20               #hp
        bottomsInMyDMs = 0    #number of bottom hands so far
        result = []           #list of attacks gotten
        hpresult = []         #hp at end of each turn
        offsetresult = []
        atkresult = []
        justAte = False       #used to modify offsets
        for i in range(0,len(seq)):
            adj = seq[i]          #adjustment to offset based on manup
            if (adj < 0):         #negative numbers used to indicate variable effects
                adj = getRealAdj(adj, conversation, prevcom)
            #print(adj)
            offset += adj
            offsetresult.append(offset)
            mycommand = rng[offset]     #determines attack type
            atkresult.append(mycommand)
            if (mycommand > 40 and mycommand <= 60):     #fire attack
                result.append("f")
                if (hp == 3):
                    hp = 2
                    offset += 12
                else:
                    result.append("fail")
                    print(result)
                    return(False)
            elif (mycommand > 60 and mycommand <= 80):   #bottom hand
                result.append("b")
                if (bottomsInMyDMs <3 and hp >= 8):      #take bottom hand
                    hp -= 3
                    bottomsInMyDMs += 1
                else:                                    #take top hand
                    result[-1] = "bt"
                    if (hp >= 8):
                        hp -= 4
                    else:
                        hp -= 1
            elif (mycommand > 80 and mycommand <= 100):  #top hand
                result.append("t")
                if (hp >= 8):
                    hp -= 4
                else:
                    hp -= 1
            else:
                result.append("fail")
                print(result)
                return(False)
            hpresult.append(hp)

            if (hp == 2):                                      #heal
                if (conversation < 12):
                    hp = 12
                    offset += offsets[conversation] + 220 + (2*PIE_OFFSET)          #normal offset for turn + difference between spare and heal
                    justAte = True
                else:                                              #end of fight
                    result.append("success ")
                    print(result)
                    return(True)
            elif (justAte):                                    #no textbox so constant offset
                offset += 83
                conversation += 1
                justAte = False
            else:                                             #normal turn
                conversation += 1
                offset += offsets[conversation - 1]
            prevcom = mycommand
        return(False)
    except TypeError:
        print("You got insanely unlucky and the tool was unable to find a successful manip with the options available to it. \nTry changing RNG before the fight and trying again. \nIf you have any questions, please contact @svool_gsviv_ on discord.")

def getValidAttacks(branch):
    if(branch[HP] == 3):
        return([40, 60])
    elif ((branch[HP] >= 7) and ((branch[BOTTOMS] == 3) or (branch[BOTTOMS] == 2 and ((branch[HP] == 8 and branch[CONVERSATION] == 9) or (branch[HP] == 9 and branch[CONVERSATION] == 8))) or (branch[BOTTOMS] == 1 and branch[HP] > 7 and branch[CONVERSATION] == 8) or (branch[BOTTOMS] == 0 and branch[CONVERSATION] == 4))):
        return([60, 80])
    else:
        return([60,100])

def getActions(sequence):
    try:
        seq = sequence[6:]
        textseq = []
        for action in seq:
            if (action == ZZ):
                text = "ZZ"
            elif (action == DZZ):
                text = "DZZ"
            elif (action == XZZ):
                text = "XZZ"
            elif (action == SZZ):
                text = "SZZ"
            elif (action == ZSZ):
                text = "ZSZ"
            elif (action == DDZZ):
                text = "DDZZ"
            elif (action == DXZZ):
                text = "DXZZ"
            elif (action == DSZZ):
                text = "DSZZ"
            elif (action == DZSZ):
                text = "DZSZ"
            elif (action == SXZZ):
                text = "SXZZ"
            elif (action == SSZZ):
                text = "SSZZ"
            elif (action == SZSZ):
                text = "SZSZ"
            elif (action == XSZZ):
                text = "XSZZ"
            elif (action == XZSZ):
                text = "XZSZ"
            elif (action == ZSSZ):
                text = "ZSSZ"
            elif (action == ZXZZ):
                text = "ZXZZ"
            elif (action == ZZXZ):
                text = "ZZXZ"
            elif (action == DZZXZ):
                text = "DZZXZ"
            elif (action == XZZXZ):
                text = "XZZXZ"
            elif (action == SZZXZ):
                text = "SZZXZ"
            elif (action == ZSZXZ):
                text = "ZSZXZ"
            elif (action == ZZSXZ):
                text = "ZZSXZ"
            elif (action == ZZXSZ):
                text = "ZZXSZ"
            elif (action == SSZZXZ):
                text = "DDZZXZ"
            elif (action == DXZZXZ):
                text = "DXZZXZ"
            elif (action == DSZZXZ):
                text = "DSZZXZ"
            elif (action == DZSZXZ):
                text = "DZSZXZ"
            elif (action == DZZSXZ):
                text = "DZZSXZ"
            elif (action == DZZXSZ):
                text = "DZZXSZ"
            elif (action == SXZZXZ):
                text = "SXZZXZ"
            elif (action == SSZZXZ):
                text = "SSZZXZ"
            elif (action == SZSZXZ):
                text = "SZSZXZ"
            elif (action == SZZSXZ):
                text = "SZZSXZ"
            elif (action == SZZXSZ):
                text = "SZZXSZ"
            elif (action == ZSSZXZ):
                text = "ZSSZXZ"
            elif (action == ZSZSXZ):
                text = "ZSZSXZ"
            elif (action == ZSZXSZ):
                text = "ZSZXSZ"
            elif (action == ZZSXSZ):
                text = "ZZSXSZ"
            elif (action == ZZXSSZ):
                text = "ZZXSSZ"
            elif (action == XSZZXZ):
                text = "XSZZXZ"
            elif (action == XZSZXZ):
                text = "XZSZXZ"
            elif (action == XZZXSZ):
                text = "XZZXSZ"
            elif (action == LZXZZXZ):
                text = "LZXZZXZ"
            elif (action == ZXLZZXZ):
                text = "ZXLZZXZ"
            textseq.append(text)
        return(textseq)
    except TypeError:
        pass

def fight():
    global stack
    #frames used, offset, bottom hands, conversation, hp,
    branch0 = [0, 0, 0, 1, 20, 0]
    stack.append(branch0)
    target_frames = 100
    bestresult = None

    while (True):
        skip = False
        try:
            parent = stack.pop()
        except IndexError:
            break
        needHeal = False
        noD = False
        if (parent[HP] == 2):
            if (parent[CONVERSATION] > 10):
                if (parent[FRAMES] < target_frames):
                    target_frames = parent[FRAMES]
                    bestresult = parent
                skip = True
            else:
                parent[HP] = 12
                needHeal = True
        elif ((parent[HP] == 8 or parent[HP] == 9) and parent[CONVERSATION > 7]):
            noD = True
        if (not skip):
            if (not needHeal):
                if (parent[HP] > 7 and parent[CONVERSATION] > 6):
                    offset = 83
                else:
                    offset = offsets[parent[CONVERSATION] - 1]
                for manip in norms:
                    if (not((manip[0] == DZZ or manip[0] == DDZZ or manip[0] == DXZZ or manip[0] == DSZZ) and (noD))):
                        child = copy.deepcopy(parent)
                        adj = manip[0]
                        if (adj < 0):
                            adj = getRealAdj(adj, child[CONVERSATION], child[PREVIOUS_ATK])
                        child[CURRENT_OFFSET] += offset + adj
                        child[PREVIOUS_ATK] = rng[child[CURRENT_OFFSET]]
                        atkrng = getValidAttacks(child)
                        child[FRAMES] += manip[1]
                        if (child[PREVIOUS_ATK] > atkrng[0] and child[PREVIOUS_ATK] <= atkrng[1] and child[FRAMES] < target_frames):
                            if (child[HP] <= 7):
                                child[HP] -= 1
                                if (child[HP] == 2):
                                    child[CURRENT_OFFSET] += 12
                            elif (child[PREVIOUS_ATK] > 60 and child[PREVIOUS_ATK] <= 80 and child[BOTTOMS] < 3):
                                child[BOTTOMS] += 1
                                child[HP] -= 3
                            else:
                                child[HP] -= 4
                            child[CONVERSATION] += 1
                            child.append(manip[0])
                            stack.append(copy.deepcopy(child))
            else:
                offset = offsets[parent[CONVERSATION] - 1] + 220 + (2*PIE_OFFSET)
                for manip in mcs:
                    child = copy.deepcopy(parent)
                    adj = manip[0]
                    if(adj < 0):
                        adj = getRealAdj(adj, child[CONVERSATION], child[PREVIOUS_ATK])
                    child[CURRENT_OFFSET] += offset + adj
                    child[PREVIOUS_ATK] = rng[child[CURRENT_OFFSET]]
                    atkrng = getValidAttacks(child)
                    child[FRAMES] += manip[1]
                    if (child[PREVIOUS_ATK] > atkrng[0] and child[PREVIOUS_ATK] <= atkrng[1]):
                        child[FRAMES] += manip[1]
                        if (child[FRAMES] < target_frames):
                            if (child[PREVIOUS_ATK]  > 60 and child[PREVIOUS_ATK] <= 80 and child[BOTTOMS] < 3):
                                child[BOTTOMS] += 1
                                child[HP] -= 3
                            else:
                                child[HP] -= 4
                            child.append(manip[0])
                            stack.append(copy.deepcopy(child))
    return(bestresult)

print("finding manips...\n\n\n")
a = fight()
if (verifySequence(a)):
    print(getActions(a))
    #print(a)
    print("\n\nHow to read: \nEach element in the list is what to do on one turn. \n A 'D' means to delay closing toriel's text after sparing on the previous turn. \nAn 'S' means to add a frame of space. \nZ and X mean to press Z or X respectively.\n\nFor example: DXZZ would mean to first delay toriel's text be a frame on the previous turn, then once the heart is back on the spare button, first press X, then on the next frame press Z/Enter, then Z/Enter again on the frame after that.")
else:
    print("An error has occured, please DM @svool_gsviv_ on Discord with a copy of \nyour listofrands.txt and they will try to figure out what went wrong as soon as possible. \nSorry for the inconvinience! In the meantime, you can try to use a different \nset of RNG entering the toriel fight, as this is likely an edge case bug. \n(I would reccomend using a 0-frame manip at rock skip or changing whether you get hit at napstablook)")
jhlkffhjdkl = input("\n Enter to close")
























#hi
