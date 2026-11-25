from common import ceil
import map
import areas
import contexts
from farm_common import harvest_with_companion, plant_crop, NO_COSTS, get_unlock_yield, get_polyculture_yield
import farm_context

NO_OVERPLANTS = [ ]

def get_crop_costs(count, ctx):
	if count < 1:
		return NO_COSTS
	
	_, _, cx, cy, _ = contexts.get_area(ctx)
	plot_yield = get_unlock_yield(Unlocks.Carrots) * get_polyculture_yield()
	crop_yield = cx * cy * plot_yield
	crop_count = ceil(count / crop_yield)
	total_yield = crop_count * crop_yield

	component_need_count = total_yield / plot_yield
	component_costs = get_cost(Entities.Carrot)
	component_crop_costs = {}
	for item in component_costs:
		item_count = component_costs[item]
		component_crop_costs[item] = farm.get_crop_costs(ctx, item, component_need_count * item_count)	
	
	return crop_count, total_yield, component_crop_costs

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
		
def farm_crop_block(ctx):
	change_hat(Hats.Carrot_Hat)
	pat = map.create_serpentine_pattern(ctx)
	while True:
		if not map.do_for_pattern(pat, farm_plot, ctx):
			return False
		if farm_context.check_farming_goal(ctx):
			return True

def _farm_block(ctx, bx, by, bcx, bcy):
	x0, y0, cx, cy, _ = contexts.get_area(ctx)
	block_ctx = contexts.create_override_slice(ctx, areas.create_relative(bx * bcx, by * bcy, 4, 8))
	drone = spawn_drone(farm_crop_block, block_ctx)
	if drone != None:
		return drone
	
	farm_crop_block(block_ctx)
	return None

def farm_crop(ctx):

	# plant all and patrol until healthy
	x0, y0, cx, cy, _ = contexts.get_area(ctx)
	map.move_to(cx // 2, cy // 2)
	drones = []
	for col in range(0, 8):
		for row in range(0, 4):
			drone = _farm_block(ctx, col, row, 4, 8)
			if drone != None:
				drones.append(drone)
	for drone in drones:
		wait_for(drone)

	# # plant all and patrol until healthy
	# x0, y0, cx, cy, _ = contexts.get_area(ctx)
	# drones = []
	# for col in range(x0 + 1, x0 + cx):
	# 	drone = spawn_drone(_plant_col_d, (col, y0, cy))
	# 	drones.append(drone)
	# _plant_col_d((x0, y0, cy))
	# for drone in drones:
	# 	wait_for(drone)
	
	#harvest()

	return True