from egat.testset import UnorderedTestSet
from selenium import webdriver

class MultipleBrowserTest(UnorderedTestSet):
    def setup(self): 
        if self.environment.get('browser', '') == "Chrome":
            self.browser = webdriver.Chrome()
        elif self.environment.get('browser', '') == "Firefox":
            self.browser = webdriver.Firefox()
        else:
            self.browser = webdriver.Firefox()

    def teardown(self):
        self.browser.quit()

    def test_open_eg_home(self):
        self.browser.get("http://e-gineering.com")

    def test_open_eg_contact(self):
        self.browser.get("http://e-gineering.com/contact.html")
