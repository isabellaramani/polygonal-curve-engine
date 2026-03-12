import math
from poligoni_stellati import Vertex, Polygon, get_determinant, generate_random_polygon, get_angle_bisector

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


def test_get_determinant():
    V1 = Vertex("V1", 1.3, 2.8)
    V2 = Vertex("V2", 3.6, 4.1)
    V3 = Vertex("V3", 5.9, 6.4)
    V4 = Vertex("V4", 7.3, 8.3)
    det = get_determinant(V1, V2, V3, V4)
    expected = (V1.x - V2.x) * (V3.y - V4.y) - (V1.y - V2.y) * (V3.x - V4.x)
    assert is_near(det, expected)


def test_get_angle_bisector():

    ang1 = math.radians(30)
    ang2 = math.radians(50)
    expected = math.radians(40)
    assert is_near(get_angle_bisector(ang1, ang2),
                   expected)

    ang1 = math.radians(350)
    ang2 = math.radians(10)
    expected = get_angle_bisector(ang1, ang2)
    assert is_near(expected, 0.0) or is_near(
        expected, 2 * math.pi)

    ang1 = math.radians(350)
    ang2 = math.radians(0)
    expected = math.radians(355)
    assert is_near(get_angle_bisector(ang1, ang2),
                   expected)

    ang1 = math.radians(10)
    ang2 = math.radians(350)
    expected = get_angle_bisector(ang1, ang2)
    assert is_near(expected, 0.0) or is_near(
        expected, 2 * math.pi)

    ang1 = math.radians(-10)
    ang2 = math.radians(10)
    expected = get_angle_bisector(ang1, ang2)
    assert is_near(expected, 0.0) or is_near(
        expected, 2 * math.pi)


def test_is_empty():
    P_1 = Polygon()
    assert P_1.is_empty()
    P_2 = Polygon([Vertex("V", 1, 1)])
    assert not P_2.is_empty()


def test_add_vertex():
    P = Polygon()
    v = Vertex("V", 1, 2)
    P.add_vertex(v)
    assert len(P.vertices) == 1
    assert is_near(P.vertices[0].x, v.x)
    assert is_near(P.vertices[0].y, v.y)


def test_get_v_i():
    P = Polygon(
        [Vertex("V1", 5.6, 2.9), Vertex(
            "V2", 3.2, 4.1), Vertex("V3", 7.6, 1.8)]
    )
    assert P.get_v(2).name == "V2"
    # DUBBIO: in questo caso deve restituire esattamente 3 e 4?
    assert is_near(P.get_v(2).x, 3.2)
    assert is_near(P.get_v(2).y, 4.1)


def test_eliminate_vertex():
    P_1 = Polygon([Vertex("V1", 1, 0), Vertex(
        "V2", 0, 0), Vertex("V3", -4, 0)])
    P_1.eliminate_vertex(2)
    assert len(P_1.vertices) == 2
    P_2 = Polygon([Vertex("V1", 0, 0), Vertex("V2", 1, 2), Vertex("V3", 2, 4)])
    P_2.eliminate_vertex(2)
    assert len(P_2.vertices) == 2


