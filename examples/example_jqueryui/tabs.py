__author__ = 'Brenda'

from egat.testset import SequentialTestSet
from webdriver_resource import WebDriverResource
from selenium import webdriver

class Test8(SequentialTestSet):
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
        # Verifying the tabs page at starting position
        self.browser.find_element_by_link_text('Tabs').click()
        self.browser.get_screenshot_as_file('Screenshots/Tabs/tabs_pagedisplayed.png')
        self.browser.switch_to_frame(self.browser.find_element_by_css_selector('#content > iframe'))
        if self.browser.find_element_by_id('tabs'):
            assert(True)
        else:
            assert(False)

    def testStep4(self):
        # Verifying the first tab
        if self.browser.find_element_by_link_text('Nunc tincidunt'):
            assert(True)
        else:
            assert(False)

    def testStep5(self):
        # Verifying that when first tab is displayed the associated text is displayed
        self.browser.get_screenshot_as_file('Screenshots/Tabs/tabs_tab1.png')
        if "false" in self.browser.find_element_by_id('tabs-1').get_attribute('aria-hidden'):
            assert(True)
        else:
            assert(False)
        element1 = self.browser.find_element_by_id('tabs-1').text
        if "Proin elit arcu" in element1:
            assert(True)
        else:
            assert(False)

    def testStep6(self):
        # Verifying that when second tab is displayed the associated text is displayed
        self.browser.find_element_by_link_text('Proin dolor').click()
        self.browser.get_screenshot_as_file('Screenshots/Tabs/tabs_tab2.png')
        if 'false' in self.browser.find_element_by_id('tabs-2').get_attribute('aria-hidden'):
            assert(True)
        else:
            assert(False)
        element2 = self.browser.find_element_by_id('tabs-2').text
        if "Morbi tincidunt" in element2:
            assert(True)
        else:
            assert(False)

    def testStep7(self):
        # Verifying that when third tab is displayed the associated text is displayed
        self.browser.find_element_by_link_text('Aenean lacinia').click()
        self.browser.get_screenshot_as_file('Screenshots/Tabs/tabs_tab3.png')
        if 'false' in self.browser.find_element_by_id('tabs-3').get_attribute('aria-hidden'):
            assert(True)
        else:
            assert(False)
        element3 = self.browser.find_element_by_id('tabs-3').text
        if "Mauris eleifend est et turpis" in element3:
            assert(True)
        else:
            assert(False)

    def testStep8(self):
        self.browser.quit()