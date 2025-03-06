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
            if field_name == "Рік випуску": return str(int(num))
            elif field_name == "Обєм двигуна": return f"{num:.1f}"
            elif field_name == "Ціна": return str(int(num))
            return str(num)
        except ValueError:
            value = input(f"Некоректне значення для {field_name}. Введіть ще раз: ")

def format_value(field, value):
    try:
        if not value: return ""
        if field == "Рік випуску": return str(int(float(value)))
        elif field == "Ціна": return str(int(float(value)))
        elif field == "Обєм двигуна": return f"{float(value):.1f}"
    except: pass
    return value

def add_car():
    car = {
        "Марка": input("Марка: ").strip(),
        "Модель": input("Модель: ").strip(),
        "Тип кузова": input("Тип кузова: ").strip(),
        "Обєм двигуна": validate_number(input("Обєм двигуна (л): "), "Обєм двигуна", 0.5),
        "Рік випуску": validate_number(input("Рік випуску: "), "Рік випуску", 1900, CURRENT_YEAR),
        "Ціна": validate_number(input("Ціна: "), "Ціна", 1)
    }
    with open(FILENAME, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        if not file_exists(): writer.writeheader()
        writer.writerow(car)
    print("Дані додано!")

def update_file_format():
    if not file_exists(): return
    try:
        with open(FILENAME, "r", encoding="utf-8") as file: data = list(csv.DictReader(file))
        if not data: return
        need_update = any("." in row.get(field, "") for row in data for field in ["Рік випуску", "Ціна"])
        if need_update:
            for row in data:
                for field in FIELDS:
                    if field in row: row[field] = format_value(field, row[field])
            with open(FILENAME, "w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=FIELDS)
                writer.writeheader()
                writer.writerows(data)
    except Exception as e: print(f"Помилка при оновленні файлу: {e}")

def display_cars():
    if not file_exists():
        print("Файл ще не створений або порожній.")
        return
    try:
        update_file_format()
        with open(FILENAME, "r", encoding="utf-8") as file: data = list(csv.DictReader(file))
        if not data:
            print("Файл порожній.")
            return
        print("\n" + " | ".join(FIELDS))
        print("-" * 80)
        for row in data:
            print(" | ".join([format_value(field, row.get(field, "")) for field in FIELDS]))
    except Exception as e: print(f"Помилка при читанні файлу: {e}")

def clear_file():
    if file_exists():
        os.remove(FILENAME)
        print("Всі дані видалені!")
    else: print("Файл ще не створений або вже порожній.")

def get_existing_models():
    if not file_exists(): return []
    try:
        with open(FILENAME, "r", encoding="utf-8") as file:
            return [row.get("Модель", "").strip().lower() for row in csv.DictReader(file)]
    except: return []

def delete_car():
    if not file_exists():
        print("Файл ще не створений або порожній.")
        return
    models = get_existing_models()
    if not models:
        print("У файлі немає жодної моделі для видалення.")
        return
    unique_models = list(set(models))
    print("Список існуючих моделей:")
    for idx, model in enumerate(unique_models, 1): print(f"{idx}. {model}")
    try:
        choice = int(input("Оберіть модель за номером для видалення: "))
        if choice < 1 or choice > len(unique_models):
            print("Невірний вибір.")
            return
        model_to_delete = unique_models[choice - 1]
        with open(FILENAME, "r", encoding="utf-8") as file: data = list(csv.DictReader(file))
        new_data = [row for row in data if model_to_delete != row.get("Модель", "").strip().lower()]
        deleted = len(data) - len(new_data)
        if deleted == 0: print(f"Автомобіль з моделлю '{model_to_delete}' не знайдений.")
        else:
            with open(FILENAME, "w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=FIELDS)
                writer.writeheader()
                writer.writerows(new_data)
            print(f"Видалено {deleted} запис(ів) з моделлю '{model_to_delete}'!")
    except Exception as e: print(f"Помилка при видаленні: {e}")

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
        else: print("Невірний вибір. Спробуйте ще раз.")

if __name__ == "__main__": main()