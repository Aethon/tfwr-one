from movement import move_to

# pattern_node {
#    data:
#     next:
#    prev:
# }
_next_dlist_id = 0

def _make_dlist_node(data):
	global _next_dlist_id
	node = { "id": _next_dlist_id }
	_next_dlist_id = _next_dlist_id + 1
	if data != None:
		node["data"] = data
	return node
	
def make_dlist():
	node = _make_dlist_node(None)
	node["prev"] = node
	node["next"] = node
	return node

def is_empty_dlist(node):
	id = node["id"]
	return node["next"]["id"] == id and node["prev"]["id"] == id
				
def add_node_after(data, node):
	new = _make_dlist_node(data)
	new["prev"] = node
	new["next"] = node["next"]
	node["next"] = new
	new["next"]["prev"] = new
	return new

def add_node_before(data, node):
	new = _make_dlist_node(data)
	new["next"] = node
	new["prev"] = node["prev"]
	node["prev"] = new
	new["prev"]["next"] = new
	return new

def remove_node(node):
	node["prev"]["next"] = node["next"]
	node["next"]["prev"] = node["prev"]

def nodes_are_same(a, b):
	return a["id"] == b["id"]
	
def make_serpentine_pattern(start, size):
	xi, yi = start
	dx, dy = size
	pattern = make_dlist()
	last = pattern
	for x in range(xi, dx):
		if x % 2 == 0:
			r = range(yi, dy)
		else:
			r = range(yi + dy - 1, yi - 1, -1)
		for y in r:
			add_node_after({ "x": x, "y": y }, last)
	return pattern

def make_world_serpentine():
	return make_serpentine_pattern((0, 0), (get_world_size(), get_world_size()))
	
def do_for_pattern(pattern, action):
	here = pattern["next"]
	while not nodes_are_same(here, pattern):
		data = here["data"]
		move_to(data["x"], data["y"])
		result = action()
		if result == 1:
			here = here["next"]
			return 1 # done
		if result == 2:
			remove_node(here)
		here = here["next"]
				
	return 0