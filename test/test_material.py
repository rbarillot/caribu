from math import isnan, sqrt
from nose.tools import assert_almost_equal

from alinea.caribu.caribu import radiosity, raycasting


def test_raycasting_translucent():
    points = [(0, 0, 0), (sqrt(2), 0, 0), (0, sqrt(2), 0)]
    triangles = [points]
    lights = [(100, (0, 0, -1))]

    # no reflectance, black body
    materials = [(0., 0.)]
    res = raycasting(triangles, materials, lights)
    assert_almost_equal(res['area'][0], 1, 3)
    assert_almost_equal(res['Ei_sup'][0], -1, 3)
    assert_almost_equal(res['Ei_inf'][0], -1, 3)
    assert isnan(res['Eabs'][0])

    # full reflectance, mirror
    materials = [(1., 0.)]
    res = raycasting(triangles, materials, lights)
    assert_almost_equal(res['area'][0], 1, 3)
    assert_almost_equal(res['Ei_sup'][0], 100, 0)
    assert_almost_equal(res['Ei_inf'][0], 0, 3)
    assert_almost_equal(res['Eabs'][0], 0, 3)

    # semi reflectance
    materials = [(0.5, 0.)]
    res = raycasting(triangles, materials, lights)
    assert_almost_equal(res['area'][0], 1, 3)
    assert_almost_equal(res['Ei_sup'][0], 100, 0)
    assert_almost_equal(res['Ei_inf'][0], 0, 3)
    assert_almost_equal(res['Eabs'][0], 50, 0)


def test_raycasting_opaque():
    points = [(0, 0, 0), (sqrt(2), 0, 0), (0, sqrt(2), 0)]
    triangles = [points]
    lights = [(100, (0, 0, -1))]

    # no reflectance, black body
    materials = [(0., )]
    res = raycasting(triangles, materials, lights)
    assert_almost_equal(res['area'][0], 1, 3)
    assert_almost_equal(res['Ei_sup'][0], -1, 3)
    assert_almost_equal(res['Ei_inf'][0], -1, 3)
    assert_almost_equal(res['Eabs'][0], -1, 3)

    # top
    materials = [(0.1,)]
    res = raycasting(triangles, materials, lights)
    assert_almost_equal(res['area'][0], 1, 3)
    assert_almost_equal(res['Ei_sup'][0], 100, 0)
    assert_almost_equal(res['Ei_inf'][0], -1, 0)
    assert_almost_equal(res['Eabs'][0], 90, 0)

    # bottom
    # triangles = [[points[0], points[2], points[1]]]
    # materials = [(0.1,)]
    # res = raycasting(triangles, materials, lights)
    # assert_almost_equal(res['area'][0], 1, 3)
    # assert_almost_equal(res['Ei_sup'][0], -1, 0)
    # assert_almost_equal(res['Ei_inf'][0], 100, 0)
    # assert_almost_equal(res['Eabs'][0], 90, 0)


def test_raycasting_closed_box():
    pts1 = [(0, 0, 0), (1, 0, 0), (0, 0, 1)]
    pts2 = [(0, 0, 0), (0, 0, 1), (0, 1, 0)]
    pts3 = [(0, 0, 0), (0, 1, 0), (1, 0, 0)]
    pts4 = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
    triangles = [pts1, pts2, pts3, pts4]
    lights = [(100, (0, 0, -1))]

    # no transmittance
    materials = [(0.1, 0.)] * len(triangles)
    res = raycasting(triangles, materials, lights)
    assert_almost_equal(res['area'][0], 0.5, 3)
    assert_almost_equal(res['Ei_sup'][0], 0, 3)
    assert_almost_equal(res['Ei_inf'][0], 0, 3)
    assert_almost_equal(res['Eabs'][0], 0, 3)

    assert_almost_equal(res['area'][1], 0.5, 3)
    assert_almost_equal(res['Ei_sup'][1], 0, 3)
    assert_almost_equal(res['Ei_inf'][1], 0, 3)
    assert_almost_equal(res['Eabs'][1], 0, 3)

    assert_almost_equal(res['area'][2], 0.5, 3)
    assert_almost_equal(res['Ei_sup'][2], 0, 3)
    assert_almost_equal(res['Ei_inf'][2], 0, 0)
    assert_almost_equal(res['Eabs'][2], 0, 0)

    assert_almost_equal(res['area'][3], 0.866, 3)  # TODO
    assert_almost_equal(res['Ei_sup'][3], 57.6, 0)
    assert_almost_equal(res['Ei_inf'][3], 0, 3)
    assert_almost_equal(res['Eabs'][3], 57.6 * 0.9, 0)


def test_raycasting_opaque_box():
    # need a closed box
    pts1 = [(0, 0, 0), (1, 0, 0), (0, 0, 1)]
    pts2 = [(0, 0, 0), (0, 0, 1), (0, 1, 0)]
    pts3 = [(0, 0, 0), (0, 1, 0), (1, 0, 0)]
    pts4 = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
    triangles = [pts1, pts2, pts3, pts4]
    lights = [(100, (0, 0, -1))]

    # no reflectance, black body
    materials = [(0.1, )] * len(triangles)
    res = raycasting(triangles, materials, lights)
    assert_almost_equal(res['area'][0], 0.5, 3)
    # assert_almost_equal(res['Ei_sup'][0], 0, 3)
    # assert_almost_equal(res['Ei_inf'][0], 0, 3)
    assert_almost_equal(res['Eabs'][0], 0, 3)

    assert_almost_equal(res['area'][1], 0.5, 3)
    # assert_almost_equal(res['Ei_sup'][1], 0, 3)
    # assert_almost_equal(res['Ei_inf'][1], 0, 3)
    assert_almost_equal(res['Eabs'][1], 0, 3)

    assert_almost_equal(res['area'][2], 0.5, 3)
    # assert_almost_equal(res['Ei_sup'][2], 0, 3)
    # assert_almost_equal(res['Ei_inf'][2], 0, 0)
    assert_almost_equal(res['Eabs'][2], 0, 0)

    assert_almost_equal(res['area'][3], 0.866, 3)  # TODO
    # assert_almost_equal(res['Ei_sup'][3], 57.6, 0)
    # assert_almost_equal(res['Ei_inf'][3], 0, 3)
    assert_almost_equal(res['Eabs'][3], 57.6 * 0.9, 0)


def test_raycasting_asymmetric_material():
    points = [(0, 0, 0), (sqrt(2), 0, 0), (0, sqrt(2), 0)]
    triangles = [points]
    lights = [(100, (0, 0, -1))]
    materials = [(0.1, 0., 0.2, 0.)]

    # top
    res = raycasting(triangles, materials, lights)
    assert_almost_equal(res['area'][0], 1, 3)
    assert_almost_equal(res['Ei_sup'][0], 100, 0)
    assert_almost_equal(res['Ei_inf'][0], 0, 0)
    assert_almost_equal(res['Eabs'][0], 90, 0)

    # bottom
    triangles = [reversed(points)]
    res = raycasting(triangles, materials, lights)
    assert_almost_equal(res['area'][0], 1, 3)
    assert_almost_equal(res['Ei_sup'][0], 0, 0)
    assert_almost_equal(res['Ei_inf'][0], 100, 0)
    assert_almost_equal(res['Eabs'][0], 80, 0)
