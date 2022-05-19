from PyQt5 import QtWidgets, QtCore
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os
from random import randint

from enum import Enum

# типы машин
class CarType(Enum):

  KEYCAR = 2
  SEDAN = 3
  SUV = 5
  MINIVAN = 5
  MICROBUS = 7

# режимы мойки автомобиля
class WashType(Enum):

  WATER = 20
  FOAM = 50 
  WAX = 10
  VACUUM = 40

import random

class Place():

  def __init__(self):
    self.cars = []
    self.washes = 0
    self.timeLeft = 0
  def init(self):
    self.washes = random.randint(2, 5) # за одну мойку от 2 до 5 режимов
    self.timeLeft = self.cars[0].value * self.washes # высчитаем время

class MainWindow(QtWidgets.QMainWindow):

  def __init__(self, places: list, *args, **kwargs):
    super(MainWindow, self).__init__(*args, **kwargs)
    
    self.places = places
    self.income = 0


    self.graphWidget = pg.PlotWidget()
    self.setCentralWidget(self.graphWidget)

    self.x = [0]
    self.y = [0]

    self.graphWidget.setBackground('w')

    pen = pg.mkPen(color=(255, 0, 0))
    self.data_line =  self.graphWidget.plot(self.x, self.y, pen=pen)
    self.timer = QtCore.QTimer()
    self.timer.setInterval(100)
    self.timer.timeout.connect(self.update_plot_data)
    self.timer.start()

  def minuteForward(self, place):
    print(f'Income: {self.income}, Places: {len(self.places)}, Cars: {len(place.cars)}')
    if place.timeLeft == 0: # если время кончилось
      if len(place.cars) == 0:
        return
      else:
        place.cars.pop(0)
        if len(place.cars) == 0:
          return
        place.washes = random.randint(2, 5)
        place.timeLeft = place.cars[0].value * place.washes

    else:
      place.washes -= 1
      place.timeLeft -= 1
      self.income += random.choice(list(WashType)).value
  
  def update_plot_data(self):
    for place in self.places:
        self.minuteForward(place)

    self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.

    self.y.append(self.income)  # Add a new random value.

    self.data_line.setData(self.x, self.y)

places = list()

for i in range(4):
  places.append(Place())
  cars = list()
  for j in range(8):
    cars.append(random.choice(list(CarType)))
  places[i].cars = cars
  places[i].init()

app = QtWidgets.QApplication(sys.argv)
w = MainWindow(places)
w.show()
sys.exit(app.exec_())