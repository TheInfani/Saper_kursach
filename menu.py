import tkinter as tk
from tkinter import colorchooser
import webbrowser
import os
import sys
import json
try:
    import customtkinter as ctk
    import pygame
    from PIL import Image, ImageTk, ImageSequence
except ImportError:
    os.system('pip install -r requirements.txt')
    os.execl(sys.executable, sys.executable, *sys.argv)
    
music_vol = 0.3
sfx_vol = 0.5   
button_visible = None # Видимость кнопок управления, по умолчанию включены
theme_color = None # light,dark или system

# Функция загрузки настроек из файла
def load_audio_settings():
    global music_vol, sfx_vol, button_visible, theme_color
    if os.path.exists("settings.txt"): # Проверка наличия файла
        try:
            with open("settings.txt", "r") as f:
                lines = f.readlines()
                music_vol = float(lines[0].strip())
                sfx_vol = float(lines[1].strip())
                button_visible = lines[2].strip() == "True" # Читаем как строку и преобразуем в булево значение
                theme_color = lines[3].strip() # light,dark или system
                set_cell_colors() # Устанавливаем цвета клеток в зависимости от темы
        except Exception:
            pass

# Функция сохранения настроек в файл
def save_audio_settings():
    with open("settings.txt", "w") as f:
        f.write(f"{music_vol}\n{sfx_vol}\n{button_visible}\n{theme_color}") 
 
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
def set_cell_colors():
    global cell_def_color, cell_open_color
    if theme_color == "light":
        cell_def_color = "#A9A9A9" # Цвет клеток
        cell_open_color = "#F6F6F6" # Цвет чистой клетки
    else:
        cell_def_color = "#474747" # Цвет клеток
        cell_open_color = "#CDCDCD" # Цвет чистой клетки
set_cell_colors()
cell_outline_color = "#0006bd" # Цвет активной обводки
flag_color = "#0c8628" # Цвет флага
timer = 0 # таймер сеунд на прохождение игры

ctk.set_appearance_mode(theme_color) # Глобальная тема зависящая от системных настроек
ctk.set_default_color_theme("dark-blue") # Глобальная цветовая тема

ctk.deactivate_automatic_dpi_awareness()

class ClassButton(ctk.CTkButton):
    def __init__(self, master, text, command,
                 fg_color=("#D9D8D8", "#515151"),
                 hover_color=("#BABABA", "#373737")):

        def command_with_sound():
            snd_open.play()
            command()

        super().__init__(
            master=master,              # root
            text=text,                  # Текст на кнопке
            command=command_with_sound, # Функция при нажатии
            width=110,                  # Ширина
            height=25,                  # Высота
            fg_color=fg_color,          # Цвет кнопки
            hover_color=hover_color,    # Цвет кнопки при наведении
            text_color=("black", "white"), # Цвет текста
            corner_radius=8,            # Закругленные углы
            font=ctk.CTkFont(size=12)   # Шрифт
        )

class ErrorWindow(ctk.CTkToplevel):
    def __init__ (self, master, error_text, size):
        super().__init__(master)
        self.title("Помилка")
        self.geometry(size)
        self.resizable(False, False)
        label = ctk.CTkLabel(self, text=error_text, font=("Arial", 16, "bold"))
        label.pack(expand=True, pady=10)
        btn = ClassButton(self, text="Ок", command=self.destroy)
        btn.pack(side="bottom", pady=10)
        self.attributes('-topmost', True) # Чтобы ошибка поверх вылазила

# Настройки для игры
game_mode = 'single'

