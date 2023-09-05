from shapes import *
import random

EDGE_PROB = 0.3


def random_arr(n):
    if n <= 0:
        return []
    if n == 1:
        return [1]

    arr = [1] + [random.randint(0, 1) for _ in range(n - 1)]
    random.shuffle(arr)
    return arr


# make circles
def generate_random_graph(canvas, n, edge_prob=EDGE_PROB):
    circles = []
    edges = []

    center_x = canvas.winfo_width() / 2
    center_y = canvas.winfo_height() / 2
    rad = min(canvas.winfo_width(), canvas.winfo_height()) / 3

    deg = 2 * math.pi / n
    offset = random.random() * 2 * math.pi

    for i in range(n):
        circles.append(Scircle(i, canvas, int(center_x + rad * math.cos(offset + deg * i)),
                               int(center_y + rad * math.sin(offset + deg * i)), color="white"))

        edge_idx_arr = random_arr(i)
        for j, draw in enumerate(edge_idx_arr):
            # randomly add edges
            if draw != 0:
                edges.append(Edge(i, canvas, circles[j], circles[i]))

    for circle in circles:
        circle.canvas.tkraise(circle.circle)

    return circles, edges


def colored_properly(edges):
    for edge in edges:
        if edge.c1.color == edge.c2.color:
            print(f"{edge.c1.name} same color as {edge.c2.name}")
            return False

    return True
