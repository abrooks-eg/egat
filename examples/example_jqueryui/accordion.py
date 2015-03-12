__author__ = 'Brenda'

from egat.testset import SequentialTestSet
from webdriver_resource import WebDriverResource
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

class Test2(SequentialTestSet):
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
        # Verifying the accordion page at starting position
        self.browser.find_element_by_link_text('Accordion').click()
        self.browser.get_screenshot_as_file('Screenshots/Accordion/accordion_pagedisplayed.png')
        self.browser.switch_to_frame(self.browser.find_element_by_css_selector('#content > iframe'))
        element1 = self.browser.find_element_by_id('ui-id-1')
        assert element1.text == 'Section 1'
        element2 = self.browser.find_element_by_id('ui-id-2').text
        if ("Mauris mauris ante" in element2):
            self.browser.get_screenshot_as_file('Screenshots/Accordion/accordion_section1.png')
            assert(True)
        else:
            assert(False)

    def testStep4(self):
        # Attempt to click on next section to view accordion effect
        self.browser.find_element_by_id('ui-id-3').click()
        WebDriverWait(self.browser, 5).until(expected_conditions.visibility_of(self.browser.find_element_by_id('ui-id-4')))
        element3 = self.browser.find_element_by_id('ui-id-3')
        assert element3.text == 'Section 2'
        element4 = self.browser.find_element_by_id('ui-id-4').text
        if ("Sed non urna" in element4):
            self.browser.get_screenshot_as_file('Screenshots/Accordion/accordion_section2.png')
            assert(True)
        else:
            assert(False)

    def testStep5(self):
        # Attempt to click on next section to view accordion effect
        self.browser.find_element_by_id('ui-id-5').click()
        WebDriverWait(self.browser, 5).until(expected_conditions.visibility_of(self.browser.find_element_by_id('ui-id-6')))
        element5 = self.browser.find_element_by_id('ui-id-5')
        assert element5.text == 'Section 3'
        element6 = self.browser.find_element_by_id('ui-id-6').text
        if ("List item one" in element6):
            self.browser.get_screenshot_as_file('Screenshots/Accordion/accordion_section3.png')
            assert(True)
        else:
            assert(False)

    def testStep6(self):
        # Attempt to click on next section to view accordion effect
        self.browser.find_element_by_id('ui-id-7').click()
        WebDriverWait(self.browser, 5).until(expected_conditions.visibility_of(self.browser.find_element_by_id('ui-id-8')))
        element7 = self.browser.find_element_by_id('ui-id-7')
        assert element7.text == 'Section 4'
        element8 = self.browser.find_element_by_id('ui-id-8').text
        if ("Suspendisse eu nisl" in element8):
            self.browser.get_screenshot_as_file('Screenshots/Accordion/accordion_section4.png')
            assert(True)
        else:
            assert(False)

    def testStep7(self):
        # Close browser window
        self.browser.quit()
