__author__ = 'Brenda'

from egat.testset import SequentialTestSet
from webdriver_resource import WebDriverResource
from selenium import webdriver
import time
from selenium.webdriver.support.ui import Select

class Test7(SequentialTestSet):
    def testStep1(self):
        # We can access the configuration parameters from inside any test function.
        base_url = self.configuration["base_url"]
        port = self.configuration["port"]

    @WebDriverResource.decorator
    def testStep2(self):
        # Verifying that the page is loaded and exists by checking for a specific meta content identifier
        self.browser = webdriver.Firefox()
        self.browser.get("http://jqueryui.com")
        if self.browser.find_element_by_css_selector("meta[name='author']"):
            assert(True)
        else:
            assert(False)

    def testStep3(self):
        # Verifying the Select a Speed page at starting position
        self.browser.find_element_by_link_text('Hide').click()
        self.browser.get_screenshot_as_file('Screenshots/Hide/hide_pagedisplayed.png')
        self.browser.switch_to_frame(self.browser.find_element_by_css_selector('#content > iframe'))
        element1 = self.browser.find_element_by_id('effect').text
        if ("hendrerit vitae, mi." in element1):
            assert(True)
        else:
            assert(False)

    def testStep4(self):
        # Verifying that the hide effect occurs
        time.sleep(3)
        while self.browser.find_element_by_id('button').click():
            self.browser.get_screenshot_as_file('Screenshots/Hide/hidden_effect_blind.png')
            if "hidden" in self.browser.find_element_by_xpath('/*[@id="effect"]').get_attribute('style'):
                assert(True)
            else:
                assert(False)

    def testStep5(self):
        # Change the effect type
        select = Select(self.browser.find_element_by_id('effectTypes'))
        select.select_by_visible_text('Bounce')
        if self.browser.find_element_by_xpath('//*[@id="effectTypes"]/option[2]'):
            assert(True)
        else:
            assert(False)

    def testStep6(self):
         # Verifying that the hide effect occurs
         while self.browser.find_element_by_id('button').click():
            self.browser.get_screenshot_as_file('Screenshots/Hide/hidden_effect_bounce.png')
            if "hidden" in self.browser.find_element_by_xpath('/*[@id="effect"]').Select():
                assert(True)
            else:
                assert(False)
         time.sleep(3)

    def testStep7(self):
        self.browser.quit()