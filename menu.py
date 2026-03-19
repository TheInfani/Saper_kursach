# А мне ещё переводить на укр всё...

import tkinter as tk
from tkinter import colorchooser

rows = 10 # Количество строк
cols = 10 # Количество колонок
difficult = 1 # Сложность
cell_size = 50 # Размер клетки
cell_def_color = "#c0c0c0" # Цвет клеток
cell_open_color = "white" # Цвет чистой клетки
cell_outline_color = "red" # Цвет активной обводки
flag_color = "green" # Цвет флага

settings = [rows, cols, difficult, cell_size, cell_def_color, cell_open_color, cell_outline_color, flag_color]
root = tk.Tk() 

def incorect_close():
    incorect.destroy()

def incorect_type():
    global incorect
    incorect = tk.Toplevel(root)
    incorect.title("Ошибка")
    incorect.geometry("400x100")
    incorect.resizable(False, False)
    label = tk.Label(incorect,text="Введён некоректный тип данных",font=("Arial", 14, "bold"))
    label.pack(expand=True)
    incorect_btn = tk.Button(incorect, text="Ок", width=10, command=incorect_close)
    incorect_btn.pack(side=tk.BOTTOM, pady=10)
  
# Отрисовка тестового отображения клеток
def tryy():
    global rows, cols, difficult, cell_size, cell_def_color, cell_open_color, cell_outline_color, flag_color, settings, incorect
    
    try:
       cell_size = int(size_cell.get())
    except ValueError:
        incorect_type()
    try:
       difficult = int(difficultf.get())
    except ValueError:
        incorect_type()
    try:
       rows = cols = int(size.get())
    except ValueError:
        incorect_type()    
 
    try:
        if int(size.get()) < 3:
            incorect = tk.Toplevel(root)
            incorect.title("Ошибка")
            incorect.geometry("400x120")
            incorect.resizable(False, False)
            label = tk.Label(incorect,text="Введите размер поля больше 2",font=("Arial", 14, "bold"))
            label.pack(expand=True)
            incorect_btn = tk.Button(incorect, text="Ок", width=10, command=incorect_close)
            incorect_btn.pack(side=tk.BOTTOM, pady=10)

        elif int(difficultf.get()) < 1 or int(difficultf.get()) > 10:
            incorect = tk.Toplevel(root)
            incorect.title("Ошибка")
            incorect.geometry("400x180")
            incorect.resizable(False, False)
            label = tk.Label(incorect,text="Введите сложность в\nдиапазоне от 1 до 10",font=("Arial", 14, "bold"))
            label.pack(expand=True)
            incorect_btn = tk.Button(incorect, text="Ок", width=10, command=incorect_close)
            incorect_btn.pack(side=tk.BOTTOM, pady=10)  

        elif int(size_cell.get()) < 10:
            incorect = tk.Toplevel(root)
            incorect.title("Ошибка")
            incorect.geometry("280x150")
            incorect.resizable(False, False)
            label = tk.Label(incorect,text="Введите размер\nклетки больше 10",font=("Arial", 14, "bold"))
            label.pack(expand=True)
            incorect_btn = tk.Button(incorect, text="Ок", width=10, command=incorect_close)
            incorect_btn.pack(side=tk.BOTTOM, pady=10)
 
    except ValueError:
        print("gg")
        
    canvas.delete("all")
    canvas.create_rectangle(100, 100, 100 + cell_size, 100 + cell_size, fill=cell_open_color)
    canvas.create_rectangle(100, 100, 100 + cell_size, 100 + cell_size, outline="black", width=1)
    canvas.create_rectangle(99, 99, 100 + cell_size + 1, 100 + cell_size + 1, outline="black", width=1)
    canvas.create_rectangle(102 + cell_size, 100, 102 + cell_size + cell_size, 100 + cell_size, fill=cell_def_color)
    canvas.create_rectangle(102 + cell_size, 100, 102 + cell_size + cell_size, 100 + cell_size, outline=cell_outline_color, width=1)
    canvas.create_rectangle(102 + cell_size, 99, 102 + cell_size + cell_size + 1, 100 + cell_size + 1, outline=cell_outline_color, width=1)
    canvas.create_text(102 + cell_size + cell_size/2, 98 + cell_size/2, text="🚩", font=("Arial", round(cell_size/3),"bold"), fill=flag_color)
    canvas.create_text(100 + + cell_size/2, 100 + cell_size/2, text="1", font=("Arial", round(cell_size/3),"bold"), fill="blue")


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
    try:

        if int(size.get()) < 3:
            tryy()  

        elif int(difficultf.get()) < 1 or int(difficultf.get()) > 10:
            tryy()  

        elif int(size_cell.get()) < 10:
            tryy()  

        else:
            if size.get() != "":
                rows = cols = int(size.get())
            if difficultf.get() != "":
                difficult = int(difficultf.get())
            if size_cell.get() != "":
                cell_size = int(size_cell.get())
            settings = [rows, cols, difficult, cell_size, cell_def_color, cell_open_color, cell_outline_color, flag_color]
            print(settings)
            root.quit()

    except ValueError:
        incorect_type()
           
   

