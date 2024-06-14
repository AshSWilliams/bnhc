"""
Tests for the functions in match.py
"""
import json
import pytest

from src.match import filter_jobs_by_location, get_candidate_location

class TestMatch:
    """Tests match functions"""
    @pytest.fixture(autouse=True)
    def set_up(self):
        with open("tests/members.json") as file:
            self.members = json.load(file)
        with open("tests/jobs.json") as file:
            self.jobs = json.load(file)
    
    def test_filter_jobs_by_location(self):
        """Test filter_jobs_by_location"""
        jobs = self.jobs.copy()
        assert filter_jobs_by_location(self.members[0], jobs) == [self.jobs[0], self.jobs[2], self.jobs[3], self.jobs[5], self.jobs[6]]
    
    def test_get_candidate_location(self):
        """Test get_candidate_location"""
        job_locations = set([job["location"].lower() for job in self.jobs])
        assert get_candidate_location(self.members[0], job_locations) == ["london"]
        assert set(get_candidate_location(self.members[3], job_locations)) == set(["edinburgh", "york", "manchester"])

