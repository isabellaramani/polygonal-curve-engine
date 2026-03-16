import math
import pytest
from poligonali_stellate import Vertex, Polygonal

TOLERANCE = 0.0005


def is_near(a, b):
    return math.fabs(a - b) < TOLERANCE


def test_change_coordinates():
    V = Vertex("v", 0.5, 0.2)
    V.change_coordinates(1, 2)
    assert is_near(V.x, 1)
    assert is_near(V.y, 2)
    assert is_near(V.angle, math.atan2(2, 1))


def test_change_angle():
    V = Vertex("v", 1.5, 2.3)
    V.change_angle(math.pi / 4)
    assert is_near(V.angle, math.pi / 4)
    assert is_near(V.x, math.cos(math.pi / 4))
    assert is_near(V.y, math.sin(math.pi / 4))


def test_save_state():
    v1 = Vertex("v1", 0, 0)
    v2 = Vertex("v2", 1, 1)
    P = Polygonal([v1, v2])
    assert len(P.history) == 1
    P.save_state()
    assert len(P.history) == 2
    assert P.history[1][0].name == "v1"
    assert P.history[1][0].x == 0
    assert P.history[1][1].y == 1


def test_is_empty():
    P_1 = Polygonal()
    assert P_1.is_empty()
    P_2 = Polygonal([Vertex("V", 1, 1)])
    assert not P_2.is_empty()


def test_get_v_i():
    P = Polygonal(
        [Vertex("V1", 5.6, 2.9), Vertex("V2", 3.2, 4.1), Vertex("V3", 7.6, 1.8)]
    )
    assert P.get_v(2).name == "V2"
    assert is_near(P.get_v(2).x, 3.2)
    assert is_near(P.get_v(2).y, 4.1)


def test_add_vertex():
    P = Polygonal()
    v = Vertex("V", 1, 2)
    P.add_vertex(v)
    assert len(P.vertices) == 1
    assert is_near(P.vertices[0].x, v.x)
    assert is_near(P.vertices[0].y, v.y)


def test_eliminate_vertex():
    P_1 = Polygonal([Vertex("V1", 1, 0), Vertex("V2", 0, 0), Vertex("V3", -4, 0)])
    P_1.eliminate_vertex(2)
    assert len(P_1.vertices) == 2
    P_2 = Polygonal([Vertex("V1", 0, 0), Vertex("V2", 1, 2), Vertex("V3", 2, 4)])
    P_2.eliminate_vertex(2)
    assert len(P_2.vertices) == 2


def test_get_rotation_angle():
    P = Polygonal(
        [
            Vertex("V1", 1.3, 2.1),
            Vertex("V2", 2.7, 3.9),
            Vertex("V3", 4.9, 1.5),
            Vertex("V4", 0.5, 0.8),
            Vertex("V5", 3.5, 1.8),
        ]
    )
    rot_angle = P.get_rotation_angle(2)
    # Calcolo vettori V2->V1 e V3->V2
    vec1_x = P.get_v(2).x - P.get_v(1).x
    vec1_y = P.get_v(2).y - P.get_v(1).y
    vec2_x = P.get_v(3).x - P.get_v(2).x
    vec2_y = P.get_v(3).y - P.get_v(2).y
    # Calcolo prodotto scalare e norme
    dot_product = vec1_x * vec2_x + vec1_y * vec2_y
    norm_1 = math.sqrt(vec1_x**2 + vec1_y**2)
    norm_2 = math.sqrt(vec2_x**2 + vec2_y**2)
    abs_value_rot_vi = math.acos(dot_product / (norm_1 * norm_2))
    det = vec1_x * vec2_y - vec1_y * vec2_x
    expected_angle = math.copysign(abs_value_rot_vi, det)
    assert is_near(rot_angle, expected_angle)


def test_get_winding_number():
    # Poligonale a farfalla (winding number = 0)
    P = Polygonal(
        [
            Vertex("V1", -1.4, -1.2),
            Vertex("V2", 1.7, 1.6),
            Vertex("V3", 1.3, -1.4),
            Vertex("V4", -1.5, 1.9),
        ]
    )
    winding_number = P.get_winding_number()
    expected_sum = (
        P.get_rotation_angle(1)
        + P.get_rotation_angle(2)
        + P.get_rotation_angle(3)
        + P.get_rotation_angle(4)
    )
    expected_winding_number = expected_sum / (2 * math.pi)
    assert is_near(winding_number, expected_winding_number)


def test_is_left_turn():
    P = Polygonal([Vertex("V1", 3.4, 0), Vertex("V2", 1, 0), Vertex("V3", 1, -1)])
    assert P.is_left_turn(2)
    P_2 = Polygonal(
        [
            Vertex("V1", -math.sqrt(3) / 2, 0.5),
            Vertex("V2", math.sqrt(3) / 2, 0.5),
            Vertex("V3", -math.sqrt(2) / 2, math.sqrt(2) / 2),
            Vertex("V4", math.sqrt(2) / 2, math.sqrt(2) / 2),
            Vertex("V5", 0, 1),
        ]
    )
    assert P_2.is_left_turn(4)


def test_is_right_turn():
    P = Polygonal([Vertex("V1", 3.4, 0), Vertex("V2", 1, 0), Vertex("V3", 1, 1)])
    assert P.is_right_turn(2)
    P_2 = Polygonal(
        [
            Vertex("V1", -math.sqrt(3) / 2, 0.5),
            Vertex("V2", math.sqrt(3) / 2, 0.5),
            Vertex("V3", -math.sqrt(2) / 2, math.sqrt(2) / 2),
            Vertex("V4", math.sqrt(2) / 2, math.sqrt(2) / 2),
            Vertex("V5", 0, 1),
        ]
    )
    assert P_2.is_right_turn(3)


def test_center_Polygonal():
    P = Polygonal(
        [Vertex("V1", 1.5, 2.4), Vertex("V2", 3.6, 4.1), Vertex("V3", 2.7, 9.8)]
    )
    coords = [(1.5, 2.4), (3.6, 4.1), (2.7, 9.8)]
    # Calcolo centro
    center_x = (1.5 + 3.6 + 2.7) / 3
    center_y = (2.4 + 4.1 + 9.8) / 3
    P.center_polygonal()
    for i in range(1, 4):
        expected_x = coords[i - 1][0] - center_x
        expected_y = coords[i - 1][1] - center_y
        assert is_near(P.get_v(i).x, expected_x)
        assert is_near(P.get_v(i).y, expected_y)


