import tkinter as tk
from tkinter import colorchooser
import customtkinter as ctk
import webbrowser
import os
import sys
try:
    import pygame
except ImportError:
    os.system('pip install pygame')
    os.system('pip install pygame-ce')
    os.execl(sys.executable, sys.executable, *sys.argv)
try:
    from PIL import Image, ImageTk, ImageSequence
except ImportError:
    os.system('pip install Pillow')
  
music_vol = 0.3
sfx_vol = 0.5   
  
# Функция загрузки настроек из файла
def load_audio_settings():
    global music_vol, sfx_vol
    if os.path.exists("audio_settings.txt"): # Проверка наличия файла
        try:
            with open("audio_settings.txt", "r") as f:
                lines = f.readlines()
                music_vol = float(lines[0].strip())
                sfx_vol = float(lines[1].strip())
        except Exception:
            pass

# Функция сохранения настроек в файл
def save_audio_settings():
    with open("audio_settings.txt", "w") as f:
        f.write(f"{music_vol}\n{sfx_vol}") 
 
pygame.mixer.init()
load_audio_settings()

snd_open = pygame.mixer.Sound("sounds//open.mp3")
snd_loose = pygame.mixer.Sound("sounds//loose.mp3")
snd_win = pygame.mixer.Sound("sounds//win.mp3")
snd_open.set_volume(sfx_vol)
snd_win.set_volume(sfx_vol)
snd_loose.set_volume(sfx_vol)

rows = 10 # Количество строк
cols = 10 # Количество колонок
difficult = 1 # Сложность
cell_size = 50 # Размер клетки
cell_def_color = "#474747" # Цвет клеток
cell_open_color = "#CDCDCD" # Цвет чистой клетки
cell_outline_color = "#0006bd" # Цвет активной обводки
flag_color = "#0c8628" # Цвет флага
timer = 0 # таймер сеунд на прохождение игры
theme_color = "system" # light,dark или system

ctk.set_appearance_mode(theme_color) # Глобальная тема зависящая от системных настроек
ctk.set_default_color_theme("dark-blue") # Глобальная цветовая тема

ctk.deactivate_automatic_dpi_awareness()

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

class ErrorWindow(ctk.CTkToplevel):
    def __init__ (self, master, error_text, size):
        super().__init__(master)
        self.title("Ошибка")
        self.geometry(size)
        self.resizable(False, False)
        label = ctk.CTkLabel(self, text=error_text, font=("Arial", 16, "bold"))
        label.pack(expand=True, pady=10)
        btn = ClassButton(self, text="Ок", command=self.destroy)
        btn.pack(side="bottom", pady=10)
        self.attributes('-topmost', True) # Чтобы ошибка поверх вылазила

# Настройки для игры
game_mode = 'single'

settings = [rows, cols, difficult, cell_size, cell_def_color, cell_open_color, cell_outline_color, flag_color, timer]
root = ctk.CTk() 

