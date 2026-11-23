import contexts

_FERTILIZE_KEY = "fertilize"
_WATER_TO_KEY = "water_to"
_PLANT_COMPANIONS = "plant_companions"
_DO_NOT_OVERPLANT = "do_not_overplant"

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

def set_use_fertilizer(ctx, value):
	contexts.set_value(ctx, _FERTILIZE_KEY, value == True)

def set_water_to(ctx, value):
	contexts.set_value(ctx, _WATER_TO_KEY, value)

