# import map

# def create(start, size, hat, init_pattern, init_plot):
# 	if start == None:
# 		xi = 0
# 		yi = 0
# 	else:
# 		xi, yi = start
			
# 	if size == None:
# 		dx = get_world_size()
# 		dy = dx
# 	else:
# 		dx, dy = size
	
# 	map = []
		
# 	context = {
# 		"start": (xi, yi),
# 		"size": (dx, dy),
# 		"hat": hat,
# 		"plot_map": map
# 	}

# 	for x in range(xi, dx):
# 		for y in range(yi, dy):
# 			plot = {
# 				"context": context,
# 				"pos": (x, y),
# 				"planted": None,
# 				"is_companion_for": None,
# 				"petal_count": None
# 			}
# 			if init_plot != None:
# 				init_plot(plot)
# 			map.append(plot)
	
# 	context["pattern"] = make_pattern((xi,yi), (dx_dy), map)
	
# def get_plot(context, pos):
# 	dx, dy = context["size"]
# 	x, y = pos
# 	return context["plot_map"][x * dy + y]
	
# def init_serpentine_pattern(context):
# 	xi, yi = context["start"]
# 	dx, dy = context["size"]
# 	pattern = make_dlist()
# 	last = pattern
# 	for x in range(xi, dx):
# 		if x % 2 == 0:
# 			r = range(yi, dy)
# 		else:
# 			r = range(yi + dy - 1, yi - 1, -1)
# 		for y in r:
# 			add_node_after(get_plot(context, (x, y), last))
# 	context["pattern"] = pattern
 

   
# def create_serpentine_pattern(xi, yi, dx, dy):
# 	xi = max(xi, 0)
# 	yi = max(yi, 0)
# 	dx = min(dx, map.dx())
# 	dy = min(dy, map.dy())
	
# 	pattern = []
# 	for x in range(xi, dx):
# 		if x % 2 == 0:
# 			r = range(yi, dy)
# 		else:
# 			r = range(yi + dy - 1, yi - 1, -1)
# 		for y in r:
# 			pattern,append((x, y))
# 	return pattern
	
# def do_for_pattern(pattern, action):
# 	current = 0
# 	for pos in pattern:
# 		if not action():
# 			return False
# 	return True