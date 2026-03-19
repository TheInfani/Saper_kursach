import random
import tkinter as tk
import os
import sys
from tkinter import *
from menu import *
import math

menu()
window_license()

rows = settings[0] # 10 # Количество строк
cols = settings[1] # 10 # Количество колонок
cell_size = settings[3] # 50 # Размер клетки
num_size = round(cell_size/3) # Размер цифр
cell_def_color = settings[4] # "gray" # Цвет клеток
cell_open_color = settings[5] # "white" # Цвет открытой клетки
cell_outline_color = settings[6] # "red" # Цвет активной обводки
flag_color = settings[7] # "green" # Цвет флага
first_click = 0 # Проверка первого клика
min_count = 0 # Количество мин

for widget in root.winfo_children():
    widget.destroy()

nrow = math.ceil(rows/2) # Текущая строка
ncol = math.ceil(cols/2) # Текущая колонка

nnmbr = 0

difficult = settings[2] # 1 # Сложность
inv_difficult = 11 - difficult # Инвертированная сложность

matrix = [] # Матрица мин 

# СОЗДАНИЕ МАТРИЦЫ МИН
for i in range(rows):
    row = []
    for j in range(cols):
        if  random.randint(0, inv_difficult) == 1:
            row.append(1)
            min_count += 1
        else:
            row.append(0)
    matrix.append(row)
   
# Создаём матрицу открытых клеток
matrix_open = [] # Матрица открытых клеток
for i in range(rows):
    row = []
    for j in range(cols):
        row.append(0)
    matrix_open.append(row)
    
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
if cols*cell_size >= 350:
    root.geometry(f"{(cols * cell_size) + cols+4}x{(rows * cell_size) + rows + 130}")
else:
    root.geometry("350x480")
root.resizable(False, False)

# Создаем холст (Canvas) в верхней части окна
canvas = tk.Canvas(root, width=(cols*cell_size)+cols+4, height=(rows*cell_size)+rows) 
canvas.pack(pady=10)

# Обработчик кликов
def handle_click(event):
    # Фикс с обводкой при использовании кнопок и мышки
    global nrow, ncol
    x1 = ncol * (cell_size + 1) - cell_size + 1
    y1 = nrow * (cell_size + 1) - cell_size + 1
    canvas.create_rectangle(x1, y1, x1 + cell_size, y1 + cell_size, outline="black", width=1)
    canvas.create_rectangle(x1 - 1, y1 - 1, x1 + cell_size + 1, y1 + cell_size + 1, outline="black", width=1)
    # Проверяем, что клик внутри игрового поля
    max_x = 2 + cols * (cell_size + 1)
    max_y = 2 + rows * (cell_size + 1)
    
    if event.x < 2 or event.x > max_x or event.y < 2 or event.y > max_y:
        return
    else:
        ncol = (event.x - 2) // (cell_size + 1) + 1
        nrow = (event.y - 2) // (cell_size + 1) + 1
        if event.num == 1:
            scan()
        elif event.num == 3:
            flag()
        
# Привязываем обработчик кликов к холсту
canvas.bind('<Button-1>', handle_click)
canvas.bind('<Button-3>', handle_click)
# Привязка стрелочек на клавиатуре (привязываем к root, чтобы работало всегда)
root.bind('<Left>', lambda event: mleft())
root.bind('<Right>', lambda event: mright())
root.bind('<Up>', lambda event: mup())
root.bind('<Down>', lambda event: mdown())

# ОТРИСОВКА БАЗОВОГО ПОЛЯ
mins_label = tk.Label(root, text="Откройте первую клетку", font=("Arial", 12))
mins_label.pack(side=tk.TOP, pady=5)

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
kva(cell_size, rows, cols, cell_def_color)

# Рисуем начальную обводку для удобсва
x1_new = ncol * (cell_size + 1) - cell_size + 1
y1_new = nrow * (cell_size + 1) - cell_size + 1
canvas.create_rectangle(x1_new, y1_new, x1_new + cell_size, y1_new + cell_size, outline=cell_outline_color, width=1)
canvas.create_rectangle(x1_new - 1, y1_new - 1, x1_new + cell_size + 1, y1_new + cell_size + 1, outline=cell_outline_color, width=1)

