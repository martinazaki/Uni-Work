'''
A simple 1-player dice game
'''

from random import random, seed
from math import ceil

if __name__ == "__main__":
    seed()

    dice = []
    for i in range(0,5):
        dice.append(ceil(random()*6))

    print("Your dice are:")
    for i in range(0,5):
        print(f"{i}: {dice[i]}")

    for i in range(0,2):
        print("Which dice do you want to reroll?")
        reroll = input().split()
        for j in reroll:
            dice[int(j)] = ceil(random()*6)
        print("Your dice are:")
        for j in range(0,5):
            print(f"{j}: {dice[j]}")

    counts = {}
    for d in dice:
        if d in counts:
            counts[d] += 1
        else:
            counts[d] = 1

    if len(counts) == 1:
        print("5 of a kind!")
    elif len(counts) == 2:
        if 4 in counts.values():
            print("4 of a kind!")
        else:
            print("Full house!")
    elif len(counts) == 3:
        if 3 in counts.values():
            print("Three of a kind!")
        else:
            print("Two-pair!")
    elif len(counts) == 4:
        print("Pair!")
    elif 1 not in counts.values() or 6 not in counts.values():
        print("Straight")
