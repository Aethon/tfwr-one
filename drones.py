
def run_work(drone_work, direct_work):
	drone_results = []
	direct_results = []

	drones = []
	while len(drone_work) > 0 or len(direct_work) or len(drones) > 0:

		while len(drone_work) > 0:
			task = drone_work[0]
			drone = spawn_drone(task)
			if drone == None:
				break
			drone_work.pop(0)
			drones.append(drone)

		if direct_work != None and len(direct_work) > 0:
			task = direct_work.pop(0)
			direct_results.append(task())

		if len(drones) > 0:
			drone = drones.pop(0)
			drone_results.append(wait_for(drone))

	return (drone_results, direct_results)
