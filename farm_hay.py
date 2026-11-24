import map
import contexts
from farm_common import harvest_with_companion, plant_crop

NO_OVERPLANTS = [ ]

def get_crop_costs(count, ctx):
	return count, {}

def plant_grass():
	return plant(Entities.Grass)
	
# plant/harvest hay
def farm_plot(ctx):
	global NO_OVERPLANTS
	
	harvest_with_companion(ctx, True, NO_OVERPLANTS)
	plant_crop(ctx, plant_grass)
	
	return True
	
def farm(ctx):
	change_hat(Hats.Straw_Hat)
	pat = map.create_serpentine_pattern(ctx)
	return map.do_for_pattern(pat, farm_plot, ctx)
	
