from common import ceil
import map
import contexts
import farm_context
from farm_common import harvest_with_companion, plant_crop, NO_COSTS, get_unlock_yield
import farm_hay

def get_crop_costs(count, ctx):
	if count < 1:
		return NO_COSTS
		
	_, _, cx, cy, _ = contexts.get_area(ctx)
	plot_yield = get_unlock_yield(Unlocks.Grass)
	crop_yield = cx * cy * plot_yield / 2 # half of yield is converted to weird
	crop_count = ceil(count / crop_yield)
	total_yield = crop_count * crop_yield

	return crop_count, total_yield, {}

def farm_crop(ctx):
	change_hat(Hats.Purple_Hat)
	pat = map.create_serpentine_pattern(ctx)
	local_ctx = contexts.create_override(ctx)
	farm_context.set_use_fertilizer(local_ctx, True)
	return map.do_for_pattern(pat, farm_hay.farm_plot, local_ctx)
	