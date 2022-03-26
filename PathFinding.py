import sys
import random
from collections import deque
from sympy.combinatorics.permutations import Permutation

sys.setrecursionlimit(100000)


def afficher(liste):
    i = 0
    while i < n:
        j = 0
        while j < n:
            print(liste[n * i + j], end=' ')
            j += 1
        print('')
        i += 1
    print("----------------------")


def solvable(state):
    permutation_parity = Permutation(state.statelist).signature()
    pos = state.getpos(0)
    d = pos.x + pos.y
    empty_parity = 1 if (d % 2 == 0) else -1
    return empty_parity == permutation_parity


class Vector:
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y


class State:
    statelist = []
    f = 0
    g = 0
    h = 0

    def __init__(self, initialstate):
        self.statelist = initialstate

    def getpos(self, d):
        i = 0
        while i < n:
            j = 0
            while j < n:
                if self.statelist[n * i + j] == d:
                    return Vector(i, j)
                j += 1
            i += 1
        return Vector(-1, -1)

    def down(self):
        LC = self.statelist[:]
        empty = self.getpos(0)
        LC[empty.x * n + empty.y] = LC[(empty.x + 1) * n + empty.y]
        LC[(empty.x + 1) * n + empty.y] = 0
        return LC

    def up(self):
        LC = self.statelist[:]
        empty = self.getpos(0)
        LC[empty.x * n + empty.y] = LC[(empty.x - 1) * n + empty.y]
        LC[(empty.x - 1) * n + empty.y] = 0
        return LC

    def left(self):
        LC = self.statelist[:]
        empty = self.getpos(0)
        LC[empty.x * n + empty.y] = LC[empty.x * n + empty.y - 1]
        LC[empty.x * n + empty.y - 1] = 0
        return LC

    def right(self):
        LC = self.statelist[:]
        empty = self.getpos(0)
        LC[empty.x * n + empty.y] = LC[empty.x * n + empty.y + 1]
        LC[empty.x * n + empty.y + 1] = 0
        return LC


class GameNode:

    def __init__(self, L):

        self.state = State(L)
        self.generatechildnodes()

    def generatechildnodes(self):
        self.children = []
        if self.state.getpos(0).x == n - 1:
            self.children.append(State(self.state.up()))
        elif self.state.getpos(0).x == 0:
            self.children.append(State(self.state.down()))
        else:
            self.children.append(State(self.state.down()))
            self.children.append(State(self.state.up()))

        if self.state.getpos(0).y == n - 1:
            self.children.append(State(self.state.left()))
        elif self.state.getpos(0).y == 0:
            self.children.append(State(self.state.right()))
        else:
            self.children.append(State(self.state.left()))
            self.children.append(State(self.state.right()))


class Profondeur:
    def __init__(self):
        self.nb = 0
        self.found=False

    def resolve(self, state, visited):
        afficher(state.statelist)
        self.nb += 1
        if state.statelist == final.statelist:
            print('Nombre de noeuds visité par profondeur est ', str(self.nb))
            self.found=True
            return
        else:
            if state.statelist not in visited:
                visited.append(state.statelist)
                node = GameNode(state.statelist)
                for st in node.children:
                    self.resolve(st,visited)
                    if self.found:
                        return


def Largeur(stateini):
    visited = []
    current = []
    nb = 0
    visited.append(stateini.statelist)
    current.append(stateini.statelist)
    while current:
        state = current.pop(0)
        nb += 1
        afficher(state)
        if state == final.statelist:
            print('Nombre de noeuds visité par largeur est ', str(nb))
            return state
        node = GameNode(state)
        for st in node.children:
            if st.statelist not in visited:
                visited.append(st.statelist)
                current.append(st.statelist)


