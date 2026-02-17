import math


class Vertice:
    def __init__(self, nome, x, y):
        self.nome = nome  # Es: "v1", "v2"
        self.x = float(x)
        self.y = float(y)
        # Calcolo automatico dell'angolo (ex theta)
        # atan2 gestisce correttamente i quadranti (-PI a +PI)
        self.angolo = math.atan2(self.y, self.x)

    def cambio_coordinate(self, x, y):
        """
        Sposta il vertice a nuove coordinate (x, y) 
        e ricalcola l'angolo automaticamente.
        """
        self.x = x
        self.y = y
        self.angolo = math.atan2(y, x)

    def cambio_angolo(self, nuovo_angolo):
        """
        Sposta il vertice sulla circonferenza unitaria (R=1) 
        in base al nuovo angolo fornito.
        """
        self.angolo = nuovo_angolo
        self.x = math.cos(nuovo_angolo)
        self.y = math.sin(nuovo_angolo)


origine = Vertice("origine", 0, 0)

# Il poligono è una lista di vertici.


class Poligono:
    def __init__(self, vertici=None):
        if vertici is None:
            self.vertici = []
        else:
            self.vertici = vertici  # Lista di oggetti Vertice

    # Per inizializzare un poligono (diverso da T_0 !)
    def aggiungi_vertice(self, v):
        self.vertici.append(v)

    # Restituisce il vertice i-esimo (1-based)
    def v(self, i):
        n = len(self.vertici)
        if n == 0:
            return None  # Gestione caso poligono vuoto
        indice_modulato = (i-1) % n
        return self.vertici[indice_modulato]

    def calcola_angolo_di_rotazione(self, i):
        """
        Calcola l'angolo di rotazione necessario per spostare v_i in v_{i+1}.
        """
        v_i = self.v(i)
        v_ip1 = self.v(i+1)
        v_im1 = self.v(i-1)

        valore_assoluto_rot_vi = math.arccos(((v_i.x-v_im1.x) * (v_ip1.x-v_i.x) + (v_i.y-v_im1.y) * (v_ip1.y-v_i.y)) / (
            math.sqrt((v_i.x-v_im1.x)**2 + (v_i.y-v_im1.y)**2) * math.sqrt((v_ip1.x-v_i.x)**2 + (v_ip1.y-v_i.y)**2)))
        determinante = (v_ip1.x - v_i.x) * (v_i.y - v_im1.y) - \
            (v_ip1.y - v_i.y) * (v_i.x - v_im1.x)
        rot_vi = math.copysign(valore_assoluto_rot_vi, determinante)
        return rot_vi

    def calcola_numero_di_avvolgimento(self, i):
        somma_rotazioni = 0
        for i in range(1, len(self.vertici)):
            rot_vi = self.calcola_angolo_di_rotazione(i)
            somma_rotazioni = somma_rotazioni + rot_vi
        numero_di_avvolgimento = somma_rotazioni / (2 * math.pi)
        return numero_di_avvolgimento

    def verifica_svolta_a_sinistra(self, i):
        if self.calcola_angolo_di_rotazione(i) > 0:
            return True
        else:
            return False

    def verifica_regolarita_traslazione(self, i, vertice):
        """
        Verifica se il vertice non appartiene ai coni interdetti di v_i.
        """
        v_i = self.v(i)
        v_im1 = self.v(i-1)
        v_ip1 = self.v(i+1)
        v_im2 = self.v(i-2)
        v_ip2 = self.v(i+2)

        def appartiene_al_cono(v, p, o, a, b):
            """
            Verifica se il vertice p appartiene al cono tra a e b, con origine o contenente v.
            """
            def det(u_x, u_y, v_x, v_y):
                return u_x * v_y - u_y * v_x

            # Vettori OA, OB e OV
            OA_x = a.x - o.x
            OA_y = a.y - o.y
            OB_x = b.x - o.x
            OB_y = b.y - o.y
            OV_x = v.x - o.x
            OV_y = v.y - o.y
            OP_x = p.x - o.x
            OP_y = p.y - o.y

            # Calcola i determinanti per verificare la posizione di OV rispetto a OA e OB
            det_OA_OB = det(OA_x, OA_y, OB_x, OB_y)
            det_OA_OV = det(OA_x, OA_y, OV_x, OV_y)
            det_OB_OV = det(OB_x, OB_y, OV_x, OV_y)
            det_OA_OP = det(OA_x, OA_y, OP_x, OP_y)
            det_OB_OP = det(OB_x, OB_y, OP_x, OP_y)

            # Caso cono convesso
            if det_OA_OV*det_OA_OB < 0:
                if det_OA_OP < 0
                return True

            # Caso cono concavo
            if det_OA_OV*det_OA_OB > 0:

    def centra_poligono(self):
        """
        Centra il poligono spostando tutti i vertici in modo che il centro di massa sia nell'origine (0, 0).
        """
        n = len(self.vertici)
        if n == 0:
            return  # Gestione caso poligono vuoto

        # Calcola il centro di massa
        centro_x = sum(v.x for v in self.vertici) / n
        centro_y = sum(v.y for v in self.vertici) / n

        # Sposta ogni vertice in modo che il centro di massa sia all'origine
        for v in self.vertici:
            v.cambio_coordinate(v.x - centro_x, v.y - centro_y)

    def trasla_vertici_su_circonferenza_unitaria(self):
        raggio = max(math.hypot(v.x, v.y) for v in self.vertici)
        if raggio == 0:
            return  # Gestione caso poligono con tutti i vertici all'origine

        def trasla_vertice_su_circonferenza(i):
            # Se la proiezione non appartiene al cono interdetto, proietta il vertice sulla circonferenza
            v = self.v(i)
            proiezione_v = Vertice("proiezione_v", 0, 0)
            proiezione_v_angolo = v.angolo
            proiezione_v.x = raggio * math.cos(proiezione_v_angolo)
            proiezione_v.y = raggio * math.sin(proiezione_v_angolo)

            if verifica_regolarita_traslazione(i, proiezione_v) == True:
                return v.cambio_coordinate(proiezione_v.x, proiezione_v.y)
            else:
                # Calcolo punto medio dell'arco tra v_im1 e v_ip2
                v_im1 = self.v(i-1)
                v_ip2 = self.v(i+2)
                punto_medio_arco = Vertice("punto_medio_arco", 0, 0)
                punto_medio_arco_angolo = (v_im1.angolo + v_ip2.angolo) / 2
                punto_medio_arco.x = raggio * math.cos(punto_medio_arco_angolo)
                punto_medio_arco.y = raggio * math.sin(punto_medio_arco_angolo)
                if verifica_regolarita_traslazione(i, punto_medio_arco) == True:
                    return v.cambio_coordinate(punto_medio_arco.x, punto_medio_arco.y)
                # Calcolo punto medio dell'arco tra v_im2 e v_ip1
                v_im2 = self.v(i-2)
                v_ip1 = self.v(i+1)
                punto_medio_arco2 = Vertice("punto_medio_arco2", 0, 0)
                punto_medio_arco2_angolo = (v_im2.angolo + v_ip1.angolo) / 2
                punto_medio_arco2.x = raggio * \
                    math.cos(punto_medio_arco2_angolo)
                punto_medio_arco2.y = raggio * \
                    math.sin(punto_medio_arco2_angolo)
                if verifica_regolarita_traslazione(i, punto_medio_arco2) == True:
                    return v.cambio_coordinate(punto_medio_arco2.x, punto_medio_arco2.y)
        for i in range(1, len(self.vertici)):
            trasla_vertice_su_circonferenza(i)

        # Normalizza le coordinate dei vertici sulla circonferenza unitaria
        for i in range(1, len(self.vertici)):
            x = self.v(i).x
            y = self.v(i).y
            norma = math.hypot(x, y)
            self.v(i).cambio_coordinate(x/norma, y/norma)

    # Funzionale solo se i vertici apartengono ad una circonferenza
    def verifica_ordine_ciclico(self, lista_vertici):
        n = len(lista_vertici)
        if n <= 2:
            return True
        # Verifica se la lista di vertici è ordinata in senso orario
        for i in range(1, n):
            v_i = lista_vertici[i-1]
            v_ip1 = lista_vertici[i]
            determinante = (v_i.x * v_ip1.y - v_i.y * v_ip1.x)
            if determinante > 0:
                return False
        else:
            return True

    # Funzione per traslare i vertici del poligono su circonferenza unitaria


# Poligono di prova
Poligono1 = Poligono((Vertice("v1", 1, 0), Vertice(
    "v2", 0, 1), Vertice("v3", -1, 0), Vertice("v4", 0, -1)))
