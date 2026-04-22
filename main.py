"""
Графическое приложение "Weather Diary"
Интерфейс на Tkinter для ведения дневника погоды.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from weather_manager import WeatherDiary
import random  # Демонстрация использования random


class WeatherDiaryApp:
    """Главный класс приложения."""

    def __init__(self, root):
        self.diary = WeatherDiary()
        self.root = root
        self.root.title("🌤️ Weather Diary - Дневник погоды")
        self.root.geometry("750x550")
        self.root.resizable(True, True)
        
        # Настройка стилей
        self._setup_styles()
        
        # Создание интерфейса
        self._create_input_frame()
        self._create_filter_frame()
        self._create_table_frame()
        self._create_status_bar()
        
        # Загрузка данных
        self.refresh_table()
        
        # Случайный факт о погоде (использование random)
        self.show_random_weather_fact()

    def _setup_styles(self):
        """Настройка стилей для виджетов."""
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Segoe UI', 10, 'bold'))
        style.configure("TLabel", font=('Segoe UI', 9))
        style.configure("TButton", font=('Segoe UI', 9))
        style.configure("TLabelframe.Label", font=('Segoe UI', 10, 'bold'))

    def _create_input_frame(self):
        """Создание фрейма для ввода данных."""
        frame = ttk.LabelFrame(self.root, text="📝 Добавить запись о погоде", padding=10)
        frame.pack(fill="x", padx=10, pady=5)

        # Дата
        ttk.Label(frame, text="Дата:").grid(row=0, column=0, sticky="w", pady=2)
        self.entry_date = ttk.Entry(frame, width=20)
        self.entry_date.grid(row=0, column=1, padx=5, pady=2, sticky="w")
        ttk.Label(frame, text="(ГГГГ-ММ-ДД)", foreground="gray").grid(
            row=0, column=2, sticky="w", padx=5)

        # Температура
        ttk.Label(frame, text="Температура:").grid(row=1, column=0, sticky="w", pady=2)
        self.entry_temp = ttk.Entry(frame, width=10)
        self.entry_temp.grid(row=1, column=1, padx=5, pady=2, sticky="w")
        ttk.Label(frame, text="°C", foreground="gray").grid(
            row=1, column=2, sticky="w", padx=5)

        # Описание
        ttk.Label(frame, text="Описание:").grid(row=2, column=0, sticky="w", pady=2)
        self.entry_desc = ttk.Entry(frame, width=40)
        self.entry_desc.grid(row=2, column=1, columnspan=2, padx=5, pady=2, sticky="w")

        # Осадки (да/нет)
        ttk.Label(frame, text="Осадки:").grid(row=3, column=0, sticky="w", pady=2)
        self.precip_var = tk.BooleanVar(value=False)
        self.check_precip = ttk.Checkbutton(frame, text="Были осадки", 
                                            variable=self.precip_var)
        self.check_precip.grid(row=3, column=1, padx=5, pady=2, sticky="w")

        # Кнопка добавления
        btn_add = ttk.Button(frame, text="➕ Добавить запись", 
                            command=self.add_record, width=20)
        btn_add.grid(row=4, column=1, pady=10, sticky="w")

    def _create_filter_frame(self):
        """Создание фрейма для фильтрации."""
        frame = ttk.LabelFrame(self.root, text="🔍 Фильтрация", padding=10)
        frame.pack(fill="x", padx=10, pady=5)

        # Фильтр по дате
        ttk.Label(frame, text="По дате:").grid(row=0, column=0, sticky="w", pady=2)
        self.filter_date = ttk.Entry(frame, width=15)
        self.filter_date.grid(row=0, column=1, padx=5, pady=2, sticky="w")
        ttk.Label(frame, text="(ГГГГ-ММ-ДД)", foreground="gray").grid(
            row=0, column=2, sticky="w", padx=5)

        # Фильтр по температуре
        ttk.Label(frame, text="Температура выше:").grid(row=0, column=3, sticky="w", pady=2, padx=(20,0))
        self.filter_temp = ttk.Entry(frame, width=8)
        self.filter_temp.grid(row=0, column=4, padx=5, pady=2, sticky="w")
        ttk.Label(frame, text="°C", foreground="gray").grid(
            row=0, column=5, sticky="w", padx=5)

        # Кнопки управления фильтром
        btn_apply = ttk.Button(frame, text="Применить фильтр", 
                              command=self.apply_filter, width=18)
        btn_apply.grid(row=1, column=1, pady=5, sticky="w")

        btn_reset = ttk.Button(frame, text="Сбросить фильтр", 
                              command=self.reset_filter, width=18)
        btn_reset.grid(row=1, column=4, pady=5, sticky="w")

    def _create_table_frame(self):
        """Создание таблицы для отображения записей."""
        frame = ttk.Frame(self.root)
        frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Определение колонок
        columns = ("ID", "Дата", "Температура (°C)", "Описание", "Осадки")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", height=12)

        # Настройка колонок
        self.tree.heading("ID", text="ID")
        self.tree.heading("Дата", text="Дата")
        self.tree.heading("Температура (°C)", text="Температура (°C)")
        self.tree.heading("Описание", text="Описание")
        self.tree.heading("Осадки", text="Осадки")

        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Дата", width=100, anchor="center")
        self.tree.column("Температура (°C)", width=120, anchor="center")
        self.tree.column("Описание", width=250)
        self.tree.column("Осадки", width=80, anchor="center")

        # Добавление скроллбара
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def _create_status_bar(self):
        """Создание статусной строки."""
        self.status_var = tk.StringVar()
        self.status_var.set("Готов к работе")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, 
                               relief="sunken", anchor="w")
        status_bar.pack(side="bottom", fill="x", padx=10, pady=3)

    def add_record(self):
        """Обработчик добавления записи."""
        date = self.entry_date.get().strip()
        temp = self.entry_temp.get().strip()
        desc = self.entry_desc.get().strip()
        precip = self.precip_var.get()

        success, message = self.diary.add_record(date, temp, desc, precip)

        if success:
            messagebox.showinfo("✅ Успех", message)
            # Очистка полей
            self.entry_date.delete(0, tk.END)
            self.entry_temp.delete(0, tk.END)
            self.entry_desc.delete(0, tk.END)
            self.precip_var.set(False)
            self.refresh_table()
            self.status_var.set(f"Запись добавлена. Всего записей: {len(self.diary.records)}")
        else:
            messagebox.showerror("❌ Ошибка валидации", message)
            self.status_var.set(f"Ошибка: {message}")

    def refresh_table(self, records=None):
        """Обновление данных в таблице."""
        # Очистка таблицы
        for row in self.tree.get_children():
            self.tree.delete(row)

        if records is None:
            records = self.diary.get_all_records()

        # Заполнение таблицы
        for record in records:
            precip_text = "🌧️ Да" if record['precipitation'] else "☀️ Нет"
            temp_formatted = f"{record['temperature']:.1f}°C"
            
            self.tree.insert("", "end", values=(
                record['id'],
                record['date'],
                temp_formatted,
                record['description'],
                precip_text
            ))

        self.status_var.set(f"Отображено записей: {len(records)} из {len(self.diary.records)}")

    def apply_filter(self):
        """Применение фильтров."""
        date_filter = self.filter_date.get().strip()
        temp_filter_str = self.filter_temp.get().strip()

        min_temp = None
        if temp_filter_str:
            try:
                min_temp = float(temp_filter_str)
            except ValueError:
                messagebox.showerror("Ошибка", "Температура для фильтра должна быть числом")
                return

        # Применение комбинированного фильтра
        filtered = self.diary.filter_combined(date=date_filter, min_temp=min_temp)
        self.refresh_table(filtered)
        
        # Обновление статуса
        if date_filter and min_temp is not None:
            self.status_var.set(f"Фильтр: дата={date_filter}, t ≥ {min_temp}°C")
        elif date_filter:
            self.status_var.set(f"Фильтр: дата={date_filter}")
        elif min_temp is not None:
            self.status_var.set(f"Фильтр: температура ≥ {min_temp}°C")
        else:
            self.status_var.set("Фильтр сброшен")

    def reset_filter(self):
        """Сброс фильтров."""
        self.filter_date.delete(0, tk.END)
        self.filter_temp.delete(0, tk.END)
        self.refresh_table()
        self.status_var.set(f"Фильтр сброшен. Всего записей: {len(self.diary.records)}")

    def show_random_weather_fact(self):
        """Показывает случайный факт о погоде (демонстрация random)."""
        facts = [
            "🌪️ Самая высокая температура на Земле: +56.7°C (Долина Смерти, США)",
            "❄️ Самая низкая температура: -89.2°C (Антарктида)",
            "🌈 Радуга может быть видна ночью — это лунная радуга",
            "⚡ Каждую секунду на Земле происходит около 100 ударов молний",
            "☔ В индийском городе Маусинрам выпадает до 12 метров осадков в год"
        ]
        fact = random.choice(facts)
        self.status_var.set(fact)


def main():
    """Точка входа в приложение."""
    root = tk.Tk()
    app = WeatherDiaryApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
