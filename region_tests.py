from kabanos_engine import engine
import pygame as pg

from tkinter import *
from tkinter import ttk

from colorama import Fore, Style

# dungeon settings preset
settings = {
    "width":50,
    "height":50,
    "birthChance":60,
    "deathLimit":3,
    "birthLimit":4,
    "steps":11
}

# global variables 
global width, height, birthChance, birthLimit, deathLimit, steps, generated_level
generated_level = []

# engine functions
def display_cave():
    global generated_level
    gen = engine.Cave_Generator(settings["width"],settings["height"],settings["birthChance"],settings["birthLimit"],settings["deathLimit"],int(settings["steps"]))
    generated_level, starting_point = gen.generate_cave()

    for indexx, x in enumerate(generated_level):
        collumn = ""
        for indexy, y in enumerate(x):
            if indexx == starting_point[0] and indexy == starting_point[1]:
                collumn += Fore.GREEN + "█" + Style.RESET_ALL
            elif y == 1: 
                collumn += Fore.YELLOW + str(y) + Style.RESET_ALL
            else:
                collumn += Fore.BLACK + str(y) + Style.RESET_ALL
        print(collumn)

def GetRegion(startx, starty):
    tiles = []

    for x in range(3):
        for y in range(3):
            pass

    return tiles

def print_regions():
    global generated_level

    listRegions = []
    mapRegions = []
    queue = []

    for x in generated_level:
        empty_list = []
        for y in x:
            empty_list.append(0)
        mapRegions.append(empty_list)


    for indexx, x in enumerate(generated_level):
        for indexy, y in enumerate(x):
            if mapRegions[indexx][indexy] == 0 and generated_level[indexx][indexy] == 0:
                newRegion = GetRegion(indexx, indexy)
                listRegions.append(newRegion)

                for value in newRegion:
                    mapRegions[indexx][indexy] == 1

    for indexx, x in enumerate(generated_level):
        collumn = ""
        for indexy, y in enumerate(x):
            if y == 1: 
                collumn += Fore.YELLOW + str(y) + Style.RESET_ALL
            else:
                collumn += Fore.BLACK + str(y) + Style.RESET_ALL
        print(collumn)

# tkinter
root = Tk()
root.title("Region assingment tests")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N,W,E,S))
mainframe.columnconfigure(0, weight=1)

ttk.Button(mainframe, text="Generate Dungeon", command=display_cave).grid(column=0, row=0, sticky=(W,E))
ttk.Button(mainframe, text="Assing Regions", command=print_regions).grid(column=1, row=0, sticky=(W,E))

root.mainloop()