import math
import copy
from poligoni_stellati import Vertex, Polygon, is_near
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

# Verifiche dei passi dell'algoritmo su casi specifici

# Caso A1 su v5
P = Polygon([Vertex("v1", -0.866025, 0.5), Vertex("v2", 0.866025, 0.5),
             Vertex("v3", 0, 1), Vertex("v4", 0.707107, -0.707107),
             Vertex("v5", -0.707107, -0.707107), Vertex("v6", 0, -1)])
# Verificato"""

"""# Caso A211 su v7
    P = Polygon([Vertex("v1", -0.866025, 0.5), Vertex("v2", 0.866025, 0.5),
                Vertex("v3", -0.707107, 0.707107), Vertex("v4",
                                                        0.707107, -0.707107),
                Vertex("v5", 0.707107, 0.707107), Vertex("v6", 0, -1),
                Vertex("v7", -0.866025, -0.5), Vertex("v8", 0, 1)])
    # Verificato"""

"""# Caso A212 su v7
    P = Polygon([Vertex("v1", -0.866025, 0.5), Vertex("v2", 1, 0),
                Vertex("v3", -0.707107, 0.707107), Vertex("v4",
                                                        0.707107, -0.707107),
                Vertex("v5", 0.707107, 0.707107), Vertex("v6", 0, -1),
                Vertex("v7", -0.866025, -0.5), Vertex("v8", 0.866025, 0.5)])
    # Verificato"""

"""# Caso A22 su v7
    P = Polygon([Vertex("v1", -0.866025, 0.5), Vertex("v2", 1, 0),
                Vertex("v3", -0.707107, 0.707107), Vertex("v4",
                                                        0.707107, -0.707107),
                Vertex("v5", 0.707107, 0.707107), Vertex(
                    "v6", -0.707107, -0.707107),
                Vertex("v7", 0, 1), Vertex("v8", 0, -1)])
    # Verificato"""

"""# Caso A231 su v5
    P = Polygon([Vertex("v1", -0.866025, 0.5), Vertex("v2", 1, 0),
                Vertex("v3", 0, 1), Vertex("v4",
                                            0, -1),
                Vertex("v5", -0.707107, -0.707107), Vertex(
                    "v6", 0.707107, -0.707107),
                Vertex("v7", -0.707107, 0.707107)])
    # Verificato"""

"""# Caso A2321 su v5
    P = Polygon([Vertex("v1", -1, 0), Vertex("v2", 1, 0),
                Vertex("v3", 0, 1), Vertex("v4",
                                            0, -1),
                Vertex("v5", -0.707107, -0.707107), Vertex(
                    "v6", 0.707107, -0.707107),
                Vertex("v7", -0.866025, -0.5), Vertex(
                    "v8", 0.866025, 0.5)])
    # Verificato"""

"""# Caso A2322 su v5
    P = Polygon([Vertex("v1", -1, 0), Vertex("v2", 1, 0),
                Vertex("v3", 0, 1), Vertex("v4",
                                            0.707107, -0.707107),
                Vertex("v5", -0.707107, -0.707107), Vertex(
                    "v6", 0.866025, -0.5),
                Vertex("v7", -0.866025, -0.5), Vertex(
                    "v8", 0, -1)])
    # Verificato"""

"""# Caso B21 su v5
    P = Polygon([Vertex("v1", -1, 0), Vertex("v2", 1, 0),
                Vertex("v3", 0, 1), Vertex("v4",
                                            0, -1),
                Vertex("v5", 0.707107, -0.707107), Vertex(
                    "v6", 0.5, -0.866025)
                ])
    # Verificato"""

"""# Caso B2211 su v5
    P = Polygon([Vertex("v1", -1, 0), Vertex("v2", 1, 0),
                Vertex("v3", 0, 1), Vertex("v4",
                                            0, -1),
                Vertex("v5", 0.707107, -0.707107), Vertex(
                    "v6", -0.5, -0.866025), Vertex("v7", 0.866025, 0.5)
                ])
    # Verificato"""

"""# Caso B22121 su v5
P = Polygon([Vertex("v1", -1, 0), Vertex("v2", 1, 0),
             Vertex("v3", 0, 1), Vertex("v4",
                                        0, -1),
             Vertex("v5", 0.707107, -0.707107), Vertex(
    "v6", -0.5, -0.866025), Vertex("v7", 0.866025, -0.5), Vertex("v8", -0.5, 0.866025)
])
# Verificato"""

"""# Caso B22122 su v5
    P = Polygon([Vertex("v1", -1, 0), Vertex("v2", 1, 0),
                Vertex("v3", 0, 1), Vertex("v4",
                                            0, -1),
                Vertex("v5", 0.707107, -0.707107), Vertex(
                    "v6", -0.866025, -0.5), Vertex("v7", 0.866025, -0.5), Vertex("v8", -0.5, -0.866025)
                ])
    # Verificato"""

