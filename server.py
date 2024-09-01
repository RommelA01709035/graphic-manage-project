'''
Juan Eduardo Rosas Ceron
Imanol Muñiz Ramirez
Romel Pacheco Hernandez

Proyecto Modelacion de sistemas multiagentes y graficas computacionales
'''

# Librerias
from flask import Flask, request, jsonify
#from mesa import Agent, Model
#from mesa.space import MultiGrid
#from mesa.time import RandomActivation
#import numpy as np
#import pandas as pd
#import seaborn as sn

# Clase cell que nos ayuda a guardar informacion
class Cell():
    def __init__(self, x, y, wall):
        # posicion
        self.pos = (x, y)

        # valor de los muros
        if wall[0] == '1': self.up = True
        else: self.up = False
        if wall[1] == '1': self.left = True
        else: self.left = False
        if wall[2] == '1': self.down = True
        else: self.down = False
        if wall[3] == '1': self.right = True
        else: self.right = False

        # valor de los puntos de interes 1 si es falsa alarma 2 si es una victima
        self.poi = 0

        # valor del fuego 1 si es un humo 2 si es fuego
        self.fire = 0

        # arreglo con la posicion de la casilla donde se conecta con puerta
        self.door = []

        # True si la casilla es una entrada a la estructura
        self.entrance = False

# Abrimos el archivo txt 
with open('mapa.txt', 'r') as map:
    text = map.read()

# Obtenemos los valores de los muros
walls = []
for i in range(8):
    for j in range(6):
        new_wall = text[:4]
        walls.append(new_wall)
        text = text[5:]

# Obtenemos los valores de los poi (point of interest)
pois = []
for i in range(3):
    pos_poi_x = text[0]
    pos_poi_y = text[2]
    pos_poi_state = text[4]
    text = text[6:]
    pois.append( (pos_poi_x, pos_poi_y, pos_poi_state) )

# Obtenemos los valores del fuego
fires = []
for i in range(10):
    pos_fire_x = text[0]
    pos_fire_y = text[2]
    text = text[4:]
    fires.append( (pos_fire_x, pos_fire_y) )

# Obtenemos las casillas que estan conectadas por una puerta
doors = []
for i in range(8):
    pos_doorA_x = text[0]
    pos_doorA_y = text[2]
    pos_doorB_x = text[4]
    pos_doorB_y = text[6]
    text = text[8:]
    doors.append( ( (pos_doorA_x, pos_doorA_y), (pos_doorB_x, pos_doorB_y) ) )

# Obtenemos
entrances = []
for i in range(4):
    pos_entrance_x = text[0]
    pos_entrance_y = text[2]
    text = text[4:]
    entrances.append( (pos_entrance_x, pos_entrance_y) )

cells = []
for i in range(6):
    for j in range(8):
        w = walls[0]
        del walls[0]

        c = Cell(i + 1,j + 1,w)
        cells.append(c)

        if (str(i + 1), str(j + 1), 'v') in pois:
            c.poi = 2
        elif (str(i + 1), str(j + 1), 'f') in pois:
            c.poi = 1

        if (str(i + 1), str(j + 1)) in fires:
            c.fire = 2

        for d in doors:
            if (str(i + 1), str(j + 1)) == d[0]:
                c.door = d[1]
            elif (str(i + 1), str(j + 1)) == d[1]:
                c.door = d[0]

        if (str(i + 1), str(j + 1)) in entrances:
            c.entrance = True

# Diccionario con la composicion inicial de celdas
map = {}

for c in cells:
    map[f"Cell {c.pos[0]}{c.pos[1]}"] = [c.pos[0], c.pos[1], c.up, c.left, c.down, c.right, c.poi, c.fire, c.door, c.entrance]

# API que manda los datos a Unity
app = Flask(__name__)

@app.route("/", methods=['GET'])
def get_data():
    return jsonify(map)

if __name__ == '__main__':
    app.run(debug=True)