import bisect
import itertools
import copy
from pathlib import Path

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

candlesOrMagicScrollOffsets = scrollOffsetsWithPause(2, 40, 50)

# Data section

encounter_data = {
    "ruins1" : {
        4 : (2, (0, 1)),
        5 : (2, (1, 2))
    },
    "ruins1_hardmode" : {
        126 : (3, (0, 1)),
        125 : (3, (1, 2)),
        120 : (3, (2, 3)),
    },
    "ruins2" : {
        4 : (20, (0, 5)),
        5 : (20, (5, 10)),
        7 : (20, (10, 15)),
        6 : (20, (15, 18)),
        9 : (20, (18, 20)),
    },
    "ruins2_hardmode" : {
        125 : (20, (0, 5)),
        126 : (20, (5, 10)),
        123 : (20, (10, 15)),
        122 : (20, (15, 18)),
        124 : (20, (18, 20)),
    },
    "ruins3" : {
        6 : (20, (0, 5)),
        7 : (20, (5, 10)),
        8 : (20, (10, 15)),
        9 : (20, (15, 18)),
        10 : (20, (18, 20)),
    },
    "ruins3_hardmode" : {
        125 : (20, (0, 5)),
        126 : (20, (5, 10)),
        123 : (20, (10, 15)),
        122 : (20, (15, 18)),
        124 : (20, (18, 20)),
    },
    "ruins4" : {
        11 : (20, (0, 4)),
        12 : (20, (4, 8)),
        13 : (20, (8, 12)),
        16 : (20, (12, 16)),
        17 : (20, (16, 19)),
        15 : (20, (19, 20)),
    },
    "ruins4_hardmode" : {
        128 : (20, (0, 4)),
        129 : (20, (4, 8)),
        130 : (20, (8, 12)),
        121 : (20, (12, 16)),
        124 : (20, (16, 19)),
        132 : (20, (19, 20)),
    },
    "ruins5" : {
        18 : (15, (0, 2)),
        11 : (15, (2, 9)),
        13 : (15, (9, 15)),
    },
    "ruins5_hardmode" : {
        128 : (20, (0, 4)),
        129 : (20, (4, 8)),
        130 : (20, (8, 12)),
        121 : (20, (12, 16)),
        124 : (20, (16, 19)),
        132 : (20, (19, 20)),
    },
    "ruins6" : {
        18 : (15, (0, 2)),
        11 : (15, (2, 9)),
        13 : (15, (9, 15)),
    },
    "ruins6_hardmode" : {
        128 : (20, (0, 4)),
        129 : (20, (4, 8)),
        130 : (20, (8, 12)),
        121 : (20, (12, 16)),
        124 : (20, (16, 19)),
        132 : (20, (19, 20)),
    },
    "tundra1" : {
        30 : (15, (0, 8)),
        32 : (15, (8, 15)),
    },
    "jerry" : {
        35 : (15, (0, 8.5)),
        36 : (15, (8.5, 15)),
    },
    "water1" : {
        43 : (15, (11, 15)),
        53 : (15, (7, 11)),
        40 : (15, (4, 7)),
        54 : (15, (0, 4)),
    },
    "water2" : {
        54 : (15, (10, 15)),
        55 : (15, (4, 10)),
        41 : (15, (0, 4)),
    },
    "fire1" : {
        50 : (15, (10, 15)),
        78 : (15, (6, 10)),
        77 : (15, (0, 6)),
    },
    "core1" : {
        66 : (15, (13, 15)),
        64 : (15, (10, 13)),
        65 : (15, (7, 10)),
        68 : (15, (4, 7)),
        67 : (15, (2, 4)),
        60 : (15, (1, 2)),
        59 : (15, (0, 1)),
    }
}

