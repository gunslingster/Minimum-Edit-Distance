import pygame as pg
import math
pg.init()

width = 900
height = 900
screen = pg.display.set_mode((width, height))
black = (0,0,0)
white = (255,255,255)
grey = (100,100,100)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
orange = (255,165,0)
fps = 10
clock = pg.time.Clock()

def draw_grid(surface, spacing=20, color=grey):
    for i in range(surface.get_width()):
        pg.draw.line(surface, color, (i*spacing, 0), (i*spacing, surface.get_height()))
    for i in range(surface.get_height()):
        pg.draw.line(surface, color, (0, i*spacing), (surface.get_width(), i*spacing))
        
class Cell():
    def __init__(self, size, pos, content, isnum=False):
        self.size = size
        self.pos = pos
        self.content = content
        self.isnum = isnum
        self.image = pg.Surface((size, size))
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
    
    def draw(self):
        font = pg.font.SysFont('arial', 20)
        text = font.render(str(self.content), True, red)
        self.image.blit(text, (5,0))
        screen.blit(self.image, self.pos)

class Board():
    def __init__(self, surface, cell_size):
        self.cell_size = cell_size
        self.surface = surface
        self.cols = self.surface.get_width() // self.cell_size
        self.rows = self.surface.get_height() // self.cell_size
        self.cells = {}
        self.initialize()
    
    def initialize(self):
        str1 = input('Enter str1: ')
        str2 = input('Enter str2: ')
        self.cells[(0, 1)] = Cell(20, (0, self.cell_size), '#')
        self.cells[(1, 0)] = Cell(20, (self.cell_size, 0), '#')
        self.cells[(1, 1)] = Cell(20, (self.cell_size, self.cell_size), '0', isnum=True)
        for i in range(2, 2 + len(str1)):
            self.cells[(0, i)] = Cell(20, (0, self.cell_size * i), str1[i-2])
            self.cells[(1, i)] = Cell(20, (self.cell_size, self.cell_size * i), i-1, isnum=True)
        for i in range(2, 2 + len(str2)):
            self.cells[(i, 0)] = Cell(20, (self.cell_size * i, 0), str2[i-2])
            self.cells[(i, 1)] = Cell(20, (self.cell_size * i, self.cell_size), i-1, isnum=True)
        for i in range(2, len(str1)+2):
            for j in range(2, len(str2)+2):
                char1 = str1[i-2]
                char2 = str2[j-2]
                cost3_offset = (0 if char1==char2 else 2)
                cost3 = int(self.cells[(j-1,i-1)].content) + cost3_offset
                cost2 = int(self.cells[(j-1, i)].content) + 1
                cost1 = int(self.cells[(j, i-1)].content) + 1   
                min_cost = min(min(cost1, cost2), cost3)
                self.cells[(j, i)] = Cell(20, (j*self.cell_size, i*self.cell_size), min_cost, isnum=True)
        print(f'Minimum edit distance is: {self.cells[(len(str2)+1, len(str1)+1)].content}')
        
    def draw(self):
        for cell in self.cells.values():
            cell.draw()
    
def main():
    running = True
    b = Board(screen, 20)
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        screen.fill(black)
        b.draw()
        draw_grid(screen, color=white)
        pg.display.flip()

main()
pg.quit()
