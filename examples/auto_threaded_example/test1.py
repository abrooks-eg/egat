import egat.testset as testset
from selenium import webdriver

class Test1(testset.UnorderedTestSet):
    browser = None

    def setup(self):
        self.browser = webdriver.Firefox()

    def teardown(self):
        self.browser.quit()

    def test_step1(self):
        self.browser.get("http://www.google.com")

    def test_step2(self):
        self.browser.get("http://www.duckduckgo.com")

    def test_step3(self):
        self.browser.get("http://www.bing.com")
