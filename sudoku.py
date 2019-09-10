# -*- coding:utf-8 -*-
import pgzrun
import random


WIDTH= 700
HEIGHT= 900

#Высота и ширина поля в пикселях

sudokupole = Actor("sudokupole", center = (WIDTH/2,600/2+50))
youwin2 = Actor("youwin2", center = (-10000,-10000))
chisla = [0]*9
kletki = [0]*9
notsee = open('sudokunotsee.txt')   #в файле sudokunotsee.txt написано,
notsee = notsee.read()              #какие цифры, где должны стоять
see = open('sudokusee.txt')         #в файле sudokusee.txt написано,
see = see.read()                    #какие цифры видны изначально, и где они стоят
i1 = 0                  #i1 и j1 - строка и столбец,
j1 = 0                  #в которых находится выбранная клетка
a = 0
for i in range(0,9):
    chisla[i] = [0,0]                                                                   #chisla - это массив с объектами чисел,
    chisla[i][1] = Actor("mychislo" + str(i+1), center = (50 + 32 + i*3 + i*64, 775))   #которые находятся внизу экрана
    chisla[i][0] = Actor("white", center = (50 + 32 + i*64 + i*3, 775))                 #и на которые надо нажимать для постановки их на поле
    kletki[i] = [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]                                                   #kletki - это массив
    for j in range(0,9):                                                                                                                    #с каждой клеткой поля,
        kletki[i][j][0] = Actor("white", center = (50 + 3 + j + 32 + j*64 + j//3*3, 50 + 3 + i + 32 + i*64 + i//3*3))                       #у каждой из которых,
        if see[i*9+j]=="0":                                                                                                                 #есть три объекта:
            kletki[i][j][1] = Actor("false0", center = (50 + 3 + j + 32 + j*64 + j//3*3, 50 + 3 + i + 32 + i*64 + i//3*3))                  #фон
        else:                                                                                                                               #число на нем
            kletki[i][j][1] = Actor("mychislo" + see[i*9+j], center = (50 + 3 + j + 32 + j*64 + j//3*3, 50 + 3 + i + 32 + i*64 + i//3*3))   #и поставленно или нет(1 или 0)
            kletki[i][j][2] = 1
kletki[0][0][0].image = "blue"  #а здесь мы задаем задний фон левой верхней клетки синим, как бкдто мы кликнули по этой клетке
def stechkin(i1,j1,n):
    global kletki
    for x in range(0,9):
        for y in range(0,9):
            if (x!=i1 or y!=j1) and kletki[x][y][0].image != "red":
                if kletki[x][y][1].image[-1] == kletki[i1][j1][1].image[-1] != "0":     #Данная функция меняет фон всех клеток в строке i1,
                    kletki[x][y][0].image = n                                           #столбце j1, в квадратике, в котором находится клетка с координатами(i1, j1),
                if x == i1:                                                             #а также клеток, в которых стоит то же число, что и в клетке скоординатами(i1, j1),
                    kletki[x][y][0].image = n                                           #кроме клетки с координатой(i1, j1), и клеток, в которых стоят неверные цифры,
                if y == j1:                                                             #на фон n
                    kletki[x][y][0].image = n                                           #
                if i1//3*3 <= x < (i1//3 + 1)*3 and j1//3*3 <= y < (j1//3 + 1)*3 :
                    kletki[x][y][0].image = n
def on_mouse_down(pos):
    global i1, j1, b
    b = 0                                                                           #b - количество поставленных чисел
    if kletki[i1][j1][2] == 0:                  #поставлено или нет число в выбранную клетку нет 
        for i in range(0,9):
            if chisla[i][1].collidepoint(pos):      #Если мы кликнули по нижним числам, то
                stechkin(i1,j1,"white")
                if chisla[i][1].image != "mychislo" + notsee[i1*9+j1]:  #Если поставленное число не соответствует соответствующему числу в строке notsee,
                    kletki[i1][j1][0].image = "red"                     #то меняем фон на красный
                else:
                    kletki[i1][j1][0].image = "blue"                    #Если мы поставили правильное число, то меняем фон на синий
                kletki[i1][j1][1].image = "chislo" + str(i+1)   #Ставим выбранное число в клетку
                stechkin(i1,j1,"grey")
                break
    for i in range(0,9):                    #Проходим по всем клеточкам
        for j in range(0,9):
            if kletki[i][j][1].image[-1] == notsee[i*9 + j] != 0:       #Считаем, сколько всего правильно поставленных цифр
                b += 1
            if kletki[i][j][0].collidepoint(pos):               #Если мы кликнули по какой-то клеточке, то:
                stechkin(i1,j1,"white")                         #Смена фона всех подсвеченных клеточек на белый
                if kletki[i][j][0].image != "red":              #Если выбранная клеточка не красная,
                    kletki[i][j][0].image = "blue"              #меняем ее фон на синий
                if kletki[i1][j1][0].image == "blue" and (i1 != i or j1 != j):     #Фон предыдущей выбранной клеточки меняем на белый
                    kletki[i1][j1][0].image = "white"
                i1 = i      #задаём новые координаты
                j1 = j      #текущей клетки
                stechkin(i1,j1,"grey")
    if b == 81 :                    #Если все клеточки открыты правильно, то перетаскиваем победное окно на экран
        youwin2.x = WIDTH/2
        youwin2.y = 700/2
    
def draw():
    screen.clear()
    screen.fill((0,0,0))
    ##sudokupole.draw()
    if youwin2.x < 0:                       #Если победное окно не на экране, то отрисовываем поле
        for i in range(0,9):
            chisla[i][0].draw()
            chisla[i][1].draw()
            for j in range(0,9):
                kletki[i][j][0].draw()
                kletki[i][j][1].draw()
    youwin2.draw()                          #И отрисовываем победное окно
pgzrun.go()
