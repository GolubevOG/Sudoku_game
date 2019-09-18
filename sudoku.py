# -*- coding:utf-8 -*-
from collections import Counter
import random
import pgzrun
def adjust_rows_from_cols(cols: list):
    rows = []
    for i in range(9):
        _row = []
        for j in range(9):
            _row.append(0)
        rows.append(_row)
    for col_index in range(9):
        for elem_index in range(9):
            rows[elem_index][col_index] = cols[col_index][elem_index]
    return rows

def adjust_cols_from_rows(rows: list):
    cols = []
    for i in range(9):
        col = []
        for j in range(9):
            col.append(0)
        cols.append(col)

    for row_index in range(9):
        for elem_index in range(9):
            cols[elem_index][row_index] = rows[row_index][elem_index]
    return cols

def print_pole(rows):
    for az in rows:
        for buki in az:
            print(buki, end=' ')
        print()

def get_square_elements(x, y, strs): # int -> int -> list(list(int)) -> set(int)
    str_coords = [i for i in range(x // 3 * 3, (x + 3) // 3 * 3)]
    col_coords = [i for i in range(y // 3 * 3, (y + 3) // 3 * 3)]
    res = []
    for str_coord in str_coords:
        for col_coord in col_coords:
            res.append(strs[str_coord][col_coord])
    return res

def read_field(file='field.txt'):
    with open(file, 'r', encoding='utf8') as field_file:
        lines = field_file.read()
        rows = []
        for boundary in range(0,73,9):
            row = lines[boundary:boundary+9].split('')
            rows.append(row)
    return rows

def write_to_txt(rows, filename):
    with open(filename, 'w', encoding='utf8') as file:
        for field_row in rows:
            for field_elem in field_row:
                print(field_elem, end='', file=file)

def checker(rows):

    cols = adjust_cols_from_rows(rows)
    correct = True
    for r in rows:
        R = r[:]
        while 'X' in R:
            R.remove('X')
        if 2 in Counter(R).values():
            correct = False
    for c in cols:
        C = c[:]
        while 'X' in C:
            C.remove('X')
        if 2 in Counter(C).values():
            correct = False
    for sq_x in range(3):
        for sq_y in range(3):
            square = get_square_elements(sq_x*3, sq_y*3, rows)
            while 'X' in square:
                square.remove('X')
            if 2 in Counter(square).values():
                correct = False
    return correct

def generate_primary_field():
    decset = [i for i in range(1,10)]
    random.shuffle(decset)
    pole_rows = []

    for _ in range(9):
        pst = []
        for __ in range(9):
            if _ <= 2:
                value = (_ * 3 + __ + 1) % 9
            elif 3 <= _ <= 5:
                value = (_ * 3 + __ + 2) % 9
            else:
                value = (_ * 3 + __ + 3) % 9
            if value == 0:
                value = 9
            pst.append(decset[value-1])
        pole_rows.append(pst)

    return pole_rows


def generate_field():
    pole_rows = generate_primary_field()
    # shuffling rows
    row_block0 = pole_rows[:3]
    random.shuffle(row_block0)
    row_block1 = pole_rows[3:6]
    random.shuffle(row_block1)
    row_block2 = pole_rows[6:]
    random.shuffle(row_block2)
    row_blocks = [row_block0, row_block1, row_block2]
    random.shuffle(row_blocks)
    # setting new rows and columns
    new_pole_rows = []
    new_pole_cols = []
    for row_block in row_blocks:
        new_pole_rows.extend(row_block)
    pole_rows = new_pole_rows
    pole_cols = adjust_cols_from_rows(pole_rows)
    # shuffling columns
    col_block0 = pole_cols[:3]
    random.shuffle(col_block0)
    col_block1 = pole_cols[3:6]
    random.shuffle(col_block1)
    col_block2 = pole_cols[6:]
    random.shuffle(col_block2)
    col_blocks = [col_block0, col_block1, col_block2]
    random.shuffle(col_blocks)
    # setting new rows and columns
    for col_block in col_blocks:
        new_pole_cols.extend(col_block)
    pole_cols = new_pole_cols
    pole_rows = adjust_rows_from_cols(pole_cols)

    return pole_rows

def set_difficulty(field_rows:list, difficulty:int):
    for row in range(9):
        indexes = [i for i in range(9)]
        random.shuffle(indexes)
        if difficulty == 1:
            indexes_to_erase = indexes[:3]
        elif difficulty == 2:
            indexes_to_erase = indexes[:5]
        elif difficulty == 3:
            if row % 2 == 0:
                indexes_to_erase = indexes[:7]
            else:
                indexes_to_erase = indexes[:6]
        for i in indexes_to_erase:
            field_rows[row][i] = '0'

    return field_rows

def gen_main(): # gen.main()
    field_rows = generate_field()
    write_to_txt(field_rows, 'sudokunotsee.txt')
    see = set_difficulty(field_rows, 1)
    write_to_txt(see, 'sudokusee.txt')

WIDTH= 900
HEIGHT= 700
##ширина и длина окна

sudokupole = Actor("sudokupole", center = (WIDTH/2,600/2+50))
##вывод этого поля(просто решеточек), картинки добавляются отдельно

youwin2 = Actor("youwin2", center = (-10000,-10000))
##картинка выигрыша, которая сначала не видна, но потом ее координаты меняют, чтобы она заслонила поле

chisla = [0]*9
kletki = [0]*9
##создаются пока что обычные массивы для чисел и клеток

gen_main()
notsee = open('sudokunotsee.txt')
notsee = notsee.read()
see = open('sudokusee.txt')
see = see.read()
##see - это то, что мы видим, на самом деле просто в одну строчку записано все, что стоит на поле в начальный момент времени слева направо сверху вниз
##not see - это уже разгаданный судоку, опять же написанный в одну строчку слева направо сверху вниз
i1 = 0
j1 = 0
## координаты синенькой клетки(синенька клетка это та, по которой вы в последнй раз щелкнули курсором)
a = 0
## какая-то переменная, которая вообще нигде не используется

for i in range(0,9):
    chisla[i] =[0,0]
    ## переделываем в двумерный массив

    chisla[i][1] = Actor("mychislo" + str(i+1),
                         center = (775, 50 + 32 + i*3 + i*64)
                        #center = (50 + 32 + i*3 + i*64, 775))
                         )
    ## вторая ячейка заполняется картинкой данного числа и собственное координатой
    chisla[i][0] = Actor("white",
                        #center = (50 + 32 + i*64 + i*3, 775)
                         center = (775, 50 + 32 + i*3 + i*64)
                         )
    ## первая ячейка заполняется белым цевтом, типа фон и тоже координатой
    kletki[i] = [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]

    ## трехмерный массив создан в нулевой клетке фон, в первой клетке опять ничего, если мы этого не должны видеть, и стоит число если мы должны это видеть
    ## опять же вторая клетка заполнена 0, если первая клетка заполнена ничем и 1 если заполнена числом
    for j in range(0,9):
        kletki[i][j][0] = Actor("white", center = (50 + 3 + j + 32 + j*64 + j//3*3, 50 + 3 + i + 32 + i*64 + i//3*3))
        ## пока что снова ставит заглушку
        if see[i*9+j]=="0":
            kletki[i][j][1] = Actor("false0", center = (50 + 3 + j + 32 + j*64 + j//3*3, 50 + 3 + i + 32 + i*64 + i//3*3))
        else:
            kletki[i][j][1] = Actor("mychislo" + see[i*9+j], center = (50 + 3 + j + 32 + j*64 + j//3*3, 50 + 3 + i + 32 + i*64 + i//3*3))
            kletki[i][j][2] = 1

kletki[0][0][0].image = "blue"
## изначально левая верхняя клетка считается как будто мы на нее тыкнули и подсвечивается голубым


def stechkin(i1,j1,n):
    ## эта функция подсвечивает серым клетки, на которых записано такое же число что и на голубой клетке(если это число вообще записано) или если клетки в одном столбце или строке или квадрате 3*3 с голубой
    ##также эта функция потом убирает серый цвет, то есть делает белую заливку, когда меняется голубая клетка
    global kletki
    ##пробегается по всем клеткам
    for x in range(0,9):
        for y in range(0,9):
            if (x!=i1 or y!=j1) and kletki[x][y][0].image != "red":
                if kletki[x][y][1].image[-1] == kletki[i1][j1][1].image[-1] != "0":##типа если совпадают чиселки в клеточках, то подсветка
                    kletki[x][y][0].image = n
                if x == i1:## если находятся в одном столбце
                    kletki[x][y][0].image = n
                if y == j1:## если находятся в одной строке
                    kletki[x][y][0].image = n
                if i1//3*3 <= x < (i1//3 + 1)*3 and j1//3*3 <= y < (j1//3 + 1)*3 :##если находятся в одном квадрате 3*3
                    kletki[x][y][0].image = n


def on_mouse_down(pos):##когда щелкаем мышкой
    global i1, j1, b
    b = 0
    if kletki[i1][j1][2] == 0:##это если в голубой клетке ничего не стоит
        for i in range(0,9):
            if chisla[i][1].collidepoint(pos):## если мы нажали на число чтобы его поставить
                stechkin(i1,j1,"white")## у нас опять убирается серый цвет
                if chisla[i][1].image != "mychislo" + notsee[i1*9+j1]:## если поставленное число не совпадает с задуманным, то задний фон красный, иначе остается голубым
                    kletki[i1][j1][0].image = "red"
                else:
                    kletki[i1][j1][0].image = "blue"
                kletki[i1][j1][1].image = "chislo" + str(i+1)## в любом случае в клетку записывается новое число
                stechkin(i1,j1,"grey")##опять серая подсветка
                break
    for i in range(0,9):##снова пробегается по всем клеткам
        for j in range(0,9):
            if kletki[i][j][1].image[-1] == notsee[i*9 + j] != 0:##cчитает сколько правильных b-количество уже разгаданных
                b += 1
            if kletki[i][j][0].collidepoint(pos):##если мы нажали на новую клетку. то старые голубые стираются
                stechkin(i1,j1,"white")

                if kletki[i][j][0].image != "red":##если новая клетка не красная, то перекрашиваем ее в синюю
                    kletki[i][j][0].image = "blue"
                if kletki[i1][j1][0].image == "blue" and (i1 != i or j1 != j):##если клетка на которую мы теперь нажали не совпадает с предыдущей, то мы снимаем с нее синий цвет
                    kletki[i1][j1][0].image = "white"
                i1 = i
                j1 = j
                ## теперь задаем координаты новой синей клетки
                stechkin(i1,j1,"grey")## и соответственно подсвечиваем серым все то, что должно быть подсвечено(описано выше)
    if b == 81 :## если все клетки совпадают с задуманными, то мы победили и высвечивается картинка(ее координаты проосто меняются, поэтому она появляется)
        youwin2.x = WIDTH/2
        youwin2.y = 700/2

def draw():
    screen.clear()##все убирает с поля
    screen.fill((0,0,0))##заполняет белым
    ##sudokupole.draw()
    if youwin2.x < 0:##если еще не высветилось что мы победили, то рисуются сначала фоны, потом сами картинки для чисеи и для каждой клетки
        for i in range(0,9):
            chisla[i][0].draw()
            chisla[i][1].draw()
            for j in range(0,9):
                kletki[i][j][0].draw()
                kletki[i][j][1].draw()
    youwin2.draw()
pgzrun.go()
