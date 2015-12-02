# SOME FUNCTIONs to be used internally inside the
# Project to provide simplification

class Debugger():

	def __init__(self, debug_switch=False):
		self.debug_switch = debug_switch

	def set_debug(self, to):
		self.debug_switch = to

	def debug(self, *args):
		if (self.debug_switch):
			for argument in args:
				print(argument)
