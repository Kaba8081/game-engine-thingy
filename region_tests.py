from kabanos_engine import engine
import pygame as pg

from tkinter import *
from tkinter import ttk

from colorama import Fore, Style

# global variables 
global width, height, birthChance, birthLimit, deathLimit, steps, generated_level, settings, regionColors

# dungeon settings preset
settings = {
    "width":70,
    "height":70,
    "birthChance":60,
    "deathLimit":3,
    "birthLimit":4,
    "steps":11
}

generated_level = []

regionColors = [Fore.RED, Fore.BLUE, Fore.GREEN, Fore.MAGENTA, Fore.CYAN, Fore.WHITE]

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

def GetRegion(startx, starty, d_map, generator_settings):
    def check_neighbours(startx, starty, d_map, queue, done, generator_settings):
        for x in range(3):
            for y in range(3):
                if x == 1 and y == 1:
                    pass
                elif startx+(x-1) > generator_settings["width"] or startx+(x-1) < 0:
                    print("szerkosc")
                elif starty+(y-1) > generator_settings["height"] or starty+(y-1) < 0:
                    print("wysokosc")
                elif d_map[startx+(x-1)][starty+(y-1)] == 0:
                    if (startx+(x-1),starty+(y-1)) not in queue and (startx+(x-1),starty+(y-1)) not in done:
                        queue.append((startx+(x-1),starty+(y-1)))
        return queue

    queue = []
    done = []

    queue = [(startx,starty)]
    while len(queue) > 0:
        queue = check_neighbours(queue[0][0], queue[0][1], d_map, queue, done, generator_settings)
        done.append(queue.pop(0))

    return done

def print_regions():
    global generated_level, settings

    listRegions = []
    mapRegions = []

    for x in generated_level:
        empty_list = []
        for y in x:
            empty_list.append(0)
        mapRegions.append(empty_list)


    for indexx, x in enumerate(generated_level):
        for indexy, y in enumerate(x):
            if mapRegions[indexx][indexy] == 0 and generated_level[indexx][indexy] == 0:
                newRegion = GetRegion(indexx, indexy, generated_level, settings)
                listRegions.append(newRegion)

                for index, value in enumerate(newRegion):
                    mapRegions[newRegion[index][0]][newRegion[index][1]] = 1

    for indexx, x in enumerate(generated_level):
        collumn = ""
        for indexy, y in enumerate(x):
            if y == 1: 
                collumn += Fore.YELLOW + str(y) + Style.RESET_ALL
            elif y == 0 and mapRegions[indexx][indexy] == 1:
                for index, region in enumerate(listRegions):
                    for tile in region:
                        if indexx == tile[0] and indexy == tile[1]:
                            collumn += regionColors[index%len(regionColors)] + str(y) + Style.RESET_ALL
            elif y == 0:
                collumn += Fore.RED + str(y) + Style.RESET_ALL
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