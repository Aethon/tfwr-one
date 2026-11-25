from common import ceil
import map
import areas
import contexts
import farm_context
from farm_common import harvest_with_companion, plant_crop, NO_COSTS, get_unlock_yield

def get_crop_costs(count, ctx):
	if count < 1:
		return NO_COSTS

	_, _, cx, cy, _ = contexts.get_area(ctx)
	apple_count = cx * cy
	apple_yield = get_unlock_yield(Unlocks.Dinosaurs)
	crop_yield = apple_count ** 2 * apple_yield
	crops_needed = ceil(count / crop_yield)
	total_yield = crop_count * crop_yield
	
	component_count_needed = crops_needed * apple_count
	component_costs = get_cost(Entities.Apple)
	component_crop_costs = {}
	for item in component_costs:
		item_count = component_costs[item]
		component_crop_costs[item] = farm.get_crop_costs(ctx, item, component_count_needed * item_count)
	
	return crop_count, total_yield, component_crop_costs

def _check_full(ctx):
	area = contexts.get_area(ctx)

	x = get_pos_x()
	y = get_pos_y()

	xe = x + 1
	if areas.is_in((xe, y), area):
		if get_entity_type(East) != Entities.Dinosaur:
			return True

	xw = x - 1
	if areas.is_in((xw, y), area):
		if get_entity_type(West) != Entities.Dinosaur:
			return True

	yn = y + 1
	if areas.is_in((x, yn), area):
		if get_entity_type(North) != Entities.Dinosaur:
			return True

	ys = y - 1
	if areas.is_in((x, ys), area):
		if get_entity_type(South) != Entities.Dinosaur:
			return True

	return False

def ensure_soil(ctx):
	if get_ground_type() != Grounds.Soil:
		till()
	return True
	
def farm_crop(ctx):

	x0, y0, cx, cy, _ = contexts.get_area(ctx)
	map.move_to(x0, y0)
	pat = map.create_ouroboros_pattern(ctx)
	
	map.do_for_pattern(pat, ensure_soil, ctx)
	
	change_hat(Hats.Dinosaur_Hat)
	while map.do_for_pattern(pat, _check_full, ctx):
		pass
		
	change_hat(Hats.Wizard_Hat)

	return True
