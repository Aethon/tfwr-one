import map
import contexts
import farm_context
from farm_common import harvest_with_companion, plant_crop

PUMPKIN_LIST_KEY = "pumpkins"
NO_OVERPLANTS = [ Entities.Pumpkin ]

def get_crop_costs(count, ctx):
	component_costs = get_cost(Entities.Pumpkin)
	plot_yield = 2**(num_unlocked(Unlocks.Pumpkin) - 1) * 0.7 # reduced for failure rate (20% +breathing room)

	component_crop_costs = {}
	for item in component_costs:
		item_count = component_costs[item]
		component_crop_costs[item] = farm.get_crop_costs(item_count * count / plot_yield)	
	
	return count, component_crop_costs

def plant_pumpkin():
	return plant(Entities.Pumpkin)

def farm_plot(ctx):
	
	if get_entity_type() == Entities.Pumpkin:
		if can_harvest():
			# all good; no need to come back
			return True
	else:        
		harvest_with_companion(ctx, True, NO_OVERPLANTS)
		if get_ground_type() != Grounds.Soil:
			till()
		plant_crop(ctx, plant_pumpkin)
		
	# need to come back and check on it
	contexts.get_value(ctx, PUMPKIN_LIST_KEY).append((get_pos_x(), get_pos_y()))
	return True
	
def farm(ctx):

	change_hat(Hats.Pumpkin_Hat)
	pat = map.create_serpentine_pattern(ctx)
	local_ctx = contexts.create_override(ctx)
	while True:
		next_pat = []
		contexts.set_value(local_ctx, PUMPKIN_LIST_KEY, next_pat)
		if not map.do_for_pattern(pat, farm_plot, local_ctx):
			return False
		pat = next_pat
		if len(pat) == 0:
			break
		farm_context.set_water_to(local_ctx, 0.5) # only water on the cleanup passes
		
	return harvest()
