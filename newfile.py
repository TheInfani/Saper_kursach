import random
import tkinter as tk
import os
import sys
from tkinter import *
from menu import *
import math
import customtkinter as ctk
import pygame
from PIL import Image, ImageSequence


isInGame = True

class AnimatedGif(ctk.CTkLabel):
    def __init__(self, master, path):
        self.img = Image.open("sounds//gif.gif")
        self.frames = [ctk.CTkImage(light_image=f.copy(), size=(200, 200)) 
                       for f in ImageSequence.Iterator(self.img)]
        
        super().__init__(master, image=self.frames[0], text="")
        self.current_frame = 0
        self.animate()

    def animate(self):
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.configure(image=self.frames[self.current_frame])

        self.after(60, self.animate)

def pashalka():
    pash_win = ctk.CTkToplevel(root)
    pash_win.title("Пасхалка")
    pash_win.resizable(False, False)
    pash_win.attributes('-topmost', True)
    win_w = 220
    win_h = 220
    screen_w = pash_win.winfo_screenwidth()
    screen_h = pash_win.winfo_screenheight()
    random_x = random.randint(0, screen_w - win_w)
    random_y = random.randint(0, screen_h - win_h)
    pash_win.geometry(f"{win_w}x{win_h}+{random_x}+{random_y}")
    anim = AnimatedGif(pash_win, "sounds//gif.gif")
    anim.pack(expand=True)

# Функция сохранения настроек в файл
def save_audio_settings():
    with open("audio_settings.txt", "w") as f:
        f.write(f"{music_vol}\n{sfx_vol}") 
 
pygame.mixer.init()
load_audio_settings()

pygame.mixer.music.load("sounds//best_music.mp3")
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(music_vol)
snd_open.set_volume(sfx_vol)
snd_win.set_volume(sfx_vol)
snd_loose.set_volume(sfx_vol)
                     
rows = settings[0] # 10 # Количество строк
cols = settings[1] # 10 # Количество колонок
cell_size = settings[3] # 50 # Размер клетки
num_size = round(cell_size/3) # Размер цифр
cell_def_color = settings[4] # "gray" # Цвет клеток
cell_open_color = settings[5] # "white" # Цвет открытой клетки
cell_outline_color = settings[6] # "red" # Цвет активной обводки
flag_color = settings[7] # "green" # Цвет флага
timer = settings[8] # 0 # Время на игру, 0 для отключения таймера
print(timer)
button_visible = settings[9] # True # Видимость кнопок управления

first_click = 0 # Проверка первого клика
min_count = 0 # Количество мин
theme_color = "system" # light,dark или system

# Видимость кнопок управления
if button_visible:
    button_canvas_size = 130
else:
    button_canvas_size = 60

# Перезапуск вместо закрытия окна при нажатии на крестик
root.protocol("WM_DELETE_WINDOW", lambda: restart(root))

ctk.set_appearance_mode(theme_color) # Глобальная тема зависящая от системных настроек
ctk.set_default_color_theme("dark-blue") # Глобальная цветовая тема

ctk.deactivate_automatic_dpi_awareness()

try:
    if int(timer) > 0:
        is_timer_on = 1
    else:
        is_timer_on = 0
except ValueError:
    is_timer_on = 0

def update_timer():
    global timer, first_click

    if is_timer_on == 1:
        if timer <= 0: 
            show_lose_window(lose_from_min=False)
            return

    timer -= 1
    timer_label.configure(text=f"Время: {timer}")

    root.timer_id = root.after(1000, update_timer)

# Класс для кнопок
class ClassButton(ctk.CTkButton):
    def __init__(self, master, text, command):
        
        def command_with_sound():
            snd_open.play()
            command()
            
        super().__init__(
            master=master,             # root
            text=text,                 # Текст на кнопке
            command=command_with_sound, # Функция при нажатии
            width=50,                  # Ширина
            height=25,                 # Высота
            fg_color="#515151",        # Цвет кнопки
            hover_color="#373737",     # Цвет при наведении мыши
            text_color="white",        # Цвет текста
            corner_radius=8,           # Закругленные углы
            font=ctk.CTkFont(size=12) # Шрифт
        )


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




# Создаем основное окно
root.deiconify()
root.title("Сапер")
if cols*cell_size >= 350:
    root.geometry(f"{(cols * cell_size) + cols+4}x{(rows * cell_size) + rows + button_canvas_size}")
else:
    root.geometry("350x480")
root.resizable(False, False)

# Создаем холст (Canvas) в верхней части окна
canvas = ctk.CTkCanvas(root, width=(cols*cell_size)+cols+4, height=(rows*cell_size)+rows, bg = "#242424", highlightthickness=0, borderwidth=0) 
canvas.pack(pady=10)

# Обработчик кликов
def handle_click(event):
    if isInGame == False:
        return
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
            flag(ncol, nrow)
        
