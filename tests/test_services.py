import os
import unittest
from unittest.mock import Mock, patch

from cmdb_clients import CMDB, VALI, JIRA, Config, Logger


class TestServices(unittest.TestCase):
    def setUp(self):
        # Reset Config singleton state between tests
        cfg = Config()
        cfg._data.clear()

    def test_cmdb_get_item_calls_requests(self):
        c = CMDB('https://api.example.com')
        mock_resp = Mock()
        mock_resp.json.return_value = {'id': '123'}
        mock_resp.raise_for_status.return_value = None

        with patch('requests.request', return_value=mock_resp) as mock_req:
            res = c.get_item('123')
            self.assertEqual(res, {'id': '123'})
            mock_req.assert_called_once()
            args, kwargs = mock_req.call_args
            self.assertEqual(args[0], 'GET')
            self.assertEqual(args[1], 'https://api.example.com/items/123')

    def test_vali_validate_calls_requests(self):
        v = VALI('https://vali.example.com')
        payload = {'foo': 'bar'}
        mock_resp = Mock()
        mock_resp.json.return_value = {'ok': True}
        mock_resp.raise_for_status.return_value = None

        with patch('requests.request', return_value=mock_resp) as mock_req:
            res = v.validate(payload)
            self.assertEqual(res, {'ok': True})
            mock_req.assert_called_once()
            args, kwargs = mock_req.call_args
            self.assertEqual(args[0], 'POST')
            self.assertEqual(args[1], 'https://vali.example.com/validate')
            self.assertIn('json', kwargs)
            self.assertEqual(kwargs['json'], payload)

    def test_jira_create_issue_calls_requests(self):
        j = JIRA('https://jira.example.com')
        payload = {'summary': 'Issue'}
        mock_resp = Mock()
        mock_resp.json.return_value = {'key': 'PROJ-1'}
        mock_resp.raise_for_status.return_value = None

        with patch('requests.request', return_value=mock_resp) as mock_req:
            res = j.create_issue('PROJ', payload)
            self.assertEqual(res, {'key': 'PROJ-1'})
            mock_req.assert_called_once()
            args, kwargs = mock_req.call_args
            self.assertEqual(args[0], 'POST')
            self.assertEqual(args[1], 'https://jira.example.com/projects/PROJ/issues')

    def test_config_env_and_dict(self):
        cfg = Config()
        cfg.load_dict({'A': '1'})
        # env fallback
        os.environ['B'] = 'env-b'
        self.assertEqual(cfg.get('A'), '1')
        self.assertEqual(cfg.get('B'), 'env-b')
        self.assertEqual(cfg.get('C', 'default'), 'default')

    def test_logger_singleton(self):
        l1 = Logger()
        l2 = Logger()
        self.assertIs(l1, l2)
        self.assertTrue(hasattr(l1, 'get'))


if __name__ == '__main__':
    unittest.main()
