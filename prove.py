from poligonali_stellate import (
    is_near,
    generate_random_polygonal,
)

# CONTROLLO 1000 POLIGONI CASUALI CON I VERTICI NON SOVRAPPOSTI
for i in range(1, 1000):
    P = generate_random_polygonal(10)
    while True:
        P = generate_random_polygonal(10)
        # Controlliamo tutte le possibili coppie di vertici
        for i in range(10):
            for j in range(i + 1, 10):
                v1 = P.get_v(i)
                v2 = P.get_v(j)

                # Se la distanza tra le X è minore della tolleranza
                # E anche la distanza tra le Y è minore della tolleranza, sono troppo vicini
                sovrapposition = is_near(v1.x, v2.x) and is_near(v1.y, v2.y)
                if sovrapposition is True:
                    break
            if sovrapposition is True:
                break
        if sovrapposition:
            P = generate_random_polygonal(10)
            continue
        else:
            break
    P.print_vertices()
    P.reduce_polygonal()
    print("Ho ridotto 1000 curve poligonali con successo!")
