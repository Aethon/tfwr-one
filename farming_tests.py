import map
import hay
import wood
import carrots
import pumpkin
import power
import cactus
import strange
import testing

# area: area to work tests in; must be normalized
def test_hay(area):
	context = { "area": area }
	plot_pos = map.get_pos_in_area((0, 0), area)
	
	map.move_to_pos(plot_pos)	
	harvest()
	testing.assert(hay.plant_grass(), "planting grass on empty")
	
	wood.plant_bush()
	testing.assert_not(hay.plant_grass(), "planting grass on non-empty")
	
	testing.assert(hay.farm(context), "farming hay")

def test_wood(area):
	context = { "area": area }
	plot_pos = map.get_pos_in_area((0, 0), area)
	
	map.move_to_pos(plot_pos)	
	
	# plants on empty
	harvest()
	testing.assert(wood.plant_bush(), "planting bush on empty")
	
	# does not plant on non-empty
	testing.assert_not(wood.plant_bush(), "planting bush on non-empty")
		
	# plants on empty	
	harvest()
	testing.assert(wood.plant_tree(), "planting tree on empty")

	# does not plant on non-empty
	testing.assert_not(wood.plant_tree(), "planting tree on non-empty")
			
	testing.assert(wood.farm(context), "farming wood")
	
def test_carrots(area):
	context = { "area": area }
	plot_pos = map.get_pos_in_area((0, 0), area)
	
	map.move_to_pos(plot_pos)	
	
	# plants on empty
	harvest()
	testing.assert(carrots.plant_carrots(), "planting carrots on empty")
	
	# does not plant on non-empty
	testing.assert_not(carrots.plant_carrots(), "planting carrots on non-empty")
					
	testing.assert(carrots.farm(context), "farming carrots")
	
def test_pumpkin(area):
	context = { "area": area }
	plot_pos = map.get_pos_in_area((0, 0), area)
	
	map.move_to_pos(plot_pos)	
						
	testing.assert(pumpkin.farm(context), "farming pumpkin")
	
def test_power(area):
	context = { "area": area }
	plot_pos = map.get_pos_in_area((0, 0), area)
	
	map.move_to_pos(plot_pos)	
						
	testing.assert(power.farm(context), "farming power")
	
def test_cactus(area):
	context = { "area": area }
	plot_pos = map.get_pos_in_area((0, 0), area)
	
	map.move_to_pos(plot_pos)	
						
	testing.assert(cactus.farm(context), "farming cactus")
	
def test_strange(area):
	context = { "area": area }
	plot_pos = map.get_pos_in_area((0, 0), area)
	
	map.move_to_pos(plot_pos)
						
	testing.assert(strange.farm(context), "farming strange")