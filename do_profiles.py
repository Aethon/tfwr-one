import map
import farm_context
import profile
import farm_pumpkin

map.init(None, None)

contexts = []
#contexts.append(profile.create_context((5, 5), "farm pumpkin"))
#contexts.append(profile.create_context((10, 10), "farm pumpkin"))
contexts.append(profile.create_context((15, 15), "farm pumpkin"))
#wc = profile.create_context((15, 15), "farm pumpkin with water")
#farm_context.set_water_to(wc, 1)
#contexts.append(wc)

profile.profile_context_set(pumpkin.farm, Items.Pumpkin, contexts, 2)