# Отрисовка тестового отображения клеток
def tryy():
    global rows, cols, difficult, cell_size, cell_def_color, cell_open_color, cell_outline_color, flag_color, settings, timer
    
    # Проверка ввода на некорректные типы данных
    try:
        cell_size = int(size_cell.get())
        difficult = int(difficultf.get())
        rows = cols = int(size.get())
        timer = int(timer_enter.get())
    except ValueError:
        ErrorWindow(root, "Введён некорректный тип данных", "350x100")
        return

    # Проверка диапазонов
    if rows < 5 or rows > 25:
        ErrorWindow(root, "Введите размер поля в диапазоне от 5 до 25", "450x100")
        return
        
    elif difficult < 1 or difficult > 10:
        ErrorWindow(root, "Введите сложность в\nдиапазоне от 1 до 10", "300x120")  
        return
        
    elif cell_size < 10:
        ErrorWindow(root, "Введите размер\nклетки больше 10", "230x120")
        return  

    elif timer < 0:
        ErrorWindow(root, "Введите положительное значение времени,\nили 0 для отключения таймера", "400x120")
        return
        
    canvas.delete("all")
    canvas.create_rectangle(100, 100, 100 + cell_size, 100 + cell_size, fill=cell_open_color)
    canvas.create_rectangle(100, 100, 100 + cell_size, 100 + cell_size, outline="black", width=1)
    canvas.create_rectangle(99, 99, 100 + cell_size + 1, 100 + cell_size + 1, outline="black", width=1)
    canvas.create_rectangle(102 + cell_size, 100, 102 + cell_size + cell_size, 100 + cell_size, fill=cell_def_color)
    canvas.create_rectangle(102 + cell_size, 100, 102 + cell_size + cell_size, 100 + cell_size, outline=cell_outline_color, width=1)
    canvas.create_rectangle(102 + cell_size, 99, 102 + cell_size + cell_size + 1, 100 + cell_size + 1, outline=cell_outline_color, width=1)
    canvas.create_text(102 + cell_size + cell_size/2, 98 + cell_size/2, text="🚩", font=("Arial", round(cell_size/3),"bold"), fill=flag_color)
    canvas.create_text(100 + + cell_size/2, 100 + cell_size/2, text="1", font=("Arial", round(cell_size/3),"bold"), fill="blue")


    cell_size = int(size_cell.get())
    calculate_max_size()

    
# По хорошему переписать одной функцией, но что-то не хочу
def choose_color():
    global cell_def_color
    color = colorchooser.askcolor()[1]
    if color:
        cell_def_color = color
    print(cell_def_color)
    tryy()

def choose_color2():
    global cell_open_color
    color = colorchooser.askcolor()[1]
    if color:
        cell_open_color = color
    print(cell_open_color)
    tryy()

def choose_color3():
    global cell_outline_color
    color = colorchooser.askcolor()[1]
    if color:
        cell_outline_color = color
    print(cell_outline_color)
    tryy()
    
def choose_color4():
    global flag_color
    color = colorchooser.askcolor()[1]
    if color:
        flag_color = color
    print(flag_color)
    tryy()

def start():

    global rows, cols, difficult, cell_size, cell_def_color, cell_open_color, cell_outline_color, flag_color, settings, timer
    # Проверка ввода на некорректные типы данных
    try:
        cell_size = int(size_cell.get())
        difficult = int(difficultf.get())
        rows = cols = int(size.get())
        timer = int(timer_enter.get())
    except ValueError:
        ErrorWindow(root, "Введён некорректный тип данных", "350x100")
        return
    
    # Проверка диапазонов
    if rows < 5 or rows > 25:
        ErrorWindow(root, "Введите размер поля в диапазоне от 5 до 25", "450x100")
        return 
        
    elif difficult < 1 or difficult > 10:
        ErrorWindow(root, "Введите сложность в\nдиапазоне от 1 до 10", "300x120")  
        return
        
    elif cell_size < 10:
        ErrorWindow(root, "Введите размер\nклетки больше 10", "230x120")
        return
    
    elif timer < 0:
        ErrorWindow(root, "Введите положительное значение времени,\nили 0 для отключения таймера", "260x120")
        return
    
    settings = [rows, cols, difficult, cell_size, cell_def_color, cell_open_color, cell_outline_color, flag_color, timer]
    print(settings)
    root.quit()


