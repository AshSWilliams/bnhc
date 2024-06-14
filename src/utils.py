"""
Utility functions
"""
import requests

def get_api(url):
    """
    Retrieve data from the test API
    """
    response = requests.get(url)
    return response.json()

def format_output(name, best_jobs):
    """
    Format the output we're showing to the user
    """
    output_string = "Candidate {} should apply for the following job(s):".format(name)
    job_string = " {} in {},"
    for job in best_jobs:
        output_string += job_string.format(job["title"], job["location"])
    return output_string[:-1] # Strip the trailing comma