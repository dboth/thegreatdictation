# WORD ALIGNER
# Processing the Levenshtein Data to align input words to output words

# TO BE DONE

import frames

class WordAligner(object):
	def __init__(self, lev, inp, target):

		# DEBUGGER DONT TOUCH
		self.d = frames.Debugger()
		self.debug = self.d.debug

		# VALUES
		self.lev = lev
		self.inp = inp
		self.target = target
		self.createPositionMap()

	def createPositionMap(self):
		pass

	def calcWordErrors(self):
		pass

	def finalize(self):
		self.debug("TEST RUN INITIALIZED\n--------------------")

if __name__ == "__main__":
	import levenshtein as lev

	levenshtein = lev.levenshtein("Ich bin Elefant", "Ich bin ein Elefant")
	w = WordAligner(levenshtein, "Ich bin Elefant", "Ich bin ein Elefant")

	w.d.debug_switch = True

	w.finalize()
