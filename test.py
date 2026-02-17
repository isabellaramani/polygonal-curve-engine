import math
from poligoni_stellati import Vertice

TOLERANCE = 0.0005

def is_near(a, b):
    return math.fabs(a - b) < TOLERANCE

def test_cambio_coordinate():
    V = Vertice("v", 0.5, 0.2)
    V.cambio_coordinate(1, 2)
    assert is_near(V.x, 1)
    assert is_near(V.y, 2)
    assert is_near(V.angolo, math.atan2(2, 1))
