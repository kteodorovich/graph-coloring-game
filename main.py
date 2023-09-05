import tkinter as tk
from tkinter import messagebox

from graphs import *

WIDTH = 600
HEIGHT = 600


def make_color_palette(canvas):
    global c_color
    names = ["red", "yellow", "green", "blue"]
    colors = []
    for i, name in enumerate(names):
        colors.append(Scircle(name, canvas, 25 + 50 * i, 25, color=name))

    if c_color is None:
        c_color = names[0]
    for color in colors:
        if color.name == c_color:
            color.highlight_outline()

    return colors


# event handlers
def click(event):
    global selected, nodes, colors, c_color
    for node in nodes:
        if node.contains(event.x, event.y):
            selected = node
            return
    selected = None

    new_color = False
    for color in colors:
        if color.contains(event.x, event.y):
            new_color = True
            c_color = color.name
            print(f"selected color: {c_color}")
            break

    if new_color:
        for color in colors:
            if color.name == c_color:
                color.highlight_outline()
            else:
                color.reset_outline()


def change_color(event):
    for node in nodes:
        if node.contains(event.x, event.y):
            if node.color != c_color:
                node.change_color(c_color)
            else:
                node.change_color(DEFAULT_COLOR)
            return


def release_mouse(event):
    global selected
    selected = None


def move_mouse(event):
    global selected
    if selected is not None:
        selected.update_pos(event.x, event.y)


def on_space(event):
    global nodes, edges, selected, colors
    canvas.delete("all")
    n = random.randint(3, 10)
    nodes, edges = generate_random_graph(canvas, n)
    selected = nodes[0]
    colors = make_color_palette(canvas)


def check_coloring():
    global edges
    good = colored_properly(edges)
    msg = "GOOD" if good else "BAD"
    messagebox.showinfo(title="Check Coloring", message=msg)
    canvas.focus_set()


def reset_colors():
    global nodes
    for node in nodes:
        node.reset_color()
    canvas.focus_set()


def check_layout():
    global edges

    good = True
    for i, e1 in enumerate(edges):
        for e2 in edges[i + 1:]:
            if e1.intersects(e2):
                print(f"{e1.name} intersects {e2.name}!")
                good = False
                break

    msg = "GOOD" if good else "BAD"
    messagebox.showinfo(title="Check Layout", message=msg)
    canvas.focus_set()


# make window
win = tk.Tk()
win.geometry(f"{WIDTH}x{HEIGHT}")

button_panel = tk.PanedWindow()
button_panel.pack(fill="x")

b1 = tk.Button(button_panel, text="Check coloring", command=check_coloring)
b1.pack(side=tk.RIGHT)

b3 = tk.Button(button_panel, text="Check layout", command=check_layout)
b3.pack(side=tk.RIGHT)

b2 = tk.Button(button_panel, text="Reset colors", command=reset_colors)
b2.pack(side=tk.RIGHT)

text = "Welcome to Scircle!\n--> Right-click to color\n--> SPACE to get a new graph"
textbox = tk.Label(button_panel, wraplength=250, justify=tk.LEFT, text=text)
textbox.pack(side=tk.LEFT)

canvas = tk.Canvas(win, width=WIDTH, height=HEIGHT)
canvas.pack(fill=tk.BOTH, expand=True)  # configure canvas to occupy the whole main window
canvas.update()

# make graph
n = random.randint(3, 10)
nodes, edges = generate_random_graph(canvas, n)
selected = nodes[0]

# make color palette
c_color = None
colors = make_color_palette(canvas)

# mouse event handler
canvas.focus_set()
canvas.bind("<Button-1>", click)
canvas.bind("<Button-2>", change_color)
canvas.bind("<B1-Motion>", move_mouse)
canvas.bind("<ButtonRelease-1>", release_mouse)
canvas.bind("<space>", on_space)
canvas.bind("<Return>", check_coloring)

# main loop
win.mainloop()
