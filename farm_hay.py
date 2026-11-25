from common import ceil
import map
import contexts
from farm_common import harvest_with_companion, plant_crop, NO_COSTS, get_unlock_yield, get_polyculture_yield

NO_OVERPLANTS = [ ]

def get_crop_costs(count, ctx):
	if count < 1:
		return NO_COSTS

	_, _, cx, cy, _ = contexts.get_area(ctx)
	plot_yield = get_unlock_yield(Unlocks.Grass) * get_polyculture_yield()
	crop_yield = cx * cy * plot_yield
	crop_count = ceil(count / crop_yield)
	total_yield = crop_count * crop_yield

	return crop_count, total_yield, {}

def plant_grass():
	return plant(Entities.Grass)
	
# plant/harvest hay
def farm_plot(ctx):
	global NO_OVERPLANTS
	
	harvest_with_companion(ctx, True, NO_OVERPLANTS)
	plant_crop(ctx, plant_grass)
	
	return True
	
def farm_crop(ctx):
	change_hat(Hats.Straw_Hat)
	pat = map.create_serpentine_pattern(ctx)
	return map.do_for_pattern(pat, farm_plot, ctx)
	
