# E-gAT
E-gAT is a set of tools for writing automated functional tests. 

E-gAT is a great fit for executing tests in a less-than-perfect environment - when tests have very long execution times, when you need to test in multiple environments/browsers, and when it’s prohibitive to execute every test in a pristine environment (like a unit test). But it’s also an excellent platform for continuous integration / automated build environments and regression tests where you expect the vast majority of tests to succeed - where you need to limit human tester time but need to know quickly if something has broken.

Currently, E-gAT supports tests written in the Python language. It includes a test class, a test runner, and a configurable logger designed to give the tester more control over execution of tests with support for test parallelization, synchronization, ordered execution, and fast failure. It comes ready to build Page Object based solutions, but one-off tests work well, too.

