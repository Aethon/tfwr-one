import map
import areas
import contexts
import farm_context

NO_COSTS = (0, 0, {})

# ensure the ground has a minimum amount of water
def water(min):
	if (get_water() < min and num_items(Items.Water) > 0):
		use_item(Items.Water)

# harvest everything on the farm directly
def gather_all():
	for x in range(get_world_size()):
		for y in range(get_world_size()):
			move_to(x, y)                    
			if can_harvest():
				harvest()

def plant_crop(ctx, plant):
	if not plant():
		return False
	if farm_context.use_fertilizer(ctx) and num_items(Items.Fertilizer) > 0:
		use_item(Items.Fertilizer)
	water = farm_context.water_to(ctx)
	if water > 0 and num_items(Items.Water) > 0 and get_water() < water:
		use_item(Items.Water)
	return True

# harvest, adding a companion if needed
# (note: not using a map here due to circular references)
def harvest_with_companion(ctx, force, no_everplants):
	import farm_hay
	import farm_wood
	import farm_carrots
	
	if not force:
		if not can_harvest():
			return False

	cr = get_companion()
	if cr != None:
		comp, pos = cr
		if areas.is_in(pos, contexts.get_area(ctx)):
			x = get_pos_x()
			y = get_pos_y()
			map.move_to_pos(pos)
			entity_type = get_entity_type()
			if entity_type not in no_everplants and entity_type != comp:
				harvest()
				if comp == Entities.Grass:
					farm_hay.plant_grass()
				elif comp == Entities.Bush:
					farm_wood.plant_bush()
				elif comp == Entities.Tree:
					farm_wood.plant_tree()
				elif comp == Entities.Carrot:
					farm_carrots.plant_carrots()
				else:
					print("?!")
			map.move_to(x, y)
		
	return harvest()
	

def get_unlock_yield(unlock):
	return 2**(num_unlocked(unlock) - 1)

def get_polyculture_yield():
	num = num_unlocked(Unlocks.Polyculture)
	if num == 0:
		return 1
	return 5 * 2**(num - 1)