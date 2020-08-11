import sys
import pygame as pg

from tkinter import *
from tkinter import ttk

sys.path.append('/kabanos_engine')
from kabanos_engine import engine

pg.init()

WIDTH = int(input("Szerokosc:"))
HEIGHT = int(input("Wysokosc:"))
PLACING_MODE = False
CURRENT_SETTINGS = None
FONT = pg.font.SysFont("Arial", 25,bold=False,italic=False)
COLOR_BUTTON = None
ALL_COLOR_BUTTONS = []

clock = pg.time.Clock()
allSprites = pg.sprite.Group()

screen = pg.display.set_mode((WIDTH,HEIGHT))
pg.display.set_caption("Button generator")

def draw_new_button():
    global COLOR_BUTTON
    mouse_pos = pg.mouse.get_pos()
    pos_x = 0
    pos_y = 0
    
    if CURRENT_SETTINGS[4]:
        pos_x = WIDTH/2
    else:
        pos_x = mouse_pos[0]
    if CURRENT_SETTINGS[5]:
        pos_y = HEIGHT/2
    else:
        pos_y = mouse_pos[1]

    pos_x = pos_x - int(CURRENT_SETTINGS[0]/2)
    pos_y = pos_y - int(CURRENT_SETTINGS[1]/2)

    b = engine.Color_Button(pos_x, pos_y, CURRENT_SETTINGS[0], CURRENT_SETTINGS[1],CURRENT_SETTINGS[2],CURRENT_SETTINGS[3],CURRENT_SETTINGS[6],CURRENT_SETTINGS[7],CURRENT_SETTINGS[8], FONT)
    COLOR_BUTTON = b

def new_button():
    root = Tk()
    root.title("Nowy przycisk")

    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    mainframe.columnconfigure(0, weight=1)

    width = StringVar()
    height = StringVar()
    color = StringVar()
    text = StringVar()
    text_x = StringVar()
    text_y = StringVar()
    value = StringVar()

    center_width = IntVar()
    center_height = IntVar()
    no_value = IntVar()

    ttk.Label(mainframe, text="Szerokość").grid(column=0, row=0, sticky=W)
    ttk.Label(mainframe, text="Wysokość").grid(column=0, row=1, sticky=W)
    ttk.Label(mainframe, text="Kolor").grid(column=0, row=2, sticky=W)
    ttk.Label(mainframe, text="Tekst").grid(column=0, row=3, sticky=W)
    ttk.Label(mainframe, text="Tekst-x").grid(column=0, row=4, sticky=W)
    ttk.Label(mainframe, text="Tekst-y").grid(column=0, row=5, sticky=W)
    ttk.Label(mainframe, text="Wartość").grid(column=0, row=6, sticky=W)

    width_entry = ttk.Entry(mainframe, width=6, textvariable=width)
    width_entry.grid(column=1, row=0, sticky=(W,E))

    height_entry = ttk.Entry(mainframe, width=6, textvariable=height)
    height_entry.grid(column=1, row=1, sticky=(W,E))

    color_entry = ttk.Entry(mainframe, width=6, textvariable=color)
    color_entry.grid(column=1, row=2, sticky=(W,E))

    text_entry = ttk.Entry(mainframe, width=6, textvariable=text)
    text_entry.grid(column=1, row=3, sticky=(W,E))

    text_x_entry = ttk.Entry(mainframe, width=6, textvariable=text_x)
    text_x_entry.grid(column=1, row=4, sticky=(W,E))

    text_y_entry = ttk.Entry(mainframe, width=6, textvariable=text_y)
    text_y_entry.grid(column=1, row=5, sticky=(W,E))

    value_entry = ttk.Entry(mainframe, width=6, textvariable=value)
    value_entry.grid(column=1, row=6, sticky=(W,E))

    def update_entries():
        if no_value.get() == 0:
            value_entry.config(state='enabled')
        elif no_value.get() == 1:
            value_entry.config(state='disabled')

    def set_value(entry,text):
        entry.delete(0, END)
        entry.insert(0, text)
        return

    def update_values():
        set_value(width_entry,CURRENT_SETTINGS[0])
        set_value(height_entry,CURRENT_SETTINGS[1])
        set_value(text_entry,CURRENT_SETTINGS[3])
        set_value(text_x_entry,CURRENT_SETTINGS[6])
        set_value(text_y_entry,CURRENT_SETTINGS[7])
        set_value(value_entry,CURRENT_SETTINGS[8])

    center_width_entry = Checkbutton(mainframe, text="Wyśrodkuj wysokość", variable=center_width, onvalue=1, offvalue=0)
    center_width_entry.grid(column=0, row=7, sticky=W)
    center_height_entry = Checkbutton(mainframe, text="Wyśrodkuj szerokość", variable=center_height, onvalue=1, offvalue=0)
    center_height_entry.grid(column=0, row=8, sticky=W)
    
    no_value_entry = Checkbutton(mainframe, text="Brak wartości", variable=no_value, onvalue=1, offvalue=0, command=update_entries)
    no_value_entry.grid(column=0, row=9, sticky=W)

    ttk.Button(mainframe, text="Gotowe", command=root.destroy).grid(column=1, row=10, sticky=(W,E))

    if CURRENT_SETTINGS != None:
        update_values()

    for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)
    
    root.mainloop()
    value1 = 0
    if value.get() != '':
        value1 = value.get()

    if color.get() == '':
        return int(width.get()), int(height.get()), (13, 181, 46), text.get(), center_width.get(), center_height.get(), int(text_x.get()), int(text_y.get()), int(value1)
    else:
        color_rgb = (13, 181, 46)
        if color.get() == 'BLUE':
            color_rgb = (24, 125, 201)
        elif color.get() == 'RED':
            color_rgb = (191, 8, 8)
        return int(width.get()), int(height.get()), color_rgb, text.get(), center_width.get(), center_height.get(), int(text_x.get()), int(text_y.get()), int(value1)
    # width, height, color, text, center_width, center_height, text_x, text_y, value
    
