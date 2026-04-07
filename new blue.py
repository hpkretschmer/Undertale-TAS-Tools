import sys, os, math

with open(os.path.join(sys.path[0], "listofrands1.txt"), "r") as rngstr:
    rng = rngstr.readlines()
    for i in range(len(rng)):
        rng[i] = round(20*float(rng[i])) + 5
    rng.pop(0)
    rng.pop(0)
    rng.pop(0)


times = [[], [], [], []]
for j in range(4):
    for i4th in range(math.floor(len(rng)/4)):
        times[j].append(rng[(4*i4th) + j])

bests = []
with open(os.path.join(sys.path[0], "bests.txt"), "w") as f:
    for j in range(4):
        f.write(f"j = {j}\n")
        best = [-1, -1, -1, 1000000]
        for i4th in range(len(times[j]) - 200):
            turntimer = 316
            i = i4th
            sum = 0
            length = 0
            going = True
            vals = []
            while going:
                vals.append(times[j][i])
                if turntimer >= 600 + times[j][i]:
                    going = False
                turntimer += 37 - times[j][i]
                i += 1
                sum += times[j][i]
                length += 1
            if sum < best[3]:
                best = [j, i*4 + j - 4*length, length, sum]
                bestvals = vals
                f.write(f"   sum = {sum}   len = {length}   i = {j + 4*(i - length)}\n      {vals}\n")
        bests.append([best, bestvals])
for j in bests:
    for part in j:
        print(part)
