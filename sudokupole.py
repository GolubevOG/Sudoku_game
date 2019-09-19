# -*- coding:utf-8 -*-
import random


def maingen():
    w = 9
    h = 9
    spis = []
    a = [i for i in range(3)]
    b = [i for i in range(3, 6)]
    c = [i for i in range(6, 9)]
    
    def generation1(field):
        for i in range(1, len(field)):
            for j in range(len(field[i])):
                if i == 3 or i == 6:
                    x = (j + 2) % 9
                else:
                    x = (j + 3) % 9
                field[i][j] = field[i - 1][x]
    
    def generation2(field, n, l):
            fieldx = field[:]
            for i in range(len(field)):
                field[i] = fieldx[n[i]]
                
            fieldx = []
            for i in field:
                fieldx.append(i[:])
            
            for i in range(len(field)):
                for j in range(len(field[i])):
                    field[i][j] = fieldx[i][l[j]]
                    
    
    def gan1(field2):
        for i in range(36):
            while True:
                x = random.randint(0, 8)
                y = random.randint(0, 8)
                if field2[x][y] == 0:
                    field2[x][y] = field1[x][y]
                    break
                
    random.shuffle(a)
    random.shuffle(b)
    random.shuffle(c)
    n = a + b + c
    
    random.shuffle(a)
    random.shuffle(b)
    random.shuffle(c)
    l = a + b + c
    
    field1 = [[(i + 1) for i in range(h)] for j in range(w)]
    random.shuffle(field1[0])
    
    generation1(field1)
    generation2(field1, n, l)
    f = open("sudokunotsee.txt", "w")
    for i in field1:
        for j in i:
            print(j, end = "", file = f)
    f.close()
    
    field2 = [[(0) for i in range(h)] for j in range(w)]
    gan1(field2)
    
    fel = open("sudokusee.txt", "w")
    for i in field2:
        for j in i:
            print(j, end = "", file = fel)
    fel.close()
