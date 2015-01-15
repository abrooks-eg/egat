from egautotest.testset import UnorderedTestSet
from selenium import webdriver 

class TestSeleniumDebugging(UnorderedTestSet):
    def setup(self):
        self.browser = webdriver.Firefox()

    def teardown(self):
        self.browser.quit()

    def testDuck(self):
        self.browser.get("http://duckduckgo.com")

    def testGoogle(self):
        self.browser.get("http://google.com")

    def testBing(self):
        self.browser.get("http://bing.com")
        assert(False)

    def testYahoo(self):
        self.browser.get("http://yahoo.com")