# ПЕРЕМЕЩЕНИЕ
# Перемещение влево
def mleft():
    global nrow, ncol
    
    if ncol > 1:
        x1 = ncol * (cell_size + 1) - cell_size + 1
        y1 = nrow * (cell_size + 1) - cell_size + 1
        canvas.create_rectangle(x1, y1, x1 + cell_size, y1 + cell_size, outline="black", width=1)
        canvas.create_rectangle(x1 - 1, y1 - 1, x1 + cell_size + 1, y1 + cell_size + 1, outline="black", width=1)

        ncol -= 1
        x1_new = ncol * (cell_size + 1) - cell_size + 1
        y1_new = nrow * (cell_size + 1) - cell_size + 1
        canvas.create_rectangle(x1_new, y1_new, x1_new + cell_size, y1_new + cell_size, outline=cell_outline_color, width=1)
        canvas.create_rectangle(x1_new - 1, y1_new - 1, x1_new + cell_size + 1, y1_new + cell_size + 1, outline=cell_outline_color, width=1)
        
# Перемещение вправо
def mright():
    global nrow, ncol
    
    if ncol < 10:
        x1 = ncol * (cell_size + 1) - cell_size + 1
        y1 = nrow * (cell_size + 1) - cell_size + 1
        canvas.create_rectangle(x1, y1, x1 + cell_size, y1 + cell_size, outline="black", width=1)
        canvas.create_rectangle(x1 - 1, y1 - 1, x1 + cell_size + 1, y1 + cell_size + 1, outline="black", width=1)

        ncol += 1
        x1_new = ncol * (cell_size + 1) - cell_size + 1
        y1_new = nrow * (cell_size + 1) - cell_size + 1
        canvas.create_rectangle(x1_new, y1_new, x1_new + cell_size, y1_new + cell_size, outline=cell_outline_color, width=1)
        canvas.create_rectangle(x1_new - 1, y1_new - 1, x1_new + cell_size + 1, y1_new + cell_size + 1, outline=cell_outline_color, width=1)
        
# Перемещение вверх
def mup():
    global nrow, ncol
    
    if nrow > 1:
        x1 = ncol * (cell_size + 1) - cell_size + 1
        y1 = nrow * (cell_size + 1) - cell_size + 1
        canvas.create_rectangle(x1, y1, x1 + cell_size, y1 + cell_size, outline="black", width=1)
        canvas.create_rectangle(x1 - 1, y1 - 1, x1 + cell_size + 1, y1 + cell_size + 1, outline="black", width=1)

        nrow -= 1
        x1_new = ncol * (cell_size + 1) - cell_size + 1
        y1_new = nrow * (cell_size + 1) - cell_size + 1
        canvas.create_rectangle(x1_new, y1_new, x1_new + cell_size, y1_new + cell_size, outline=cell_outline_color, width=1)
        canvas.create_rectangle(x1_new - 1, y1_new - 1, x1_new + cell_size + 1, y1_new + cell_size + 1, outline=cell_outline_color, width=1)

# Перемещение вниз
def mdown():
    global nrow, ncol
    
    if nrow < 10:
        x1 = ncol * (cell_size + 1) - cell_size + 1
        y1 = nrow * (cell_size + 1) - cell_size + 1
        canvas.create_rectangle(x1, y1, x1 + cell_size, y1 + cell_size, outline="black", width=1)
        canvas.create_rectangle(x1 - 1, y1 - 1, x1 + cell_size + 1, y1 + cell_size + 1, outline="black", width=1)

        nrow += 1
        x1_new = ncol * (cell_size + 1) - cell_size + 1
        y1_new = nrow * (cell_size + 1) - cell_size + 1
        canvas.create_rectangle(x1_new, y1_new, x1_new + cell_size, y1_new + cell_size, outline=cell_outline_color, width=1)
        canvas.create_rectangle(x1_new - 1, y1_new - 1, x1_new + cell_size + 1, y1_new + cell_size + 1, outline=cell_outline_color, width=1)    

# ВЗАИМОДЕЙСТВИЕ

