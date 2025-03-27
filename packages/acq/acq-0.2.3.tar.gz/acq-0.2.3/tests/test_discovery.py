import unittest

from acq.discovery import discover

from unittest import mock

NOT_A_MODULE = 'Not A Module'
NOT_ANOTHER_MODULE = 'Not Another Module'
NOT_YET_ANOTHER_MODULE = 'Not Yet Another Module'


class DiscoveryTestCase(unittest.TestCase):
    class FancyClass:
        pass

    class FancySubClass(FancyClass):
        pass

    @mock.patch('importlib.import_module')
    def test_discover_imports_expected_module(self, import_module):
        import_module.return_value = NOT_A_MODULE

        modules = discover('example1')

        import_module.assert_called_once_with('example1')
        assert modules[0] == NOT_A_MODULE

    @mock.patch('importlib.import_module')
    def test_discover_imports_multiple_modules(self, import_module):
        import_module.side_effect = [
            NOT_A_MODULE,
            NOT_ANOTHER_MODULE,
            NOT_YET_ANOTHER_MODULE,
        ]

        modules = discover('example1', 'example2', 'example3')

        import_module.assert_has_calls(
            [
                mock.call('example1'),
                mock.call('example2'),
                mock.call('example3'),
            ]
        )

        assert modules[0] == NOT_A_MODULE
        assert modules[1] == NOT_ANOTHER_MODULE

    @mock.patch('importlib.import_module')
    def test_discover_called_with_no_modules(self, import_module):
        assert discover() == []
        assert import_module.call_count == 0

    @mock.patch('importlib.import_module')
    def test_discover_ignores_non_existant_modules(self, import_module):
        import_module.side_effect = [
            NOT_A_MODULE,
            ModuleNotFoundError('That is not a module.'),
            NOT_ANOTHER_MODULE,
        ]
        modules = discover('example1', 'example2', 'example3')
        assert len(modules) == 2

    @mock.patch('importlib.import_module')
    def test_discover_called_with_package_names(self, import_module):
        import_module.side_effect = [
            NOT_A_MODULE,
            NOT_ANOTHER_MODULE,
        ]
        modules = discover(package_names=['example1', 'example2'])

        assert len(modules) == 2
        assert modules[0] == NOT_A_MODULE
        assert modules[1] == NOT_ANOTHER_MODULE

    @mock.patch('importlib.import_module')
    def test_discover_called_with_package_names_and_module_names(
        self, import_module
    ):
        discover(
            'registration',
            'identification',
            package_names=['example1', 'example2'],
        )

        assert import_module.call_count == 4
        import_module.assert_has_calls(
            [
                mock.call('example1.registration'),
                mock.call('example1.identification'),
                mock.call('example2.registration'),
                mock.call('example2.identification'),
            ],
            any_order=True,
        )

    @mock.patch('importlib.import_module')
    def test_discover_returns_module_when_given_module(self, import_module):
        results = discover(unittest)

        self.assertEqual(import_module.call_count, 0)
        self.assertEqual(len(results), 1)
        self.assertIs(results[0], unittest)

    @mock.patch('importlib.import_module')
    def test_discover_gets_matching_instance_via_types(self, import_module):
        fake_module = mock.MagicMock()
        import_module.return_value = fake_module

        fake_module.FancyClass = self.FancyClass

        types = discover('example1', types=(self.FancyClass,))
        fancy_classes = list(types[self.FancyClass])

        self.assertEqual(len(fancy_classes), 1)
        self.assertIs(fancy_classes[0], self.FancyClass)

    @mock.patch('importlib.import_module')
    def test_discover_gets_class_via_types(self, import_module):
        fake_module = mock.MagicMock()
        import_module.return_value = fake_module

        fake_module.FancySubClass = self.FancySubClass

        types = discover('example1', types=(self.FancyClass,))
        fancy_classes = list(types[self.FancyClass])

        self.assertEqual(len(fancy_classes), 1)
        self.assertIs(fancy_classes[0], self.FancySubClass)

    @mock.patch('importlib.import_module')
    def test_discover_gets_instance_via_types(self, import_module):
        fake_module = mock.MagicMock()
        instance = self.FancySubClass()

        import_module.return_value = fake_module
        fake_module.fancy_sub_instance = instance

        types = discover('example1', types=(self.FancyClass,))
        fancy_classes = list(types[self.FancyClass])

        self.assertEqual(len(fancy_classes), 1)
        self.assertIs(fancy_classes[0], instance)
