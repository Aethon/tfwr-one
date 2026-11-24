import farm_hay
import farm_wood
import farm_carrots
import farm_pumpkin
import farm_power
import farm_cactus
import farm_weird
import strategy
import farm_context

_POWER_MIN = 50000
_POWER_MAX = 60000

_farmers = {}
_farmers[Items.Wood] = { "order": 0, "crop": Entities.Tree, "farm": farm_wood.farm }
_farmers[Items.Hay] = { "order": 1, "crop": Entities.Grass, "farm": farm_hay.farm }
_farmers[Items.Carrot] = { "order": 2, "crop": Entities.Carrot, "farm": farm_carrots.farm }
_farmers[Items.Pumpkin] = { "order": 3, "crop": Entities.Pumpkin, "source_factor": 1.5, "farm": farm_pumpkin.farm }
_farmers[Items.Power] = { "order": 4, "crop": Entities.Sunflower, "farm": farm_power.farm }
_farmers[Items.Cactus] = { "order": 5, "crop": Entities.Cactus, "farm": farm_cactus.farm }
_farmers[Items.Weird_Substance] = { "order": 6, "crop": None, "farm": farm_weird.farm }

def get_entity_for_item(item):
	if item not in _farmers:
		return None
	return _farmers[item]["crop"]

def can_farm(item):
	return item in _farmers
 

def _collect_costs(component_cost_map, total_cost_map):
	for item in component_cost_map:
		_, _, item_count, sub_cost_map, _ = component_cost_map[item]
		prev_count = 0
		if item in total_cost_map:
			prev_count = total_cost_map[item]
		total_cost_map[item] = prev_count + item_count
		_collect_costs(sub_cost_map, total_cost_map)

def _select_farmer(component_cost_map, context):
	collected_item_costs = {}
	_collect_costs(component_cost_map, collected_item_costs)

	min_order = None
	min_farmer = None
	
	for item in collected_item_costs:
		farmer = _farmers[item]
		order = farmer["order"]
		if min_order == None or order < min_order:
			min_order = order
			min_farmer = farmer

	return min_farmer

def _select_power_farmer(ctx):
	power_count = num_items(Items.Power)
	power_to = farm_context.power_to(ctx)
	if power_to == None:
		if power_count > _POWER_MIN:
			return None
		power_to = _POWER_MAX
		farm_context.set_power_to(power_to)
	if power_count >= _POWER_MAX:
		farm_context.set_power_to(None)
		return None

	return _select_farmer({ Items.Power, strategy.get_item_costs(Items.Power, power_to, strategy.get_real_inventory()) }, ctx)

def select_farmer(component_cost_map, ctx):
	pf = _select_power_farmer(ctx)
	if pf != None:
		return pf
	return _select_farmer(component_cost_map, ctx)

def farm_for(component_cost_map, ctx):
	farmer = select_farmer(component_cost_map, ctx)
	if farmer == None:
		return False
	return farmer["farm"](ctx)
