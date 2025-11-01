import unittest
from unittest.mock import Mock, patch

from one_clients import JIRA


class TestJiraJql(unittest.TestCase):
    def test_jql_with_issues_array(self):
        j = JIRA('https://jira.example.com')
        mock_resp = Mock()
        mock_resp.json.return_value = {
            'issues': [
                {'key': 'PROJ-1'},
                {'key': 'PROJ-2'},
            ]
        }
        mock_resp.raise_for_status.return_value = None

        with patch('requests.request', return_value=mock_resp) as mock_req:
            res = j.jql('project = PROJ')
            self.assertEqual(res, ['PROJ-1', 'PROJ-2'])
            mock_req.assert_called_once()
            args, kwargs = mock_req.call_args
            self.assertEqual(args[0], 'GET')
            # URL built from base_url + path
            self.assertEqual(args[1], 'https://jira.example.com/search')
            self.assertIn('params', kwargs)
            self.assertEqual(kwargs['params']['jql'], 'project = PROJ')

    def test_jql_with_list_response(self):
        j = JIRA('https://jira.example.com')
        mock_resp = Mock()
        mock_resp.json.return_value = ['PROJ-3', 'PROJ-4']
        mock_resp.raise_for_status.return_value = None

        with patch('requests.request', return_value=mock_resp) as mock_req:
            res = j.jql('project = PROJ')
            self.assertEqual(res, ['PROJ-3', 'PROJ-4'])

    def test_jql_custom_path(self):
        j = JIRA('https://jira.example.com')
        mock_resp = Mock()
        mock_resp.json.return_value = {'issues': [{'key': 'X-1'}]}
        mock_resp.raise_for_status.return_value = None

        with patch('requests.request', return_value=mock_resp) as mock_req:
            res = j.jql('project = X', path='/rest/api/2/search')
            self.assertEqual(res, ['X-1'])
            args, kwargs = mock_req.call_args
            self.assertEqual(args[1], 'https://jira.example.com/rest/api/2/search')


if __name__ == '__main__':
    unittest.main()
