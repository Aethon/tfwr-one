import map
import farm
from common import format_number

def get_available_unlocks():
	def can_unlock(unlock):
		unlock_cost = get_cost(unlock)
		if len(unlock_cost) == 0:
			# no cost => already have it
			return False
					
		for item in unlock_cost:
			if not farm.can_farm(item):
				return False

		return True

	available = []

	for unlock in Unlocks:
		if can_unlock(unlock):
			available.append(unlock)

	return available

# (count: int, have: int, need: int, component_cost: { Item -> tuple }, total_needed)
def get_item_costs(item, count, inventory):
	entity = farm.get_entity_for_item(item)
	crop_yield = farm.get_yield_for_item(item)

	have = inventory[item]
	reduction = min(count, have)
	need = count - reduction
	inventory[item] = have - reduction

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

def get_unlock_costs(unlock, inventory):
	unlock_cost = get_cost(unlock)
	component_costs = {}
	total = 0
	for item in unlock_cost:
		item_cost = get_item_costs(item, unlock_cost[item], inventory)
		component_costs[item] = item_cost
		_, _, _, _, sub_total = item_cost
		total = total + sub_total
	return component_costs, total

def get_real_inventory():
	inventory = {}
	for item in Items:
		inventory[item] = num_items(item)
	return inventory

def get_selected_unlock_costs(unlocks, get_inventory):
	if get_inventory == None:
		get_inventory = get_real_inventory

	selected_unlock_costs = {}
	for unlock in unlocks:
		inventory = get_inventory()
		selected_unlock_costs[unlock] = get_unlock_costs(unlock, inventory)

	return selected_unlock_costs
	

def select_next_unlock(unlock_cost_map):
	
	min_unlock = None
	min_item_count = None
	min_cost_map = None
	for unlock in unlock_cost_map:
		cost_map, item_count = unlock_cost_map[unlock]
		if min_unlock == None or item_count < min_item_count:
			min_unlock = unlock
			min_item_count = item_count
			min_cost_map = cost_map

	if min_unlock == None:
		return None

	return (min_unlock, min_item_count, min_cost_map)

def dump_unlock_costs(unlock_cost_map):
	def dump_item_costs(indent, item_cost_map):
		for item in item_cost_map:
			count, have, need, sub_cost_map, total = item_cost_map[item]
			quick_print(indent, "-", item, "requires", format_number(count), "have", format_number(have), "=> needs", format_number(need))
			dump_item_costs(indent + "  ", sub_cost_map)

	quick_print("Unlock costs:")
	for unlock in unlock_cost_map:
		component_cost_map, total = unlock_cost_map[unlock]
		quick_print("-", unlock, "(", format_number(total), "items", ")")
		dump_item_costs("  ", component_cost_map)

# Farm a round
def farm_for_next_unlock(ctx, get_inventory):

	available_unlocks = get_available_unlocks()
	unlock_cost_map = get_selected_unlock_costs(available_unlocks, None)
	dump_unlock_costs(unlock_cost_map)
	selected_unlock, item_count, selected_cost_map = select_next_unlock(unlock_cost_map)
	quick_print()
	print("Unlocking", selected_unlock)
	do_a_flip()
	
	if item_count == 0:
		unlock(selected_unlock)
		pet_the_piggy()
		do_a_flip()
		map.init(None, None)
		return True

	return farm.farm_for(selected_cost_map, ctx)
	
def farm_unlocks(ctx, get_inventory):
	while farm_for_next_unlock(ctx, get_inventory):
		pass
	
