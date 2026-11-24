import farm_hay
import farm_wood
import farm_carrots
import farm_pumpkin
import farm_power
import farm_cactus
import farm_weird

_farmers = {}
_farmers[Items.Hay] = { "crop": Entities.Grass, "farm": farm_hay.farm }
_farmers[Items.Wood] = { "crop": Entities.Tree, "farm": farm_wood.farm }
_farmers[Items.Carrot] = { "crop": Entities.Carrot, "farm": farm_carrots.farm }
_farmers[Items.Pumpkin] = { "crop": Entities.Pumpkin, "source_factor": 1.5, "farm": farm_pumpkin.farm }
_farmers[Items.Power] = { "crop": Entities.Sunflower, "farm": farm_power.farm }
_farmers[Items.Cactus] = { "crop": Entities.Cactus, "farm": farm_cactus.farm }
_farmers[Items.Weird_Substance] = { "crop": None, "farm": farm_weird.farm }

def get_entity_for_item(item):
	if item not in _farmers:
		return None
	return _farmers[item]["crop"]
			
# Run a farmer to ensure we have the needed count of an item
def farm_for(item, count, no_power, context):
	if num_items(item) >= count:
		# have enough of this
		return True
	
	if item not in _farmers:
		# can't farm this yet
		return False
	
	farmer = _farmers[item]            
	cost = get_cost(farmer["crop"])
	if "source_factor" in farmer:
		source_factor = farmer["source_factor"]
	else:
		source_factor = 1
	
	for source_item in cost:
		source_count = cost[source_item]
		if not farm_for(source_item, source_count * count * source_factor, no_power, context):
			return False
		
	while num_items(item) < count:
		if not no_power:
			farm_for(Items.Power, 50000, True, context)
		if not farmer["farm"](context):
			return False
		
	return True

	
# Run farmers to ensure we have all required items
def farm_for_all(cost_map, context):
	for item in cost_map:
		if not farm_for(item, cost_map[item], False, context):
			return False
	return True    
		
	
	