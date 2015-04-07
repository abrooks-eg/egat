This example showcases the special support the toolkit has for debugging Selenium
tests. Selenium debugging support is activated when you set a Selenium Webdriver
object named 'browser' in a TestSet class. If a test fails, the test runner will
take a screenshot of the browser and save the DOM. You can see this behavior in
action by running the selenium_debugging.py tests like so:

(from the root directory of the project)
./egatest examples.selenium_example