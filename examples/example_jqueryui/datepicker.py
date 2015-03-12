__author__ = 'Brenda'

from egat.testset import SequentialTestSet
from webdriver_resource import WebDriverResource
from selenium import webdriver
import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

class Test3(SequentialTestSet):
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
        # Verifying the datepicker page at starting position
        self.browser.find_element_by_link_text('Datepicker').click()
        self.browser.get_screenshot_as_file('Screenshots/Datepicker/datepicker_startingpoint.png')
        self.browser.switch_to_frame(self.browser.find_element_by_css_selector('#content > iframe'))
        self.browser.find_element_by_id('datepicker').click()
        wait = WebDriverWait(self.browser,5)
        wait.until(expected_conditions.visibility_of(self.browser.find_element_by_id("ui-datepicker-div")))
        if self.browser.find_element_by_id('ui-datepicker-div'):
            assert(True)
        else:
            assert(False)
        self.browser.get_screenshot_as_file('Screenshots/Datepicker/datepicker_calendar_display.png')

    def testStep4(self):
        # Verifying that the default date is today's date
        # Saves date element as integer
        dateelement1 = int(self.browser.find_element_by_class_name('ui-datepicker-today').text)
        print dateelement1

        # Saves today's date as integer
        dateelement2 = int(datetime.datetime.strftime(datetime.datetime.now(),'%d'))
        # Validates that default date is today's date
        print dateelement2

        if dateelement1 == dateelement2:
            assert(True)
        else:
            assert(False)
        # Verifies if the date is between the 1st and the 26th then adds 2 days
        if dateelement1 <= 26 and dateelement1 >= 1:
            print str(dateelement1) + " is <= 26 and >= 1"
            dateelement3 = dateelement2 + 2
            print dateelement3
        # if date is greater than 26th, it subtracts 2 days
        else:
            dateelement3 = dateelement2 - 2
            print str(dateelement1) + " is > 26"
            print dateelement3
        # System selects the date that is either 2 days after or 2 days before from previous if statement
        self.browser.find_element_by_link_text(str(dateelement3)).click()

    def testStep5(self):
        self.browser.get_screenshot_as_file('Screenshots/Datepicker/datepicker_new_date.png')
        # Verify that the date displayed
        input_element = self.browser.find_element_by_id('datepicker')
        date_input = (input_element.get_attribute('value'))
        # Verify month
        if (int(date_input[0:2])) == (int(datetime.datetime.strftime(datetime.datetime.now(),'%m'))):
            assert(True)
        else:
            assert(False)
        # Verify day - NOTE: day is reliant on if the day is less than or equal to 26 or greater than or equal to 1
        if (int(date_input[3:5])<=26 and int(date_input[3:5])>=1):
            if (int(date_input[3:5])) == (int(datetime.datetime.strftime(datetime.datetime.now(),'%d'))+2):
                assert(True)
            else:
                assert(False)
        elif (int(date_input[3:5])>26):
            if (int(date_input[3:5])) == (int(datetime.datetime.strftime(datetime.datetime.now(),'%d'))-2):
                assert(True)
            else:
                assert(False)
        else:
            assert(False)
        # Verify year
        if (int(date_input[6:10])) == (int(datetime.datetime.strftime(datetime.datetime.now(),'%Y'))):
            assert(True)
        else:
            assert(False)

    def testStep6(self):
        # Close web browser window
        self.browser.quit()