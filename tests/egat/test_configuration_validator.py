import unittest
from egat.parse import ConfigurationValidator
from egat.parse import ParseError

class TestConfigurationValidator_ValidateConfigJSON(unittest.TestCase):
    def test_root_json_not_dict(self):
        self.assertRaises(ParseError, ConfigurationValidator.validate_config_json, [])
        self.assertRaises(ParseError, ConfigurationValidator.validate_config_json, "")
        self.assertRaises(ParseError, ConfigurationValidator.validate_config_json, 44)
        self.assertRaises(ParseError, ConfigurationValidator.validate_config_json, 4.4)
        self.assertRaises(ParseError, ConfigurationValidator.validate_config_json, 44e44)

    def test_configuration_not_dict(self):
        json = {u'configuration': []}
        self.assertRaises(ParseError, ConfigurationValidator.validate_config_json, json)

        json = {u'configuration': u"not a dict"}
        self.assertRaises(ParseError, ConfigurationValidator.validate_config_json, json)

        json = {u'configuration': 4}
        self.assertRaises(ParseError, ConfigurationValidator.validate_config_json, json)

    def test_tests_not_present(self):
        self.assertRaises(KeyError, ConfigurationValidator.validate_config_json, {})

    def test_options_not_dict(self):
        json = {u'tests': [], u'options': []}
        self.assertRaises(ParseError, ConfigurationValidator.validate_config_json, json)
        json = {u'tests': [], u'options': ""}
        self.assertRaises(ParseError, ConfigurationValidator.validate_config_json, json)
        json = {u'tests': [], u'options': 44}
        self.assertRaises(ParseError, ConfigurationValidator.validate_config_json, json)
        json = {u'tests': [], u'options': 4.4}
        self.assertRaises(ParseError, ConfigurationValidator.validate_config_json, json)
        json = {u'tests': [], u'options': 44e44}
        self.assertRaises(ParseError, ConfigurationValidator.validate_config_json, json)

    def test_good_auto_threaded_config(self):
        json = {
            u'options': {
                u'-t': 10,
                u'-l': u".",
            },

            u'tests': [
                u'mod1',
                {
                    u'tests': [
                        u'mod2.test1',
                        u'mod2.test2',
                    ],
                    u'configuration': {
                        u'base_url': u'http://localhost:8000',
                    },
                    u'environments': [
                        {
                            u'browser': u'Chrome',
                        },
                        {
                            u'browser': u'Firefox',
                        },
                    ],
                },
            ],

            u'configuration': {
                u'base_url': u'localhost:9000',
            },

            u'extraneous_key': {},
        }

        ConfigurationValidator.validate_config_json(json)

    def test_good_user_threaded_config(self):
        json = {
            u'options': {
                u'-l': u".",
                u'-u': u'',
            },

            u'tests': [
                [
                    u'mod1'
                ],
                [
                    u'mod2.test1',
                    u'mod2.test2',
                ],
            ],
            u'configuration': {
                u'base_url': u'localhost:9000',
            },
            u'extraneous_key': {},
        }

        ConfigurationValidator.validate_config_json(json)

class TestConfigurationValidator_ValidateUserThreadedJSON(unittest.TestCase):
    def test_tests_not_2d_list(self):
        json = {u'options': {u'-u': ''}, u'tests': {}}
        self.assertRaises(ParseError, ConfigurationValidator.validate_config_json, json)

        json = {u'options': {u'-u': ''}, u'tests': u"module.ClassName"}
        self.assertRaises(ParseError, ConfigurationValidator.validate_config_json, json)

        json = {u'options': {u'-u': ''}, u'tests': [u"str", {}]}
        self.assertRaises(ParseError, ConfigurationValidator.validate_config_json, json)

        json = {u'options': {u'-u': ''}, u'tests': [[u"str"], {}]}
        self.assertRaises(ParseError, ConfigurationValidator.validate_config_json, json)

    def test_tests_is_not_2d_list_of_strings(self):
        json = {u'options': {u'-u': ''}, u'tests': [[u"str", u"str"], [u"str", {}]]}
        self.assertRaises(TypeError, ConfigurationValidator.validate_config_json, json)

        json = {u'options': {u'-u': ''}, u'tests': [[u"str", u"str"], [u"str", 1]]}
        self.assertRaises(TypeError, ConfigurationValidator.validate_config_json, json)

    def test_environments_present(self):
        json = {u'options': {u'-u': ''}, u'tests': [], u'environments': []}
        self.assertRaises(ParseError, ConfigurationValidator.validate_config_json, json)

