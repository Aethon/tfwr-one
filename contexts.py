# A context is a tuple: (base_context?, area: abs, properties: {})

import areas

def _create(ctx, area):
	return (ctx, area, {})

def create_override(ctx):
	return _create(ctx, None)

def create_override_slice(ctx, sub_area):
	return _create(ctx, areas.get_base_area(get_area(ctx), sub_area))

# Create a global context with a given area.
# The area is forced to absolute.
def create(area):
	return _create(None, areas.force_absolute(area))

def get_value(ctx, key):
	base, _, props = ctx
	if key in props:
		return props[key]
	
	if base != None:
		return get_value(base, key)

	return None

def set_value(ctx, key, value):
	base, _, props = ctx
	props[key] = value

def reset_value(ctx, key):
	base, _, props = ctx
	if key in props:
		props.pop(key)

def get_area(ctx):
	base, area, _ = ctx
	if area != None:
		return area
	if base != None:
		return get_area(base)
	return

