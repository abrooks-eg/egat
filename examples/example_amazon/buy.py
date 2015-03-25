__author__ = 'Brenda'

from egat.testset import SequentialTestSet
from webdriver_resource import WebDriverResource
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from egat.execution_groups import execution_group

@execution_group("test3")
class Test3(SequentialTestSet):
    def testStep1(self):
        # We can access the configuration parameters from inside any test function.
        base_url = self.configuration["base_url"]
        port = self.configuration["port"]

    @WebDriverResource.decorator
    def testStep2(self):
        # Verifying that the page is loaded and exists by checking for a specific meta content identifier
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
        # Search for and select book
        self.browser.find_element_by_id('twotabsearchtextbox').click()
        self.browser.find_element_by_id('twotabsearchtextbox').send_keys('python')
        self.browser.find_element_by_id('twotabsearchtextbox').send_keys(Keys.ENTER)
        time.sleep(5)
        self.browser.find_element_by_link_text('Learning Python, 5th Edition').click()

    def testStep4(self):
        # Adding book to cart
        self.browser.find_element_by_xpath('//*[@id="buyNewSection"]').click()

    def testStep5(self):
        self.browser.find_element_by_xpath('//*[@id="add-to-cart-button"]').click()
        checkout_span = self.browser.find_elements_by_xpath('//*[@id="confirm-text"]')
        for span in checkout_span:
            if "1 item added to Cart" in span.text:
                assert(True)
            else:
                assert(False)
        time.sleep(10)

    def testStep6(self):
        self.browser.quit()