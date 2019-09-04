import pgzrun
import random


WIDTH= 700
HEIGHT= 900


sudokupole = Actor("sudokupole", center = (WIDTH/2,600/2+50))
youwin2 = Actor("youwin2", center = (-10000,-10000))
chisla = [0]*9
kletki = [0]*9
notsee = open('sudokunotsee.txt')
notsee = notsee.read()
see = open('sudokusee.txt')
see = see.read()
i1 = 0
j1 = 0
a = 0

for i in range(0,9):
    chisla[i] =[0,0]
    chisla[i][1] = Actor("mychislo" + str(i+1), center = (50 + 32 + i*3 + i*64, 775))
    chisla[i][0] = Actor("white", center = (50 + 32 + i*64 + i*3, 775))
    kletki[i] = [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
    for j in range(0,9):
        kletki[i][j][0] = Actor("white", center = (50 + 3 + j + 32 + j*64 + j//3*3, 50 + 3 + i + 32 + i*64 + i//3*3))
        if see[i*9+j]=="0":
            kletki[i][j][1] = Actor("false0", center = (50 + 3 + j + 32 + j*64 + j//3*3, 50 + 3 + i + 32 + i*64 + i//3*3))
        else:
            kletki[i][j][1] = Actor("mychislo" + see[i*9+j], center = (50 + 3 + j + 32 + j*64 + j//3*3, 50 + 3 + i + 32 + i*64 + i//3*3))
            kletki[i][j][2] = 1
kletki[0][0][0].image = "blue"
def stechkin(i1,j1,n):
    global kletki
    for x in range(0,9):
        for y in range(0,9):
            if (x!=i1 or y!=j1) and kletki[x][y][0].image != "red":
                if kletki[x][y][1].image[-1] == kletki[i1][j1][1].image[-1] != "0":
                    kletki[x][y][0].image = n
                if x == i1:
                    kletki[x][y][0].image = n
                if y == j1:
                    kletki[x][y][0].image = n
                if i1//3*3 <= x < (i1//3 + 1)*3 and j1//3*3 <= y < (j1//3 + 1)*3 :
                    kletki[x][y][0].image = n
def on_mouse_down(pos):
    global i1, j1, b
    b = 0
    if kletki[i1][j1][2] == 0:
        for i in range(0,9):
            if chisla[i][1].collidepoint(pos):
                stechkin(i1,j1,"white")
                if chisla[i][1].image != "mychislo" + notsee[i1*9+j1]:
                    kletki[i1][j1][0].image = "red"
                else:
                    kletki[i1][j1][0].image = "blue"
                kletki[i1][j1][1].image = "chislo" + str(i+1)
                stechkin(i1,j1,"grey")
                break
    for i in range(0,9):
        for j in range(0,9):
            if kletki[i][j][1].image[-1] == notsee[i*9 + j] != 0:
                b += 1
            if kletki[i][j][0].collidepoint(pos):
                stechkin(i1,j1,"white")
                if kletki[i][j][0].image != "red":
                    kletki[i][j][0].image = "blue"
                if kletki[i1][j1][0].image == "blue" and (i1 != i or j1 != j):
                    kletki[i1][j1][0].image = "white"
                i1 = i
                j1 = j
                stechkin(i1,j1,"grey")
    if b == 81 :
        youwin2.x = WIDTH/2
        youwin2.y = 700/2
    
def draw():
    screen.clear()
    screen.fill((0,0,0))
    ##sudokupole.draw()
    if youwin2.x < 0:
        for i in range(0,9):
            chisla[i][0].draw()
            chisla[i][1].draw()
            for j in range(0,9):
                kletki[i][j][0].draw()
                kletki[i][j][1].draw()
    youwin2.draw()
pgzrun.go()
