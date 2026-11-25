import contexts

_FERTILIZE_KEY = "fertilize"
_WATER_TO_KEY = "water_to"
_PLANT_COMPANIONS = "plant_companions"
_DO_NOT_OVERPLANT = "do_not_overplant"
_POWER_TO = "power_to"

_CHECK_FARMING_GOAL = "check_farming_goal"

def use_fertilizer(ctx):
	val = contexts.get_value(ctx, _FERTILIZE_KEY)
	if val != None:
		return val == True
	return False

def water_to(ctx):
	val = contexts.get_value(ctx, _WATER_TO_KEY)
	if val != None:
		return val
	return 0.0

def power_to(ctx):
	return contexts.get_value(ctx, _POWER_TO)

def check_farming_goal(ctx):
	fn = contexts.get_value(ctx, _CHECK_FARMING_GOAL)
	if fn == None:
		return True
	return fn(ctx)

def set_use_fertilizer(ctx, value):
	contexts.set_value(ctx, _FERTILIZE_KEY, value == True)

def set_water_to(ctx, value):
	contexts.set_value(ctx, _WATER_TO_KEY, value)

def set_power_to(ctx, value):
	contexts.set_value(ctx, _POWER_TO, value)

def set_farming_goal_check(ctx, item, count):
	def check(ctx):
		return num_items(item) > count
	contexts.set_value(ctx, _CHECK_FARMING_GOAL, check)
