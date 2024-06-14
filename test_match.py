import unittest

from match import match_jobs

class TestMatchJobs(unittest.TestCase):
    def test_match_jobs(self):
        candidate = {
            "bio": "Experienced software engineer with Python skills",
        }
        jobs = [
            {
                "title": "Python Developer",
                "location": "San Francisco",
            },
            {
                "title": "Java Developer",
                "location": "New York",
            },
            {
                "title": "Frontend Developer",
                "location": "San Francisco",
            },
        ]
        expected_result = {
            "Python Developer": 1,
            "Frontend Developer": 0,
        }
        self.assertEqual(match_jobs(candidate, jobs), expected_result)

if __name__ == "__main__":
    unittest.main()