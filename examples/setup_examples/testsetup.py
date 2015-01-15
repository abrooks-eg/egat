from egautotest.testset import SequentialTestSet
from egautotest.testset import UnorderedTestSet
from selenium import webdriver

# In the SequentialTestSet, the setup and teardown methods will be called before any
# tests are executed and after all tests are finished, respectively. If you run 
# these tests you will see that the browser only launches once. 
#
# This is a special behavior which is built into the TestRunner, so 'setup' and 
# 'teardown' are reserved keywords when working with the TestSet class.
class TestSetupAndTeardown1(SequentialTestSet):
    def setup(self):
        self.browser = webdriver.Firefox()

    def testDuck(self):
        self.browser.get("http://duckduckgo.com")

    def testGoogle(self):
        self.browser.get("http://google.com")

    def testBing(self):
        self.browser.get("http://bing.com")
        assert(False)

    def testYahoo(self):
        self.browser.get("http://yahoo.com")

    def teardown(self):
        self.browser.quit()

# In the UnorderedTestSet, the setup and teardown methods will be called before each
# test method and after each test method , respectively. If you run these tests you 
# will see the browser launch before each test and quit after each test.
class TestSetupAndTeardown2(UnorderedTestSet):
    def setup(self):
        self.browser = webdriver.Firefox()

    def testDuck(self):
        self.browser.get("http://duckduckgo.com")

    def testGoogle(self):
        self.browser.get("http://google.com")

    def testBing(self):
        self.browser.get("http://bing.com")
        assert(False)

    def testYahoo(self):
        self.browser.get("http://yahoo.com")

    def teardown(self):
        self.browser.quit()
