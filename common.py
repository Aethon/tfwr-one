def format_number(num):
	if num < 1000:
		return str(num)
	if num < 1000000:
		return str(num / 1000) + "K"
	if num < 1000000000:
		return str(num / 1000000) + "M"
	if num < 1000000000000:
		return str(num / 1000000000) + "B"
	return str(num / 1000000000000) + "T"
    