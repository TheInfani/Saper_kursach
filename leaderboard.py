import customtkinter as ctk

root = ctk.CTk()
root.title("Меню настроек игры")
root.geometry("300x670")
root.resizable(False, False)

# таблица рекордов (очки, время прохождения, сложность, размер, количество мин)      очки = (количество мин * слоность * размер поля) / (время прохождения / (количество мин * сложность))
records_data = [
    [4348, 23, 5, 10, 20]
]

# Фрейм пресетов настроек
frame_records = ctk.CTkFrame(root, width=300, height=670, fg_color="transparent", border_width=0, corner_radius=0)
frame_records.pack(side="right")
frame_records.pack_propagate(False)
    
frame_record_list = ctk.CTkFrame(frame_records, width=300, height=570)
frame_record_list.pack(side="top")
frame_record_list.pack_propagate(False)

label = ctk.CTkLabel(frame_record_list, text="Пресеты настроек", font=("Arial", 16, "bold"))
label.pack(pady=10)

# Создаем прокручиваемую область
scroll_frame = ctk.CTkScrollableFrame(frame_record_list, width=180, height=500, border_width=0, corner_radius=0, fg_color="transparent", scrollbar_fg_color="transparent")
scroll_frame.pack(pady=5, padx=5, fill="both", expand=True)
scroll_frame._scrollbar.configure(width=0)

# # Функция для применения пресета
# def apply_preset(p_size, p_diff, p_cell):
#     size.delete(0, tk.END)
#     size.insert(0, p_size)
#     difficultf.delete(0, tk.END)
#     difficultf.insert(0, p_diff)
#     size_cell.delete(0, tk.END)
#     size_cell.insert(0, p_cell)
#     tryy() # Обновляем предпросмотр

# Создаем кнопки пресетов в цикле
for i in records_data:
    preset_button = ctk.CTkButton(scroll_frame, text=f"Очки: {i[0]}  Время (секунды): {i[1]}\nСложность: {i[2]}  Размер поля: {i[3]}  Мин: {i[4]}", command=lambda val=i: apply_preset(val[1], val[2], val[3]), height=60)
    preset_button.pack(pady=5, fill="x")

def add_preset():
    r_count
    r_diff = difficultf.get()
    r_size = size_cell.get()
    r_time = start_timer
    r_mine = min_count
    preset_name = f"{p_name.get()}\n({p_size}x{p_size})"
    if not preset_name:
        preset_name = f"Пресет {len(presets_data)+1}\n({p_size}x{p_size})"
    presets_data.append([preset_name, p_size, p_diff, p_cell])
    preset_button = ctk.CTkButton(scroll_frame, text=preset_name, command=lambda val=presets_data[-1]: apply_preset(val[1], val[2], val[3]), height=60)
    preset_button.pack(pady=5, fill="x")
    save_presets()

root.mainloop()