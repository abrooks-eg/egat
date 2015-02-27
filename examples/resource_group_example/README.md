This example showcases the use of SharedResources to describe dependencies between
classes. The resourse_group_test.py defines a few tests, some of which cannot be run
concurrently.

To run these tests, execute this command from the root of the project:
    ./egatest -c examples/resource_group_example/resource_group_test.json

Depending on the speed of your processor, you may see all tests executed in one
thread, even though we specified two threads in the configuration file. But rest
assured, no tests with the same SharedResource will be run at the same time.