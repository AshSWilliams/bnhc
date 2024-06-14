"""
Entrypoint to the script
"""
from utils import get_api, format_output
from match import match_jobs

members_url = "https://bn-hiring-challenge.fly.dev/members.json"
jobs_url = "https://bn-hiring-challenge.fly.dev/jobs.json"

def main():
    """
    Main script for the function
    """
    members = get_api(members_url)
    jobs = get_api(jobs_url)
    
    for candidate in members:
        best_jobs = match_jobs(candidate, jobs.copy())
        print(format_output(candidate["name"], best_jobs))


if __name__ == "__main__":
    main()