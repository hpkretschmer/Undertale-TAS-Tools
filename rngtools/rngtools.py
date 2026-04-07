import bisect
import itertools

def binsearch(sorted_list, value):
    index = bisect.bisect_left(sorted_list, value)
    return index < len(sorted_list) and sorted_list[index] == value

randomVals = []
chooseVals = []
yyRandomVals = []
startOffset = 0
searchDistance = 2000
manips = [{} for _ in range(11)]

# load random(randomArg) calls from a file
def loadRandoms(filepath = "listOfRands.txt", randomArg = 1):
    global randomVals
    randomVals = [float(line) / randomArg for line in open(filepath).readlines()]

# load choose(0, 1, ..., n-1) calls from a file
def loadChooses(filepath = "listOfChooses.txt"):
    global chooseVals
    chooseVals = [int(line) for line in open(filepath).readlines()]

def loadBoth():
    loadRandoms()
    loadChooses()

def loadYYRandoms(filepath):
    global yyRandomVals
    import numpy as np
    yyRandomVals = list(np.fromfile(filepath, dtype=np.uint32))
    
def yyRandomToRandom(randomArg = 1):
    return list(map(lambda e : 2.3283064365386963e-10 * randomArg * e, yyRandomVals))

# find indices of randomVals where randomVal * randomArg is in targetRange = [l, r]
# offset specifies the starting index to search from
def findRandomIndex(randomArg, targetRange, offset):
    ls = []
    l = max(0, offset - startOffset - 1)
    r = min(len(randomVals), offset - startOffset - 1 + searchDistance)
    # print(l, r, offset)
    for i in range(l, r):
        val = randomVals[i] * randomArg
        if targetRange[0] <= val <= targetRange[1]:
            ls.append(i)
    return ls

# find number of extra RNG calls to produce
def findRandomOffset(randomArg, targetRange, offset):
    return [i - (offset - startOffset - 1) for i in findRandomIndex(randomArg, targetRange, offset)]

# find indices of randomVals where randomVal * randomArg is in targetRange for multiple (randomArg, targetRange, offset) tuples
def findRandomsIndex(*args):
    assert all(a2[2] - a1[2] > 0 for a1, a2 in zip(args, args[1:])), "Offsets must be strictly increasing"
    foundIndices = [findRandomIndex(*arg) for arg in args]
    relativeOffsets = [arg[2] - args[0][2] for arg in args[1:]]
    ls = []
    for i in foundIndices[0]:
        if all(binsearch(found, i + offset) for found, offset in zip(foundIndices[1:], relativeOffsets)):
            ls.append(i)
    return ls

# find number of extra RNG calls to produce
def findRandomsOffset(*args):
    return [i - (args[0][2] - startOffset - 1) for i in findRandomsIndex(*args)]

# find indices of chooseVals where chooseVal == targetVal
# offset specifies the starting index to search from
def findChooseIndex(targetValue, offset):
    ls = []
    l = max(0, offset - startOffset - 1)
    r = min(len(chooseVals), offset - startOffset - 1 + searchDistance)
    print(l, r, offset)
    for i in range(l, r):
        if chooseVals[i] == targetValue:
            ls.append(i)
    return ls

# find number of extra RNG calls to produce
def findChooseOffset(targetValue, offset):
    return [i - (offset - startOffset - 1) for i in findChooseIndex(targetValue, offset)]

# find indices of chooseVals where chooseVal == targetVal for multiple (targetVal, offset) tuples
def findChoosesIndex(*args):
    assert all(a2[1] - a1[1] > 0 for a1, a2 in zip(args, args[1:])), "Offsets must be strictly increasing"
    foundIndices = [findChooseIndex(*arg) for arg in args]
    relativeOffsets = [arg[1] - args[0][1] for arg in args[1:]]
    ls = []
    for i in foundIndices[0]:
        if all(binsearch(found, i + offset) for found, offset in zip(foundIndices[1:], relativeOffsets)):
            ls.append(i)
    return ls

# find number of extra RNG calls to produce
def findChoosesOffset(*args):
    return [i - (args[0][1] - startOffset - 1) for i in findChoosesIndex(*args)]

def stepManip(
        stepRandomArg, 
        stepOffset, 
        encounter, 
        blconOffset, 
        kills, 
        maxkills,
        maxDelay = 30
):
    delay_to_offsets = {}
    populationfactor = min(8, maxkills / (maxkills - kills))
    for stepDelay, blconDelay in itertools.product(
        range(min(maxDelay + 1, stepRandomArg)), 
        range(6)
    ):
        def totaldelay():
            res = blconDelay + int(stepDelay * populationfactor) + 1
            return res
        if totaldelay() > maxDelay:
            continue
        if totaldelay() not in delay_to_offsets:
            delay_to_offsets[totaldelay()] = []
        delay_to_offsets[totaldelay()] += findRandomsOffset(
            (stepRandomArg, (0, 0.5 + stepDelay), stepOffset),
            encounter,
            (5, (0, 0.5 + blconDelay), blconOffset)
        )
    offset_to_delay = {}
    for delay, offsets in delay_to_offsets.items():
        for offset in offsets:
            if offset not in offset_to_delay:
                offset_to_delay[offset] = delay
            else:
                offset_to_delay[offset] = min(offset_to_delay[offset], delay)
    return sorted(offset_to_delay.items(), key=lambda x: (x[1], x[0]))

