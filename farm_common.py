import map
import farm_context

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
		return false
	if farm_context.use_fertilizer(context) and num_items(Items.Fertilizer) > 0:
		use_item(Items.Fertilizer)
	water = farm_context.water_to(context)
	if water > 0 and num_items(Items.Water) > 0 and get_water() < water:
		use_item(Items.Water)

# harvest, adding a companion if needed
# (note: not using a map here due to circular references)
def harvest_with_companion(context, force, no_everplants):
	import hay
	import wood
	import carrots
	
	if not force:
		if not can_harvest():
			return False

	cr = get_companion()
	if cr != None:
		comp, (cx, cy) = cr
		if map.is_in_area((cx, cy), context["area"]):
			x = get_pos_x()
			y = get_pos_y()
			map.move_to(cx, cy)
			entity_type = get_entity_type()
			if entity_type not in no_everplants and entity_type != comp:
				harvest()
				if comp == Entities.Grass:
					hay.plant_grass()
				elif comp == Entities.Bush:
					wood.plant_bush()
				elif comp == Entities.Tree:
					wood.plant_tree()
				elif comp == Entities.Carrot:
					carrots.plant_carrots()
				else:
					print("?!")
			map.move_to(x, y)
		
	return harvest()
	


	