# Привязываем обработчик кликов к холсту
canvas.bind('<Button-1>', handle_click)
canvas.bind('<Button-3>', handle_click)
# Привязка стрелочек на клавиатуре (привязываем к root, чтобы работало всегда)
root.bind('<Left>', lambda event: mleft())
root.bind('<Right>', lambda event: mright())
root.bind('<Up>', lambda event: mup())
root.bind('<Down>', lambda event: mdown())
root.bind('<F5>', lambda event: debug())
root.bind('<m>', lambda event: setting_window())
root.bind('<p>', lambda event: pashalka())
# Альтернанита для руского языка, так как ткинтер не определяет кирилицу
def keypres(event):
    print(event.keycode)
    if event.keycode == 77:
        setting_window()
root.bind('<Key>', keypres)

# ОТРИСОВКА БАЗОВОГО ПОЛЯ
top_info_frame = ctk.CTkFrame(root, fg_color="transparent")
top_info_frame.pack(side=tk.TOP, pady=5)

# Текст с флажками
mins_label = ctk.CTkLabel(top_info_frame, text="Откройте первую клетку", font=("Arial", 12))
mins_label.pack(side=tk.LEFT, padx=15)

if is_timer_on == 1:
    timer_text = f"Время: {timer}"
else:
    timer_text = "Время: Не установлено"

# Текст таймера
timer_label = ctk.CTkLabel(top_info_frame, text=timer_text, font=("Arial", 12))
timer_label.pack(side=tk.LEFT, padx=15)

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
                if matrix[j-1][i-1] == 1:
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
    
    snd_open.play()
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
    
    snd_open.play()
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
    
    snd_open.play()
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
    
    snd_open.play()
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
    if char == "💣":
        x1 = ncol * (cell_size + 1) - cell_size + 1
        y1 = nrow * (cell_size + 1) - cell_size + 1
        canvas.create_rectangle(x1, y1, x1 + cell_size, y1 + cell_size, fill=cell_def_color)
        color = "darkred"
        canvas.create_text(x, y, text=str(char), font=("Segoe UI Emoji", num_size))
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

# Проверка победы
def check_win():
    total_cells = rows * cols
    mine_cells = 0
    for row in matrix:
        mine_cells += row.count(1)
        
    opened_cells = 0
    for row in matrix_open:
        opened_cells += row.count(1)
        
    return opened_cells == (total_cells - mine_cells)

# Алгоритм открывания и рекурсия
def open_cell(x, y):
    if x < 1 or x > cols or y < 1 or y > rows:
        return
    
    # Проверка клетки
    if matrix_open[y-1][x-1] == 1:
        return
    
    if matrix_flag[y-1][x-1] == 1:
        matrix_flag[y-1][x-1] = 0
        global min_count
        min_count += 1
        mins_label.configure(text=f"Флажков: {min_count}")
        
    # Открытие клетки
    matrix_open[y-1][x-1] = 1
    
    x1 = x * (cell_size + 1) - cell_size + 1
    y1 = y * (cell_size + 1) - cell_size + 1
    canvas.create_rectangle(x1, y1, x1 + cell_size, y1 + cell_size, fill=cell_open_color)
    
    # КОНЕЦ ИГРЫ НА МИНЕ 
    if matrix[y-1][x-1] == 1:
        show_lose_window(lose_from_min=True)
        draw_text(x, y, "💣")
        return
    
    if check_win():
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
                    if matrix[j-1][i-1] == 1:
                        min_count -= 1
                    matrix[j-1][i-1] = 0
        mins_label.configure(text=f"Флажков: {min_count}")
        first_click = 1
        if is_timer_on == 1:
            update_timer()
    
    snd_open.play()
    open_cell(ncol, nrow)
                
# Установка флага
def flag(ncol=ncol, nrow=nrow):
    global min_count
    
    snd_open.play()
    if matrix_flag[nrow-1][ncol-1] == 0 and matrix_open[nrow-1][ncol-1] == 0:
        draw_text(ncol, nrow, "🚩")
        matrix_flag[nrow-1][ncol-1] = 1
        min_count -= 1
        mins_label.configure(text=f"Флажков: {min_count}") # Обновление текста с количеством флажков
    elif matrix_flag[nrow-1][ncol-1] == 1 and matrix_open[nrow-1][ncol-1] == 0:
            x1 = ncol * (cell_size + 1) - cell_size + 1
            y1 = nrow * (cell_size + 1) - cell_size + 1
            canvas.create_rectangle(x1, y1, x1 + cell_size, y1 + cell_size, fill=cell_def_color)
            matrix_flag[nrow-1][ncol-1] = 0
            min_count += 1
            mins_label.configure(text=f"Флажков: {min_count}")

