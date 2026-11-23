import testing
import map
import farming_tests

map.init(None, None)

farming_tests.test_hay((0, 0, 5, 5))
farming_tests.test_wood((5, 0, 5, 5))
farming_tests.test_carrots((10, 0, 5, 5))
farming_tests.test_pumpkin((15, 0, 5, 5))
farming_tests.test_power((20, 0, 5, 5))
farming_tests.test_cactus((25, 0, 5, 5))
farming_tests.test_strange((0, 5, 5, 5))