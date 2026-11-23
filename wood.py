import map
from farm_common import harvest_with_companion
import hay

NO_OVERPLANTS = [ Entities.Tree ]
	
def plant_bush():
	return plant(Entities.Bush)
	
def plant_tree():
	return plant(Entities.Tree)

# plant/harvest wood and hay
def farm_plot(context):
	global NO_OVERPLANTS
		
	if (get_pos_x() + get_pos_y()) % 2 == 1:
		return hay.farm_plot(context)
	
	harvest_with_companion(context, True, NO_OVERPLANTS)
	plant_tree()
	return True

	
def farm(context):
	change_hat(Hats.Tree_Hat)
	pat = map.create_serpentine_pattern(context["area"])
	return map.do_for_pattern(pat, farm_plot, context)
