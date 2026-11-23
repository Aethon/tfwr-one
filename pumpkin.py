import map
import farm_context
from farm_common import harvest_with_companion

PUMPKIN_LIST_KEY = "pumpkins"
NO_OVERPLANTS = [ Entities.Pumpkin ]

def plant_pumpkin():
	return plant(Entities.Pumpkin)

def farm_plot(context):
	
	if get_entity_type() == Entities.Pumpkin:
		if can_harvest():
			# all good; no need to come back
			return True
	else:        
		harvest_with_companion(context, True, NO_OVERPLANTS)
		if get_ground_type() != Grounds.Soil:
			till()
		farm_context.plant_crop(context, plant_pumpkin)
		
	# need to come back and check on it
	context[PUMPKIN_LIST_KEY].append((get_pos_x(), get_pos_y()))
	return True
	
def farm(context):

	change_hat(Hats.Pumpkin_Hat)
	pat = map.create_serpentine_pattern(context["area"])
	context[PUMPKIN_LIST_KEY] = []
	while map.do_for_pattern(pat, farm_plot, context):
		pat = context[PUMPKIN_LIST_KEY]
		if len(pat) == 0:
			break
		context[PUMPKIN_LIST_KEY] = []
		farm_context.set_water_to(context, 0.5) # only water on the cleanup passes
		
	return harvest()
