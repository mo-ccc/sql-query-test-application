from .test_base import TestBase
from main import db

class TestTest(TestBase):
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
        print(response.json)
        self.assertEqual(response.status_code, 200)
        self.assertIn("rows", response.json)
        self.assertFalse(response.json["issues"])
    
    def test_execute_incorrect(self):
        response = self.client.post(
            '/test/1/execute',
            json={"query": "SELECT * FROM users LIMIT 1;"}
        )
        print(response.json)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json["issues"])

    def test_execute_error(self):
        response = self.client.post(
            '/test/1/execute',
            json={"query": "select * from user1;"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual("relation \"user1\" does not exist", response.json["error"])

    def test_submit_correct(self):
        response = self.client.post(
            '/test/1/submit',
            json={"query": ("SELECT device_cat, COUNT(device_cat) AS b FROM google_users "
                            "GROUP BY device_cat ORDER BY b DESC;")}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["result"], 1)

    def test_submit_incorrect(self):
        response = self.client.post(
            '/test/1/submit',
            json={"query": "SELECT user_id FROM users LIMIT 3;"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["result"], 0)

    def test_submit_error(self):
        response = self.client.post(
            '/test/1/submit',
            json={"query": "SELECT from user1;"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["result"], 0)

    def test_submit_twice(self):
        response = self.client.post(
            '/test/1/submit',
            json={"query": "SELECT from user1;"}
        )
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            '/test/1/submit',
            json={"query": "SELECT from user1;"}
        )
        self.assertEqual(response.status_code, 400)

    
    