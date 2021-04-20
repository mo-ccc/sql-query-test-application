from .test_base import TestBase

class TestUser(TestBase):
    def test_get_test(self):
        response = self.client.get('/test/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn("question", response.json)

    def test_execute_correct(self):
        response = self.client.post(
            '/test/1/execute',
            json={"query": ("SELECT device_cat, COUNT(device_cat) AS a FROM google_users "
                            "GROUP BY device_cat ORDER BY a DESC;")}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("rows", response.json)
        self.assertFalse(response.json["issues"])
    
    def test_execute_incorrect(self):
        response = self.client.post(
            '/test/1/execute',
            json={"query": "SELECT * FROM users LIMIT 1;"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json["issues"])

    def test_execute_error(self):
        response = self.client.post(
            '/test/1/execute',
            json={"query": "select s from table;"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("syntax error", response.json["error"])

    