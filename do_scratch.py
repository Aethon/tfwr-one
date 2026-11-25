import common

import map
import areas
import contexts
# import farm
import farm_context
# import farm_weird
# import farm_gold
# import farm_cactus
import farm_pumpkin
# import farm_bones
# import farm_carrots
import farm_power

map.init(32, None)

# def color_d(info):
#     area, id = info
#     def _color(_):
#         n = id % 3
#         if n == 0:
#             plant(Entities.Grass)
#         elif n == 1:
#             plant(Entities.Bush)
#         else:
#             till()
#         return True

#     ctx = contexts.create(area)
#     pat = map.create_serpentine_pattern(ctx)

#     map.do_for_pattern(pat, _color, ctx)

# sub_areas = areas.divide(map.get_area(), 7, 3, 32, True)
# print(len(sub_areas))
# id = 0
# for sub in sub_areas:
#     spawn_drone(color_d, (sub, id))
#     id = id + 1

ctx = contexts.create_override(map.get_context())
farm_context.set_farming_goal_check(ctx, Items.Pumpkin, 400000000)
farm_pumpkin.farm_crop(ctx)

# #farm.dump_crop_costs(Items.Hay, farm.get_crop_costs(map.get_context(), Items.Hay, 1000000))
# #farm.dump_crop_costs(Items.Gold, farm.get_crop_costs(map.get_context(), Items.Gold, 1000000))