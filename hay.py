import map
import farm_context
from farm_common import harvest_with_companion

NO_OVERPLANTS = [ ]

def plant_grass():
	return plant(Entities.Grass)
	
# plant/harvest hay
def farm_plot(context):
	global NO_OVERPLANTS
	
	harvest_with_companion(context, True, NO_OVERPLANTS)
	farm_context.plant_crop(context, plant_grass)
	
	return True
	
def farm(context):
	change_hat(Hats.Straw_Hat)
	pat = map.create_serpentine_pattern(context["area"])
	return map.do_for_pattern(pat, farm_plot, context)
	
