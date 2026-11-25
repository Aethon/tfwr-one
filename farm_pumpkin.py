from common import ceil
import map
import drones
import areas
import contexts
import farm_context
from farm_common import harvest_with_companion, plant_crop, NO_COSTS, get_unlock_yield

NO_OVERPLANTS = [ Entities.Pumpkin ]

def get_crop_costs(count, ctx):
	if count < 1:
		return NO_COSTS
	
	_, _, cx, cy, _ = contexts.get_area(ctx)
	plot_yield = get_unlock_yield(Unlocks.Pumpkins) * 0.7 # reduced for failure rate (20% +breathing room)
	crop_yield = cx * cy * min(6, min(cy, cy)) # big pumplink multiplier
	crop_count = ceil(count / crop_yield)
	total_yield = crop_count * crop_yield

	component_need_count = total_yield / plot_yield
	component_costs = get_cost(Entities.Pumpkin)
	component_crop_costs = {}
	for item in component_costs:
		item_count = component_costs[item]
		component_crop_costs[item] = farm.get_crop_costs(ctx, item, component_need_count * item_count)	
	
	return crop_count, total_yield, component_crop_costs

def plant_pumpkin():
	if get_ground_type() != Grounds.Soil:
		till()
	return plant(Entities.Pumpkin)

def _make_farm_task(ctx, area, hat):
	block_ctx = contexts.create_override_slice(ctx, area)
	pat = map.create_serpentine_pattern(block_ctx)

	def farm_area():
		if hat != None:
			change_hat(hat)

		run_pat = pat
		while True:
			next_pat = []
			def farm_plot(_):
				if get_entity_type() == Entities.Pumpkin:
					if can_harvest():
						# all good; no need to come back
						return True
				else:        
					harvest() # harvest_with_companion(ctx, True, NO_OVERPLANTS)
					plant_crop(block_ctx, plant_pumpkin)
					
				# need to come back and check on it
				next_pat.append((get_pos_x(), get_pos_y()))
				return True

			if not map.do_for_pattern(run_pat, farm_plot, block_ctx):
				return False
			run_pat = next_pat
			if len(run_pat) == 0:
				return
			farm_context.set_water_to(block_ctx, 0.5) # only water on the cleanup passes

	return farm_area

def farm_crop(ctx):
	
	change_hat(Hats.Pumpkin_Hat)

	work_areas = areas.divide(map.get_area(), 4, 4, 32, True)
	direct_area = work_areas.pop()

	while True:
		work = []
		for drone_area in work_areas:
			work.append(_make_farm_task(ctx, drone_area, Hats.Pumpkin_Hat))
		direct = [ _make_farm_task(ctx, direct_area, None) ]
		drones.run_work(work, direct)

		harvest()

		# until the goal is achieved
		if farm_context.check_farming_goal(ctx):
			return True


	return True