import math

# Classe per rappresentare un vertice con etichetta, coordinate e angolo


class Vertice:
    def __init__(self, nome, x, y):
        self.nome = nome  # Nome del vertice, ad esempio: "v1", "v2"
        self.x = float(x)
        self.y = float(y)
        # Calcolo dell'angolo del vertice su circonferenza unitaria (mantiene l'informazione del quadrante)
        self.theta = math.atan2(self.y, self.x)

    # Metodo per cambiare le coordinate del vertice e aggiornare l'angolo di conseguenza
    def cambio_coordinate(self, x, y):
        self.x = x
        self.y = y
        self.theta = math.atan2(y, x)

    # Metodo per cambiare l'angolo del vertice e aggiornare le coordinate di conseguenza
    def cambio_angolo(self, theta):
        self.theta = theta
        self.x = math.cos(theta)
        self.y = math.sin(theta)

    def __repr__(self):
        return f"{self.nome}({self.x:.2f}, {self.y:.2f})"

    # test github
