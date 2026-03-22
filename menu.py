import socket
import tkinter as tk
from tkinter import colorchooser
import customtkinter as ctk

rows = 10 # Количество строк
cols = 10 # Количество колонок
difficult = 1 # Сложность
cell_size = 50 # Размер клетки
cell_def_color = "#474747" # Цвет клеток
cell_open_color = "#CDCDCD" # Цвет чистой клетки
cell_outline_color = "#0006bd" # Цвет активной обводки
flag_color = "#0c8628" # Цвет флага

ctk.set_appearance_mode("system") # Глобальная тема зависящая от системных настроек
ctk.set_default_color_theme("dark-blue") # Глобальная цветовая тема

ctk.deactivate_automatic_dpi_awareness()

class ClassButton(ctk.CTkButton):
    def __init__(self, master, text, command):
        super().__init__(
            master=master,             # root
            text=text,                 # Текст на кнопке
            command=command,           # Функция при нажатии
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

# Настройки для сетевой игры
game_mode = 'single'
# player_name = 'Игрок'
# host_ip = '127.0.0.1'

settings = [rows, cols, difficult, cell_size, cell_def_color, cell_open_color, cell_outline_color, flag_color, game_mode]
root = ctk.CTk() 

# Отрисовка тестового отображения клеток
def tryy():
    global rows, cols, difficult, cell_size, cell_def_color, cell_open_color, cell_outline_color, flag_color, settings, incorect
    
    # Проверка ввода на некорректные типы данных
    try:
        cell_size = int(size_cell.get())
        difficult = int(difficultf.get())
        rows = cols = int(size.get())
    except ValueError:
        ErrorWindow(root, "Введён некорректный тип данных", "350x100")
        return

    # Проверка диапазонов
    if rows < 5 or rows > 25:
        ErrorWindow(root, "Введите размер поля в диапазоне от 5 до 25", "450x100")
        return # Снова останавливаем функцию при ошибке
        
    elif difficult < 1 or difficult > 10:
        ErrorWindow(root, "Введите сложность в\nдиапазоне от 1 до 10", "300x120")  
        return
        
    elif cell_size < 10:
        ErrorWindow(root, "Введите размер\nклетки больше 10", "230x120")
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

    global rows, cols, difficult, cell_size, cell_def_color, cell_open_color, cell_outline_color, flag_color, settings, incorect 
    # Проверка ввода на некорректные типы данных
    try:
        cell_size = int(size_cell.get())
        difficult = int(difficultf.get())
        rows = cols = int(size.get())
    except ValueError:
        ErrorWindow(root, "Введён некорректный тип данных", "350x100")
        return
    
    # Проверка диапазонов
    if rows < 5 or rows > 25:
        ErrorWindow(root, "Введите размер поля в диапазоне от 5 до 25", "450x100")
        return # Снова останавливаем функцию при ошибке
        
    elif difficult < 1 or difficult > 10:
        ErrorWindow(root, "Введите сложность в\nдиапазоне от 1 до 10", "300x120")  
        return
        
    elif cell_size < 10:
        ErrorWindow(root, "Введите размер\nклетки больше 10", "230x120")
        return
    settings = [rows, cols, difficult, cell_size, cell_def_color, cell_open_color, cell_outline_color, flag_color, game_mode]
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
    global rows, cols, difficult, cell_size, cell_def_color, cell_open_color, cell_outline_color, flag_color, settings, size, difficultf, size_cell, root
    root.title("Меню настроек игры")
    root.geometry("600x480")
    root.resizable(False, False)

    # Левый фрейм
    frame_left = ctk.CTkFrame(root, width=300, height=480)
    frame_left.pack(side="left")
    frame_left.pack_propagate(False)
    
    # Выясняем размеры поля
    label = ctk.CTkLabel(frame_left, text="Размер поля (в клетках)")
    label.pack(pady=5)
    size = ctk.CTkEntry(frame_left)
    size.insert(0, 10)
    size.pack(pady=5)
   
    # Выясняем сложность
    label = ctk.CTkLabel(frame_left, text="Сложность 1-10")
    label.pack(pady=5)
    difficultf = ctk.CTkEntry(frame_left)
    difficultf.insert(0, 5)
    difficultf.pack(pady=5)
    
    # Выясняем размер клетки
    label = ctk.CTkLabel(frame_left, text="Размер клетки в пикселях")
    label.pack(pady=5)
    size_cell = ctk.CTkEntry(frame_left)
    size_cell.insert(0, 50)
    size_cell.pack(pady=5)
    
    # Рекомендация по максимальному размеру поля в зависимости от размера клетки и разрешения экрана
    global lbl_recommended
    lbl_recommended = ctk.CTkLabel(frame_left, text="", text_color="red", font=("Arial", 12, "bold"))
    lbl_recommended.pack(pady=0)
    calculate_max_size()
    
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
    frame_right = ctk.CTkFrame(root, width=300, height=480)
    frame_right.pack(side="right")
    frame_right.pack_propagate(False) # Судя с инета, это фиксирует размеры фрейма, бо без него чёт всё с`езжает
    global canvas
    canvas = tk.Canvas(frame_right, width=280, height=200, bg="#595959", highlightthickness=0, borderwidth=0)
    canvas.pack(pady=20)

    # Кнопка и надпись справа
    label = ctk.CTkLabel(frame_right, text="Если не выставить настройки,\nбудут применены настройки по умолчанию")
    label.pack(pady=5)
    btn_try = ClassButton(frame_right, text="Опробовать", command=tryy)
    btn_try.pack(side=tk.BOTTOM, pady=10) # ВНИМАНИЕ ЯРИК!!! PADY ЭТО ОТСТУП ПО Y, PADX ПО X. ВРОДЕ ЛОГИЧНО НО ЧТО-ТО НЕ ПОНЯТНО.
    if game_mode == 'single':
        btn_start = ClassButton(frame_right, text="Старт", command=start)
        btn_start.pack(side=tk.BOTTOM, pady=10)
    # elif game_mode == 'host':
    #     btn_start = ClassButton(frame_right, text="Старт", command=host_menu, width=10)
    #     btn_start.pack(side=tk.BOTTOM, pady=10)
    
    
root.withdraw() # Прячем "Родительское" меню

# #Функция для получения локального IP адреса
# def get_local_ip():
#     try:
#         s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # По ip4 создаём сокет без установления соединения
#         s.connect(("8.8.8.8", 80)) # Стучимся на гугловский днс
#         ip = s.getsockname()[0] # Получаем свой IP адрес из сокета
#         s.close() # закрываем сокет
#         return ip
#     except:
#         return "127.0.0.1" # Затычка если не достучался


def single_st():
    global game_mode
    game_mode = 'single'
    select.destroy()
    root.deiconify() # Показываем "Родительское" меню
    menu()

# def online_st():
#     global game_mode, player_name, host_ip
#     game_mode = 'online'
#     select.destroy()
#     online_win = ctk.CTkToplevel(root)
#     online_win.title("Подключение к игре")
#     online_win.geometry("300x180")
    
#     ctk.CTkLabel(online_win, text="Введите ваше имя:").pack(pady=10)
#     name_entry = ctk.CTkEntry(online_win)
#     name_entry.insert(0, "Игрок")
#     name_entry.pack(pady=5)
    
#     ctk.CTkLabel(online_win, text="IP адрес Хоста:").pack(pady=5)
#     ip_entry = ctk.CTkEntry(online_win)
#     ip_entry.insert(0, "127.0.0.1")
#     ip_entry.pack(pady=5)
    
#     def online_setting_menu():
#         global player_name, host_ip, settings
#         player_name = name_entry.get()
#         host_ip = ip_entry.get()
#         online_win.destroy()
#         settings = [10, 10, 1, 50, "#c0c0c0", "white", "red", "green", game_mode, player_name, host_ip] # Затычка
#         root.quit()
        
#     ClassButton(online_win, text="Далее", command=online_setting_menu).pack(pady=10)

# def host_st():
#     global game_mode
#     game_mode = 'host'
#     select.destroy()
#     host_win = ctk.CTkToplevel(root)
#     host_win.title("Создание сервера")
#     host_win.geometry("300x150")
    
#     ctk.CTkLabel(host_win, text="Введите ваше имя:").pack(pady=10)
#     name_entry = ctk.CTkEntry(host_win)
#     name_entry.insert(0, "Хост")
#     name_entry.pack(pady=5)
    
#     def host_setting_menu():
#         global player_name
#         player_name = name_entry.get()
#         host_win.destroy()
#         root.deiconify()
#         menu()
        
#     ClassButton(host_win, text="Далее", command=host_setting_menu).pack(pady=10)
    
    
# def host_menu():
#     global settings
#     print("Меню создания сервера")
#     try:
#         if int(size.get()) < 5 or int(size.get()) > 25:
#             tryy()  

#         elif int(difficultf.get()) < 1 or int(difficultf.get()) > 10:
#             tryy()  

#         elif int(size_cell.get()) < 10:
#             tryy()  
#         else:
#             if size.get() != "":
#                 rows = cols = int(size.get())
#             if difficultf.get() != "":
#                 difficult = int(difficultf.get())
#             if size_cell.get() != "":
#                 cell_size = int(size_cell.get())   
#     except ValueError:
#         incorect_type()
#         return

#     ip_local = get_local_ip()
#     settings = [rows, cols, difficult, cell_size, cell_def_color, cell_open_color, cell_outline_color, flag_color, game_mode, player_name, ip_local]
#     print(settings)
    
#     for widget in root.winfo_children(): 
#         widget.destroy()

        
#     root.geometry("350x250")
#     label1 = ctk.CTkLabel(root, text="Лобби игры", font=("Arial", 14, "bold"))
#     label1.pack(pady=15)
#     label2 = ctk.CTkLabel(root, text="Сообщите этот IP второму игроку:", font=("Arial", 10))
#     label2.pack(pady=5)
#     label3 = ctk.CTkLabel(root, text=ip_local, font=("Arial", 14, "bold"), fg="blue")
#     label3.pack(pady=5)
#     start_btn = ClassButton(root, text="Запустить игру", width=15, command=root.quit)
#     start_btn.pack(pady=10)


def win_select_mode():
    global select, root
    select = ctk.CTkToplevel(root)
    select.title("Выбор режима")
    select.geometry("350x120")
    select.resizable(False, False)
    label =ctk.CTkLabel(select, text="Сапёр Онлайн", font=("Arial", 16, "bold"))
    label.pack(pady=15)
    single_btn = ClassButton(select, text="Одиночная игра", command=lambda: [select.destroy(), single_st()])
    single_btn.pack(pady=10)
    # online_btn = ClassButton(select, text="Сетевая игра", width=20, command=lambda: [select.destroy(), online_st()])
    # online_btn.pack(pady=10)
    # host_btn = ClassButton(select, text="Создать лобби", width=20, command=lambda: [select.destroy(), host_st()])
    # host_btn.pack(pady=10)
    select.protocol("WM_DELETE_WINDOW", lambda: root.destroy())

win_select_mode()



root.mainloop()    