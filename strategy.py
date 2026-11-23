import map
import farm

def add_costs(source, dest):
	for add in source:
		val = 0
		if add in dest:
			val = dest[add]
		dest[add] = val + source[add]

			
# direct - dict[Unlocks -> int]     
def _expand_item_cost(item, count, inventory):
	entity = farm.get_entity_for_item(item)
	if entity == None:
		return None

	inventory_count = inventory[item]
	reduction = min(count, inventory_count)
	count = count - reduction
	inventory[item] = inventory_count - reduction
		
	entity_cost = get_cost(entity)
				
	if len(entity_cost) == 0:
		return { entity: count }
		
	cost = {}
	for sub_entity in entity_cost:
		expanded = _expand_item_cost(sub_entity, count * entity_cost[sub_entity], inventory)
		if expanded == None:
			return None
		add_costs(expanded, cost)
	return cost

def check_unlock(unlock, inventory):
	
	cost = {}
	unlock_cost = get_cost(unlock)
	quick_print(unlock, unlock_cost, len(unlock_cost))
	if len(unlock_cost) == 0:
		# no cost => already have it
		return None
		
	unlock_count = num_unlocked(unlock)
		
	for item in unlock_cost:
		expanded = _expand_item_cost(item, unlock_cost[item], inventory)
		if expanded == None:
			return None
		add_costs(expanded, cost)
		
	items = 0
	for entity in cost:
		items = items + cost[entity]

	return (cost, items)

def _get_real_inventory():
	inventory = {}
	for item in Items:
		inventory[item] = num_items(item)
	return inventory
		
def select_next_unlock(get_inventory):
	
	if get_inventory == None:
		get_inventory = _get_real_inventory
		
	easiest = None
	easiest_cost = None
	easiest_items = None
	for u in Unlocks:
		check = check_unlock(u, get_inventory())
		if check == None:
			continue
			
		cost, items = check
		if easiest == None or items < easiest_items:
			easiest = u
			easiest_cost = cost
			easiest_items = items

	if easiest == None:
		return None                
	return easiest      

# Farm until the next unlock is unlocked, or until nothing can be unlocked
def farm_next_unlock(context, get_inventory):
	   
	next_unlock = select_next_unlock(get_inventory)
	print(next_unlock)
	
	if farm.farm_for_all(get_cost(next_unlock), context):
		unlock(next_unlock)
		map.init(None, None)
		pet_the_piggy()
		return True

	print("Farming failed")
	return False 
	
def farm_unlocks(context, get_inventory):
	while farm_next_unlock(context, get_inventory):
		pass
	
		