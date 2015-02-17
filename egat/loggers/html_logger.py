import sys
import datetime
import os
import time
import cgi
from egat.loggers.test_logger import TestLogger
from egat.loggers.test_logger import LogLevel
from egat.test_result import TestResult
from itertools import groupby
from Queue import Queue
from Queue import Empty

class TestResultType():
    SUCCESS = "success"
    FAILURE = "failure"
    SKIPPED = "skipped"


class HTMLWriter():
    @staticmethod
    def write_test_results(test_results, title, fp):
        """Takes a list of TestResult objects and an open file pointer and writes 
        the test results as HTML to the given file."""

        html = ""

        html += """
            <html>
                <head>
                    <title>%s</title>
                    <style>
                           body {
                                  font-family: "Verdana";
                                  font-size: 12pt;
                              }
                              .results-table {
                                  border-collapse: collapse;
                              }
                              .results-table th {
                                  border: 1px solid black;
                                  padding: 15px;
                                  background-color: rgb(240, 240, 240);
                                  font-weight: 300;
                                  font-size: 14pt;
                              }
                              .results-table tr {
                                  border: 1px solid black;
                              }
                              .results-table td {
                                  border: 1px solid black;
                                  padding: 15px;
                              }
                              .class-header {
                                  background-color: rgb(240, 240, 240);
                                  font-family: "Verdana";
                                  font-size: 14pt;
                              }
                              .environment-header {
                                  background-color: rgb(240, 240, 240);
                                  font-family: "Verdana";
                                  font-size: 14pt;
                              }
                              .function-name {
                                  font-family: "Andale Mono";
                                  width: 700px;
                              }
                              .thread-num {
                                  text-align: center;
                              }
                              .details-btn {
                                  text-decoration: underline;
                                  text-align: center;
                                  background-color: rgb(240, 240, 240);
                                  cursor: pointer;
                              }
                              .traceback {
                                  font-family: "Andale Mono";
                                  font-size: 10pt;
                                  width: 700px;
                              }
                              .success {
                                  color: #276943;
                                  border-color: #276943;
                                  background-color: #95d7b2;
                                  text-align: center;
                              }
                              .failure {
                                  color: #671a10;
                                  border-color: #671a10;
                                  background-color: #e87a6a;
                                  text-align: center;
                              }
                              .skipped {
                                  color: #716d06;
                                  border-color: #716d06;
                                  background-color: #FFF692;
                                  text-align: center;
                              }
                              .totals {
                                  text-align: left;
                              }
                    </style>
                    <script type="text/javascript">
                        function toggleDetails(id) {
                            // check to see if we are already showing the traceback
                            testResultRow = document.querySelector("tr[id='" + id + "-result']")
                            tracebackRow = document.querySelector("tr[id='" + id + "-traceback']")
                            hiddenTracebackDiv = document.querySelector("div[id='" + id + "-hidden-traceback']")

                            if (tracebackRow === null) {
                                // the traceback is hidden; show it.
                                traceback = hiddenTracebackDiv.innerHTML
                                tracebackRow = document.createElement('tr')
                                tracebackRow.setAttribute('id', id + "-traceback")
                                tracebackRow.innerHTML = "<td></td><td class='traceback' colspan='4'>" + traceback + "</td>"
                                testResultRow.parentNode.insertBefore(tracebackRow, testResultRow.nextSibling)
                            } else {
                                // the traceback is already showing; hide it.
                                tracebackRow.parentNode.removeChild(tracebackRow)
                            }
                        }
                    </script>
                </head>
                <body>
                    <h1>%s</h1> """ % (title, title)


        results = HTMLWriter.dump_queue(test_results)

        # Calculate totals
        successes = 0
        failures = 0
        skipped = 0
        for result in results:
            if result.status == TestResultType.SUCCESS:
                successes += 1
            if result.status == TestResultType.FAILURE:
                failures += 1
            if result.status == TestResultType.SKIPPED:
                skipped += 1

        # Add totals row
        html += """
            <table class='results-table'>
                <td>Successes</td>
                <td class="success" colspan="1">%d</td>
                <td>Failures</td>
                <td class="failure" colspan="1">%d</td>
                <td>Skipped</td>
                <td class="skipped" colspan="1">%d</td>
            </table>
            <br />""" % (successes, failures, skipped)

        # Group tests by class and environment
        tests_by_class = {}
        for result in results:
            tests_by_env = tests_by_class.get(result.full_class_name(), {})
            env_str = HTMLWriter.hashable(result.environment)
            results = tests_by_env.get(env_str, []) 
            results.append(result)
            tests_by_env[env_str] = results
            tests_by_class[result.full_class_name()] = tests_by_env

        html += "<table class='results-table'>"

        # Add table headings
        html += """
            <tr>
                <th></th>
                <th></th>
                <th>Function</th>
                <th>Status</th>
                <th>Thread</th>
                <th>Details</th>
            </tr>"""

        i = 0
        for class_name, tests_by_env in tests_by_class.items():
            # Add class header
            html += """
                <tr class="class-header">
                    <td colspan="6">%s</td>
                </tr>""" % (class_name)

            for env_str, test_results in tests_by_env.items():
                # Add environment header
                html += """
                    <tr class="environment-header">
                        <td></td>
                        <td colspan="5">%s</td>
                    </tr>""" % test_results[0].environment_string()

                for result in test_results:
                    if result.traceback:
                        result.traceback = cgi.escape(result.traceback)
                        result.traceback = result.traceback.replace(' ', '&nbsp;')
                        result.traceback = result.traceback.replace('\n', '<br />')
                    row = """
                        <tr id="%s-result" class="test-result">
                            <td class='empty-cell'></td>
                            <td class='empty-cell'></td>
                            <td class='function-name'>%s</td>
                            <td class='%s'>%s</td>
                            <td class='thread-num'>%s</td>
                            <td class="details-btn">
                                <a onclick="toggleDetails(%s)">Details</a>
                            </td>
                            <td style="display:none">
                                <div id="%s-hidden-traceback" class='traceback'>%s</div
                            </td>
                        </tr>
                        """ % (i, result.func.__name__, result.status, result.status, result.thread, i, i, result.traceback)

                    html += row
                    i += 1

        html += "</table></body></html>"

        fp.write(html)

    @staticmethod
    def dump_queue(queue):
        """
        Empties all pending items in a queue and returns them in a list.
        """
        result = []

        try:
            while True:
                item = queue.get_nowait()
                result.append(item)
        except: Empty

        return result

    @staticmethod
    def hashable(d):
        """Takes a dictionary and returns a hashable string representing it."""
        return "%^&*|".join(map(str, d.keys() + d.values()))

