This example shows how a user can manually specify in which threads tests should run. Looking in user_threads.json we can see that the "-u" option is used, and looking at the "test" list we can see that it a two-dimensional list of tests.

Each list in the "tests" list represents a thread, and all the tests specified in a list will be executed in the same thread. You can see this in action by running
    ./egatest -c examples/user_defined_threads_example/user_threads.json
From the root of the project. Examine the test output and verify that Test1 and Test2 executed in one thread and Test3 executed in another.