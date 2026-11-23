# from common import plot_count
# import patterns
# import culture

# # determines there are enough resources to plant count items
# def _has_requirements(item, count):
# 	cost = get_cost(item)
# 	for item in cost:
# 		if num_items(item) < cost[item] * count:
# 			return False
# 	return True
	
# def _select_harvest_wood(size):
# 	return "wood_and_hay"
		
# def _select_harvest_carrots(size):
# 	if not _has_requirements(Entities.Carrot, size):
# 		return _select_harvest_wood(size)
# 	return "carrot"
		
# def _select_harvest_power(size):
# 	if not _has_requirements(Entities.Sunflower, size):
# 		return _select_harvest_carrots(size)
# 	return "power"    

# def _select_harvest_pumpkins(size):
# 	if not _has_requirements(Entities.Pumpkin, size * 2):
# 		return _select_harvest_carrots(size)
# 	return "pumpkin"    

# def select_harvest(size):
# 	return _select_harvest_pumpkins(size)
	
# def _harvest_wood(size):
# 	change_hat(Hats.Tree_Hat)
# 	pat = patterns.make_world_serpentine()
# 	patterns.do_for_pattern(pat, culture.farm_wood)
		
# def _harvest_carrots(size):
# 	change_hat(Hats.Carrot_Hat)
# 	pat = patterns.make_world_serpentine()
# 	patterns.do_for_pattern(pat, culture.farm_carrots)
			
# def _harvest_power(size):
# 	change_hat(Hats.Sunflower_Hat)
# 	pat = patterns.make_world_serpentine()
# 	patterns.do_for_pattern(pat, culture.farm_power)
	
# def _harvest_pumpkins(size):
# 	change_hat(Hats.Pumpkin_Hat)
# 	pat = patterns.make_world_serpentine()
# 	while not patterns.is_empty_dlist(pat):
# 		patterns.do_for_pattern(pat, culture.farm_pumpkin)
# 	harvest()

# _harvesters = {
# 	"wood_and_hay": _harvest_wood,
# 	"carrot": _harvest_carrots,
# 	"power": _harvest_power,
# 	"pumpkin": _harvest_pumpkins
# 	}
		
# def harvest_it():
# 	size = plot_count()
# 	while True:
# 		if num_items(Items.Power) < 50000:
# 			selected = _select_harvest_power(size)
# 		else:
# 			selected = select_harvest(size)
# 		if not selected in _harvesters:
# 			return
# 		harvester = _harvesters[selected]
# 		harvester(size)
