import map
import farm_context
from farm_common import harvest_with_companion
import hay

def farm(context):
	change_hat(Hats.Purple_Hat)
	farm_context.set_use_fertilizer(context, True)
	pat = map.create_serpentine_pattern(farm_context.get_area(context))
	return map.do_for_pattern(pat, hay.farm_plot, context)
	
	