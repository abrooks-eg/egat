__author__ = 'Brenda'

from egat.testset import SequentialTestSet
from webdriver_resource import WebDriverResource
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from egat.execution_groups import execution_group
from selenium.webdriver.common.action_chains import ActionChains


@execution_group("test7")
class Test7(SequentialTestSet):
    def testStep1(self):
        # We can access the configuration parameters from inside any test function.
        base_url = self.configuration["base_url"]
        port = self.configuration["port"]

    @WebDriverResource.decorator
    def testStep2(self):
        # Test setup step
        if self.environment.get('browser', '') == "Chrome":
            self.browser = webdriver.Chrome()
        elif self.environment.get('browser', '') == "Firefox":
            self.browser = webdriver.Firefox()
        else:
            self.browser = webdriver.Firefox()
        self.browser.maximize_window()
        self.browser.get("http://www.amazon.com")
        time.sleep(5)
        # Veirfy that the page is displayed as expected
        if self.browser.find_element_by_link_text('Amazon'):
            assert(True)
        else:
            assert(False)

    def testStep3(self):
        # Verify that user is not signed into the system
        all_spans = self.browser.find_elements_by_xpath('//*[@id="nav-signin-text"]')
        for span in all_spans:
            if "Sign in" in span.text:
                span.send_keys(Keys.ALT,Keys.ARROW_LEFT)
                assert(True)
            else:
                assert(False)
                self.browser.quit()

    def testStep4(self):
        # Navigate to the directory and verify text is displayed
        variable = self.browser.find_element_by_id('nav-link-shopall')
        actions = ActionChains(self.browser)
        actions.move_to_element(variable)
        actions.double_click(variable)
        actions.perform()
        directory = self.browser.find_element_by_id("siteDirectoryHeading").text
        if "EARTH'S BIGGEST SELECTION" in directory:
            assert(True)
        else:
            assert(False)

    def testStep5(self):
        # Navigate to Trade in Your Electronics
        for span in self.browser.find_elements_by_xpath('//*[@id="shopAllLinks"]/tbody/tr/td[2]/div[5]/h2'):
            self.browser.find_element_by_link_text('Trade In Your Electronics').click()
            for span in self.browser.find_elements_by_class_name('tradein-search-widget-heading'):
                if "Find the Items You'd Like to Trade In" in span.text:
                    self.browser.get_screenshot_as_file('Screenshots/trade_in.png')
                    assert(True)
                else:
                    assert(False)

    def testStep6(self):
        # Navigate to Laptops page
        self.browser.find_element_by_xpath('//*[@id="center"]/div[5]/div[1]/div[3]/div/a').click()
        for span in self.browser.find_elements_by_xpath('//*[@id="ref_541966"]/li[5]/a/span[1]'):
            if 'Laptops' in span.text:
                span.click()
                assert(True)
                for span in self.browser.find_elements_by_xpath('//*[@id="s-result-count"]/span/span'):
                    time.sleep(10)
                    self.browser.get_screenshot_as_file('Screenshots/laptops.png')
                    if 'Laptops' in span.text:
                        assert(True)
                    else:
                        assert(False)
            else:
                assert(False)

    def testStep7(self):
        # Navigate to the Top Brands page
        self.browser.find_element_by_xpath('//*[@id="ref_562215011"]/li[10]/a').click()
        self.browser.get_screenshot_as_file('Screenshots/expand_make.png')
        time.sleep(5)
        for span in self.browser.find_elements_by_xpath('//*[@id="ref_2528832011"]/li[8]/a/span'):
            if 'See more' in span.text:
                span.click()
                for span in self.browser.find_elements_by_xpath('//*[@id="breadCrumb"]'):
                    self.browser.get_screenshot_as_file('Screenshots/top_brands.png')
                    time.sleep(5)
                    if 'Top Brands' in span.text:
                        assert(True)
                    else:
                        assert(False)
                assert(True)
            else:
                assert(False)

    def testStep8(self):
        # Select Toshiba and verify that Toshiba is displayed
        for span in self.browser.find_elements_by_xpath('//*[@id="ref_2528832011"]/ul[3]/li[5]/a/span[1]'):
            if 'Toshiba' in span.text:
                assert(True)
                span.click()
                self.browser.get_screenshot_as_file('Screenshots/toshiba.png')
                for span in self.browser.find_elements_by_xpath('//*[@id="s-result-count"]/span/span'):
                    if 'Toshiba' in span.text:
                        assert(True)
                    else:
                        assert(False)
            else:
                assert(False)

        time.sleep(10)

    def testStep9(self):
        # Tear down step
        self.browser.quit()