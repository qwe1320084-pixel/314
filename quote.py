import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os
from datetime import datetime

# ------------------ Файлы данных ------------------
QUOTES_FILE = "quotes.json"
HISTORY_FILE = "history.json"

# ------------------ Загрузка/сохранение ------------------
def load_quotes():
    if not os.path.exists(QUOTES_FILE):
        default_quotes = [
            {"text": "Будь изменением, которое ты хочешь видеть в мире.", "author": "Махатма Ганди", "theme": "Мотивация"},
            {"text": "Жизнь — это то, что с тобой происходит, пока ты строишь планы.", "author": "Джон Леннон", "theme": "Жизнь"},
            {"text": "Воображение важнее знания.", "author": "Альберт Эйнштейн", "theme": "Наука"},
            {"text": "Ты упускаешь 100% выстрелов, которые не делаешь.", "author": "Уэйн Гретцки", "theme": "Спорт"},
            {"text": "Будь собой; остальные роли уже заняты.", "author": "Оскар Уайльд", "theme": "Мудрость"}
        ]
        save_quotes(default_quotes)
        return default_quotes
    with open(QUOTES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_quotes(quotes):
    with open(QUOTES_FILE, "w", encoding="utf-8") as f:
        json.dump(quotes, f, ensure_ascii=False, indent=4)

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=4)

def add_to_history(quote):
    history = load_history()
    quote_copy = quote.copy()
    quote_copy["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    history.append(quote_copy)
    save_history(history)
    return history

# ------------------ Основное приложение ------------------
class QuoteGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Quote Generator")
        self.root.geometry("700x550")

        self.quotes = load_quotes()
        self.history = load_history()

        # Переменные фильтров
        self.filter_author = tk.StringVar()
        self.filter_theme = tk.StringVar()

        self.create_widgets()
        self.refresh_history_display()

    def create_widgets(self):
        # Основной фрейм
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # ----- Отображение цитаты -----
        self.quote_label = tk.Label(main_frame, text="Нажмите кнопку, чтобы получить цитату",
                                    wraplength=650, font=("Arial", 12), justify="center")
        self.quote_label.pack(pady=20)

        # Кнопка генерации
        ttk.Button(main_frame, text="Сгенерировать цитату", command=self.generate_quote).pack(pady=5)

        # ----- Фильтры -----
        filter_frame = ttk.LabelFrame(main_frame, text="Фильтрация", padding=5)
        filter_frame.pack(fill=tk.X, pady=10)

        # Автор
        ttk.Label(filter_frame, text="Автор:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        author_combo = ttk.Combobox(filter_frame, textvariable=self.filter_author, values=self.get_authors(), width=25)
        author_combo.grid(row=0, column=1, padx=5, pady=5)
        author_combo.bind("<<ComboboxSelected>>", lambda e: self.refresh_history_display())

        # Тема
        ttk.Label(filter_frame, text="Тема:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        theme_combo = ttk.Combobox(filter_frame, textvariable=self.filter_theme, values=self.get_themes(), width=20)
        theme_combo.grid(row=0, column=3, padx=5, pady=5)
        theme_combo.bind("<<ComboboxSelected>>", lambda e: self.refresh_history_display())

        # Кнопка сброса фильтров
        ttk.Button(filter_frame, text="Сбросить фильтры", command=self.reset_filters).grid(row=0, column=4, padx=10)

        # ----- Добавление новой цитаты -----
        add_frame = ttk.LabelFrame(main_frame, text="Добавить новую цитату", padding=5)
        add_frame.pack(fill=tk
X, pady=10)

        ttk.Label(add_frame, text="Текст:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.new_text = tk.Text(add_frame, height=2, width=40)
        self.new_text.grid(row=0, column=1, padx=5, pady=5, columnspan=3)

        ttk.Label(add_frame, text="Автор:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.new_author = ttk.Entry(add_frame, width=30)
        self.new_author.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(add_frame, text="Тема:").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        self.new_theme = ttk.Entry(add_frame, width=20)
        self.new_theme.grid(row=1, column=3, padx=5, pady=5)

        ttk.Button(add_frame, text="Добавить цитату", command=self.add_quote).grid(row=2, column=1, columnspan=3, pady=10)

        # ----- История -----
        history_frame = ttk.LabelFrame(main_frame, text="История цитат", padding=5)
        history_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        scrollbar = ttk.Scrollbar(history_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.history_listbox = tk.Listbox(history_frame, yscrollcommand=scrollbar.set, height=10)
        self.history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.history_listbox.yview)

    def get_authors(self):
        return sorted(set(q["author"] for q in self.quotes))

    def get_themes(self):
        return sorted(set(q["theme"] for q in self.quotes))

    def generate_quote(self):
        if not self.quotes:
            messagebox.showwarning("Нет цитат", "Добавьте хотя бы одну цитату.")
            return
        quote = random.choice(self.quotes)
        self.quote_label.config(text=f"«{quote['text']}»\n\n— {quote['author']} (Тема: {quote['theme']})")
        self.history = add_to_history(quote)
        self.refresh_history_display()

    def refresh_history_display(self):
        self.history_listbox.delete(0, tk.END)
        filtered = self.history
        author = self.filter_author.get().strip()
        theme = self.filter_theme.get().strip()

        if author:
            filtered = [h for h in filtered if h.get("author", "") == author]
        if theme:
            filtered = [h for h in filtered if h.get("theme", "") == theme]

        for entry in reversed(filtered):  # Показываем новые сверху
            display = f"{entry['timestamp']} — {entry['author']}: {entry['text'][:60]}..."
            self.history_listbox.insert(tk.END, display)

    def reset_filters(self):
        self.filter_author.set("")
        self.filter_theme.set("")
        self.refresh_history_display()

    def add_quote(self):
        text = self.new_text.get("1.0", tk.END).strip()
        author = self.new_author.get().strip()
        theme = self.new_theme.get().strip()

        if not text or not author or not theme:
            messagebox.showerror("Ошибка", "Все поля (текст, автор, тема) обязательны для заполнения.")
            return

        new_quote = {"text": text, "author": author, "theme": theme}
        self.quotes.append(new_quote)
        save_quotes(self.quotes)

        # Очистка полей
        self.new_text.delete("1.0", tk.END)
        self.new_author.delete(0, tk.END)
        self.new_theme.delete(0, tk.END)

        # Обновление выпадающих списков фильтров
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, ttk.Combobox):
                        if "Автор" in str(child):
                            child['values'] = self.get_authors()
                        elif "Тема" in str(child):
                            child['values'] = self.get_themes()
        messagebox.showinfo("Успех", "Цитата добавлена!")

# ------------------ Запуск ------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = QuoteGenerator(root)
    root.mainloop().
