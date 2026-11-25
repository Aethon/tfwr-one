from common import pow2, format_number
import farm_hay
import farm_wood
import farm_carrots
import farm_pumpkin
import farm_power
import farm_cactus
import farm_weird
import strategy
import farm_context
import farm_bones
import farm_gold

_POWER_MIN = 50000
_POWER_MAX = 60000

# (order: int, crop: Entities, unlock: Unlocks, failure_rate: nun(0..1), farm: func(ctx), get_crop_cost: func(count, ctx))
_crop_info = {}
_crop_info[Items.Wood] = (0, Entities.Tree, Unlocks.Trees, 0.0, farm_wood.farm_crop, farm_wood.get_crop_costs)
_crop_info[Items.Hay] = (1, Entities.Grass, Unlocks.Grass, 0.0, farm_hay.farm_crop, farm_hay.get_crop_costs)
_crop_info[Items.Carrot] = (2, Entities.Carrot, Unlocks.Carrots, 0.0, farm_carrots.farm_crop, farm_carrots.get_crop_costs)
_crop_info[Items.Pumpkin] = (3, Entities.Pumpkin, Unlocks.Pumpkins,  0.4, farm_pumpkin.farm_crop, farm_pumpkin.get_crop_costs)
_crop_info[Items.Power] = (4, Entities.Sunflower, Unlocks.Sunflowers, 0.0, farm_power.farm_crop, farm_power.get_crop_costs)
_crop_info[Items.Cactus] = (5, Entities.Cactus, Unlocks.Cactus, 0.0, farm_cactus.farm_crop, farm_cactus.get_crop_costs)
_crop_info[Items.Weird_Substance] = (6, None, None, 0.0, farm_weird.farm_crop, farm_weird.get_crop_costs)
_crop_info[Items.Bone] = (7, None, Unlocks.Dinosaurs, 0.0, farm_bones.farm_crop, farm_bones.get_crop_costs)
_crop_info[Items.Gold] = (8, None, Unlocks.Treasure_Map, 0.0, farm_gold.farm_crop, farm_gold.get_crop_costs)

def get_entity_for_item(item):
	if item not in _crop_info:
		return None
	_, entity, _, _, _ = _crop_info[item]
	return entity

def get_yield_for_item(item):
	if item not in _crop_info:
		return None
	_, _, unlock, failure_rate, _ = _crop_info[item]
	return pow2(num_unlocked(unlock) - 1) * (1 - failure_rate)

def can_farm(item):
	return item in _crop_info

def get_crop_costs(ctx, item, count):
	if item not in _crop_info:
		return None
	_, _, _, _, _, get = _crop_info[item]
	return get(count, ctx)

def _collect_costs(component_cost_map, total_cost_map):
	for item in component_cost_map:
		_, _, item_count, sub_cost_map, _ = component_cost_map[item]
		if item_count == 0:
			continue

		prev_count = 0
		if item in total_cost_map:
			prev_count = total_cost_map[item]
		total_cost_map[item] = prev_count + item_count
		_collect_costs(sub_cost_map, total_cost_map)

def _select_crop(component_cost_map, context):
	collected_item_costs = {}
	_collect_costs(component_cost_map, collected_item_costs)

	quick_print("Costs:")
	for c in collected_item_costs:
		quick_print("  -", c, "=>", format_number(collected_item_costs[c]))
	min_order = None
	min_farmer = None
	
	for item in collected_item_costs:
		farmer = _crop_info[item]
		order, _, _, _, _ = farmer
		if min_order == None or order < min_order:
			min_order = order
			min_farmer = farmer

	return min_farmer

def _select_power_crop(ctx):
	power_count = num_items(Items.Power)
	power_to = farm_context.power_to(ctx)
	if power_to == None:
		if power_count > _POWER_MIN:
			return None
		power_to = _POWER_MAX
		farm_context.set_power_to(ctx, power_to)
	if power_count >= _POWER_MAX:
		farm_context.set_power_to(ctx, None)
		return None

	return _select_crop({ Items.Power: strategy.get_item_costs(Items.Power, power_to, strategy.get_real_inventory()) }, ctx)

def select_crop(component_cost_map, ctx):
	pf = _select_power_crop(ctx)
	if pf != None:
		return pf
	return _select_crop(component_cost_map, ctx)

def farm_for(component_cost_map, ctx):
	farmer = select_crop(component_cost_map, ctx)
	if farmer == None:
		return False
	_, entity, _, _, farm = farmer

	print("Planting", entity)
	return farm(ctx)

def dump_crop_costs(item, crop_cost):
	def dump(indent, cost_map):
		for item in cost_map:
			crop_count, total_yield, sub_cost_map = cost_map[item]
			quick_print(indent, "-", item, "=>", crop_count, "crops", "for", format_number(total_yield))
			dump(indent + "  ", sub_cost_map)

	dump("", { item: crop_cost })