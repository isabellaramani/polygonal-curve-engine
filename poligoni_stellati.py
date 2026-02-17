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

        # Cono interdetto relativo a v_i in v_im1
        def orientazione_di_v_risp_a_v1_v2(v, v1, v2):
            # Calcola il determinante per determinare l'orientamento
            det = (v1.x - v.x) * (v2.y - v.y) - (v1.y - v.y) * (v2.x - v.x)
            return det

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

    def trasla_vertici_su_circonferenza(self):
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
        for i in range(1, len(self.vertici)+1):
            trasla_vertice_su_circonferenza(i)


# Poligono di prova
Poligono1 = Poligono((Vertice("v1", 1, 0), Vertice(
    "v2", 0, 1), Vertice("v3", -1, 0), Vertice("v4", 0, -1)))
