import random
import tkinter as tk
import os
import sys
from tkinter import *
from menu import *

menu()
window_that_vse_okay()

rows = settings[0] # 10 # Количество строк
cols = settings[1] # 10 # Количество колонок
razk = settings[3] # 50 # Размер клетки
razch = round(razk/3) # Размер цифр
kcolor = settings[4] # "gray" # Цвет клеток
kcl_color = settings[5] # "white" # Цвет открытой клетки
k_obv = settings[6] # "red" # Цвет активной обводки
k_flag = settings[7] # "green" # Цвет флага
first_click = 0 # Проверка первого клика

for widget in root.winfo_children():
    widget.destroy()

nrow = 1 # Текущая строка
ncol = 1 # Текущая колонка

nnmbr = 0

dif = settings[2] # 1 # Сложность
idif = 11 - dif # Инвертированная сложность

matrix = [] # Матрица мин 

# Создаём матрицу открытых клеток
matrix_opn = [] # Матрица открытых клеток
for i in range(rows):
    row = []
    for j in range(cols):
        row.append(0)
    matrix_opn.append(row)
    
# Создаём матрицу флагов
matrix_flag = [] # Матрица флагов
for i in range(rows):
    row = []
    for j in range(cols):
        row.append(0)
    matrix_flag.append(row)

# Матрица победы
matrix_win = [] 
for i in range(rows):
    row = []
    for j in range(cols):
        row.append(0)
    matrix_win.append(row)

# Матрица победы для сравнения
matrix_win2 = [] 
for i in range(rows):
    row = []
    for j in range(cols):
        row.append(1)
    matrix_win2.append(row)

# Создаем основное окно
root.deiconify()
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

# Рисуем начальную обводку для удобсва
x1_new = ncol * (razk + 1) - razk + 1
y1_new = nrow * (razk + 1) - razk + 1
canvas.create_rectangle(x1_new, y1_new, x1_new + razk, y1_new + razk, outline=k_obv, width=1)
canvas.create_rectangle(x1_new - 1, y1_new - 1, x1_new + razk + 1, y1_new + razk + 1, outline=k_obv, width=1)

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
    if char == "M":
        color = "red"
    elif char == "🚩":
        color = k_flag
    elif int(char) == 1:
        color = "blue"
    elif int(char) == 2:
        color = "green"
    elif int(char) == 3:
        color = "red"
    elif int(char) == 4:
        color = "navy"        
    elif int(char) == 5:
        color = "maroon"      
    elif int(char) == 6:
        color = "turquoise"  
    elif int(char) == 7:
        color = "black"
    elif int(char) == 8:
        color = "gray"
    canvas.create_text(x, y, text=str(char), font=("Arial", razch,"bold"), fill=color)

# Алгоритм открывания и рекурсия
def open_cell(x, y):
    if x < 1 or x > cols or y < 1 or y > rows:
        return
    
    # Проверка клетки
    if matrix_opn[x-1][y-1] == 1:
        return
    
    if matrix_flag[ncol-1][nrow-1] == 1:
        matrix_flag[ncol-1][nrow-1] = 0
        
    # Открытие клетки
    matrix_opn[x-1][y-1] = 1
    matrix_win[x-1][y-1] = 1
    
    x1 = x * (razk + 1) - razk + 1
    y1 = y * (razk + 1) - razk + 1
    canvas.create_rectangle(x1, y1, x1 + razk, y1 + razk, fill=kcl_color)
    
    # КОНЕЦ ИГРЫ НА МИНЕ 
    if matrix[x-1][y-1] == 1:
        show_lose_window()
        draw_text(x, y, "M")
        return
    
    if matrix_win == matrix_win2:
        show_win_window()
                        
    count = know(x, y)  
    if count > 0:
        draw_text(x, y, count)
    else:
        # Рекурсивно открываем соседние клетки
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                if not (i == x and j == y):
                    open_cell(i, j)


# Запуск сканирования клетки      
def scan():
    global nrow, ncol, first_click
    
    if first_click == 0:
        x = ncol
        y = nrow
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                if 1 <= i <= cols and 1 <= j <= rows:
                    matrix[i-1][j-1] = 0
        first_click = 1
    
    open_cell(ncol, nrow)
                
# Установка флага
def flag():
    global ncol, nrow
    
    if matrix_flag[ncol-1][nrow-1] == 0:
        draw_text(ncol, nrow, "🚩")
        matrix_flag[ncol-1][nrow-1] = 1
    elif matrix_opn[ncol-1][nrow-1] == 1:
            x1 = ncol * (razk + 1) - razk + 1
            y1 = nrow * (razk + 1) - razk + 1
            canvas.create_rectangle(x1, y1, x1 + razk, y1 + razk, fill=kcl_color)
            matrix_flag[ncol-1][nrow-1] = 0
    else:
            x1 = ncol * (razk + 1) - razk + 1
            y1 = nrow * (razk + 1) - razk + 1
            canvas.create_rectangle(x1, y1, x1 + razk, y1 + razk, fill=kcolor)
            matrix_flag[ncol-1][nrow-1] = 0
    if matrix_flag[ncol-1][nrow-1] == matrix[ncol-1][nrow-1] == 1:
        matrix_win[ncol-1][nrow-1] = 1
    else:
        matrix_win[ncol-1][nrow-1] = 0
    
    if matrix_win == matrix_win2:
        show_win_window()

# Экран победы
def show_win_window():
    global win
    win = tk.Toplevel(root)
    win.title("Победа!")
    win.geometry("300x150")
    win.resizable(False, False)
    
    label = tk.Label(win,text=f"Вы победили!\nСложность была: {dif}",font=("Arial", 14, "bold"))
    label.pack(expand=True)
    win_btn = tk.Button(win, text="Новая игра", width=10, command=lambda:restart(win))
    win_btn.pack(side=tk.BOTTOM, pady=10)

# Экран поражения
def show_lose_window():
    global lose
    lose = tk.Toplevel(root)
    lose.attributes("-fullscreen", True)
    lose.configure(bg="black")
    
    label = tk.Label(lose, text="💀 ВЫ ПРОИГРАЛИ 💀\n\nАнекдот\nИдет медведь по лесу, видит — машина горит. Сел в нее и сгорел.", font=("Arial", 40, "bold"), fg="red", bg="black")
    label.pack(expand=True)
    lose.bind("<Escape>", lambda e: restart(lose))
    lose.protocol("WM_DELETE_WINDOW", lambda: restart(lose))

 
# Функция перезапуска игры
def restart(windows):
    windows.destroy()
    os.execl(sys.executable, sys.executable, *sys.argv) # Перезапуск кода
                                         
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
tk_button_flag = tk.Button(frame_bottom, text="Flag", width=10, command=flag)
tk_button_flag.pack(side=tk.LEFT, padx=1)            

root.mainloop()