settings = [rows, cols, difficult, cell_size, cell_def_color, cell_open_color, cell_outline_color, flag_color, timer, button_visible, theme_color]
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
        ErrorWindow(root, "Введено некоректний тип даних", "350x100")
        return

    # Проверка диапазонов
    if rows < 7 or rows > 50:
        ErrorWindow(root, "Введіть розмір поля в діапазоні від 7 до 50", "450x100")
        return
        
    elif difficult < 1 or difficult > 10:
        ErrorWindow(root, "Введіть складність в\nдіапазоні від 1 до 10", "300x120")  
        return
        
    elif cell_size < 10:
        ErrorWindow(root, "Введіть розмір\nклітинки більше 10", "230x120")
        return  

    elif timer < 0:
        ErrorWindow(root, "Введіть додатне значення часу,\nчи 0 для відключення таймера", "400x120")
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

    global rows, cols, difficult, cell_size, cell_def_color, cell_open_color, cell_outline_color, flag_color, settings, timer, button_visible, theme_color
    # Проверка ввода на некорректные типы данных
    try:
        cell_size = int(size_cell.get())
        difficult = int(difficultf.get())
        rows = cols = int(size.get())
        timer = int(timer_enter.get())
    except ValueError:
        ErrorWindow(root, "Введено некоректний тип даних", "350x100")
        return
    
    # Проверка диапазонов
    if rows < 7 or rows > 50:
        ErrorWindow(root, "Введіть розмір поля в діапазоні від 7 до 50", "450x100")
        return 
        
    elif difficult < 1 or difficult > 10:
        ErrorWindow(root, "Введіть складність в\nдіапазоні від 1 до 10", "300x120")  
        return
        
    elif cell_size < 10:
        ErrorWindow(root, "Введіть розмір\nклітинки більше 10", "230x120")
        return
    
    elif timer < 0:
        ErrorWindow(root, "Введіть додатне значення часу,\nчи 0 для відключення таймера", "400x120")
        return
    
    settings = [rows, cols, difficult, cell_size, cell_def_color, cell_open_color, cell_outline_color, flag_color, timer, button_visible, theme_color]
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
    

# Данные пресетов: [Название, Размер, Сложность, Размер клетки]
presets_data = [
    ["По замовчуванню\n(10x10)", 10, 5, 50],
    ["Мінімальне поле\n(7x7)", 7, 5, 50],
    ["Найлегший\n(7x7)", 7, 1, 50],
    ["Поле 15 клітинок\n(15x15)", 15, 5, 50],
    ["Складність 10\n(10x10)", 10, 10, 50],
    ["Максимум\n(50x50)", 50, 10, 30]
]

# Функции для сохранения и загрузки пресетов настроек в файл
def save_presets():
    global presets_data
    with open("presets.json", "w", encoding='utf-8') as f:
        json.dump(presets_data, f, ensure_ascii=False, separators=(',', ': '), indent=4, sort_keys=False)
        
def load_presets():
    global presets_data
    try:
        with open("presets.json", "r", encoding='utf-8') as f:
            presets_data = json.load(f)
    except Exception:
        pass

load_presets() # Загружаем пресеты при запуске

# Функция для применения пресета
def apply_preset(p_size, p_diff, p_cell):
    size.delete(0, tk.END)
    size.insert(0, p_size)
    difficultf.delete(0, tk.END)
    difficultf.insert(0, p_diff)
    size_cell.delete(0, tk.END)
    size_cell.insert(0, p_cell)
    tryy() # Обновляем предпросмотр
            
def refresh_scroll_pres():
    global scroll_pres_frame
    for widget in scroll_pres_frame.winfo_children():
        widget.destroy()

    for i in presets_data:
        preset_button = ctk.CTkButton(scroll_pres_frame, text=i[0], command=lambda val=i: apply_preset(val[1], val[2], val[3]), height=60, width=250)
        preset_button.pack(pady=5) #fill="x"

