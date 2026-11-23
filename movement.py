
# # Move to the give spot, using a wrap if it is closer                                
# def move_to(x, y):
# 	_move_to_axis(get_pos_x(), x, get_world_size(), East, West)
# 	_move_to_axis(get_pos_y(), y, get_world_size(), North, South)

# # Move along one axis
# def _move_to_axis(pcurr, pdest, pmax, forward, backward):
# 	if (pcurr == pdest):
# 		return

# 	delta = pdest - pcurr
# 	if delta > 0:
# 		dir = 1
# 	else:
# 		dir = -1
# 		delta = -delta

# 	if delta > pmax / 2:
# 		delta = pmax - delta
# 		dir = -dir
	
# 	if dir == 1:
# 		go = forward
# 	else:
# 		go = backward
	
# 	for _ in range(delta):
# 		move(go)

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
	
# # Performs action once for each cell in the area,
# # stopping when action returns False.
# # Returns True if the entire area was done and action
# # never returned False.
# def do_for_pattern(pattern, action):
# 	current = 0
# 	for pos in pattern:
# 		x, y = pos
# 		if not action():
# 			quick_print("action failed; abandoning pattern")
# 			return False
# 	return True
	