class ProfondeurIterative:
    maxDepth = 0
    iteration = 0
    visited = []
    nb = 0

    def __init__(self, stateini):
        self.visited.append(stateini.statelist)

    def resolve(self, state):
        afficher(state.statelist)
        self.nb += 1
        if state.statelist == final.statelist:
            print('Nombre de noeuds visité par profondeur itérative est ', str(self.nb))
            return state
        else:
            while self.iteration <= self.maxDepth:
                node = GameNode(state.statelist)
                self.iteration += 1
                for st in node.children:
                    if st.statelist not in self.visited:
                        self.visited.append(st.statelist)
                        return self.resolve(st)
            return None

    def resolveit(self, stateinit):
        result = self.resolve(stateinit)
        if result is not None:
            return result
        self.maxDepth += 1
        self.iteration = 0
        self.visited = []
        return self.resolveit(stateinit)


class Astar:
    def h1(self, state):
        total = 0
        i = 0
        while i < n ** 2:
            if state.statelist[i] != final.statelist[i]:
                total += 1
            i += 1
        return total

    def h2(self, state):
        total = 0
        i = 1
        while i < n ** 2:
            vi = state.getpos(i)
            vf = final.getpos(i)
            total += abs(vf.x - vi.x) + abs(vf.y - vi.y)
            i += 1
        return total

    def resolve(self, state, h):
        nb = 0
        visited = []
        current = [state]
        while current:
            i = 0
            imin = 0
            min = current[0].f
            while i < len(current):
                if current[i].f < min:
                    min = current[i].f
                    imin = i
                i += 1
            curstate = current[imin]
            current.pop(imin)
            visited.append(curstate.statelist)
            nb += 1
            if curstate.statelist == final.statelist:
                return nb
            node = GameNode(curstate.statelist)
            for st in node.children:
                if st.statelist in visited:
                    continue
                st.g = curstate.g + 1
                st.h = h(st)
                st.f = st.g + st.h
                i = 0
                statefound = st
                while i < len(current):
                    if current[i].statelist == st.statelist:
                        statefound = current[i]
                        break
                    i += 1
                if statefound.g < st.g:
                    continue
                current.append(st)

    def resolveit(self, state):
        nb1 = self.resolve(state, self.h1)
        print('Nombre de noeuds visité par A* avec h1 est ', str(nb1))
        nb2 = self.resolve(state, self.h2)
        print('Nombre de noeuds visité par A* avec h2 est ', str(nb2))


def generertaquin():
    print('Donner la largeur du taquin: ')
    global n
    global initial
    global final
    n = int(input())
    lfinal = [0]
    i = 1
    while i < n ** 2:
        lfinal.append(i)
        i += 1
    linitial = lfinal.copy()
    random.shuffle(linitial)
    initial = State(linitial)
    while not solvable(initial) or linitial == lfinal:
        random.shuffle(linitial)
        initial = State(linitial)
    final = State(lfinal)
    print('Le taquin initiale: ')
    afficher(linitial)
    print('Le taquin finale: ')
    afficher(lfinal)


def main():
    generertaquin()
    c = 0
    while (c != '6'):
        print('-----------------------------------------')
        print('1-Recherche en profondeur d\'abord')
        print('2-Recherche en largeur d\'abord')
        print('3-Recherche en profendeur itérative')
        print('4-Recherche en A*')
        print('5-Regénerer taquin')
        print('6-Quitter')
        print('-----------------------------------------')
        print('Ecrire le numéro du choix: ')
        c = input()
        if c == '1':
            pr = Profondeur()
            state = pr.resolve(initial,[])
        elif c == '2':
            state = Largeur(initial)
        elif c == '3':
            prit = ProfondeurIterative(initial)
            state = prit.resolveit(initial)
        elif c == '4':
            astar = Astar()
            astar.resolveit(initial)
        elif c == '5':
            generertaquin()
        elif c == '6':
            break


#Manually generate the board:
#n= 3
#initial= State([3, 1, 2, 6, 7, 4, 5, 0, 8])
#final= State([0, 1, 2, 3, 4, 5, 6, 7, 8])

if __name__ == "__main__":
    main()