def test_is_circle():
    P_1 = Polygonal(
        [
            Vertex("V1", 1, 0),
            Vertex("V2", 0, 1),
            Vertex("V3", -1, 0),
            Vertex("V4", 0, -1),
        ]
    )
    assert P_1.is_circle()
    P_2 = Polygonal(
        [
            Vertex("V1", 1, 0),
            Vertex("V2", 0, 1),
            Vertex("V3", -1, 0),
            Vertex("V4", 0, 0.8),
            Vertex("V5", 0.5, 0.5),
        ]
    )
    assert not P_2.is_circle()
    P_3 = Polygonal(
        [
            Vertex("V1", 0.5, 0),
            Vertex("V2", -0.9, 1.5),
            Vertex("V3", -1.9, 3),
            Vertex("V4", -10.7, 37.5),
        ]
    )
    assert not P_3.is_circle()


def test_get_unitary_radius():
    P = Polygonal(
        [
            Vertex("V1", 2, 0),
            Vertex("V2", 0, 2),
            Vertex("V3", -2, 0),
            Vertex("V4", 0, -2),
        ]
    )
    P.get_unitary_radius()
    for v in P.vertices:
        assert is_near(math.sqrt(v.x**2 + v.y**2), 1)


def test_is_clockwise():
    P_1 = Polygonal(
        [
            Vertex("V1", -1, 0),
            Vertex("V2", math.sqrt(3) / 2, 0.5),
            Vertex("V3", 1, 0),
            Vertex("V4", 0, -1),
        ]
    )
    assert P_1.is_clockwise(P_1.vertices)
    P_2 = Polygonal(
        [Vertex("V1", 0.5, math.sqrt(3) / 2), Vertex("V2", -1, 0), Vertex("V3", 0, 1)]
    )
    assert P_2.is_clockwise(P_2.vertices)
    P_3 = Polygonal(
        [Vertex("V1", 0.5, math.sqrt(3) / 2), Vertex("V2", -1, 0), Vertex("V3", 0, -1)]
    )
    assert not P_3.is_clockwise(P_3.vertices)
    P_4 = Polygonal(
        [
            Vertex("V1", -1, 0),
            Vertex("V2", math.sqrt(3) / 2, 0.5),
            Vertex("V3", 1, 0),
            Vertex("V4", 0, -1),
            Vertex("V5", 0, -1),
        ]
    )
    assert P_4.is_clockwise(P_4.vertices)
    P_5 = Polygonal([Vertex("V1", -1, 0), Vertex("V2", -1, 0), Vertex("V3", 0, -1)])
    assert P_5.is_clockwise(P_5.vertices)
    P_6 = Polygonal(
        [
            Vertex("v1", -1, 0),
            Vertex("v2", 1, 0),
            Vertex("v3", -0.707107, 0.707107),
            Vertex("v4", 0.707107, -0.707107),
            Vertex("v5", 0.707107, 0.707107),
            Vertex("v6", 0, -1),
            Vertex("v7", -0.866025, -0.5),
            Vertex("v8", 0, 1),
        ]
    )
    assert P_6.is_clockwise([P_6.get_v(7), P_6.get_v(8), P_6.get_v(2)])
    assert P_6.is_clockwise([P_6.get_v(7), P_6.get_v(8), P_6.get_v(5)])
    P_7 = Polygonal(
        [
            Vertex("v1", -1, 0),
            Vertex("v2", 1, 0),
            Vertex("v3", 0, 1),
            Vertex("v4", 0, -1),
            Vertex("v5", 0.707107, -0.707107),
            Vertex("v6", 0.5, -0.866025),
        ]
    )
    assert P_7.is_clockwise([P_7.get_v(2), P_7.get_v(2), P_7.get_v(5)])
    P_8 = Polygonal(
        [
            Vertex("v1", -0.866025, 0.5),
            Vertex("v2", 0.866025, 0.5),
            Vertex("v3", 0, 1),
            Vertex("v4", 0.707107, -0.707107),
            Vertex("v5", -0.707107, -0.707107),
            Vertex("v6", 0, -1),
        ]
    )
    assert not P_8.is_clockwise([P_8.get_v(5), P_8.get_v(6), P_8.get_v(1)])


def test_is_counterclockwise():
    P_1 = Polygonal(
        [
            Vertex("V1", -1, 0),
            Vertex("V2", math.sqrt(3) / 2, 0.5),
            Vertex("V3", 1, 0),
            Vertex("V4", 0, -1),
        ]
    )
    assert not P_1.is_counterclockwise(P_1.vertices)
    P_2 = Polygonal(
        [Vertex("V1", 0.5, math.sqrt(3) / 2), Vertex("V2", -1, 0), Vertex("V3", 0, 1)]
    )
    assert not P_2.is_counterclockwise(P_2.vertices)
    P_3 = Polygonal(
        [Vertex("V1", 0.5, math.sqrt(3) / 2), Vertex("V2", -1, 0), Vertex("V3", 0, -1)]
    )
    assert P_3.is_counterclockwise(P_3.vertices)
    P_4 = Polygonal(
        [
            Vertex("V1", -1, 0),
            Vertex("V2", math.sqrt(3) / 2, 0.5),
            Vertex("V3", 1, 0),
            Vertex("V4", 0, -1),
            Vertex("V5", 0, -1),
        ]
    )
    assert not P_4.is_counterclockwise(P_4.vertices)
    P_5 = Polygonal([Vertex("V1", -1, 0), Vertex("V2", -1, 0), Vertex("V3", 0, -1)])
    assert P_5.is_counterclockwise(P_5.vertices)