class TestConfigurationValidator_ValidateAutoThreadedJSON(unittest.TestCase):
    def test_json_is_dict_or_unicode(self):
        self.assertRaises(ParseError, ConfigurationValidator.validate_auto_threaded_json, [])
        self.assertRaises(ParseError, ConfigurationValidator.validate_auto_threaded_json, 4)
        self.assertRaises(ParseError, ConfigurationValidator.validate_auto_threaded_json, 4.4)
        self.assertRaises(ParseError, ConfigurationValidator.validate_auto_threaded_json, 44e44)

    def test_tests_key_not_present(self):
        self.assertRaises(KeyError, ConfigurationValidator.validate_auto_threaded_json, {})

    def test_tests_key_not_list(self):
        self.assertRaises(ParseError, ConfigurationValidator.validate_auto_threaded_json, {u'tests': {}})
        self.assertRaises(ParseError, ConfigurationValidator.validate_auto_threaded_json, {u'tests': u'str'})
        self.assertRaises(ParseError, ConfigurationValidator.validate_auto_threaded_json, {u'tests': 4})
        self.assertRaises(ParseError, ConfigurationValidator.validate_auto_threaded_json, {u'tests': 4.4})
        self.assertRaises(ParseError, ConfigurationValidator.validate_auto_threaded_json, {u'tests': 44e44})

    def test_options_not_dict(self):
        self.assertRaises(ParseError, ConfigurationValidator.validate_auto_threaded_json, {u'tests': [], u'options': []})
        self.assertRaises(ParseError, ConfigurationValidator.validate_auto_threaded_json, {u'tests': [], u'options': u'str'})
        self.assertRaises(ParseError, ConfigurationValidator.validate_auto_threaded_json, {u'tests': [], u'options': 4})
        self.assertRaises(ParseError, ConfigurationValidator.validate_auto_threaded_json, {u'tests': [], u'options': 4.4})
        self.assertRaises(ParseError, ConfigurationValidator.validate_auto_threaded_json, {u'tests': [], u'options': 44e44})

    def test_environments_not_list_of_dicts(self):
        self.assertRaises(ParseError, ConfigurationValidator.validate_auto_threaded_json, {u'tests': [], u'environments': u'str'})
        self.assertRaises(ParseError, ConfigurationValidator.validate_auto_threaded_json, {u'tests': [], u'environments': 4})
        self.assertRaises(ParseError, ConfigurationValidator.validate_auto_threaded_json, {u'tests': [], u'environments': 4.4})
        self.assertRaises(ParseError, ConfigurationValidator.validate_auto_threaded_json, {u'tests': [], u'environments': 44e44})

        self.assertRaises(ParseError, ConfigurationValidator.validate_auto_threaded_json, {u'tests': [], u'environments': [[]]})
        self.assertRaises(ParseError, ConfigurationValidator.validate_auto_threaded_json, {u'tests': [], u'environments': [u'str']})
        self.assertRaises(ParseError, ConfigurationValidator.validate_auto_threaded_json, {u'tests': [], u'environments': [4]})
        self.assertRaises(ParseError, ConfigurationValidator.validate_auto_threaded_json, {u'tests': [], u'environments': [4.4]})
        self.assertRaises(ParseError, ConfigurationValidator.validate_auto_threaded_json, {u'tests': [], u'environments': [44e44]})

    def test_environments_empty_list(self):
        ConfigurationValidator.validate_auto_threaded_json({u'tests': [], u'environments': []})
