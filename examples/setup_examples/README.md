This example shows how the special setup() and teardown() methods work on a TestSet. The example tests are Selenium tests, and before executing each test we must open a browser. This is done in the setup() method. Likewise, closing the browser is done in the teardown() method.

In the SequentialTestSet, setup() is called before any tests are executed and teardown() is called after all tests are finished. You can see this in action by running
    ./egatest examples.setup_examples.testsetup.TestSetupAndTeardown1
You should see the browser open, run each test, and then close.

In the UnorderedTestSet, setup() is called before each test is executed and teardown() is called after each test is finished. You can see this in action by running
    ./egatest examples.setup_examples.testsetup.TestSetupAndTeardown2
You should see the browser open and close between each test.