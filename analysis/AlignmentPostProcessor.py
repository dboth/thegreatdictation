class AlignmentPostProcessor():
	def __init__(self, alignment):
		self.alignment = alignment

	def convertToWordAlignment(self):
		"""
			Creates a wordwise alignment based on self.alignment (characterwise).
			Outputs in dict format:
				{ TARGET_START_INDEX: [TARGET_END_INDEX, TARGET_STRING, INPUT_STRING, INPUT_START_INDEX, INPUT_END_INDEX, ERROR_WEIGHT_OF_INPUT] }
				e.g. { 5: [8, "Maus", "Haus", 4, 7, 1]}
				all indices are INCLUSIVE!
		"""

		return self.alignment

if __name__ == "__main__":
	import aligner
	a = aligner.Aligner(u"julia hallo", u"Hallo Julia")

	app = AlignmentPostProcessor(a.finalize())
	print(app.convertToWordAlignment())