# Экран победы
def show_win_window():
    global win
    pygame.mixer.music.stop()
    snd_win.play()
    if is_timer_on == 1 and hasattr(root, 'timer_id'):
        root.after_cancel(root.timer_id)
    win = ctk.CTkToplevel(root)
    win.title("Победа!")
    win.geometry("300x150")
    win.resizable(False, False)
    
    label = ctk.CTkLabel(win,text=f"Вы победили!\nСложность была: {difficult}",font=("Arial", 14, "bold"))
    label.pack(expand=True)
    win_btn = ctk.CTkButton(win, text="Новая игра", width=10, command=lambda:restart(win))
    win_btn.pack(side=tk.BOTTOM, pady=10)
    
    # Блокировка основного окна при открытии окна поражения
    win.grab_set()
    win.focus_set()

    # При закрытии окна крестиком срабатывает выход в меню
    win.protocol("WM_DELETE_WINDOW", lambda: restart(win))

# Открытие всех мин при поражении
def open_all_mines():
    for i in range(cols):
        for j in range(rows):
            if matrix[j][i] == 1:
                draw_text(i+1, j+1, "💣")

# Экран поражения
def show_lose_window(lose_from_min=True):
    global lose, isInGame
    isInGame = False
    pygame.mixer.music.stop()
    snd_loose.play()
    if is_timer_on == 1 and hasattr(root, 'timer_id'):
        root.after_cancel(root.timer_id)
    lose = ctk.CTkToplevel(root)
    lose.title("Поражение!")
    lose.geometry("300x150")
    lose.resizable(False, False)
    if lose_from_min:
        label = ctk.CTkLabel(lose, text="💀 ВЫ ПРОИГРАЛИ 💀", font=("Arial", 14, "bold"))
    else:
        label = ctk.CTkLabel(lose, text="⌛ВРЕМЯ ВЫШЛО⌛", font=("Arial", 14, "bold"))
    label.pack(expand=True)
    open_all_mines()
    
    btn_menu = ctk.CTkButton(lose, text="В меню", width=10, command=lambda: restart(lose))
    btn_menu.pack(side=tk.BOTTOM, pady=10)

    # Блокировка основного окна при открытии окна поражения
    lose.grab_set()
    lose.focus_set()

    # При закрытии окна крестиком срабатывает выход в меню
    lose.protocol("WM_DELETE_WINDOW", lambda: restart(lose))

# Функция перезапуска игры
def restart(windows):
    pygame.mixer.music.stop()
    windows.destroy()
    os.execl(sys.executable, sys.executable, *sys.argv) # Перезапуск кода
# *sys.argv применяет текущие аргументы командой строки, sys.executable исходный путь к интерпритатору

# ФУНКЦИЯ ОКНА ОТЛАДКИ  
def debug():
    debug_win = ctk.CTkToplevel(root)
    debug_win.title("Debug")
    debug_win.resizable(True, False)
    debug_win.attributes('-topmost', True) # Чтобы окно поверх вылазило
    
    # Конвертируем матрицу в табличный вид 
    matrix_table = ""
    for row in matrix:               
        for cell in row:            
            matrix_table += str(cell) + "   " 
        matrix_table += "\n"
        
    label_name = ctk.CTkLabel(debug_win, text="Матрица мин", font=("Arial", 16, "bold"))
    label_name.pack(side=tk.TOP, pady=25)
    label = ctk.CTkLabel(debug_win, text=matrix_table, font=("Arial", 12, "bold"))
    label.pack(expand=True, padx=25, pady=25)
                                     
# КНОПКИ
frame_bottom = ctk.CTkFrame(root, fg_color="transparent")
frame_bottom.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

center_frame = ctk.CTkFrame(frame_bottom, fg_color="transparent")
center_frame.pack(expand=True)

# Кнопка влево
tk_button_left = ClassButton(center_frame, text="Left", command=mleft)
tk_button_left.pack(side=tk.LEFT, padx=1)

# Фрейм под кнопки Up и Down
frame_ud = ctk.CTkFrame(center_frame, fg_color="transparent")
frame_ud.pack(side=tk.LEFT, padx=1)

# Кнопка вверх
tk_button_up = ClassButton(frame_ud, text="Up", command=mup)
tk_button_up.pack(side=tk.TOP, padx=1)

# Кнопка вниз
tk_button_down = ClassButton(frame_ud, text="Down", command=mdown)
tk_button_down.pack(side=tk.BOTTOM, padx=1)

# Кнопка вправо
tk_button_right = ClassButton(center_frame, text="Right", command=mright)
tk_button_right.pack(side=tk.LEFT, padx=1)

# Кнопка открыть
tk_button_open = ClassButton(center_frame, text="Open", command=scan)
tk_button_open.pack(side=tk.LEFT, padx=20)

# Кнопка флажка
tk_button_flag = ClassButton(center_frame, text="Flag", command=flag)
tk_button_flag.pack(side=tk.LEFT, padx=1)            

root.mainloop()