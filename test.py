import inspect
import sys

class TestCase:
	def __init__(self, name):
		self.name = name

	def setUp(self):
		pass

	def run(self, result):
		result.testStarted()
		self.setUp()
		
		try:
			method = getattr(self, self.name)
			method()
		except:
			result.testFailed()

		self.tearDown()

	def tearDown(self):
		pass

class TestResult:
	def __init__(self):
		self.runCount = 0
		self.errorCount = 0

	def testStarted(self):
		self.runCount = self.runCount + 1

	def testFailed(self):
		self.errorCount = self.errorCount + 1

	def summary(self):
		return "%d run, %d failed" % (self.runCount, self.errorCount)

class TestSuite:
	def __init__(self, testCaseClass=None):
		self.tests = []
		if testCaseClass is not None:
			self.addFromTestCase(testCaseClass)
			

	def add(self, test):
		self.tests.append(test)

	def addFromTestCase(self, testCaseClass):
		methods = inspect.getmembers(testCaseClass, inspect.ismethod)
		testMethods = filter(lambda(name, y): name.startswith('test'), methods)
		tests = dict(testMethods).keys()
		for test in tests:
			module = __import__(__name__)
			testCase = getattr(module, testCaseClass.__name__)
			self.add(testCase(test))

	def run(self, result):
		for test in self.tests:
			test.run(result)

class WasRun(TestCase):
	def __init__(self, name):
		TestCase.__init__(self, name)

	def setUp(self):
		self.log = "setUp "

	def testMethod(self):
		self.log = self.log + "testMethod "

	def testBrokenMethod(self):
		raise Exception

	def tearDown(self):
		self.log = self.log + "tearDown"		

class TestCaseTest(TestCase):
	def setUp(self):
		self.result = TestResult()

	def testTemplateMethod(self):
		test = WasRun("testMethod")
		test.run(self.result)
		assert("setUp testMethod tearDown" == test.log)

	def testResult(self):
		test = WasRun("testMethod")
		test.run(self.result)
		assert("1 run, 0 failed" == self.result.summary())

	def testFailedResult(self):
		test = WasRun("testBrokenMethod")
		test.run(self.result)
		assert("1 run, 1 failed" == self.result.summary())		

	def testFailedResultFormatting(self):
		result = TestResult()
		result.testStarted()
		result.testFailed()
		assert("1 run, 1 failed" == result.summary())

	def testSuite(self):
		suite = TestSuite()
		suite.add(WasRun("testMethod"))
		suite.add(WasRun("testBrokenMethod"))
		suite.run(self.result)
		assert("2 run, 1 failed" == self.result.summary())

	def testGetMembers(self):
		methods = inspect.getmembers(WasRun, inspect.ismethod)
		testMethods = filter(lambda(name, y): name.startswith('test'), methods)
		assert(['testBrokenMethod', 'testMethod'] == dict(testMethods).keys())

	def testSuiteFromTestCase(self):
		suite = TestSuite(WasRun)
		suite.run(self.result)
		assert("2 run, 1 failed" == self.result.summary())

suite = TestSuite(TestCaseTest)
result = TestResult()
suite.run(result)
print result.summary()
