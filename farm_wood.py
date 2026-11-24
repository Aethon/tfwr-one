import map
import contexts
from farm_common import harvest_with_companion, plant_crop
import farm_hay

NO_OVERPLANTS = [ Entities.Tree ]
	
def plant_bush():
	return plant(Entities.Bush)
	
def plant_tree():
	return plant(Entities.Tree)

# plant/harvest wood and hay
def farm_plot(ctx):
	global NO_OVERPLANTS
		
	if (get_pos_x() + get_pos_y()) % 2 == 1:
		return farm_hay.farm_plot(ctx)
	
	harvest_with_companion(ctx, True, NO_OVERPLANTS)
	plant_crop(ctx, plant_tree)

	return True

	
def farm(ctx):
	change_hat(Hats.Tree_Hat)
	pat = map.create_serpentine_pattern(ctx)
	return map.do_for_pattern(pat, farm_plot, ctx)
