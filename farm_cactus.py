import map
import contexts
from farm_common import harvest_with_companion, plant_crop

CACTUS_LIST_KEY = "cactii"
NO_OVERPLANTS = [ Entities.Cactus ]

def plant_cactus():
	if get_ground_type() != Grounds.Soil:
		till()
	return plant(Entities.Cactus)

def farm_plot(ctx):
	
	if get_entity_type() == Entities.Cactus:
		if can_harvest():
			# all good; no need to come back
			return True
	else:        
		harvest_with_companion(ctx, True, NO_OVERPLANTS)
		if not plant_crop(ctx, plant_cactus):
			return False

	# need to come back and check on it
	contexts.get_value(ctx, CACTUS_LIST_KEY).append((get_pos_x(), get_pos_y()))
	return True

def _sort(ctx, unsorted_rows, unsorted_cols):
	xi, yi, dx, dy, _ = contexts.get_area(ctx)
	next_unsorted_rows = set()
	next_unsorted_cols = set()
	
	for row in unsorted_rows:
		changed = True
		while changed:
			changed = False
			for col in range(xi, xi + dx - 1):
				map.move_to(col, row)
				this = measure()
				that = measure(East)
				if (that < this):
					swap(East)
					next_unsorted_cols.add(col)
					next_unsorted_cols.add(col + 1)
					next_unsorted_rows.add(row)
					changed = True
				
	for col in unsorted_cols:
		changed = True
		while changed:
			changed = False
			for row in range(yi, yi + dy - 1):
				map.move_to(col, row)
				this = measure()
				that = measure(North)
				if (that < this):
					swap(North)
					next_unsorted_rows.add(row)
					next_unsorted_rows.add(row + 1)
					next_unsorted_cols.add(col)
					changed = True
	
	return next_unsorted_rows, next_unsorted_cols
	
def farm(ctx):
	change_hat(Hats.Cactus_Hat)
	pat = map.create_serpentine_pattern(ctx)
	local_ctx = contexts.create_override(ctx)

	# plant all cactii and wait for them to mature
	while True:
		next_pat = []
		contexts.set_value(local_ctx, CACTUS_LIST_KEY, next_pat)
		map.do_for_pattern(pat, farm_plot, local_ctx)
		pat = next_pat
		if len(pat) == 0:
			break
	
	# sort them all
	xi, yi, dx, dy, _ = contexts.get_area(ctx)
	unsorted_rows = set()
	for y in range(yi, yi + dy):
		unsorted_rows.add(y)
		
	unsorted_cols = set()
	for x in range(xi, xi + dx):
		unsorted_cols.add(x)
	
	while len(unsorted_rows) > 0 or len(unsorted_cols) > 0:
		unsorted_rows, unsorted_cols = _sort(ctx, unsorted_rows, unsorted_cols)
	
	return harvest()
	