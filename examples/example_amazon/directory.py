__author__ = 'Brenda'

from egat.testset import SequentialTestSet
from webdriver_resource import WebDriverResource
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from egat.execution_groups import execution_group

@execution_group("test6")
class Test6(SequentialTestSet):
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
        # Verify that the appropriate window is displayed
        if self.browser.find_element_by_link_text('Amazon'):
            assert(True)
        else:
            assert(False)

    def testStep3(self):
        # Verifies user is not signed in
        all_spans = self.browser.find_elements_by_xpath('//*[@id="nav-signin-text"]')
        for span in all_spans:
            if "Sign in" in span.text:
                span.send_keys(Keys.ALT,Keys.ARROW_LEFT)
                assert(True)
            else:
                assert(False)
                self.browser.quit()

    def testStep4(self):
        # Navigate to the directory and verify directory title
        (webdriver.ActionChains(self.browser)).double_click(self.browser.find_element_by_id('nav-link-shopall')).perform()
        directory = self.browser.find_element_by_id("siteDirectoryHeading").text
        if "EARTH'S BIGGEST SELECTION" in directory:
            assert(True)
        else:
            assert(False)

    def testStep5(self):
        # Verify section title is displayed
        for span in self.browser.find_elements_by_xpath('//*[@id="shopAllLinks"]/tbody/tr/td[1]/div[1]/h2'):
            if 'Unlimited Instant Videos' in span.text:
                assert(True)
            else:
                assert(False)

    def testStep6(self):
        # Verify section title is displayed
        for span in self.browser.find_elements_by_xpath('//*[@id="shopAllLinks"]/tbody/tr/td[1]/div[2]/h2'):
            if 'Digital & Prime Music' in span.text:
                assert(True)
            else:
                assert(False)

    def testStep7(self):
        # Verify section title is displayed
        for span in self.browser.find_elements_by_xpath('//*[@id="shopAllLinks"]/tbody/tr/td[1]/div[3]/h2'):
            if 'Appstore for Android' in span.text:
                assert(True)
            else:
                assert(False)

    def testStep8(self):
        # Verify section title is displayed
        for span in self.browser.find_elements_by_xpath('//*[@id="shopAllLinks"]/tbody/tr/td[1]/div[4]/h2'):
            if 'Amazon Cloud Drive' in span.text:
                assert(True)
            else:
                assert(False)

    def testStep9(self):
        # Verify section title is displayed
        for span in self.browser.find_elements_by_xpath('//*[@id="shopAllLinks"]/tbody/tr/td[1]/div[5]/h2'):
            if 'Kindle E-readers & Books' in span.text:
                assert(True)
            else:
                assert(False)

    def testStep10(self):
        # Verify section title is displayed
        for span in self.browser.find_elements_by_xpath('//*[@id="shopAllLinks"]/tbody/tr/td[1]/div[6]/h2'):
            if 'Fire Tablets' in span.text:
                assert(True)
            else:
                assert(False)

    def testStep11(self):
        # Verify section title is displayed
        for span in self.browser.find_elements_by_xpath('//*[@id="shopAllLinks"]/tbody/tr/td[2]/div[1]/h2'):
            if 'Fire TV' in span.text:
                assert(True)
            else:
                assert(False)

    def testStep12(self):
        # Verify section title is displayed
        for span in self.browser.find_elements_by_xpath('//*[@id="shopAllLinks"]/tbody/tr/td[2]/div[2]/h2'):
            if 'Fire Phone' in span.text:
                assert(True)
            else:
                assert(False)

    def testStep13(self):
        # Verify section title is displayed
        for span in self.browser.find_elements_by_xpath('//*[@id="shopAllLinks"]/tbody/tr/td[2]/div[3]/h2'):
            if 'Books & Audible' in span.text:
                assert(True)
            else:
                assert(False)

    def testStep14(self):
        # Verify section title is displayed
        for span in self.browser.find_elements_by_xpath('//*[@id="shopAllLinks"]/tbody/tr/td[2]/div[4]/h2'):
            if 'Movies, Music & Games' in span.text:
                assert(True)
            else:
                assert(False)

    def testStep15(self):
        # Verify section title is displayed
        for span in self.browser.find_elements_by_xpath('//*[@id="shopAllLinks"]/tbody/tr/td[2]/div[5]/h2'):
            if 'Electronics & Computers' in span.text:
                assert(True)
            else:
                assert(False)

    def testStep16(self):
        # Verify section title is displayed
        for span in self.browser.find_elements_by_xpath('//*[@id="shopAllLinks"]/tbody/tr/td[3]/div[1]/h2'):
            if 'Home, Garden & Tools' in span.text:
                assert(True)
            else:
                assert(False)

    def testStep17(self):
        # Verify section title is displayed
        for span in self.browser.find_elements_by_xpath('//*[@id="shopAllLinks"]/tbody/tr/td[3]/div[2]/h2'):
            if 'Beauty, Health & Grocery' in span.text:
                assert(True)
            else:
                assert(False)

    def testStep18(self):
        # Verify section title is displayed
        for span in self.browser.find_elements_by_xpath('//*[@id="shopAllLinks"]/tbody/tr/td[3]/div[3]/h2'):
            if 'Toys, Kids & Baby' in span.text:
                assert(True)
            else:
                assert(False)

    def testStep19(self):
        # Verify section title is displayed
        for span in self.browser.find_elements_by_xpath('//*[@id="shopAllLinks"]/tbody/tr/td[3]/div[4]/h2'):
            if 'Clothing, Shoes & Jewelry' in span.text:
                assert(True)
            else:
                assert(False)

    def testStep20(self):
        # Verify section title is displayed
        for span in self.browser.find_elements_by_xpath('//*[@id="shopAllLinks"]/tbody/tr/td[4]/div[1]/h2'):
            if 'Sports & Outdoors' in span.text:
                assert(True)
            else:
                assert(False)

    def testStep21(self):
        # Verify section title is displayed
        for span in self.browser.find_elements_by_xpath('//*[@id="shopAllLinks"]/tbody/tr/td[4]/div[2]/h2'):
            if 'Automotive & Industrial' in span.text:
                assert(True)
            else:
                assert(False)

    def testStep22(self):
        # Verify section title is displayed
        for span in self.browser.find_elements_by_xpath('//*[@id="shopAllLinks"]/tbody/tr/td[4]/div[3]/h2'):
            if 'Credit & Payment Products' in span.text:
                assert(True)
            else:
                assert(False)

    def testStep23(self):
        # Verify shortcut links
        shortcut_span = self.browser.find_elements_by_css_selector('#shortcutLinks')
        for span in shortcut_span:
            if 'Bargains:' in span.text:
                assert(True)
            else:
                assert(False)
            if 'Gifts & Lists:' in span.text:
                assert(True)
            else:
                assert(False)
            if 'Amazon Exclusives:' in span.text:
                assert(True)
            else:
                assert(False)
            if 'Amazon Private Label Brands:' in span.text:
                assert(True)
            else:
                assert(False)
            if 'Sell With Amazon:' in span.text:
                assert(True)
            else:
                assert(False)
            if 'Buy With Amazon:' in span.text:
                assert(True)
            else:
                assert(False)
            if 'For Developers:' in span.text:
                assert(True)
            else:
                assert(False)
            if 'Amazon Mobile Shopping Apps:' in span.text:
                assert(True)
            else:
                assert(False)

    def testStep24(self):
        # Verify sections within a segment in the directory
        android_span = self.browser.find_elements_by_css_selector('#shopAllLinks')
        for span in android_span:
            if 'Appstore for Android' in span.text:
                android_items = self.browser.find_elements_by_css_selector('#shopAllLinks')
                for span in android_items:
                    if 'Apps' in span.text:
                        assert(True)
                    else:
                        assert(False)
                    if 'Games' in span.text:
                        assert(True)
                    else:
                        assert(False)
                    if 'Free App of the Day' in span.text:
                        assert(True)
                    else:
                        assert(False)
                    if 'Amazon Coins' in span.text:
                        assert(True)
                    else:
                        assert(False)
                    if 'Download Amazon Appstore' in span.text:
                        assert(True)
                    else:
                        assert(False)
                    if 'Amazon Apps' in span.text:
                        assert(True)
                    else:
                        assert(False)
                    if 'Your Apps and Devices' in span.text:
                        assert(True)
                    else:
                        assert(False)
            else:
                assert(False)

    def testStep25(self):
        # Verify a link displays as expected
        self.browser.find_element_by_link_text('Free App of the Day').click()
        freeapp_text = self.browser.find_element_by_tag_name('h1').text
        if 'Amazon Appstore for Android' in freeapp_text:
            assert(True)
        else:
            assert(False)
        self.browser.find_element_by_class_name('pageBanner').send_keys(Keys.ALT,Keys.ARROW_LEFT)

    def testStep26(self):
        # Verify shortcut links
        shortcut_span = self.browser.find_elements_by_css_selector('#shortcutLinks')
        for span in shortcut_span:
            if 'Amazon Private Label Brands:' in span.text:
                if self.browser.find_element_by_link_text('AmazonBasics Electronics and Accessories'):
                    assert(True)
                else:
                    assert(False)
                if self.browser.find_element_by_link_text('Pinzon Bedding and Bath'):
                    assert(True)
                else:
                    assert(False)
                if self.browser.find_element_by_link_text('Strathwood Outdoor Furniture and Living'):
                    assert(True)
                else:
                    assert(False)
                if self.browser.find_element_by_link_text('Amazon Gear Shop'):
                    assert(True)
                else:
                    assert(False)
            else:
                assert(False)

    def testStep27(self):
        # Verify a link within the shortcut links
        shortcut_span = self.browser.find_elements_by_css_selector('#shortcutLinks')
        for span in shortcut_span:
            if 'Bargains:' in span.text:
                self.browser.find_element_by_link_text('Outlet').click()
                outlet_span = self.browser.find_elements_by_class_name('pageBanner')
                for span in outlet_span:
                    if 'Online shopping for outlet deals' in span.text:
                        assert(True)
                    else:
                        assert(False)
            else:
                assert(False)
        self.browser.find_element_by_class_name('pageBanner').send_keys(Keys.ALT,Keys.ARROW_LEFT)

    def testStep28(self):
        # Verify that browsing history inspirations are displayed
        recommend_span = self.browser.find_elements_by_class_name('rhfUpsellColumnTitle')
        for span in recommend_span:
            if 'Inspired by your browsing history' in span.text:
                assert(True)
            else:
                assert(False)

    def testStep29(self):
        # Tear down step
        self.browser.quit()