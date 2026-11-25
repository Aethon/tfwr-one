import map
import areas
import contexts
import farm_hay
import farm_wood
import farm_carrots
import farm_pumpkin
import farm_power
import farm_cactus
import farm_weird
import testing

# area: area to work tests in; must be normalized
def test_hay(area):
	ctx = contexts.create_override_slice(map.get_context(), area)
	plot_pos = areas.get_base_pos((0, 0), area)	
	map.move_to_pos(plot_pos)

	harvest()
	testing.assert(farm_hay.plant_grass(), "planting grass on empty")
	
	farm_wood.plant_bush()
	testing.assert_not(farm_hay.plant_grass(), "planting grass on non-empty")
	
	testing.assert(farm_hay.farm_crop(ctx), "farming hay")

def test_wood(area):
	ctx = contexts.create_override_slice(map.get_context(), area)
	plot_pos = areas.get_base_pos((0, 0), area)	
	map.move_to_pos(plot_pos)	
	
	# plants on empty
	harvest()
	testing.assert(farm_wood.plant_bush(), "planting bush on empty")
	
	# does not plant on non-empty
	testing.assert_not(farm_wood.plant_bush(), "planting bush on non-empty")
		
	# plants on empty	
	harvest()
	testing.assert(farm_wood.plant_tree(), "planting tree on empty")

	# does not plant on non-empty
	testing.assert_not(farm_wood.plant_tree(), "planting tree on non-empty")
			
	testing.assert(farm_wood.farm_crop(ctx), "farming wood")
	
def test_carrots(area):
	ctx = contexts.create_override_slice(map.get_context(), area)
	plot_pos = areas.get_base_pos((0, 0), area)	
	map.move_to_pos(plot_pos)	
	
	# plants on empty
	harvest()
	testing.assert(farm_carrots.plant_carrots(), "planting carrots on empty")
	
	# does not plant on non-empty
	testing.assert_not(farm_carrots.plant_carrots(), "planting carrots on non-empty")
					
	testing.assert(farm_carrots.farm_crop(ctx), "farming carrots")
	
def test_pumpkin(area):
	ctx = contexts.create_override_slice(map.get_context(), area)	
						
	testing.assert(farm_pumpkin.farm_crop(ctx), "farming pumpkin")
	
def test_power(area):
	ctx = contexts.create_override_slice(map.get_context(), area)
						
	testing.assert(farm_power.farm_crop(ctx), "farming power")
	
def test_cactus(area):
	ctx = contexts.create_override_slice(map.get_context(), area)
						
	testing.assert(farm_cactus.farm_crop(ctx), "farming cactus")
	
def test_weird(area):
	ctx = contexts.create_override_slice(map.get_context(), area)
						
	testing.assert(farm_weird.farm_crop(ctx), "farming strange")