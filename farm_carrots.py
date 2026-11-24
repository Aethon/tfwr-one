import map
import contexts
from farm_common import harvest_with_companion, plant_crop

NO_OVERPLANTS = [ Entities.Carrot ]

def plant_carrots():
	if get_ground_type() != Grounds.Soil:
		till()
	return plant(Entities.Carrot)
	
# plant/harvest carrots
def farm_plot(ctx):
	global NO_OVERPLANTS
	
	harvest_with_companion(ctx, True, NO_OVERPLANTS)
	plant_crop(ctx, plant_carrots)
	return True
		
def farm(ctx):
	change_hat(Hats.Carrot_Hat)
	pat = map.create_serpentine_pattern(ctx)
	return map.do_for_pattern(pat, farm_plot, ctx)
