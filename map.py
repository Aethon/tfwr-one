import areas
import contexts

_dx = None
_dy = None
_plots = None
_area = None
_ctx = None

# Move to the give spot, using a wrap if it is closer                                
def move_to_pos(pos):
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
	global _area
	global _ctx

	clear()
	
	if size == None:
		size = get_world_size()
	else:
		set_world_size(size)
	
	_dx = size
	_dy = size
	
	_plots = []
				
	for x in range(0, _dx):
		for y in range(0, _dy):
			plot = {
				"pos": (x, y)
			}
			if init_plot != None:
				init_plot(plot)
			_plots.append(plot)
	
	_area = areas.create_absolute(0, 0, _dx, _dy)
	_ctx = contexts.create(_area)

def get_area():
	return _area
	
def get_context():
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
		x0 = None
		y0 = None
		cx = None
		cy = None
	else:
		x0, y0, cx, cy = area

	x0 = _normalize_axis_start(x0, _dx)
	y0 = _normalize_axis_start(y0, _dy)
	cx = _normalize_axis_count(cx, x0, _dx)
	cy = _normalize_axis_count(cy, y0, _dy)    
				
	return x0, y0, cx, cy


def create_serpentine_pattern(ctx):
	x0, y0, cx, cy, _ = contexts.get_area(ctx)
	
	pattern = []
	for x in range(x0, x0 + cx):
		if x % 2 == 0:
			r = range(y0, y0 + cy)
		else:
			r = range(y0 + cy - 1, y0 - 1, -1)
		for y in r:
			pattern.append((x, y))
	return pattern

def create_ouroboros_pattern(ctx):
	x0, y0, cx, cy, _ = contexts.get_area(ctx)
	
	pattern = []
	for x in range(x0, x0 + cx):
		pattern.append((x, y0))
	
	for x in range(x0 + cx - 1, x0 - 1, - 1):
		if x % 2 == 1:
			r = range(y0 + 1, y0 + cy)
		else:
			r = range(y0 + cy - 1, y0, -1)
		for y in r:
			pattern.append((x, y))
	return pattern

def do_for_pattern(pattern, action, ctx):
	current = 0
	for pos in pattern:
		x, y = pos
		move_to(x, y)
		if not action(ctx):
			return False
	return True

	