# Основное меню
def menu():
    global rows, cols, difficult, cell_size, cell_def_color, cell_open_color, cell_outline_color, flag_color, settings, size, difficultf, size_cell, root, timer_enter, presets_data
    root.title("Меню налаштувань гри")
    root.geometry("900x670")
    root.resizable(False, False)

    # Левый фрейм
    frame_left = ctk.CTkFrame(root, width=300, height=670, corner_radius=0, fg_color="transparent")
    frame_left.pack(side="left")
    frame_left.pack_propagate(False)
    label = ctk.CTkLabel(frame_left, text="Налаштування гри", font=("Arial", 16, "bold"))
    label.pack(pady=5)
    
    # Выясняем размеры поля
    label = ctk.CTkLabel(frame_left, text="Розмір поля в клітинках (від 7 до 50)")
    label.pack(pady=5)
    size = ctk.CTkEntry(frame_left)
    size.insert(0, 10)
    size.pack(pady=5)
   
    # Выясняем сложность
    label = ctk.CTkLabel(frame_left, text="Складність (від 1 до 10)")
    label.pack(pady=5)
    difficultf = ctk.CTkEntry(frame_left)
    difficultf.insert(0, 5)
    difficultf.pack(pady=5)
    
    # Выясняем размер клетки
    label = ctk.CTkLabel(frame_left, text="Розмір клітинки в пікселях (від 10)")
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
    label = ctk.CTkLabel(frame_left, text="Час на проходження гри\n(в секундах, 0 - без таймера)")
    label.pack(pady=5)
    timer_enter = ctk.CTkEntry(frame_left)
    timer_enter.insert(0, 0)
    timer_enter.pack(pady=5)
    
    # Выясняем цвет келток по умолчанию
    label = ctk.CTkLabel(frame_left, text="Колір клітинок по замовчуванню")
    label.pack(pady=5)
    btn = ClassButton(frame_left, text="Вибрати колір", command=choose_color)
    btn.pack(pady=5)
    
    # Выясняем цвет открытх келток
    label = ctk.CTkLabel(frame_left, text="Колір відкритих клітинок")
    label.pack(pady=5)
    btn2 = ClassButton(frame_left, text="Вибрати колір", command=choose_color2)
    btn2.pack(pady=5)
    
    # Выясняем цвет активной обводки
    label = ctk.CTkLabel(frame_left, text="Колір активної обводки")
    label.pack(pady=5)
    btn3 = ClassButton(frame_left, text="Вибрати колір", command=choose_color3)
    btn3.pack(pady=5)
    
    # Выясняем цвет чистых флага
    label = ctk.CTkLabel(frame_left, text="Колір прапорця")
    label.pack(pady=5)
    btn4 = ClassButton(frame_left, text="Вибрати колір", command=choose_color4)
    btn4.pack(pady=5)

    # Правый фрейм 
    frame_right = ctk.CTkFrame(root, width=300, height=670, corner_radius=0, fg_color="transparent")
    frame_right.pack(side="right")
    frame_right.pack_propagate(False) # Судя с инета, это фиксирует размеры фрейма, бо без него чёт всё с`езжает
    label =ctk.CTkLabel(frame_right, text="Попередній перегляд поля", font=("Arial", 16, "bold"))
    label.pack(pady=10)
    global canvas
    canvas = tk.Canvas(frame_right, width=280, height=200, bg="#929292", highlightthickness=0, borderwidth=0)
    canvas.pack(pady=20)

    # Кнопка и надпись справа
    label = ctk.CTkLabel(frame_right, text="Якщо не встановити налаштування,\nбудуть застосовані параметри\nза замовчуванням")
    label.pack(pady=10)
    label = ctk.CTkLabel(frame_right, text="Вводьте значення в форматі\n цілих чисел без одиниць виміру", font=("Arial", 14), text_color="red")
    label.pack(pady=10)
    btn_try = ClassButton(frame_right, text="Випробувати", command=tryy)
    btn_try.pack(side=tk.BOTTOM, pady=10) # ВНИМАНИЕ ЯРИК!!! PADY ЭТО ОТСТУП ПО Y, PADX ПО X. ВРОДЕ ЛОГИЧНО НО ЧТО-ТО НЕ ПОНЯТНО.
    if game_mode == 'single':
        btn_start = ClassButton(frame_right, text="Старт", command=start)
        btn_start.pack(side=tk.BOTTOM, pady=10) 
    
    # Фрейм пресетов настроек
    frame_presets = ctk.CTkFrame(root, width=300, height=670, fg_color="transparent", border_width=0, corner_radius=0)
    frame_presets.pack(side="right")
    frame_presets.pack_propagate(False)
    
    frame_list = ctk.CTkFrame(frame_presets, width=300, height=550,fg_color="transparent", corner_radius=0)
    frame_list.pack(side="top")
    frame_list.pack_propagate(False)

    label = ctk.CTkLabel(frame_list, text="Пресети налаштувань", font=("Arial", 16, "bold"))
    label.pack(pady=10)

    # Создаем прокручиваемую область
    global scroll_pres_frame
    scroll_pres_frame = ctk.CTkScrollableFrame(frame_list, width=180, height=550, border_width=0, corner_radius=0, fg_color="transparent", scrollbar_fg_color="transparent", scrollbar_button_color="#BABABA")
    scroll_pres_frame.pack(pady=5, padx=5, fill="both", expand=True)
    scroll_pres_frame._scrollbar.configure(width=0)

    # Создаем кнопки пресетов в цикле
    refresh_scroll_pres()
    
    def add_preset():
        p_size = size.get()
        p_diff = difficultf.get()
        p_cell = size_cell.get()
        if p_name.get() == "":
            preset_name = f"Пресет {len(presets_data)+1}\n({p_size}x{p_size})"
        else:
            preset_name = f"{p_name.get()}\n({p_size}x{p_size})"   
        presets_data.append([preset_name, p_size, p_diff, p_cell])
        preset_button = ctk.CTkButton(scroll_pres_frame, text=preset_name, command=lambda val=presets_data[-1]: apply_preset(val[1], val[2], val[3]), height=60, width=250)
        preset_button.pack(pady=5)
        save_presets()

    # Фрейм удаления пресетов
    frame_del_btn = ctk.CTkFrame(frame_presets, width=300, height=30, fg_color="transparent", border_width=0, corner_radius=0)
    frame_del_btn.pack(side=tk.BOTTOM, pady=5, padx=25)
    frame_del_btn.pack_propagate(False)
    
    del_btn = ctk.CTkButton(frame_del_btn, text="Меню видалення пресетів", command=window_presets_del, width=250, fg_color="#A30000", hover_color="#7A0000")
    del_btn.pack()
    
    # Кнопка добавления пресета
    add_button = ctk.CTkButton(frame_presets, text="Додати свій пресет", command=add_preset, width=250)
    add_button.pack(side=tk.BOTTOM, pady=5)
    
    p_name = ctk.CTkEntry(frame_presets, width=250)
    p_name.insert(0, "Назва пресету")
    p_name.pack(side=tk.BOTTOM, pady=5) 
    
