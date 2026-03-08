import math
import copy

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


def get_determinant(V1: Vertex, V2: Vertex, V3: Vertex, V4: Vertex) -> float:
    """Calcola il determinante dei vettori V1-V2 e V3-V4."""
    return (V1.x - V2.x) * (V3.y - V4.y) - (V1.y - V2.y) * (V3.x - V4.x)


origine = Vertex("Origine", 0, 0)


class Polygon:
    def __init__(self, vertices: list[Vertex] = None) -> None:
        """Inizializza un poligono come una lista di vertici.

        Se non viene fornita una lista di vertici
        inizializza un poligono vuoto.
        """
        if vertices is None:
            self.vertices = []
        else:
            self.vertices = vertices
        self.history = []

    def save_state(self) -> None:
        """Salva lo stato attuale del poligono nella cronologia."""
        self.history.append(copy.deepcopy(self.vertices))

    def is_empty(self) -> bool:
        """Verifica se il poligono è vuoto."""
        return len(self.vertices) == 0

    def add_vertex(self, V: Vertex) -> None:
        """Aggiunge un vertice al poligono."""
        self.vertices.append(V)

    def get_v(self, i: int) -> Vertex:
        """Restituisce il vertice v_i, con i che parte da 1."""
        n = len(self.vertices)
        # Gestisce il caso poligono vuoto.
        if n == 0:
            return None
        return self.vertices[(i - 1) % n]

    def eliminate_vertex(self, i: int) -> None:
        """Elimina il vertice i-esimo se appartiene
        al segmento [v_im1,vip1]."""
        v_im1 = self.get_v(i - 1)
        v_i = self.get_v(i)
        v_ip1 = self.get_v(i + 1)
        # controllo se i vettori sono
        # allineati con il determinante
        det = get_determinant(v_im1, v_i, v_ip1, v_i)
        # Controllo se il punto è interno al segmento
        is_between_x = min(v_im1.x, v_ip1.x) <= v_i.x <= max(v_im1.x, v_ip1.x)
        is_between_y = min(v_im1.y, v_ip1.y) <= v_i.y <= max(v_im1.y, v_ip1.y)

        if is_near(det, 0.0) and is_between_x and is_between_y:
            self.vertices.remove(v_i)
        else:
            raise ValueError("Il vertice non appartiene al segmento.")

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

        # Calcolo prodotto scalare.
        dot_product = vec1_x * vec2_x + vec1_y * vec2_y
        norm_1 = math.sqrt(vec1_x**2 + vec1_y**2)
        norm_2 = math.sqrt(vec2_x**2 + vec2_y**2)

        abs_value_rot_vi = math.acos(dot_product / (norm_1 * norm_2))
        det = vec1_x * vec2_y - vec1_y * vec2_x
        rot_vi = math.copysign(abs_value_rot_vi, det)
        return rot_vi

    def get_winding_number(self) -> int:
        """Calcola l'indice di avvolgimento del poligono."""
        sum_rotation_angles = 0
        # Calcola la somma degli angoli di rotazione
        # per tutti i vertici del poligono.
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

    def center_polygon(self) -> None:
        """Centra il poligono spostando tutti i vertici
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

    def is_circle(self) -> bool:
        """Verifica se i vertici del poligono appartengono
        ad una circonferenza."""
        n = len(self.vertices)
        if n < 3:
            return False  # Almeno 3 punti per definire una circonferenza

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
            # Devo risolvere il sistema di equazioni:
            # y - M_12.y = m_perp_12 * (x - M_12.x)
            # y - M_23.y = m_perp_23 * (x - M_23.x)
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
        """Porta tutti i vertici di un poligono già su una
        circonferenza su circonferenza unitaria."""
        if self.is_circle() is False:
            raise ValueError("I vertici non appartengono ad una circonferenza.")
        for v in self.vertices:
            v.change_coordinates(
                v.x / math.sqrt(v.x**2 + v.y**2), v.y / math.sqrt(v.x**2 + v.y**2)
            )

    def is_clockwise(self, list_vertices: list[Vertex]) -> bool:
        """Verifica se i vertici sulla circonferenza unitaria
        sono ordinati in senso orario
        (accetta anche vertici non distinti)."""
        if self.is_circle() is False:
            raise ValueError("I vertici non appartengono ad una circonferenza.")

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
        """Verifica se i vertici sulla circonferenza unitaria
        sono ordinati in senso antiorario
        (accetta anche vertici non distinti)."""
        if self.is_circle() is False:
            raise ValueError("I vertici non appartengono ad una circonferenza.")

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
            if diff < 0 and not is_near(diff, 2 * math.pi):
                return False
            # Gestisco il caso in cui il vertice è vicino al vertice base

        return True

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
        """Equidistanza i vertici del poligono sulla circonferenza"""
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

    def rotate_vertex(self, i: int, delta_angle: float) -> None:
        """Ruota il vertice i rispetto all'origine spostandolo di
        'delta_angle'. Un delta positivo ruota in senso antiorario,
        negativo in senso orario."""
        # Calcoliamo il nuovo angolo sommandolo a quello attuale
        new_angle = (self.get_v(i).angle + delta_angle) % (2 * math.pi)
        self.get_v(i).change_angle(new_angle)

    def is_translation_regular(self, i: int, U: Vertex) -> bool:
        """Verifica se la traslazione del vertice
        i-esimo in un punto è regolare."""
        V_im2 = self.get_v(i - 2)
        V_im1 = self.get_v(i - 1)
        V_i = self.get_v(i)
        V_ip1 = self.get_v(i + 1)
        V_ip2 = self.get_v(i + 2)

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
        estremi il vertice precedente e quello successivo."""
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

    def move_and_eliminate(self, i: int) -> None:
        self.move_to_midpoint(i)
        self.eliminate_vertex(i)

    def weak_translation_clockwise(self, i: int, target_angle: float) -> None:
        """Trasla il vertice i-esimo lungo la circonferenza unitaria
        in senso orario fino all'angolo target_angle preservando ordine
        e regolarità traslando tutti i vertici collegati
        (vedi lemma 2.12)."""

        if self.is_circle() is False:
            raise ValueError("I vertici non appartengono ad una circonferenza.")

        target_x = math.cos(target_angle)
        target_y = math.sin(target_angle)
        target = Vertex("Target", target_x, target_y)

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

        # Vertici del poligono e target ordinati
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

        for idx, v in enumerate(active_vertices_in_A):
            k = idx + 1
            angle_v = (v_base.angle + diff_angle * k / M) % (2 * math.pi)
            v_x = math.cos(angle_v)
            v_y = math.sin(angle_v)
            v.change_coordinates(v_x, v_y)

    def weak_translation_counterclockwise(self, i: int, target_angle: float) -> None:
        """Trasla il vertice i-esimo lungo la circonferenza unitaria
        in senso orario fino all'angolo target_angle preservando ordine
        e regolarità traslando tutti i vertici collegati
        (vedi lemma 2.12)."""

        if self.is_circle() is False:
            raise ValueError("I vertici non appartengono ad una circonferenza.")

        target_x = math.cos(target_angle)
        target_y = math.sin(target_angle)
        target = Vertex("Target", target_x, target_y)

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

        # Vertici del poligono e target ordinati
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

        for idx, v in enumerate(active_vertices_in_A):
            k = idx + 1
            angle_v = (v_base.angle - diff_angle * k / M) % (2 * math.pi)
            v_x = math.cos(angle_v)
            v_y = math.sin(angle_v)
            v.change_coordinates(v_x, v_y)
        print([v.angle for v in self.vertices])
