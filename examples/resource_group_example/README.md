This example showcases the use of SharedResources to describe dependencies between
classes. The resourse_group_test.py defines a few tests, some of which cannot be run
concurrently.

To run these tests, execute this command from the root of the project:
    ./egatest -c examples/resource_group_example/resource_group_test.json

If you look closely at the start and end times of the tests in the test results,
you will see that none of the tests with the same Shared Resource were executed
concurrently.