# Функция для расчёта максимального рекомендованного размера поля в зависимости от размера клетки и разрешения экрана           
def calculate_max_size():
    try:
        c_size = int(size_cell.get())
        if c_size > 0:
            screen_w = root.winfo_screenwidth()
            screen_h = root.winfo_screenheight()

            max_safe = min((screen_w - 54) // (c_size + 1), (screen_h - 200) // (c_size + 1))
            
            lbl_recommended.configure(text=f"Макс. рекомендований розмір поля: {max_safe}")
    except ValueError:
        pass

# Основное меню
def menu():
    global rows, cols, difficult, cell_size, cell_def_color, cell_open_color, cell_outline_color, flag_color, settings, size, difficultf, size_cell, root, timer_enter
    root.title("Меню настроек игры")
    root.geometry("600x630")
    root.resizable(False, False)

    # Левый фрейм
    frame_left = ctk.CTkFrame(root, width=300, height=630)
    frame_left.pack(side="left")
    frame_left.pack_propagate(False)
    
    # Выясняем размеры поля
    label = ctk.CTkLabel(frame_left, text="Размер поля в клетках (от 5 до 25)")
    label.pack(pady=5)
    size = ctk.CTkEntry(frame_left)
    size.insert(0, 10)
    size.pack(pady=5)
   
    # Выясняем сложность
    label = ctk.CTkLabel(frame_left, text="Сложность от 1 до 10")
    label.pack(pady=5)
    difficultf = ctk.CTkEntry(frame_left)
    difficultf.insert(0, 5)
    difficultf.pack(pady=5)
    
    # Выясняем размер клетки
    label = ctk.CTkLabel(frame_left, text="Размер клетки в пикселях (от 10)")
    label.pack(pady=5)
    size_cell = ctk.CTkEntry(frame_left)
    size_cell.insert(0, 50)
    size_cell.pack(pady=5)
    
    # Рекомендация по максимальному размеру поля в зависимости от размера клетки и разрешения экрана
    global lbl_recommended
    lbl_recommended = ctk.CTkLabel(frame_left, text="", text_color="red", font=("Arial", 12, "bold"))
    lbl_recommended.pack(pady=0)
    calculate_max_size()    
    
    # Выясняем размер таймера
    label = ctk.CTkLabel(frame_left, text="Время на прохождение игры\n(в секундах, 0 - без таймера)")
    label.pack(pady=5)
    timer_enter = ctk.CTkEntry(frame_left)
    timer_enter.insert(0, 0)
    timer_enter.pack(pady=5)
    
    # Выясняем цвет келток по умолчанию
    label = ctk.CTkLabel(frame_left, text="Цвет клеток по умолчанию")
    label.pack(pady=5)
    btn = ClassButton(frame_left, text="Выбрать цвет", command=choose_color)
    btn.pack(pady=5)
    
    # Выясняем цвет открытх келток
    label = ctk.CTkLabel(frame_left, text="Цвет открытых клеток")
    label.pack(pady=5)
    btn2 = ClassButton(frame_left, text="Выбрать цвет", command=choose_color2)
    btn2.pack(pady=5)
    
    # Выясняем цвет активной обводки
    label = ctk.CTkLabel(frame_left, text="Цвет Активной обводки")
    label.pack(pady=5)
    btn3 = ClassButton(frame_left, text="Выбрать цвет", command=choose_color3)
    btn3.pack(pady=5)
    
    # Выясняем цвет чистых флага
    label = ctk.CTkLabel(frame_left, text="Цвет флага")
    label.pack(pady=5)
    btn4 = ClassButton(frame_left, text="Выбрать цвет", command=choose_color4)
    btn4.pack(pady=5)

    # Правый фрейм 
    frame_right = ctk.CTkFrame(root, width=300, height=630)
    frame_right.pack(side="right")
    frame_right.pack_propagate(False) # Судя с инета, это фиксирует размеры фрейма, бо без него чёт всё с`езжает
    global canvas
    canvas = tk.Canvas(frame_right, width=280, height=200, bg="#9A9A9A", highlightthickness=0, borderwidth=0)
    canvas.pack(pady=20)

    # Кнопка и надпись справа
    label = ctk.CTkLabel(frame_right, text="Если не выставить настройки,\nбудут применены настройки по умолчанию")
    label.pack(pady=10)
    label = ctk.CTkLabel(frame_right, text="Вводите значения в формате\n целых чисел без единиц измерения", font=("Arial", 14), text_color="red")
    label.pack(pady=10)
    btn_try = ClassButton(frame_right, text="Опробовать", command=tryy)
    btn_try.pack(side=tk.BOTTOM, pady=10) # ВНИМАНИЕ ЯРИК!!! PADY ЭТО ОТСТУП ПО Y, PADX ПО X. ВРОДЕ ЛОГИЧНО НО ЧТО-ТО НЕ ПОНЯТНО.
    if game_mode == 'single':
        btn_start = ClassButton(frame_right, text="Старт", command=start)
        btn_start.pack(side=tk.BOTTOM, pady=10)    
    
root.withdraw() # Прячем "Родительское" меню

def setting_window():
    global sett_w, root
    sett_w = ctk.CTkToplevel(root)
    sett_w.title("Настройки звука")
    sett_w.geometry("350x250")
    sett_w.resizable(False, False)
    sett_w.attributes('-topmost', True)
    
    def update_music_vol(value):
        global music_vol
        music_vol = float(value)
        pygame.mixer.music.set_volume(music_vol)
        save_audio_settings()
    
    def update_sfx_vol(value):
        global sfx_vol
        sfx_vol = float(value)
        snd_open.play()
        snd_open.set_volume(sfx_vol)
        snd_win.set_volume(sfx_vol)
        snd_loose.set_volume(sfx_vol)
        save_audio_settings()
    
    label = ctk.CTkLabel(sett_w, text="Громкость музыки:", font=("Arial", 14))
    label.pack(pady=15)
    slider_music = ctk.CTkSlider(sett_w, from_=0.0, to=1.0, number_of_steps=20, command=update_music_vol) # from_ минимальное значение, to - максимальное значение, command - функция при изменении ползунка!
    slider_music.set(music_vol) # Ставим ползунок на текущее значение
    slider_music.pack(pady=5)

    label = ctk.CTkLabel(sett_w, text="Громкость эффектов:", font=("Arial", 14))
    label.pack(pady=15)
    slider_sfx = ctk.CTkSlider(sett_w, from_=0.0, to=1.0,number_of_steps=20, command=update_sfx_vol) # number_of_steps можно задать сколько шагов есть у слайдера
    slider_sfx.set(sfx_vol) # Ставим ползунок на текущее значение
    slider_sfx.pack(pady=15)
    
    label = ctk.CTkLabel(sett_w, text="Вы можете нажать \"M\" на клавиатуре\nво время игры, для смены настроек", font=("Arial", 14))
    label.pack(pady=10)

    ctk.CTkButton(sett_w, text="Закрыть", command=sett_w.destroy, width=120).pack(pady=(20, 10))

def single_st():
    global game_mode
    game_mode = 'single'
    select.destroy()
    root.deiconify() # Показываем "Родительское" меню
    menu()

def open_browser():
    webbrowser.open_new_tab("https://github.com/TheInfani/Saper_kursach")

def destroy_st():
    try:
        sett_w.destroy()
    except Exception:
        pass

def win_select_mode():
    global select, root, sett_w
    select = ctk.CTkToplevel(root)
    select.title("Выбор режима")
    select.geometry("350x200")
    select.resizable(False, False)
    label =ctk.CTkLabel(select, text="Сапёр Офлайн", font=("Arial", 16, "bold"))
    label.pack(pady=15)
    single_btn = ClassButton(select, text="Одиночная игра", command=lambda: [select.destroy(),destroy_st(), single_st()])
    single_btn.pack(pady=10)
    github_btn = ClassButton(select, text="GitHub проекта", command=open_browser)
    github_btn.pack(pady=10)
    settings_btn = ClassButton(select, text="Настройки", command=setting_window)
    settings_btn.pack(pady=10)
    select.protocol("WM_DELETE_WINDOW", lambda: root.destroy())

win_select_mode()

root.mainloop()    