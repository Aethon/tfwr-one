from common import ceil
import map
import areas
import contexts
import farm_context
from farm_common import harvest_with_companion, plant_crop, NO_COSTS, get_unlock_yield

PUMPKIN_LIST_KEY = "pumpkins"
NO_OVERPLANTS = [ Entities.Pumpkin ]

def get_crop_costs(count, ctx):
	if count < 1:
		return NO_COSTS
	
	_, _, cx, cy, _ = contexts.get_area(ctx)
	plot_yield = get_unlock_yield(Unlocks.Pumpkins) * 0.7 # reduced for failure rate (20% +breathing room)
	crop_yield = cx * cy * min(6, min(cy, cy)) # big pumplink multiplier
	crop_count = ceil(count / crop_yield)
	total_yield = crop_count * crop_yield

	component_need_count = total_yield / plot_yield
	component_costs = get_cost(Entities.Pumpkin)
	component_crop_costs = {}
	for item in component_costs:
		item_count = component_costs[item]
		component_crop_costs[item] = farm.get_crop_costs(ctx, item, component_need_count * item_count)	
	
	return crop_count, total_yield, component_crop_costs

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
	
def farm_block_crop(ctx):

	change_hat(Hats.Pumpkin_Hat)
	
	while True:
		local_ctx = contexts.create_override(ctx)
		pat = map.create_serpentine_pattern(local_ctx)
		while True:
			next_pat = []
			contexts.set_value(local_ctx, PUMPKIN_LIST_KEY, next_pat)
			if not map.do_for_pattern(pat, farm_plot, local_ctx):
				return False
			pat = next_pat
			if len(pat) == 0:
				break
			farm_context.set_water_to(local_ctx, 0.5) # only water on the cleanup passes
		harvest()
		
		if farm_context.check_farming_goal(ctx):
			return True
				
# def _plant_col_d(info):
# 	col, y0, cy = info
# 	ready = False
# 	while not ready:
# 		ready = True
# 		for row in range(y0, y0 + cy):
# 			map.move_to(col, row)
# 			if get_entity_type() == Entities.Pumpkin:
# 				if not can_harvest():
# 					ready = False
# 					if get_water() < 0.5 and num_items(Items.Water) > 0:
# 						use_item(Items.Water)
# 			else:        
# 				ready = False
# 				harvest()
# 				if get_ground_type() != Grounds.Soil:
# 					till()
# 				plant_pumpkin()

# def _manage_block_plot(ctx):
# 	if get_entity_type() == Entities.Pumpkin:
# 		if not can_harvest():
# 			ready = False
# 			if get_water() < 0.5 and num_items(Items.Water) > 0:
# 				use_item(Items.Water)
# 	else:        
# 		ready = False
# 		harvest()
# 		if get_ground_type() != Grounds.Soil:
# 			till()
# 		plant_pumpkin()

# def _farm_block_d(info):
# 	ctx = info
# 	pat = map.create_serpentine_pattern(ctx)
# 	ready = False
# 	while not ready:
# 		ready = True
# 		for row in range(y0, y0 + cy):
# 			map.move_to(col, row)
# 			if get_entity_type() == Entities.Pumpkin:
# 				if not can_harvest():
# 					ready = False
# 					if get_water() < 0.5 and num_items(Items.Water) > 0:
# 						use_item(Items.Water)
# 			else:        
# 				ready = False
# 				harvest()
# 				if get_ground_type() != Grounds.Soil:
# 					till()
# 				plant_pumpkin()

def _farm_block(ctx, bx, by, bcx, bcy):
	x0, y0, cx, cy, _ = contexts.get_area(ctx)
	block_ctx = contexts.create_override_slice(ctx, areas.create_relative(bx * bcx, by * bcy, bcx - 1, bcy - 1))
	drone = spawn_drone(farm_block_crop, block_ctx)
	if drone != None:
		return drone
	
	farm_block_crop(block_ctx)
	return None

def farm_crop(ctx):
	
	change_hat(Hats.Pumpkin_Hat)

	# plant all and patrol until healthy
	#x0, y0, cx, cy, _ = contexts.get_area(ctx)
	#map.move_to(cx // 2, cy // 2)
	drones = []
	for col in range(0, 4):
		for row in range(0, 4):
			drone = _farm_block(ctx, col, row, 8, 8)
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
	
	# harvest()

	return True