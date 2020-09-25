import pyautogui as pg
import time
import random

"""
fbcomment.py ver. 20.09.26 by mariafshan
This program automatically tag people on Facebook. Please don't use this program to spam people, I wrote this primarily
to ease my workload at managing Facebook communities.

HOW TO USE:
1. Input the text file containing the list of names separated by \n
2. Click the textbox you would like to write comment in

Auto Comment On Any Facebook Post With Just 10 Lines Of Python Script (Unlimited)
https://www.youtube.com/watch?v=yokcJBSMySQ
"""

def main():
    # Click the textbox you would like to write comment in
    time.sleep(2)
    names = []

    # tag people
    filename = input()
    with open(filename) as file:
        for line in file:
            line = line.rsplit("\n")
            names.append(line[0])

    # pg.typewrite("@" + names[0])

    # for i in range(1):
    #     pg.typewrite("@" + names[i])

    for name in names:
        seconds = random.randint(1, 5)
        pg.typewrite("@" + name + " ")
        time.sleep(seconds)
        pg.typewrite("\n" + " ")
    file.close()
    return

if __name__ == '__main__':
    main()
