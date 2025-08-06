import harmonify

def open_api1():
	print("Doing API stuff...")

@harmonify.allow_inject
def open_api2():
	print("More API stuff...")

@harmonify.no_inject
def restricted_api(uname, passwd):
	print(f"Doing restricted API access with:\n\tUsername: {uname}\n\tPassword: {passwd}")