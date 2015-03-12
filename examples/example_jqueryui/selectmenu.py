__author__ = 'Brenda'

from egat.testset import SequentialTestSet
from webdriver_resource import WebDriverResource
from selenium import webdriver

class Test6(SequentialTestSet):
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
        self.browser.find_element_by_link_text('Selectmenu').click()
        self.browser.get_screenshot_as_file('Screenshots/Selectmenu/selectmenu_pagedisplayed.png')
        self.browser.switch_to_frame(self.browser.find_element_by_css_selector('#content > iframe'))
        if self.browser.find_element_by_class_name('ui-selectmenu-text').text == "Medium":
            assert(True)
        else:
            assert(False)

    def testStep4(self):
        # Changing Select a Speed from Medium to Slow
        self.browser.find_element_by_class_name('ui-selectmenu-text').click()
        self.browser.find_element_by_xpath('//*[@id="ui-id-2"]').click()
        if self.browser.find_element_by_class_name('ui-selectmenu-text').text == "Slow":
            assert(True)
            self.browser.get_screenshot_as_file('Screenshots/Selectmenu/speed_change.png')
        else:
            assert(False)

    def testStep5(self):
        # Verifying the Select a File at starting position
        if self.browser.find_element_by_xpath('//*[@id="files-button"]/span[2]').text == "jQuery.js":
            assert(True)
        else:
            assert(False)

    def testStep6(self):
        # Changing the Select a File from jQuery.js to Some unknown file
        self.browser.find_element_by_xpath('//*[@id="files-button"]/span[2]').click()
        self.browser.find_element_by_xpath('//*[@id="ui-id-8"]').click()
        if self.browser.find_element_by_xpath('//*[@id="files-button"]/span[2]').text == "Some unknown file":
            assert(True)
            self.browser.get_screenshot_as_file('Screenshots/Selectmenu/file_change.png')
        else:
            assert(False)

    def testStep7(self):
        # Verify the Select a number at starting position
        if self.browser.find_element_by_xpath('//*[@id="number-button"]/span[2]').text == "2":
            assert(True)
        else:
            assert(False)

    def testStep8(self):
        # changing the Select a number from 2 to 6
        self.browser.find_element_by_xpath('//*[@id="number-button"]/span[2]').click()
        self.browser.find_element_by_xpath('//*[@id="ui-id-15"]').click()
        if self.browser.find_element_by_xpath('//*[@id="number-button"]/span[2]').text == '6':
            assert(True)
            self.browser.get_screenshot_as_file('Screenshots/Selectmenu/number_change.png')
        else:
            assert(False)

    def testStep9(self):
        self.browser.quit()