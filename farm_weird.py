import map
import contexts
import farm_context
from farm_common import harvest_with_companion
import farm_hay

def farm(ctx):
	change_hat(Hats.Purple_Hat)
	pat = map.create_serpentine_pattern(ctx)
	local_ctx = contexts.create_override(ctx)
	farm_context.set_use_fertilizer(local_ctx, True)
	return map.do_for_pattern(pat, farm_hay.farm_plot, local_ctx)
	
	