"""# Caso B222 su v7
P = Polygon([Vertex("v1", -1, 0), Vertex("v2", 1, 0),
             Vertex("v3", -0.707107, 0.707107), Vertex("v4",
                                                       0, -1),
             Vertex("v5", 0, 1), Vertex(
    "v6", -0.866025, -0.5), Vertex("v7", 0.866025, -0.5), Vertex("v8", 0.5, 0.866025)
])
# Verificato"""

"""# Caso C1 su v4
        P = Polygon([Vertex("v1", -0.866025, 0.5),
                Vertex("v2", 0.866025, 0.5), Vertex("v3", -0.707107, 0.707107),
                Vertex("v4", 0.707107, 0.707107), Vertex("v5", 0, 1)])
    # Verificato"""

"""# Caso C211 su v6
P = Polygon([Vertex("v1", -0.866025, 0.5), Vertex("v2", 0.866025, 0.5),
             Vertex("v3", -0.707107, 0.707107), Vertex("v4",
                                                       0, -1),
             Vertex("v5", 0.707107, 0.707107), Vertex(
                 "v6", 0.707107, -0.707107),
             Vertex("v7", 0.5, -0.866025)])
# Verificato"""

"""# Caso C212 su v6
P = Polygon([Vertex("v1", -0.866025, 0.5), Vertex("v2", 0.866025, 0.5),
             Vertex("v3", -0.707107, 0.707107), Vertex("v4",
                                                       0, -1),
             Vertex("v5", 0.707107, 0.707107), Vertex(
                 "v6", 0.707107, -0.707107),
             Vertex("v7", -0.5, -0.866025)])
# Verificato"""

"""# Caso C22 su v8
P = Polygon([Vertex("v1", -0.866025, 0.5), Vertex("v2", 1, 0),
             Vertex("v3", 0.707107, 0.707107), Vertex("v4",
                                                      0.707107, -0.707107),
             Vertex("v5", -0.707107, 0.707107), Vertex(
                 "v6", -0.707107, -0.707107),
             Vertex("v7", 0.5, 0.866025),
             Vertex("v8", 0, -1), Vertex("v9", 0, 1)])
# Verificato"""


def print_vertices():
    for vertex in P.vertices:
        print(f"{vertex.name}: ({vertex.x}, {vertex.y})")
    # print(f"{P.get_v_i(1).name}: ({P.get_v_i(1).x}, {P.get_v_i(1).y})")


print("Hai creato la seguente curva poligonale:")
print_vertices()

n = len(P.vertices)