monsters_to_battlegroup = {
    "Froggit": 4,
    "Whimsun": 5,
    "Froggit, Whimsun": 6,
    "Moldsmal": 7,
    "Moldsmal, Moldsmal, Moldsmal": 8,
    "Triple Moldsmal": 8,
    "Froggit, Froggit": 9,
    "Moldsmal, Moldsmal (Ruins)": 10,
    "Moldsmal, Migosp": 11,
    "Migosp, Vegetoid": 12,
    "Loox": 13,
    "Loox, Vegetoid, Migosp": 15,
    "Vegetoid, Vegetoid": 16,
    "Loox, Loox": 17,
    "Vegetoid": 18,
    "Snowdrake": 30,
    "Icecap": 32,
    "Icecap, Jerry": 35,
    "Icecap, Jerry, Snowdrake": 36,
    "Aaron": 40,
    "Temmie": 41,
    "Woshua": 43,
    "Tsunderplane": 50,
    "Moldsmal, Moldsmal (Waterfall)": 53,
    "Woshua, Aaron": 54,
    "Moldbygg, Woshua": 55,
    "Madjick": 59,
    "Knight Knight": 60,
    "Final Froggit": 126,
    "Whimsalot, Final Froggit": 64,
    "Whimsalot, Astigmatism": 65,
    "Final Froggit, Astigmatism": 66,
    "Final Froggit, Astigmatism, Whimsalot": 67,
    "Triple Core": 67,
    "Knight Knight, Madjick": 68,
    "Tsunderplane, Vulkin": 77,
    "Pyrope, Pyrope": 78,
    "Final Froggit, Astigmatism (Hard Mode)": 120,
    "Final Froggit, Migospel": 121,
    "Parsnik": 122,
    "Moldessa, Moldessa": 123,
    "Moldessa, Moldessa, Moldessa": 124,
    "Triple Moldessa": 124,
    "Final Froggit, Whimsalot": 125,
    "Moldessa, Migospel": 128,
    "Parsnik, Migospel": 129,
    "Parsnik, Parsnik": 130,
    "Astigmatism, Astigmatism": 132,
}

