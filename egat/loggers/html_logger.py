import sys
import datetime
import os
import time
import cgi
import itertools
import inspect
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

    default_css = """
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
        .details {
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
        .empty-total {
            text-align: center;
        }
        .class-totals-container {
            padding: 0px !important;
            border-collapse: collapse !important;
            background-color: rgb(240, 240, 240);
        }
        .class-totals-table td {
            border-top: 0px solid black;
            border-right: 0px solid black;
            border-bottom: 0px solid black;
            border-left: 0px solid black;
            padding: 15px;
        }
        """

    @staticmethod
    def write_test_results(test_results, start_time, end_time, fp, css_path=None):
        """Takes a list of TestResult objects and an open file pointer and writes 
        the test results as HTML to the given file."""

        css_str = ""
        if css_path:
            css_str = '<link rel="stylesheet" href="%s" type="text/css">' % css_path
        else:
            css_str = '<style>%s</style>' % HTMLWriter.default_css

        title = "Test Run %s" % start_time.strftime("%m-%d-%y %H:%I %p")

        html = """
            <html>
                <head>
                    <title>%s</title>
                    %s
                    <script type="text/javascript">
                        function toggleFuncDetails(id) {
                            // check to see if we are already showing the traceback
                            var testResultRow = document.querySelector("tr[id='" + id + "-result']")
                            var detailsRow = document.querySelector("tr[id='" + id + "-details']")
                            var hiddenDetailsDiv = document.querySelector("div[id='" + id + "-hidden-details']")

                            if (detailsRow === null) {
                                // the details are hidden; show it.
                                var details = hiddenDetailsDiv.innerHTML
                                detailsRow = document.createElement('tr')
                                detailsRow.setAttribute('id', id + "-details")
                                detailsRow.innerHTML = "<td></td><td></td><td class='details' colspan='4'>" + details + "</td>"
                                testResultRow.parentNode.insertBefore(detailsRow, testResultRow.nextSibling)
                            } else {
                                // the details are already showing; hide them.
                                detailsRow.parentNode.removeChild(detailsRow)
                            }
                        }

                        function toggleClassDetails(button, id) {
                            var classRow = document.querySelector("tr[id='" + id + "-class']")
                            var rowsToHide = []

                            if (classRow.className.indexOf("collapsed") > -1) {
                                // classRow is collapsed. Expand it.
                                button.textContent = "-"
                                classRow.className = classRow.className.replace("collapsed", "")
                                var currentNode = classRow.nextElementSibling
                                while (currentNode.className == null ||
                                    currentNode.className.indexOf("class-header") == -1) {
                                    currentNode.style.display = "table-row"
                                    currentNode = currentNode.nextElementSibling
                                }
                            } else {
                                // classRow is expanded. Collapse it.
                                button.textContent = "+"
                                classRow.className = classRow.className + " collapsed"
                                var currentNode = classRow.nextElementSibling
                                while (currentNode.className == null ||
                                    currentNode.className.indexOf("class-header") == -1) {
                                    currentNode.style.display = "none"
                                    currentNode = currentNode.nextElementSibling
                                }
                            }
                        }
                    </script>
                </head>
                <body>""" % (title, css_str)

        html += """
            <div id="header-image"></div>
            <div class="header">
                <h1 id="title">%s</h1> 
                <h3>Start time: %s</h3>
                <h3>End time: %s</h3>
                <h3>Duration: %s</h3>
            </div>
        """  % (
            title,
            start_time.strftime("%m-%d-%y %H:%M:%S"),
            end_time.strftime("%m-%d-%y %H:%M:%S"),
            str(end_time - start_time).split('.', 2)[0]
        )

        results = HTMLWriter.dump_queue(test_results)

        # Calculate totals
        successes = len(filter(lambda r: r.status == TestResultType.SUCCESS, results))
        failures = len(filter(lambda r: r.status == TestResultType.FAILURE, results))
        skipped = len(filter(lambda r: r.status == TestResultType.SKIPPED, results))

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
            # find class totals
            all_results = list(itertools.chain(*tests_by_env.values()))
            successes = len(filter(lambda r: r.status == TestResultType.SUCCESS, all_results))
            failures = len(filter(lambda r: r.status == TestResultType.FAILURE, all_results))
            skipped = len(filter(lambda r: r.status == TestResultType.SKIPPED, all_results))

            # Add class header
            html += """
                <tr id="%s-class" class="class-header">
                    <td>
                        <a onclick="toggleClassDetails(this, %s)">-</a>
                    </td>
                    <td colspan="5">%s</td>
                </tr>
                <tr>
                    <td colspan="6" class="class-totals-container">
                        <table class='class-totals-table'>
                            <td>Successes:</td>
                            <td colspan="1">%d</td>
                            <td>Failures:</td>
                            <td colspan="1">%d</td>
                            <td>Skipped:</td>
                            <td colspan="1">%d</td>
                        </table>
                    </td>
                </tr>
                """ % (i, i, class_name, successes, failures, skipped)
            i += 1

            for env_str, test_results in tests_by_env.items():
                if test_results[0].environment:
                    # Add environment header
                    html += """
                        <tr class="environment-header">
                            <td></td>
                            <td colspan="5">%s</td>
                        </tr>""" % test_results[0].environment_string()

                for result in test_results:
                    # Format the traceback
                    traceback_str = ""
                    if result.traceback:
                        traceback_str = cgi.escape(result.traceback)
                        traceback_str = traceback_str.replace(' ', '&nbsp;')
                        traceback_str = traceback_str.replace('\n', '<br />')

                    # Format the resource_groups
                    def print_resource_groups(rgroup):
                        if inspect.isclass(rgroup):
                            return rgroup.__name__
                        else:
                            return str(rgroup)
                    resource_group_str = map(print_resource_groups, result.resource_groups)

                    row = """
                        <tr id="%s-result" class="test-result">
                            <td class='empty-cell'></td>
                            <td class='empty-cell'></td>
                            <td class='function-name'>%s</td>
                            <td class='%s'>%s</td>
                            <td class='thread-num'>%s</td>
                            <td class="details-btn">
                                <a onclick="toggleFuncDetails(%s)">Details</a>
                            </td>
                            <td style="display:none">
                                <div id="%s-hidden-details" class='details'>
                                    Resource Groups: %s<br/>
                                    Execution Groups: %s<br/>
                                    Start Time: %s<br />
                                    End Time: %s<br />
                                    Duration: %s<br />
                                    %s
                                </div>
                            </td>
                        </tr>
                        """ % (i, 
                               result.func.__name__, 
                               result.status, 
                               result.status, 
                               result.thread + 1, 
                               i, 
                               i, 
                               resource_group_str, 
                               result.execution_groups, 
                               result.start_time.strftime("%m-%d-%y %H:%M:%S"),
                               result.end_time.strftime("%m-%d-%y %H:%M:%S"),
                               str(result.end_time - result.start_time),
                               traceback_str)

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
    start_time = None
    end_time = None
    test_title = None
    css_path = None

    def __init__(self, log_dir=None, log_level=LogLevel.ERROR, css_path=None):
        TestLogger.__init__(self, log_dir=log_dir, log_level=log_level)
        if css_path: css_path = os.path.abspath(css_path) 
        self.css_path = css_path

    def startingTests(self):
        if not self.log_dir: self.log_dir = "."

        # Set up the log file
        self.start_time = datetime.datetime.now()
        self.log_dir = self.log_dir.rstrip('/')
        self.test_title = "Test Run %s" % self.start_time.strftime("%m-%d-%y %H:%M:%S")
        self.log_dir += "/%s" % self.test_title.replace(':', '.')
        os.mkdir(self.log_dir)
        log_name = "%s/results.html" % self.log_dir
        self.out = open(log_name, 'w')

        self.results = Queue()
        self.current_tests = {}
    
    def finishedTests(self):
        self.end_time = datetime.datetime.now()
        HTMLWriter.write_test_results(
            self.results, 
            self.start_time, 
            self.end_time, 
            self.out, 
            css_path=self.css_path
        )

    def runningTestFunction(self, instance, func, thread_num=None):
        result = TestResult(instance, func, thread=thread_num)
        result.start_time = datetime.datetime.now()
        self.current_tests[(instance, func, thread_num)] = result

    def finishedTestFunction(self, instance, func, thread_num=None, browser=None):
        result = self.current_tests.pop((instance, func, thread_num))
        result.end_time = datetime.datetime.now()
        if not result.status: result.status = TestResultType.SUCCESS
        self.results.put(result)

        if self.log_level == LogLevel.DEBUG:
            self.log_debug_info(instance, func)

    def skippingTestFunction(self, instance, func, thread_num=None):
        result = TestResult(instance, func, status=TestResultType.SKIPPED, thread=thread_num)
        result.start_time = datetime.datetime.now()
        result.end_time = datetime.datetime.now()
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

