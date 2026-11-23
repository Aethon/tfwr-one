import areas
import contexts
_dx = None
_dy = None
_plots = None
_ctx = None

# Move to the give spot, using a wrap if it is closer                                
def move_to_pos(pos):
	global _dx
	global _dy
	x, y = pos
	_move_to_axis(get_pos_x(), x, _dx, East, West)
	_move_to_axis(get_pos_y(), y, _dx, North, South)
		
# Move to the give spot, using a wrap if it is closer                                
def move_to(x, y):
	_move_to_axis(get_pos_x(), x, get_world_size(), East, West)
	_move_to_axis(get_pos_y(), y, get_world_size(), North, South)

# Move along one axis
def _move_to_axis(pcurr, pdest, pmax, forward, backward):
	if (pcurr == pdest):
		return

	delta = pdest - pcurr
	if delta > 0:
		dir = 1
	else:
		dir = -1
		delta = -delta

	if delta > pmax / 2:
		delta = pmax - delta
		dir = -dir
	
	if dir == 1:
		go = forward
	else:
		go = backward
	
	for _ in range(delta):
		move(go)
		
def init(size, init_plot):
	global _dx
	global _dy
	global _plots
	global _ctx

	clear()
	
	world_size = get_world_size()
	
	if size == None:
		_dx = world_size
		_dy = world_size
	else:
		dx, dy = size
		_dx = max(min(dx, world_size), 1)
		_dy = max(min(dy, world_size), 1)
	
	_plots = []
				
	for x in range(0, _dx):
		for y in range(0, _dy):
			plot = {
				"pos": (x, y)
			}
			if init_plot != None:
				init_plot(plot)
			_plots.append(plot)

	_ctx = context.create((0, 0, _dx, _dy))

def ctx():
	return _ctx

def get_size():
	return _dx, _dy
	
def get_plot(pos):
	x, y = pos
	return _plots[x * _dy + y]
	
def _normalize_axis_start(ni, map_dn):
	if ni == None:
		return 0
	return min(max(ni, 0), map_dn - 1)

# map_ni--ni---dn-->--map_dn 
def _normalize_axis_count(dn, ni, map_dn):
	if dn == None:
		return map_dn - ni
	
	if ni + dn > map_dn:
		return map_dn - ni

	return dn
		
def normalize(area):
	global _dx
	global _dy
	if area == None:
		xi = None
		yi = None
		dx = None
		dy = None
	else:
		xi, yi, dx, dy = area

	xi = _normalize_axis_start(xi, _dx)
	yi = _normalize_axis_start(yi, _dy)
	dx = _normalize_axis_count(dx, xi, _dx)
	dy = _normalize_axis_count(dy, yi, _dy)    
				
	return xi, yi, dx, dy
	
def is_in_area(pos, area):
	x, y = pos
	xi, yi, dx, dy = area
	return not (x < xi or x >= xi + dx or y < yi or y >= yi + dy)

def get_pos_in_area(pos, area):
	x, y = pos
	xi, yi, dx, dy = area
	in_pos = min(xi + max(x, 0), dx), min(yi + max(y, 0), dy)
	return in_pos
		
def create_serpentine_pattern(area):
	xi, yi, dx, dy = normalize(area)
	
	pattern = []
	for x in range(xi, xi + dx):
		if x % 2 == 0:
			r = range(yi, yi + dy)
		else:
			r = range(yi + dy - 1, yi - 1, -1)
		for y in r:
			pattern.append((x, y))
	return pattern
	
def do_for_pattern(pattern, action, context):
	current = 0
	for pos in pattern:
		x, y = pos
		move_to(x, y)
		if not action(context):
			return False
	return True

	