# todo stepmanipOffset

def doubleStepManip(
        stepRandomArg1,
        stepOffset1,
        stepRandomArg2, 
        stepOffset2, 
        encounter, 
        blconOffset, 
        kills, 
        maxkills,
        maxDelay = 30
):
    delay_to_offsets = {}
    populationfactor = min(8, maxkills / (maxkills - kills))
    for stepDelay1, stepDelay2, blconDelay in itertools.product(
        range(min(maxDelay + 1, stepRandomArg1)), 
        range(min(maxDelay + 1, stepRandomArg2)), 
        range(6)
    ):
        def totaldelay():
            res = blconDelay + int(stepDelay1 * populationfactor) + int(stepDelay2 * populationfactor) + 2
            return res
        if totaldelay() > maxDelay:
            continue
        if totaldelay() not in delay_to_offsets:
            delay_to_offsets[totaldelay()] = []
        delay_to_offsets[totaldelay()] += findRandomsOffset(
            (stepRandomArg1, (0, 0.5 + stepDelay1), stepOffset1),
            (stepRandomArg2, (0, 0.5 + stepDelay2), stepOffset2),
            encounter,
            (5, (0, 0.5 + blconDelay), blconOffset)
        )
    offset_to_delay = {}
    for delay, offsets in delay_to_offsets.items():
        for offset in offsets:
            if offset not in offset_to_delay:
                offset_to_delay[offset] = delay
            else:
                offset_to_delay[offset] = min(offset_to_delay[offset], delay)
    return sorted(offset_to_delay.items(), key=lambda x: (x[1], x[0]))


from data import manips, encounter_data, monsters_to_battlegroup

def addManip(offsetDelayList, categoryname):
    reversemanips = manips[categoryname]["reversemanips"]
    baselen = len(next(iter(manips[categoryname]["manips"][0])))
    return sorted((
        (offset, delay1 + len(reversemanips[offset]) - baselen, reversemanips[offset]) 
        for offset, delay1 in offsetDelayList
        if offset in reversemanips),
        key = lambda x: (x[1], x[0])
    )

def addManipNoDelay(offsetList, categoryname):
    reversemanips = manips[categoryname]["reversemanips"]
    baselen = len(next(iter(manips[categoryname]["manips"][0])))
    return sorted((
        (offset, len(reversemanips[offset]) - baselen, reversemanips[offset]) 
        for offset in offsetList
        if offset in reversemanips),
        key = lambda x: (x[1], x[0])
    )

# generate (randomArg, targetRange, offset) tuple for blcon with given frames and offset
def exactBlcon(frames, offset):
    assert frames in range(15, 21)
    if frames == 15:
        return (5, (0, 0.5), offset)
    if frames == 20:
        return (5, (4.5, 5), offset)
    return (5, (frames - 15 - 0.5, frames - 15 + 0.5), offset)

# generate (randomArg, targetRange, offset) tuple for encounter with given encounterer, monsters and offset
def encounter(encounterer, monsters, offset):
    if type(monsters) is str:
        monsters = monsters_to_battlegroup[monsters]
    return encounter_data[encounterer][monsters] + (offset,)

# generate list of rng offsets for scrolling text, where
# oneframeoffset is the smallest number of extra rng calls that can be made
def scrollOffsets(oneframeoffset, length = 200):
    extracalls = list(range(oneframeoffset, oneframeoffset + 2 * length + 2, 2))
    dp = [0] * (length + 1)
    for i in range(1, length+1):
        dp[i] = dp[i-1] + extracalls[i-1]
    return dp

# generate list of rng offsets for scrolling text with a pause, where
# oneframeoffset is the smallest number of extra rng calls that can be made
# pausestart is the first frame with a duplicate number of rng calls, i.e. where scrollOffsets breaks
# pauseend is the last frame with that number of rng calls
# both measured as the difference to the oneframeoffset frame
def scrollOffsetsWithPause(oneframeoffset, pausestart, pauseend, length = 200):
    basecalls = list(range(oneframeoffset, oneframeoffset + 2 * length + 2, 2))
    extracalls = \
        basecalls[:pausestart] + \
        (pauseend - pausestart + 1) * [basecalls[pausestart]] + \
        basecalls[pausestart:]
    dp = [0] * (length + 1)
    for i in range(1, length+1):
        dp[i] = dp[i-1] + extracalls[i-1]
    return dp

# candlesOrMagicScrollOffsets = scrollOffsetsWithPause(2, 40, 50)