def log_positions():
    COLOR_BUTTONS = []
    for button in ALL_COLOR_BUTTONS:
        COLOR_BUTTONS.append([button.width, button.height, button.color, button.text, button.pos_x, button.pos_y, button.label_x, button.label_y, button.value])

    print('\n'*20)
    print("--- COLOR BUTTONS ---")
    for setting in COLOR_BUTTONS:
        print(setting)
    print("-"*21)

while True:
    screen.fill((0,0,0))
    allSprites = pg.sprite.Group()

    if PLACING_MODE:
        draw_new_button()
    else:
        COLOR_BUTTON = None

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            log_positions()
            sys.exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_1:
                CURRENT_SETTINGS = new_button()
                PLACING_MODE = True
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if CURRENT_SETTINGS != None:
                    mouse_pos = pg.mouse.get_pos()

                    pos_x = 0
                    pos_y = 0
                    
                    if CURRENT_SETTINGS[4]:
                        pos_x = WIDTH/2
                    else:
                        pos_x = mouse_pos[0]
                    if CURRENT_SETTINGS[5]:
                        pos_y = HEIGHT/2
                    else:
                        pos_y = mouse_pos[1]

                    pos_x = pos_x - int(CURRENT_SETTINGS[0]/2)
                    pos_y = pos_y - int(CURRENT_SETTINGS[1]/2)

                    PLACING_MODE = False
                    ALL_COLOR_BUTTONS.append(engine.Color_Button(pos_x, pos_y, CURRENT_SETTINGS[0], CURRENT_SETTINGS[1],CURRENT_SETTINGS[2],CURRENT_SETTINGS[3],CURRENT_SETTINGS[6],CURRENT_SETTINGS[7],CURRENT_SETTINGS[8], FONT))

        if COLOR_BUTTON != None:
            COLOR_BUTTON.update(screen)
        for button in ALL_COLOR_BUTTONS:
            button.update(screen) # there would be a return value check in a normal use
        clock.tick(60)
        pg.display.flip()