import unittest
from unittest.mock import patch
from main import app


class Testing(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.custom_history = []

    @patch("main.analyze_frequency")
    def test_word_frequency(self, mock_analyze_frequency):

        response = self.app.get("/frequency?topic=Python&n=1")
        # check if the response is 200
        self.assertEqual(response.status_code, 200)

        response_data = response.get_json()
        # print(response_data)
        # check if the response has the required keys
        self.assertIn("topic", response_data)
        self.assertIn("top_words", response_data)

    @patch("main.analyze_frequency")
    def test_word_frequency_with_invalid_parameters(self, mock_analyze_frequency):
        # Test when 'topic' is None
        response_topic_none = self.app.get("/frequency?n=1")
        self.assertEqual(response_topic_none.status_code, 400)
        response_data_topic_none = response_topic_none.get_json()
        self.assertIn("error", response_data_topic_none)
        self.assertEqual(response_data_topic_none["error"], "topic is required")

        # Test when 'n' is less than 1
        response_n_invalid = self.app.get("/frequency?topic=Python&n=0")
        self.assertEqual(response_n_invalid.status_code, 400)
        response_data_n_invalid = response_n_invalid.get_json()
        self.assertIn("error", response_data_n_invalid)
        self.assertEqual(response_data_n_invalid["error"], "n must be greater than 0")

    @patch("main.get_search_history")
    def test_get_search_history(self, mock_get_search_history):
        self.assertEqual(len(self.custom_history), 0)
        response = self.app.get("/frequency?topic=Python&n=1")
        self.assertEqual(response.status_code, 200)
        self.custom_history.append(response)
        self.assertEqual(len(self.custom_history), 1)


if __name__ == "__main__":
    unittest.main()
