from .test_base import TestBase

class TestUser(TestBase):
    def test_register(self):
        response = self.client.post(
            '/user',
            json={"email": "test@email.com"}
        )
        self.assertIn('tests', response.json)
        self.assertEqual(response.status_code, 201)