def test_sort_vertices_clockwise():
    P_1 = Polygonal(
        [
            Vertex("V1", 0, 1),
            Vertex("V2", 1, 0),
            Vertex("V3", 0, -1),
            Vertex("V4", -1, 0),
        ]
    )
    list_1 = [
        Vertex("V4", -1, 0),
        Vertex("V2", 1, 0),
        Vertex("V3", 0, -1),
        Vertex("V1", 0, 1),
    ]
    sorted_vertices_1 = P_1.sort_vertices_clockwise(list_1)
    expected_order_1 = ["V4", "V1", "V2", "V3"]
    for v, expected_name in zip(sorted_vertices_1, expected_order_1):
        assert v.name == expected_name
    P_2 = Polygonal(
        [
            Vertex("V1", 4, 0),
            Vertex("V2", -4, 0),
            Vertex("V3", 0, 4),
            Vertex("V4", 0, -4),
            Vertex("V5", 2 * math.sqrt(2), 2 * math.sqrt(2)),
            Vertex("V6", -2 * math.sqrt(2), 2 * math.sqrt(2)),
        ]
    )
    list_2 = [P_2.get_v(4), P_2.get_v(5), P_2.get_v(1), P_2.get_v(2)]
    sorted_vertices_2 = P_2.sort_vertices_clockwise(list_2)
    expected_order_2 = ["V4", "V2", "V5", "V1"]
    for v, expected_name in zip(sorted_vertices_2, expected_order_2):
        assert v.name == expected_name
    list_3 = [P_2.get_v(4), P_2.get_v(6), P_2.get_v(2), P_2.get_v(3), P_2.get_v(1)]
    sorted_vertices_3 = P_2.sort_vertices_clockwise(list_3)
    expected_order_3 = ["V4", "V2", "V6", "V3", "V1"]
    for v, expected_name in zip(sorted_vertices_3, expected_order_3):
        assert v.name == expected_name


def test_sort_vertices_counterclockwise():
    P_1 = Polygonal(
        [
            Vertex("V1", 0, 1),
            Vertex("V2", 1, 0),
            Vertex("V3", 0, -1),
            Vertex("V4", -1, 0),
        ]
    )
    list_1 = [
        Vertex("V4", -1, 0),
        Vertex("V2", 1, 0),
        Vertex("V3", 0, -1),
        Vertex("V1", 0, 1),
    ]
    sorted_vertices_1 = P_1.sort_vertices_counterclockwise(list_1)
    expected_order_1 = ["V4", "V3", "V2", "V1"]
    for v, expected_name in zip(sorted_vertices_1, expected_order_1):
        assert v.name == expected_name
    P_2 = Polygonal(
        [
            Vertex("V1", 4, 0),
            Vertex("V2", -4, 0),
            Vertex("V3", 0, 4),
            Vertex("V4", 0, -4),
            Vertex("V5", 2 * math.sqrt(2), 2 * math.sqrt(2)),
            Vertex("V6", -2 * math.sqrt(2), 2 * math.sqrt(2)),
        ]
    )
    list_2 = [P_2.get_v(4), P_2.get_v(5), P_2.get_v(1), P_2.get_v(2)]
    sorted_vertices_2 = P_2.sort_vertices_counterclockwise(list_2)
    expected_order_2 = ["V4", "V1", "V5", "V2"]
    for v, expected_name in zip(sorted_vertices_2, expected_order_2):
        assert v.name == expected_name
    list_3 = [P_2.get_v(4), P_2.get_v(6), P_2.get_v(2), P_2.get_v(3), P_2.get_v(1)]
    sorted_vertices_3 = P_2.sort_vertices_counterclockwise(list_3)
    expected_order_3 = ["V4", "V1", "V3", "V6", "V2"]
    for v, expected_name in zip(sorted_vertices_3, expected_order_3):
        assert v.name == expected_name


def test_get_equispaced_vertices():
    P = Polygonal(
        [
            Vertex("V1", 1, 0),
            Vertex("V2", 1 / 2, math.sqrt(3) / 2),
            Vertex("V3", -1, 0),
            Vertex("V4", math.sqrt(2) / 2, math.sqrt(2) / 2),
        ]
    )
    P.get_equispaced_vertices()
    expected_angles = [0, math.pi, 3 * math.pi / 2, math.pi / 2]
    for v, expected_angle in zip(P.vertices, expected_angles):
        assert is_near(v.angle, expected_angle)


def test_get_equispaced_vertices_fixed_12():
    P = Polygonal(
        [
            Vertex("V1", -1, 0),
            Vertex("V2", 1, 0),
            Vertex("V3", 1 / 2, math.sqrt(3) / 2),
            Vertex("V4", math.sqrt(2) / 2, math.sqrt(2) / 2),
        ]
    )
    P.get_equispaced_vertices_fixed_12()
    expected_angles = [math.pi, 0, 2 * math.pi / 3, math.pi / 3]
    for v, expected_angle in zip(P.vertices, expected_angles):
        assert is_near(v.angle, expected_angle)


def test_rotate_vertices():
    P = Polygonal(
        [
            Vertex("V1", 1, 0),
            Vertex("V2", 0, 1),
            Vertex("V3", -1, 0),
        ]
    )
    P.rotate_vertex(3, +math.pi / 2)
    expected_angle = 3 * math.pi / 2
    assert is_near(P.get_v(3).angle, expected_angle)


def test_is_translation_regular():
    P = Polygonal(
        [
            Vertex("V1", 1, 0),
            Vertex("V2", -1, 0),
            Vertex("V3", 0, 1),
            Vertex("V4", 0, -1),
            Vertex("V5", math.sqrt(2) / 2, math.sqrt(2) / 2),
        ]
    )
    # Si vede facilmente tramite disegno dove
    # posso traslare 4
    A = Vertex("A", -math.sqrt(2) / 2, -math.sqrt(2) / 2)
    assert P.is_translation_regular(4, A)
    B = Vertex("B", -math.sqrt(2) / 2, +math.sqrt(2) / 2)
    assert not P.is_translation_regular(4, B)
    P_2 = Polygonal(
        [
            Vertex("V1", -math.sqrt(3) / 2, 0.5),
            Vertex("V2", math.sqrt(3) / 2, 0.5),
            Vertex("V3", -math.sqrt(2) / 2, math.sqrt(2) / 2),
            Vertex("V4", math.sqrt(2) / 2, math.sqrt(2) / 2),
            Vertex("V5", 0, 1),
        ]
    )
    M_x = (math.sqrt(3) / 2 + math.sqrt(2) / 2) / 2
    M_y = (0.5 + math.sqrt(2) / 2) / 2
    M = Vertex("M", M_x, M_y)
    assert P_2.is_translation_regular(4, M)


def test_move_to_circle():
    P = Polygonal(
        [
            Vertex("V1", 1.3, 2.1),
            Vertex("V2", 2.7, 3.9),
            Vertex("V3", 4.9, 1.5),
            Vertex("V4", 0.5, 0.8),
            Vertex("V5", 3.5, 1.8),
        ]
    )
    P.move_to_circle()
    assert P.is_circle()
    P = Polygonal(
        [
            Vertex("V1", 1.3, -2.1),
            Vertex("V2", 38, 39),
            Vertex("V3", 4.9, 19),
            Vertex("V4", 0.5, 0.8),
            Vertex("V5", -20.5, 1.8),
        ]
    )
    P.move_to_circle()
    assert P.is_circle()


