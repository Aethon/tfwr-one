import map
from farm_common import harvest_with_companion

CACTUS_LIST_KEY = "cactii"
NO_OVERPLANTS = [ Entities.Cactus ]

def farm_plot(context):
	global CACTUS_LIST_KEY
	global NO_OVERPLANTS
	
	if get_entity_type() == Entities.Cactus:
		if can_harvest():
			# all good; no need to come back
			return True
	else:        
		harvest_with_companion(context, True, NO_OVERPLANTS)
		if get_ground_type() != Grounds.Soil:
			till()
		plant(Entities.Cactus)
		
	# need to come back and check on it
	context[CACTUS_LIST_KEY].append((get_pos_x(), get_pos_y()))
	return True

def _sort(context, unsorted_rows, unsorted_cols):
	xi, yi, dx, dy = context["area"]
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
	
def farm(context):
	global CACTUS_LIST_KEY
	
	change_hat(Hats.Cactus_Hat)
	
	# plant all cactii and wait for them to mature
	pat = map.create_serpentine_pattern(context["area"])
	context[CACTUS_LIST_KEY] = []
	while map.do_for_pattern(pat, farm_plot, context):
		pat = context[CACTUS_LIST_KEY]
		if len(pat) == 0:
			break
		context[CACTUS_LIST_KEY] = []
	
	# sort them all
	xi, yi, dx, dy = context["area"]
	unsorted_rows = set()
	for y in range(yi, yi + dy):
		unsorted_rows.add(y)
		
	unsorted_cols = set()
	for x in range(xi, xi + dx):
		unsorted_cols.add(x)
	
	while len(unsorted_rows) > 0 or len(unsorted_cols) > 0:
		unsorted_rows, unsorted_cols = _sort(context, unsorted_rows, unsorted_cols)
	
	return harvest()
	