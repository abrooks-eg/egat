__author__ = 'Brenda'

from egat.testset import SequentialTestSet
from webdriver_resource import WebDriverResource
from selenium import webdriver
import time

class Test5(SequentialTestSet):
    def testStep1(self):
        # We can access the configuration parameters from inside any test function.
        base_url = self.configuration["base_url"]
        port = self.configuration["port"]

    @WebDriverResource.decorator
    def testStep2(self):
        # Verifying that the page is loaded and exists by checking for a specific meta content identifier
        self.driver = webdriver.Firefox()
        self.driver.get("http://jqueryui.com")
        if self.driver.find_element_by_css_selector("meta[name='author']"):
            assert(True)
        else:
            assert(False)

    def testStep3(self):
        # Verifying the toggle class page at starting position
        self.driver.find_element_by_link_text('Toggle Class').click()
        time.sleep(3)
        self.driver.get_screenshot_as_file('Screenshots/Toggle_class/toggleclass_pagedisplayed.png')
        self.driver.switch_to_frame(self.driver.find_element_by_css_selector('#content > iframe'))
        if self.driver.find_element_by_class_name('newClass'):
            assert(True)
        else:
            assert(False)

    def testStep4(self):
        # Click button to toggle class
        self.driver.find_element_by_id('button').click()
        time.sleep(3)
        self.driver.get_screenshot_as_file('Screenshots/Toggle_class/toggleclass_toggled.png')
        if self.driver.find_element_by_class_name('ui-corner-all'):
            assert(True)
        else:
            assert(False)

    def testStep5(self):
        # Click button to toggle class
        self.driver.find_element_by_id('button').click()
        time.sleep(3)
        self.driver.get_screenshot_as_file('Screenshots/Toggle_class/toggleclass_toggled_again.png')
        if self.driver.find_element_by_class_name('newClass'):
            assert(True)
        else:
            assert(False)

    def testStep6(self):
        self.driver.quit()