def test_move_to_midpoint():
    P = Polygonal(
        [
            Vertex("V1", 1, 0),
            Vertex("V2", -1, 0),
            Vertex("V3", 0, 1),
            Vertex("V4", 0, -1),
            Vertex("V5", math.sqrt(2) / 2, math.sqrt(2) / 2),
        ]
    )
    P.move_to_midpoint(4)
    assert is_near(P.get_v(4).x, math.sqrt(2) / 4)
    assert is_near(P.get_v(4).y, (2 + math.sqrt(2)) / 4)
    P_2 = Polygonal(
        [
            Vertex("V1", -math.sqrt(3) / 2, 0.5),
            Vertex("V2", math.sqrt(3) / 2, 0.5),
            Vertex("V3", -math.sqrt(2) / 2, math.sqrt(2) / 2),
            Vertex("V4", math.sqrt(2) / 2, math.sqrt(2) / 2),
            Vertex("V5", 0, 1),
        ]
    )
    P_2.move_to_midpoint(3)
    assert is_near(P_2.get_v(3).x, (math.sqrt(3) / 2 + math.sqrt(2) / 2) / 2)
    assert is_near(P_2.get_v(3).y, (0.5 + math.sqrt(2) / 2) / 2)


def test_move_and_eliminate():
    P = Polygonal(
        [
            Vertex("V1", 1, 0),
            Vertex("V2", -1, 0),
            Vertex("V3", 0, 1),
            Vertex("V4", 0, -1),
            Vertex("V5", math.sqrt(2) / 2, math.sqrt(2) / 2),
        ]
    )
    P.move_and_eliminate(4)
    assert len(P.vertices) == 4
    assert is_near(P.get_v(1).x, 1)
    assert is_near(P.get_v(1).y, 0)
    assert is_near(P.get_v(2).x, -1)
    assert is_near(P.get_v(2).y, 0)
    assert is_near(P.get_v(3).x, 0)
    assert is_near(P.get_v(3).y, 1)
    assert is_near(P.get_v(4).x, math.sqrt(2) / 2)
    assert is_near(P.get_v(4).y, math.sqrt(2) / 2)


def test_weak_translation_clockwise():
    P_1 = Polygonal(
        [
            Vertex("V1", -math.sqrt(2) / 2, math.sqrt(2) / 2),
            Vertex("V2", 0, -1),
            Vertex("V3", 0, 1),
            Vertex("V4", -math.sqrt(2) / 2, -math.sqrt(2) / 2),
            Vertex("V5", 1, 0),
            Vertex("V6", -1, 0),
            Vertex("V7", math.sqrt(2) / 2, math.sqrt(2) / 2),
            Vertex("V8", math.sqrt(2) / 2, -math.sqrt(2) / 2),
        ]
    )
    P_1.weak_translation_clockwise(1, math.pi / 6)
    # Si vede dal disegno che V1, V3 e V7 sono quelli che vanno traslati
    assert is_near(P_1.get_v(1).angle, math.pi / 6)
    assert is_near(P_1.get_v(3).angle, math.pi / 9)
    assert is_near(P_1.get_v(7).angle, math.pi / 18)
    P_2 = Polygonal(
        [
            Vertex("V1", -math.sqrt(2) / 2, math.sqrt(2) / 2),
            Vertex("V2", 0, -1),
            Vertex("V3", 0, 1),
            Vertex("V4", -math.sqrt(2) / 2, -math.sqrt(2) / 2),
        ]
    )
    P_2.weak_translation_clockwise(3, math.pi / 3)
    # Si vede dal disegno che viene traslato solo V3
    assert is_near(P_2.get_v(3).angle, math.pi / 3)
    P_3 = Polygonal(
        [
            Vertex("V1", -math.sqrt(2) / 2, math.sqrt(2) / 2),
            Vertex("V2", 0, -1),
            Vertex("V3", math.sqrt(2) / 2, math.sqrt(2) / 2),
            Vertex("V4", -1, 0),
            Vertex("V5", 1, 0),
            Vertex("V6", math.sqrt(2) / 2, -math.sqrt(2) / 2),
        ]
    )
    P_3.weak_translation_clockwise(6, 4 * math.pi / 3)
    # Si vede dal disegno che V1, V3 e V7 sono quelli che vanno traslati
    assert is_near(P_3.get_v(6).angle, 4 * math.pi / 3)
    assert is_near(P_3.get_v(2).angle, 7 * math.pi / 6)


def test_weak_translation_counterclockwise():
    P_1 = Polygonal(
        [
            Vertex("V1", -math.sqrt(2) / 2, math.sqrt(2) / 2),
            Vertex("V2", 0, -1),
            Vertex("V3", 0, 1),
            Vertex("V4", -math.sqrt(2) / 2, -math.sqrt(2) / 2),
            Vertex("V5", 1, 0),
            Vertex("V6", -1, 0),
            Vertex("V7", math.sqrt(2) / 2, math.sqrt(2) / 2),
            Vertex("V8", math.sqrt(2) / 2, -math.sqrt(2) / 2),
        ]
    )
    P_1.weak_translation_counterclockwise(7, 5 * math.pi / 6)
    assert is_near(P_1.get_v(7).angle, 5 * math.pi / 6)
    assert is_near(P_1.get_v(3).angle, 16 * math.pi / 18)
    assert is_near(P_1.get_v(1).angle, 17 * math.pi / 18)


def test_get_next_clockwise():
    P = Polygonal(
        [
            Vertex("V1", 1, 0),
            Vertex("V2", 0, 1),
            Vertex("V3", -1, 0),
            Vertex("V4", 0, -1),
        ]
    )
    assert P.get_next_clockwise(1).name == "V4"


def test_get_next_counterclockwise():
    P = Polygonal(
        [
            Vertex("V1", 1, 0),
            Vertex("V2", 0, 1),
            Vertex("V3", -1, 0),
            Vertex("V4", 0, -1),
        ]
    )
    assert P.get_next_counterclockwise(1).name == "V2"