manips = {
    "Whimsun" : { # single Whimsun
        "namelength" : 30,
        "endspace" : 78,
        "manips" : [
            { # 0 frame
                "ZZ" : 0,
            }, 
            { # 1 frame
                "SZZ" : 10,
                "XZZ" : 104,
            }, # 2 frame
            {
                "SSZZ" : 22,
                "SXZZ" : 112,
                "XSZZ" : 160,
                "ZXZZ" : 66,
                "LXRZ" : 82,
            },
            { # 3 frame
                "SSSZZ" : 36,
                "SSXZZ" : 122,
                "SXSZZ" : 168,
                "XSSZZ" : 216,
                "SZXZZ" : 76,
                "SLXRZ" : 92,
                "XZXZZ" : 170,
                "XLXRZ" : 186,
                "ZSXZZ" : 96,
                "LSXRZ" : 120,
                "ZXSZZ" : 72,
                "LXSRZ" : 88,
                "ZXXZZ" : 174,
                "LXXRZ" : 190,
            }, 
            { # 4 frame
                "SSSSZZ" : 52,
                "SSSXZZ" : 134,
                "SSXSZZ" : 178,
                "SXSSZZ" : 224,
                "XSSSZZ" : 272,
                "SSZXZZ" : 88,
                "SSLXRZ" : 104,
                "SXZXLD" : 0, #todo
                "SXLXZD" : 0, #todo
                "XSZXLD" : 0, #todo
                "XSLXZD" : 0, #todo
                "SZSXZZ" : 106,
                "SLSXRZ" : 130,
                "SZXSZZ" : 82,
                "SLXSRZ" : 98,
                "SZXXZZ" : 184,
                "SLXXRZ" : 200,
                "XZSXZZ" : 200, 
                "XLSXRZ" : 224,
                "XZXSZZ" : 176,
                "XLXSRZ" : 192,
                "XZXXZZ" : 278,
                "XLXXRZ" : 294,
                "ZSSXZZ" : 126,
                "LSSXRZ" : 158,
                "ZSXSZZ" : 102,
                "LSXSRZ" : 126,
                "ZSXXZZ" : 204,
                "LSXXRZ" : 228,
                "ZXSSZZ" : 80,
                "LXSSRZ" : 96,
                "ZXSXZZ" : 178,
                "LXSXRZ" : 194,
                "ZXXSZZ" : 230,
                "LXXSRZ" : 246,
                "ZXZXZZ" : 132,
                "LXRXZZ" : 148,
                "LXZXRZ" : 164,
            }
        ]
    },
    "Froggit_doesntknow" : { # Froggit, Whimsun on the turn Froggit is killed, with flavor text "Froggit doesn't seem to know why it's here."
        "namelength" : 30,
        "endspace" : 78,
        "manips" : [
            { # 0 frame
                "ZZ" : 0,
            }, 
            { # 1 frame
                "SZZ" : 6,
                "XZZ" : 180,
            }, # 2 frame
            {
                "SSZZ" : 14,
                "SXZZ" : 184,
                "XSZZ" : 272,
                "ZXZZ" : 66,
                "LXRZ" : 82,
            },
            { # 3 frame
                "SSSZZ" : 24,
                "SSXZZ" : 190,
                "SXSZZ" : 276,
                "XSSZZ" : 364,
                "SZXZZ" : 72,
                "SLXRZ" : 88,
                "XZXZZ" : 246,
                "XLXRZ" : 262,
                "ZSXZZ" : 96,
                "LSXRZ" : 120,
                "ZXSZZ" : 72,
                "LXSRZ" : 88,
                "ZXXZZ" : 246,
                "LXXRZ" : 262,
            }, 
            { # 4 frame
                "SSSSZZ" : 36,
                "SSSXZZ" : 198,
                "SSXSZZ" : 282,
                "SXSSZZ" : 368,
                "XSSSZZ" : 456,
                "SSZXZZ" : 80,
                "SSLXRZ" : 96,
                "SXZXLD" : 0, #todo
                "SXLXZD" : 0, #todo
                "XSZXLD" : 0, #todo
                "XSLXZD" : 0, #todo
                "SZSXZZ" : 102,
                "SLSXRZ" : 126,
                "SZXSZZ" : 78,
                "SLXSRZ" : 94,
                "SZXXZZ" : 252,
                "SLXXRZ" : 268,
                "XZSXZZ" : 276, 
                "XLSXRZ" : 300,
                "XZXSZZ" : 252,
                "XLXSRZ" : 268,
                "XZXXZZ" : 426,
                "XLXXRZ" : 442,
                "ZSSXZZ" : 126,
                "LSSXRZ" : 158,
                "ZSXSZZ" : 102,
                "LSXSRZ" : 126,
                "ZSXXZZ" : 276,
                "LSXXRZ" : 300,
                "ZXSSZZ" : 80,
                "LXSSRZ" : 96,
                "ZXSXZZ" : 250,
                "LXSXRZ" : 266,
                "ZXXSZZ" : 338,
                "LXXSRZ" : 354,
                "ZXZXZZ" : 132,
                "LXRXZZ" : 148,
                "LXZXRZ" : 164,
            }
        ]
    },
    "Froggit_hops" : { # Froggit, Whimsun on the turn Froggit is killed, with flavor text "Froggit hops to and fro."
        "namelength" : 30,
        "endspace" : 78,
        "manips" : [
            { # 0 frame
                "ZZ" : 0,
            }, 
            { # 1 frame
                "SZZ" : 6,
                "XZZ" : 100,
            }, # 2 frame
            {
                "SSZZ" : 14,
                "SXZZ" : 104,
                "XSZZ" : 152,
                "ZXZZ" : 66,
                "LXRZ" : 82,
            },
            { # 3 frame
                "SSSZZ" : 24,
                "SSXZZ" : 110,
                "SXSZZ" : 156,
                "XSSZZ" : 204,
                "SZXZZ" : 72,
                "SLXRZ" : 88,
                "XZXZZ" : 166,
                "XLXRZ" : 182,
                "ZSXZZ" : 96,
                "LSXRZ" : 120,
                "ZXSZZ" : 72,
                "LXSRZ" : 88,
                "ZXXZZ" : 166,
                "LXXRZ" : 182,
            }, 
            { # 4 frame
                "SSSSZZ" : 36,
                "SSSXZZ" : 118,
                "SSXSZZ" : 162,
                "SXSSZZ" : 208,
                "XSSSZZ" : 256,
                "SSZXZZ" : 80,
                "SSLXRZ" : 96,
                "SZSXZZ" : 102,
                "SXZXLD" : 0, #todo
                "SXLXZD" : 0, #todo
                "XSZXLD" : 0, #todo
                "XSLXZD" : 0, #todo
                "SLSXRZ" : 126,
                "SZXSZZ" : 78,
                "SLXSRZ" : 94,
                "SZXXZZ" : 172,
                "SLXXRZ" : 188,
                "XZSXZZ" : 196, 
                "XLSXRZ" : 220,
                "XZXSZZ" : 172,
                "XLXSRZ" : 188,
                "XZXXZZ" : 266,
                "XLXXRZ" : 282,
                "ZSSXZZ" : 126,
                "LSSXRZ" : 158,
                "ZSXSZZ" : 102,
                "LSXSRZ" : 126,
                "ZSXXZZ" : 196,
                "LSXXRZ" : 220,
                "ZXSSZZ" : 80,
                "LXSSRZ" : 96,
                "ZXSXZZ" : 170,
                "LXSXRZ" : 186,
                "ZXXSZZ" : 218,
                "LXXSRZ" : 234,
                "ZXZXZZ" : 132,
                "LXRXZZ" : 148,
                "LXZXRZ" : 164,
            }
        ]
    },
    "Icecap" : { # single Icecap
        "namelength" : 30,
        "endspace" : 82,
        "manips" : [
            { # 0 frame
                "ZZ" : 0,
            }, 
            { # 1 frame
                "SZZ" : 10,
                "XZZ" : 96,
            }, # 2 frame
            {
                "SSZZ" : 22,
                "SXZZ" : 104,
                "XSZZ" : 148,
                "ZXZZ" : 66,
                "LXRZ" : 82,
            },
            { # 3 frame
                "SSSZZ" : 36,
                "SSXZZ" : 114,
                "SXSZZ" : 156,
                "XSSZZ" : 200,
                "SZXZZ" : 76,
                "SLXRZ" : 92,
                "XZXZZ" : 162,
                "XLXRZ" : 178,
                "ZSXZZ" : 96,
                "LSXRZ" : 120,
                "ZXSZZ" : 72,
                "LXSRZ" : 88,
                "ZXXZZ" : 166,
                "LXXRZ" : 182,
            },
            { # 4 frame
                "SSSSZZ" : 52,
                "SSSXZZ" : 126,
                "SSXSZZ" : 166,
                "SXSSZZ" : 208,
                "XSSSZZ" : 252,
                "SSZXZZ" : 88,
                "SSLXRZ" : 104,
                "SXZXLD" : 0, #todo
                "SXLXZD" : 0, #todo
                "XSZXLD" : 0, #todo
                "XSLXZD" : 0, #todo
                "SZSXZZ" : 106,
                "SLSXRZ" : 130,
                "SZXSZZ" : 82,
                "SLXSRZ" : 98,
                "SZXXZZ" : 176,
                "SLXXRZ" : 292,
                "XZSXZZ" : 292, 
                "XLSXRZ" : 216,
                "XZXSZZ" : 168,
                "XLXSRZ" : 184,
                "XZXXZZ" : 262,
                "XLXXRZ" : 278,
                "ZSSXZZ" : 126,
                "LSSXRZ" : 158,
                "ZSXSZZ" : 102,
                "LSXSRZ" : 126,
                "ZSXXZZ" : 196,
                "LSXXRZ" : 220,
                "ZXSSZZ" : 80,
                "LXSSRZ" : 96,
                "ZXSXZZ" : 170,
                "LXSXRZ" : 186,
                "ZXXSZZ" : 218,
                "LXXSRZ" : 234,
                "ZXZXZZ" : 132,
                "LXRXZZ" : 148,
                "LXZXRZ" : 164,
            }
        ]
    },
    "Aaron_sweating_flee" : { # Woshua, Aaron on the turn Aaron is fled, with flavor text "Aaron is sweating bullets. Literally."
        "namelength" : 38,
        "endspace" : 0,
        "manips" : [
            { # 0 frame
                "LD" : 0,
            }, 
            { # 1 frame
                "SLD" : 6,
                "XLD" : 156,
            }, # 2 frame
            {
                "SSLD" : 14,
                "SXLD" : 160,
                "XSLD" : 236,
                "ZXLD" : 62,
                "LXZD" : 82,
            },
            { # 3 frame
                "SSSLD" : 24,
                "SSXLD" : 166,
                "SXSLD" : 240,
                "XSSLD" : 316,
                "SZXLD" : 68,
                "SLXZD" : 88,
                "XZXLD" : 218,
                "XLXZD" : 238,
                "ZSXLD" : 90,
                "LSXZD" : 120,
                "ZXSLD" : 68,
                "LXSZD" : 88,
                "ZXXLD" : 218,
                "LXXZD" : 238,
            }, 
            { # 4 frame
                "SSSSLD" : 36,
                "SSSXLD" : 174,
                "SSXSLD" : 246,
                "SXSSLD" : 320,
                "XSSSLD" : 396,
                "SSZXLD" : 76,
                "SSLXZD" : 104,
                "SXZXLD" : 222, 
                "SXLXZD" : 242, 
                "XSZXLD" : 298, 
                "XSLXZD" : 318, 
                "SZSXLD" : 96,
                "SLSXZD" : 126,
                "SZXSLD" : 74,
                "SLXSZD" : 94,
                "SZXXLD" : 224,
                "SLXXZD" : 244,
                "XZSXLD" : 246, 
                "XLSXZD" : 276,
                "XZXSLD" : 224,
                "XLXSZD" : 244,
                "XZXXLD" : 374,
                "XLXXZD" : 394,
                "ZSSXLD" : 118,
                "LSSXZD" : 158,
                "ZSXSLD" : 96,
                "LSXSZD" : 126,
                "ZSXXLD" : 246,
                "LSXXZD" : 276,
                "ZXSSLD" : 76,
                "LXSSZD" : 96,
                "ZXSXLD" : 222,
                "LXSXZD" : 242,
                "ZXXSLD" : 298,
                "LXXSZD" : 318,
                "ZXZXLD" : 124,
                "LXRXLD" : 144,
                "LXZXZD" : 164,
            }
        ]
    },
}

