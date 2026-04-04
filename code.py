import json
import base64
from datetime import datetime, timedelta  # Исправлено: правильный импорт

class BusStop:
    def __init__(self, name, coordinates, time_to_next, info):
        self.name = name
        self.coordinates = coordinates
        self.time_to_next = time_to_next
        self.info = info

class BusRoute:
    def __init__(self):
        self.stops = []  # Исправлено: имя переменной согласовано с методами

    def add_stop(self, stop):
        self.stops.append(stop)

    def get_total_time(self):
        total = 0
        for stop in self.stops[:-1]:
            total += stop.time_to_next
        return total

    def bus_location(self, current_index, n_stops, start_time):
        # Исправлено: имя аргумента start_time
        target_index = min(current_index + n_stops, len(self.stops) - 1)
        target_stop = self.stops[target_index]
        
        time_in_way = 0
        for i in range(current_index, target_index):
            time_in_way += self.stops[i].time_to_next
        
        arrival_time = start_time + timedelta(minutes=time_in_way)
        return target_stop.name, arrival_time

    def get_reverse_route(self):
        rev_route = BusRoute()
        reversed_stops = self.stops[::-1]
        for i in range(len(reversed_stops)):
            original = reversed_stops[i]
            if i < len(reversed_stops) - 1:
                # Берем время до следующей из "предыдущей" остановки оригинала
                time = reversed_stops[i+1].time_to_next 
            else:
                time = 0     
            
            # Важно: создание остановки должно быть ВНУТРИ цикла for (убрал лишний отступ)
            new_stop = BusStop(original.name, original.coordinates, time, "Обратно: " + original.info)
            rev_route.add_stop(new_stop)
        return rev_route

    def save_to_file(self, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            for stop in self.stops:
                data = {
                    "n": stop.name, 
                    "c": stop.coordinates, 
                    "t": stop.time_to_next, 
                    "i": stop.info
                }
                json_data = json.dumps(data, ensure_ascii=False)
                b64_data = base64.b64encode(json_data.encode('utf-8')).decode()
                f.write(b64_data + '\n')

# --- ПРИМЕР ЗАПУСКА ---
if __name__ == "__main__":
    # 1. Создаем маршрут
    my_route = BusRoute()
    my_route.add_stop(BusStop("Вокзал", (55.7, 37.6), 10, "Старт"))
    my_route.add_stop(BusStop("Парк", (55.8, 37.7), 15, "Зеленая зона"))
    my_route.add_stop(BusStop("Конечная", (55.9, 37.8), 0, "Конец пути"))

    # 2. Считаем общее время
    print(f"Общее время: {my_route.get_total_time()} мин.")

    # 3. Где будет автобус через 2 остановки от начала?
    now = datetime.now()
    name, arr_time = my_route.bus_location(0, 2, now)
    print(f"Через 2 остановки будет: {name}, Время: {arr_time.strftime('%H:%M')}")

    # 4. Сохраняем в файл
    my_route.save_to_file("route_data.txt")
    print("Данные сохранены в Base64")

