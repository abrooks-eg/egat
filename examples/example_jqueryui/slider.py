__author__ = 'Brenda'

from egat.testset import SequentialTestSet
from webdriver_resource import WebDriverResource
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

class Test4(SequentialTestSet):
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
        # Verifying the slider page at starting position
        self.browser.find_element_by_link_text('Slider').click()
        self.browser.get_screenshot_as_file('Screenshots/Slider/slider_pagedisplayed.png')
        self.browser.switch_to_frame(self.browser.find_element_by_css_selector('#content > iframe'))
        self.browser.find_element_by_id('slider').click()
        if self.browser.find_element_by_id('slider'):
            assert(True)
        else:
            assert(False)

    def testStep4(self):
        # Verify that on key simulation, the slider will move to the right
        self.browser.find_element_by_id('slider').send_keys("{RIGHT}")
        wait = WebDriverWait(self.browser,5)
        wait.until(expected_conditions.visibility_of(self.browser.find_element_by_css_selector('#slider > span')))
        self.browser.get_screenshot_as_file('Screenshots/Slider/slider_atfinishpoint.png')
        if self.browser.find_element_by_xpath('//*[@id="slider"]/span').get_attribute('style') == "left: 50%;":
            assert(True)
        else:
            assert(False)

    def testStep5(self):
        # Close browser window
        self.browser.quit()