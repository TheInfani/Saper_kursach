import random
import turtle
import tkinter as tk
from tkinter import *

rows = 10 # Количество строк
cols = 10 # Количество колонок
razk = 50 # Размер клетки
razch = round(razk/3) # Размер цифр
kcolor = "gray" # Цвет клеток
kcl_color = "white" # Цвет чистой клетки
k_obv = "green" # Цвет активной обводки
first_click = 0 # Проверка первого клика

nrow = 8 # Текущая строка
ncol = 8 # Текущая колонка

nnmbr = 0

dif = 5 # Сложность
idif = 11 - dif # Инвертированная сложность

matrix = [] # Матрица мин
matrix_opn = [] # Матрица открытых клеток

# Создаём матрицу открытых пклеток
for i in range(rows):
    row = []
    for j in range(cols):
        row.append(0)
    matrix_opn.append(row) 

# Создаем основное окно
root = tk.Tk()
root.title("Tkinter")
root.geometry(f"{(cols * razk) + cols+4}x{(rows * razk) + rows + 100}")
root.resizable(False, False)

# Создаем холст (Canvas) в верхней части окна
canvas = tk.Canvas(root, width=(cols*razk)+cols+4, height=(rows*razk)+rows) 
canvas.pack(pady=10)

# ОТРИСОВКА БАЗОВОГО ПОЛЯ
def kva(stor, kolv_str, kolv_stbl, colors):
    x1 = 0
    y1 = 2
    x2 = stor
    y2 = stor + 2
    for i in range(0, kolv_str):
        x1 = 2
        x2 = stor + 2
        for x in range(0, kolv_stbl):    
            canvas.create_rectangle(x1, y1, x2, y2, fill=colors)
            x1 = x1 + stor + 1
            x2 = x2 + stor + 1
        y1 = y1 + stor + 1
        y2 = y2 + stor + 1

# СОЗДАНИЕ МАТРИЦЫ МИН
for i in range(rows):
    row = []
    for j in range(cols):
        if  random.randint(0, idif) == 1:
            row.append(1)
        else:
            row.append(0)
    matrix.append(row)

# СКАНИРОВАНИЕ ВОКРУГ  КЛЕТКИ, 1 ЦИФРА
def know(x, y):
    
    nmbr = 0   
    for i in range(x-1, x+2):
        for j in range(y-1, y+2):
           if 1 <= i <= cols and 1 <= j <= rows:
                if matrix[i-1][j-1] == 1:
                    nmbr += 1
                    
    return nmbr


# ЗАПУК ОТРИСОВКИ ПОЛЯ
kva(razk, rows, cols, kcolor)


# ПЕРЕМЕЩЕНИЕ
# Перемещение влево
def mleft():
    global nrow, ncol
    
    if ncol > 1:
        x1 = ncol * (razk + 1) - razk + 1
        y1 = nrow * (razk + 1) - razk + 1
        canvas.create_rectangle(x1, y1, x1 + razk, y1 + razk, outline="black", width=1)
        canvas.create_rectangle(x1 - 1, y1 - 1, x1 + razk + 1, y1 + razk + 1, outline="black", width=1)

        ncol -= 1
        x1_new = ncol * (razk + 1) - razk + 1
        y1_new = nrow * (razk + 1) - razk + 1
        canvas.create_rectangle(x1_new, y1_new, x1_new + razk, y1_new + razk, outline=k_obv, width=1)
        canvas.create_rectangle(x1_new - 1, y1_new - 1, x1_new + razk + 1, y1_new + razk + 1, outline=k_obv, width=1)
        
# Перемещение вправо
def mright():
    global nrow, ncol
    
    if ncol < 10:
        x1 = ncol * (razk + 1) - razk + 1
        y1 = nrow * (razk + 1) - razk + 1
        canvas.create_rectangle(x1, y1, x1 + razk, y1 + razk, outline="black", width=1)
        canvas.create_rectangle(x1 - 1, y1 - 1, x1 + razk + 1, y1 + razk + 1, outline="black", width=1)

        ncol += 1
        x1_new = ncol * (razk + 1) - razk + 1
        y1_new = nrow * (razk + 1) - razk + 1
        canvas.create_rectangle(x1_new, y1_new, x1_new + razk, y1_new + razk, outline=k_obv, width=1)
        canvas.create_rectangle(x1_new - 1, y1_new - 1, x1_new + razk + 1, y1_new + razk + 1, outline=k_obv, width=1)
        
