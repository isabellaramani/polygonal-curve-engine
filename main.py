import math
import copy
import random
from poligoni_stellati import (
    Vertex,
    Polygon,
    is_near,
    generate_random_polygon,
    print_vertices,
)
from visualizer import PolygonVisualizer


# PER IL MOMENTO INSERISCO I VERTICI NEL MAIN

# # P = Polygon()
# # print("Inserisci le coordinate dei vertici. Per terminare, digita 'fine'.")

# idx = 1
# while True:
#     input_string = input(
#         f"Inserisci le coordinate (x y) del vertice {idx}-esimo: ")
#     if input_string.lower() == "fine":
#         break
#     try:
#         x, y = map(float, input_string.split())
#         P.add_vertex(Vertex(f"v{idx}", x, y))
#         idx += 1
#     except ValueError:
#         print("Input non valido. Inserisci due numeri separati da uno"
#               " spazio.")


# GONTROLLO 100 POLIGONI CASUALI

# for i in range(1,100):
#     # Genero poligoni casuali
#     P = generate_random_polygon(10)
#     while not P.is_left_turn(2):
#         P = generate_random_polygon(10)

#     print("Hai creato la seguente curva poligonale:")
#     print_vertices(P)

#     # Creiamo una copia del poligono originale per le trasformazioni
#     P_transformed = Polygon(list(P.vertices))
#     P_transformed = copy.deepcopy(P)
#     P_transformed.save_state()  # Salviamo lo stato iniziale nella storia

#     P_transformed.reduce_polygon()
#     P_transformed.get_equispaced_vertices()

P = Polygon(
    [
        Vertex("v1", 0.9386937996125804, 0.34475201314698195),
        Vertex("v2", 0.5577227493581884, -0.8300273097003154),
        Vertex("v3", 0.8495709053973892, -0.5274744322735088),
        Vertex("v4", 0.37382803211697113, 0.9274980336386449),
        Vertex("v5", -0.9282248435043767, 0.3720196767662637),
        Vertex("v6", 0.11082186843019914, 0.9938402856986829),
        Vertex("v7", 0.055353192646783844, -0.9984668367371087),
        Vertex("v8", 0.09183406603173161, 0.9957743239891654),
        Vertex("v9", -0.05595823175927017, -0.9984331105779575),
        Vertex("v10", 0.5700494503892732, -0.821610384617239),
    ]
)

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
