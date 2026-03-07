import math
import copy
from poligoni_stellati import Vertex, Polygon, is_near
from visualizer import PolygonVisualizer

# Chiedo di inserire le coordinate dei vertici del poligono stellato
# con questo ordine: x1 y1 x2 y2 x3 y3 ...
P = Polygon()
print("Inserisci le coordinate dei vertici. Per terminare, digita 'fine'.")

idx = 1
while True:
    input_string = input(
        f"Inserisci le coordinate (x y) del vertice {idx}-esimo: ")
    if input_string.lower() == 'fine':
        break
    try:
        x, y = map(float, input_string.split())
        P.add_vertex(Vertex(f"v{idx}", x, y))
        idx += 1
    except ValueError:
        print("Input non valido. Inserisci due numeri separati da uno spazio.")


def print_vertices():
    for vertex in P.vertices:
        print(f"{vertex.name}: ({vertex.x}, {vertex.y})")
    # print(f"{P.get_v_i(1).name}: ({P.get_v_i(1).x}, {P.get_v_i(1).y})")


print("Hai creato la seguente curva poligonale:")
print_vertices()

n = len(P.vertices)

P_transformed = Polygon(list(P.vertices))
# Creiamo una copia del poligono originale per le trasformazioni
P_transformed = copy.deepcopy(P)
P_transformed.save_state()  # Salviamo lo stato iniziale nella storia

if n == 1:
    print("Il poligono stellato è un punto.")
if n == 2:
    print("Il poligono stellato è un segmento.")
    P_transformed.save_state()
if n == 3:
    print("Il poligono stellato è un triangolo.")
else:
    if not P.is_circle():
        raise ValueError("La curva poligonale non è inscritta in un cerchio.")
    # Porto la curva poliginale su circonferenza di raggio 1
    # Controlla se c'è ALMENO UN vertice fuori dalla circonferenza unitaria
    if any(not is_near(math.hypot(v.x, v.y), 1.0)
           for v in P_transformed.vertices):
        P_transformed.get_unitary_radius()
        P_transformed.save_state()

    # Elimino i vertici appartenenti ai lati
    for i in range(3, n+1):
        if is_near(P_transformed.get_rotation_angle(i), 0):
            P_transformed.eliminate_vertex(i)
            P_transformed.save_state()
            print(f"Eliminato vertice {i} perché appartiene già ad un lato.")

    # Porto il vertice v1 in (-1,0)
    if (not is_near(P_transformed.get_v(1).x, -1) or
            not is_near(P_transformed.get_v(1).y, 0)):
        if P_transformed.get_v(1).angle < math.pi:
            P_transformed.weak_translation_counterclockwise(1, math.pi)
            P_transformed.save_state()
        else:
            P_transformed.weak_translation_clockwise(1, math.pi)
            P_transformed.save_state()
    else:
        print("Vertice v1 già in (-1,0).")

    # Porto il vertice v2 in (1,0)
    if (not is_near(P_transformed.get_v(2).x, 1) or
            not is_near(P_transformed.get_v(2).y, 0)):
        if P_transformed.get_v(2).angle < math.pi:
            P_transformed.weak_translation_clockwise(2, 0)
            P_transformed.save_state()
        else:
            P_transformed.weak_translation_counterclockwise(2, 0)
            P_transformed.save_state()
    else:
        print("Vertice v2 già in (1,0).")

    # Caso in cui la poligonale sarà sinistrorsa
    if P_transformed.is_left_turn(2):
        print("La poligonale sarà sinistrorsa.")
        # Ciclo sui vertici da 4 a n
        curr_idx = 4
        while curr_idx <= len(P_transformed.vertices):
            # Se elimino il vertice 4 curr_idx potrebbe diminuire
            # ma devo partire dal 4
            if curr_idx <= 3:
                curr_idx = 4
            """ # Caso in cui i è dispari
            if curr_idx % 2 == 1:
                # Caso A
                if P_transformed.is_right_turn(curr_idx-1):
                    # Caso A1
                    if P_transformed.is_left_turn(curr_idx):

                        P_transformed.move_to_midpoint(curr_idx-1)
                        P_transformed.save_state()

                        P_transformed.eliminate_vertex(curr_idx-1)
                        P_transformed.save_state()

                        curr_idx += 1
                    # Caso A2
                    if P_transformed.is_right_turn(curr_idx):
                        # Caso A21
                        if P_transformed.is_clockwise(
                                [P_transformed.get_v(curr_idx),
                                  P_transformed.get_v(curr_idx+1),
                                  P_transformed.get_v(2)]):
                            if P_transformed.is_clockwise(
                                    [P_transformed.get_v(curr_idx),
                                      P_transformed.get_v(curr_idx+1),
                                      P_transformed.get_v(curr_idx-2)]):
                                P_transformed.move_and_eliminate(curr_idx-2)
                            else:
                                angle = (
                                    P_transformed.get_v(curr_idx-2).angle +
                                    math.pi / 1000)
                                P_transformed.
                                    weak_translation_counterclockwise(
                                        curr_idx-2, angle)
                                P_transformed.move_and_eliminate(curr_idx-2)"""

            if curr_idx % 2 == 0:
                # Caso C
                if P_transformed.is_right_turn(curr_idx-1):
                    # Caso C1
                    if P_transformed.is_left_turn(curr_idx):

                        P_transformed.move_to_midpoint(curr_idx-1)
                        P_transformed.save_state()

                        P_transformed.eliminate_vertex(curr_idx-1)
                        P_transformed.save_state()
                        # Decremento curr_idx di 1 perché ho tolto un vertice
                        # e devo ripetere il controllo sul vertice corrente
                        curr_idx -= 1
                        break
                    # Caso C2
                    else:
                        # Caso C21
                        if P_transformed.is_counterclockwise(
                                [P_transformed.get_v(curr_idx),
                                 P_transformed.get_v(curr_idx+1),
                                 P_transformed.get_v(1)]):
                            if P_transformed.is_counterclockwise(
                                    [P_transformed.get_v(curr_idx),
                                     P_transformed.get_v(curr_idx+1),
                                     P_transformed.get_v(curr_idx-2)]):
                                P_transformed.move_and_eliminate(
                                    curr_idx-2)
                            else:
                                angle = (
                                    P_transformed.get_v(curr_idx-2).angle -
                                    math.pi / 1000)
                                P_transformed.\
                                    weak_translation_clockwise(
                                        curr_idx-2, angle)
                                P_transformed.move_and_eliminate(
                                    curr_idx-2)
                        continue
                continue


# ESEMPIO CASO C1:
# V1 = -0.866025 0.5
# V2 = 0.866025 0.5
# V3 = -0.707107 0.707107
# V4 = 0.707107 0.707107
# V5 = 0 1
# fine


# FINE DELL'ALGORITMO - INIZIO GRAFICA

print("\nAlgoritmo completato con successo!")

# Creiamo il visualizzatore passandogli tutta la storia
# del poligono
vis = PolygonVisualizer(P_transformed.history)

# Avviamo l'animazione
vis.show(interval=1000)
