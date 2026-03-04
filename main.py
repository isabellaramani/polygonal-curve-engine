import math
from poligoni_stellati import Vertex, Polygon, is_near

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

if not P.is_circle():
    raise ValueError("La curva poligonale non è inscritta in un cerchio.")

# Porto la curva poliginale su circonferenza di raggio 1
P.get_unitary_radius()

# Porto il vertice v1 in (-1,0)
if not is_near(P.get_v(1).x, 1) or not is_near(P.get_v(1).y, 0):
    if P.get_v(1).angle < math.pi:
        P.weak_translation_counterclockwise(math.pi)
    else:
        P.weak_translation_clockwise(math.pi)

# Porto il vertice v2 in (1,0)
if not is_near(P.get_v(2).x, 1) or not is_near(P.get_v(2).y, 0):
    if P.get_v(2).angle < math.pi:
        P.weak_translation_clockwise(math.pi)
    else:
        P.weak_translation_counterclockwise(math.pi)

# Equidistanzio i vertici:
P.get_equispaced_vertices()

# Elimino i vertici appartenenti ai lati
for i in range(3, n+1):
    if is_near(P.get_rotation_angle(i), 0):
        P.eliminate_vertex(i)


# Algoritmo

P_transformed = Polygon(list(P.vertices))

if n == 2:
    print("Il poligono stellato è un triangolo.")
else:
    # Caso in cui la poligonale sarà sinistrorsa
    if P_transformed.is_left_turn(2):
        # Ciclo sui vertici da 4 a n
        for i in range(4, n+1):
            # Caso in cui i è dispari
            if i % 2 == 1:
                # Caso A
                if P_transformed.is_right_turn(i-1):
                    # Caso A1
                    if P_transformed.is_left_turn(i):
                        P_transformed.move_and_eliminate(i-1)
                    # Caso A2
                    if P_transformed.is_right_turn(i):
                        # Caso A21
                        if P_transformed.is_clockwise(
                                [P_transformed.get_v(i),
                                 P_transformed.get_v(i+1),
                                 P_transformed.get_v(2)]):
                            if P_transformed.is_clockwise(
                                    [P_transformed.get_v(i),
                                     P_transformed.get_v(i+1),
                                     P_transformed.get_v(i-2)]):
                                P_transformed.move_and_eliminate(i-2)
                            else:
                                angle = (
                                    P_transformed.get_v(i-2).angle +
                                    math.pi / 1000)
                                P_transformed.\
                                    weak_translation_counterclockwise(
                                        angle)
                                P_transformed.move_and_eliminate(i-2)
