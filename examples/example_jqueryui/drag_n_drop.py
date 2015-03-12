__author__ = 'Brenda'

from egat.testset import SequentialTestSet
from webdriver_resource import WebDriverResource
from selenium import webdriver
from selenium.webdriver.common import action_chains

class Test1(SequentialTestSet):
    def testStep1(self):
        # We can access the configuration parameters from inside any test function.
        base_url = self.configuration["base_url"]
        port = self.configuration["port"]

    @WebDriverResource.decorator
    def testStep2(self):
        # Verifying that the page is loaded and exists by checking for a specific meta content identifier
        self.browser = webdriver.Firefox()
        self.browser.get("http://jqueryui.com")
        self.browser.save_screenshot('Screenshots\jqueryui_page.png')
        if self.browser.find_element_by_css_selector("meta[name='author']"):
            self.browser.get_screenshot_as_file('Screenshots/Drag_n_drop/jqueryui_startingpoint.png')
            assert(True)
        else:
            assert(False)

    def testStep3(self):
        # Navigate to new page and verify page by class name
        self.browser.find_element_by_link_text("Droppable").click()
        self.browser.get_screenshot_as_file('Screenshots/Drag_n_drop/droppable_pagedisplayed.png')
        if self.browser.find_element_by_class_name("entry-title"):
            assert(True)
        else:
            assert(False)

    def testStep4(self):
        # Dragging and dropping a page element
        self.browser.switch_to_frame(self.browser.find_element_by_tag_name("iframe"))
        element = self.browser.find_element_by_id("draggable")
        target = self.browser.find_element_by_id("droppable")
        action_chains.ActionChains(self.browser).drag_and_drop(element,target).perform()
        self.browser.get_screenshot_as_file('Screenshots/Drag_n_drop/dropped_effect.png')

    def testStep5(self):
        # Verifying that Droppable is changed to Dropped after teststep4 is completed
        element = self.browser.find_element_by_id('droppable')
        assert element.text == 'Dropped!'
        self.browser.get_screenshot_as_file('Screenshots/Drag_n_drop/dropped_icon.png')

    def testStep6(self):
        # Close browser at end of test
        self.browser.quit()



