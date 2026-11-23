# creates an error condition at runtime
# with `message` displayed
def fail(message):
	change_hat(Hats.Traffic_Cone)
	x = 1 + message

# asserts that `val` is truthy
# or fails with a message
def assert(val, message):
	if not val:
		fail(message)

# asserts that `val` is not truthy
# or fails with a message
def assert_not(val, message):
	if val:
		fail(message)

# asserts that `val` is not truthy
# or fails with a message
def assert_equal(actual, expected):
	if actual != expected:
		fail(str(actual) + " did not equal " + str(expected))