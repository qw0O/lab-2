import json
import base64
from datatime import datatime, timedelta

class BusStop:
  def __init__(self, name, coordinates, time_to_next, info):
    self.name = name
    self.coordinates = coordinates
    self.time_to_next = time_to_next
    self.info = info

  
  def __init__(self):
    self.stop = []
  
  def add_stop(self, stop):
    self.stops.append(stop)

def get_total_time(self):
  total = 0
  for stop in self.stops[:-1]:
    total += stop.time_to_next
  return total

def bus_location(self, current_index, n_stops, starts_time):
  target_index = min(current_index + n_stops, len(self.stops)-1)
  target_stop = self.stops[target_index]
  
  time_in_way = 0
  for i in range(current_index, target_index):
    time_in_way += self.stops[i].time_to_next
  arrival_time = start_time + timedelta(minutes=time_in_way)
return target_stop.name, arrival_time
