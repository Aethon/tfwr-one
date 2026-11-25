from common import ceil
import map
import contexts
from farm_common import harvest_with_companion, plant_crop, NO_COSTS, get_unlock_yield, get_polyculture_yield
import farm_hay

NO_OVERPLANTS = [ ]

def get_crop_costs(count, ctx):
	if count < 1:
		return NO_COSTS
		
	_, _, cx, cy, _ = contexts.get_area(ctx)
	plot_yield = get_unlock_yield(Unlocks.Trees) * get_polyculture_yield()
	crop_yield = cx * cy * plot_yield / 2 # trees are planted in a checkboard
	crop_count = ceil(count / crop_yield)
	total_yield = crop_count * crop_yield

	return crop_count, total_yield, {}

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
	
def farm_crop(ctx):
	change_hat(Hats.Tree_Hat)
	pat = map.create_serpentine_pattern(ctx)
	return map.do_for_pattern(pat, farm_plot, ctx)
