import os
import tempfile
import unittest

from cmdb_clients import Config


class TestConfigParsing(unittest.TestCase):
    def setUp(self):
        self.cfg = Config()
        self.cfg._data.clear()
        self.cfg.set_schema({
            'INT_VAL': {'type': 'int', 'env': 'INT_VAL'},
            'BOOL_VAL': {'type': 'bool', 'env': 'BOOL_VAL'},
            'FLOAT_VAL': {'type': 'float', 'env': 'FLOAT_VAL'},
            'JSON_VAL': {'type': 'json', 'env': 'JSON_VAL'},
            'SECRET': {'env': 'SECRET', 'secret': True},
            'FILE_SECRET': {'env': 'FILE_SECRET', 'secret': True},
        })

    def test_casting_types_from_env(self):
        os.environ['INT_VAL'] = '10'
        os.environ['BOOL_VAL'] = 'true'
        os.environ['FLOAT_VAL'] = '3.14'
        os.environ['JSON_VAL'] = '{"a": 1}'

        self.assertEqual(self.cfg.get('INT_VAL'), 10)
        self.assertEqual(self.cfg.get('BOOL_VAL'), True)
        self.assertAlmostEqual(self.cfg.get('FLOAT_VAL'), 3.14)
        self.assertEqual(self.cfg.get('JSON_VAL'), {'a': 1})

    def test_secret_masking_and_file_secret(self):
        # file secret
        with tempfile.NamedTemporaryFile('w+', delete=False) as tf:
            tf.write('supersecret')
            tf.flush()
            path = tf.name

        os.environ['FILE_SECRET'] = f'file://{path}'
        os.environ['SECRET'] = 'plainsecret'

        # actual values
        self.assertEqual(self.cfg.get('FILE_SECRET'), 'supersecret')
        self.assertEqual(self.cfg.get('SECRET'), 'plainsecret')

        # masked output
        d = self.cfg.as_dict(mask_secrets=True)
        self.assertEqual(d['SECRET'], '*****')
        self.assertEqual(d['FILE_SECRET'], '*****')


if __name__ == '__main__':
    unittest.main()
