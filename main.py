import random
import time

import pygame

pygame.init()

WIDTH, HEIGHT = 500, 500

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sorter")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

font = pygame.font.SysFont("Cabri", 50)
clock = pygame.time.Clock()


class Screen:
    def __init__(self, pos, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.Surface((width, height))
        self.pos = pos

    def redraw(self):
        pass


def split_screens(n: int):
    screens = [Screen((0,0), WIDTH, HEIGHT)]
    new_screens = screens
    length = 1
    count = 0
    horizontal = True

    for split in range(n):
        if horizontal:
            new = [Screen((screens[count].pos[0], screens[count].pos[1]),
                           screens[count].width, screens[count].height // 2),
                   Screen((screens[count].pos[0], (screens[count].height // 2) + (count//2 * screens[count].height)),
                           screens[count].width, screens[count].height // 2)]
        else:
            new = [Screen((screens[count].pos[0], screens[count].pos[1]),
                           screens[count].width // 2, screens[count].height),
                   Screen(((screens[count].width // 2) + (count//2 * screens[count].width), screens[count].pos[1]),
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


def redraw_window():
    pass


def main():
    run = True
    while run:
        clock.tick()

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

        redraw_window()
        pygame.display.update()


if __name__ == "__main__":
    splits = 0
    while True:
        screens = split_screens(splits)
        print(len(screens), splits)
        splits += 1
        for i in screens:
            # print(i.pos, i.width, i.height)
            pygame.draw.rect(win, (random.randint(0,255), random.randint(0,255), random.randint(0,255)), (i.pos[0],i.pos[1],i.width,i.height))
            pygame.display.update()
        time.sleep(1)

    pygame.quit()