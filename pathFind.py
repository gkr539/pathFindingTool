import pygame
import math
import queue
import collections
import heapq
#from collections import heapq
WIDTH = 400
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Path Finding Alg")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.nei = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_back(self):
        self.color = YELLOW

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbours(self, grid):
        self.nei = []
        #down
        if self.row + 1 < self.total_rows and not grid[self.row + 1][self.col].is_barrier():
            self.nei.append(grid[self.row + 1][self.col])
        #up
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.nei.append(grid[self.row - 1][self.col])
        #left
        if self.col > 0 and not grid[self.row ][self.col - 1].is_barrier():
            self.nei.append(grid[self.row][self.col - 1])
        #right
        if self.col + 1 < self.total_rows  and not grid[self.row][self.col + 1].is_barrier():
            self.nei.append(grid[self.row][self.col + 1])

    #compare , less than
    def __lt__(self, other):
        return False

def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1-x2) + abs(y1-y2)

def make_grid(rows, width):
    grid = []
    gap = width // rows
    grid = [[Spot(i, j, gap, rows) for j in range(rows) ] for i in range(rows)]
    # for i in range(rows):
    #     grid.append([])
    #     for j in range(rows):
    #         spot = Spot(i, j, gap, rows)
    #         grid[i].append(spot)
    return grid

#grid lines
def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i*gap), (width, i*gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j*gap, 0), (j*gap, width))

def draw(win, grid, rows, width):
    win.fill(WHITE)
    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    #pos[0] is distance from left, pos[1] is distance from top
    gap = width // rows
    y,x = pos
    row = y // gap
    col = x // gap
    return row, col

#it finds shortest path to every node
def dijkstra(draw, grid, start, end):
    heap = []
    distance = {}
    distance[start] = 0
    visited = {}
    came_from = {}

    heapq.heappush(heap, (0,start))
    while heap:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        dis, node = heapq.heappop(heap)
        visited[node] = True
        if node == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return
        for nei in node.nei:
            if nei in visited:
                continue
            newD = distance.get(node,float('inf')) + 1
            if newD < distance.get(nei, float('inf')):
                came_from[nei] = node
                distance[nei] = newD
                heapq.heappush(heap, (newD, nei))
                nei.make_open()
        draw()
        if node != start:
            node.make_closed()
    #reconstruct_path(came_from, end, draw)








def bfsTraversal(draw, grid, start, end):
    pass

def dfsTraversal(draw, grid, start, end):
    visited = set()
    ans = []
    stack = []
    stack.append(start)
    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        draw()
        cur = stack[-1]
        stack.pop()
        if cur == end:
            cur.make_open()
            break
        if cur not in visited:
            ans.append(cur)
            visited.add(cur)
            if cur != start and cur != end:
                cur.make_open()
        for nei in cur.nei:
            if nei not in visited:
                # if nei != start and nei != end:
                #     nei.make_open()
                stack.append(nei)
        #cur.make_closed()
    # for spot in ans:
    #     draw()
    #     if spot != start and spot != end:
    #         spot.make_path()

    end.make_end()
    return


def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()
#it finds shortest path to end node
def aStar(draw, grid, start, end):
    count = 0
    open_set = queue.PriorityQueue()
    #tie breaker if same f score, ==> count
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot : float('inf') for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot : float('inf') for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())
    open_set_hash = {start}
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = open_set.get()[2]
        open_set_hash.remove(current)
        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return
            #make path
        for nei in current.nei:
            temp_g_score = g_score[current] + 1
            if temp_g_score < g_score[nei]:
                came_from[nei] = current
                g_score[nei] = temp_g_score
                f_score[nei] = temp_g_score + h(nei.get_pos(), end.get_pos())
                if nei not in open_set_hash:
                    count +=1
                    open_set.put((f_score[nei], count, nei))
                    open_set_hash.add(nei)
                    nei.make_open()
        draw()
        if current != start:
            current.make_closed()
    return




def main(win,width):
    ROWS = 50
    grid = make_grid(ROWS, width)
    start = None
    end = None
    run = True
    started = False

    while run :
        draw(win,grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            #left mouse
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.make_start()
                elif not end and spot != start:
                    end = spot
                    end.make_end()
                elif spot != end and spot != start:
                    spot.make_barrier()


            #right mouse
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbours(grid)

                    aStar(lambda : draw(win,grid, ROWS, width), grid, start, end)
                elif event.key == pygame.K_d and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbours(grid)
                    dfsTraversal(lambda : draw(win, grid, ROWS, width), grid, start, end)
                elif event.key == pygame.K_k and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbours(grid)
                    dijkstra(lambda : draw(win, grid, ROWS, width), grid, start, end)
                    #dfsTraversal(lambda : draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)


    pygame.quit()


main(WIN, WIDTH)










