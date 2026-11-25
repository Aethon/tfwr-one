from common import ceil
import map
import contexts
import farm
import farm_context
from farm_common import harvest_with_companion, plant_crop, NO_COSTS, get_unlock_yield

DIR_OFFSETS = {
	East: (1, 0),
	West: (-1, 0),
	North: (0, 1),
	South: (0, -1)
}

DIR_OPPOSITES = {
	East: West,
	West: East,
	North: South,
	South: North
}

def get_crop_costs(count, ctx):
	if count < 1:
		return NO_COSTS

	_, _, cx, cy, _ = contexts.get_area(ctx)
	plot_yield = get_unlock_yield(Unlocks.Treasure_Map)
	crop_yield = cx * cy * plot_yield * 300 # reuses
	crop_count = ceil(count / crop_yield)
	total_yield = crop_count * crop_yield

	required_weird = crop_count * 300 * max(cx, cy) * plot_yield # required weird scales with unlocks
	
	return crop_count, total_yield, { Items.Weird_Substance: farm.get_crop_costs(ctx, Items.Weird_Substance, count) }

# def get_item_costs(count):
# 	entity = Entities.Treasure
# 	crop_yield = farm.get_yield_for_item(item)

# 	if need == 0 or entity == None:
# 		return count, have, need, {}, need

# 	entity_cost = get_cost(entity)
# 	if len(entity_cost) == 0:
# 		return count, have, need, {}, need

# 	component_costs = {}
# 	total = need
# 	need_after_yield = need / crop_yield
# 	for component_item in entity_cost:
# 		component_count = entity_cost[component_item]
# 		component_cost_tree = get_item_costs(component_item, need_after_yield * component_count, inventory)
# 		component_costs[component_item] = component_cost_tree
# 		_, _, _, _, sub_total = component_cost_tree
# 		total += sub_total

# 	return count, have, need, component_costs, total

def _move_next(path, visited):	
	for dir in [East, West, North, South]:
		if not can_move(dir):
			continue

		dx, dy = DIR_OFFSETS[dir]
		dir_pos = (get_pos_x() + dx, get_pos_y() + dy)
		if dir_pos in visited:
			continue

		move(dir)
		path.append(DIR_OPPOSITES[dir])
		visited.add(dir_pos)
		return True
	
	return False

def _find_treasure(ctx):
	visited = set()
	path = []
	pos = (get_pos_x(), get_pos_y())
	visited.add(pos)
	while True:

		# move outward
		while True:
			if get_entity_type() == Entities.Treasure:
				return True
			if not _move_next(path, visited):
				break

		# retreat
		if len(path) == 0:
			return True
		move(path.pop())

	return False

# # map { pos -> tuple }
# # (left: dir|None, right: dir|None, forward: dir|None, back: dir|None)
# def _map_maze(ctx):
# 	visited = set()
# 	path = []
# 	pos = (get_pos_x(), get_pos_y())
# 	visited.add(pos)
# 	while True:

# 		# move outward
# 		while True:
# 			if not _move_next(path, visited):
# 				break

# 		# retreat
# 		if len(path) == 0:
# 			return True
# 		move(path.pop())

# 	return False

def farm_crop(ctx):

	change_hat(Hats.Gold_Hat)
	plant(Entities.Bush)
	use_item(Items.Water)
	while not can_harvest():
		pass
	
	_, _, cx, cy, _ = contexts.get_area(ctx)
	n = min(cx, cy)
	while True:
		use_item(Items.Weird_Substance, n * 2**(num_unlocked(Unlocks.Mazes) - 1))
		if not _find_treasure(ctx):
			break

	return True
		



