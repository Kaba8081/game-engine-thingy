from kabanos_engine import engine

from tkinter import *
from tkinter import ttk

from colorama import Fore, Style

global width, height, birthChance, birthLimit, deathLimit, steps

# x,y, 60, 4, 3, 20

# engine init
def display_cave():
    gen = engine.Cave_Generator(width.get(),height.get(),birthChance.get(),birthLimit.get(),deathLimit.get(),int(steps.get()))
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

# tkinter 
root = Tk()
root.title("Generator jaskin")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)

mainframe.columnconfigure(0, pad=8)
mainframe.columnconfigure(1, pad=8)
mainframe.columnconfigure(2, pad=8)
mainframe.columnconfigure(3, pad=8)
mainframe.columnconfigure(4, pad=8)
mainframe.columnconfigure(5, pad=8)
mainframe.columnconfigure(6, pad=8)

number_of_steps = StringVar()

width = Scale(mainframe, from_=150, to=0)
width.set(50)
width.grid(column=0, row=1, sticky=W+E)

height = Scale(mainframe, from_=150, to=0)
height.set(50)
height.grid(column=1, row=1, sticky=W+E)

birthChance = Scale(mainframe, from_=100, to=0)
birthChance.set(60)
birthChance.grid(column=2, row=1, sticky=W+E)

deathLimit = Scale(mainframe, from_=10, to=0)
deathLimit.set(3)
deathLimit.grid(column=3, row=1, sticky=W+E)

birthLimit = Scale(mainframe, from_=10, to=0)
birthLimit.set(4)
birthLimit.grid(column=4, row=1, sticky=W+E)

steps = ttk.Entry(mainframe, width=6, textvariable=number_of_steps)
steps.grid(column=5, row=1, sticky=(W,E))

ttk.Label(mainframe, text="Szerokość").grid(column=0, row=0, sticky=N)
ttk.Label(mainframe, text="Wysokość").grid(column=1, row=0, sticky=N)
ttk.Label(mainframe, text="Szansa").grid(column=2, row=0, sticky=N)
ttk.Label(mainframe, text="d_limit").grid(column=3, row=0, sticky=N)
ttk.Label(mainframe, text="n_limit").grid(column=4, row=0, sticky=N)
ttk.Label(mainframe, text="Kroki").grid(column=5, row=0, sticky=N)
ttk.Button(mainframe, text="Gotowe", command=display_cave).grid(column=6, row=3, sticky=(W,E))

root.mainloop()
