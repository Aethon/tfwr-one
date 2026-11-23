import map
from farm_common import harvest_with_companion
import hay

SUNFLOWER_PATTERNS_KEY = "sunflower_patterns"
NO_OVERPLANTS = [ Entities.Sunflower ]

def _plant_plot(context):
	global SUNFLOWER_PATTERNS_KEY
	global NO_OVERPLANTS

	if not harvest_with_companion(context, True, NO_OVERPLANTS):
		harvest()
		
	if get_ground_type() != Grounds.Soil:
		till()
	if (plant(Entities.Sunflower)):
		context[SUNFLOWER_PATTERNS_KEY][measure() - 7].append((get_pos_x(), get_pos_y()))
	
	return True

def _harvest_plot(context):
	global NO_OVERPLANTS
	
	harvest_with_companion(context, True, NO_OVERPLANTS)
	hay.farm_plot(context)    
	return True

def _init_patterns():
	patterns = []
	for petals in range(7, 16):
		patterns.append([])
	return patterns

def farm(context):
	global SUNFLOWER_PATTERNS_KEY
	
	change_hat(Hats.Sunflower_Hat)
		
	plant_pat = map.create_serpentine_pattern(context["area"])
	harvest_pats = _init_patterns()
	context[SUNFLOWER_PATTERNS_KEY] = harvest_pats    
	if not map.do_for_pattern(plant_pat, _plant_plot, context):
		return False
	
	context[SUNFLOWER_PATTERNS_KEY] = None
	for petals in range(len(harvest_pats) - 1, -1, -1):
		pat = harvest_pats[petals]
		if len(pat) == 0:
			continue
		if not map.do_for_pattern(pat, _harvest_plot, context):
			return False
	
	return True