class HTMLLogger(TestLogger):
    """A logger that writes test output to an interactive HTML page."""
    out = None
    results = None
    current_tests = None
    test_title = None

    def startingTests(self):
        if not self.log_dir: self.log_dir = "."

        # Set up the log file
        start_time = datetime.datetime.now().strftime("%m-%d-%y %H:%M:%S")
        self.log_dir = self.log_dir.rstrip('/')
        self.test_title = "Test Run %s" % start_time
        self.log_dir += "/%s" % self.test_title.replace(':', '.')
        os.mkdir(self.log_dir)
        log_name = "%s/results.html" % self.log_dir
        self.out = open(log_name, 'w')

        self.results = Queue()
        self.current_tests = {}
    
    def finishedTests(self):
        HTMLWriter.write_test_results(self.results, self.test_title, self.out)

    def runningTestFunction(self, instance, func, thread_num=None):
        result = TestResult(instance, func, thread=thread_num)
        self.current_tests[(instance, func, thread_num)] = result

    def finishedTestFunction(self, instance, func, thread_num=None, browser=None):
        result = self.current_tests.pop((instance, func, thread_num))
        if not result.status: result.status = TestResultType.SUCCESS
        self.results.put(result)

        if self.log_level == LogLevel.DEBUG:
            self.log_debug_info(instance, func)

    def skippingTestFunction(self, instance, func, thread_num=None):
        result = TestResult(instance, func, status=TestResultType.SKIPPED, thread=thread_num)
        self.results.put(result)

    def foundException(self, instance, func, e, tb, thread_num=None, browser=None):
        result = self.current_tests[(instance, func, thread_num)]
        result.status = TestResultType.FAILURE
        result.error = e
        result.traceback = tb

        if self.log_level == LogLevel.ERROR:
            self.log_debug_info(instance, func)

    def log_debug_info(self, classname, func):
        """Takes a class instance and a function object. If the class has an 
        attribute called 'browser' this method will take a screenshot of the browser 
        window and save the page source to the log_dir."""
        browser = getattr(instance, 'browser', None)
        if browser:
            func_str = HTMLLogger.format_function_name(classname, func)
            path = self.log_dir if self.log_dir else "."
            browser.save_screenshot('%s/%s.png' % (path, func_str))
            with open('%s/%s.html' % (path, func_str), 'a') as f:
                f.write(browser.page_source.encode('utf8'))

