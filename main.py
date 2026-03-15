import math
import copy
import random
from poligoni_stellati import Vertex, Polygon, is_near, generate_random_polygon, print_vertices
from visualizer import PolygonVisualizer


# PER IL MOMENTO INSERISCO I VERTICI NEL MAIN

"""# P = Polygon()
# print("Inserisci le coordinate dei vertici. Per terminare, digita 'fine'.")

idx = 1
while True:
    input_string = input(
        f"Inserisci le coordinate (x y) del vertice {idx}-esimo: ")
    if input_string.lower() == "fine":
        break
    try:
        x, y = map(float, input_string.split())
        P.add_vertex(Vertex(f"v{idx}", x, y))
        idx += 1
    except ValueError:
        print("Input non valido. Inserisci due numeri separati da uno"
              " spazio.")"""



# Genero poligoni casuali
P = generate_random_polygon(10)
while not P.is_left_turn(2):
    P = generate_random_polygon(10)

P = Polygon([
            Vertex("v1", -0.5068742002067848, 0.8620200375656776),
            Vertex("v2", 0.7520253624389999, 0.6591341701417784),
            Vertex("v3", -0.3092065180782928, 0.9509949154322006),
            Vertex("v4", 0.42361462122292637, -0.9058425098692138),
            Vertex("v5", 0.7901677992712248, 0.6128905685315033),
            Vertex("v6", -0.22855411471047704, -0.97353120989977),
            Vertex("v7", -0.5166463961669043, -0.8561988678617545),
            Vertex("v8", 0.08543763157117978, -0.9963435206350806),
            Vertex("v9", 0.69989885290182, -0.7142419727982363),
            Vertex("v10", 0.13047116695475403, 0.9914521040340096)
        ])

print("Hai creato la seguente curva poligonale:")
print_vertices(P)

# Creiamo una copia del poligono originale per le trasformazioni
P_transformed = Polygon(list(P.vertices))
P_transformed = copy.deepcopy(P)
P_transformed.save_state()  # Salviamo lo stato iniziale nella storia

P_transformed.reduce_polygon()
P_transformed.get_equispaced_vertices()

# FINE DELL'ALGORITMO - INIZIO GRAFICA

print("\nAlgoritmo completato con successo!")

# Creiamo il visualizzatore passandogli tutta la storia
# del poligono
vis = PolygonVisualizer(P_transformed.history)

# Avviamo l'animazione
vis.show(interval=1000)