def refresh_scroll():
    global scroll_del_frame
    for widget in scroll_del_frame.winfo_children():
        widget.destroy()
    
    for i in presets_data:
        btn = ctk.CTkButton(scroll_del_frame, text=i[0], height=60, width=250, fg_color="#A30000", hover_color="#7A0000")
        btn.configure(command=lambda p=i: delete_and_refresh(p))
        btn.pack(pady=5)  
        
# Функция удаления пресетов
def delete_and_refresh(preset_to_delete):
    if preset_to_delete in presets_data:
        presets_data.remove(preset_to_delete)
    save_presets()
    refresh_scroll()
    refresh_scroll_pres()
    
# Фрейм удаления пресетов
def window_presets_del():
    global w_delpres, root, records_data
    w_delpres = ctk.CTkToplevel(root)
    w_delpres.title("Видалення пресетів")
    w_delpres.geometry("300x670")
    w_delpres.resizable(False, False)
    w_delpres.attributes('-topmost', True)
    
    frame_pres_del = ctk.CTkFrame(w_delpres, width=300, height=600, fg_color="transparent", border_width=0, corner_radius=0)
    frame_pres_del.pack(side="right")
    frame_pres_del.pack_propagate(False)

    label = ctk.CTkLabel(frame_pres_del, text="Натисніть на пресет\nдля видалення", font=("Arial", 16, "bold"))
    label.pack(pady=5)

    # Создаем прокручиваемую область
    global scroll_del_frame
    scroll_del_frame = ctk.CTkScrollableFrame(frame_pres_del, width=300, height=600, border_width=0, corner_radius=0, fg_color="transparent", scrollbar_fg_color="transparent")
    scroll_del_frame.pack(pady=5, padx=5, fill="both", expand=True)
    scroll_del_frame._scrollbar.configure(width=0)

    # Создаем кнопки рекордов в цикле
    refresh_scroll()

