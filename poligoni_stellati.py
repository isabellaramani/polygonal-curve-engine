import math


class Vertex:
    def __init__(self, name: str, x: float, y: float) -> None:
        """
        Inizializza un vertice con nome, coordinate (x, y)
        e calcola l'angolo rispetto all'origine.
        """
        self.name = name  # Es: "v1", "v2"
        self.x = float(x)
        self.y = float(y)
        # atan2 restituisce l'angolo fra -pi e pi
        self.angle = math.atan2(self.y, self.x)

    def change_coordinates(self, x: float, y: float) -> None:
        """
        Sposta il vertice a nuove coordinate (x, y)
        e ricalcola l'angolo.
        """
        self.x = x
        self.y = y
        self.angle = math.atan2(y, x)

    def change_angle(self, new_angle: float) -> None:
        """
        Sposta il vertice sulla circonferenza unitaria (R=1)
        in base al nuovo angolo fornito.
        """
        self.angle = new_angle
        self.x = math.cos(new_angle)
        self.y = math.sin(new_angle)


def get_determinant(
    V1: 'Vertex',
    V2: 'Vertex',
    V3: 'Vertex',
    V4: 'Vertex'
) -> float:
    """
    Calcola il determinante dei vettori V1-V2 e V3-V4.
     """
    return ((V1.x - V2.x) * (V3.y - V4.y) -
            (V1.y - V2.y) * (V3.x - V4.x))


origine = Vertex("Origine", 0, 0)


class Polygon:
    def __init__(self, vertices: list[Vertex] = None) -> None:
        """
        Inizializza un poligono come una lista di vertici.
        """
        # Se non viene fornita una lista di vertici
        # inizializza un poligono vuoto.
        if vertices is None:
            self.vertices = []
        else:
            self.vertices = vertices

    def add_vertex(self, V: Vertex) -> None:
        """
        Aggiunge un vertice al poligono.
        """
        self.vertices.append(V)

    def get_v_i(self, i: int) -> Vertex:
        """
        Restituisce il vertice v_i, con i che parte da 1.
        """
        n = len(self.vertices)
        # Gestisce il caso poligono vuoto.
        if n == 0:
            return None
        return self.vertices[(i-1) % n]

    def get_rotation_angle(self, i: int) -> float:
        """
        Calcola l'angolo di rotazione di v_i.
        """
        V_i = self.get_v_i(i)
        V_ip1 = self.get_v_i(i+1)
        V_im1 = self.get_v_i(i-1)

        # Calcolo dei vettori v_im1->v_i e v_i->v_ip1.
        vec1_x = V_i.x - V_im1.x
        vec1_y = V_i.y - V_im1.y
        vec2_x = V_ip1.x - V_i.x
        vec2_y = V_ip1.y - V_i.y

        # Calcolo prodotto scalare.
        dot_product = vec1_x * vec2_x + vec1_y * vec2_y
        norm_1 = math.sqrt(vec1_x**2 + vec1_y**2)
        norm_2 = math.sqrt(vec2_x**2 + vec2_y**2)

        abs_value_rot_vi = math.acos(dot_product / (norm_1 * norm_2))
        det = vec2_x * vec1_y - vec2_y * vec1_x
        rot_vi = math.copysign(abs_value_rot_vi, det)
        return rot_vi

    def get_winding_number(self) -> int:
        """
        Calcola l'indice di avvolgimento del poligono.
        """
        sum_rotation_angles = 0
        # Calcola la somma degli angoli di rotazione
        # per tutti i vertici del poligono.
        for j in range(1, len(self.vertices)+1):
            rot_vj = self.get_rotation_angle(j)
            sum_rotation_angles = sum_rotation_angles + rot_vj
        winding_number = sum_rotation_angles / (2 * math.pi)
        return round(winding_number)

    def is_left_turn(self, i: int) -> bool:
        """
        Verifica se in v_i svolta a sinistra.
        """
        if self.get_rotation_angle(i) > 0:
            return True
        else:
            return False

    def center_polygon(self):
        """
        Centra il poligono spostando tutti i vertici
        in modo che il centro di massa sia nell'origine (0, 0).
        """
        n = len(self.vertices)
        if n == 0:
            return  # Gestione caso poligono vuoto

        # Calcola il centro di massa
        center_x = sum(v.x for v in self.vertices) / n
        center_y = sum(v.y for v in self.vertices) / n

        # Sposta ogni vertice in modo che il centro di massa sia all'origine
        for v in self.vertices:
            v.change_coordinates(v.x - center_x, v.y - center_y)

    # Funzionale solo se i vertici apartengono ad una circonferenza

    def is_clockwise(self, list_vertices: list[Vertex]) -> bool:
        """
        Verifica se i vertici sulla circonferenza unitaria
        sono ordinati in senso orario.
        """
        n = len(list_vertices)
        if n <= 2:
            return True

        # Prendo l'angolo del primo vertice come riferimento
        base_angle = list_vertices[0].angle

        for j in range(1, n-1):
            current_angle = list_vertices[j].angle
            # Calcolo la differenza angolare rispetto all'angolo di riferimento
            # Sarà crescente in senso antiorario
            current_angle_normalised = (
                current_angle - base_angle) % (2 * math.pi)
            next_angle = list_vertices[(j + 1) % n].angle
            next_angle_normalised = (next_angle - base_angle) % (2 * math.pi)

            # Calcoliamo la differenza fra angoli compresi fra [0, 2pi]
            diff = (next_angle_normalised - current_angle_normalised)

            # Se diff è positiva percorrendo la circonferenza
            # a partire dal vertice base i due sono in senso antiorario
            if diff > 0:
                return False

        return True


# Poligono di prova
Poligono1 = Polygon((Vertex("v1", 1, 0), Vertex(
    "v2", 0, 1), Vertex("v3", -1, 0), Vertex("v4", 0, -1)))