# Перемещение вверх
def mup():
    global nrow, ncol
    
    if nrow > 1:
        x1 = ncol * (razk + 1) - razk + 1
        y1 = nrow * (razk + 1) - razk + 1
        canvas.create_rectangle(x1, y1, x1 + razk, y1 + razk, outline="black", width=1)
        canvas.create_rectangle(x1 - 1, y1 - 1, x1 + razk + 1, y1 + razk + 1, outline="black", width=1)

        nrow -= 1
        x1_new = ncol * (razk + 1) - razk + 1
        y1_new = nrow * (razk + 1) - razk + 1
        canvas.create_rectangle(x1_new, y1_new, x1_new + razk, y1_new + razk, outline=k_obv, width=1)
        canvas.create_rectangle(x1_new - 1, y1_new - 1, x1_new + razk + 1, y1_new + razk + 1, outline=k_obv, width=1)

# Перемещение вниз
def mdown():
    global nrow, ncol
    
    if nrow < 10:
        x1 = ncol * (razk + 1) - razk + 1
        y1 = nrow * (razk + 1) - razk + 1
        canvas.create_rectangle(x1, y1, x1 + razk, y1 + razk, outline="black", width=1)
        canvas.create_rectangle(x1 - 1, y1 - 1, x1 + razk + 1, y1 + razk + 1, outline="black", width=1)

        nrow += 1
        x1_new = ncol * (razk + 1) - razk + 1
        y1_new = nrow * (razk + 1) - razk + 1
        canvas.create_rectangle(x1_new, y1_new, x1_new + razk, y1_new + razk, outline=k_obv, width=1)
        canvas.create_rectangle(x1_new - 1, y1_new - 1, x1_new + razk + 1, y1_new + razk + 1, outline=k_obv, width=1)    

# ВЗАИМОДЕЙСТВИЕ

# Рисование текста
def draw_text(col, row, char):
    x = (col * (razk + 1) - razk + 1) + (razk / 2)
    y = (row * (razk + 1) - razk + 1) + (razk / 2)
    canvas.create_text(x, y, text=str(char), font=("Arial", razch,"bold"), fill="black")

# Открытие мины
def mopen():
    global nrow, ncol, first_click
    if first_click == 0:
        matrix[ncol-1][nrow-1] = 0
        first_click += 1
    x1 = ncol * (razk + 1) - razk + 1
    y1 = nrow * (razk + 1) - razk + 1
    canvas.create_rectangle(x1, y1, x1 + razk, y1 + razk, fill=kcl_color)
    if matrix[ncol-1][nrow-1] == 1:
        draw_text(ncol, nrow, "М")
    else:
        if know(ncol, nrow) == 0:
            print("Пусто")
        else:
            draw_text(ncol, nrow, know(ncol, nrow))
    
        
# Алгоритм открывания и рекурсия
def open_cell(x, y):
    if x < 1 or x > cols or y < 1 or y > rows:
        return
    
    # Проверка клетки
    if matrix_opn[x-1][y-1] == 1:
        return
    
    # Открытие клетки
    matrix_opn[x-1][y-1] = 1
    
    x1 = x * (razk + 1) - razk + 1
    y1 = y * (razk + 1) - razk + 1
    canvas.create_rectangle(x1, y1, x1 + razk, y1 + razk, fill=kcl_color)
    
    # ВРЕМЕННО РИСУЕМ МИНУ ВМЕСТО КОНЦА ИГРЫ
    if matrix[x-1][y-1] == 1:
        draw_text(x, y, "М")
        return
    
    count = know(x, y)  
    if count > 0:
        draw_text(x, y, count)
    else:
        # Рекурсивно открываем соседние клетки
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                if not (i == x and j == y):
                    open_cell(i, j)
 
        
def scan():
    global nrow, ncol, first_click
    
    if first_click == 0:
        matrix[ncol-1][nrow-1] = 0
        first_click = 1
    
    open_cell(ncol, nrow)
                
                                   
# КНОПКИ
frame_bottom = tk.Frame(root)
frame_bottom.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

# Кнопка влево
tk_button_left = tk.Button(frame_bottom, text="Left", width=7, command=mleft)
tk_button_left.pack(side=tk.LEFT, padx=1)

# Фрейм под кнопки Up и Down
frame_ud = tk.Frame(frame_bottom)
frame_ud.pack(side=tk.LEFT, padx=1)

# Кнопка вверх
tk_button_up = tk.Button(frame_ud, text="Up", width=7, command=mup)
tk_button_up.pack(side=tk.TOP, padx=1)

# Кнопка вниз
tk_button_down = tk.Button(frame_ud, text="Down", width=7, command=mdown)
tk_button_down.pack(side=tk.BOTTOM, padx=1)

# Кнопка вправо
tk_button_right = tk.Button(frame_bottom, text="Right", width=7, command=mright)
tk_button_right.pack(side=tk.LEFT, padx=1)

# Кнопка открыть
tk_button_open = tk.Button(frame_bottom, text="Open", width=10, command=scan)
tk_button_open.pack(side=tk.LEFT, padx=20)

# Кнопка флажка
#tk_button_min = tk.Button(frame_bottom, text="Min", command=mmin)
#tk_button_min.pack(side=tk.LEFT, padx=20)            

root.mainloop()