# Creiamo una copia del poligono originale per le trasformazioni
P_transformed = Polygon(list(P.vertices))
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
    if any(not is_near(math.hypot(v.x, v.y), 1.0) for v in P_transformed.vertices):
        P_transformed.get_unitary_radius()
        P_transformed.save_state()

    # Elimino i vertici appartenenti ai lati
    for i in range(3, n + 1):
        if is_near(P_transformed.get_rotation_angle(i), 0):
            P_transformed.eliminate_vertex(i)
            P_transformed.save_state()
            print(f"Eliminato vertice {i} perché appartiene già ad un lato.")

    # Porto il vertice v1 in (-1,0)
    if not is_near(P_transformed.get_v(1).x, -1) or not is_near(
        P_transformed.get_v(1).y, 0
    ):
        if P_transformed.get_v(1).angle < math.pi:
            P_transformed.weak_translation_counterclockwise(1, math.pi)
            P_transformed.save_state()
        else:
            P_transformed.weak_translation_clockwise(1, math.pi)
            P_transformed.save_state()
    else:
        print("Vertice v1 già in (-1,0).")

    # Porto il vertice v2 in (1,0)
    if not is_near(P_transformed.get_v(2).x, 1) or not is_near(
        P_transformed.get_v(2).y, 0
    ):
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
        while curr_idx <= n + 2:
            # Se elimino il vertice 4 curr_idx potrebbe diminuire
            # ma devo partire dal 4
            if curr_idx <= 3:
                curr_idx = 4
            print(f"Sto processando il vertice v{curr_idx}")

            # Caso in cui i è dispari
            if curr_idx % 2 == 1:
                # Caso A
                if P_transformed.is_right_turn(curr_idx-1):
                    print("Caso A")
                    # Caso A1
                    if P_transformed.is_left_turn(curr_idx):
                        print("Caso A1")
                        P_transformed.move_to_midpoint(curr_idx-1)
                        P_transformed.save_state()

                        P_transformed.eliminate_vertex(curr_idx-1)
                        P_transformed.save_state()
                    # Caso A2
                    else:
                        print("Caso A2")
                        # Caso A21
                        if P_transformed.is_clockwise(
                                [P_transformed.get_v(curr_idx),
                                 P_transformed.get_v(curr_idx+1),
                                 P_transformed.get_v(2)]):
                            print("Caso A21")
                            # Caso A211
                            if P_transformed.is_clockwise(
                                    [P_transformed.get_v(curr_idx),
                                     P_transformed.get_v(curr_idx+1),
                                     P_transformed.get_v(curr_idx-2)]):
                                print("Caso A211")
                                P_transformed.move_to_midpoint(curr_idx-1)
                                P_transformed.save_state()

                                P_transformed.eliminate_vertex(curr_idx-1)
                                P_transformed.save_state()

                            # Caso A212
                            else:
                                print("Caso A212")
                                angle = P_transformed.get_v(
                                    curr_idx+1).angle / 2
                                P_transformed.\
                                    weak_translation_clockwise(
                                        curr_idx-2, angle)
                                P_transformed.save_state()

                                P_transformed.move_to_midpoint(curr_idx-1)
                                P_transformed.save_state()

                                P_transformed.eliminate_vertex(curr_idx-1)
                                P_transformed.save_state()

                        # Caso A22
                        if P_transformed.is_clockwise(
                                [P_transformed.get_v(curr_idx),
                                 P_transformed.get_v(2),
                                 P_transformed.get_v(curr_idx+1),
                                 P_transformed.get_v(1)]):
                            print("Caso A22")
                            # Primo passaggio
                            vertices_to_check = [
                                P_transformed.get_v(curr_idx-4),
                                P_transformed.get_v(curr_idx),
                                P_transformed.get_v(curr_idx-2)]
                            if not P_transformed.is_clockwise(
                                    vertices_to_check):
                                angle_1 = (
                                    math.pi +
                                    P_transformed.get_v(curr_idx).angle) / 2
                                angle_2 = P_transformed.get_v(
                                    curr_idx).angle / 2

                                P_transformed.weak_translation_clockwise(
                                    curr_idx-2, angle_2)
                                P_transformed.save_state()

                                P_transformed.\
                                    weak_translation_counterclockwise(
                                        curr_idx-4, angle_1)
                                P_transformed.save_state()

                            vertices_check = [
                                P_transformed.get_v(curr_idx-4),
                                P_transformed.get_v(curr_idx),
                                P_transformed.get_v(curr_idx-2)]
                            if not P_transformed.is_clockwise(
                                    vertices_check) is True:
                                raise ValueError(
                                    "Primo passaggio non riuscito")
                            # Secondo passaggio
                            vertices_to_check_2 = [
                                P_transformed.get_v(curr_idx-4),
                                P_transformed.get_v(curr_idx-1),
                                P_transformed.get_v(curr_idx)]
                            if not P_transformed.is_clockwise(
                                    vertices_to_check_2):
                                angle_3 = (
                                    P_transformed.get_v(
                                        curr_idx-4).angle +
                                    P_transformed.get_v(
                                        curr_idx).angle) / 2

                                P_transformed.weak_translation_clockwise(
                                    curr_idx-1, angle_3)
                                P_transformed.save_state()

                            if not P_transformed.is_clockwise(
                                    [P_transformed.get_v(curr_idx-4),
                                     P_transformed.get_v(curr_idx-1),
                                     P_transformed.get_v(curr_idx)]) is True:
                                raise ValueError(
                                    "Secondo passaggio non riuscito")

                            P_transformed.move_to_midpoint(curr_idx-2)
                            P_transformed.save_state()

                            P_transformed.eliminate_vertex(curr_idx-2)
                            P_transformed.save_state()

                        # Caso A23 (j<1<2<j+1)
                        else:
                            print("Caso A23")
                            if not P_transformed.is_clockwise(
                                    [P_transformed.get_v(curr_idx),
                                     P_transformed.get_v(1),
                                     P_transformed.get_v(2),
                                     P_transformed.get_v(curr_idx+1)]):
                                raise ValueError(
                                    "Controllo per caso A23 non riuscito, "
                                    "dovrebbe essere vero")
                            # Caso A231
                            if P_transformed.is_clockwise(
                                    [P_transformed.get_v(curr_idx),
                                     P_transformed.get_v(1),
                                     P_transformed.get_v(curr_idx+2)]):
                                print("Caso A231")
                                angle = (P_transformed.get_next_clockwise(
                                    1).angle + P_transformed.get_v(1).angle) / 2
                                P_transformed.weak_translation_clockwise(
                                    curr_idx, angle)
                                P_transformed.save_state()

                            # Caso A232
                            else:
                                print("Caso A232")
                                if not P_transformed.is_clockwise(
                                        [P_transformed.get_v(curr_idx),
                                         P_transformed.get_v(curr_idx+2),
                                         P_transformed.get_v(1)]):
                                    raise ValueError(
                                        "Controllo per caso A232 non riuscito,"
                                        "dovrebbe essere falso")
                                # Caso A2321
                                if P_transformed.is_right_turn(curr_idx+2):
                                    P_transformed.move_to_midpoint(curr_idx+1)
                                    P_transformed.save_state()
                                    print("Caso A2321")

                                    P_transformed.eliminate_vertex(curr_idx+1)
                                    P_transformed.save_state()

                                    P_transformed.move_to_midpoint(curr_idx)
                                    P_transformed.save_state()

                                    P_transformed.eliminate_vertex(curr_idx)
                                    P_transformed.save_state()

                                # Caso A2322
                                else:
                                    print("Caso A2322")
                                    angle = (P_transformed.get_v(
                                        curr_idx-2).angle + P_transformed.get_v(1).angle) / 2
                                    P_transformed.weak_translation_counterclockwise(
                                        curr_idx+1, angle)
                                    P_transformed.save_state()
                                    if not P_transformed.is_clockwise(
                                            [P_transformed.get_v(1),
                                             P_transformed.get_v(curr_idx+1),
                                             P_transformed.get_v(curr_idx-2)]):
                                        raise ValueError(
                                            "Passaggio non riuscito")
                                    P_transformed.move_to_midpoint(curr_idx-1)
                                    P_transformed.save_state()

                                    P_transformed.eliminate_vertex(curr_idx-1)
                                    P_transformed.save_state()

                                    # Nella teoria sarebbe j ma la lista si è aggiornata con l'eliminazione di i-1
                                    P_transformed.move_to_midpoint(curr_idx-1)
                                    P_transformed.save_state()

                                    P_transformed.eliminate_vertex(curr_idx-1)
                                    P_transformed.save_state()

                # Caso B
                else:
                    print("Caso B")
                    # Caso B1
                    if P_transformed.is_clockwise([P_transformed.get_v(curr_idx), P_transformed.get_v(2), P_transformed.get_v(curr_idx-2)]):
                        print("Caso B1")
                        # Non facciamo nulla
                        curr_idx += 1
                        continue
                    # Caso B2
                    else:
                        print("Caso B2")
                        if not P_transformed.is_clockwise([P_transformed.get_v(curr_idx), P_transformed.get_v(curr_idx-1), P_transformed.get_v(2)]):
                            raise ValueError(
                                "Controllo per caso B2 non riuscito, dovrebbe essere falso")
                        # Caso B21
                        if P_transformed.is_right_turn(curr_idx):
                            print("Caso B21")
                            if not P_transformed.is_clockwise([P_transformed.get_v(2),
                                                               P_transformed.get_v(
                                                                   curr_idx-3),
                                                               P_transformed.get_v(curr_idx)]):
                                # Traslo i-3 fra j e 2
                                angle = (
                                    2 * math.pi - P_transformed.get_v(curr_idx).angle) / 2

                                P_transformed.weak_translation_counterclockwise(
                                    curr_idx-3, 2 * math.pi - angle)
                                P_transformed.save_state()

                            P_transformed.move_to_midpoint(curr_idx-1)
                            P_transformed.save_state()

                            P_transformed.eliminate_vertex(curr_idx-1)
                            P_transformed.save_state()

                        # Caso B22
                        else:
                            print("Caso B22")
                            # Caso B221
                            print("I vertici sono")
                            for v in P_transformed.vertices:
                                print(f"{v.x} e {v.y}")
                            if P_transformed.is_clockwise([P_transformed.get_v(curr_idx),
                                                           P_transformed.get_v(curr_idx+1), P_transformed.get_v(1)]):
                                print("Caso B221")
                                # Caso B2211
                                if P_transformed.is_clockwise([P_transformed.get_v(curr_idx),
                                                               P_transformed.get_v(curr_idx+2), P_transformed.get_v(2)]):
                                    print("Caso B2211")
                                    if not P_transformed.is_clockwise([P_transformed.get_v(curr_idx-2),
                                                                       P_transformed.get_v(curr_idx), P_transformed.get_v(2)]):
                                        angle = P_transformed.get_next_counterclockwise(
                                            2).angle / 2
                                        print(
                                            f"{P_transformed.get_next_counterclockwise(2).angle}")
                                        P_transformed.weak_translation_counterclockwise(
                                            curr_idx, angle)
                                        P_transformed.save_state()
                                        print(
                                            f"{P_transformed.get_v(5).angle}")
                                        if not P_transformed.is_clockwise([P_transformed.get_v(curr_idx-2),
                                                                           P_transformed.get_v(curr_idx), P_transformed.get_v(2)]):
                                            raise ValueError(
                                                "Controllo dopo traslazione non riuscito, dovrebbe essere vero")

                                # Caso B2212
                                else:
                                    print("Caso B2212")
                                    if not P_transformed.is_clockwise([P_transformed.get_v(2),
                                                                       P_transformed.get_v(curr_idx+2), P_transformed.get_v(curr_idx)]):
                                        raise ValueError(
                                            "Non entra in nessun caso")
                                    # Caso B22121
                                    if P_transformed.is_left_turn(curr_idx+2):
                                        print("Caso B22121")
                                        P_transformed.move_to_midpoint(
                                            curr_idx+1)
                                        P_transformed.save_state()

                                        P_transformed.eliminate_vertex(
                                            curr_idx+1)
                                        P_transformed.save_state()

                                        P_transformed.move_to_midpoint(
                                            curr_idx)
                                        P_transformed.save_state()

                                        P_transformed.eliminate_vertex(
                                            curr_idx)
                                        P_transformed.save_state()

                                    # Caso B22122
                                    else:
                                        print("Caso B22122")
                                        if not P_transformed.is_clockwise([P_transformed.get_v(curr_idx-3),
                                                                           P_transformed.get_v(curr_idx), P_transformed.get_v(curr_idx-1)]):
                                            # Traslo i-3 in un intorno di 2
                                            angle = (
                                                2 * math.pi - P_transformed.get_next_clockwise(2).angle) / 2
                                            P_transformed.weak_translation_counterclockwise(
                                                curr_idx-3, 2 * math.pi - angle)
                                            P_transformed.save_state()
                                        if not P_transformed.is_clockwise([P_transformed.get_v(curr_idx-3),
                                                                           P_transformed.get_v(curr_idx), P_transformed.get_v(curr_idx-1)]):
                                            raise ValueError(
                                                "Controllo dopo traslazione non riuscito, dovrebbe essere vero")

                                        if not P_transformed.is_clockwise([P_transformed.get_v(curr_idx-2),
                                                                           P_transformed.get_v(curr_idx+1), P_transformed.get_v(2)]):
                                            # Traslo j+1
                                            angle = (
                                                P_transformed.get_next_counterclockwise(2).angle) / 2
                                            P_transformed.weak_translation_clockwise(
                                                curr_idx+1, angle)
                                            P_transformed.save_state()
                                        if not P_transformed.is_clockwise([P_transformed.get_v(curr_idx-2),
                                                                           P_transformed.get_v(curr_idx+1), P_transformed.get_v(2)]):
                                            raise ValueError(
                                                "Controllo dopo traslazione non riuscito, dovrebbe essere vero")
                                        P_transformed.move_to_midpoint(
                                            curr_idx-1)
                                        P_transformed.save_state()

                                        P_transformed.eliminate_vertex(
                                            curr_idx-1)
                                        P_transformed.save_state()

                            # caso B222
                            else:
                                print("Caso B222")
                                if not P_transformed.is_clockwise([P_transformed.get_v(1),
                                                                   P_transformed.get_v(curr_idx+1), P_transformed.get_v(curr_idx)]):
                                    raise ValueError(
                                        "Non entra in nessun caso")
                                # Passaggio 1
                                if not P_transformed.is_clockwise([P_transformed.get_v(curr_idx-2),
                                                                   P_transformed.get_v(curr_idx+1), P_transformed.get_v(curr_idx)]):
                                    angle = (
                                        math.pi + P_transformed.get_v(curr_idx+1).angle) / 2
                                    P_transformed.weak_translation_counterclockwise(
                                        curr_idx-2, angle)
                                    P_transformed.save_state()
                                if not P_transformed.is_clockwise([P_transformed.get_v(curr_idx-2),
                                                                   P_transformed.get_v(curr_idx+1), P_transformed.get_v(curr_idx)]):
                                    raise ValueError(
                                        "Controllo dopo traslazione non riuscito, dovrebbe essere vero")
                                # Passaggio 2
                                if not P_transformed.is_clockwise([P_transformed.get_v(curr_idx-3),
                                                                   P_transformed.get_v(curr_idx), P_transformed.get_v(curr_idx-1)]):
                                    angle = (
                                        2 * math.pi + P_transformed.get_v(curr_idx).angle) / 2
                                    P_transformed.weak_translation_counterclockwise(
                                        curr_idx-3, angle)
                                    P_transformed.save_state()
                                    if not P_transformed.is_clockwise([P_transformed.get_v(curr_idx-3),
                                                                       P_transformed.get_v(curr_idx), P_transformed.get_v(curr_idx-1)]):
                                        raise ValueError(
                                            "Controllo dopo traslazione non riuscito, dovrebbe essere vero")
                                P_transformed.move_to_midpoint(
                                    curr_idx-1)
                                P_transformed.save_state()

                                P_transformed.eliminate_vertex(
                                    curr_idx-1)
                                P_transformed.save_state()

            # ==========================================
            # INIZIO DEL BLOCCO PARI (SPECCHIO)
            # ==========================================
            elif curr_idx % 2 == 0:
                # Caso C (Speculare di A)
                if P_transformed.is_right_turn(curr_idx-1):
                    print("Caso C")
                    # Caso C1
                    if P_transformed.is_left_turn(curr_idx):
                        print("Caso C1")
                        P_transformed.move_to_midpoint(curr_idx-1)
                        P_transformed.save_state()

                        P_transformed.eliminate_vertex(curr_idx-1)
                        P_transformed.save_state()

                    # Caso C2
                    else:
                        print("Caso C2")
                        # Caso C21
                        if P_transformed.is_clockwise(
                                [P_transformed.get_v(curr_idx),
                                 P_transformed.get_v(curr_idx+1),
                                 P_transformed.get_v(1)]):
                            print("Caso C21")

                            # Caso C211
                            if P_transformed.is_clockwise(
                                    [P_transformed.get_v(curr_idx),
                                     P_transformed.get_v(curr_idx+1),
                                     P_transformed.get_v(curr_idx-2)]):
                                print("Caso C211")

                                P_transformed.move_to_midpoint(curr_idx-1)
                                P_transformed.save_state()

                                P_transformed.eliminate_vertex(curr_idx-1)
                                P_transformed.save_state()

                            # Caso C212
                            else:
                                print("Caso C212")
                                angle = (P_transformed.get_v(
                                    curr_idx+1).angle + math.pi) / 2
                                P_transformed.\
                                    weak_translation_clockwise(
                                        curr_idx-2, angle)
                                P_transformed.save_state()

                                P_transformed.move_to_midpoint(curr_idx-1)
                                P_transformed.save_state()

                                P_transformed.eliminate_vertex(curr_idx-1)
                                P_transformed.save_state()

                        # Caso C22
                        if P_transformed.is_clockwise(
                                [P_transformed.get_v(curr_idx),
                                 P_transformed.get_v(1),
                                 P_transformed.get_v(curr_idx+1),
                                 P_transformed.get_v(2)]):
                            print("Caso C22")
                            # Primo passaggio
                            vertices_to_check = [
                                P_transformed.get_v(curr_idx-4),
                                P_transformed.get_v(curr_idx),
                                P_transformed.get_v(curr_idx-2)]
                            if not P_transformed.is_clockwise(
                                    vertices_to_check):
                                angle_1 = (
                                    2 * math.pi +
                                    P_transformed.get_v(curr_idx).angle) / 2
                                angle_2 = (
                                    math.pi + P_transformed.get_v(curr_idx).angle) / 2

                                P_transformed.\
                                    weak_translation_counterclockwise(
                                        curr_idx-4, angle_1)
                                P_transformed.save_state()

                                P_transformed.weak_translation_clockwise(
                                    curr_idx-2, angle_2)
                                P_transformed.save_state()

                            vertices_check = [
                                P_transformed.get_v(curr_idx-4),
                                P_transformed.get_v(curr_idx),
                                P_transformed.get_v(curr_idx-2)]
                            if not P_transformed.is_clockwise(
                                    vertices_check) is True:
                                raise ValueError(
                                    "Primo passaggio non riuscito")
                            # Secondo passaggio
                            vertices_to_check_2 = [
                                P_transformed.get_v(curr_idx-4),
                                P_transformed.get_v(curr_idx-1),
                                P_transformed.get_v(curr_idx)]
                            if not P_transformed.is_clockwise(
                                    vertices_to_check_2):
                                angle_3 = (
                                    P_transformed.get_v(
                                        curr_idx-4).angle +
                                    P_transformed.get_v(
                                        curr_idx).angle) / 2

                                P_transformed.weak_translation_clockwise(
                                    curr_idx-1, angle_3)
                                P_transformed.save_state()

                            if not P_transformed.is_clockwise(
                                    [P_transformed.get_v(curr_idx-4),
                                     P_transformed.get_v(curr_idx-1),
                                     P_transformed.get_v(curr_idx)]) is True:
                                raise ValueError(
                                    "Secondo passaggio non riuscito")

                            P_transformed.move_to_midpoint(curr_idx-2)
                            P_transformed.save_state()

                            P_transformed.eliminate_vertex(curr_idx-2)
                            P_transformed.save_state()

                        # Caso C23 (j<2<1<j+1)
                        else:
                            print("Caso C23")
                            if not P_transformed.is_clockwise(
                                    [P_transformed.get_v(curr_idx),
                                     P_transformed.get_v(2),
                                     P_transformed.get_v(1),
                                     P_transformed.get_v(curr_idx+1)]):
                                raise ValueError(
                                    "Controllo per caso C23 non riuscito, "
                                    "dovrebbe essere vero")
                            # Caso C231
                            if P_transformed.is_clockwise(
                                    [P_transformed.get_v(curr_idx),
                                     P_transformed.get_v(1),
                                     P_transformed.get_v(curr_idx+2)]):
                                print("Caso C231")
                                angle = (P_transformed.get_next_clockwise(
                                    2).angle + P_transformed.get_v(2).angle) / 2
                                P_transformed.weak_translation_clockwise(
                                    curr_idx, angle)
                                P_transformed.save_state()

                            # Caso C232
                            else:
                                print("Caso C232")
                                if not P_transformed.is_clockwise(
                                        [P_transformed.get_v(curr_idx),
                                         P_transformed.get_v(curr_idx+2),
                                         P_transformed.get_v(2)]):
                                    raise ValueError(
                                        "Controllo per caso C232 non riuscito,"
                                        "dovrebbe essere falso")
                                # Caso C2321
                                if P_transformed.is_right_turn(curr_idx+2):
                                    print("Caso C2321")
                                    P_transformed.move_to_midpoint(curr_idx+1)
                                    P_transformed.save_state()

                                    P_transformed.eliminate_vertex(curr_idx+1)
                                    P_transformed.save_state()

                                    P_transformed.move_to_midpoint(curr_idx)
                                    P_transformed.save_state()

                                    P_transformed.eliminate_vertex(curr_idx)
                                    P_transformed.save_state()
                                # Caso C2322
                                else:
                                    print("Caso c2322")
                                    angle = (P_transformed.get_v(
                                        curr_idx-2).angle + P_transformed.get_v(2).angle) / 2
                                    P_transformed.weak_translation_counterclockwise(
                                        curr_idx+1, angle)
                                    P_transformed.save_state()
                                    if not P_transformed.is_clockwise(
                                            [P_transformed.get_v(2),
                                             P_transformed.get_v(curr_idx+1),
                                             P_transformed.get_v(curr_idx-2)]):
                                        raise ValueError(
                                            "Passaggio non riuscito")
                                    P_transformed.move_to_midpoint(curr_idx-1)
                                    P_transformed.save_state()

                                    P_transformed.eliminate_vertex(curr_idx-1)
                                    P_transformed.save_state()

                                    # Nella teoria sarebbe j ma la lista si è aggiornata con l'eliminazione di i-1
                                    P_transformed.move_to_midpoint(curr_idx-1)
                                    P_transformed.save_state()

                                    P_transformed.eliminate_vertex(curr_idx-1)
                                    P_transformed.save_state()

                # Caso D
                else:
                    print("Caso D")
                    # Caso D1
                    if P_transformed.is_clockwise([P_transformed.get_v(curr_idx), P_transformed.get_v(1), P_transformed.get_v(curr_idx-2)]):
                        print("Caso D1")
                        # Non facciamo nulla
                        curr_idx += 1
                        continue
                    # Caso D2
                    else:
                        print("Caso D2")
                        if not P_transformed.is_clockwise([P_transformed.get_v(curr_idx), P_transformed.get_v(curr_idx-1), P_transformed.get_v(1)]):
                            raise ValueError(
                                "Controllo per caso B2 non riuscito, dovrebbe essere falso")
                        # Caso D21
                        if P_transformed.is_right_turn(curr_idx):
                            print("Caso D21")
                            if not P_transformed.is_clockwise([P_transformed.get_v(1),
                                                               P_transformed.get_v(
                                                                   curr_idx-3),
                                                               P_transformed.get_v(curr_idx)]):
                                # Traslo i-3 fra j e 1
                                angle = (
                                    P_transformed.get_v(1).angle + P_transformed.get_v(curr_idx).angle) / 2

                                P_transformed.weak_translation_counterclockwise(
                                    curr_idx-3, angle)
                                P_transformed.save_state()

                            P_transformed.move_to_midpoint(curr_idx-1)
                            P_transformed.save_state()

                            P_transformed.eliminate_vertex(curr_idx-1)
                            P_transformed.save_state()

                        # Caso D22
                        else:
                            print("Caso D22")
                            # Caso D221
                            if P_transformed.is_clockwise([P_transformed.get_v(curr_idx),
                                                           P_transformed.get_v(curr_idx+1), P_transformed.get_v(2)]):
                                print("Caso D221")
                                # Caso D2211
                                if P_transformed.is_clockwise([P_transformed.get_v(curr_idx),
                                                               P_transformed.get_v(curr_idx+2), P_transformed.get_v(1)]):
                                    print("Caso D2211")
                                    if not P_transformed.is_clockwise([P_transformed.get_v(curr_idx-2),
                                                                       P_transformed.get_v(curr_idx), P_transformed.get_v(2)]):
                                        angle = (P_transformed.get_next_counterclockwise(
                                            1).angle + P_transformed.get_v(1).angle) / 2
                                        print(f"L'angolo è {angle}")
                                        P_transformed.weak_translation_counterclockwise(
                                            curr_idx, angle)
                                        P_transformed.save_state()
                                        if not P_transformed.is_clockwise([P_transformed.get_v(curr_idx-2),
                                                                           P_transformed.get_v(curr_idx), P_transformed.get_v(2)]):
                                            raise ValueError(
                                                "Controllo dopo traslazione non riuscito, dovrebbe essere vero")

                                # Caso D2212
                                else:
                                    print("Caso D2212")
                                    if not P_transformed.is_clockwise([P_transformed.get_v(1),
                                                                       P_transformed.get_v(curr_idx+2), P_transformed.get_v(curr_idx)]):
                                        raise ValueError(
                                            "Non entra in nessun caso")
                                    # Caso D22121
                                    if P_transformed.is_left_turn(curr_idx+2):
                                        print("Caso D22121")
                                        P_transformed.move_to_midpoint(
                                            curr_idx+1)
                                        P_transformed.save_state()

                                        P_transformed.eliminate_vertex(
                                            curr_idx+1)
                                        P_transformed.save_state()

                                        P_transformed.move_to_midpoint(
                                            curr_idx)
                                        P_transformed.save_state()

                                        P_transformed.eliminate_vertex(
                                            curr_idx)
                                        P_transformed.save_state()

                                    # Caso D22122
                                    else:
                                        print("Caso D22122")
                                        if not P_transformed.is_clockwise([P_transformed.get_v(curr_idx-3),
                                                                           P_transformed.get_v(curr_idx), P_transformed.get_v(curr_idx-1)]):
                                            # Traslo i-3 in un intorno di 1
                                            angle = (
                                                P_transformed.get_v(1).angle + P_transformed.get_next_clockwise(1).angle) / 2
                                            P_transformed.weak_translation_counterclockwise(
                                                curr_idx-3, angle)
                                            P_transformed.save_state()
                                        if not P_transformed.is_clockwise([P_transformed.get_v(curr_idx-3),
                                                                           P_transformed.get_v(curr_idx), P_transformed.get_v(curr_idx-1)]):
                                            raise ValueError(
                                                "Controllo dopo traslazione non riuscito, dovrebbe essere vero")

                                        if not P_transformed.is_clockwise([P_transformed.get_v(curr_idx-2),
                                                                           P_transformed.get_v(curr_idx+1), P_transformed.get_v(1)]):
                                            # Traslo j+1
                                            angle = (
                                                P_transformed.get_next_counterclockwise(1).angle + P_transformed.get_v(1).angle) / 2
                                            P_transformed.weak_translation_clockwise(
                                                curr_idx+1, angle)
                                            P_transformed.save_state()
                                        if not P_transformed.is_clockwise([P_transformed.get_v(curr_idx-2),
                                                                           P_transformed.get_v(curr_idx+1), P_transformed.get_v(1)]):
                                            raise ValueError(
                                                "Controllo dopo traslazione non riuscito, dovrebbe essere vero")
                                        P_transformed.move_to_midpoint(
                                            curr_idx-1)
                                        P_transformed.save_state()

                                        P_transformed.eliminate_vertex(
                                            curr_idx-1)
                                        P_transformed.save_state()

                            # caso D222
                            else:
                                print("Caso D222")
                                if not P_transformed.is_clockwise([P_transformed.get_v(2),
                                                                   P_transformed.get_v(curr_idx+1), P_transformed.get_v(curr_idx)]):
                                    raise ValueError(
                                        "Non entra in nessun caso")
                                # Passaggio 1
                                if not P_transformed.is_clockwise([P_transformed.get_v(curr_idx-2),
                                                                   P_transformed.get_v(curr_idx+1), P_transformed.get_v(curr_idx)]):
                                    angle = (
                                        P_transformed.get_next_counterclockwise(2).angle + P_transformed.get_v(2).angle) / 2
                                    P_transformed.weak_translation_counterclockwise(
                                        curr_idx-2, angle)
                                    P_transformed.save_state()
                                if not P_transformed.is_clockwise([P_transformed.get_v(curr_idx-2),
                                                                   P_transformed.get_v(curr_idx+1), P_transformed.get_v(curr_idx)]):
                                    raise ValueError(
                                        "Controllo dopo traslazione non riuscito, dovrebbe essere vero")
                                # Passaggio 2
                                if not P_transformed.is_clockwise([P_transformed.get_v(curr_idx-3),
                                                                   P_transformed.get_v(curr_idx), P_transformed.get_v(curr_idx-1)]):
                                    angle = (
                                        P_transformed.get_v(1).angle + P_transformed.get_v(curr_idx).angle) / 2
                                    P_transformed.weak_translation_counterclockwise(
                                        curr_idx-3, angle)
                                    P_transformed.save_state()
                                    if not P_transformed.is_clockwise([P_transformed.get_v(curr_idx-3),
                                                                       P_transformed.get_v(curr_idx), P_transformed.get_v(curr_idx-1)]):
                                        raise ValueError(
                                            "Controllo dopo traslazione non riuscito, dovrebbe essere vero")
                                P_transformed.move_to_midpoint(
                                    curr_idx-1)
                                P_transformed.save_state()

                                P_transformed.eliminate_vertex(
                                    curr_idx-1)
                                P_transformed.save_state()
            curr_idx = 4

# FINE DELL'ALGORITMO - INIZIO GRAFICA

print("\nAlgoritmo completato con successo!")

# Creiamo il visualizzatore passandogli tutta la storia
# del poligono
vis = PolygonVisualizer(P_transformed.history)

# Avviamo l'animazione
vis.show(interval=1000)
