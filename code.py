import base64

class BusStop:
    def __init__(self, name, coords, time_to_next):
        self.name = name
        self.coords = coords           
        self.time_to_next = time_to_next

    def to_string(self):
        return f"{self.name}|{self.coords[0]},{self.coords[1]}|{self.time_to_next}"


class BusRoute:
    """Класс, описывающий маршрут автобуса."""
    def __init__(self):
        self.stops = []

    def add_stop(self, name, coords, time_to_next=0):
        """1. Добавление остановки в маршрут."""
        new_stop = BusStop(name, coords, time_to_next)
        self.stops.append(new_stop)

    def calculate_total_time(self):
        """2. Расчет общего времени маршрута."""
        total_time = sum(stop.time_to_next for stop in self.stops)
        return total_time

    def get_bus_after_n_stops(self, current_index, n):
        """3. Определение, где будет автобус через N остановок 
        и расчет времени прибытия."""
        if current_index < 0 or current_index >= len(self.stops):
            return "Ошибка: Неверный индекс текущей остановки."
        
        target_index = current_index + n
        
        if target_index >= len(self.stops):
            return "Автобус доедет до конечной остановки раньше."
            
        target_stop = self.stops[target_index]
        travel_time = 0
        
        for i in range(current_index, target_index):
            travel_time += self.stops[i].time_to_next
            
        return target_stop.name, travel_time

    def build_reverse_route(self):
        """4. Построение обратного маршрута."""
        reversed_route = BusRoute()
        
        for i in range(len(self.stops) - 1, -1, -1):
            name = self.stops[i].name
            coords = self.stops[i].coords
            
            if i > 0:
                time_to_next = self.stops[i-1].time_to_next
            else:
                time_to_next = 0 # Для конечной остановки (которая стала первой)
                
            reversed_route.add_stop(name, coords, time_to_next)
            
        return reversed_route

    def save_to_base64_file(self, filename):
        """Сохранение маршрута в текстовый файл (каждая строка в Base64)."""
        with open(filename, 'w', encoding='utf-8') as file:
            for stop in self.stops:
                stop_str = stop.to_string()
                encoded_bytes = base64.b64encode(stop_str.encode('utf-8'))
                encoded_str = encoded_bytes.decode('utf-8')
                file.write(encoded_str + '\n')
        print(f"Маршрут успешно сохранен в файл: {filename}")


# === Пример использования (Тестирование) ===
if __name__ == "__main__":
    route = BusRoute()

    #Пример остановок
    route.add_stop("ВДНХ", (55.820251, 37.632709), 1)
    route.add_stop("Метро ВДНХ", (55.822508, 37.641941), 13)
    route.add_stop("Сергея Эйзенштейна", (55.82981, 37.64621), 7)
    route.add_stop("1-й Сельскохозяйственный проезд", (55.831175, 37.646157), 8)
    route.add_stop("Киностудия им. Горького", (55.834720, 37.635839), 0)

    print("--- Прямой маршрут ---")
    for s in route.stops:
        print(f"Остановка: {s.name}, до следующей: {s.time_to_next} мин.")

    # Проверка общего времени
    print(f"\nОбщее время маршрута: {route.calculate_total_time()} минут.")

    # Проверка: где будет автобус через 3 остановки
    start_idx = 0
    stops_to_go = 3
    result = route.get_bus_after_n_stops(start_idx, stops_to_go)
    if isinstance(result, tuple):
        destination, time_needed = result
        print(f"\nЕсли сесть на остановке '{route.stops[start_idx].name}', "
              f"через {stops_to_go} остановки(ок) автобус будет на остановке '{destination}'.")
        print(f"Время прибытия (в пути): {time_needed} минут.")
    else:
        print(result)

    # Проверка обратного маршрута
    print("\n--- Обратный маршрут ---")
    rev_route = route.build_reverse_route()
    for s in rev_route.stops:
        print(f"Остановка: {s.name}, до следующей: {s.time_to_next} мин.")

    # Сохранение в файл, проверка & декодирование
    print("\n--- Сохранение ---")
    route.save_to_base64_file("route_data.txt")

    print("\n--- Проверка чтения из файла ---")
with open("route_data.txt", "r") as f:
    for line in f:
        decoded = base64.b64decode(line).decode('utf-8')
        print(f"Декодировано: {decoded}")
