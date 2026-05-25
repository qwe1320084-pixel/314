import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import json
import os
from datetime import datetime

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Password Generator")
        self.root.geometry("700x500")
        self.root.resizable(True, True)
        
        # Файл для сохранения истории
        self.history_file = "password_history.json"
        
        # Переменные для хранения настроек
        self.password_length = tk.IntVar(value=12)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_letters = tk.BooleanVar(value=True)
        self.use_special = tk.BooleanVar(value=True)
        
        # История паролей (список словарей)
        self.history = []
        
        # Загрузка истории из файла
        self.load_history()
        
        # Создание интерфейса
        self.create_widgets()
        
        # Обновление отображения истории
        self.update_history_display()
        
    def create_widgets(self):
        # Основной фрейм для настроек
        settings_frame = ttk.LabelFrame(self.root, text="Настройки пароля", padding=10)
        settings_frame.pack(fill="x", padx=10, pady=5)
        
        # Ползунок длины пароля
        length_frame = ttk.Frame(settings_frame)
        length_frame.pack(fill="x", pady=5)
        
        ttk.Label(length_frame, text="Длина пароля:").pack(side="left", padx=(0, 10))
        self.length_scale = ttk.Scale(length_frame, from_=4, to=50, orient="horizontal", 
                                      variable=self.password_length, command=self.update_length_label)
        self.length_scale.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        self.length_label = ttk.Label(length_frame, text="12")
        self.length_label.pack(side="left")
        
        # Чекбоксы для выбора символов
        chars_frame = ttk.Frame(settings_frame)
        chars_frame.pack(fill="x", pady=10)
        
        ttk.Checkbutton(chars_frame, text="Цифры (0-9)", variable=self.use_digits).pack(side="left", padx=5)
        ttk.Checkbutton(chars_frame, text="Буквы (A-Z, a-z)", variable=self.use_letters).pack(side="left", padx=5)
        ttk.Checkbutton(chars_frame, text="Спецсимволы (!@#$%^&*)", variable=self.use_special).pack(side="left", padx=5)
        
        # Кнопка генерации
        generate_btn = ttk.Button(settings_frame, text="Сгенерировать пароль", command=self.generate_password)
        generate_btn.pack(pady=10)
        
        # Фрейм для отображения сгенерированного пароля
        result_frame = ttk.LabelFrame(self.root, text="Сгенерированный пароль", padding=10)
        result_frame.pack(fill="x", padx=10, pady=5)
        
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(result_frame, textvariable=self.password_var, 
                                        font=("Courier", 12), state="readonly")
        self.password_entry.pack(fill="x", padx=5, pady=5)
        
        # Кнопка копирования
        copy_btn = ttk.Button(result_frame, text="Копировать в буфер", command=self.copy_to_clipboard)
        copy_btn.pack(pady=5)
        
        # Фрейм для истории
        history_frame = ttk.LabelFrame(self.root, text="История паролей", padding=10)
        history_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Таблица истории с scrollbar
        tree_frame = ttk.Frame(history_frame)
        tree_frame.pack(fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.tree = ttk.Treeview(tree_frame, columns=("date", "password", "length", "chars"), 
                                 show="headings", yscrollcommand=scrollbar.set)
        
        self.tree.heading("date", text="Дата и время")
        self.tree.heading("password", text="Пароль")
        self.tree.heading("length", text="Длина")
        self.tree.heading("chars", text="Типы символов")
        
        self.tree.column("date", width=150)
        self.tree.column("password", width=250)
        self.tree.column("length", width=60)
        self.tree.column("chars", width=150)
        
        self.tree.pack(fill="both", expand=True)
        scrollbar.config(command=self.tree.yview)
        
        # Кнопки управления историей
        history_buttons_frame = ttk.Frame(history_frame)
        history_buttons_frame.pack(fill="x", pady=(10, 0))
        
        ttk.Button(history_buttons_frame, text="Очистить историю", command=self.clear_history).pack(side="left", padx=5)
        ttk.Button(history_buttons_frame, text="Удалить выбранный", command=self.delete_selected).pack(side="left", padx=5)
        
    def update_length_label(self, event=None):
        """Обновление отображения длины пароля"""
        self.length_label.config(text=str(int(self.password_length.get())))
        
    def get_character_set(self):
        """Получение набора символов на основе выбранных опций"""
        chars = ""
        
        if self.use_letters.get():
            chars += string.ascii_letters
        if self.use_digits.get():
            chars += string.digits
        if self.use_special.get():
            chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
            
        return chars
    
    def generate_password(self):
        """Генерация случайного пароля"""
        # Проверка корректности ввода
        length = int(self.password_length.get())
        
        if length < 4:
            messagebox.showwarning("Ошибка", "Минимальная длина пароля - 4 символа")
            self.password_length.set(4)
            length = 4
        elif length > 50:
            messagebox.showwarning("Ошибка", "Максимальная длина пароля - 50 символов")
            self.password_length.set(50)
            length = 50
            
        chars = self.get_character_set()
        
        if not chars:
            messagebox.showwarning("Ошибка", "Выберите хотя бы один тип символов")
            return
        
        # Генерация пароля
        password = []
        for _ in range(length):
            password.append(random.choice(chars))
        
        # Перемешиваем для лучшей случайности (хотя random.choice уже случайный)
        random.shuffle(password)
        generated_password = ''.join(password)
        
        # Отображение пароля
        self.password_var.set(generated_password)
        
        # Сохранение в историю
        self.save_to_history(generated_password)
        
    def save_to_history(self, password):
        """Сохранение пароля в историю"""
        # Определение типов использованных символов
        char_types = []
        if self.use_letters.get():
            char_types.append("буквы")
        if self.use_digits.get():
            char_types.append("цифры")
        if self.use_special.get():
            char_types.append("спецсимволы")
        
        char_types_str = ", ".join(char_types)
        
        history_entry = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "password": password,
            "length": int(self.password_length.get()),
            "chars": char_types_str
        }
        
        self.history.append(history_entry)
        self.save_history_to_file()
        self.update_history_display()
        
    def update_history_display(self):
        """Обновление отображения таблицы истории"""
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Добавление записей из истории
        for entry in self.history:
            self.tree.insert("", "end", values=(entry["date"], entry["password"], 
                                               entry["length"], entry["chars"]))
    
    def copy_to_clipboard(self):
        """Копирование пароля в буфер обмена"""
        password = self.password_var.get()
        if password:
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            messagebox.showinfo("Успех", "Пароль скопирован в буфер обмена")
        else:
            messagebox.showwarning("Ошибка", "Нет пароля для копирования")
    
    def save_history_to_file(self):
        """Сохранение истории в JSON файл"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить историю: {str(e)}")
    
    def load_history(self):
        """Загрузка истории из JSON файла"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить историю: {str(e)}")
                self.history = []
        else:
            self.history = []
    
    def clear_history(self):
        """Очистка всей истории"""
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите очистить всю историю?"):
            self.history = []
            self.save_history_to_file()
            self.update_history_display()
            messagebox.showinfo("Успех", "История очищена")
    
    def delete_selected(self):
        """Удаление выбранной записи из истории"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Ошибка", "Выберите запись для удаления")
            return
            
        if messagebox.askyesno("Подтверждение", "Удалить выбранную запись?"):
            # Получение индекса выбранной записи
            index = self.tree.index(selected[0])
            del self.history[index]
            self.save_history_to_file()
            self.update_history_display()
            messagebox.showinfo("Успех", "Запись удалена")

def main():
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