def completeManips():
    newmanips = {}
    for name, manipdict in manips.items():
        newmanips[name + "_lvup"] = copy.deepcopy(manipdict)
        newmanips[name + "_lvup"]["endspace"] += 44

    manips.update(newmanips)

    for manipdict in manips.values():
        namelength = manipdict["namelength"]
        endspace = manipdict["endspace"]
        maniplist = manipdict["manips"]
        manipdict["reversemanips"] = {}
        basestr = next(iter(maniplist[0]))
        for i in range(1, 11):
            if i >= len(maniplist):
                maniplist.append({})
            for manip, offset in maniplist[i-1].items():
                # add manip with extra name frame
                if manip[-1] == basestr[-1]:
                    maniplist[i][manip[:-1] + "S" + basestr[-1]] = offset + namelength
                # add manip with space at end
                maniplist[i][manip + "S"] = offset + endspace 
            for manip, offset in maniplist[i].items():
                if offset not in manipdict["reversemanips"]:
                    manipdict["reversemanips"][offset] = manip
completeManips()

cutscenes = {
    "snowdin1_geno" : [16, 82, 66, 110, 40, 10, 66, 60, 10, 114, 122, 62, 122, 36, 92, 58, 64, 96, 96, 146, 96, 10, 74, 72, 14, 36, 42, 46, 88, 90, 82, 72],
    "snowdin1_ngplus": [16, 106, 112, 104, 78, 62, 122, 36, 92, 58, 64, 96, 96, 146, 96, 22, 56, 86, 52, 80, 50, 124, 62, 70, 40, 72, 44, 56, 80, 48, 90, 70, 94, 16, 66, 84, 64, 72, 122, 28, 14, 54, 38, 14, 66, 96, 108, 38, 12, 58, 34, 36, 42, 56, 8, 56, 132, 124, 150, 70, 50, 76, 140, 90],
    "snowdin2_geno" : [74, 52, 66, 68, 62, 48, 76, 40, 60, 18, 24, 78, 82, 24, 54, 50, 28, 70, 50, 26, 94, 62, 98, 62, 24, 66, 84],
}