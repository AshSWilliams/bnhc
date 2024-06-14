"""
Tests for the functions in match.py
"""
import json
import pytest

from src.match import filter_jobs_by_location, get_candidate_location, rank_jobs

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
        assert get_candidate_location(self.members[0], job_locations.copy()) == ["london"]
        assert set(get_candidate_location(self.members[3], job_locations.copy())) == set(["edinburgh", "york", "manchester"])
        assert get_candidate_location(self.members[4], job_locations.copy()) == ["london"]
    
    def test_rank_jobs(self):
        """Test rank_jobs"""
        bio = self.members[0]["bio"]
        job_titles = [job["title"].lower() for job in self.jobs]
        assert rank_jobs(bio, job_titles) == {"ux designer": 1}

