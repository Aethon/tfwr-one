from common import ceil
import map
import areas
import contexts
from farm_common import harvest_with_companion, plant_crop, NO_COSTS, get_unlock_yield
import farm_hay
import farm_context
import drones

NO_OVERPLANTS = [ Entities.Sunflower ]

def get_crop_costs(count, ctx):
	if count < 1:
		return NO_COSTS

	_, _, cx, cy, _ = contexts.get_area(ctx)	
	plot_yield = get_unlock_yield(Unlocks.Sunflowers) * 8 # harvested in order to get gain
	crop_yield = cx * cy * plot_yield
	crop_count = ceil(count / crop_yield)
	total_yield = crop_count * crop_yield

	component_need_count = total_yield / plot_yield
	component_costs = get_cost(Entities.Sunflower)
	component_crop_costs = {}
	for item in component_costs:
		item_count = component_costs[item]
		component_crop_costs[item] = farm.get_crop_costs(ctx, item, component_need_count * item_count)	
	
	return crop_count, total_yield, {}

def plant_sunflower():
	if get_ground_type() != Grounds.Soil:
		till()
	return plant(Entities.Sunflower)

def _make_harvest_task(ctx, pat, hat):

	def harvest_area():
		if hat != None:
			change_hat(hat)
		
		def harvest_plot(ctx):
			while get_entity_type() == Entities.Sunflower and not can_harvest():
				pass
			harvest()
			return True
		
		return map.do_for_pattern(pat, harvest_plot, ctx)

	return harvest_area

def _make_plant_task(ctx, area, hat):
	block_ctx = contexts.create_override_slice(ctx, area)
	pat = map.create_serpentine_pattern(block_ctx)

	def plant_area():
		if hat != None:
			change_hat(hat)

		petals = []
		for i in range(7, 16):
			petals.append([])

		def plant_plot(_):
			plant_sunflower()
			p = measure()
			petals[p - 7].append((get_pos_x(), get_pos_y()))
			if p >= 13 and get_water() < 0.5 and num_items(Items.Water) > 0:
				use_item(Items.Water)
			return True

		if map.do_for_pattern(pat, plant_plot, ctx):
			return petals

		return None

	return plant_area

def farm_crop(ctx):
	
	change_hat(Hats.Golden_Sunflower_Hat)

	work_areas = areas.divide(map.get_area(), 4, 4, 32, True)
	direct_area = work_areas.pop()

	while True:
		
		# plant all
		work = []
		for drone_area in work_areas:
			work.append(_make_plant_task(ctx, drone_area, Hats.Sunflower_Hat))
		direct = [ _make_plant_task(ctx, direct_area, None) ]
		(drone_pats, direct_pats) = drones.run_work(work, direct)

		# for each max petal count, harvest
		for petals in range(15, 6, -1):
			p_index = petals - 7
			work = []	
			for p in drone_pats:
				work.append(_make_harvest_task(ctx, p[p_index], Hats.Sunflower_Hat))
			direct = [ _make_harvest_task(ctx, direct_pats[0][p_index], None)]
			drones.run_work(work, direct)

		# until the goal is achieved
		if farm_context.check_farming_goal(ctx):
			return True
	
	return True