def test_get_rotation_angle():
    P = Polygon(
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
    # Poligono a farfalla (winding number = 0)
    P = Polygon(
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
    P = Polygon([Vertex("V1", 3.4, 0), Vertex(
        "V2", 1, 0), Vertex("V3", 1, -1)])
    assert P.is_left_turn(2)
    P_2 = Polygon(
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
    P = Polygon([Vertex("V1", 3.4, 0), Vertex("V2", 1, 0), Vertex("V3", 1, 1)])
    assert P.is_right_turn(2)
    P_2 = Polygon(
        [
            Vertex("V1", -math.sqrt(3) / 2, 0.5),
            Vertex("V2", math.sqrt(3) / 2, 0.5),
            Vertex("V3", -math.sqrt(2) / 2, math.sqrt(2) / 2),
            Vertex("V4", math.sqrt(2) / 2, math.sqrt(2) / 2),
            Vertex("V5", 0, 1),
        ]
    )
    assert P_2.is_right_turn(3)


def test_center_polygon():
    P = Polygon(
        [Vertex("V1", 1.5, 2.4), Vertex(
            "V2", 3.6, 4.1), Vertex("V3", 2.7, 9.8)]
    )
    coords = [(1.5, 2.4), (3.6, 4.1), (2.7, 9.8)]
    # Calcolo centro
    center_x = (1.5 + 3.6 + 2.7) / 3
    center_y = (2.4 + 4.1 + 9.8) / 3
    P.center_polygon()

    for i in range(1, 4):
        expected_x = coords[i - 1][0] - center_x
        expected_y = coords[i - 1][1] - center_y
        assert is_near(P.get_v(i).x, expected_x)
        assert is_near(P.get_v(i).y, expected_y)


def test_is_circle():
    P_1 = Polygon(
        [
            Vertex("V1", 1, 0),
            Vertex("V2", 0, 1),
            Vertex("V3", -1, 0),
            Vertex("V4", 0, -1),
        ]
    )
    assert P_1.is_circle()

    P_2 = Polygon(
        [
            Vertex("V1", 1, 0),
            Vertex("V2", 0, 1),
            Vertex("V3", -1, 0),
            Vertex("V4", 0, 0.8),
            Vertex("V5", 0.5, 0.5),
        ]
    )
    assert not P_2.is_circle()

    P_3 = Polygon(
        [
            Vertex("V1", 0.5, 0),
            Vertex("V2", -0.9, 1.5),
            Vertex("V3", -1.9, 3),
            Vertex("V4", -10.7, 37.5),
        ]
    )
    assert not P_3.is_circle()


def test_is_clockwise():
    P_1 = Polygon(
        [
            Vertex("V1", -1, 0),
            Vertex("V2", math.sqrt(3) / 2, 0.5),
            Vertex("V3", 1, 0),
            Vertex("V4", 0, -1),
        ]
    )
    assert P_1.is_clockwise(P_1.vertices)
    P_2 = Polygon(
        [Vertex("V1", 0.5, math.sqrt(3) / 2),
         Vertex("V2", -1, 0), Vertex("V3", 0, 1)]
    )
    assert P_2.is_clockwise(P_2.vertices)
    P_3 = Polygon(
        [Vertex("V1", 0.5, math.sqrt(3) / 2),
         Vertex("V2", -1, 0), Vertex("V3", 0, -1)]
    )
    assert not P_3.is_clockwise(P_3.vertices)
    P_4 = Polygon(
        [
            Vertex("V1", -1, 0),
            Vertex("V2", math.sqrt(3) / 2, 0.5),
            Vertex("V3", 1, 0),
            Vertex("V4", 0, -1),
            Vertex("V5", 0, -1),
        ]
    )
    assert P_4.is_clockwise(P_4.vertices)
    P_5 = Polygon(
        [Vertex("V1", -1, 0), Vertex("V2", -1, 0), Vertex("V3", 0, -1)])
    assert P_5.is_clockwise(P_5.vertices)

    P_6 = Polygon([Vertex("v1", -1, 0), Vertex("v2", 1, 0),
                   Vertex("v3", -0.707107, 0.707107), Vertex("v4",
                                                             0.707107, -0.707107),
                   Vertex("v5", 0.707107, 0.707107), Vertex("v6", 0, -1),
                   Vertex("v7", -0.866025, -0.5), Vertex("v8", 0, 1)])
    assert P_6.is_clockwise([P_6.get_v(7), P_6.get_v(8), P_6.get_v(2)])
    assert P_6.is_clockwise([P_6.get_v(7), P_6.get_v(8), P_6.get_v(5)])

    P_7 = Polygon([Vertex("v1", -1, 0), Vertex("v2", 1, 0),
                   Vertex("v3", 0, 1), Vertex("v4",
                                              0, -1),
                   Vertex("v5", 0.707107, -0.707107), Vertex(
        "v6", 0.5, -0.866025)
    ])
    assert P_7.is_clockwise([P_7.get_v(2), P_7.get_v(2), P_7.get_v(5)])

    P_8 = Polygon([Vertex("v1", -0.866025, 0.5), Vertex("v2", 0.866025, 0.5),
                   Vertex("v3", 0, 1), Vertex("v4", 0.707107, -0.707107),
                   Vertex("v5", -0.707107, -0.707107), Vertex("v6", 0, -1)])
    assert not P_8.is_clockwise([P_8.get_v(5),
                                 P_8.get_v(6), P_8.get_v(1)])


def test_is_counterclockwise():
    P_1 = Polygon(
        [
            Vertex("V1", -1, 0),
            Vertex("V2", math.sqrt(3) / 2, 0.5),
            Vertex("V3", 1, 0),
            Vertex("V4", 0, -1),
        ]
    )
    assert not P_1.is_counterclockwise(P_1.vertices)
    P_2 = Polygon(
        [Vertex("V1", 0.5, math.sqrt(3) / 2),
         Vertex("V2", -1, 0), Vertex("V3", 0, 1)]
    )
    assert not P_2.is_counterclockwise(P_2.vertices)
    P_3 = Polygon(
        [Vertex("V1", 0.5, math.sqrt(3) / 2),
         Vertex("V2", -1, 0), Vertex("V3", 0, -1)]
    )
    assert P_3.is_counterclockwise(P_3.vertices)
    P_4 = Polygon(
        [
            Vertex("V1", -1, 0),
            Vertex("V2", math.sqrt(3) / 2, 0.5),
            Vertex("V3", 1, 0),
            Vertex("V4", 0, -1),
            Vertex("V5", 0, -1),
        ]
    )
    assert not P_4.is_counterclockwise(P_4.vertices)
    P_5 = Polygon(
        [Vertex("V1", -1, 0), Vertex("V2", -1, 0), Vertex("V3", 0, -1)])
    assert P_5.is_counterclockwise(P_5.vertices)


def test_get_unitary_radius():
    P = Polygon(
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


def test_sort_vertices_clockwise():
    P_1 = Polygon(
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

    P_2 = Polygon(
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

    list_3 = [P_2.get_v(4), P_2.get_v(6), P_2.get_v(2),
              P_2.get_v(3), P_2.get_v(1)]
    sorted_vertices_3 = P_2.sort_vertices_clockwise(list_3)
    expected_order_3 = ["V4", "V2", "V6", "V3", "V1"]
    for v, expected_name in zip(sorted_vertices_3, expected_order_3):
        assert v.name == expected_name


def test_sort_vertices_counterclockwise():
    P_1 = Polygon(
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

    P_2 = Polygon(
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

    list_3 = [P_2.get_v(4), P_2.get_v(6), P_2.get_v(2),
              P_2.get_v(3), P_2.get_v(1)]
    sorted_vertices_3 = P_2.sort_vertices_counterclockwise(list_3)
    expected_order_3 = ["V4", "V1", "V3", "V6", "V2"]
    for v, expected_name in zip(sorted_vertices_3, expected_order_3):
        assert v.name == expected_name


def test_get_equispaced_vertices():
    P = Polygon(
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


def test_rotate_vertices():
    P = Polygon(
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
    P = Polygon(
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

    P_2 = Polygon(
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


def test_move_to_midpoint():
    P = Polygon(
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

    P_2 = Polygon(
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
    P = Polygon(
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
    P_1 = Polygon(
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

    P_2 = Polygon(
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

    P_3 = Polygon(
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
    P_1 = Polygon(
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
    P = Polygon(
        [
            Vertex("V1", 1, 0),
            Vertex("V2", 0, 1),
            Vertex("V3", -1, 0),
            Vertex("V4", 0, -1),
        ]
    )
    assert P.get_next_clockwise(1).name == "V4"


def test_get_next_counterclockwise():
    P = Polygon(
        [
            Vertex("V1", 1, 0),
            Vertex("V2", 0, 1),
            Vertex("V3", -1, 0),
            Vertex("V4", 0, -1),
        ]
    )
    assert P.get_next_counterclockwise(1).name == "V2"


def test_reduce_polygon():
    # Caso A1
    P = Polygon([Vertex("v1", -0.866025, 0.5), Vertex("v2", 0.866025, 0.5),
                 Vertex("v3", 0, 1), Vertex("v4", 0.707107, -0.707107),
                 Vertex("v5", -0.707107, -0.707107), Vertex("v6", 0, -1)])
    P.reduce_polygon()
    assert P.is_polygon_reduced()
    # Caso A211 su tutti i vertici
    P = Polygon([Vertex("v1", -0.866025, 0.5), Vertex("v2", 0.866025, 0.5),
                Vertex("v3", -0.707107, 0.707107), Vertex("v4",
                                                          0.707107, -0.707107),
                Vertex("v5", 0.707107, 0.707107), Vertex("v6", 0, -1),
                Vertex("v7", -0.866025, -0.5), Vertex("v8", 0, 1)])
    P.reduce_polygon()
    assert P.is_polygon_reduced()
    # Caso A212 su tutti i vertici
    P = Polygon([Vertex("v1", -0.866025, 0.5), Vertex("v2", 1, 0),
                Vertex("v3", -0.707107, 0.707107), Vertex("v4",
                                                          0.707107, -0.707107),
                Vertex("v5", 0.707107, 0.707107), Vertex("v6", 0, -1),
                Vertex("v7", -0.866025, -0.5), Vertex("v8", 0.866025, 0.5)])
    P.reduce_polygon()
    assert P.is_polygon_reduced()
    # Caso A22 su tutti i vertici
    P = Polygon([Vertex("v1", -0.866025, 0.5), Vertex("v2", 1, 0),
                Vertex("v3", -0.707107, 0.707107), Vertex("v4",
                                                          0.707107, -0.707107),
                Vertex("v5", 0.707107, 0.707107), Vertex(
        "v6", -0.707107, -0.707107),
        Vertex("v7", 0, 1), Vertex("v8", 0, -1)])
    P.reduce_polygon()
    assert P.is_polygon_reduced()
    # Caso A231 su tutti i vertici
    P = Polygon([Vertex("v1", -0.866025, 0.5), Vertex("v2", 1, 0),
                Vertex("v3", 0, 1), Vertex("v4",
                                           0, -1),
                Vertex("v5", -0.707107, -0.707107), Vertex(
        "v6", 0.707107, -0.707107),
        Vertex("v7", -0.707107, 0.707107)])
    P.reduce_polygon()
    assert P.is_polygon_reduced()
    # Caso A2321 su tutti i vertici
    P = Polygon([Vertex("v1", -1, 0), Vertex("v2", 1, 0),
                Vertex("v3", 0, 1), Vertex("v4",
                                           0, -1),
                Vertex("v5", -0.707107, -0.707107), Vertex(
        "v6", 0.707107, -0.707107),
        Vertex("v7", -0.866025, -0.5), Vertex(
        "v8", 0.866025, 0.5)])
    P.reduce_polygon()
    assert P.is_polygon_reduced()
    # Caso A2322 su tutti i vertici
    P = Polygon([Vertex("v1", -1, 0), Vertex("v2", 1, 0),
                Vertex("v3", 0, 1), Vertex("v4",
                                           0.707107, -0.707107),
                Vertex("v5", -0.707107, -0.707107), Vertex(
        "v6", 0.866025, -0.5),
        Vertex("v7", -0.866025, -0.5), Vertex(
        "v8", 0, -1)])
    P.reduce_polygon()
    assert P.is_polygon_reduced()
    # Caso B21 su tutti i vertici
    P = Polygon([Vertex("v1", -1, 0), Vertex("v2", 1, 0),
                Vertex("v3", 0, 1), Vertex("v4",
                                           0, -1),
                Vertex("v5", 0.707107, -0.707107), Vertex(
        "v6", 0.5, -0.866025)
    ])
    P.reduce_polygon()
    assert P.is_polygon_reduced()
    # Caso B2211 su tutti i vertici
    P = Polygon([Vertex("v1", -1, 0), Vertex("v2", 1, 0),
                Vertex("v3", 0, 1), Vertex("v4",
                                           0, -1),
                Vertex("v5", 0.707107, -0.707107), Vertex(
        "v6", -0.5, -0.866025), Vertex("v7", 0.866025, 0.5)
    ])
    P.reduce_polygon()
    assert P.is_polygon_reduced()
    # Caso B22121 su tutti i vertici
    P = Polygon([Vertex("v1", -1, 0), Vertex("v2", 1, 0),
                Vertex("v3", 0, 1), Vertex("v4",
                                           0, -1),
                Vertex("v5", 0.707107, -0.707107), Vertex(
        "v6", -0.5, -0.866025), Vertex("v7", 0.866025, -0.5), Vertex("v8", -0.5, 0.866025)
    ])
    P.reduce_polygon()
    assert P.is_polygon_reduced()
    # Caso B22122 su tutti i vertici
    P = Polygon([Vertex("v1", -1, 0), Vertex("v2", 1, 0),
                Vertex("v3", 0, 1), Vertex("v4",
                                           0, -1),
                Vertex("v5", 0.707107, -0.707107), Vertex(
        "v6", -0.866025, -0.5), Vertex("v7", 0.866025, -0.5), Vertex("v8", -0.5, -0.866025)
    ])
    P.reduce_polygon()
    assert P.is_polygon_reduced()
    # Caso B222 su tutti i vertici
    P = Polygon([Vertex("v1", -1, 0), Vertex("v2", 1, 0),
                Vertex("v3", -0.707107, 0.707107), Vertex("v4",
                                                          0, -1),
                Vertex("v5", 0, 1), Vertex(
        "v6", -0.866025, -0.5), Vertex("v7", 0.866025, -0.5), Vertex("v8", 0.5, 0.866025)
    ])
    P.reduce_polygon()
    assert P.is_polygon_reduced()
    # Caso C1 su tutti i vertici
    P = Polygon([Vertex("v1", -0.866025, 0.5),
                Vertex("v2", 0.866025, 0.5), Vertex("v3", -0.707107, 0.707107),
                Vertex("v4", 0.707107, 0.707107), Vertex("v5", 0, 1)])
    P.reduce_polygon()
    assert P.is_polygon_reduced()
    # Caso C211 su tutti i vertici
    P = Polygon([Vertex("v1", -0.866025, 0.5), Vertex("v2", 0.866025, 0.5),
                Vertex("v3", -0.707107, 0.707107), Vertex("v4",
                                                          0, -1),
                Vertex("v5", 0.707107, 0.707107), Vertex(
                    "v6", 0.707107, -0.707107),
                Vertex("v7", 0.5, -0.866025)])
    P.reduce_polygon()
    assert P.is_polygon_reduced()
    # Caso C212 su tutti i vertici
    P = Polygon([Vertex("v1", -0.866025, 0.5), Vertex("v2", 0.866025, 0.5),
                Vertex("v3", -0.707107, 0.707107), Vertex("v4",
                                                          0, -1),
                Vertex("v5", 0.707107, 0.707107), Vertex(
                    "v6", 0.707107, -0.707107),
                Vertex("v7", -0.5, -0.866025)])
    P.reduce_polygon()
    assert P.is_polygon_reduced()
    # Caso C22 su v8  RISOLTO MANUALMENTE CONSIDERANDO C22
    P = Polygon([Vertex("v1", -0.866025, 0.5), Vertex("v2", 1, 0),
                Vertex("v3", 0.707107, 0.707107), Vertex("v4",
                                                         0.707107, -0.707107),
                Vertex("v5", -0.707107, 0.707107), Vertex(
                    "v6", -0.707107, -0.707107),
                Vertex("v7", 0.5, 0.866025),
                Vertex("v8", 0, -1), Vertex("v9", 0, 1)])
    P.reduce_polygon()
    assert P.is_polygon_reduced()
    P = Polygon(
        [
            Vertex("v1", 0.4151333452873365, -0.9097605759926867),
            Vertex("v2", 0.4660853714569506, 0.8847397507255094),
            Vertex("v3", -0.04901314988810457, -0.9987981333272736),
            Vertex("v4", -0.33200881737487076, 0.9432762825309134),
            Vertex("v5", -0.5179906796570459, -0.8553862611641783),
            Vertex("v6", 0.5447833116815444, -0.8385768559370628),
            Vertex("v7", -0.9427412284073673, 0.3335250759102951),
            Vertex("v8", 0.21846212384139263, 0.9758454285626941),
            Vertex("v9", 0.04214390550647695, -0.9991115509434676),
            Vertex("v10", 0.11180311253381658, 0.9937303779334467),
        ]
    )
    P.reduce_polygon()
    assert P.is_polygon_reduced()

    # Risolto manualmente considerando C2322
    P = Polygon([
        Vertex("v1", 0.9822979314554909, -0.1873253155829816),
        Vertex("v2", -0.8676696270010948, 0.4971412459048042),
        Vertex("v3", -0.4846368510846364, -0.8747154523448),
        Vertex("v4", -0.29340126152361345, -0.955989382648339),
        Vertex("v5", -0.3602401598579339, -0.9328595967376496),
        Vertex("v6", 0.2503476116287866, -0.9681560170508482),
        Vertex("v7", -0.7014911941776061, 0.7126781212379655),
        Vertex("v8", 0.17165646568010495, -0.9851568696356002),
        Vertex("v9", 0.7087614959245248, 0.7054481851240599),
        Vertex("v10", 0.9340723516373792, -0.35708380235823656)
    ])
    P.reduce_polygon()
    assert P.is_polygon_reduced()

    # Risolto con casi limite C212 e D211
    P = Polygon([
        Vertex("v1", -0.027064249416564268, 0.99963369611249),
        Vertex("v2", -0.47046008597247124, 0.8824212755293103),
        Vertex("v3", 0.043156452696938574, -0.999068326287355),
        Vertex("v4", 0.5789189989831471, 0.8153850578814594),
        Vertex("v5", -0.6194249797590352, 0.7850558543508346),
        Vertex("v6", -0.6988412987788333, 0.7152767570116573),
        Vertex("v7", -0.9469475854993759, -0.3213880369847364),
        Vertex("v8", 0.8233008094392888, 0.5676053005184253),
        Vertex("v9", 0.32845338780422884, -0.9445201808537099),
        Vertex("v10", -0.09221411342817709, -0.9957392014401438)
    ])
    P.reduce_polygon()
    assert P.is_polygon_reduced()

    # Caso in cui inizia come sinistrorsa e diventa desrtrorsa
    # Ancora da ridurre
    P = Polygon([
        Vertex("v1", 0.3437300059454709, 0.9390685188061234),
        Vertex("v2", -0.1664430775964021, 0.9860510645601668),
        Vertex("v3", 0.9364502081098824, 0.3508005241315324),
        Vertex("v4", 0.40515783346200185, -0.9142467555230245),
        Vertex("v5", 0.37018462362294713, -0.9289582038138944),
        Vertex("v6", -0.5671139068187114, -0.8236393729617459),
        Vertex("v7", 0.2411510433589672, 0.9704875961530274),
        Vertex("v8", 0.20813455918082324, -0.9781002020624494),
        Vertex("v9", -0.8931146784951343, 0.44982904647936306),
        Vertex("v10", -0.04240571295747442, 0.9991004731800343)
    ])
    # Quando l'algoritmo sarà finito
    """for i in range(1, 100):
        P = generate_random_polygon(10)
        P.reduce_polygon()
        assert P.is_polygon_reduced()"""
