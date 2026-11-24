import map
import contexts
from farm_common import harvest_with_companion, plant_crop

CACTUS_LIST_KEY = "cactii"
NO_OVERPLANTS = [ Entities.Cactus ]

def get_crop_costs(count, ctx):
	if count == 0:
		return 0, {}

	_, _, cx, cy, _ = contexts.get_area(ctx)

	component_costs = get_cost(Entities.Cactus)
	plot_yield = 2**(num_unlocked(Unlocks.Cactus) - 1)
	plot_count = cx * cy
	crop_yield = plot_count ** 2 * plot_yield
	crops_needed = max(count / crop_yield, 1)
	count_needed = crops_needed * plot_count

	component_crop_costs = {}
	for item in component_costs:
		count = component_costs[item]
		component_crop_costs[item] = farm.get_crop_costs(count_needed * count)
	
	return count, component_crop_costs

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
	
def farm(ctx):
	change_hat(Hats.Cactus_Hat)
	pat = map.create_serpentine_pattern(ctx)
	local_ctx = contexts.create_override(ctx)

	# plant all cactii and wait for them to mature
	while True:
		next_pat = []
		contexts.set_value(local_ctx, CACTUS_LIST_KEY, next_pat)
		map.do_for_pattern(pat, farm_plot, local_ctx)
		pat = next_pat
		if len(pat) == 0:
			break
	
	# sort them
	xi, yi, dx, dy, _ = contexts.get_area(ctx)
	
	for row in range(yi, yi + dy):
		map.move_to(xi, row)
		_sort_line(xi, dx, East, West)
				
	for col in range(xi, xi + dx):
		map.move_to(col, yi)
		_sort_line(yi, dy, North, South)
	
	return harvest()
	