import math

DEFAULT_COLOR = "white"


class Scircle:
    def __init__(self, name, canvas, x=0, y=0, r=15, color=DEFAULT_COLOR):
        self.name = name
        self.canvas = canvas
        self.x = x
        self.y = y
        self.r = r
        self.color = color
        outline = "black" if color == DEFAULT_COLOR else ""
        self.circle = canvas.create_oval(x - r, y - r, x + r, y + r, fill=color, outline=outline)
        self.edges = []

    def update_pos(self, x, y):
        self.canvas.move(self.circle, x - self.x, y - self.y)
        self.x = x
        self.y = y
        self.update_edges()

    def print_info(self):
        print(f"{self.name} @ ({self.x},{self.y})")

    def contains(self, x, y):
        x_diff = self.x - x
        y_diff = self.y - y
        return math.sqrt(x_diff * x_diff + y_diff * y_diff) <= self.r

    def add_edge(self, edge):
        self.edges.append(edge)

    def update_edges(self):
        for edge in self.edges:
            edge.update()

    def change_color(self, color):
        self.color = color
        self.canvas.itemconfig(self.circle, fill=color)
        self.canvas.itemconfig(self.circle, outline="black" if color == DEFAULT_COLOR else "")

    def reset_color(self):
        self.change_color(DEFAULT_COLOR)

    def highlight_outline(self):
        self.canvas.itemconfig(self.circle, outline="black", width=5)

    def reset_outline(self):
        self.change_color(self.color)


class Edge:
    def __init__(self, name, canvas, c1, c2):
        self.name = name
        self.canvas = canvas
        self.c1 = c1
        self.c2 = c2
        c1.add_edge(self)
        c2.add_edge(self)
        self.create_line()

    def create_line(self):
        self.line = self.canvas.create_line(self.c1.x, self.c1.y, self.c2.x, self.c2.y)

    def update(self):
        self.canvas.coords(self.line, self.c1.x, self.c1.y, self.c2.x, self.c2.y)

    def intersects(self, edge):
        slope1 = (self.c2.y - self.c1.y) / (self.c2.x - self.c1.x)
        slope2 = (edge.c2.y - edge.c1.y) / (edge.c2.x - edge.c1.x)

        f1 = lambda x: slope1 * (x - self.c1.x) + self.c1.y
        f2 = lambda x: slope2 * (x - edge.c1.x) + edge.c1.y

        start1 = min(self.c1.x + 1, self.c2.x + 1)
        start2 = min(edge.c1.x + 1, edge.c2.x + 1)
        end1 = max(self.c1.x, self.c2.x)
        end2 = max(edge.c1.x, edge.c2.x)

        interval = (max(start1, start2), min(end1, end2))

        for x in range(*interval):
            if f1(x) == f2(x):
                return True

        return False
