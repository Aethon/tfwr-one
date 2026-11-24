import map
import contexts
import farm_context
from farm_common import harvest_with_companion, plant_crop

DIR_OFFSETS = {
	East: (1, 0),
	West: (-1, 0),
	North: (0, 1),
	South: (0, -1)
}

def get_crop_costs(count, ctx):
	if count == 0:
		return 0, {}

	_, _, cx, cy, _ = contexts.get_area(ctx)

	unlock_factor = 2**(num_unlocked(Unlocks.Treasure_Map) - 1)
	gold_yield = unlock_factor * cx * cy * 300 # reuses
	crops_needed = max(count / gold_yield, 1)
	required_weird = crops_needed * 300 * max(cx, cy) * unlock_factor
	
	return count, { Items.Weird_Substance: farm.get_crop_costs(Items.Weird_Substance, required_weird) }

def get_item_costs(count):
	entity = Entities.Gold
	crop_yield = farm.get_yield_for_item(item)

	if need == 0 or entity == None:
		return count, have, need, {}, need

	entity_cost = get_cost(entity)
	if len(entity_cost) == 0:
		return count, have, need, {}, need

	component_costs = {}
	total = need
	need_after_yield = need / crop_yield
	for component_item in entity_cost:
		component_count = entity_cost[component_item]
		component_cost_tree = get_item_costs(component_item, need_after_yield * component_count, inventory)
		component_costs[component_item] = component_cost_tree
		_, _, _, _, sub_total = component_cost_tree
		total += sub_total

	return count, have, need, component_costs, total

def _move_next(visited):	
	for dir in [East, West, North, South]:
		if not can_move(dir):
			continue

		dx, dy = DIR_OFFSETS[dir]
		dir_pos = (get_pos_x() + dx, get_pos_y() + dy)
		if dir_pos in visited:
			continue

		move(dir)
		return True
	
	return False

def _find_treasure(ctx):
	visited = set()
	path = []
	while True:

		# move outward
		while True:
			if get_entity_type() == Entities.Treasure:
				return True

			pos = (get_pos_x(), get_pos_y())
			path.append(pos)
			visited.add(pos)
			if not _move_next(visited):
				break

		# retreat
		while True:
			if len(path) == 0:
				return True
			
			retreat_pos = path.pop()
			map.move_to_pos(retreat_pos)
			if _move_next(visited):
				break

	return False

def farm(ctx):

	change_hat(Hats.Gold_Hat)
	plant(Entities.Bush)
	use_item(Items.Water)
	while not can_harvest():
		pass
	
	use_item(Items.Weird_Substance, 10 * 2**(num_unlocked(Unlocks.Mazes) - 1))

	while True:
		use_item(Items.Weird_Substance, 10 * 2**(num_unlocked(Unlocks.Mazes) - 1))
		if not _find_treasure(ctx):
			break

	return True
		



