# from movement import move_to

# # ensure the ground has a minimum amount of water
# def water(min):
# 	if (get_water() < min and num_items(Items.Water) > 0):
# 		use_item(Items.Water)

# # harvest everything on the farm directly
# def gather_all():
# 	for x in range(get_world_size()):
# 		for y in range(get_world_size()):
# 			move_to(x, y)                    
# 			if can_harvest():
# 				harvest()

# # harvest, adding a companion if needed TODO: use map
# def harvest_with_companion():
# 	if not can_harvest():
# 		return False
		
# 	cr = get_companion()
# 	if cr != None:
# 		comp, (cx, cy) = cr
# 		x = get_pos_x()
# 		y = get_pos_y()
# 		move_to(cx, cy)
# 		harvest()
# 		plant_simple(comp)
# 		move_to(x, y)
		
# 	return harvest()
							
# # plant/harvest hay
# def farm_hay():
# 	harvest_with_companion()
# 	return plant_simple(Entities.Grass)

# # plant/harvest wood and hay
# def farm_wood():
# 	if (get_pos_x() + get_pos_y()) % 2 == 1:
# 		return farm_hay()
	
# 	harvest_with_companion()
# 	plant_simple(Entities.Tree)    
# 	return 0
	
# # plant/harvest carrots
# def farm_carrots():
# 	harvest_with_companion()
# 	plant_simple(Entities.Carrot)
# 	return 0
	
# def farm_pumpkin():
# 	if get_entity_type() == Entities.Pumpkin:
# 		if can_harvest():
# 			# this is a good pumpkin; no need to come back here
# 			return 2
# 		else:
# 			# still growing; move on
# 			return 0
# 	if can_harvest():
# 		harvest()
# 	if get_ground_type() != Grounds.Soil:
# 		till()
# 	plant(Entities.Pumpkin)
# 	return 0

# def farm_power():
# 	if can_harvest():
# 		harvest()
# 	if get_ground_type() != Grounds.Soil:
# 		till()
# 	plant(Entities.Sunflower)
# 	return 0


# def plant_grass():
# 	return plant(Entities.Grass)
	
# def plant_bush():
# 	return plant(Entities.Bush)
	
# def plant_tree():
# 	return plant(Entities.Tree)
	
# def plant_carrot():
# 	if get_ground_type() != Grounds.Soil:
# 		till()
# 	return plant(Entities.Carrot)
	
# _planters = {}
# _planters[Entities.Grass] = plant_grass
# _planters[Entities.Bush] = plant_bush
# _planters[Entities.Tree] = plant_tree
# _planters[Entities.Carrot] = plant_carrot

# def plant_simple(type):
# 	if type not in _planters:
# 		return False
# 	return _planters[type]()
	