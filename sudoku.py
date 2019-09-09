import pgzrun
import random

#screen properties
WIDTH= 700
HEIGHT= 900

#"images/sudokupole.png" load
sudokupole = Actor("sudokupole", center = (WIDTH/2,600/2+50))
#"images/youwin2.png" load
youwin2 = Actor("youwin2", center = (-10000,-10000))
#bottom 1-9 numeral buttons
chisla = [0]*9
#field
kletki = [0]*9
#full and true solved field
notsee = open('sudokunotsee.txt')
notsee = notsee.read()
#partially solved field, that can see player(where 0 - empty)
see = open('sudokusee.txt')
see = see.read()
#y of current cell(with mouse)
i1 = 0
#x of current cell(with mouse)
j1 = 0
#this variable like inflatable darts - unnecessary
a = 0

for i in range(0,9):
    chisla[i] =[0,0]
    #load image of current "chislo"
    chisla[i][1] = Actor("mychislo" + str(i+1), center = (50 + 32 + i*3 + i*64, 775))
    #load background color of cell
    chisla[i][0] = Actor("white", center = (50 + 32 + i*64 + i*3, 775))
    #set default settings for every field cell
    kletki[i] = [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
    for j in range(0,9):
        #set background color
        kletki[i][j][0] = Actor("white", center = (50 + 3 + j + 32 + j*64 + j//3*3, 50 + 3 + i + 32 + i*64 + i//3*3))
        if see[i*9+j]=="0":
            #if cell is empty(for us in "see.txt"): draw "image/false0.png"
            kletki[i][j][1] = Actor("false0", center = (50 + 3 + j + 32 + j*64 + j//3*3, 50 + 3 + i + 32 + i*64 + i//3*3))
        else:
            #else draw this "chislo"
            kletki[i][j][1] = Actor("mychislo" + see[i*9+j], center = (50 + 3 + j + 32 + j*64 + j//3*3, 50 + 3 + i + 32 + i*64 + i//3*3))
            #this means, that we can't change this cell. This is starting numeral
            kletki[i][j][2] = 1
#set color of starting cell blue(as ssssselected)
kletki[0][0][0].image = "blue"
#this function fill all the cells inside a 3x3 square, in a row, in a column with color(n), all same numerals, current cell has [i1, j1] coordinates
def stechkin(i1,j1,n):
    global kletki
    for x in range(0,9):
        for y in range(0,9):
            if (x!=i1 or y!=j1) and kletki[x][y][0].image != "red":
                #all same numerals
                if kletki[x][y][1].image[-1] == kletki[i1][j1][1].image[-1] != "0":
                    kletki[x][y][0].image = n
                #row
                if x == i1:
                    kletki[x][y][0].image = n
                #column
                if y == j1:
                    kletki[x][y][0].image = n
                #3x3 square
                if i1//3*3 <= x < (i1//3 + 1)*3 and j1//3*3 <= y < (j1//3 + 1)*3 :
                    kletki[x][y][0].image = n
def on_mouse_down(pos):
    global i1, j1, b
    #number of correct cells
    b = 0
    #if we can change this cell
    if kletki[i1][j1][2] == 0:
        for i in range(0,9):
            if chisla[i][1].collidepoint(pos):
                #clear last cells
                stechkin(i1,j1,"white")
                #wrong numeral
                if chisla[i][1].image != "mychislo" + notsee[i1*9+j1]:
                    kletki[i1][j1][0].image = "red"
                #true numeral
                else:
                    kletki[i1][j1][0].image = "blue"
                #set choosen numeral
                kletki[i1][j1][1].image = "chislo" + str(i+1)
                #fill cells, when choose 1-9(in bottom)
                stechkin(i1,j1,"grey")
                break
    for i in range(0,9):
        for j in range(0,9):
            #true cell
            if kletki[i][j][1].image[-1] == notsee[i*9 + j] != 0:
                b += 1
            if kletki[i][j][0].collidepoint(pos):
                #clear last cells
                stechkin(i1,j1,"white")
                if kletki[i][j][0].image != "red":
                    kletki[i][j][0].image = "blue"
                if kletki[i1][j1][0].image == "blue" and (i1 != i or j1 != j):
                    kletki[i1][j1][0].image = "white"
                #refresh current cell
                i1 = i
                j1 = j
                #when clicking on cell - fill cells with grey
                stechkin(i1,j1,"grey")
    #win check(all 9x9 cells is correct)
    if b == 81 :
        #set coordinates of win-page to screen
        youwin2.x = WIDTH/2
        youwin2.y = 700/2
    
def draw():
    screen.clear()
    screen.fill((0,0,0))
    ##sudokupole.draw()
    #if still no win - draw the field
    if youwin2.x < 0:
        for i in range(0,9):
            chisla[i][0].draw()
            chisla[i][1].draw()
            for j in range(0,9):
                kletki[i][j][0].draw()
                kletki[i][j][1].draw()
    youwin2.draw()
#last line of pygame zero
pgzrun.go()
