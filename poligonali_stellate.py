import math
import copy
import random

TOLERANCE = 0.0005


def is_near(a, b):
    return math.fabs(a - b) < TOLERANCE


class Vertex:
    def __init__(self, name: str, x: float, y: float) -> None:
        """Inizializza un vertice con nome, coordinate (x, y)
        e calcola l'angolo rispetto all'origine.
        """
        self.name = name  # Es: "v1", "v2"
        self.x = float(x)
        self.y = float(y)
        # atan2 restituisce l'angolo fra 0 e 2*pi
        self.angle = math.atan2(self.y, self.x) % (2 * math.pi)

    def change_coordinates(self, x: float, y: float) -> None:
        """Sposta il vertice a nuove coordinate (x, y)
        e ricalcola l'angolo.
        """
        self.x = x
        self.y = y
        self.angle = math.atan2(y, x) % (2 * math.pi)

    def change_angle(self, new_angle: float) -> None:
        """Sposta il vertice sulla circonferenza unitaria (R=1)
        in base al nuovo angolo fornito.
        """
        self.angle = new_angle
        self.x = math.cos(new_angle)
        self.y = math.sin(new_angle)


class Polygonal:
    def __init__(self, vertices: list[Vertex] = None) -> None:
        """Inizializza una poligonale come una lista di vertici.
        Se non viene fornita una lista di vertici
        inizializza una poligonale vuoto.
        """
        if vertices is None:
            self.vertices = []
        else:
            self.vertices = vertices
        self.history = [vertices]

    def save_state(self) -> None:
        """Salva lo stato attuale della poligonale nella cronologia."""
        self.history.append(copy.deepcopy(self.vertices))

    def is_empty(self) -> bool:
        """Verifica se la poligonale è vuota."""
        return len(self.vertices) == 0

    def print_vertices(self) -> None:
        """Stampa nome e coordinate dei vertici della poligonale."""
        for vertex in self.vertices:
            print(f"{vertex.name}: ({vertex.x}, {vertex.y})")

    def get_v(self, i: int) -> Vertex:
        """Restituisce il vertice v_i, con i che parte da 1."""
        n = len(self.vertices)
        # Gestisce il caso poligonale vuota.
        if n == 0:
            return None
        return self.vertices[(i - 1) % n]

    def add_vertex(self, V: Vertex) -> None:
        """Aggiunge un vertice alla poligonale."""
        self.vertices.append(V)

    def eliminate_vertex(self, i: int) -> None:
        """Elimina il vertice i-esimo se appartiene
        al segmento [v_im1,vip1]."""
        v_im1 = self.get_v(i - 1)
        v_i = self.get_v(i)
        v_ip1 = self.get_v(i + 1)
        # Controllo se i vettori sono allineati con il determinante
        det = (v_im1.x - v_i.x) * (v_ip1.y - v_i.y) - (v_im1.y - v_i.y) * (
            v_ip1.x - v_i.x
        )
        # Controllo se il punto è interno al segmento
        is_between_x = min(v_im1.x, v_ip1.x) <= v_i.x <= max(v_im1.x, v_ip1.x)
        is_between_y = min(v_im1.y, v_ip1.y) <= v_i.y <= max(v_im1.y, v_ip1.y)
        print(f"Ho eliminato il vertice {self.get_v(i).name}")
        if is_near(det, 0.0) and is_between_x and is_between_y:
            self.vertices.remove(v_i)
        else:
            raise ValueError("Il vertice non appartiene al segmento.")
        self.save_state()

    def get_rotation_angle(self, i: int) -> float:
        """Calcola l'angolo di rotazione di v_i."""
        v_i = self.get_v(i)
        v_ip1 = self.get_v(i + 1)
        v_im1 = self.get_v(i - 1)
        # Calcolo dei vettori v_im1->v_i e v_i->v_ip1.
        vec1_x = v_i.x - v_im1.x
        vec1_y = v_i.y - v_im1.y
        vec2_x = v_ip1.x - v_i.x
        vec2_y = v_ip1.y - v_i.y
        # Calcolo prodotto scalare e norme.
        dot_product = vec1_x * vec2_x + vec1_y * vec2_y
        norm_1 = math.sqrt(vec1_x**2 + vec1_y**2)
        norm_2 = math.sqrt(vec2_x**2 + vec2_y**2)
        # Se due vertici sono identici, la norma è 0.
        if norm_1 == 0.0 or norm_2 == 0.0:
            return 0.0
        # Calcolo il valore del coseno
        cos_val = dot_product / (norm_1 * norm_2)
        # Gestisco errori di approssimazione
        cos_val = max(-1.0, min(1.0, cos_val))
        abs_value_rot_vi = math.acos(cos_val)
        det = vec1_x * vec2_y - vec1_y * vec2_x
        rot_vi = math.copysign(abs_value_rot_vi, det)
        return rot_vi

    def get_winding_number(self) -> int:
        """Calcola l'indice di avvolgimento della poligonale."""
        sum_rotation_angles = 0
        # Calcola la somma degli angoli di rotazione
        # per tutti i vertici della poligonale.
        for j in range(1, len(self.vertices) + 1):
            rot_vj = self.get_rotation_angle(j)
            sum_rotation_angles = sum_rotation_angles + rot_vj
        winding_number = sum_rotation_angles / (2 * math.pi)
        return round(winding_number)

    def is_left_turn(self, i: int) -> bool:
        """Verifica se in v_i svolta a sinistra."""
        if self.get_rotation_angle(i) > 0:
            return True
        return False

    def is_right_turn(self, i: int) -> bool:
        """Verifica se in v_i svolta a destra."""
        if self.get_rotation_angle(i) < 0:
            return True
        return False

    def center_polygonal(self) -> None:
        """Centra la poligonale spostando tutti i vertici
        in modo che il centro di massa sia nell'origine (0, 0).
        """
        n = len(self.vertices)
        if n == 0:
            return None
        # Calcola il centro di massa
        center_x = sum(v.x for v in self.vertices) / n
        center_y = sum(v.y for v in self.vertices) / n
        # Sposta ogni vertice in modo che il centro di massa sia all'origine
        for v in self.vertices:
            v.change_coordinates(v.x - center_x, v.y - center_y)
        self.save_state()

    def is_circle(self) -> bool:
        """Verifica se i vertici della poligonale appartengono
        ad una circonferenza."""
        n = len(self.vertices)
        if n < 3:
            return False  # Almeno 3 punti per definire una circonferenza
        # Caso circonferenza unitaria per non avere errori con vertici vicini
        if all(is_near(v.x**2 + v.y**2, 1.0) for v in self.vertices):
            return True
        # Calcola circocentro e raggio usando i primi 3 vertici
        V1, V2, V3 = self.vertices[0], self.vertices[1], self.vertices[2]

        def calculate_circumcenter(V1: Vertex, V2: Vertex, V3: Vertex) -> Vertex:
            """Calcola il circocentro dei tre vertici V1, V2, V3."""
            # Calcola i punti medi dei segmenti V1-V2 e V2-V3
            M_12 = Vertex("Midpoint12", (V1.x + V2.x) / 2, (V1.y + V2.y) / 2)
            M_23 = Vertex("Midpoint23", (V2.x + V3.x) / 2, (V2.y + V3.y) / 2)
            # Calcola coefficiente delle rette perpendicolari a V1-V2 e V2-V3
            if is_near(V1.x, V2.x):
                # Il segmento è verticale, la perpendicolare è orizzontale
                m_perp_12 = 0.0
            elif is_near(V1.y, V2.y):
                # Il segmento è orizzontale, la perpendicolare è verticale
                m_perp_12 = float("inf")
            else:
                # Caso normale
                m_12 = (V1.y - V2.y) / (V1.x - V2.x)
                m_perp_12 = -1 / m_12
            if is_near(V2.x, V3.x):
                m_perp_23 = 0.0
            elif is_near(V2.y, V3.y):
                m_perp_23 = float("inf")
            else:
                m_23 = (V2.y - V3.y) / (V2.x - V3.x)
                m_perp_23 = -1 / m_23
            # Intersezione delle due rette perpendicolari
            if m_perp_12 == float("inf"):
                x = M_12.x
                y = m_perp_23 * (x - M_23.x) + M_23.y
            elif m_perp_23 == float("inf"):
                x = M_23.x
                y = m_perp_12 * (x - M_12.x) + M_12.y
            else:
                A = [[-m_perp_12, 1], [-m_perp_23, 1]]
                b = [M_12.y - m_perp_12 * M_12.x, M_23.y - m_perp_23 * M_23.x]
                # Risolvo il sistema lineare Ax = b
                det_A = A[0][0] * A[1][1] - A[0][1] * A[1][0]
                if det_A == 0:
                    return None  # Le rette sono parallele
                x = (b[0] * A[1][1] - b[1] * A[0][1]) / det_A
                y = (A[0][0] * b[1] - A[1][0] * b[0]) / det_A
            return Vertex("Circumcenter", x, y)

        center = calculate_circumcenter(V1, V2, V3)
        radius = math.sqrt((V1.x - center.x) ** 2 + (V1.y - center.y) ** 2)
        for v in self.vertices[3:]:
            distanza = math.sqrt((v.x - center.x) ** 2 + (v.y - center.y) ** 2)
            if not is_near(distanza, radius):
                return False
        return True

    def get_unitary_radius(self) -> None:
        """Porta tutti i vertici di una poligonale già su una
        circonferenza su circonferenza unitaria."""
        if self.is_circle() is False:
            raise ValueError("I vertici non appartengono ad una circonferenza.")
        for v in self.vertices:
            v.change_coordinates(
                v.x / math.sqrt(v.x**2 + v.y**2), v.y / math.sqrt(v.x**2 + v.y**2)
            )
        self.save_state()

    def is_translation_regular(self, i: int, U: Vertex) -> bool:
        """Verifica se la traslazione del vertice
        i-esimo in un punto è regolare."""
        V_im2 = self.get_v(i - 2)
        V_im1 = self.get_v(i - 1)
        V_i = self.get_v(i)
        V_ip1 = self.get_v(i + 1)
        V_ip2 = self.get_v(i + 2)

        # Funzione per verificare i coni
        def is_in_cone(o: Vertex, A: Vertex, B: Vertex, Q: Vertex, P: Vertex) -> bool:
            """Verifica se il punto P sta nel cono
            definito da A,O,B contenente Q."""
            # Calcola gli angoli rispetto all'origine O (da -pi a pi)
            angle_A = math.atan2(A.y - o.y, A.x - o.x)
            angle_B = math.atan2(B.y - o.y, B.x - o.x)
            angle_Q = math.atan2(Q.y - o.y, Q.x - o.x)
            angle_P = math.atan2(P.y - o.y, P.x - o.x)
            # Tiene OA come riferimento
            diff_B = (angle_B - angle_A) % (2 * math.pi)
            diff_Q = (angle_Q - angle_A) % (2 * math.pi)
            diff_P = (angle_P - angle_A) % (2 * math.pi)
            if diff_Q < diff_B < diff_P or diff_P < diff_B < diff_Q:
                return False
            else:
                return True

        # Cono relativo a v_i in v_im1
        # Punto opposto a v_ip1 sulla semiretta v_im1-vip1
        test_point_v_im1 = Vertex(
            "Test point 1", V_im1.x - (V_ip1.x - V_im1.x), V_im1.y - (V_ip1.y - V_im1.y)
        )
        # P deve appartenere al cono contenente v_i
        # formato da v_im1-test_point_v_im1
        if is_in_cone(V_im1, test_point_v_im1, V_im2, V_i, U) is False:
            return False
        # Cono relativo a v_i in v_ip1
        # Punto opposto a v_im1 sulla semiretta v_ip1-vim1
        test_point_v_ip1 = Vertex(
            "Test point 2", V_ip1.x - (V_im1.x - V_ip1.x), V_ip1.y - (V_im1.y - V_ip1.y)
        )
        # P deve appartenere al cono contenente v_i
        # formato da v_im1-test_point_v_im1
        if is_in_cone(V_ip1, test_point_v_ip1, V_ip2, V_i, U) is False:
            return False
        return True

    def move_to_midpoint(self, i: int) -> None:
        """Trasla il vertice i-esimo nel punto medio del segmento con
        estremi i vertic precedente e successivo."""
        V_im1 = self.get_v(i - 1)
        V_ip1 = self.get_v(i + 1)
        # Punto medio
        M = Vertex("M", (V_im1.x + V_ip1.x) / 2, (V_im1.y + V_ip1.y) / 2)
        if self.is_translation_regular(i, M) is True:
            self.get_v(i).change_coordinates(
                (V_im1.x + V_ip1.x) / 2, (V_im1.y + V_ip1.y) / 2
            )
        else:
            raise ValueError("Non si può fare con trasformazioni regolari.")
        self.save_state()

    def move_and_eliminate(self, i: int) -> None:
        """Trasla il vertice i-esimo nel punto medio del segmento con
        estremi i vertici precedente e successivo e lo elimina."""
        self.move_to_midpoint(i)
        self.eliminate_vertex(i)
        print(f"Ho eliminato il vertice {self.get_v(i).name}")

    def move_to_circle(self) -> None:
        """
        Centra la poligonale nell'origine e proietta i vertici sulla circonferenza unitaria.
        """
        # Centriamo la poligonale nell'origine
        self.center_polygonal()
        # Verifico se i vertici sono già su una circonferenza
        if self.is_circle() is True:
            self.get_unitary_radius()
            return None
        n = len(self.vertices)
        # Calcoliamo il raggio massimo
        r = max(math.hypot(v.x, v.y) for v in self.vertices)
        # Ciclo sui vertici (da 1 a n)
        for i in range(1, n + 1):
            v = self.get_v(i)
            # Coordinate del vertice proiettato sul cerchio
            new_x = r * math.cos(v.angle)
            new_y = r * math.sin(v.angle)
            new_vertex = Vertex(v.name, new_x, new_y)
            new_angle = new_vertex.angle
            success_a = False
            # Proviamo la proiezione diretta
            if self.is_translation_regular(i, new_vertex) is True:
                while True:
                    if self.is_translation_regular(i, new_vertex) is False:
                        break
                    collision = False
                    for z in self.vertices:
                        if z.name == v.name:
                            continue
                        if is_near(z.x, new_vertex.x) and is_near(z.y, new_vertex.y):
                            collision = True
                            break
                    if collision:
                        new_angle += 10 * TOLERANCE
                        new_x = r * math.cos(new_angle)
                        new_y = r * math.sin(new_angle)
                        continue  # Ricontrolla tutti i vertici z con il nuovo angolo
                    v.change_coordinates(new_x, new_y)
                    self.save_state()
                    success_a = True
                    break
            # Ricerca sui punti medi (se la proiezione diretta ha fallito)
            if not success_a:

                def get_arc_midpoint(v1: Vertex, v2: Vertex) -> float:
                    """Ritorna l'angolo del punto medio di un arco tra i vertici v1 e v2."""
                    sin_sum = math.sin(v1.angle) + math.sin(v2.angle)
                    cos_sum = math.cos(v1.angle) + math.cos(v2.angle)
                    return math.atan2(sin_sum, cos_sum)

                neighbors = [
                    self.get_v(i - 2),
                    self.get_v(i - 1),
                    self.get_v(i + 1),
                    self.get_v(i + 2),
                ]
                candidates = []
                for idx_a in range(len(neighbors)):
                    for idx_b in range(idx_a + 1, len(neighbors)):
                        mid_angle = get_arc_midpoint(neighbors[idx_a], neighbors[idx_b])
                        candidates.append(mid_angle)
                success_b = False
                # Proviamo i candidati uno ad uno
                for cand_angle in candidates:
                    new_x_cand = r * math.cos(cand_angle)
                    new_y_cand = r * math.sin(cand_angle)
                    new_vertex = Vertex(v.name, new_x_cand, new_y_cand)
                    new_angle = cand_angle  # Parto dall'angolo del candidato
                    while True:
                        if self.is_translation_regular(i, new_vertex) is False:
                            break
                        collision_cand = False
                        for z in self.vertices:
                            if z.name == v.name:
                                continue
                            if is_near(z.x, new_vertex.x) and is_near(
                                z.y, new_vertex.y
                            ):
                                collision_cand = True
                                break
                        if collision_cand:
                            new_angle += 10 * TOLERANCE
                            new_x = r * math.cos(new_angle)
                            new_y = r * math.sin(new_angle)
                            continue  # Ricontrolla tutti i vertici z con il nuovo angolo
                        success_b = True
                        break
                    if success_b:
                        v.change_coordinates(new_x, new_y)
                        self.save_state()
                        break  # Esco dal ciclo dei candidati
        self.get_unitary_radius()

    def is_clockwise(self, list_vertices: list[Vertex]) -> bool:
        """Verifica se i vertici sulla circonferenza unitaria
        sono ordinati in senso orario
        (accetta anche vertici non distinti)."""
        if self.is_circle() is False:
            raise ValueError("I vertici non appartengono ad una circonferenza.")
        cleaned_list = [list_vertices[0]]
        # Tolgo uno dei vertici consecutivi uguali
        for i in range(1, len(list_vertices)):
            v_current = list_vertices[i]
            v_prev = cleaned_list[-1]
            # Se il vertice corrente è diverso dall'ultimo inserito, lo aggiungo
            if v_current != v_prev and not is_near(v_current.angle, v_prev.angle):
                cleaned_list.append(v_current)
        # Se la lista ha più di un elemento, confronto il primo con l'ultimo
        if len(cleaned_list) > 1:
            first_v = cleaned_list[0]
            last_v = cleaned_list[-1]
            # Se l'ultimo è praticamente coincidente con il primo, lo elimino
            if last_v == first_v or is_near(last_v.angle, first_v.angle):
                cleaned_list.pop()
        list_vertices = cleaned_list
        n = len(list_vertices)
        if n <= 2:
            return True
        # Prendo l'angolo del primo vertice come riferimento
        base_angle = list_vertices[0].angle
        for j in range(1, n - 1):
            current_angle = list_vertices[j].angle
            # Calcolo la differenza angolare rispetto all'angolo di riferimento
            # Sarà crescente in senso antiorario
            current_angle_normalised = (current_angle - base_angle) % (2 * math.pi)
            next_angle = list_vertices[(j + 1) % n].angle
            next_angle_normalised = (next_angle - base_angle) % (2 * math.pi)
            # Calcoliamo la differenza fra angoli compresi fra [0, 2pi]
            diff = next_angle_normalised - current_angle_normalised
            # Gestione caso vertici coincidenti o vicini
            v_current = list_vertices[j]
            v_next = list_vertices[(j + 1) % n]
            if v_current == v_next or is_near(v_current.angle, v_next.angle):
                continue
            # Se diff è positiva percorrendo la circonferenza
            # a partire dal vertice base i due sono in senso antiorario
            if diff > 0 and not is_near(diff, 2 * math.pi):
                return False
            # Gestisco il caso in cui il vertice è vicino al vertice base
        return True

    def is_counterclockwise(self, list_vertices: list[Vertex]) -> bool:
        """Verifica se i vertici sono in senso antiorario invertendo la lista e usando is_clockwise."""
        return self.is_clockwise(list_vertices[::-1])

    def sort_vertices_clockwise(self, list_vertices: list[Vertex]) -> list[Vertex]:
        """Restituisce i vertici ordinati in senso orario
        a partire dal primo vertice della lista."""
        if self.is_circle() is False:
            raise ValueError("I vertici non appartengono ad una circonferenza.")
        if self.is_clockwise(list_vertices):
            return list_vertices
        else:
            # Calcola gli angoli rispetto
            # all'angolo del primo vertice
            base_angle = list_vertices[0].angle

            def clockwise_distance(v):
                diff = (base_angle - v.angle) % (2 * math.pi)
                return diff

        # Il primo rimarrà in posizione 0 perché la sua diff è 0
        return sorted(list_vertices, key=clockwise_distance)

    def sort_vertices_counterclockwise(
        self, list_vertices: list[Vertex]
    ) -> list[Vertex]:
        """Restituisce i vertici ordinati in senso antiorario
        a partire dal primo vertice della lista."""
        if self.is_circle() is False:
            raise ValueError("I vertici non appartengono ad una circonferenza.")
        if self.is_counterclockwise(list_vertices):
            return list_vertices
        else:
            # Calcola gli angoli rispetto
            # all'angolo del primo vertice
            base_angle = list_vertices[0].angle

            def counterclockwise_distance(v):
                diff = (v.angle - base_angle) % (2 * math.pi)
                return diff

        # Il primo rimarrà in posizione 0 perché la sua diff è 0
        return sorted(list_vertices, key=counterclockwise_distance)

    def get_equispaced_vertices(self) -> None:
        """Equidistanza i vertici della poligonale sulla circonferenza"""
        if self.is_circle() is False:
            raise ValueError("I vertici non appartengono ad una circonferenza.")
        n = len(self.vertices)
        sorted_vertices = self.sort_vertices_clockwise(self.vertices)
        base_angle = sorted_vertices[0].angle
        # Assegna ad ogni vertice un nuovo angolo equispaziato
        for j in range(n):
            # Sottraiamo per andare in senso orario
            new_angle = (base_angle - (2 * math.pi * j / n)) % (2 * math.pi)
            sorted_vertices[j].change_angle(new_angle)
        self.save_state()

    def get_equispaced_vertices_fixed_12(self) -> None:
        """Equidistanza i vertici sul cerchio, tenendo fermi v1 e v2."""
        if self.is_circle() is False:
            raise ValueError("I vertici non appartengono ad una circonferenza.")

        n = len(self.vertices)
        if n <= 2:
            return  # Niente da spostare
        # Troviamo i vertici fissi
        v1 = self.get_v(1)
        v2 = self.get_v(2)
        # Otteniamo l'ordine orario attuale di tutti i vertici sul cerchio
        sorted_vertices = self.sort_vertices_clockwise(self.vertices)
        # Estraiamo solo i vertici che si trovano nel percorso da v2 a v1
        idx_v2 = sorted_vertices.index(v2)
        vertices_to_move = []
        curr_idx = (idx_v2 + 1) % n
        while sorted_vertices[curr_idx].name != v1.name:
            vertices_to_move.append(sorted_vertices[curr_idx])
            curr_idx = (curr_idx + 1) % n
        # Calcoliamo lo spazio orario totale disponibile tra v1 e v2
        # di solito sarà pi greco
        total_gap = (v2.angle - v1.angle) % (2 * math.pi)
        # Dividiamo lo spazio
        num_steps = len(vertices_to_move) + 1
        step_size = total_gap / num_steps
        # Spalmiamo i vertici uno ad uno
        for i, v in enumerate(vertices_to_move):
            # Andiamo in senso orario
            new_angle = (v2.angle - step_size * (i + 1)) % (2 * math.pi)
            v.change_angle(new_angle)
        # Estraiamo solo i vertici che si trovano nel percorso da v1 a v2
        idx_v1 = sorted_vertices.index(v1)
        vertices_to_move = []
        curr_idx = (idx_v1 + 1) % n
        while sorted_vertices[curr_idx].name != v2.name:
            vertices_to_move.append(sorted_vertices[curr_idx])
            curr_idx = (curr_idx + 1) % n
        # Calcoliamo lo spazio orario totale disponibile tra v1 e v2
        # di solito sarà pi greco
        total_gap = (v1.angle - v2.angle) % (2 * math.pi)
        # Dividiamo lo spazio
        num_steps = len(vertices_to_move) + 1
        step_size = total_gap / num_steps
        # Spalmiamo i vertici uno ad uno
        for i, v in enumerate(vertices_to_move):
            # Andiamo in senso orario
            new_angle = (v1.angle - step_size * (i + 1)) % (2 * math.pi)
            v.change_angle(new_angle)
        self.save_state()

    def rotate_vertex(self, i: int, delta_angle: float) -> None:
        """Ruota il vertice i rispetto all'origine spostandolo di
        'delta_angle'. Un delta positivo ruota in senso antiorario,
        negativo in senso orario."""
        # Calcoliamo il nuovo angolo sommandolo a quello attuale
        new_angle = (self.get_v(i).angle + delta_angle) % (2 * math.pi)
        self.get_v(i).change_angle(new_angle)
        self.save_state()

    def weak_translation_clockwise(self, i: int, target_angle: float) -> None:
        """Trasla il vertice i-esimo lungo la circonferenza unitaria
        in senso orario fino all'angolo target_angle preservando ordine
        e regolarità traslando tutti i vertici collegati
        (vedi lemma 2.12)."""
        if self.is_circle() is False:
            raise ValueError("I vertici non appartengono ad una circonferenza.")
        # Vertice finale
        target_x = math.cos(target_angle)
        target_y = math.sin(target_angle)
        target = Vertex("Target", target_x, target_y)
        # Vertice iniziale
        v_i = self.get_v(i)

        # Chiamo A l'arco fra v_i e target
        def is_in_arc_A(v: Vertex) -> bool:
            """Verifica se il vertice appartiene
            all'arco orario A tra v_i e punto target."""
            # Caso non incluso nel senso orario
            if v == v_i:
                return True
            # Se v è in senso orario rispetto a v_i e target,
            # allora è in A
            return self.is_clockwise([self.get_v(i), v, target])

        def get_active_vertices() -> list[Vertex]:
            """Ritorna la lista dei vertici collegati che vanno traslati."""

            def is_edge_active(j: int, k: int) -> bool:
                """Verifica se il lato con estremi v_j e v_k
                è attivo (ovvero almeno dei suoi estremi è in A)."""
                if k == j + 1 or k == j - 1:
                    v1 = self.get_v(j)
                    v2 = self.get_v(k)
                    return is_in_arc_A(v1) or is_in_arc_A(v2)
                else:
                    return False

            n = len(self.vertices)
            # Creo l'insieme degli indici attivi
            active_indices = {i % n}
            curr_idx = i
            # Poligonali attive "in avanti"
            while True:
                next_idx = curr_idx + 1
                # Se il lato (corrente, successivo) è attivo e
                # non l'abbiamo già visitato
                if (
                    is_edge_active(curr_idx, next_idx)
                    and (next_idx % n) not in active_indices
                ):
                    # Aggiungo vertice e passo al successivo
                    active_indices.add(next_idx % n)
                    curr_idx = next_idx
                else:
                    break
            # Poligonali attive "all'indietro"
            curr_idx = i
            while True:
                prev_idx = curr_idx - 1
                # Se il lato (precedente, corrente) è attivo
                # e non l'abbiamo già visitato
                if (
                    is_edge_active(prev_idx, curr_idx)
                    and (prev_idx % n) not in active_indices
                ):
                    active_indices.add(prev_idx % n)
                    curr_idx = prev_idx
                else:
                    break
            # Costruiamo la lista finale prendendo i vertici
            list_active_vertices = [self.get_v(idx) for idx in active_indices]
            return list_active_vertices

        # Lista dei vertici attivi
        active_vertices = get_active_vertices()
        # Lista dei vertici attivi di A
        active_vertices_in_A = [v for v in active_vertices if is_in_arc_A(v)]
        # Lista dei vertici attivi di A da traslare
        # in ordine (ovvero ordinati in senso antiorario !A PARTIRE DA v_i)
        active_vertices_in_A.remove(v_i)
        active_vertices_in_A.insert(0, v_i)
        active_vertices_in_A = list(
            reversed(self.sort_vertices_clockwise(active_vertices_in_A))
        )

        # Calcolo il vertice successivo al vertice target
        # Vertici della poligonale e target ordinati
        # in senso orario a partire da v1
        sorted_vertices = self.sort_vertices_clockwise(self.vertices + [target])
        # Chiediamo in che posizione si trova il target
        indice_target = sorted_vertices.index(target)
        # Estraiamo il vertice successivo.
        v_base = sorted_vertices[(indice_target + 1) % len(sorted_vertices)]
        # Vertici da spostare
        M = len(active_vertices_in_A)
        # Angolo di distanza per traslare i vertici
        diff_angle = (target_angle - v_base.angle) % (2 * math.pi)
        prev_angle = v_base.angle
        for idx, v in enumerate(active_vertices_in_A):
            k = idx + 1
            angle_v = (v_base.angle + diff_angle * k / M) % (2 * math.pi)
            # Controllo anti-sovrapposizione con altri vertici
            while True:
                for w in self.vertices:
                    if w.name == v.name:
                        continue
                    if is_near(w.angle, angle_v):
                        angle_v -= 10 * TOLERANCE
                break
            v_x = math.cos(angle_v)
            v_y = math.sin(angle_v)
            v.change_coordinates(v_x, v_y)
            self.save_state()

    def weak_translation_counterclockwise(self, i: int, target_angle: float) -> None:
        """Trasla il vertice i-esimo lungo la circonferenza unitaria
        in senso orario fino all'angolo target_angle preservando ordine
        e regolarità traslando tutti i vertici collegati
        (vedi lemma 2.12)."""
        if self.is_circle() is False:
            raise ValueError("I vertici non appartengono ad una circonferenza.")
        # Vertice finale
        target_x = math.cos(target_angle)
        target_y = math.sin(target_angle)
        target = Vertex("Target", target_x, target_y)
        # Vertice iniziale
        v_i = self.get_v(i)

        # Chiamo A l'arco fra v_i e target
        def is_in_arc_A(v: Vertex) -> bool:
            """Verifica se il vertice appartiene
            all'arco antiorario A tra v_i e punto target."""
            # Caso non incluso nel senso antiorario
            if v == v_i:
                return True
            # Se v è in senso antiorario rispetto a v_i e target,
            # allora è in A
            return self.is_counterclockwise([self.get_v(i), v, target])

        def get_active_vertices() -> list[Vertex]:
            """Ritorna la lista dei vertici collegati che vanno traslati."""

            def is_edge_active(j: int, k: int) -> bool:
                """Verifica se il lato con estremi v_j e v_k
                è attivo (ovvero almeno dei suoi estremi è in A)."""
                if k == j + 1 or k == j - 1:
                    v1 = self.get_v(j)
                    v2 = self.get_v(k)
                    return is_in_arc_A(v1) or is_in_arc_A(v2)
                else:
                    return False

            n = len(self.vertices)
            # Creo l'insieme degli indici attivi
            active_indices = {i % n}
            curr_idx = i
            # Poligonali attive "in avanti"
            while True:
                next_idx = curr_idx + 1
                # Se il lato (corrente, successivo) è attivo e
                # non l'abbiamo già visitato
                if (
                    is_edge_active(curr_idx, next_idx)
                    and (next_idx % n) not in active_indices
                ):
                    # Aggiungo vertice e passo al successivo
                    active_indices.add(next_idx % n)
                    curr_idx = next_idx
                else:
                    break
            # Poligonali attive "all'indietro"
            curr_idx = i
            while True:
                prev_idx = curr_idx - 1
                # Se il lato (precedente, corrente) è attivo
                # e non l'abbiamo già visitato
                if (
                    is_edge_active(prev_idx, curr_idx)
                    and (prev_idx % n) not in active_indices
                ):
                    active_indices.add(prev_idx % n)
                    curr_idx = prev_idx
                else:
                    break
            # Costruiamo la lista finale prendendo i vertici
            list_active_vertices = [self.get_v(idx) for idx in active_indices]
            return list_active_vertices

        # Lista dei vertici attivi
        active_vertices = get_active_vertices()
        # Lista dei vertici attivi di A
        active_vertices_in_A = [v for v in active_vertices if is_in_arc_A(v)]
        # Lista dei vertici attivi di A da traslare
        # in ordine (ovvero ordinati in senso antiorario  !A PARTIRE DA v_i)
        active_vertices_in_A.remove(v_i)
        active_vertices_in_A.insert(0, v_i)
        active_vertices_in_A = list(
            reversed(self.sort_vertices_counterclockwise(active_vertices_in_A))
        )
        # Calcolo il vertice successivo al vertice target
        # Vertici della poligonale e target ordinati
        # in senso antiorario a partire da v1
        sorted_vertices = self.sort_vertices_counterclockwise(self.vertices + [target])
        # Chiediamo in che posizione si trova il target
        indice_target = sorted_vertices.index(target)
        # Estraiamo il vertice successivo.
        v_base = sorted_vertices[(indice_target + 1) % len(sorted_vertices)]
        # Vertici da spostare
        M = len(active_vertices_in_A)
        # Angolo di distanza per traslare i vertici
        diff_angle = (v_base.angle - target.angle) % (2 * math.pi)
        prev_angle = v_base.angle
        for idx, v in enumerate(active_vertices_in_A):
            k = idx + 1
            angle_v = (v_base.angle - diff_angle * k / M) % (2 * math.pi)
            # Controllo anti-sovrapposizione con altri vertici
            while True:
                for w in self.vertices:
                    if w.name == v.name:
                        continue
                    if is_near(w.angle, angle_v):
                        angle_v += 10 * TOLERANCE
                break
            v_x = math.cos(angle_v)
            v_y = math.sin(angle_v)
            v.change_coordinates(v_x, v_y)
            self.save_state()

    def get_next_clockwise(self, i: int) -> Vertex:
        """Restituisce il vertice successivo all'i-esimo in senso orario."""
        sorted_vertices = self.sort_vertices_clockwise(self.vertices)
        start_vertex = self.get_v(i)
        # Trovo in che posizione si trova ora nella lista ordinata
        current_idx = sorted_vertices.index(start_vertex)
        # Calcolo l'indice successivo.
        next_idx = (current_idx + 1) % len(sorted_vertices)
        # Ritorno il vertice trovato
        return sorted_vertices[next_idx]

    def get_next_counterclockwise(self, i: int) -> Vertex:
        """Restituisce il vertice successivo all'i-esimo in senso antiorario."""
        sorted_vertices = self.sort_vertices_counterclockwise(self.vertices)
        start_vertex = self.get_v(i)
        # Trovo in che posizione si trova ora nella lista ordinata
        current_idx = sorted_vertices.index(start_vertex)
        # Calcolo l'indice successivo.
        next_idx = (current_idx + 1) % len(sorted_vertices)
        # Ritorno il vertice trovato
        return sorted_vertices[next_idx]

    def permute_vertices_backward(self):
        """
        Ruota i vertici all'indietro di 1 posizione .
        Il vecchio v2 diventa il nuovo v1, v3 diventa v2, ..., e il vecchio v1 diventa l'ultimo.
        """
        # Estraggo il primo elemento e lo metto alla fine
        self.vertices.append(self.vertices.pop(0))
        print("Ho permutato ciclicamente i vertici indietro di 1.")

    def is_polygonal_reduced(self):
        n = len(self.vertices)
        if n == 4:
            return is_near(self.get_winding_number(), 0)
        else:
            return is_near(math.fabs(self.get_winding_number()), (n - 1) / 2)

    def case_A1(self, i: int) -> int:
        """Svolge le operazioni del caso A1 tornando l'indice da processare."""
        print("Caso A1")
        self.move_to_midpoint(i - 1)
        self.eliminate_vertex(i - 1)
        return i - 1

    def case_A21(self, i: int) -> int:
        """Svolge le operazioni del caso A21 tornando l'indice da processare."""
        print("Caso A21")
        if self.is_left_turn(2) is True:
            if self.is_clockwise(
                [
                    self.get_v(i),
                    self.get_v(i + 1),
                    self.get_v(i - 2),
                ]
            ):
                self.move_to_midpoint(i - 1)
                self.eliminate_vertex(i - 1)
                return i - 1
            else:
                # Caso j=1
                if i % len(self.vertices) == 1:
                    angle = (self.get_next_clockwise(2).angle + 2 * math.pi) / 2

                else:
                    angle = self.get_v(i + 1).angle / 2
                self.weak_translation_clockwise(i - 2, angle)

                self.move_to_midpoint(i - 1)
                self.eliminate_vertex(i - 1)
                return i - 1
        else:
            # Caso A211
            if not self.is_counterclockwise(
                [
                    self.get_v(i),
                    self.get_v(i + 1),
                    self.get_v(i - 2),
                ]
            ):
                # Caso j=1
                if i % len(self.vertices) == 1:

                    angle = (
                        self.get_next_counterclockwise(2).angle + self.get_v(2).angle
                    ) / 2

                else:
                    angle = (self.get_v(i + 1).angle + 2 * math.pi) / 2
                self.weak_translation_counterclockwise(i - 2, angle)
            self.move_to_midpoint(i - 1)
            self.eliminate_vertex(i - 1)
            return i - 1

    def case_A22(self, i: int) -> int:
        """Svolge le operazioni del caso A22 tornando l'indice da processare."""
        print("Caso A22")
        if self.is_left_turn(2) is True:
            # Primo passaggio
            vertices_to_check = [
                self.get_v(i - 4),
                self.get_v(i),
                self.get_v(i - 2),
            ]
            if not self.is_clockwise(vertices_to_check):
                angle_1 = (math.pi + self.get_v(i).angle) / 2

                self.weak_translation_counterclockwise(i - 4, angle_1)
            if not self.is_clockwise(vertices_to_check):
                angle_2 = self.get_v(i).angle / 2
                self.weak_translation_clockwise(i - 2, angle_2)
            vertices_check = [
                self.get_v(i - 4),
                self.get_v(i),
                self.get_v(i - 2),
            ]
            if not self.is_clockwise(vertices_check) is True:
                raise ValueError("Primo passaggio non riuscito.")
            # Secondo passaggio
            vertices_to_check_2 = [
                self.get_v(i - 4),
                self.get_v(i - 1),
                self.get_v(i),
            ]
            if not self.is_clockwise(vertices_to_check_2):
                angle_3 = (self.get_v(i - 4).angle + self.get_v(i).angle) / 2
                self.weak_translation_clockwise(i - 1, angle_3)

            if (
                not self.is_clockwise(
                    [
                        self.get_v(i - 4),
                        self.get_v(i - 1),
                        self.get_v(i),
                    ]
                )
                is True
            ):
                raise ValueError("Secondo passaggio non riuscito.")
            self.move_to_midpoint(i - 2)
            self.eliminate_vertex(i - 2)
            return i - 1
        else:
            # Primo passaggio
            vertices_to_check = [
                self.get_v(i - 4),
                self.get_v(i),
                self.get_v(i - 2),
            ]
            if not self.is_counterclockwise(vertices_to_check):
                angle_1 = (math.pi + self.get_v(i).angle) / 2

                self.weak_translation_clockwise(i - 4, angle_1)
            if not self.is_counterclockwise(vertices_to_check):

                angle_2 = (self.get_v(i).angle + 2 * math.pi) / 2
                self.weak_translation_counterclockwise(i - 2, angle_2)
            vertices_check = [
                self.get_v(i - 4),
                self.get_v(i),
                self.get_v(i - 2),
            ]
            if not self.is_counterclockwise(vertices_check) is True:
                raise ValueError("Primo passaggio non riuscito")
            # Secondo passaggio
            vertices_to_check_2 = [
                self.get_v(i - 4),
                self.get_v(i - 1),
                self.get_v(i),
            ]
            if not self.is_counterclockwise(vertices_to_check_2):

                angle_3 = (self.get_v(i - 4).angle + self.get_v(i).angle) / 2
                self.weak_translation_counterclockwise(i - 1, angle_3)
            if (
                not self.is_counterclockwise(
                    [
                        self.get_v(i - 4),
                        self.get_v(i - 1),
                        self.get_v(i),
                    ]
                )
                is True
            ):
                raise ValueError("Secondo passaggio non riuscito")
            self.move_to_midpoint(i - 2)
            self.eliminate_vertex(i - 2)
            return i - 1

    def case_A231(self, i: int) -> int:
        """Svolge le operazioni del caso A231 tornando l'indice da processare."""
        print("Caso A231")
        if self.is_left_turn(2) is True:
            angle = (self.get_next_clockwise(1).angle + self.get_v(1).angle) / 2
            self.weak_translation_clockwise(i, angle)
            return i
        else:
            angle = (self.get_next_counterclockwise(1).angle + self.get_v(1).angle) / 2
            self.weak_translation_counterclockwise(i, angle)
            return i

    def case_A2321(self, i: int) -> int:
        """Svolge le operazioni del caso A2321 tornando l'indice da processare."""
        print("Caso A2321")
        self.move_to_midpoint(i + 1)
        self.eliminate_vertex(i + 1)
        self.move_to_midpoint(i)
        self.eliminate_vertex(i)
        return i

    def case_A2322(self, i: int) -> int:
        """Svolge le operazioni del caso A2322 tornando l'indice da processare."""
        print("Caso A2322")
        if self.is_left_turn(2) is True:
            angle = (self.get_v(i - 2).angle + self.get_v(1).angle) / 2
            self.weak_translation_counterclockwise(i + 1, angle)
            if not self.is_clockwise(
                [
                    self.get_v(1),
                    self.get_v(i + 1),
                    self.get_v(i - 2),
                ]
            ):
                raise ValueError("Passaggio non riuscito.")
            self.move_to_midpoint(i - 1)
            self.eliminate_vertex(i - 1)
            # Nella teoria sarebbe j ma la lista si è aggiornata con l'eliminazione di i-1
            self.move_to_midpoint(i - 1)
            self.eliminate_vertex(i - 1)
            self.move_to_midpoint(i - 1)
            self.eliminate_vertex(i - 1)
            return i - 2
        else:
            angle = (self.get_v(i - 2).angle + self.get_v(1).angle) / 2
            self.weak_translation_clockwise(i + 1, angle)
            if not self.is_counterclockwise(
                [
                    self.get_v(1),
                    self.get_v(i + 1),
                    self.get_v(i - 2),
                ]
            ):
                raise ValueError("Passaggio non riuscito")
            self.move_to_midpoint(i - 1)
            self.eliminate_vertex(i - 1)
            self.move_to_midpoint(i - 1)
            self.eliminate_vertex(i - 1)
            self.move_to_midpoint(i - 1)
            self.eliminate_vertex(i - 1)
            return i - 2

    def case_B1(self, i: int) -> int:
        """Svolge le operazioni del caso B1 tornando l'indice da processare."""
        print("Caso B1")
        return i + 1

    def case_B21(self, i: int) -> int:
        """Svolge le operazioni del caso B21 tornando l'indice da processare."""
        print("Caso B21")
        if self.is_left_turn(2) is True:
            if not self.is_clockwise(
                [
                    self.get_v(2),
                    self.get_v(i - 3),
                    self.get_v(i),
                ]
            ):
                # Traslo i-3 fra j e 2
                angle = (2 * math.pi + self.get_v(i).angle) / 2
                self.weak_translation_counterclockwise(i - 3, angle)
            self.move_to_midpoint(i - 1)
            self.eliminate_vertex(i - 1)
            return i - 1
        else:
            if not self.is_counterclockwise(
                [
                    self.get_v(2),
                    self.get_v(i - 3),
                    self.get_v(i),
                ]
            ):
                angle = (self.get_v(2).angle + self.get_v(i).angle) / 2
                self.weak_translation_clockwise(i - 3, angle)
            self.move_to_midpoint(i - 1)
            self.eliminate_vertex(i - 1)
            return i - 1

    def case_B2211(self, i: int) -> int:
        """Svolge le operazioni del caso B2211 tornando l'indice da processare."""
        print("Caso B2211")
        if self.is_left_turn(2) is True:
            if not self.is_clockwise(
                [
                    self.get_v(i - 2),
                    self.get_v(i),
                    self.get_v(2),
                ]
            ):
                angle = self.get_next_counterclockwise(2).angle / 2
                self.weak_translation_counterclockwise(i, angle)
                if not self.is_clockwise(
                    [
                        self.get_v(i - 2),
                        self.get_v(i),
                        self.get_v(2),
                    ]
                ):
                    raise ValueError("Controllo dopo traslazione non riuscito.")
                return i
        else:
            if not self.is_counterclockwise(
                [
                    self.get_v(i - 2),
                    self.get_v(i),
                    self.get_v(2),
                ]
            ):
                angle = (self.get_next_clockwise(2).angle + 2 * math.pi) / 2
                self.weak_translation_clockwise(i, angle)
                if not self.is_counterclockwise(
                    [
                        self.get_v(i - 2),
                        self.get_v(i),
                        self.get_v(2),
                    ]
                ):
                    raise ValueError("Controllo dopo traslazione non riuscito")
                return i

    def case_B22121(self, i: int) -> int:
        """Svolge le operazioni del caso B22121 tornando l'indice da processare."""
        print("Caso B22121")
        self.move_to_midpoint(i + 1)
        self.eliminate_vertex(i + 1)
        if i % len(self.vertices) == 1:
            self.move_to_midpoint(i - 1)
            self.eliminate_vertex(i - 1)
        else:
            self.move_to_midpoint(i)
            self.eliminate_vertex(i)
        return i - 1

    def case_B22122(self, i: int) -> int:
        """Svolge le operazioni del caso B22122 tornando l'indice da processare."""
        print("Caso B22122")
        if self.is_left_turn(2) is True:
            if not self.is_clockwise(
                [
                    self.get_v(i - 3),
                    self.get_v(i),
                    self.get_v(i - 1),
                ]
            ):
                # Traslo i-3 in un intorno di 2
                angle = (2 * math.pi - self.get_next_clockwise(2).angle) / 2
                self.weak_translation_counterclockwise(
                    i - 3,
                    2 * math.pi - angle,
                )
            if not self.is_clockwise(
                [
                    self.get_v(i - 3),
                    self.get_v(i),
                    self.get_v(i - 1),
                ]
            ):
                raise ValueError("Controllo dopo traslazione non riuscito.")

            if not self.is_clockwise(
                [
                    self.get_v(i - 2),
                    self.get_v(i + 1),
                    self.get_v(2),
                ]
            ):
                # Traslo j+1
                angle = (self.get_next_counterclockwise(2).angle) / 2
                self.weak_translation_clockwise(i + 1, angle)
            if not self.is_clockwise(
                [
                    self.get_v(i - 2),
                    self.get_v(i + 1),
                    self.get_v(2),
                ]
            ):
                raise ValueError("Controllo dopo traslazione non riuscito.")
            self.move_to_midpoint(i - 1)
            self.eliminate_vertex(i - 1)
            return i - 1
        else:
            if not self.is_counterclockwise(
                [
                    self.get_v(i - 3),
                    self.get_v(i),
                    self.get_v(i - 1),
                ]
            ):

                angle = (
                    self.get_v(2).angle + self.get_next_counterclockwise(2).angle
                ) / 2
                self.weak_translation_clockwise(i - 3, angle)
            if not self.is_counterclockwise(
                [
                    self.get_v(i - 3),
                    self.get_v(i),
                    self.get_v(i - 1),
                ]
            ):
                raise ValueError("Controllo dopo traslazione non riuscito")

            if not self.is_counterclockwise(
                [
                    self.get_v(i - 2),
                    self.get_v(i + 1),
                    self.get_v(2),
                ]
            ):
                angle = (self.get_next_clockwise(2).angle + 2 * math.pi) / 2
                self.weak_translation_counterclockwise(i + 1, angle)
            if not self.is_counterclockwise(
                [
                    self.get_v(i - 2),
                    self.get_v(i + 1),
                    self.get_v(2),
                ]
            ):
                raise ValueError("Controllo dopo traslazione non riuscito")
            self.move_to_midpoint(i - 1)
            self.eliminate_vertex(i - 1)
            return i - 1

    def case_B222(self, i: int) -> int:
        """Svolge le operazioni del caso B222 tornando l'indice da processare."""
        print("Caso B222")
        if self.is_left_turn(2) is True:
            # Passaggio 1
            if not self.is_clockwise(
                [
                    self.get_v(i - 2),
                    self.get_v(i + 1),
                    self.get_v(i),
                ]
            ):
                angle = (
                    self.get_next_counterclockwise(i + 1).angle
                    + self.get_v(i + 1).angle
                ) / 2
                self.weak_translation_counterclockwise(i - 2, angle)
            if not self.is_clockwise(
                [
                    self.get_v(i - 2),
                    self.get_v(i + 1),
                    self.get_v(i),
                ]
            ):
                raise ValueError("Controllo dopo traslazione non riuscito.")

            # Passaggio 2
            if not self.is_clockwise(
                [
                    self.get_v(i - 3),
                    self.get_v(i),
                    self.get_v(i - 1),
                ]
            ):
                angle = (2 * math.pi + self.get_v(i).angle) / 2
                self.weak_translation_counterclockwise(i - 3, angle)
            if not self.is_clockwise(
                [
                    self.get_v(i - 3),
                    self.get_v(i),
                    self.get_v(i - 1),
                ]
            ):
                raise ValueError("Controllo dopo traslazione non riuscito.")
            self.move_to_midpoint(i - 1)
            self.eliminate_vertex(i - 1)
            return i - 1
        else:
            # Passaggio 1
            if not self.is_counterclockwise(
                [
                    self.get_v(i - 2),
                    self.get_v(i + 1),
                    self.get_v(i),
                ]
            ):
                angle = (
                    self.get_next_clockwise(i + 1).angle + self.get_v(i + 1).angle
                ) / 2
                self.weak_translation_clockwise(i - 2, angle)

            if not self.is_counterclockwise(
                [
                    self.get_v(i - 2),
                    self.get_v(i + 1),
                    self.get_v(i),
                ]
            ):
                raise ValueError("Controllo dopo traslazione non riuscito")

            # Passaggio 2
            if not self.is_counterclockwise(
                [
                    self.get_v(i - 3),
                    self.get_v(i),
                    self.get_v(i - 1),
                ]
            ):

                angle = (self.get_v(2).angle + self.get_v(i).angle) / 2
                self.weak_translation_clockwise(i - 3, angle)
            if not self.is_counterclockwise(
                [
                    self.get_v(i - 3),
                    self.get_v(i),
                    self.get_v(i - 1),
                ]
            ):
                raise ValueError("Controllo dopo traslazione non riuscito")
            self.move_to_midpoint(i - 1)
            self.eliminate_vertex(i - 1)
            return i - 1

    def case_C1(self, i: int) -> int:
        """Svolge le operazioni del caso C1 tornando l'indice da processare."""
        print("Caso C1")
        self.move_to_midpoint(i - 1)
        self.eliminate_vertex(i - 1)
        return i - 1

    def case_C21(self, i: int) -> int:
        """Svolge le operazioni del caso C21 tornando l'indice da processare."""
        print("Caso C21")
        if self.is_left_turn(2) is True:
            # Caso C211
            if self.is_clockwise(
                [
                    self.get_v(i),
                    self.get_v(i + 1),
                    self.get_v(i - 2),
                ]
            ):
                self.move_to_midpoint(i - 1)
                self.eliminate_vertex(i - 1)
                return i - 1

            # Caso C212
            else:
                # Caso limite j+1 = 1
                if (i + 1) % len(self.vertices) == 1:
                    angle = (self.get_v(1).angle + self.get_next_clockwise(1).angle) / 2
                    self.weak_translation_clockwise(i - 2, angle)
                    self.move_to_midpoint(i - 1)
                    self.eliminate_vertex(i - 1)
                    return 4
                else:
                    angle = (self.get_v(i + 1).angle + math.pi) / 2
                    self.weak_translation_clockwise(i - 2, angle)
                    self.move_to_midpoint(i - 1)
                    self.eliminate_vertex(i - 1)
                    return i - 1
        else:
            if self.is_counterclockwise(
                [
                    self.get_v(i),
                    self.get_v(i + 1),
                    self.get_v(i - 2),
                ]
            ):
                self.move_to_midpoint(i - 1)
                self.eliminate_vertex(i - 1)
                return i - 1
            else:
                # Caso limite j+1 = 1
                if (i + 1) % len(self.vertices) == 1:
                    angle = (
                        self.get_v(1).angle + self.get_next_counterclockwise(1).angle
                    ) / 2
                    self.weak_translation_counterclockwise(i - 2, angle)
                    self.move_to_midpoint(i - 1)
                    self.eliminate_vertex(i - 1)
                    return 4
                else:
                    angle = (self.get_v(i + 1).angle + math.pi) / 2
                    self.weak_translation_counterclockwise(i - 2, angle)
                    self.move_to_midpoint(i - 1)
                    self.eliminate_vertex(i - 1)
                    return i - 1

    def case_C22(self, i: int) -> int:
        """Svolge le operazioni del caso C22 tornando l'indice da processare."""
        print("Caso C22")
        if self.is_left_turn(2) is True:
            # Primo passaggio
            vertices_to_check = [
                self.get_v(i - 4),
                self.get_v(i),
                self.get_v(i - 2),
            ]
            if not self.is_clockwise(vertices_to_check):
                angle_1 = (2 * math.pi + self.get_v(i).angle) / 2
                angle_2 = (math.pi + self.get_v(i).angle) / 2
                self.weak_translation_counterclockwise(i - 4, angle_1)
                self.weak_translation_clockwise(i - 2, angle_2)

            vertices_check = [
                self.get_v(i - 4),
                self.get_v(i),
                self.get_v(i - 2),
            ]
            if not self.is_clockwise(vertices_check) is True:
                raise ValueError("Primo passaggio non riuscito")

            # Secondo passaggio
            vertices_to_check_2 = [
                self.get_v(i - 4),
                self.get_v(i - 1),
                self.get_v(i),
            ]
            if not self.is_clockwise(vertices_to_check_2):
                angle_3 = (self.get_v(i - 4).angle + self.get_v(i).angle) / 2
                if (i - 4) == 2:
                    angle_3 = (2 * math.pi + self.get_v(i).angle) / 2
                self.weak_translation_clockwise(i - 1, angle_3)

            if (
                not self.is_clockwise(
                    [
                        self.get_v(i - 4),
                        self.get_v(i - 1),
                        self.get_v(i),
                    ]
                )
                is True
            ):
                raise ValueError("Secondo passaggio non riuscito")
            self.move_to_midpoint(i - 2)
            self.eliminate_vertex(i - 2)
            return i - 1
        else:
            # Primo passaggio
            vertices_to_check = [
                self.get_v(i - 4),
                self.get_v(i),
                self.get_v(i - 2),
            ]
            if not self.is_counterclockwise(vertices_to_check):

                angle_1 = (self.get_v(2).angle + self.get_v(i).angle) / 2
                angle_2 = (math.pi + self.get_v(i).angle) / 2
                self.weak_translation_clockwise(i - 4, angle_1)
                self.weak_translation_counterclockwise(i - 2, angle_2)
            vertices_check = [
                self.get_v(i - 4),
                self.get_v(i),
                self.get_v(i - 2),
            ]
            if not self.is_counterclockwise(vertices_check) is True:
                raise ValueError("Primo passaggio non riuscito")
            # Secondo passaggio
            vertices_to_check_2 = [
                self.get_v(i - 4),
                self.get_v(i - 1),
                self.get_v(i),
            ]
            if not self.is_counterclockwise(vertices_to_check_2):
                angle_3 = (self.get_v(i - 4).angle + self.get_v(i).angle) / 2
                if (i - 4) == 2:
                    angle_3 = (self.get_v(2).angle + self.get_v(i).angle) / 2
                self.weak_translation_counterclockwise(i - 1, angle_3)
            if (
                not self.is_counterclockwise(
                    [
                        self.get_v(i - 4),
                        self.get_v(i - 1),
                        self.get_v(i),
                    ]
                )
                is True
            ):
                raise ValueError("Secondo passaggio non riuscito")
            self.move_to_midpoint(i - 2)
            self.eliminate_vertex(i - 2)
            return i - 1

    def case_C231(self, i: int) -> int:
        """Svolge le operazioni del caso C231 tornando l'indice da processare."""
        print("Caso C231")
        if self.is_left_turn(2) is True:
            angle = (
                self.get_next_clockwise(
                    # self.get_v(2).angle) / 2
                    2
                ).angle
                + 2 * math.pi
            ) / 2
            self.weak_translation_clockwise(i, angle)
            return i
        else:
            angle = (self.get_next_counterclockwise(2).angle + self.get_v(2).angle) / 2
            self.weak_translation_counterclockwise(i, angle)
            return i

    def case_C2321(self, i: int) -> int:
        """Svolge le operazioni del caso C2321 tornando l'indice da processare."""
        print("Caso C2321")
        self.move_to_midpoint(i + 1)
        self.eliminate_vertex(i + 1)
        self.move_to_midpoint(i)
        self.eliminate_vertex(i)
        return i

    def case_C2322(self, i: int) -> int:
        """Svolge le operazioni del caso C2322 tornando l'indice da processare."""
        print("Caso C2322")
        if self.is_left_turn(2) is True:
            angle = (self.get_v(i - 2).angle + 2 * math.pi) / 2
            self.weak_translation_counterclockwise(i + 1, angle)
            if not self.is_clockwise(
                [
                    self.get_v(2),
                    self.get_v(i + 1),
                    self.get_v(i - 2),
                ]
            ):
                raise ValueError("Passaggio non riuscito.")
            self.move_to_midpoint(i - 1)
            self.eliminate_vertex(i - 1)
            # Nella teoria sarebbe j ma la lista si è aggiornata con l'eliminazione di i-1
            self.move_to_midpoint(i - 1)
            self.eliminate_vertex(i - 1)
            self.move_to_midpoint(i - 1)
            self.eliminate_vertex(i - 1)
            return i - 2
        else:
            angle = (self.get_v(i - 2).angle + self.get_v(2).angle) / 2
            self.weak_translation_clockwise(i + 1, angle)
            if not self.is_counterclockwise(
                [
                    self.get_v(2),
                    self.get_v(i + 1),
                    self.get_v(i - 2),
                ]
            ):
                raise ValueError("Passaggio non riuscito")
            self.move_to_midpoint(i - 1)
            self.eliminate_vertex(i - 1)
            self.move_to_midpoint(i - 1)
            self.eliminate_vertex(i - 1)
            self.move_to_midpoint(i - 1)
            self.eliminate_vertex(i - 1)
            return i - 2

    def case_D1(self, i: int) -> int:
        """Svolge le operazioni del caso D1 tornando l'indice da processare."""
        print("Caso D1")
        return i + 1

    def case_D21(self, i: int) -> int:
        """Svolge le operazioni del caso D21 tornando l'indice da processare."""
        print("Caso D21")
        if self.is_left_turn(2) is True:
            if not self.is_clockwise(
                [
                    self.get_v(1),
                    self.get_v(i - 3),
                    self.get_v(i),
                ]
            ):
                # Traslo i-3 fra j e 1
                angle = (self.get_v(1).angle + self.get_v(i).angle) / 2
                self.weak_translation_counterclockwise(i - 3, angle)
            self.move_to_midpoint(i - 1)
            self.eliminate_vertex(i - 1)
            return i - 1
        else:
            if not self.is_counterclockwise(
                [
                    self.get_v(1),
                    self.get_v(i - 3),
                    self.get_v(i),
                ]
            ):
                # Traslo i-3 fra j e 1
                angle = (self.get_v(1).angle + self.get_v(i).angle) / 2
                self.weak_translation_clockwise(i - 3, angle)
            self.move_to_midpoint(i - 1)
            self.eliminate_vertex(i - 1)
            return i - 1

    def case_D2211(self, i: int) -> int:
        """Svolge le operazioni del caso D2211 tornando l'indice da processare."""
        print("Caso D2211")
        if self.is_left_turn(2) is True:
            if not self.is_clockwise(
                [
                    self.get_v(i - 2),
                    self.get_v(i),
                    self.get_v(1),
                ]
            ):
                # Caso limite i = 4
                if i == 4:
                    angle = self.get_v(1).angle + math.pi / 6
                else:
                    angle = (
                        self.get_next_counterclockwise(1).angle + self.get_v(1).angle
                    ) / 2
                self.weak_translation_counterclockwise(i, angle)
                if not self.is_clockwise(
                    [
                        self.get_v(i - 2),
                        self.get_v(i),
                        self.get_v(2),
                    ]
                ):
                    raise ValueError("Controllo dopo traslazione non riuscito")
            return i + 1
        else:
            if not self.is_counterclockwise(
                [
                    self.get_v(i - 2),
                    self.get_v(i),
                    self.get_v(1),
                ]
            ):
                if i == 4:
                    angle = (self.get_v(1).angle + self.get_next_clockwise(1).angle) / 2
                    self.weak_translation_clockwise(i, angle)

                else:
                    angle = (self.get_next_clockwise(1).angle + self.get_v(1).angle) / 2
                    self.weak_translation_clockwise(i, angle)
                    if not self.is_counterclockwise(
                        [
                            self.get_v(i - 2),
                            self.get_v(i),
                            self.get_v(2),
                        ]
                    ):
                        raise ValueError("Controllo dopo traslazione non riuscito")
            return i + 1

    def case_D22121(self, i: int) -> int:
        """Svolge le operazioni del caso D22121 tornando l'indice da processare."""
        print("Caso D22121")
        self.move_to_midpoint(i + 1)
        self.eliminate_vertex(i + 1)
        self.move_to_midpoint(i)
        self.eliminate_vertex(i)
        if (i + 1) % len(self.vertices) == 1:
            return i - 1
        else:
            return i

    def case_D22122(self, i: int) -> int:
        """Svolge le operazioni del caso D22122 tornando l'indice da processare."""
        print("Caso D22122")
        if self.is_left_turn(2) is True:
            # Caso limite
            if i == 4:
                if (
                    self.is_clockwise(
                        [
                            self.get_v(2),
                            self.get_v(5),
                            self.get_v(4),
                        ]
                    )
                    is True
                ):
                    self.move_to_midpoint(3)
                    self.eliminate_vertex(3)

                    self.move_to_midpoint(4)
                    self.eliminate_vertex(4)
                    return 4
                else:
                    self.permute_vertices_backward()
                    print(
                        f"I nuovi riferimenti sono {self.get_v(1).name} e {self.get_v(2).name}."
                    )
                    self.weak_translation_clockwise(1, math.pi)
                    self.weak_translation_clockwise(2, 0)
                    return i
            if not self.is_clockwise(
                [
                    self.get_v(i - 3),
                    self.get_v(i),
                    self.get_v(i - 1),
                ]
            ):
                # Traslo i-3 in un intorno di 1
                angle = (self.get_v(1).angle + self.get_next_clockwise(1).angle) / 2
                self.weak_translation_counterclockwise(i - 3, angle)
            if not self.is_clockwise(
                [
                    self.get_v(i - 3),
                    self.get_v(i),
                    self.get_v(i - 1),
                ]
            ):
                raise ValueError("Controllo dopo traslazione non riuscito")
            if not self.is_clockwise(
                [
                    self.get_v(i - 2),
                    self.get_v(i + 1),
                    self.get_v(1),
                ]
            ):
                # Traslo j+1
                angle = (
                    self.get_next_counterclockwise(1).angle + self.get_v(1).angle
                ) / 2
                self.weak_translation_clockwise(i + 1, angle)
            if not self.is_clockwise(
                [
                    self.get_v(i - 2),
                    self.get_v(i + 1),
                    self.get_v(1),
                ]
            ):
                raise ValueError("Controllo dopo traslazione non riuscito")

            self.move_to_midpoint(i - 1)
            self.eliminate_vertex(i - 1)
            return i - 1
        else:
            # Caso limite
            if i == 4:
                if (
                    self.is_counterclockwise(
                        [
                            self.get_v(2),
                            self.get_v(5),
                            self.get_v(4),
                        ]
                    )
                    is True
                ):
                    self.move_to_midpoint(3)
                    self.eliminate_vertex(3)

                    self.move_to_midpoint(4)
                    self.eliminate_vertex(4)
                    return i
                else:
                    self.permute_vertices_backward()
                    print(
                        f"I nuovi riferimenti sono {self.get_v(1).name} e {self.get_v(2).name}."
                    )
                    self.weak_translation_counterclockwise(1, math.pi)
                    self.weak_translation_counterclockwise(2, 0)
                    return i
            if not self.is_counterclockwise(
                [
                    self.get_v(i - 3),
                    self.get_v(i),
                    self.get_v(i - 1),
                ]
            ):
                # Traslo i-3 in un intorno di 1
                angle = (
                    self.get_v(1).angle + self.get_next_counterclockwise(1).angle
                ) / 2
                self.weak_translation_clockwise(i - 3, angle)
            if not self.is_counterclockwise(
                [
                    self.get_v(i - 3),
                    self.get_v(i),
                    self.get_v(i - 1),
                ]
            ):
                raise ValueError("Controllo dopo traslazione non riuscito")
            if not self.is_counterclockwise(
                [
                    self.get_v(i - 2),
                    self.get_v(i + 1),
                    self.get_v(1),
                ]
            ):
                # Traslo j+1
                angle = (self.get_next_clockwise(1).angle + self.get_v(1).angle) / 2
                self.weak_translation_counterclockwise(i + 1, angle)
            if not self.is_counterclockwise(
                [
                    self.get_v(i - 2),
                    self.get_v(i + 1),
                    self.get_v(1),
                ]
            ):
                raise ValueError("Controllo dopo traslazione non riuscito")
            self.move_to_midpoint(i - 1)
            self.eliminate_vertex(i - 1)
            return i - 1

    def case_D222(self, i: int) -> int:
        """Svolge le operazioni del caso D222 tornando l'indice da processare."""
        print("Caso D222")
        if self.is_left_turn(2) is True:
            if not self.is_clockwise(
                [
                    self.get_v(2),
                    self.get_v(i + 1),
                    self.get_v(i),
                ]
            ):
                raise ValueError("Non entra in nessun caso")
            # Passaggio 1
            if not self.is_clockwise(
                [
                    self.get_v(i - 2),
                    self.get_v(i + 1),
                    self.get_v(i),
                ]
            ):
                angle = (self.get_next_clockwise(2).angle + 2 * math.pi) / 2
                self.weak_translation_counterclockwise(i - 2, angle)
            if not self.is_clockwise(
                [
                    self.get_v(i - 2),
                    self.get_v(i + 1),
                    self.get_v(i),
                ]
            ):
                raise ValueError("Controllo dopo traslazione non riuscito")
            # Passaggio 2
            if not self.is_clockwise(
                [
                    self.get_v(i - 3),
                    self.get_v(i),
                    self.get_v(i - 1),
                ]
            ):
                angle = (self.get_v(1).angle + self.get_v(i).angle) / 2
                self.weak_translation_counterclockwise(i - 3, angle)
            if not self.is_clockwise(
                [
                    self.get_v(i - 3),
                    self.get_v(i),
                    self.get_v(i - 1),
                ]
            ):
                raise ValueError("Controllo dopo traslazione non riuscito")
            self.move_to_midpoint(i - 1)
            self.eliminate_vertex(i - 1)
            return i - 1
        else:
            if not self.is_counterclockwise(
                [
                    self.get_v(2),
                    self.get_v(i + 1),
                    self.get_v(i),
                ]
            ):
                raise ValueError("Non entra in nessun caso")
            # Passaggio 1
            if not self.is_counterclockwise(
                [
                    self.get_v(i - 2),
                    self.get_v(i + 1),
                    self.get_v(i),
                ]
            ):
                angle = (
                    self.get_next_counterclockwise(2).angle + self.get_v(2).angle
                ) / 2
                self.weak_translation_clockwise(i - 2, angle)
            if not self.is_counterclockwise(
                [
                    self.get_v(i - 2),
                    self.get_v(i + 1),
                    self.get_v(i),
                ]
            ):
                raise ValueError("Controllo dopo traslazione non riuscito")
            # Passaggio 2
            if not self.is_counterclockwise(
                [
                    self.get_v(i - 3),
                    self.get_v(i),
                    self.get_v(i - 1),
                ]
            ):
                angle = (self.get_v(1).angle + self.get_v(i).angle) / 2
                self.weak_translation_clockwise(i - 3, angle)
            if not self.is_counterclockwise(
                [
                    self.get_v(i - 3),
                    self.get_v(i),
                    self.get_v(i - 1),
                ]
            ):
                raise ValueError("Controllo dopo traslazione non riuscito")
            self.move_to_midpoint(i - 1)
            self.eliminate_vertex(i - 1)
            return i - 1

    def reduce_polygonal(self):
        """Esegue l'algoritmo di riduzione di Mehlhorn-Yap sulla poligonale."""
        print("I vertici sono della poligonale da ridurre sono:")
        self.print_vertices
        self.save_state()
        n = len(self.vertices)
        # Casi banali
        if n == 1:
            print("La poligonale è un punto.")
        if n == 2:
            print("La poligonale è un segmento.")
        if n == 3:
            print("La poligonale è un triangolo.")
        # Elimino i vertici appartenenti ai lati
        for i in range(3, n + 1):
            if is_near(self.get_rotation_angle(i), 0):
                self.eliminate_vertex(i)
                print(f"Eliminato vertice {i} perché appartiene già ad un lato.")
        if self.is_polygonal_reduced():
            return None
        if not self.is_circle():
            self.move_to_circle()
            if not self.is_circle():
                raise ValueError("La curva poligonale non è inscritta in un cerchio.")
        # Porto la curva poliginale su circonferenza di raggio 1
        if any(not is_near(math.hypot(v.x, v.y), 1.0) for v in self.vertices):
            self.get_unitary_radius()
        # Inizio l'algoritmo dal quarto vertice
        i = 4
        while self.is_polygonal_reduced() is False:
            # Rimetto i vertici di riferimento apposto ogni volta
            # Porto il vertice v(1) in (-1,0)
            if not is_near(self.get_v(1).x, -1) or not is_near(self.get_v(1).y, 0):
                if self.get_v(1).angle < math.pi:
                    self.weak_translation_counterclockwise(1, math.pi)
                else:
                    self.weak_translation_clockwise(1, math.pi)
                print(
                    f"Ho traslato il vertice di riferimento {self.get_v(1).name} in (-1,0)."
                )
            # Porto il vertice v(2) in (1,0)
            if not is_near(self.get_v(2).x, 1) or not is_near(self.get_v(2).y, 0):
                if self.get_v(2).angle < math.pi:
                    self.weak_translation_clockwise(2, 0)
                else:
                    self.weak_translation_counterclockwise(2, 0)
                print(
                    f"Ho traslato il vertice di riferimento {self.get_v(2).name} in (1,0)."
                )
            print(f"Sto processando il vertice {self.get_v(i).name} con indice {i}.")
            # Caso svolta a destra in 2
            if self.is_right_turn(2):
                # Caso i dispari
                if i % 2 == 1:
                    # Caso A
                    if self.is_left_turn(i - 1):
                        # Caso A1
                        if self.is_right_turn(i):
                            i = self.case_A1(i)
                            continue
                        # Caso A2
                        else:
                            # Caso A21
                            if self.is_counterclockwise(
                                [
                                    self.get_v(i),
                                    self.get_v(i + 1),
                                    self.get_v(2),
                                ]
                            ):
                                i = self.case_A21(i)
                                continue
                            # Caso A22
                            if self.is_counterclockwise(
                                [
                                    self.get_v(i),
                                    self.get_v(2),
                                    self.get_v(i + 1),
                                    self.get_v(1),
                                ]
                            ):
                                i = self.case_A22(i)
                            # Caso A23
                            else:
                                if not self.is_counterclockwise(
                                    [
                                        self.get_v(i),
                                        self.get_v(1),
                                        self.get_v(2),
                                        self.get_v(i + 1),
                                    ]
                                ):
                                    raise ValueError(
                                        "Controllo per caso A23 non riuscito"
                                    )
                                # Caso A231
                                if (
                                    self.is_counterclockwise(
                                        [
                                            self.get_v(i),
                                            self.get_v(1),
                                            self.get_v(i + 2),
                                        ]
                                    )
                                    and (i + 2) % len(self.vertices) != 1
                                ):
                                    i = self.case_A231(i)
                                    continue
                                # Caso A232
                                else:
                                    print("Caso A232")
                                    if not self.is_counterclockwise(
                                        [
                                            self.get_v(i),
                                            self.get_v(i + 2),
                                            self.get_v(1),
                                        ]
                                    ):
                                        raise ValueError(
                                            "Controllo per caso A232 non riuscito"
                                        )
                                    # Caso A2321
                                    if self.is_left_turn(i + 2):
                                        i = self.case_A2321(i)
                                    # Caso A2322
                                    else:
                                        i = self.case_A2322(i)
                    # Caso B
                    else:
                        # Caso B1
                        if self.is_counterclockwise(
                            [
                                self.get_v(i),
                                self.get_v(2),
                                self.get_v(i - 2),
                            ]
                        ):
                            i = self.case_B1(i)
                            continue
                        # Caso B2
                        else:
                            if not self.is_counterclockwise(
                                [
                                    self.get_v(i),
                                    self.get_v(i - 1),
                                    self.get_v(2),
                                ]
                            ):
                                raise ValueError("Controllo per caso B2 non riuscito")
                            # Caso B21
                            if self.is_left_turn(i):
                                i = self.case_B21(i)
                                continue
                            # Caso B22
                            else:
                                # Caso B221
                                if self.is_counterclockwise(
                                    [
                                        self.get_v(i),
                                        self.get_v(i + 1),
                                        self.get_v(1),
                                    ]
                                ):
                                    # Caso B2211
                                    if (
                                        self.is_counterclockwise(
                                            [
                                                self.get_v(i),
                                                self.get_v(i + 2),
                                                self.get_v(2),
                                            ]
                                        )
                                        and not (i + 2) % len(self.vertices) == 2
                                    ):
                                        i = self.case_B2211(i)
                                        continue
                                    # Caso B2212
                                    else:
                                        if not self.is_counterclockwise(
                                            [
                                                self.get_v(2),
                                                self.get_v(i + 2),
                                                self.get_v(i),
                                            ]
                                        ):
                                            raise ValueError("Non entra in nessun caso")
                                        # Caso B22121
                                        if self.is_right_turn(i + 2):
                                            i = self.case_B22121(i)
                                            continue
                                        # Caso B22122
                                        else:
                                            i = self.case_B22122(i)
                                            continue
                                # caso B222
                                else:
                                    if not self.is_counterclockwise(
                                        [
                                            self.get_v(1),
                                            self.get_v(i + 1),
                                            self.get_v(i),
                                        ]
                                    ):
                                        raise ValueError("Non entra in nessun caso")
                                    i = self.case_B222(i)
                                    continue

                # Caso i pari
                elif i % 2 == 0:
                    # Caso C
                    if self.is_left_turn(i - 1):
                        # Caso C1
                        if self.is_right_turn(i):
                            i = self.case_C1(i)
                            continue
                        # Caso C2
                        else:
                            print("Caso C2")
                            # Caso limite j = 4 E22
                            if i == 4:
                                print("C.L. E22")
                                if self.is_counterclockwise(
                                    [self.get_v(4), self.get_v(5), self.get_v(2)]
                                ):
                                    self.move_to_midpoint(3)
                                    self.eliminate_vertex(3)
                                    i -= 1
                                    continue
                                # Permuto gli indici così la poligonale è stellata fino a 4
                                else:
                                    self.permute_vertices_backward()
                                    print(
                                        f"I nuovi riferimenti sono {self.get_v(1).name} e {self.get_v(2).name}."
                                    )
                                    self.weak_translation_counterclockwise(1, math.pi)
                                    self.weak_translation_counterclockwise(2, 0)
                                    continue
                            # Caso C21
                            if self.is_counterclockwise(
                                [
                                    self.get_v(i),
                                    self.get_v(i + 1),
                                    self.get_v(1),
                                ]
                            ):
                                i = self.case_C21(i)
                                continue
                            # Caso C22
                            if self.is_counterclockwise(
                                [
                                    self.get_v(i),
                                    self.get_v(1),
                                    self.get_v(i + 1),
                                    self.get_v(2),
                                ]
                            ):
                                i = self.case_C22(i)
                                continue
                            # Caso C23 (j<2<1<j+1)
                            else:
                                print("Caso C23")
                                if not self.is_counterclockwise(
                                    [
                                        self.get_v(i),
                                        self.get_v(2),
                                        self.get_v(1),
                                        self.get_v(i + 1),
                                    ]
                                ):
                                    raise ValueError(
                                        "Controllo per caso C23 non riuscito, dovrebbe essere vero"
                                    )
                                # Caso C231
                                if self.is_counterclockwise(
                                    [
                                        self.get_v(i),
                                        self.get_v(2),
                                        self.get_v(i + 2),
                                    ]
                                ):
                                    i = self.case_C231(i)
                                    continue
                                # Caso C232
                                else:
                                    if not self.is_counterclockwise(
                                        [
                                            self.get_v(i),
                                            self.get_v(i + 2),
                                            self.get_v(2),
                                        ]
                                    ):
                                        raise ValueError(
                                            "Controllo per caso C232 non riuscito"
                                        )
                                    # Caso C2321
                                    if self.is_left_turn(i + 2):
                                        i = self.case_C2321(i)
                                        continue
                                    # Caso C2322
                                    else:
                                        i = self.case_C2322(i)
                                        continue
                    # Caso D
                    else:
                        # Caso D1
                        if self.is_counterclockwise(
                            [
                                self.get_v(i),
                                self.get_v(1),
                                self.get_v(i - 2),
                            ]
                        ):
                            i = self.case_D1(i)
                            continue
                        # Caso D2
                        else:
                            if not self.is_counterclockwise(
                                [
                                    self.get_v(i),
                                    self.get_v(i - 1),
                                    self.get_v(1),
                                ]
                            ):
                                raise ValueError("Controllo per caso D2 non riuscito")
                            # Caso D21
                            if self.is_left_turn(i):
                                i = self.case_D21(i)
                                continue
                            # Caso D22
                            else:
                                # Caso D221
                                if self.is_counterclockwise(
                                    [
                                        self.get_v(i),
                                        self.get_v(i + 1),
                                        self.get_v(2),
                                    ]
                                ):
                                    # Caso D2211
                                    if (
                                        self.is_counterclockwise(
                                            [
                                                self.get_v(i),
                                                self.get_v(i + 2),
                                                self.get_v(1),
                                            ]
                                        )
                                        and not (i + 2) % len(self.vertices) == 1
                                    ):
                                        i = self.case_D2211(i)
                                        continue
                                    # Caso D2212
                                    else:
                                        if not self.is_counterclockwise(
                                            [
                                                self.get_v(1),
                                                self.get_v(i + 2),
                                                self.get_v(i),
                                            ]
                                        ):
                                            raise ValueError("Non entra in nessun caso")
                                        # Caso D22121
                                        if self.is_right_turn(i + 2):
                                            i = self.case_D22121(i)
                                            continue
                                        # Caso D22122
                                        else:
                                            i = self.case_D22122(i)
                                            continue
                                # caso D222
                                else:
                                    i = self.case_D222(i)
                                    continue
            # Caso svolta a sinistra in 2
            if self.is_left_turn(2):
                # Caso i dispari
                if i % 2 == 1:
                    # Caso A
                    if self.is_right_turn(i - 1):
                        # Caso A1
                        if self.is_left_turn(i):
                            i = self.case_A1(i)
                            continue
                        # Caso A2
                        else:
                            # Caso A21
                            if self.is_clockwise(
                                [
                                    self.get_v(i),
                                    self.get_v(i + 1),
                                    self.get_v(2),
                                ]
                            ):
                                i = self.case_A21(i)
                                continue
                            # Caso A22
                            if self.is_clockwise(
                                [
                                    self.get_v(i),
                                    self.get_v(2),
                                    self.get_v(i + 1),
                                    self.get_v(1),
                                ]
                            ):
                                i = self.case_A22(i)
                                continue
                            # Caso A23
                            else:
                                if not self.is_clockwise(
                                    [
                                        self.get_v(i),
                                        self.get_v(1),
                                        self.get_v(2),
                                        self.get_v(i + 1),
                                    ]
                                ):
                                    raise ValueError("Controllo non riuscito.")
                                # Caso A231
                                if (
                                    self.is_clockwise(
                                        [
                                            self.get_v(i),
                                            self.get_v(1),
                                            self.get_v(i + 2),
                                        ]
                                    )
                                    and (i + 2) % len(self.vertices) != 1
                                ):
                                    i = self.case_A231(i)
                                    continue
                                # Caso A232
                                else:
                                    if not self.is_clockwise(
                                        [
                                            self.get_v(i),
                                            self.get_v(i + 2),
                                            self.get_v(1),
                                        ]
                                    ):
                                        raise ValueError("Controllo non riuscito.")
                                    # Caso A2321
                                    if self.is_right_turn(i + 2):
                                        i = self.case_A2321(i)
                                        continue
                                    # Caso A2322
                                    else:
                                        i = self.case_A2322(i)
                                        continue
                    # Caso B
                    else:
                        # Caso B1
                        if self.is_clockwise(
                            [
                                self.get_v(i),
                                self.get_v(2),
                                self.get_v(i - 2),
                            ]
                        ):
                            # Non facciamo nulla
                            i = self.case_B1(i)
                            continue
                        # Caso B2
                        else:
                            if not self.is_clockwise(
                                [
                                    self.get_v(i),
                                    self.get_v(i - 1),
                                    self.get_v(2),
                                ]
                            ):
                                raise ValueError("Controllo per caso B2 non riuscito.")
                            # Caso B21
                            if self.is_right_turn(i):
                                i = self.case_B21(i)
                                continue
                            # Caso B22
                            else:
                                # Caso B221
                                if self.is_clockwise(
                                    [
                                        self.get_v(i),
                                        self.get_v(i + 1),
                                        self.get_v(1),
                                    ]
                                ):
                                    # Caso B2211
                                    if (
                                        self.is_clockwise(
                                            [
                                                self.get_v(i),
                                                self.get_v(i + 2),
                                                self.get_v(2),
                                            ]
                                        )
                                        and (i + 2) % len(self.vertices) != 2
                                    ):
                                        i = self.case_B2211(i)
                                        continue
                                    # Caso B2212
                                    else:
                                        if not self.is_clockwise(
                                            [
                                                self.get_v(2),
                                                self.get_v(i + 2),
                                                self.get_v(i),
                                            ]
                                        ):
                                            raise ValueError(
                                                "Non entra in nessun caso."
                                            )
                                        # Caso B22121
                                        if self.is_left_turn(i + 2):
                                            i = self.case_B22121(i)
                                            continue
                                        # Caso B22122
                                        else:
                                            i = self.case_B22122(i)
                                            continue
                                # caso B222
                                else:
                                    if not self.is_clockwise(
                                        [
                                            self.get_v(1),
                                            self.get_v(i + 1),
                                            self.get_v(i),
                                        ]
                                    ):
                                        raise ValueError("Non entra in nessun caso.")
                                    i = self.case_B222(i)
                                    continue
                # Caso i pari
                elif i % 2 == 0:
                    # Caso C (Speculare di A)
                    if self.is_right_turn(i - 1):
                        # Caso C1
                        if self.is_left_turn(i):
                            i = self.case_C1(i)
                            continue
                        # Caso C2
                        else:
                            # Caso limite j-2 = 2 E22
                            if i == 4:
                                print("E22")
                                if self.is_clockwise(
                                    [self.get_v(4), self.get_v(5), self.get_v(2)]
                                ):
                                    self.move_to_midpoint(3)
                                    self.eliminate_vertex(3)
                                    i -= 1
                                    continue
                                # Permuto gli indici così la poligonale è stellata fino a 4
                                else:
                                    self.permute_vertices_backward()
                                    print(
                                        f"I nuovi riferimenti sono {self.get_v(1).name} e {self.get_v(2).name}."
                                    )
                                    self.weak_translation_clockwise(1, math.pi)
                                    self.weak_translation_clockwise(2, 0)
                                    continue
                            # Caso C21
                            if self.is_clockwise(
                                [
                                    self.get_v(i),
                                    self.get_v(i + 1),
                                    self.get_v(1),
                                ]
                            ):
                                i = self.case_C21(i)
                                continue
                            # Caso C22
                            if self.is_clockwise(
                                [
                                    self.get_v(i),
                                    self.get_v(1),
                                    self.get_v(i + 1),
                                    self.get_v(2),
                                ]
                            ):
                                i = self.case_C22(i)
                                continue
                            # Caso C23
                            else:
                                if not self.is_clockwise(
                                    [
                                        self.get_v(i),
                                        self.get_v(2),
                                        self.get_v(1),
                                        self.get_v(i + 1),
                                    ]
                                ):
                                    raise ValueError("Controllo non riuscito.")
                                # Caso C231
                                if self.is_clockwise(
                                    [
                                        self.get_v(i),
                                        self.get_v(2),
                                        self.get_v(i + 2),
                                    ]
                                ):
                                    i = self.case_C231(i)
                                    continue
                                # Caso C232
                                else:
                                    if not self.is_clockwise(
                                        [
                                            self.get_v(i),
                                            self.get_v(i + 2),
                                            self.get_v(2),
                                        ]
                                    ):
                                        raise ValueError(
                                            "Controllo per caso C232 non riuscito."
                                        )
                                    # Caso C2321
                                    if self.is_right_turn(i + 2):
                                        i = self.case_C2321(i)
                                        continue
                                    # Caso C2322
                                    else:
                                        i = self.case_C2322(i)
                                        continue
                    # Caso D
                    else:
                        # Caso D1
                        if self.is_clockwise(
                            [
                                self.get_v(i),
                                self.get_v(1),
                                self.get_v(i - 2),
                            ]
                        ):
                            i = self.case_D1(i)
                            continue
                        # Caso D2
                        else:
                            if not self.is_clockwise(
                                [
                                    self.get_v(i),
                                    self.get_v(i - 1),
                                    self.get_v(1),
                                ]
                            ):
                                raise ValueError("Non entra in nessun caso.")
                            # Caso D21
                            if self.is_right_turn(i):
                                i = self.case_D21(i)
                                continue
                            # Caso D22
                            else:
                                # Caso D221
                                if self.is_clockwise(
                                    [
                                        self.get_v(i),
                                        self.get_v(i + 1),
                                        self.get_v(2),
                                    ]
                                ):
                                    # Caso D2211
                                    if (
                                        self.is_clockwise(
                                            [
                                                self.get_v(i),
                                                self.get_v(i + 2),
                                                self.get_v(1),
                                            ]
                                        )
                                        and (i + 2) % len(self.vertices) != 1
                                    ):
                                        i = self.case_D2211(i)
                                        continue
                                    # Caso D2212
                                    else:
                                        print("Caso D2212")
                                        if not self.is_clockwise(
                                            [
                                                self.get_v(1),
                                                self.get_v(i + 2),
                                                self.get_v(i),
                                            ]
                                        ):
                                            raise ValueError("Non entra in nessun caso")
                                        # Caso D22121
                                        if self.is_left_turn(i + 2):
                                            print("Caso D22121")
                                            self.move_to_midpoint(i + 1)
                                            self.eliminate_vertex(i + 1)
                                            self.move_to_midpoint(i)
                                            self.eliminate_vertex(i)
                                            continue
                                        # Caso D22122
                                        else:
                                            i = self.case_D22122(i)
                                            continue
                                # caso D222
                                else:
                                    i = self.case_D222(i)
                                    continue
        self.get_equispaced_vertices()


def generate_random_polygonal(number_vertices: int) -> Polygonal:
    """Genera una poligonale casuale con number_vertices vertici sulla circonferenza unitaria."""
    vertices = []
    for i in range(1, number_vertices + 1):
        # Genera coordinate casuali tra -1 e 1
        x = random.uniform(-1, 1)
        y = math.sqrt(1 - x**2) * random.choice([1, -1])
        vertices.append(Vertex(f"v{i}", x, y))

    return Polygonal(vertices)
