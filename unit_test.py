import unittest
import requests

API_URL = "http://ece444pra5.eu-north-1.elasticbeanstalk.com/predict"

TEST_CASES = {
"fake_1": "Breaking: President spotted on Mars with aliens",
"fake_2": "Scientists confirm the earth is flat and NASA admits global cover-up.",
"real_1": "The World Health Organization issued new guidelines for pandemic response.",
"real_2": "Trump announces tariffs on Canada"
}

class TestFakeNewsAPI(unittest.TestCase):
    def test_predictions(self):
        for label, text in TEST_CASES.items():
            with self.subTest(test_case=label):
                try:
                    response = requests.post(API_URL, json={"message": text}, timeout=10)
                    self.assertEqual(response.status_code, 200, f"HTTP status not 200 for {label}")
                    data = response.json()
                    self.assertIn("label", data, f"No 'label' in response for {label}")
                    print(f"{label} -> {data['label']}")
                except Exception as e:
                    self.fail(f"Request failed for {label}: {e}")

if __name__ == "__main__":
    unittest.main()
