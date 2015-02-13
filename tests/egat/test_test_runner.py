import unittest
from egat.test_runner import TestRunner

class TestBuildTests(unittest.TestCase):
    def test_basic(self):
        test_obj = {
            'tests': ['test1', 'test2'],
        }

        expected = [
            {
                'test': 'test1',
                'configuration': {},
                'environment': {},
            },
            {
                'test': 'test2',
                'configuration': {},
                'environment': {},
            },
        ]

        flat_tests = TestRunner._build_tests(test_obj)
        self.assertEqual(sorted(flat_tests), sorted(expected))

    def test_basic_configuration(self):
        test_obj = {
            'tests': ['test1', 'test2'],
            'configuration': {
                'base_url': 'http://github.com',
                'port': 80,
            }
        }

        expected = [
            {
                'test': 'test1',
                'configuration': {
                    'base_url': 'http://github.com',
                    'port': 80,
                },
                'environment': {},
            },
            {
                'test': 'test2',
                'configuration': {
                    'base_url': 'http://github.com',
                    'port': 80,
                },
                'environment': {},
            },
        ]

        flat_tests = TestRunner._build_tests(test_obj)
        self.assertEqual(sorted(flat_tests), sorted(expected))

    def test_basic_single_environment(self):
        test_obj = {
            'tests': ['test1', 'test2'],
            'environments': [                
                {
                    'base_url': 'http://github.com',
                    'port': 80,
                },
            ],
        }

        expected = [
            {
                'test': 'test1',
                'configuration': {},
                'environment': {
                    'base_url': 'http://github.com',
                    'port': 80,
                },
            },
            {
                'test': 'test2',
                'configuration': {},
                'environment': {
                    'base_url': 'http://github.com',
                    'port': 80,
                },
            },
        ]

        flat_tests = TestRunner._build_tests(test_obj)
        self.assertEqual(sorted(flat_tests), sorted(expected))

    def test_basic_multiple_environments(self):
        test_obj = {
            'tests': ['test1', 'test2'],
            'environments': [                
                {
                    'base_url': 'http://github.com',
                    'port': 80,
                },
                {
                    'base_url': 'http://localhost',
                    'port': 8080,
                },
                {
                    'base_url': 'http://staging',
                    'port': 80,
                },
            ],
        }

        expected = [
            {
                'test': 'test1',
                'configuration': {},
                'environment': {
                    'base_url': 'http://github.com',
                    'port': 80,
                },
            },
            {
                'test': 'test1',
                'configuration': {},
                'environment': {
                    'base_url': 'http://localhost',
                    'port': 8080,
                },
            },
            {
                'test': 'test1',
                'configuration': {},
                'environment': {
                    'base_url': 'http://staging',
                    'port': 80,
                },
            },
            {
                'test': 'test2',
                'configuration': {},
                'environment': {
                    'base_url': 'http://github.com',
                    'port': 80,
                },
            },
            {
                'test': 'test2',
                'configuration': {},
                'environment': {
                    'base_url': 'http://localhost',
                    'port': 8080,
                },
            },
            {
                'test': 'test2',
                'configuration': {},
                'environment': {
                    'base_url': 'http://staging',
                    'port': 80,
                },
            },
        ]

        flat_tests = TestRunner._build_tests(test_obj)
        self.assertEqual(sorted(flat_tests), sorted(expected))

    def test_multiple_environments_with_config(self):
        test_obj = {
            'tests': ['test1', 'test2'],
            'configuration': {
                'username': 'bob',
                'password': 'pass1word',
            },
            'environments': [                
                {
                    'base_url': 'http://github.com',
                    'port': 80,
                },
                {
                    'base_url': 'http://localhost',
                    'port': 8080,
                },
                {
                    'base_url': 'http://staging',
                    'port': 80,
                },
            ],
        }

        expected = [
            {
                'test': 'test1',
                'configuration': {
                    'username': 'bob',
                    'password': 'pass1word',
                },
                'environment': {
                    'base_url': 'http://github.com',
                    'port': 80,
                },
            },
            {
                'test': 'test1',
                'configuration': {
                    'username': 'bob',
                    'password': 'pass1word',
                },
                'environment': {
                    'base_url': 'http://localhost',
                    'port': 8080,
                },
            },
            {
                'test': 'test1',
                'configuration': {
                    'username': 'bob',
                    'password': 'pass1word',
                },
                'environment': {
                    'base_url': 'http://staging',
                    'port': 80,
                },
            },
            {
                'test': 'test2',
                'configuration': {
                    'username': 'bob',
                    'password': 'pass1word',
                },
                'environment': {
                    'base_url': 'http://github.com',
                    'port': 80,
                },
            },
            {
                'test': 'test2',
                'configuration': {
                    'username': 'bob',
                    'password': 'pass1word',
                },
                'environment': {
                    'base_url': 'http://localhost',
                    'port': 8080,
                },
            },
            {
                'test': 'test2',
                'configuration': {
                    'username': 'bob',
                    'password': 'pass1word',
                },
                'environment': {
                    'base_url': 'http://staging',
                    'port': 80,
                },
            },
        ]

        flat_tests = TestRunner._build_tests(test_obj)
        self.assertEqual(sorted(flat_tests), sorted(expected))

    def test_nested(self):
        test_obj = {
            'tests': [
                {
                    'tests': [
                        'test1',
                    ],
                },
                {
                    'tests': [
                        'test2',
                        'test3',
                    ],
                },
                {
                    'tests': [
                        {
                            'tests': [
                                'test4',
                                'test5',
                            ],
                            'configuration': {
                                'base_url': 'http://localhost',
                                'password': 'secret'
                            }
                        },
                    ],
                    'configuration': {
                        'username': 'bob',
                        'password': 'pass1word',
                    },
                },
            ],
            'configuration': {
                'base_url': 'http://github.com',
                'port': 80,
            }
        }

        expected = [
            {
                'test': 'test1',
                'configuration': {
                    'base_url': 'http://github.com',
                    'port': 80,
                },
                'environment': {},
            },
            {
                'test': 'test2',
                'configuration': {
                    'base_url': 'http://github.com',
                    'port': 80,
                },
                'environment': {},
            },
            {
                'test': 'test3',
                'configuration': {
                    'base_url': 'http://github.com',
                    'port': 80,
                },
                'environment': {},
            },
            {
                'test': 'test4',
                'configuration': {
                    'base_url': 'http://localhost',
                    'port': 80,
                    'username': 'bob',
                    'password': 'secret',
                },
                'environment': {},
            },
            {
                'test': 'test5',
                'configuration': {
                    'base_url': 'http://localhost',
                    'port': 80,
                    'username': 'bob',
                    'password': 'secret',
                },
                'environment': {},
            },
        ]

        flat_tests = TestRunner._build_tests(test_obj)
        self.assertEqual(sorted(flat_tests), sorted(expected))

    def test_nested_with_environments(self):
        test_obj = {
            'tests': [
                {
                    'tests': [
                        'test1',
                    ],
                    'environments': [
                        {
                            'base_url': 'http://staging',
                        },
                    ]
                },
                {
                    'tests': [
                        'test2',
                        'test3',
                    ],
                },
                {
                    'tests': [
                        {
                            'tests': [
                                'test4',
                                'test5',
                            ],
                            'configuration': {
                                'base_url': 'http://localhost',
                                'password': 'secret'
                            },
                            'environments': [
                                {
                                    'database': 'db1:5796',
                                    'memcache': 'localhost:7777'
                                },
                                {
                                    'database': 'db2:5796',
                                    'memcache': 'localhost:8888'
                                },
                            ],
                        },
                    ],
                    'configuration': {
                        'username': 'bob',
                        'password': 'pass1word',
                    },
                    'environments': [
                        {
                            'database': 'http://localhost:5796',
                            'number_of_clients': 10,
                        },
                        {
                            'database': 'http://localhost:5796',
                            'number_of_clients': 50,
                        },
                    ],
                },
            ],
            'configuration': {
                'base_url': 'http://github.com',
                'port': 80,
            }
        }

        expected = [
            {
                'test': 'test1',
                'configuration': {
                    'base_url': 'http://github.com',
                    'port': 80,
                },
                'environment': {
                    'base_url': 'http://staging',
                },
            },
            {
                'test': 'test2',
                'configuration': {
                    'base_url': 'http://github.com',
                    'port': 80,
                },
                'environment': {},
            },
            {
                'test': 'test3',
                'configuration': {
                    'base_url': 'http://github.com',
                    'port': 80,
                },
                'environment': {},
            },
            {
                'test': 'test4',
                'configuration': {
                    'base_url': 'http://localhost',
                    'port': 80,
                    'username': 'bob',
                    'password': 'secret',
                },
                'environment': {
                    'number_of_clients': 10,
                    'database': 'db1:5796',
                    'memcache': 'localhost:7777'
                },
            },
            {
                'test': 'test5',
                'configuration': {
                    'base_url': 'http://localhost',
                    'port': 80,
                    'username': 'bob',
                    'password': 'secret',
                },
                'environment': {
                    'number_of_clients': 10,
                    'database': 'db1:5796',
                    'memcache': 'localhost:7777'
                },
            },
            {
                'test': 'test4',
                'configuration': {
                    'base_url': 'http://localhost',
                    'port': 80,
                    'username': 'bob',
                    'password': 'secret',
                },
                'environment': {
                    'number_of_clients': 50,
                    'database': 'db1:5796',
                    'memcache': 'localhost:7777'
                },
            },
            {
                'test': 'test5',
                'configuration': {
                    'base_url': 'http://localhost',
                    'port': 80,
                    'username': 'bob',
                    'password': 'secret',
                },
                'environment': {
                    'number_of_clients': 50,
                    'database': 'db1:5796',
                    'memcache': 'localhost:7777'
                },
            },
            {
                'test': 'test4',
                'configuration': {
                    'base_url': 'http://localhost',
                    'port': 80,
                    'username': 'bob',
                    'password': 'secret',
                },
                'environment': {
                    'number_of_clients': 50,
                    'database': 'db2:5796',
                    'memcache': 'localhost:8888'
                },
            },
            {
                'test': 'test5',
                'configuration': {
                    'base_url': 'http://localhost',
                    'port': 80,
                    'username': 'bob',
                    'password': 'secret',
                },
                'environment': {
                    'number_of_clients': 50,
                    'database': 'db2:5796',
                    'memcache': 'localhost:8888'
                },
            },
            {
                'test': 'test4',
                'configuration': {
                    'base_url': 'http://localhost',
                    'port': 80,
                    'username': 'bob',
                    'password': 'secret',
                },
                'environment': {
                    'number_of_clients': 10,
                    'database': 'db2:5796',
                    'memcache': 'localhost:8888'
                },
            },
            {
                'test': 'test5',
                'configuration': {
                    'base_url': 'http://localhost',
                    'port': 80,
                    'username': 'bob',
                    'password': 'secret',
                },
                'environment': {
                    'number_of_clients': 10,
                    'database': 'db2:5796',
                    'memcache': 'localhost:8888'
                },
            },
        ]

        flat_tests = TestRunner._build_tests(test_obj)
        self.assertEqual(sorted(flat_tests), sorted(expected))

    def test_nested_mixed(self):
        test_obj = {
            'tests': [
                {
                    'tests': [
                        'test1',
                        {
                            'tests': [
                                {
                                    'tests': [
                                        'test4',
                                        'test5',
                                    ],
                                    'configuration': {
                                        'base_url': 'http://localhost',
                                        'password': 'secret'
                                    }
                                },
                            ],
                            'configuration': {
                                'username': 'bob',
                                'password': 'pass1word',
                            },
                        },
                    ],
                },
                {
                    'tests': [
                        'test2',
                        'test3',
                    ],
                },
            ],
            'configuration': {
                'base_url': 'http://github.com',
                'port': 80,
            }
        }

        expected = [
            {
                'test': 'test1',
                'configuration': {
                    'base_url': 'http://github.com',
                    'port': 80,
                },
                'environment': {},
            },
            {
                'test': 'test2',
                'configuration': {
                    'base_url': 'http://github.com',
                    'port': 80,
                },
                'environment': {},
            },
            {
                'test': 'test3',
                'configuration': {
                    'base_url': 'http://github.com',
                    'port': 80,
                },
                'environment': {},
            },
            {
                'test': 'test4',
                'configuration': {
                    'base_url': 'http://localhost',
                    'port': 80,
                    'username': 'bob',
                    'password': 'secret',
                },
                'environment': {},
            },
            {
                'test': 'test5',
                'configuration': {
                    'base_url': 'http://localhost',
                    'port': 80,
                    'username': 'bob',
                    'password': 'secret',
                },
                'environment': {},
            },
        ]

        flat_tests = TestRunner._build_tests(test_obj)
        self.assertEqual(sorted(flat_tests), sorted(expected))
        
