import testing
import areas

def test_all():
    testing.assert_equal(areas._slice_axis(0, 5, 0, 5), (0, 5)) # exact
    testing.assert_equal(areas._slice_axis(-1, 5, 0, 5), (0, 4)) # before min
    testing.assert_equal(areas._slice_axis(0, 6, 0, 5), (0, 5)) # too long
    testing.assert_equal(areas._slice_axis(3, -1, 0, 5), (3, 0)) # negative length
    testing.assert_equal(areas._slice_axis(0, 100, 0, None), (0, 100)) # unbounded
    testing.assert_equal(areas._slice_axis(-5, 100, 0, None), (0, 95)) # unbounded

    testing.assert_equal(areas._create(-1, -1, 30, 40, True), (0, 0, 29, 39, True))
    testing.assert_equal(areas._create(3, 4, 30, 40, False), (3, 4, 30, 40, False))

    testing.assert_equal(areas.create_relative(0, 0, 10, 15), (0, 0, 10, 15, True))
    testing.assert_equal(areas.create_absolute(0, 0, 10, 15), (0, 0, 10, 15, False))

    abs_base = areas.create_absolute(12, 12, 10, 10)
    rel_base = areas.create_relative(2, 2, 15, 15)
    testing.assert_equal(areas.get_base_area(abs_base, rel_base), areas.create_absolute(14, 14, 8, 8))

    abs_base2 = areas.create_absolute(10, 14, 5, 40)
    testing.assert_equal(areas.get_base_area(abs_base, abs_base2), areas.create_absolute(12, 14, 3, 8))
