import csv
import os
from datetime import datetime

FILENAME = "cars.csv"
FIELDS = ["Марка", "Модель", "Тип кузова", "Обєм двигуна", "Рік випуску", "Ціна"]
CURRENT_YEAR = datetime.now().year

def file_exists(): return os.path.exists(FILENAME) and os.path.getsize(FILENAME) > 0

def validate_number(value, field_name, min_value=0, max_value=None):
    while True:
        try:
            num = float(value)
            if num < min_value or (max_value and num > max_value): raise ValueError
            return str(int(num)) if field_name in ["Рік випуску", "Ціна"] else f"{num:.01f}"
        except ValueError:
            value = input(f"Некоректне значення для {field_name}. Введіть ще раз: ")

def save_data(data):
    with open(FILENAME, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(data)

def load_data():
    if not file_exists(): return []
    with open(FILENAME, "r", encoding="utf-8") as file:
        return list(csv.DictReader(file))

def add_car():
    car = {
        "Марка": input("Марка: ").strip(),
        "Модель": input("Модель: ").strip(),
        "Тип кузова": input("Тип кузова: ").strip(),
        "Обєм двигуна": validate_number(input("Обєм двигуна (л): "), "Обєм двигуна", 0.5),
        "Рік випуску": validate_number(input("Рік випуску: "), "Рік випуску", 1900, CURRENT_YEAR),
        "Ціна": validate_number(input("Ціна: "), "Ціна", 1)
    }
    data = load_data()
    data.append(car)
    save_data(data)
    display_cars()

def display_cars():
    data = load_data()
    if not data:
        print("Файл порожній або не існує.")
        return
    print("\n" + " | ".join(FIELDS))
    print("-" * 80)
    for row in data:
        print(" | ".join(row[field] for field in FIELDS))

def delete_car():
    data = load_data()
    if not data:
        print("Файл порожній.")
        return
    display_cars()
    model_to_delete = input("Введіть модель для видалення: ").strip().lower()
    new_data = [row for row in data if row["Модель"].strip().lower() != model_to_delete]
    if len(new_data) == len(data):
        print("Такої моделі немає у списку.")
    else:
        save_data(new_data)
        print("Автомобіль(і) видалено!")
    display_cars()

def clear_file():
    save_data([])
    print("Всі дані видалені!")
    display_cars()

def main():
    while True:
        print("\n1. Додати автомобіль")
        print("2. Показати всі записи")
        print("3. Видалити всі записи")
        print("4. Видалити автомобіль")
        print("5. Вийти")
        choice = input("Оберіть опцію: ")
        if choice == "1": add_car()
        elif choice == "2": display_cars()
        elif choice == "3": clear_file()
        elif choice == "4": delete_car()
        elif choice == "5":
            print("Програма завершена.")
            break
        else:
            print("Некоректний ввід. Введіть число від 1 до 5.")

if __name__ == "__main__": main()
