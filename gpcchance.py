from fractions import Fraction
from math import prod

f = Fraction

fun = f(6, 100)
whimsuns = f(1, 2)**6
froggitwhimsuns = f(1, 4)**7
frogskips = f(81, 200)**14
blcons = [
    f(1, 10)**7,
    f(3, 10)**5,
    f(5, 10)**2,
    f(7, 10)**2,
    f(9, 10)**0,
]
steps40 = [
    f(1, 80)**1,
    f(3, 80)**3,
    f(5, 80)**0,
    f(7, 80)**0,
    f(9, 80)**0,
    f(11, 80)**1,
    f(45, 80)**1,
]
steps60 = [
    f(1, 120)**2,
    f(3, 120)**4,
    f(5, 120)**0,
    f(7, 120)**1,
    f(9, 120)**0,
]

ruins = fun * whimsuns * frogskips * prod(blcons) * prod(steps40) * prod(steps60)

print(f"Ruins chance: {float(ruins)} ({ruins})")

icecaps = f(7, 15)**6 * f(17, 30)
iceattacks = f(99, 200)**1
dogskips = f(101, 200)**2
blcons = [
    f(1, 10)**8,
    f(3, 10)**4,
    f(5, 10)**0,
    f(7, 10)**1,
    f(9, 10)**2,
]
steps30 = [
    f(1, 60)**9,
    f(3, 60)**0,
    f(5, 60)**2,
    f(7, 60)**1,
    f(9, 60)**0,
    f(11, 60)**0,
]
steps280 = [
    f(1, 560)**2,
    f(3, 560)**1,
    f(4, 560)**3,
    f(5, 560)**0,
    f(7, 560)**1,
    f(9, 560)**1,
    f(11, 560)**0,
    f(13, 560)**1,
]
petalslongsteps = f(5, 760)**1
bones = [
    f(1, 40)**0,
    f(3, 40)**4,
    f(5, 40)**2,
    f(7, 40)**2,
    f(9, 40)**1,
    f(11, 40)**0,
    f(13, 40)**2,
    f(29, 40)**1,
]

snowdin = icecaps * iceattacks * dogskips * prod(blcons) * prod(steps30) * prod(steps280) * petalslongsteps * prod(bones)

print(f"Snowdin up to Punch Card chance: {float(snowdin)} ({snowdin})")

icecaps = f(7, 15)
triple = f(13, 30)
iceattacks = f(99, 200)**2
moldsmals = f(4, 15)**3
gameover = f(1, 5)
blcons = [
    f(1, 10)**2,
    f(3, 10)**0,
    f(5, 10)**0,
    f(7, 10)**0,
    f(9, 10)**0,
]
steps30 = [
    f(1, 60)**1,
    f(3, 60)**0,
    f(5, 60)**0,
    f(7, 60)**0,
    f(9, 60)**0,
    f(11, 60)**0,
]