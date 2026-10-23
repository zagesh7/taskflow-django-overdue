from unittest.mock import MagicMock, patch

from django.test import SimpleTestCase, TestCase, override_settings

from .services import mark_overdue_tasks


class OverdueServiceTests(TestCase):
    @patch('overdue_api.services.connection.cursor')
    def test_sweep_updates_only_past_due_unfinished_tasks(self, cursor_factory):
        cursor = MagicMock()
        cursor.rowcount = 3
        cursor_factory.return_value.__enter__.return_value = cursor

        updated = mark_overdue_tasks()

        self.assertEqual(updated, 3)
        sql = next(call.args[0] for call in cursor.execute.call_args_list if call.args[0].startswith('UPDATE tasks'))
        self.assertIn("due_date < UTC_DATE()", sql)
        self.assertIn("status <> 'DONE'", sql)
        self.assertIn("status <> 'OVERDUE'", sql)


class OverdueEndpointTests(SimpleTestCase):
    @override_settings(OVERDUE_SYNC_TOKEN='sync-secret')
    def test_health_endpoint_returns_consistent_json(self):
        response = self.client.get('/health/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'data': {'status': 'ok'}})

    @override_settings(OVERDUE_SYNC_TOKEN='sync-secret')
    @patch('overdue_api.views.mark_overdue_tasks')
    def test_sync_requires_internal_token(self, sync):
        response = self.client.post('/api/tasks/sync-overdue/')

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'error': {'message': 'Unauthorized'}})
        sync.assert_not_called()

    @override_settings(OVERDUE_SYNC_TOKEN='sync-secret')
    @patch('overdue_api.views.mark_overdue_tasks', return_value=4)
    def test_valid_internal_token_runs_sweep(self, sync):
        response = self.client.post('/api/tasks/sync-overdue/', HTTP_X_INTERNAL_TOKEN='sync-secret')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'data': {'updated': 4}})
        sync.assert_called_once_with()

    @override_settings(OVERDUE_SYNC_TOKEN='')
    @patch('overdue_api.views.mark_overdue_tasks')
    def test_sync_fails_closed_when_token_is_unconfigured(self, sync):
        response = self.client.post('/api/tasks/sync-overdue/', HTTP_X_INTERNAL_TOKEN='anything')

        self.assertEqual(response.status_code, 401)
        sync.assert_not_called()
