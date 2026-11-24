import map
import contexts
from farm_common import harvest_with_companion, plant_crop
import farm_hay

SUNFLOWER_PATTERNS_KEY = "sunflower_patterns"
NO_OVERPLANTS = [ Entities.Sunflower ]

def get_crop_costs(count, ctx):
	component_costs = get_cost(Entities.Sunflower)
	plot_yield = 2**(num_unlocked(Unlocks.Sunflowers) - 1) * 8 # harvested in order to get gain

	component_crop_costs = {}
	for item in component_costs:
		item_count = component_costs[item]
		component_crop_costs[item] = farm.get_crop_costs(item_count * count / plot_yield)	
	
	return count, component_crop_costs

def plant_sunflower():
	if get_ground_type() != Grounds.Soil:
		till()
	return plant(Entities.Sunflower)

def _plant_plot(ctx):
	harvest_with_companion(ctx, True, NO_OVERPLANTS)
	if not plant_crop(ctx, plant_sunflower):
		return False
	
	contexts.get_value(ctx, SUNFLOWER_PATTERNS_KEY)[measure() - 7].append((get_pos_x(), get_pos_y()))
	
	return True

def _harvest_plot(ctx):
	harvest_with_companion(ctx, True, NO_OVERPLANTS)
	farm_hay.farm_plot(ctx)    
	return True

def _init_patterns():
	patterns = []
	for petals in range(7, 16):
		patterns.append([])
	return patterns

def farm(ctx):
	
	change_hat(Hats.Sunflower_Hat)
	plant_pat = map.create_serpentine_pattern(ctx)	
	harvest_pats = _init_patterns()
	local_ctx = contexts.create_override(ctx)
	contexts.set_value(local_ctx, SUNFLOWER_PATTERNS_KEY, harvest_pats)
	if not map.do_for_pattern(plant_pat, _plant_plot, local_ctx):
		return False
	
	for petals in range(len(harvest_pats) - 1, -1, -1):
		pat = harvest_pats[petals]
		if len(pat) == 0:
			continue
		if not map.do_for_pattern(pat, _harvest_plot, ctx):
			return False
	
	return True