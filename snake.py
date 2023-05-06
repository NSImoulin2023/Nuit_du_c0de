# cobac
# avril 2023

import pyxel
import random


class Snake:

    directions = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]

    def __init__(self, dim):
        self.dim = dim
        self.spt = Serpent(dim)
        self.nrt = Nourriture(dim)
        self.score = 0
        self.jeu = True
        pyxel.init(dim, dim)
        pyxel.load("res.pyxres")
        pyxel.run(self.update, self.draw)

    def draw(self):
        pyxel.cls(0)
        if self.jeu:
            self.nrt.place()
            self.spt.dessine()
            pyxel.text(0, 0, "Score : " + str(self.score), 7)
        else:
            pyxel.text(self.dim / 2 - 20, self.dim / 2 - 3,
                       "GAME OVER " + str(self.score), 7)

    def update(self):
        if pyxel.btn(pyxel.KEY_RIGHT):
            dir = 1
        elif pyxel.btn(pyxel.KEY_LEFT):
            dir = 2
        elif pyxel.btn(pyxel.KEY_UP):
            dir = 4
        elif pyxel.btn(pyxel.KEY_DOWN):
            dir = 3
        else:
            dir = 0

        if self.spt.est_sur_nourriture(self.nrt):
            self.score += 1
            self.nrt = Nourriture(self.dim)
            self.spt.update_position(Snake.directions[dir], False)
        else:
            self.spt.update_position(Snake.directions[dir])

        if not self.spt.est_valide():
            self.jeu = False

        if not self.jeu and pyxel.btn(pyxel.KEY_N):
            self.jeu = True
            self.score = 0
            self.spt = Serpent(self.dim)
            self.nrt = Nourriture(self.dim)


class Nourriture:
    def __init__(self, dim):
        self.x = random.randrange(0, dim - 3)
        self.y = random.randrange(0, dim - 3)
        self.coords = (self.x + 1, self.y + 1)

    def place(self):
        pyxel.blt(self.x, self.y, 0, 0, 3, 3, 3)


class Serpent:
    def __init__(self, dim):
        self.x = random.randrange(10, dim - 10)
        self.y = random.randrange(10, dim - 10)
        self.dim = dim
        self.coords = [(self.x, self.y)]
        self.dir = (1, 0)

    def est_sur_nourriture(self, n):
        return self.coords[0][0] <= n.coords[0] <= self.coords[0][0] + 2 \
            and self.coords[0][1] <= n.coords[1] <= self.coords[0][1] + 2

    def update_position(self, dir, enleve_queue=True):
        if dir != (0, 0):
            self.dir = dir

        self.x += self.dir[0]
        self.y += self.dir[1]
        self.coords.insert(0, (self.x, self.y))
        if enleve_queue:
            self.coords.pop()

    def est_valide(self):
        if self.coords[0] in self.coords[1:]:
            return False
        if self.coords[0][0] < 0 or self.coords[0][0] > self.dim - 3:
            return False
        if self.coords[0][1] < 0 or self.coords[0][1] > self.dim - 3:
            return False
        return True

    def dessine(self):
        for x, y in self.coords:
            pyxel.blt(x, y, 0, 0, 0, 3, 3)


Snake(128)
