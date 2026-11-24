import strategy

available_unlocks = strategy.get_available_unlocks()
unlock_cost_map = strategy.get_selected_unlock_costs(available_unlocks, None)

strategy.dump_unlock_costs(unlock_cost_map)

selected_unlock, selected_cost_map = strategy.select_next_unlock(unlock_cost_map)
quick_print()
quick_print("Selected", selected_unlock)