root.withdraw() # Прячем "Родительское" меню

def setting_window():
    global sett_w, root
    sett_w = ctk.CTkToplevel(root)
    sett_w.title("Налаштування")
    sett_w.geometry("350x600")
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
    
    label = ctk.CTkLabel(sett_w, text="ЗВУКИ", font=("Arial", 16, "bold"))
    label.pack(pady=15)
    
    label = ctk.CTkLabel(sett_w, text="Гучність музики:", font=("Arial", 14))
    label.pack(pady=10)
    slider_music = ctk.CTkSlider(sett_w, from_=0.0, to=1.0, number_of_steps=20, command=update_music_vol) # from_ минимальное значение, to - максимальное значение, command - функция при изменении ползунка!
    slider_music.set(music_vol) # Ставим ползунок на текущее значение
    slider_music.pack(pady=5)

    label = ctk.CTkLabel(sett_w, text="Гучність ефектів:", font=("Arial", 14))
    label.pack(pady=10)
    slider_sfx = ctk.CTkSlider(sett_w, from_=0.0, to=1.0,number_of_steps=20, command=update_sfx_vol) # number_of_steps можно задать сколько шагов есть у слайдера
    slider_sfx.set(sfx_vol) # Ставим ползунок на текущее значение
    slider_sfx.pack(pady=15)
    
    label = ctk.CTkLabel(sett_w, text="Ви можете натиснути \"S\" на клавіатурі\nпід час гри, для зміни налаштувань", font=("Arial", 12), text_color="gray")
    label.pack(pady=10)

    label = ctk.CTkLabel(sett_w, text="ЗАГАЛЬНЕ", font=("Arial", 16, "bold"))
    label.pack(pady=15)
    
    # Чекбокс для отображения кнопок управления
    buttons_var = ctk.BooleanVar(value=button_visible) # Надо ибо чекбокс не работает с дефф булианами
    def on_check():
        global button_visible
        button_visible = buttons_var.get()
        save_audio_settings() 
        
    chekboks_themes = ctk.CTkCheckBox(sett_w, text="Увімкнути відображення кнопок", variable=buttons_var, onvalue=True, offvalue=False, command=on_check)
    chekboks_themes.pack(pady=6)
    label = ctk.CTkLabel(sett_w, text="Зміниться в наступній грі", font=("Arial", 12), text_color="gray")
    label.pack(pady=5)
    
    # Чекбокс для темы
    theme_var = ctk.StringVar(value=theme_color)
    def on_theme_change():
        global theme_color
        theme_color = theme_var.get()
        save_audio_settings()
        ctk.set_appearance_mode(theme_color) # Глобальная тема зависящая от системных настроек
        set_cell_colors() # Устанавливаем цвета клеток в зависимости от темы
        

    chekboks_theme = ctk.CTkRadioButton(sett_w, text="Системна тема", variable=theme_var, value="system", command=on_theme_change)
    chekboks_theme.pack(pady=6)
    chekboks_theme2 = ctk.CTkRadioButton(sett_w, text="Світла тема", variable=theme_var, value="light", command=on_theme_change)
    chekboks_theme2.pack(pady=6)
    chekboks_theme3 = ctk.CTkRadioButton(sett_w, text="Темна тема", variable=theme_var, value="dark", command=on_theme_change)
    chekboks_theme3.pack(pady=6)

    label = ctk.CTkLabel(sett_w, text="\"Права\" на музику належать YarikGamarnik\nДякую Nek0Anim3 за зведення", font=("Arial", 12), text_color="gray")
    label.pack(pady=20)

