
class TestCase:
	def __init__(self, name):
		self.name = name
	pass

class WasRun(TestCase):
	def __init__(self, name):
		self.wasRun = None
		TestCase.__init__(self, name)

	def run(self):
		method = getattr(self, self.name)
		method()

	def testMethod(self):
		self.wasRun = 1


test = WasRun("testMethod")
print test.wasRun
test.run()
print test.wasRun
