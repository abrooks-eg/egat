This example showcases E-gAT's auto-threading capability. If you look in auto_threads.json you will see that the "-t" option has been set to 4. This means that our tests will execute in 4 threads. And that's all it takes. If two tests cannot be executed at the same time then SharedResources may be used (see the documentation or the resource_group_example).

This example can be run by executing:
    ./egatest -c examples/auto_threaded_example/auto_threads.json
from the root directory of the project
