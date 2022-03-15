import random
import time

import pygame

pygame.init()

WIDTH, HEIGHT = 970, 540

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sorter")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BG_COL = BLACK

font = pygame.font.SysFont("Cabri", 50)
clock = pygame.time.Clock()


def swap(screen, a, b):
    temp = screen.bars[a]
    screen.bars[a] = screen.bars[b]
    screen.bars[b] = temp
    return screen


def step(screen):
    pass


class Screen:
    def __init__(self, pos, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.Surface((width, height))
        self.pos = pos
        random.shuffle((nums := list(range(100))))
        self.bars = [x for x in list(nums)]
        self.green = []
        self.red = []

    def redraw(self):
        self.screen.fill(BLACK)
        pygame.draw.rect(self.screen, (100, 100, 100), pygame.Rect(0, 0, self.width, self.height), 2)

        bar_width = (self.width * 0.95) / len(self.bars)
        bar_gap = bar_width * 0.2
        max_height = self.height * 0.9

        for i, bar in enumerate(self.bars):
            col = WHITE
            if i in self.red: col = RED
            if i in self.green: col = GREEN
            pygame.draw.rect(self.screen, col, ((i*bar_width) + ((self.width * 0.05) / 2), self.height - (max_height / 100 * (bar+1)), bar_width-bar_gap, max_height / 100 * (bar+1)))


class Bubble_Sort(Screen):
    def __init__(self, pos, width, height):
        super().__init__(pos, width, height)
        self.cur_bar = 0
        self.red.append(0)
        self.swaps = 0
        self.final = False

    def step(self):
        self.red = []
        if self.bars[self.cur_bar] > self.bars[self.cur_bar + 1]:
            temp = self.bars[self.cur_bar + 1]
            self.bars[self.cur_bar + 1] = self.bars[self.cur_bar]
            self.bars[self.cur_bar] = temp
            self.red = [self.cur_bar, self.cur_bar + 1]
            self.swaps += 1
        elif self.final:
            self.green.append(self.cur_bar+1)
        self.cur_bar += 1

        if self.cur_bar >= 99:
            if self.swaps == 0:
                self.final = True
                self.cur_bar = 0
            else:
                self.swaps = 0
                self.cur_bar = 0


def split_screens(n: int):
    screens = [Bubble_Sort((0,0), WIDTH, HEIGHT)]
    new_screens = screens
    length = 1
    count = 0
    horizontal = True

    for split in range(n):
        if horizontal:
            new = [Bubble_Sort((screens[count].pos[0], screens[count].pos[1]),
                           screens[count].width, screens[count].height // 2),
                   Bubble_Sort((screens[count].pos[0], (screens[count].height // 2) + (count//2 * screens[count].height)),
                           screens[count].width, screens[count].height // 2)]
        else:
            new = [Bubble_Sort((screens[count].pos[0], screens[count].pos[1]),
                           screens[count].width // 2, screens[count].height),
                   Bubble_Sort(((screens[count].width // 2) + (count//2 * screens[count].width), screens[count].pos[1]),
                           screens[count].width // 2, screens[count].height)]

        new_screens = new_screens[:count*2] + new + new_screens[count*2:]
        del new_screens[(count*2)+2]

        if count < length-1:
            count += 1
        else:
            count = 0
            screens = new_screens
            horizontal = not horizontal
            length *= 2

    return new_screens


def redraw_window(screens):
    for i in screens:
        i.redraw()
        win.blit(i.screen, i.pos)


def main():
    run = True
    screens = split_screens(2)
    while run:
        clock.tick()
        time = clock.get_time()

        # if time % 2 == 0:
        for i in screens: i.step()

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                # elif event.key == pygame.K_SPACE:


        redraw_window(screens)
        pygame.display.update()


if __name__ == "__main__":
    main()
    pygame.quit()