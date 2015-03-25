__author__ = 'Brenda'

from egat.testset import SequentialTestSet
from webdriver_resource import WebDriverResource
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from egat.execution_groups import execution_group

@execution_group("test5")
class Test5(SequentialTestSet):
    def testStep1(self):
        # We can access the configuration parameters from inside any test function.
        base_url = self.configuration["base_url"]
        port = self.configuration["port"]

    @WebDriverResource.decorator
    def testStep2(self):
        # Verifying that the page is loaded and exists by checking for a specific meta content identifier
        if self.environment.get('browser', '') == "Chrome":
            self.browser = webdriver.Chrome()
        elif self.environment.get('browser', '') == "Firefox":
            self.browser = webdriver.Firefox()
        else:
            self.browser = webdriver.Firefox()
        self.browser.maximize_window()
        self.browser.get("http://www.amazon.com")
        time.sleep(5)
        if self.browser.find_element_by_link_text('Amazon'):
            assert(True)
        else:
            assert(False)

    def testStep3(self):
        # Search for and select book
        self.browser.find_element_by_id('twotabsearchtextbox').click()
        self.browser.find_element_by_id('twotabsearchtextbox').send_keys('python')
        self.browser.find_element_by_id('twotabsearchtextbox').send_keys(Keys.ENTER)
        time.sleep(5)
        self.browser.find_element_by_link_text('Learning Python, 5th Edition').click()

    def testStep4(self):
        # Adding book to cart
        self.browser.find_element_by_xpath('//*[@id="buyNewSection"]').click()
        self.browser.find_element_by_xpath('//*[@id="add-to-cart-button"]').click()

    def testStep5(self):
        # Search for second item
        self.browser.find_element_by_id('twotabsearchtextbox').click()
        self.browser.find_element_by_id('twotabsearchtextbox').send_keys('asics')
        self.browser.find_element_by_id('twotabsearchtextbox').send_keys(Keys.ARROW_DOWN,Keys.ARROW_DOWN,Keys.ARROW_DOWN,Keys.ENTER)
        if self.browser.find_element_by_link_text('Women'):
            assert(True)
        else:
            assert(False)
        if self.browser.find_element_by_link_text("ASICS Women's GEL-Noosa Tri 9 Running Shoe"):
            self.browser.find_element_by_link_text("ASICS Women's GEL-Noosa Tri 9 Running Shoe").click()
            assert(True)
        else:
            assert(False)

    def testStep6(self):
        # Verify and add item to cart
        all_spans = self.browser.find_elements_by_xpath('//*[@id="productTitle"]')
        for span in all_spans:
            if "ASICS Women's GEL-Noosa Tri 9 Running Shoe" in span.text:
                assert(True)
            else:
                assert(False)
        if self.browser.find_element_by_xpath('//*[@id="native_dropdown_selected_size_name"]'):
            self.browser.find_element_by_xpath('//*[@id="native_dropdown_selected_size_name"]').click()
            self.browser.find_element_by_css_selector('#native_size_name_6').click()
            assert(True)
        else:
            assert(False)
        self.browser.find_element_by_css_selector('#a-autoid-10-announce > div > div:nth-child(1) > img').click()
        time.sleep(15)
        self.browser.find_element_by_xpath('//*[@id="add-to-cart-button"]').click()
        checkout_span = self.browser.find_elements_by_xpath('//*[@id="confirm-text"]')
        for span in checkout_span:
            if "1 item added to Cart" in span.text:
                assert(True)
            else:
                assert(False)

    def testStep7(self):
        # Search for third item
        self.browser.find_element_by_link_text('Amazon').click()
        self.browser.find_element_by_id('twotabsearchtextbox').click()
        self.browser.find_element_by_id('twotabsearchtextbox').send_keys('fire tv stick')
        self.browser.find_element_by_id('twotabsearchtextbox').send_keys(Keys.ENTER)
        if self.browser.find_element_by_link_text('Fire TV Stick'):
            self.browser.find_element_by_link_text('Fire TV Stick').click()
            assert(True)
        else:
            assert(False)

    def testStep8(self):
        # Verify and add item to cart
        fire_span = self.browser.find_elements_by_xpath('//*[@id="btAsinTitle"]')
        for span in fire_span:
            if 'Fire TV Stick' in span.text:
                self.browser.find_element_by_css_selector('#bb_atc_button').click()
                firecheck_span = self.browser.find_elements_by_xpath('//*[@id="confirm-text"]')
                for span in firecheck_span:
                    if "1 item added to Cart" in span.text:
                        assert(True)
                    else:
                        assert(False)
            else:
                assert(False)

    def testStep9(self):
        # Verify items in cart
        self.browser.find_element_by_id('nav-cart').click()
        if self.browser.find_element_by_xpath('//*[@id="sc-active-cart"]/div/h2'):
            assert(True)
        else:
            assert(False)

    def testStep10(self):
        sub_spans = self.browser.find_elements_by_xpath('//*[id="activeCartViewForm"]/div[3]/p/span')
        for span in sub_spans:
            if 'Subtotal (3 items):' in span.text:
                assert(True)
            else:
                assert(False)

    def testStep11(self):
        if self.browser.find_element_by_css_selector('#activeCartViewForm > div.sc-list-body > div:nth-child(2) > div.sc-list-item-content > div.a-row.a-spacing-base.a-spacing-top-base > div.a-column.a-span8 > div > div > div.a-fixed-left-grid-col.a-float-left.a-col-left > div > a > img'):
            assert(True)
        else:
            assert(False)
        if self.browser.find_element_by_css_selector('#activeCartViewForm > div.sc-list-body > div:nth-child(1) > div.sc-list-item-content > div.a-row.a-spacing-base.a-spacing-top-base > div.a-column.a-span8 > div > div > div.a-fixed-left-grid-col.a-float-left.a-col-left > div > a > img'):
            assert(True)
        else:
            assert(False)
        if self.browser.find_element_by_css_selector('#activeCartViewForm > div.sc-list-body > div:nth-child(1) > div.sc-list-item-content > div.a-row.a-spacing-base.a-spacing-top-base > div.a-column.a-span8 > div > div > div.a-fixed-left-grid-col.a-float-left.a-col-left > div > a > img'):
            assert(True)
        else:
            assert(False)

    def testStep12(self):
        self.browser.find_element_by_css_selector('#activeCartViewForm > div.sc-list-body > div:nth-child(1) > div.sc-list-item-content > div.a-row.a-spacing-base.a-spacing-top-base > div.a-column.a-span8 > div > div > div.a-fixed-left-grid-col.a-col-right > div > span.a-size-small.sc-action-delete > span > input[type="submit"]').click()
        time.sleep(15)
        delete_spans = self.browser.find_elements_by_css_selector('#activeCartViewForm > div.sc-list-body > div:nth-child(1) > div.sc-list-item-removed-msg.a-padding-medium > div:nth-child(1) > span > a > span')
        for span in delete_spans:
            if 'Fire TV Stick' in span.text:
                wording_spans = self.browser.find_elements_by_xpath('//*[@id="activeCartViewForm"]/div[2]/div[1]/div[3]/div[1]/span')
                for span in wording_spans:
                    if 'was removed from Shopping Cart' in span.text:
                        assert(True)
                    else:
                        assert(False)
                assert(True)
            else:
                assert(False)

    def testStep13(self):
        subtotal_spans = self.browser.find_elements_by_xpath('//*[@id="activeCartViewForm"]/div[3]/p/span')
        for span in subtotal_spans:
            if 'Subtotal (2 items):' in span.text:
                assert(True)
            else:
                assert(False)

    def testStep14(self):
        self.browser.quit()