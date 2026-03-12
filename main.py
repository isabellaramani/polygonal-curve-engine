import math
import copy
import random
from poligoni_stellati import Vertex, Polygon, is_near, generate_random_polygon
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


def print_vertices(Pol: Polygon) -> None:
    """Stampa nome e coordinate dei vertici del poligono."""
    for vertex in Pol.vertices:
        print(f"{vertex.name}: ({vertex.x}, {vertex.y})")
    # print(f"{P.get_v_i(1).name}: ({P.get_v_i(1).x}, {P.get_v_i(1).y})")


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