def single_st():
    global game_mode
    game_mode = 'single'
    select.destroy()
    root.deiconify() # Показываем "Родительское" меню
    menu()

def open_browser():
    webbrowser.open_new_tab("https://github.com/TheInfani/Saper_kursach")

# таблица рекордов (очки, время прохождения, сложность, размер, количество мин)      очки = (количество мин * слоность * размер поля) / (время прохождения / (количество мин * сложность))
records_data = [
]
# [4348, 23, 5, 10, 20]

# Функции для загрузки рекордов
def load_records():
    global records_data
    try:
        with open("records.json", "r", encoding='utf-8') as f:
            records_data = json.load(f)
        records_data.sort(key=lambda x: x[0], reverse=True)
    except Exception:
        pass

def records_window():
    load_records()
    global w_records, root, records_data
    w_records = ctk.CTkToplevel(root)
    w_records.title("Рекорди")
    w_records.geometry("300x670")
    w_records.resizable(False, False)
    w_records.attributes('-topmost', True)
    
    # Фрейм рекордов
    frame_records = ctk.CTkFrame(w_records, width=300, height=670, fg_color="transparent", border_width=0, corner_radius=0)
    frame_records.pack(side="right")
    frame_records.pack_propagate(False)
        
    frame_record_list = ctk.CTkFrame(frame_records, width=300, height=570, fg_color="transparent")
    frame_record_list.pack(side="top")
    frame_record_list.pack_propagate(False)

    label = ctk.CTkLabel(frame_record_list, text="Рекорди", font=("Arial", 16, "bold"))
    label.pack(pady=10)

    # Создаем прокручиваемую область
    scroll_frame = ctk.CTkScrollableFrame(frame_record_list, width=180, height=500, border_width=0, corner_radius=0, fg_color="transparent", scrollbar_fg_color="transparent")
    scroll_frame.pack(pady=5, padx=5, fill="both", expand=True)
    scroll_frame._scrollbar.configure(width=0)


    # Создаем кнопки рекордов в цикле
    for i in records_data:
        preset_button = ctk.CTkButton(scroll_frame, text=f"Очок: {i[0]}  Час (секунди): {i[1]}\nСкладність: {i[2]}  Розмір поля: {i[3]}  Мін: {i[4]}", height=60)
        preset_button.pack(pady=5, fill="x")
        
def destroy_st():
    try:
        sett_w.destroy()
    except Exception:
        pass

def destroy_rec():
    try:
        w_records.destroy()
    except Exception:
        pass

def win_select_mode():
    global select, root, sett_w
    select = ctk.CTkToplevel(root)
    select.title("Головне меню")
    select.geometry("350x250")
    select.resizable(False, False)
    label =ctk.CTkLabel(select, text="Сапёр Офлайн", font=("Arial", 16, "bold"))
    label.pack(pady=15)
    single_btn = ClassButton(select, text="Почати гру", fg_color=("#4CAF50", "#2E7D32"), hover_color=("#66BB6A", "#388E3C"), command=lambda: [select.destroy(),destroy_st(),single_st(),destroy_rec()])
    single_btn.pack(pady=10)
    github_btn = ClassButton(select, text="GitHub проекту", fg_color=("#D6D6D6", "#8A8A8A"), hover_color=("#C0C0C0", "#707070"), command=open_browser)
    github_btn.pack(pady=10)
    settings_btn = ClassButton(select, text="Налаштування", fg_color=("#9E9E9E", "#5F5F5F"), hover_color=("#B0B0B0", "#707070"), command=setting_window)
    settings_btn.pack(pady=10)
    rec_btn = ClassButton(select, text="Рекорди", fg_color=("#42A5F5", "#1565C0"), hover_color=("#64B5F6", "#1976D2"), command=records_window)
    rec_btn.pack(pady=10)
    select.protocol("WM_DELETE_WINDOW", lambda: root.destroy())

win_select_mode()

root.mainloop()