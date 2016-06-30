import sys
import datetime
import os
import time
import cgi
import itertools
import inspect
import shutil
from egat.loggers.test_logger import TestLogger
from egat.loggers.test_logger import LogLevel
from egat.loggers.test_logger import LogScreen
from egat.test_result import TestResult
from egat.test_runner_helpers import TestFunctionType
from itertools import groupby
from Queue import Queue
from Queue import Empty
from pkg_resources import Requirement, resource_filename, DistributionNotFound
from multiprocessing import Lock
from collections import OrderedDict

class TestResultType():
    SUCCESS = "success"
    FAILURE = "failure"
    SKIPPED = "skipped"


class HTMLWriter():

    @staticmethod
    def copy_resources_to_log_dir(log_dir):
        """Copies the necessary static assets to the log_dir and returns the path 
        of the main css file."""
        css_path = resource_filename(Requirement.parse("egat"), "/egat/data/default.css")
        header_path = resource_filename(Requirement.parse("egat"), "/egat/data/egat_header.png")
        shutil.copyfile(css_path, log_dir + "/style.css")
        shutil.copyfile(header_path, log_dir + "/egat_header.png")

        return log_dir + os.sep + "style.css"

    @staticmethod
    def write_test_results(test_results, start_time, end_time, fp, css_path):
        """Takes a list of TestResult objects and an open file pointer and writes 
        the test results as HTML to the given file."""

        css_str = '<link rel="stylesheet" href="%s" type="text/css">' % css_path
        title = "Test Run %s" % start_time.strftime("%m-%d-%y %H:%I %p")

        #AB - added expand trace link and corresponding function
        html = """
            <!DOCTYPE html>
            <html lang="en">
                <head>
                    <meta charset="utf-8"/>
                    <title>%s</title>
                    %s
                    <script type="text/javascript">
                        function toggleFuncDetails(id) {
                            // check to see if we are already showing the traceback
                            var testResultRow = document.querySelector("tr[id='" + id + "-result']")
                            var detailsRow = document.querySelector("tr[id='" + id + "-details']")
                            var traceRow = document.querySelector("tr[id='" + id + "-trace']")
                            var hiddenDetailsDiv = document.querySelector("div[id='" + id + "-hidden-details']")
                            var hiddenSSDiv = document.querySelector("div[id='" + id + "-hidden-ss']")
                            var hiddenTraceDiv = document.querySelector("div[id='" + id + "-hidden-trace']")

                            if (detailsRow === null) {
                                // the details are hidden; show it.
                                var details = hiddenDetailsDiv.innerHTML
                                var ss = hiddenSSDiv.innerHTML
                                detailsRow = document.createElement('tr')
                                detailsRow.setAttribute('id', id + "-details")
                                if (hiddenTraceDiv.innerHTML.trim() == "")
                                {
                                    detailsRow.innerHTML = "<td></td><td></td><td class='details'>" + details + "<br></td><td colspan='3'>" + ss + "</td>"
                                }
                                else
                                {
                                    detailsRow.innerHTML = "<td></td><td></td><td class='details'>" + details + "<br><a onclick='toggleFuncTrace(" + id + ")'>-Trace-</a><br></td><td colspan='3'>" + ss + "</td>"
                                }
                                testResultRow.parentNode.insertBefore(detailsRow, testResultRow.nextSibling)
                            } else {
                                // the details are already showing; hide them.
                                detailsRow.parentNode.removeChild(detailsRow)
                                
                                // also hide trace if visible
                                if (traceRow !== null) {
                                    traceRow.parentNode.removeChild(traceRow)
                                }
                            }
                        }
                        
                        function toggleFuncTrace(id) {
                            // check to see if we are already showing the traceback
                            var detailsRow = document.querySelector("tr[id='" + id + "-details']")
                            var traceRow = document.querySelector("tr[id='" + id + "-trace']")
                            var hiddenTraceDiv = document.querySelector("div[id='" + id + "-hidden-trace']")

                            if (traceRow === null) {
                                // the trace is hidden; show it.
                                var trace = hiddenTraceDiv.innerHTML
                                traceRow = document.createElement('tr')
                                traceRow.setAttribute('id', id + "-trace")
                                traceRow.innerHTML = "<td></td><td></td><td class='details' colspan='4'>" + trace + "</td>"
                                detailsRow.parentNode.insertBefore(traceRow, detailsRow.nextSibling)
                            } else {
                                // the details are already showing; hide them.
                                traceRow.parentNode.removeChild(traceRow)
                            }
                        }

                        function toggleClassDetails(button, id) {
                            var classRow = document.querySelector("tr[id='" + id + "-class']")
                            var rowsToHide = []

                            if (classRow.className.indexOf("collapsed") > -1) {
                                // classRow is collapsed. Expand it.
                                button.textContent = "[-]"
                                classRow.className = classRow.className.replace("collapsed", "")
                                var currentNode = classRow.nextElementSibling
                                while (currentNode.className == null ||
                                    currentNode.className.indexOf("class-header") == -1) {
                                    currentNode.style.display = "table-row"
                                    currentNode = currentNode.nextElementSibling
                                }
                            } else {
                                // classRow is expanded. Collapse it.
                                button.textContent = "[+]"
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
            <div id="header-image">
                <img src="egat_header.png"/>
            </div>
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
            <table class='totals-table'>
                <td>Successes</td>
                <td class="success" colspan="1">%d</td>
                <td>Failures</td>
                <td class="failure" colspan="1">%d</td>
                <td>Skipped</td>
                <td class="skipped" colspan="1">%d</td>
            </table>
            <br />""" % (successes, failures, skipped)

        # Group tests by class and environment
        
        #AB - changed to ordered collection for properly ordered output
        #tests_by_class = {}
        tests_by_class = OrderedDict({})
        tests_by_env = OrderedDict({})
        for result in results:
            #AB - added variable for extra sorting by run group
            rungroup = 0
            if('group' in result.configuration.keys()):
                rungroup = result.configuration["group"]
            
            #AB - added if clause for extra sorting by run group
            if(rungroup != 0):
                tests_by_env = tests_by_class.get(result.full_class_name_with_group(), {})
            else:
                tests_by_env = tests_by_class.get(result.full_class_name(), {})
            
            env_str = HTMLWriter.hashable(result.environment)
            results = tests_by_env.get(env_str, []) 
            results.append(result)
            tests_by_env[env_str] = results
            
            #AB - added if clause for extra sorting by run group
            if(rungroup != 0):
                tests_by_class[result.full_class_name_with_group()] = tests_by_env
            else:
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

            row_classes = "class-header collapsed"
            if failures > 0:
                row_classes += " failure"
            elif skipped > 0:
                row_classes += " skipped"

            # Add class header
            html += """
                <tr id="%s-class" class="%s">
                    <td class="expand-collapse-btn">
                        <a onclick="toggleClassDetails(this, %s)">[+]</a>
                    </td>
                    <td colspan="5">
                        <span style="float:left;">
                            %s                        
                        </span>
                        <span style="float:right;">
                            Successes:
                            %d
                            Failures:
                            %d
                            Skipped:
                            %d
                        </span>
                    </td>
                </tr>
                """ % (i, row_classes, i, class_name, successes, failures, skipped)
            i += 1

            for env_str, test_results in tests_by_env.items():
                if test_results[0].environment:
                    # Add environment header
                    html += """
                        <tr class="environment-header" style="display:none;">
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
                        
                    # Format the details
                    details_str = ""
                    if result.details:
                        details_str = cgi.escape(result.details)
                        details_str = details_str.replace(' ', '&nbsp;')
                        details_str = details_str.replace('\n', '<br />')
                        
                    # Check for screenshot
                    ss_link = ""
                    if result.ss_loc:
                        ss_link = ss_link = '<a href="./' + result.ss_loc + '" target="_blank"><img src="./' + result.ss_loc + '" width="300"></a>'
                        
                    #func_str = class_name + "." + result.func.__name__
                    # remove group prefix if present
                    #if(func_str.count(".") > 2):
                    #    intStart = func_str.find(".") + 1
                    #    func_str = func_str[intStart:]
                    
                    #import os.path
                    #if(os.path.isfile(os.path.dirname(fp.name) + "/" + func_str + ".png")):
                    #    ss_link = '<a href="./' + func_str + '.png" target="_blank"><img src="./' + func_str + '.png" width="300"></a>'

                    # Format the resource_groups
                    def print_resource_groups(rgroup):
                        if inspect.isclass(rgroup):
                            return rgroup.__name__
                        else:
                            return str(rgroup)
                    resource_group_str = map(print_resource_groups, result.resource_groups)

                    #AB - Clean up output: removing Resource, Execution groups. add space before error
                    #Resource Groups: %s<br/>
                    #Execution Groups: %s<br/>
                    
                    #AB - Use HTMLParser to cleanup traceback
                    import HTMLParser
                    html_parser = HTMLParser.HTMLParser()

                    #AB - Added second div to provide expandable traceback
                    row = """
                        <tr id="%s-result" class="test-result" style="display:none">
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
                                    Start Time: %s<br />
                                    End Time: %s<br />
                                    Duration: %s<br /><br />
                                    %s
                                </div>
                                <div id="%s-hidden-ss" class='details'>
                                    %s
                                </div>
                                <div id="%s-hidden-trace" class='details'>
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
                               #resource_group_str, 
                               #result.execution_groups, 
                               result.start_time.strftime("%m-%d-%y %H:%M:%S"),
                               result.end_time.strftime("%m-%d-%y %H:%M:%S"),
                               str(result.end_time - result.start_time),
                               #AB - cleanup to allow links to display correctly
                               html_parser.unescape(details_str).replace(u'\xa0', ' '),
                               i,
                               ss_link,
                               i,
                               html_parser.unescape(traceback_str).replace(u'\xa0', ' '))

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
    failed_test_count = None
    lock = None

    def __init__(self, log_dir=None, log_level=LogLevel.ERROR, css_path=None, log_screen=LogScreen.NONE):
        if log_dir: 
            log_dir = os.path.abspath(log_dir)
        if css_path: 
            css_path = os.path.abspath(css_path) 

        TestLogger.__init__(self, log_dir=log_dir, log_level=log_level, log_screen=log_screen)
        self.css_path = css_path
        self.failed_test_count = 0
        self.lock = Lock()

    def startingTests(self):
        if not self.log_dir: self.log_dir = "."

        # Set up the log file
        self.start_time = datetime.datetime.now()
        self.log_dir = self.log_dir.rstrip(os.sep)
        
        #AB - change folder name to reflect script name
        #self.test_title = "Test Run %s" % self.start_time.strftime("%m-%d-%y %H:%M:%S")
        self.test_title = sys.argv[2].split("\\")[-1].replace(".json","") + " %s" % self.start_time.strftime("%m-%d-%y %H:%M:%S")
        
        self.log_dir += "%s%s" % (os.sep, self.test_title.replace(':', '.'))
        os.mkdir(self.log_dir)
        log_name = "%s%sresults.html" % (self.log_dir, os.sep)
        self.out = open(log_name, 'w')

        self.results = Queue()
        self.current_tests = {}
    
    def finishedTests(self):
        self.end_time = datetime.datetime.now()
        if self.css_path:
            shutil.copyfile(self.css_path, self.log_dir + "/style.css")
        else:
            self.css_path = HTMLWriter.copy_resources_to_log_dir(self.log_dir)
        HTMLWriter.write_test_results(
            self.results, 
            self.start_time, 
            self.end_time, 
            self.out, 
            css_path="style.css" # <-- this is hardcoded to work around a bug in Firefox on Windows where CSS loaded from the filesystem must use a relative path.
        )

        #AB - open test results after done writing
        self.out.close()
        
        if self.log_display:
            from selenium import webdriver
            webdriver.Firefox().get("file://" + self.log_dir + "/results.html")

        return self.failed_test_count

    def runningTestFunction(self, class_instance, func, func_type=TestFunctionType.TEST, thread_num=None):
        result = TestResult(class_instance, func, thread=thread_num)
        result.start_time = datetime.datetime.now()
        with self.lock:
            self.current_tests[(class_instance, func, thread_num)] = result

    def finishedTestFunction(self, class_instance, func, func_type=TestFunctionType.TEST, thread_num=None):
        with self.lock:
            result = self.current_tests.pop((class_instance, func, thread_num))
            # Don't log results for setup and teardown unless they fail
            if func_type == TestFunctionType.TEST or result.status == TestResultType.FAILURE:
                result.end_time = datetime.datetime.now()
                if not result.status: result.status = TestResultType.SUCCESS
                self.results.put(result)

        #AB - removed for now due to change in LogLevel structure
        #if self.log_level >= LogLevel.DEBUG:
        #    self.log_debug_info(class_instance, func)

    def skippingTestFunction(self, class_instance, func, func_type=TestFunctionType.TEST, thread_num=None):
        # Don't log results for setup and teardown unless they fail
        if func_type == TestFunctionType.TEST:
            with self.lock:
                result = TestResult(class_instance, func, status=TestResultType.SKIPPED, thread=thread_num)
                result.start_time = datetime.datetime.now()
                result.end_time = datetime.datetime.now()
                self.results.put(result)

    def foundException(self, class_instance, func, e, tb, func_type=TestFunctionType.TEST, thread_num=None):
        with self.lock:
            self.failed_test_count += 1
            result = self.current_tests[(class_instance, func, thread_num)]
        result.status = TestResultType.FAILURE
        result.error = e
        
        result.traceback = tb
        
        #AB - populate details
        #if self.log_level == LogLevel.DEBUG:
        if(tb.split("\n").pop(-2).find("AssertionError: ") == 0):
            result.details = "<b>" + tb.split("\n").pop(-2).replace("AssertionError: ","") + "</b>"
        else:
            result.details = "<b>" + tb.split("\n").pop(-2) + "</b>"

        #if self.log_level >= LogLevel.INFO:
        if self.log_screen == LogScreen.ERROR or (e == AssertionError and self.log_screen == LogScreen.ASSERT):
            result.ss_loc = self.log_debug_info(class_instance, func)
            
            #AB - added screenshot to log
            #func_str = TestLogger.format_function_name(class_instance, func)
            #path = self.log_dir if self.log_dir else "."
            #result.traceback += """\n <img src="%s/%s.png">""" % (path, func_str)

    #AB - additional logging options
    def logDetails(self, class_instance, func, str_details, thread_num=None):
        result = self.current_tests[(class_instance, func, thread_num)]
        
        if result.status == TestResultType.FAILURE:
            result.details = str_details + "\n\n" + result.details
        else:
            result.details = str_details
            result.ss_loc = self.log_debug_info(class_instance, func)