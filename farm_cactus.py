from common import ceil
import map
import contexts
from farm_common import harvest_with_companion, plant_crop, NO_COSTS, get_unlock_yield

CACTUS_LIST_KEY = "cactii"
NO_OVERPLANTS = [ Entities.Cactus ]

def get_crop_costs(count, ctx):
	if count < 1:
		return NO_COSTS

	_, _, cx, cy, _ = contexts.get_area(ctx)
	plot_yield = get_unlock_yield(Unlocks.Cactus)
	plot_count = cx * cy
	crop_yield = plot_count ** 2 * plot_yield
	crops_needed = ceil(count / crop_yield)
	total_yield = crop_count * crop_yield
	
	component_need_count = total_yield / plot_yield
	component_costs = get_cost(Entities.Cactus)
	component_crop_costs = {}
	for item in component_costs:
		item_count = component_costs[item]
		component_crop_costs[item] = farm.get_crop_costs(ctx, item, component_count_needed * item_count)
	
	return crop_count, total_yield, component_crop_costs

def plant_cactus():
	if get_ground_type() != Grounds.Soil:
		till()
	return plant(Entities.Cactus)

def farm_plot(ctx):
	
	if get_entity_type() == Entities.Cactus:
		if can_harvest():
			# all good; no need to come back
			return True
	else:        
		harvest_with_companion(ctx, True, NO_OVERPLANTS)
		if not plant_crop(ctx, plant_cactus):
			return False

	# need to come back and check on it
	contexts.get_value(ctx, CACTUS_LIST_KEY).append((get_pos_x(), get_pos_y()))
	return True

def _sort_line_pass_forward(start, end, direction):

	changed = False
	for n in range(start, end - 1):
		this = measure()
		that = measure(direction)
		if (that < this):
			swap(direction)
			changed = True
		move(direction)

	return changed

def _sort_line_pass_backward(start, end, direction,):

	changed = False
	for n in range(end, start + 1, -1):
		this = measure()
		that = measure(direction)
		if (that > this):
			swap(direction)
			changed = True
		move(direction)

	return changed

def _sort_line(start, count, forward, backward):
	n0 = start
	nn = n0 + count
	while True:
		if not _sort_line_pass_forward(n0, nn, forward):
			return
		move(backward)
		nn = nn - 1

		if not _sort_line_pass_backward(n0, nn, backward):
			return
		move(forward)
		n0 = n0 + 1

def _plant_line_d(info):
	col, y0, cy = info
	for row in range(y0, y0 + cy):
		map.move_to(col, row)
		plant_cactus()

	ready = False
	while not ready:
		ready = True
		for row in range(y0, y0 + cy):
			map.move_to(col, row)
			if not can_harvest():
				ready = False

def _sort_row_d(info):
	row, x0, cx = info
	map.move_to(x0, row)
	_sort_line(x0, cx, East, West)

def _sort_col_d(info):
	col, y0, cy = info
	map.move_to(col, y0)
	_sort_line(y0, cy, North, South)

def _plant_with_drones(ctx):
	x0, y0, cx, cy, _ = contexts.get_area(ctx)
	drones = []
	for col in range(x0, x0 + cx):
		drones.append(spawn_drone(_plant_line_d, (col, y0, cy)))
	for drone in drones:
		wait_for(drone)

def _sort_with_drones(ctx):
	x0, y0, cx, cy, _ = contexts.get_area(ctx)
	drones = []
	for row in range(y0 + 1, y0 + cy):
		drone = spawn_drone(_sort_row_d, (row, x0, cx))
		drones.append(drone)
	_sort_row_d((y0, x0, cx))
	for drone in drones:
		wait_for(drone)

	drones = []	
	for col in range(x0 + 1, x0 + cx):
		drone = spawn_drone(_sort_col_d, (col, y0, cy))
		drones.append(drone)
	_sort_col_d((x0, y0, cy))
	for drone in drones:
		wait_for(drone)

def farm_crop(ctx):
	change_hat(Hats.Cactus_Hat)

	# plant all cactii and wait for them to mature
	x0, y0, cx, cy, _ = contexts.get_area(ctx)
	drones = []
	for col in range(x0 + 1, x0 + cx):
		drone = spawn_drone(_plant_line_d, (col, y0, cy))
		drones.append(drone)
	_plant_line_d((x0, y0, cy))

	for drone in drones:
		wait_for(drone)

	# sort them
	drones = []
	for row in range(y0 + 1, y0 + cy):
		drone = spawn_drone(_sort_row_d, (row, x0, cx))
		drones.append(drone)
	_sort_row_d((y0, x0, cx))
	for drone in drones:
		wait_for(drone)

	drones = []	
	for col in range(x0 + 1, x0 + cx):
		drone = spawn_drone(_sort_col_d, (col, y0, cy))
		drones.append(drone)
	_sort_col_d((x0, y0, cy))
	for drone in drones:
		wait_for(drone)
	
	return harvest()
	