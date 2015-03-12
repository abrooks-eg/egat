__author__ = 'Brenda'

from egat.testset import SequentialTestSet
from webdriver_resource import WebDriverResource
from selenium import webdriver
import time

class Test9(SequentialTestSet):
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
        # Verifying the autocomplete page at starting position
        self.browser.find_element_by_link_text('Autocomplete').click()
        self.browser.get_screenshot_as_file('Screenshots/Autocomplete/autocomplete_pagedisplayed.png')
        self.browser.switch_to_frame(self.browser.find_element_by_tag_name('iframe'))
        self.browser.find_element_by_id('tags')
        if self.browser.find_element_by_id('tags'):
            assert(True)
        else:
            assert(False)

    def testStep4(self):
        # Verify that the Tags field is blank
        if "display: none;" in self.browser.find_element_by_id('ui-id-1').get_attribute('style'):
            assert(True)
        else:
            assert(False)

    def testStep5(self):
        # Verifying that Java is present when entering "ja"
        self.browser.find_element_by_id('tags').send_keys('ja')
        time.sleep(5)
        self.browser.get_screenshot_as_file('Screenshots/Autocomplete/autocomplete_entered.png')
        print self.browser.find_element_by_tag_name('li').text
        element2 = self.browser.find_element_by_tag_name('li').text
        if "Java" in element2:
            assert(True)
        else:
            assert(False)

    def testStep6(self):
        self.browser.quit()