# Рисование текста
def draw_text(col, row, char):
    x = (col * (cell_size + 1) - cell_size + 1) + (cell_size / 2)
    y = (row * (cell_size + 1) - cell_size + 1) + (cell_size / 2)
    if char == "M":
        color = "red"
    elif char == "🚩":
        color = flag_color
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
    canvas.create_text(x, y, text=str(char), font=("Arial", num_size,"bold"), fill=color)

# Алгоритм открывания и рекурсия
def open_cell(x, y):
    if x < 1 or x > cols or y < 1 or y > rows:
        return
    
    # Проверка клетки
    if matrix_open[x-1][y-1] == 1:
        return
    
    if matrix_flag[x-1][y-1] == 1:
        matrix_flag[x-1][y-1] = 0
        global min_count
        min_count += 1
        mins_label.config(text=f"Флажков: {min_count}")
        
    # Открытие клетки
    matrix_open[x-1][y-1] = 1
    matrix_win[x-1][y-1] = 1
    
    x1 = x * (cell_size + 1) - cell_size + 1
    y1 = y * (cell_size + 1) - cell_size + 1
    canvas.create_rectangle(x1, y1, x1 + cell_size, y1 + cell_size, fill=cell_open_color)
    
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
    global nrow, ncol, first_click, min_count
    if first_click == 0:
        x = ncol
        y = nrow
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                if 1 <= i <= cols and 1 <= j <= rows:
                    if matrix[i-1][j-1] == 1:
                        min_count -= 1
                    matrix[i-1][j-1] = 0
        mins_label.config(text=f"Флажков: {min_count}")
        first_click = 1
    
    open_cell(ncol, nrow)
                
# Установка флага
def flag():
    global ncol, nrow, min_count
    
    if matrix_flag[ncol-1][nrow-1] == 0 and matrix_open[ncol-1][nrow-1] == 0:
        draw_text(ncol, nrow, "🚩")
        matrix_flag[ncol-1][nrow-1] = 1
        min_count -= 1
        mins_label.config(text=f"Флажков: {min_count}") # Обновление текста с количеством флажков
    elif matrix_flag[ncol-1][nrow-1] == 1 and matrix_open[ncol-1][nrow-1] == 0:
            x1 = ncol * (cell_size + 1) - cell_size + 1
            y1 = nrow * (cell_size + 1) - cell_size + 1
            canvas.create_rectangle(x1, y1, x1 + cell_size, y1 + cell_size, fill=cell_def_color)
            matrix_flag[ncol-1][nrow-1] = 0
            min_count += 1
            mins_label.config(text=f"Флажков: {min_count}")
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
    
    label = tk.Label(win,text=f"Вы победили!\nСложность была: {difficult}",font=("Arial", 14, "bold"))
    label.pack(expand=True)
    win_btn = tk.Button(win, text="Новая игра", width=10, command=lambda:restart(win))
    win_btn.pack(side=tk.BOTTOM, pady=10)

def open_all_mines():
    for i in range(cols):
        for j in range(rows):
            if matrix[i][j] == 1:
                draw_text(i+1, j+1, "M")

# Экран поражения
def show_lose_window():
    global lose
    lose = tk.Toplevel(root)
    lose.title("Поражение!")
    lose.geometry("300x150")
    lose.resizable(False, False)
    label = tk.Label(lose, text="💀 ВЫ ПРОИГРАЛИ 💀", font=("Arial", 14, "bold"))
    label.pack(expand=True)
    open_all_mines()
    
    btn_menu = tk.Button(lose, text="В меню", width=10, command=lambda: restart(lose))
    btn_menu.pack(side=tk.BOTTOM, pady=10)

    # Блокировка основного окна при открытии окна поражения
    lose.grab_set()
    lose.focus_set()

    # При закрытии окна крестиком срабатывает выход в меню
    lose.protocol("WM_DELETE_WINDOW", lambda: restart(lose))

# Функция перезапуска игры
def restart(windows):
    windows.destroy()
    os.execl(sys.executable, sys.executable, *sys.argv) # Перезапуск кода
# *sys.argv применяет текущие аргументы командой строки, sys.executable исходный путь к интерпритатору
                                        
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