def test_permute_vertices_backward():
    v1 = Vertex("v1", 1, 0)
    v2 = Vertex("v2", 0, 1)
    v3 = Vertex("v3", -1, 0)
    P = Polygonal([v1, v2, v3])
    P.permute_vertices_backward()
    assert len(P.vertices) == 3
    assert P.vertices[0].name == "v2"
    assert P.vertices[1].name == "v3"
    assert P.vertices[2].name == "v1"


def test_is_polygonal_reduced():
    P_square = Polygonal(
        [
            Vertex("v1", 1, 0),
            Vertex("v2", 0, 1),
            Vertex("v3", -1, 0),
            Vertex("v4", 0, -1),
        ]
    )
    assert not P_square.is_polygonal_reduced()
    P_butterfly = Polygonal(
        [
            Vertex("V1", -1.4, -1.2),
            Vertex("V2", 1.7, 1.6),
            Vertex("V3", 1.3, -1.4),
            Vertex("V4", -1.5, 1.9),
        ]
    )
    assert P_butterfly.is_polygonal_reduced()
    P_pentagon = Polygonal(
        [
            Vertex("V1", 1.0, 0.0),
            Vertex("V2", 0.309, 0.951),
            Vertex("V3", -0.809, 0.588),
            Vertex("V4", -0.809, -0.588),
            Vertex("V5", 0.309, -0.951),
        ]
    )
    assert not P_pentagon.is_polygonal_reduced()
    P_star = Polygonal(
        [
            Vertex("V1", 1.0, 0.0),
            Vertex("V3", -0.809, 0.588),
            Vertex("V5", 0.309, -0.951),
            Vertex("V2", 0.309, 0.951),
            Vertex("V4", -0.809, -0.588),
        ]
    )
    assert P_star.is_polygonal_reduced()


