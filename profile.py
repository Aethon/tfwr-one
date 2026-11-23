import map
import farm_context

_PROFILE_DESCRIPTION_KEY = "profile_description"

def create_context(size, description):
    dx, dy = size
    context = farm_context.create((0, 0, dx, dy))
    context[_PROFILE_DESCRIPTION_KEY] = description
    return context

def profile_context(action, item, context, count):
    map.init(None, None)
	start_count = num_items(item)
	start = get_time()
	for i in range(0, count):
        action(context)
	end = get_time()
	end_count = num_items(item)
	return end - start, end_count - start_count

def profile_context_set(action, item, contexts, count):
	for context in contexts:
		time, gain = profile_context(action, item, context, count)
        xi, yi, dx, dy = farm_context.get_area(context)
		quick_print(context[_PROFILE_DESCRIPTION_KEY], "(", dx, "x", dy, ")", "took", time, "and gained", gain, item, "(", gain/time, "rate )")
