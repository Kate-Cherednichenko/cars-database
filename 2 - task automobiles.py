import csv

FILENAME = "cars.csv"
FIELDS = ["Марка", "Модель", "Тип кузова", "Обєм двигуна", "Рік випуску", "Ціна"]

def search_cars():
    while True:
        try:
            with open(FILENAME, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                data = list(reader)
                if not data:
                    print("Файл порожній.")
                    return
                
                print("\nВиберіть критерій пошуку:")
                print("1. Марка")
                print("2. Модель")
                print("3. Рік випуску")
                print("4. Ціна")
                print("5. Вийти")
                choice = input("Оберіть варіант (1-5): ").strip()

                if choice == "5":
                    print("Вихід із програми.")
                    break
                
                results = []
                if choice == "1":
                    brand = input("Марка: ").strip().lower()
                    results = [car for car in data if car["Марка"].strip().lower() == brand]
                elif choice == "2":
                    model = input("Модель: ").strip().lower()
                    results = [car for car in data if car["Модель"].strip().lower() == model]
                elif choice == "3":
                    try:
                        min_year = int(input("Рік випуску від: ").strip())
                        max_year = int(input("Рік випуску до: ").strip())
                        results = [car for car in data if min_year <= int(car["Рік випуску"]) <= max_year]
                    except ValueError:
                        print("Помилка: введіть коректні числові значення для року.")
                        continue
                elif choice == "4":
                    try:
                        min_price = int(input("Мінімальна ціна: ").strip())
                        max_price = int(input("Максимальна ціна: ").strip())
                        results = [car for car in data if min_price <= int(car["Ціна"]) <= max_price]
                    except ValueError:
                        print("Помилка: введіть коректні числові значення для ціни.")
                        continue
                else:
                    print("Невірний вибір! Спробуйте ще раз.")
                    continue
                
                if results:
                    print(f"\n{' | '.join(FIELDS)}")
                    print("-" * 60)
                    for row in results:
                        print(" | ".join(row[field] for field in FIELDS))
                else:
                    print("Нічого не знайдено.")
        except FileNotFoundError:
            print("Файл ще не створений. Додайте перший запис.")
            break

if __name__ == "__main__":
    search_cars()
