from flask import Flask, request, jsonify

# Clase Cell que nos ayuda a guardar información
class Cell():
    def __init__(self, x, y, wall):
        # posición
        self.pos = (x, y)

        # valor de los muros
        self.up = wall[0] == '1'
        self.left = wall[1] == '1'
        self.down = wall[2] == '1'
        self.right = wall[3] == '1'

        # valor de los puntos de interés 1 si es falsa alarma, 2 si es una víctima
        self.poi = 0

        # valor del fuego 1 si es humo, 2 si es fuego
        self.fire = 0

        # arreglo con la posición de la casilla donde se conecta con puerta
        self.door = []

        # True si la casilla es una entrada a la estructura
        self.entrance = False

# Abrimos el archivo txt
with open('mapa.txt', 'r') as map_file:
    text = map_file.read()

# Obtenemos los valores de los muros
walls = []
for i in range(8):
    for j in range(6):
        new_wall = text[:4]
        walls.append(new_wall)
        text = text[5:]

# Obtenemos los valores de los puntos de interés (POI)
pois = []
for i in range(3):
    pos_poi_x = text[0]
    pos_poi_y = text[2]
    pos_poi_state = text[4]
    text = text[6:]
    pois.append((pos_poi_x, pos_poi_y, pos_poi_state))

# Obtenemos los valores del fuego
fires = []
for i in range(10):
    pos_fire_x = text[0]
    pos_fire_y = text[2]
    text = text[4:]
    fires.append((pos_fire_x, pos_fire_y))

# Obtenemos las casillas que están conectadas por una puerta
doors = []
for i in range(8):
    pos_doorA_x = text[0]
    pos_doorA_y = text[2]
    pos_doorB_x = text[4]
    pos_doorB_y = text[6]
    text = text[8:]
    doors.append(((pos_doorA_x, pos_doorA_y), (pos_doorB_x, pos_doorB_y)))

# Obtenemos las posiciones de las entradas
entrances = []
for i in range(4):
    pos_entrance_x = text[0]
    pos_entrance_y = text[2]
    text = text[4:]
    entrances.append((pos_entrance_x, pos_entrance_y))

# Inicializamos las celdas
cells = []
for i in range(6):
    for j in range(8):
        w = walls.pop(0)
        c = Cell(i + 1, j + 1, w)
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

# Diccionario con la composición inicial de celdas
map_data = {}

for c in cells:
    cell_key = f"Cell {c.pos[0]}{c.pos[1]}"
    
    if cell_key not in map_data:
        map_data[cell_key] = {
            "posicion_x": c.pos[0],
            "posicion_y": c.pos[1],
            "muro_arriba": c.up,
            "muro_izquierda": c.left,
            "muro_abajo": c.down,
            "muro_derecha": c.right,
            "punto_interes": c.poi,
            "fuego": c.fire,
            "puerta": c.door,
            "entrada": c.entrance,
            "coordenadas_poi": [],
            "coordenadas_victimas": [],
            "coordenadas_fuego": [],
            "coordenadas_entradas": []
        }
    
    # Actualizar coordenadas de puntos de interés
    if c.poi == 2:  # Víctima
        map_data[cell_key]["coordenadas_victimas"].append(c.pos)
    elif c.poi == 1:  # Falsa alarma
        # Solo se agrega si no hay fuego o víctimas en la misma celda
        if map_data[cell_key]["fuego"] == 0 and not map_data[cell_key]["coordenadas_victimas"]:
            map_data[cell_key]["coordenadas_poi"].append(c.pos)
    
    # Actualizar coordenadas de fuego
    if c.fire == 2:  # Fuego
        map_data[cell_key]["coordenadas_fuego"].append(c.pos)
    
    # Actualizar coordenadas de entradas
    if c.entrance:
        map_data[cell_key]["coordenadas_entradas"].append(c.pos)

print(fires)
print(doors)
print(entrances)
print(pois)

# API que envía los datos a Unity
app = Flask(__name__)

@app.route("/", methods=['GET'])
def get_data():
    print(map_data)
    return jsonify(map_data)

if __name__ == '__main__':
    app.run(debug=True)