# Основное меню
def menu():
    global rows, cols, difficult, cell_size, cell_def_color, cell_open_color, cell_outline_color, flag_color, settings, size, difficultf, size_cell
    settings = {}
    root.title("Меню")
    root.geometry("600x450")
    root.resizable(False, False)

    # Левый фрейм
    frame_left = tk.Frame(root, width=300, height=450, bg="lightgray")
    frame_left.pack(side="left")
    frame_left.pack_propagate(False)
    
    # Выясняем размеры поля
    label = tk.Label(frame_left, text="Размер поля (в клетках)")
    label.pack(pady=5)
    size = tk.Entry(frame_left)
    size.insert(0, 10)
    size.pack(pady=5)
   
    # Выясняем сложность
    label = tk.Label(frame_left, text="Сложность 1-10")
    label.pack(pady=5)
    difficultf = tk.Entry(frame_left)
    difficultf.insert(0, 5)
    difficultf.pack(pady=5)
    
    # Выясняем размер клетки
    label = tk.Label(frame_left, text="Размер клетки в пикселях")
    label.pack(pady=5)
    size_cell = tk.Entry(frame_left)
    size_cell.insert(0, 50)
    size_cell.pack(pady=5)
    
    # Выясняем цвет келток по умолчанию
    label = tk.Label(frame_left, text="Цвет клеток по умолчанию")
    label.pack(pady=5)
    btn = tk.Button(frame_left, text="Выбрать цвет", command=choose_color)
    btn.pack(pady=5)
    
    # Выясняем цвет открытх келток
    label = tk.Label(frame_left, text="Цвет открытых клеток")
    label.pack(pady=5)
    btn2 = tk.Button(frame_left, text="Выбрать цвет", command=choose_color2)
    btn2.pack(pady=5)
    
    # Выясняем цвет активной обводки
    label = tk.Label(frame_left, text="Цвет Активной обводки")
    label.pack(pady=5)
    btn3 = tk.Button(frame_left, text="Выбрать цвет", command=choose_color3)
    btn3.pack(pady=5)
    
    # Выясняем цвет чистых флага
    label = tk.Label(frame_left, text="Цвет флага")
    label.pack(pady=5)
    btn4 = tk.Button(frame_left, text="Выбрать цвет", command=choose_color4)
    btn4.pack(pady=5)

    # Правый фрейм 
    frame_right = tk.Frame(root, width=300, height=450, bg="darkgray")
    frame_right.pack(side="right")
    frame_right.pack_propagate(False) # Судя с инета, это фиксирует размеры фрейма, бо без него чёт всё с`езжает
    global canvas
    canvas = tk.Canvas(frame_right, width=280, height=200, bg="white")
    canvas.pack(pady=20)

    # Кнопка и надпись справа
    label = tk.Label(frame_right, text="Если не выставить настройки,\nбудут применены настройки по умолчанию")
    label.pack(pady=5)
    btn_try = tk.Button(frame_right, text="Опробовать", command=tryy, width=10)
    btn_try.pack(side=tk.BOTTOM, pady=10) # ВНИМАНИЕ ЯРИК!!! PADY ЭТО ОТСТУП ПО Y, PADX ПО X. ВРОДЕ ЛОГИЧНО НО ЧТО-ТО НЕ ПОНЯТНО.
    btn_start = tk.Button(frame_right, text="Старт", command=start, width=10)
    btn_start.pack(side=tk.BOTTOM, pady=10)
    
    
root.withdraw() # Прячем "Родительское" меню

def okay_close(win):
    win.destroy() # Надо бо функия об`явлена до появления переменной, а кнопку надо ставить после
    root.deiconify() # Показываем menu
    
# Функция которая ничего не делает
def oc():
    pass  
 
# Меню с соглашением
def window_license():
    okay = tk.Toplevel(root)
    okay.title("Пользовательсоке соглашение")
    okay.geometry("600x300")
    okay.resizable(False, False) # Пусть будет
    label = tk.Label(okay,text=f"Нажимая кнопку \"дальше\" вы соглашаетесь\nна снятие ответственности с разработчика\n если что-то случится. Всем мира и добра",font=("Arial", 14, "bold"))
    label.pack(expand=True)
    okay_b = tk.Button(okay, text="Дальше", command=lambda: okay_close(okay), width=15) # Кнопка чтобы закрыть это чудо, потом сделаю рабочей (lambda добавить надо)
    okay_b.pack(side=tk.BOTTOM, pady=20)

window_license()

menu()

root.mainloop()    