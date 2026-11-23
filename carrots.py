import map
from farm_common import harvest_with_companion

NO_OVERPLANTS = [ Entities.Carrot ]

def plant_carrots():
	if get_ground_type() != Grounds.Soil:
		till()
	return plant(Entities.Carrot)
	
# plant/harvest carrots
def farm_plot(context):
	global NO_OVERPLANTS
	
	harvest_with_companion(context, True, NO_OVERPLANTS)
	plant_carrots()
	return True
		
def farm(context):
	change_hat(Hats.Carrot_Hat)
	pat = map.create_serpentine_pattern(context["area"])
	return map.do_for_pattern(pat, farm_plot, context)
