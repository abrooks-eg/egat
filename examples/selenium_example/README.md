This example showcases the special support the toolkit has for debugging Selenium
tests. Selenium debugging support is activated when you set a Selenium Webdriver
object named 'browser' in a TestSet class. If a test fails, the test runner will
take a screenshot of the browser and save the DOM. You can see this behavior in
action by running the selenium_debugging.py tests like so:

(from the root directory of the project)
./egatest -c examples/selenium_example/selenium_debugging.json

You will find the screenshots and DOM capture in the test results folder.