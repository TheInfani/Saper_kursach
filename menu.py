# А мне ещё переводить на укр всё...

import tkinter as tk
from tkinter import colorchooser

rows = 10 # Количество строк
cols = 10 # Количество колонок
dif = 1 # Сложность
razk = 50 # Размер клетки
kcolor = "#c0c0c0" # Цвет клеток
kcl_color = "white" # Цвет чистой клетки
k_obv = "red" # Цвет активной обводки
k_flag = "green" # Цвет флага

settings = [rows, cols, dif, razk, kcolor, kcl_color, k_obv, k_flag]
root = tk.Tk() 

# Отрисовка тестового отображения клеток
def tryy():
    global rows, cols, dif, razk, kcolor, kcl_color, k_obv, k_flag, settings
    if size.get() != "":
        rows = cols = int(size.get())
    if diff.get() != "":
        dif = int(diff.get())
    if size_k.get() != "":
        razk = int(size_k.get())
    settings = [rows, cols, dif, razk, kcolor, kcl_color, k_obv, k_flag]
    print(settings)
    canvas.delete("all")
    canvas.create_rectangle(100, 100, 100 + razk, 100 + razk, fill=kcl_color)
    canvas.create_rectangle(100, 100, 100 + razk, 100 + razk, outline="black", width=1)
    canvas.create_rectangle(99, 99, 100 + razk + 1, 100 + razk + 1, outline="black", width=1)
    canvas.create_rectangle(102 + razk, 100, 102 + razk + razk, 100 + razk, fill=kcolor)
    canvas.create_rectangle(102 + razk, 100, 102 + razk + razk, 100 + razk, outline=k_obv, width=1)
    canvas.create_rectangle(102 + razk, 99, 102 + razk + razk + 1, 100 + razk + 1, outline=k_obv, width=1)
    canvas.create_text(102 + razk + razk/2, 98 + razk/2, text="🚩", font=("Arial", round(razk/3),"bold"), fill=k_flag)
    canvas.create_text(100 + + razk/2, 100 + razk/2, text="1", font=("Arial", round(razk/3),"bold"), fill="blue")

def choose_color():
    global kcolor
    color = colorchooser.askcolor()[1]
    if color:
        kcolor = color
    print(kcolor)
    tryy()

def choose_color2():
    global kcl_color
    color = colorchooser.askcolor()[1]
    if color:
        kcl_color = color
    print(kcl_color)
    tryy()

def choose_color3():
    global k_obv
    color = colorchooser.askcolor()[1]
    if color:
        k_obv = color
    print(k_obv)
    tryy()
    
def choose_color4():
    global k_flag
    color = colorchooser.askcolor()[1]
    if color:
        k_flag = color
    print(k_flag)
    tryy()

def start():
    tryy()
    root.quit()

# Основное меню
def menu():
    global rows, cols, dif, razk, kcolor, kcl_color, k_obv, k_flag, settings, size, diff, size_k
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
    size.pack(pady=5)
   
    # Выясняем сложность
    label = tk.Label(frame_left, text="Сложность 1-10")
    label.pack(pady=5)
    diff = tk.Entry(frame_left)
    diff.pack(pady=5)
    
    # Выясняем размер клетки
    label = tk.Label(frame_left, text="Размер клетки в пикселях")
    label.pack(pady=5)
    size_k = tk.Entry(frame_left)
    size_k.pack(pady=5)
    
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
def window_that_vse_okay():
    okay = tk.Toplevel(root)
    okay.protocol("WM_DELETE_WINDOW", oc)
    okay.title("Пользовательсоке соглашение")
    okay.geometry("600x300")
    okay.resizable(False, False) # Пусть будет
    label = tk.Label(okay,text=f"Нажимая кнопку \"дальше\" вы соглашаетесь\nна снятие ответственности с разработчика\n если что-то случится. Всем мира и добра",font=("Arial", 14, "bold"))
    label.pack(expand=True)
    okay_b = tk.Button(okay, text="Дальше", command=lambda: okay_close(okay), width=15) # Кнопка чтобы закрыть это чудо, потом сделаю рабочей (lambda добавить надо)
    okay_b.pack(side=tk.BOTTOM, pady=20)

window_that_vse_okay()

menu()

root.mainloop()    