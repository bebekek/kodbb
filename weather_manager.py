"""
Модуль управления данными дневника погоды.
Содержит класс WeatherDiary для работы с записями, JSON и валидацией.
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Tuple, Optional

DATA_FILE = "weather_data.json"


class WeatherDiary:
    """Класс для управления записями о погоде."""

    def __init__(self):
        self.records: List[Dict] = []
        self.load_records()

    def load_records(self) -> None:
        """Загружает записи из JSON-файла с проверкой структуры."""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        # Валидация структуры каждой записи
                        valid_records = []
                        for record in data:
                            if self._is_valid_record_structure(record):
                                valid_records.append(record)
                        self.records = valid_records
                    else:
                        self.records = []
            except (json.JSONDecodeError, IOError):
                self.records = []
        else:
            self.records = []

    def _is_valid_record_structure(self, record: Dict) -> bool:
        """Проверяет, что запись содержит все необходимые поля."""
        required_fields = ['date', 'temperature', 'description', 'precipitation']
        return all(field in record for field in required_fields)

    def save_records(self) -> None:
        """Сохраняет все записи в JSON-файл с форматированием."""
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.records, f, ensure_ascii=False, indent=4)

    def validate_record(self, date: str, temperature: str, 
                        description: str) -> Tuple[bool, str]:
        """
        Проверяет корректность введённых данных.
        
        Args:
            date: Дата в строковом формате
            temperature: Температура (строка для проверки)
            description: Описание погоды
        
        Returns:
            (bool, str): (Успех, Сообщение об ошибке или успехе)
        """
        # Проверка даты
        if not date:
            return False, "Дата не может быть пустой"
        
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            return False, "Дата должна быть в формате ГГГГ-ММ-ДД (например, 2026-04-22)"

        # Проверка температуры
        if not temperature:
            return False, "Температура не может быть пустой"
        
        try:
            float(temperature)
        except ValueError:
            return False, "Температура должна быть числом (например, 15.5 или -3)"

        # Проверка описания
        if not description or len(description.strip()) == 0:
            return False, "Описание погоды не может быть пустым"
        
        if not description.isprintable():
            return False, "Описание содержит недопустимые символы"

        return True, "Данные корректны"

    def add_record(self, date: str, temperature: str, 
                   description: str, precipitation: bool) -> Tuple[bool, str]:
        """
        Добавляет новую запись после валидации.
        
        Returns:
            (bool, str): (Успех, Сообщение)
        """
        # Валидация
        is_valid, message = self.validate_record(date, temperature, description)
        if not is_valid:
            return False, message

        # Создание записи
        record = {
            'id': len(self.records) + 1,
            'date': date,
            'temperature': float(temperature),
            'description': description.strip(),
            'precipitation': precipitation
        }

        self.records.append(record)
        self.save_records()
        return True, f"Запись за {date} успешно добавлена"

    def get_all_records(self) -> List[Dict]:
        """Возвращает все записи."""
        return self.records

    def filter_by_date(self, target_date: str) -> List[Dict]:
        """
        Фильтрует записи по конкретной дате.
        
        Args:
            target_date: Дата в формате ГГГГ-ММ-ДД
        
        Returns:
            Отфильтрованный список записей
        """
        if not target_date:
            return self.records
        
        filtered = []
        for record in self.records:
            if record['date'] == target_date:
                filtered.append(record)
        return filtered

    def filter_by_temperature(self, min_temp: float) -> List[Dict]:
        """
        Фильтрует записи по минимальной температуре.
        
        Args:
            min_temp: Минимальная температура для фильтрации
        
        Returns:
            Отфильтрованный список записей
        """
        filtered = []
        for record in self.records:
            if record['temperature'] >= min_temp:
                filtered.append(record)
        return filtered

    def filter_combined(self, date: str = "", min_temp: Optional[float] = None) -> List[Dict]:
        """
        Комбинированная фильтрация по дате и температуре.
        """
        result = self.records.copy()
        
        if date:
            result = [r for r in result if r['date'] == date]
        
        if min_temp is not None:
            result = [r for r in result if r['temperature'] >= min_temp]
        
        return result
