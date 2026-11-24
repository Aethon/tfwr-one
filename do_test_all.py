import testing
import map
import areas
import test_farms
import test_areas


map.init(None, None)

test_areas.test_all()

# test_farms.test_hay(areas.create_relative(0, 0, 5, 5))
# test_farms.test_wood(areas.create_relative(5, 0, 5, 5))
# test_farms.test_carrots(areas.create_relative(10, 0, 5, 5))
# test_farms.test_pumpkin(areas.create_relative(15, 0, 5, 5))
# test_farms.test_power(areas.create_relative(20, 0, 5, 5))
test_farms.test_cactus(areas.create_relative(25, 0, 5, 5))
test_farms.test_weird(areas.create_relative(0, 5, 5, 5))