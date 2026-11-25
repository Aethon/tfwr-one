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

def pow2(exp):
	if exp == 0:
		return 1
	val = 2
	for _ in range(exp, 1, -1):
		val = val * 2
	return val

def ceil(val):
	whole = val // 1
	if val % 1 == 0:
		return whole
	return whole + 1