@pytest.mark.parametrize(
    "P",
    [
        # Caso A1
        Polygonal(
            [
                Vertex("v1", -0.866025, 0.5),
                Vertex("v2", 0.866025, 0.5),
                Vertex("v3", 0, 1),
                Vertex("v4", 0.707107, -0.707107),
                Vertex("v5", -0.707107, -0.707107),
                Vertex("v6", 0, -1),
            ]
        ),
        # Caso A211 su tutti i vertici
        Polygonal(
            [
                Vertex("v1", -0.866025, 0.5),
                Vertex("v2", 0.866025, 0.5),
                Vertex("v3", -0.707107, 0.707107),
                Vertex("v4", 0.707107, -0.707107),
                Vertex("v5", 0.707107, 0.707107),
                Vertex("v6", 0, -1),
                Vertex("v7", -0.866025, -0.5),
                Vertex("v8", 0, 1),
            ]
        ),
        # Caso A212 su tutti i vertici
        Polygonal(
            [
                Vertex("v1", -0.866025, 0.5),
                Vertex("v2", 1, 0),
                Vertex("v3", -0.707107, 0.707107),
                Vertex("v4", 0.707107, -0.707107),
                Vertex("v5", 0.707107, 0.707107),
                Vertex("v6", 0, -1),
                Vertex("v7", -0.866025, -0.5),
                Vertex("v8", 0.866025, 0.5),
            ]
        ),
        # Caso A22 su tutti i vertici
        Polygonal(
            [
                Vertex("v1", -0.866025, 0.5),
                Vertex("v2", 1, 0),
                Vertex("v3", -0.707107, 0.707107),
                Vertex("v4", 0.707107, -0.707107),
                Vertex("v5", 0.707107, 0.707107),
                Vertex("v6", -0.707107, -0.707107),
                Vertex("v7", 0, 1),
                Vertex("v8", 0, -1),
            ]
        ),
        # Caso A2321 su tutti i vertici
        Polygonal(
            [
                Vertex("v1", -1, 0),
                Vertex("v2", 1, 0),
                Vertex("v3", 0, 1),
                Vertex("v4", 0, -1),
                Vertex("v5", -0.707107, -0.707107),
                Vertex("v6", 0.707107, -0.707107),
                Vertex("v7", -0.866025, -0.5),
                Vertex("v8", 0.866025, 0.5),
            ]
        ),
        # Caso A2322 su tutti i vertici
        Polygonal(
            [
                Vertex("v1", -1, 0),
                Vertex("v2", 1, 0),
                Vertex("v3", 0, 1),
                Vertex("v4", 0.707107, -0.707107),
                Vertex("v5", -0.707107, -0.707107),
                Vertex("v6", 0.866025, -0.5),
                Vertex("v7", -0.866025, -0.5),
                Vertex("v8", 0, -1),
            ]
        ),
        # Caso B21 su tutti i vertici
        Polygonal(
            [
                Vertex("v1", -1, 0),
                Vertex("v2", 1, 0),
                Vertex("v3", 0, 1),
                Vertex("v4", 0, -1),
                Vertex("v5", 0.707107, -0.707107),
                Vertex("v6", 0.5, -0.866025),
            ]
        ),
        # Caso B2211 su tutti i vertici
        Polygonal(
            [
                Vertex("v1", -1, 0),
                Vertex("v2", 1, 0),
                Vertex("v3", 0, 1),
                Vertex("v4", 0, -1),
                Vertex("v5", 0.707107, -0.707107),
                Vertex("v6", -0.5, -0.866025),
                Vertex("v7", 0.866025, 0.5),
            ]
        ),
        # Caso B22121 su tutti i vertici
        Polygonal(
            [
                Vertex("v1", -1, 0),
                Vertex("v2", 1, 0),
                Vertex("v3", 0, 1),
                Vertex("v4", 0, -1),
                Vertex("v5", 0.707107, -0.707107),
                Vertex("v6", -0.5, -0.866025),
                Vertex("v7", 0.866025, -0.5),
                Vertex("v8", -0.5, 0.866025),
            ]
        ),
        # Caso B22122 su tutti i vertici
        Polygonal(
            [
                Vertex("v1", -1, 0),
                Vertex("v2", 1, 0),
                Vertex("v3", 0, 1),
                Vertex("v4", 0, -1),
                Vertex("v5", 0.707107, -0.707107),
                Vertex("v6", -0.866025, -0.5),
                Vertex("v7", 0.866025, -0.5),
                Vertex("v8", -0.5, -0.866025),
            ]
        ),
        # Caso B222 su tutti i vertici
        Polygonal(
            [
                Vertex("v1", -1, 0),
                Vertex("v2", 1, 0),
                Vertex("v3", -0.707107, 0.707107),
                Vertex("v4", 0, -1),
                Vertex("v5", 0, 1),
                Vertex("v6", -0.866025, -0.5),
                Vertex("v7", 0.866025, -0.5),
                Vertex("v8", 0.5, 0.866025),
            ]
        ),
        # Caso C1 su tutti i vertici
        Polygonal(
            [
                Vertex("v1", -0.866025, 0.5),
                Vertex("v2", 0.866025, 0.5),
                Vertex("v3", -0.707107, 0.707107),
                Vertex("v4", 0.707107, 0.707107),
                Vertex("v5", 0, 1),
            ]
        ),
        # Caso C211 su tutti i vertici
        Polygonal(
            [
                Vertex("v1", -0.866025, 0.5),
                Vertex("v2", 0.866025, 0.5),
                Vertex("v3", -0.707107, 0.707107),
                Vertex("v4", 0, -1),
                Vertex("v5", 0.707107, 0.707107),
                Vertex("v6", 0.707107, -0.707107),
                Vertex("v7", 0.5, -0.866025),
            ]
        ),
        # Caso C212 su tutti i vertici
        Polygonal(
            [
                Vertex("v1", -0.866025, 0.5),
                Vertex("v2", 0.866025, 0.5),
                Vertex("v3", -0.707107, 0.707107),
                Vertex("v4", 0, -1),
                Vertex("v5", 0.707107, 0.707107),
                Vertex("v6", 0.707107, -0.707107),
                Vertex("v7", -0.5, -0.866025),
            ]
        ),
        # Caso C22 su tutti i vertici
        Polygonal(
            [
                Vertex("v1", -0.866025, 0.5),
                Vertex("v2", 1, 0),
                Vertex("v3", 0.707107, 0.707107),
                Vertex("v4", 0.707107, -0.707107),
                Vertex("v5", -0.707107, 0.707107),
                Vertex("v6", -0.707107, -0.707107),
                Vertex("v7", 0.5, 0.866025),
                Vertex("v8", 0, -1),
                Vertex("v9", 0, 1),
            ]
        ),
        Polygonal(
            [
                Vertex("v1", -0.7663019028873093, -0.642480656231212),
                Vertex("v2", 0.5835688924714628, 0.8120636352772056),
                Vertex("v3", -0.5758800273453695, 0.8175342158617561),
                Vertex("v4", 0.4971473368031256, -0.8676661371227758),
                Vertex("v5", 0.4048289304860413, 0.9143924414831566),
                Vertex("v6", -0.0019052602442695132, 0.9999981849900537),
                Vertex("v7", 0.4734719948529662, -0.8808088726221783),
                Vertex("v8", 0.9961738316387703, -0.08739391945742568),
                Vertex("v9", -0.45688439031782035, 0.8895260838693341),
                Vertex("v10", 0.6673901519308159, 0.7447082550272708),
            ]
        ),
        # Risolto con casi limite C212 e D211
        Polygonal(
            [
                Vertex("v1", -0.027064249416564268, 0.99963369611249),
                Vertex("v2", -0.47046008597247124, 0.8824212755293103),
                Vertex("v3", 0.043156452696938574, -0.999068326287355),
                Vertex("v4", 0.5789189989831471, 0.8153850578814594),
                Vertex("v5", -0.6194249797590352, 0.7850558543508346),
                Vertex("v6", -0.6988412987788333, 0.7152767570116573),
                Vertex("v7", -0.9469475854993759, -0.3213880369847364),
                Vertex("v8", 0.8233008094392888, 0.5676053005184253),
                Vertex("v9", 0.32845338780422884, -0.9445201808537099),
                Vertex("v10", -0.09221411342817709, -0.9957392014401438),
            ]
        ),
        # Caso D222 risolto (era sbagliata traslazione da fare)
        Polygonal(
            [
                Vertex("v1", -0.5251063764080388, 0.8510365993631643),
                Vertex("v2", -0.8450047362943791, 0.5347588200675766),
                Vertex("v3", 0.1124306784212028, -0.9936595707533582),
                Vertex("v4", -0.396125057669658, -0.9181965686530363),
                Vertex("v5", -0.09199680840970714, -0.9957593018608601),
                Vertex("v6", 0.1421516850156288, 0.9898448860539805),
                Vertex("v7", -0.05823585492842853, 0.9983028524454666),
                Vertex("v8", 0.7574307225242187, 0.6529155386238253),
                Vertex("v9", 0.4462509178182765, 0.8949078826037604),
                Vertex("v10", -0.8010653653165059, 0.5985768793482864),
            ]
        ),
        # Caso B22121 con eliminazione di 1
        Polygonal(
            [
                Vertex("v1", 0.5219905827378799, 0.8529512480399853),
                Vertex("v2", 0.7804265648630979, -0.6252474524985966),
                Vertex("v3", 0.7265185939468239, 0.687146805747891),
                Vertex("v4", -0.7858300690463504, 0.6184424812240893),
                Vertex("v5", 0.5782723606381313, -0.8158437821801445),
                Vertex("v6", 0.9049041957432591, -0.4256153151923054),
                Vertex("v7", -0.8844293667721761, 0.46667407812194545),
                Vertex("v8", -0.920908659804275, -0.38977845027334956),
                Vertex("v9", -0.1021141749577048, -0.994772685226483),
                Vertex("v10", 0.23800921559381294, -0.9712628960752171),
            ]
        ),
        Polygonal(
            [
                Vertex("v1", -0.8621451263871016, 0.5066614067076439),
                Vertex("v2", 0.028219615828837252, 0.9996017473386453),
                Vertex("v3", -0.4759043486670984, 0.8794970442927849),
                Vertex("v4", -0.590805663549171, 0.8068138991850746),
                Vertex("v5", -0.6319788247518952, 0.7749856547480175),
                Vertex("v6", 0.5623965762117165, 0.8268676381775616),
                Vertex("v7", 0.5239292349433162, 0.8517617957925275),
                Vertex("v8", -0.0013135761418423542, 0.9999991372584877),
                Vertex("v9", -0.11065117355824272, -0.9938593048264849),
                Vertex("v10", 0.8130874681602098, 0.5821415370172616),
            ]
        ),
        # Risolto aggiungendo caso j+2 = 1 in A231
        Polygonal(
            [
                Vertex("v1", -0.6506546378203966, 0.7593737829835902),
                Vertex("v2", 0.14693488405258082, 0.9891461670796964),
                Vertex("v3", 0.01794688738789474, 0.9998389416466466),
                Vertex("v4", 0.7155122351671193, -0.6986002013499231),
                Vertex("v5", -0.7979432041137509, -0.6027326463770492),
                Vertex("v6", -0.7301201913332818, -0.6833187442236983),
                Vertex("v7", 0.9728650671751502, 0.2313732073302579),
                Vertex("v8", -0.26318205500266756, -0.9647461873076114),
                Vertex("v9", -0.9098559858670094, 0.41492419184951396),
                Vertex("v10", 0.0964292767365933, -0.995339838742556),
            ]
        ),
        # Risolto sistemando C2322 (2 * math.pi al posto di v2.angle)
        Polygonal(
            [
                Vertex("v1", -0.7528576054470708, 0.6581834287799281),
                Vertex("v2", -0.4258488352240466, -0.9047943244397164),
                Vertex("v3", 0.6910818537649417, -0.7227765016910911),
                Vertex("v4", 0.7549622062262864, -0.6557683029622111),
                Vertex("v5", 0.12032948796817289, 0.9927340098562744),
                Vertex("v6", 0.37110851358559693, -0.9285895062643605),
                Vertex("v7", 0.2644528463227458, -0.964398616792765),
                Vertex("v8", -0.768449160796814, 0.63991084322011),
                Vertex("v9", -0.4203615540940988, -0.9073566905245114),
                Vertex("v10", 0.9585598867573586, 0.28489110814435725),
            ]
        ),
        # Caso A22 risolto (nel primo passaggio dovevo mettere la verifica dopo aver effettuato la prima traslazione)
        Polygonal(
            [
                Vertex("v1", -0.3702028565084752, 0.9289509379041314),
                Vertex("v2", -0.1998719792058199, -0.9798220205365606),
                Vertex("v3", 0.9401500784375194, -0.3407606638300936),
                Vertex("v4", -0.6447138975617734, -0.7644239597832522),
                Vertex("v5", 0.901916213565757, -0.4319110367971717),
                Vertex("v6", -0.8333995151864555, -0.5526710125264224),
                Vertex("v7", 0.6497999019804244, 0.76010531335219),
                Vertex("v8", -0.6005544978507085, -0.7995838261941542),
                Vertex("v9", -0.756637204282677, -0.6538349494293606),
                Vertex("v10", -0.7444806253423975, 0.6676440657189974),
            ]
        ),  # Risolto con gestione di vertici sovrapposti nella weak translation
        Polygonal(
            [
                Vertex("v1", 0.9321080429206021, -0.36218033674224365),
                Vertex("v2", -0.8009534765116428, 0.5987265890737719),
                Vertex("v3", -0.8704112598188085, -0.4923253383491801),
                Vertex("v4", -0.26855455403114226, -0.9632644764077695),
                Vertex("v5", -0.10772600870428262, 0.9941806209379888),
                Vertex("v6", -0.9675375201536438, -0.25272741658739234),
                Vertex("v7", -0.8682184637043391, -0.49618212309884485),
                Vertex("v8", -0.7892939892326432, -0.6140154709461483),
                Vertex("v9", -0.7771818171528171, -0.6292761103736937),
                Vertex("v10", -0.11224889726286946, 0.9936801221033205),
            ]
        ),  # Risolto con D22122 con cambio di riferimento
        Polygonal(
            [
                Vertex("v1", -0.783601154338786, 0.6212642198927297),
                Vertex("v2", 0.1278279767228887, -0.9917963542819326),
                Vertex("v3", -0.738849487605207, 0.6738704880505771),
                Vertex("v4", 0.42095985155279125, 0.9070792707259118),
                Vertex("v5", 0.5592132305479929, -0.8290238614057363),
                Vertex("v6", 0.7443738516374385, -0.667763108443739),
                Vertex("v7", 0.7067287122586225, 0.707484648080274),
                Vertex("v8", 0.5156864281824529, -0.8567773968706363),
                Vertex("v9", 0.0985247668394238, 0.9951345990966434),
                Vertex("v10", 0.5927485623637383, -0.805387572424433),
            ]
        ),  # Caso E22
        Polygonal(
            [
                Vertex("v1", 0.9386937996125804, 0.34475201314698195),
                Vertex("v2", 0.5577227493581884, -0.8300273097003154),
                Vertex("v3", 0.8495709053973892, -0.5274744322735088),
                Vertex("v4", 0.37382803211697113, 0.9274980336386449),
                Vertex("v5", -0.9282248435043767, 0.3720196767662637),
                Vertex("v6", 0.11082186843019914, 0.9938402856986829),
                Vertex("v7", 0.055353192646783844, -0.9984668367371087),
                Vertex("v8", 0.09183406603173161, 0.9957743239891654),
                Vertex("v9", -0.05595823175927017, -0.9984331105779575),
                Vertex("v10", 0.5700494503892732, -0.821610384617239),
            ]
        ),
        Polygonal(
            [
                Vertex("v1", 0.8221323634570041, 0.5692963876194899),
                Vertex("v2", -0.029601855637303, -0.9995617690482306),
                Vertex("v3", 0.6783352487237904, -0.7347525368032651),
                Vertex("v4", 0.5204953623621824, -0.8538644961347558),
                Vertex("v5", -0.9160425142349107, 0.4010811789578058),
                Vertex("v6", -0.9484180585246944, 0.31702237502146335),
                Vertex("v7", -0.705221919945, 0.7089866314882728),
                Vertex("v8", -0.17617028866285156, 0.9843597052868669),
                Vertex("v9", -0.249781672951094, 0.968302182099035),
                Vertex("v10", -0.987741698852717, 0.15609720160063242),
            ]
        ),
        Polygonal(
            [
                Vertex("v1", 0.8221323634570041, 0.5692963876194899),
                Vertex("v2", -0.029601855637303, -0.9995617690482306),
                Vertex("v3", 0.6783352487237904, -0.7347525368032651),
                Vertex("v4", 0.5204953623621824, -0.8538644961347558),
                Vertex("v5", -0.9160425142349107, 0.4010811789578058),
                Vertex("v6", -0.9484180585246944, 0.31702237502146335),
                Vertex("v7", -0.705221919945, 0.7089866314882728),
                Vertex("v8", -0.17617028866285156, 0.9843597052868669),
                Vertex("v9", -0.249781672951094, 0.968302182099035),
                Vertex("v10", -0.987741698852717, 0.15609720160063242),
            ]
        ),
        Polygonal(
            [
                Vertex("v1", 0.9309730039131232, -0.3650880249816144),
                Vertex("v2", 0.12903512969783848, -0.9916400230445834),
                Vertex("v3", 0.1778554419797136, -0.9840566252803752),
                Vertex("v4", -0.3976427746306157, -0.9175403118032828),
                Vertex("v5", 0.1118661904643743, 0.993723279102884),
                Vertex("v6", -0.7421716664243356, 0.6702098309909551),
                Vertex("v7", -0.6174924619511899, 0.7865767981789562),
                Vertex("v8", 0.1442465829068753, 0.9895417744186902),
                Vertex("v9", -0.8480422565708308, 0.5299286094090914),
                Vertex("v10", -0.939596700200938, -0.3422835680711369),
            ]
        ),
        Polygonal(
            [
                Vertex("v1", 0.9822979314554909, -0.1873253155829816),
                Vertex("v2", -0.8676696270010948, 0.4971412459048042),
                Vertex("v3", -0.4846368510846364, -0.8747154523448),
                Vertex("v4", -0.29340126152361345, -0.955989382648339),
                Vertex("v5", -0.3602401598579339, -0.9328595967376496),
                Vertex("v6", 0.2503476116287866, -0.9681560170508482),
                Vertex("v7", -0.7014911941776061, 0.7126781212379655),
                Vertex("v8", 0.17165646568010495, -0.9851568696356002),
                Vertex("v9", 0.7087614959245248, 0.7054481851240599),
                Vertex("v10", 0.9340723516373792, -0.35708380235823656),
            ]
        ),
        Polygonal(
            [
                Vertex("v1", 0.8411518316704101, 0.5407990348341185),
                Vertex("v2", -0.29171521212954477, -0.9565052195425882),
                Vertex("v3", 0.23823813420522888, -0.9712067706778055),
                Vertex("v4", 0.7387788335110383, -0.6739479469188029),
                Vertex("v5", -0.5706475887748501, -0.821195061739566),
                Vertex("v6", -0.7824426077330646, -0.6227227036200637),
                Vertex("v7", 0.9090667286442682, -0.41665055246814264),
                Vertex("v8", -0.05637398002140226, -0.9984097226973235),
                Vertex("v9", -0.17900977021110775, 0.9838472961638745),
                Vertex("v10", 0.38823130650685833, -0.9215619635423208),
            ]
        ),
        Polygonal(
            [
                Vertex("v1", 0.3437300059454709, 0.9390685188061234),
                Vertex("v2", -0.1664430775964021, 0.9860510645601668),
                Vertex("v3", 0.9364502081098824, 0.3508005241315324),
                Vertex("v4", 0.40515783346200185, -0.9142467555230245),
                Vertex("v5", 0.37018462362294713, -0.9289582038138944),
                Vertex("v6", -0.5671139068187114, -0.8236393729617459),
                Vertex("v7", 0.2411510433589672, 0.9704875961530274),
                Vertex("v8", 0.20813455918082324, -0.9781002020624494),
                Vertex("v9", -0.8931146784951343, 0.44982904647936306),
                Vertex("v10", -0.04240571295747442, 0.9991004731800343),
            ]
        ),
        Polygonal(
            [
                Vertex("v1", -0.03870415533062266, -0.9992507134649157),
                Vertex("v2", 0.18367049849051953, -0.9829878676688966),
                Vertex("v3", 0.4072763921123359, -0.9133049547812379),
                Vertex("v4", -0.3084545141973216, -0.9512390933258023),
                Vertex("v5", 0.8960922681330192, 0.4438678260385868),
                Vertex("v6", -0.021813893042371912, -0.9997620487247633),
                Vertex("v7", -0.8336515479434592, -0.5522907717964102),
                Vertex("v8", -0.1177562541195667, -0.9930425291072523),
                Vertex("v9", -0.6431690600169051, -0.7657242063804505),
                Vertex("v10", 0.8097102329715413, 0.5868299060385149),
            ]
        ),
        Polygonal(
            [
                Vertex("v1", -0.5920294186750179, -0.8059163526218589),
                Vertex("v2", -0.7924600678564047, -0.6099237992184126),
                Vertex("v3", 0.6868014689132571, 0.7268450607238054),
                Vertex("v4", -0.2912546389239943, -0.9566455640963657),
                Vertex("v5", -0.340751264165704, 0.940153485325388),
                Vertex("v6", -0.4598294276335537, 0.8880072620661378),
                Vertex("v7", 0.5929430647650493, 0.8052443864734672),
                Vertex("v8", -0.11185944293464023, -0.9937240386678547),
                Vertex("v9", 0.6406438457955319, -0.7678381749068685),
                Vertex("v10", -0.9358086811135757, -0.3525083152954975),
            ]
        ),
        Polygonal(
            [
                Vertex("v1", 0.6015298356337491, 0.7988503344447161),
                Vertex("v2", 0.7708393283231181, -0.6370296146258541),
                Vertex("v3", -0.3893177155289367, -0.9211035318439127),
                Vertex("v4", 0.33235625957623105, 0.9431539199518268),
                Vertex("v5", 0.6700923419022384, 0.7422777467525035),
                Vertex("v6", -0.7364106197498774, 0.6765348469366537),
                Vertex("v7", 0.4343582929029939, 0.9007401808437309),
                Vertex("v8", 0.8820654561523997, -0.47112687363666594),
                Vertex("v9", 0.46364995773548223, 0.8860184629520345),
                Vertex("v10", -0.7412010788741263, 0.6712830704522729),
            ]
        ),
        Polygonal(
            [
                Vertex("v1", -0.9312598162899415, 0.364355807643606),
                Vertex("v2", 0.717660913450993, 0.6963927148561264),
                Vertex("v3", 0.1412086984944132, -0.989979850032067),
                Vertex("v4", 0.9334601981061827, -0.3586809983140535),
                Vertex("v5", -0.18893670688744302, 0.9819892671463005),
                Vertex("v6", 0.2755062087241116, -0.9612992920804978),
                Vertex("v7", 0.11099469420256813, 0.9938209989021556),
                Vertex("v8", -0.9653186902898165, 0.2610743690544003),
                Vertex("v9", -0.8935791857086561, 0.44890560128857265),
                Vertex("v10", -0.814386433395254, -0.5803229593095189),
            ]
        ),
    ],
)
def test_reduce_polygonal(P):
    P.reduce_polygonal()
    assert P.is_polygonal_reduced()
