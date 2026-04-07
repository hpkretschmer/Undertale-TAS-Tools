randomVals = []

searchDistance = 2000

# load random(randomArg) calls from a file
def loadRandoms(filepath = "listOfRands.txt", randomArg = 1):
    global randomVals
    randomVals = [float(line) / randomArg for line in open(filepath).readlines()]

# generate the rng calls just before the siner is created
# the value returned is both the timeloss at that offset and the number of extra rng calls used
def utusiner_timeloss(offset):
    TEXTS = [54, 2, 70, 2, 28, 2, 20, 2, 32, 0, 56, 2, 38, 2, 32, 0]
    res = 0
    curoffset = offset
    for i, text in enumerate(TEXTS):
        ww = 1 + 0.5 * (i - res)
        idealww2 = 4 + 6 * randomVals[curoffset]
        if idealww2 <= ww - 0.5:
            res += 2
        elif ww - 0.5 < idealww2 and idealww2 <= ww:
            res += 1
        curoffset += 1 + text
    return res
        
def utusiner_manip_index():
    crtmin = float('inf')
    argmin = []
    for i in range(searchDistance):
        tl = utusiner_timeloss(i)
        if tl < crtmin:
            crtmin = tl
            argmin = [i]
        elif tl == crtmin:
            argmin.append(i)
    return crtmin, argmin

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 1:
        loadRandoms()
    elif len(sys.argv) == 2:
        if sys.argv[1] == "--help":
            print("Usage: python3 utusiner.py [randomsFile] [randomArg] [searchDistance]")
            sys.exit(0)
        loadRandoms(sys.argv[1])
    elif len(sys.argv) == 3:
        loadRandoms(sys.argv[1], int(sys.argv[2]))
    elif len(sys.argv) == 4:
        loadRandoms(sys.argv[1], int(sys.argv[2]))
        searchDistance = int(sys.argv[3])
    zero_tl = utusiner_timeloss(0)
    print(f"Timeloss at offset 0: {zero_tl}")
    tl, indices = utusiner_manip_index()
    print(f"Minimum timeloss: {tl} at indices: {indices}")