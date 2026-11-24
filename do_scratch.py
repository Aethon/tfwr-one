import map
import areas
import contexts
import farm_gold

map.init(None, None)

ctx = contexts.create_override_slice(map.get_context(), areas.create_relative(0, 0, 10, 10))
farm_gold.farm(map.get_context())
