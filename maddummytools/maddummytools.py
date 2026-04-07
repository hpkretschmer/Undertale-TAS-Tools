from pathlib import Path

randomVals = []
searchDistance = 2000

# load random(randomArg) calls from a file
def loadRandoms(filepath = "listOfRands.txt", randomArg = 1):
    global randomVals
    randomVals = [float(line) / randomArg for line in open(filepath).readlines()]

# generate calls between spare and attack generation
def fourCycleManip():
    s = sum(x**2 for x in randomVals[6:18])
    sums = [(s, 0)]
    for i in range(1, searchDistance):
        s = s - randomVals[6 + i - 1]**2 + randomVals[6 + i + 11]**2
        sums.append((s, i))
    sums.sort(key=lambda x: (-x[0], x[1]))
    return sums

# generate calls during the first AHAHAHAHA textbox
defaulttearfilepath = Path(__file__).resolve().parent / "dummybullets2.txt" # get this file from discord
def tearManip(tearfilepath = defaulttearfilepath):
    minframes = float("inf")
    offsets = []
    for offset in range(searchDistance):
        frames = fastestTear(offset, tearfilepath)
        if frames < minframes:
            minframes = frames
            offsets = [offset]
        elif frames == minframes:
            offsets.append(offset)
    return minframes, offsets

teardata = None

XDIFF = 0.2
YDIFF = 11
SZDIFF = 0.1
HSPDDIFF = 0.06
def tdkey(x, y, sz, hspd):
    assert 0 <= x <= 20
    assert 0 <= y <= 1100
    assert 0 <= sz <= 1
    assert 0 <= hspd <= 6
    return (
        int(round(x / XDIFF)),
        int(round(y / YDIFF)),
        int(round(sz / SZDIFF)),
        int(round(hspd / HSPDDIFF))
    )

def initTearData(tearfilepath):
    print("Loading tear data from", tearfilepath)
    global teardata
    with open(tearfilepath) as f:
        teardata = {}
        lines = f.read().splitlines()
        for i, line in enumerate(lines):
            if i % (len(lines) // 8) == 0:
                print(100 * i // len(lines), "% done")
            x, y, sz, hspd, frames = map(float, line.split(","))
            # normalize key to avoid floating point issues
            teardata[tdkey(x, y, sz, hspd)] = int(frames)

def cround(val, diff):
    return round(val / diff) * diff

def fastestTear(offset, tearfilepath):
    if teardata is None:
        initTearData(tearfilepath)
    assert teardata is not None, "Tear data not loaded"
    minframes = float("inf")
    for i in range(23):
        x = cround(randomVals[offset + 5 * i + 1] * 20, XDIFF)
        y = cround(randomVals[offset + 5 * i + 0] * 1100, YDIFF)
        sz = cround(randomVals[offset + 5 * i + 4] * 1, SZDIFF)
        hspd = cround(randomVals[offset + 5 * i + 2] * 6, HSPDDIFF)
        # print(10 + x, -10 - y, 1 + sz, (hspd - 2) / 4)
        minframes = min(minframes, teardata.get(tdkey(x, y, sz, hspd), float("inf")))
    return minframes