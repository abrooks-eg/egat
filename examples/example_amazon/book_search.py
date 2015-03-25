__author__ = 'Brenda'

from egat.testset import SequentialTestSet
from webdriver_resource import WebDriverResource
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from egat.execution_groups import execution_group


@execution_group("test1")
class Test1(SequentialTestSet):
    def testStep1(self):
        # We can access the configuration parameters from inside any test function.
        base_url = self.configuration["base_url"]
        port = self.configuration["port"]

    @WebDriverResource.decorator
    def testStep2(self):
        if self.environment.get('browser', '') == "Chrome":
            self.browser = webdriver.Chrome()
        elif self.environment.get('browser', '') == "Firefox":
            self.browser = webdriver.Firefox()
        else:
            self.browser = webdriver.Firefox()
        self.browser.maximize_window()
        self.browser.get("http://www.amazon.com")
        time.sleep(5)
        if self.browser.find_element_by_link_text('Amazon'):
            assert(True)
        else:
            assert(False)

    def testStep3(self):
        all_spans = self.browser.find_elements_by_xpath('//*[@id="nav-signin-text"]')
        for span in all_spans:
            if "Sign in" in span.text:
                span.send_keys(Keys.ALT,Keys.ARROW_LEFT)
                assert(True)
            else:
                assert(False)
                self.browser.quit()

    def testStep4(self):
        # Entering search criteria
        self.browser.find_element_by_id('twotabsearchtextbox').click()
        self.browser.find_element_by_id('twotabsearchtextbox').send_keys('python')
        self.browser.find_element_by_id('twotabsearchtextbox').send_keys(Keys.ENTER)
        if "Show results for" in self.browser.find_element_by_class_name('shoppingEngineSectionHeaders').text:
            assert(True)
        else:
            assert(False)

    def testStep5(self):
        # Verifying objects returned in search criteria
        if self.browser.find_element_by_partial_link_text('Learning Python, 5th Edition'):
            assert(True)
        else:
            assert(False)

    def testStep6(self):
        # Opening result
        self.browser.find_element_by_link_text('Learning Python, 5th Edition').click()
        all_spans = self.browser.find_elements_by_xpath('//*[@id="productTitle"]')
        for span in all_spans:
            if 'Learning Python, 5th Edition' in span.text:
                assert(True)
            else:
                assert(False)

    def testStep7(self):
        # Verify that this is a best seller
        if self.browser.find_element_by_class_name('p13n-best-seller-badge'):
            assert(True)
        else:
            assert(False)

    def testStep8(self):
        # Verify options to buy or rent
        all_spans = self.browser.find_elements_by_xpath('//*[@id="combinedPriceBlock"]/div/div[2]/div[1]/span')
        for span in all_spans:
            if 'Rent' in span.text:
                assert(True)
            else:
                assert(False)
        other_spans = self.browser.find_elements_by_xpath('//*[@id="combinedPriceBlock"]/div/div[1]/div[1]/span')
        for span in other_spans:
            if 'Buy New' in span.text:
                assert(True)
            else:
                assert(False)

    def testStep9(self):
        # Tear down step
        self.browser.quit()