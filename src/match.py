"""
Functions for matching candidates to jobs
"""

def match_jobs(candidate, jobs):
    """
    Match members with jobs.
    """
    # First filter out the jobs which don't match the candidate's
    # desired location
    filtered_jobs = filter_jobs_by_location(candidate, jobs)
    # Then rank the jobs by how well they match the candidate's bio
    filtered_job_titles = [job["title"].lower() for job in filtered_jobs]
    job_ranking = rank_jobs(candidate["bio"], filtered_job_titles)
    # Sort the job_ranking dictionary by values in descending order
    sorted_jobs = sorted(job_ranking.items(), key=lambda x: x[1], reverse=True)

    # Get the job titles with the highest value
    highest_value = sorted_jobs[0][1]
    highest_value_jobs = [job for job in filtered_jobs if job["title"].lower() in job_ranking and job_ranking[job["title"].lower()] == highest_value]

    # Return the jobs with the highest value
    return highest_value_jobs


def filter_jobs_by_location(candidate, jobs):
    """
    Filter jobs by location
    """
    job_locations = set([job["location"].lower() for job in jobs])
    locations = get_candidate_location(candidate, job_locations)
    for job in jobs:
        if job["location"].lower() not in locations:
            jobs.remove(job)
    return jobs


def get_candidate_location(candidate, job_locations):
    """
    Figure out what location the candidate wishes to work in
    """
    ignore_next_loc = False
    prioritise_next_loc = False
    locations = []
    bio = candidate["bio"].split()
    for token in bio:
        # Sanitise the token
        token = token.lower().strip(",. ")
        if token == "outside":
            # Candidate does not want to work here
            ignore_next_loc = True
        if token == "relocate":
            # Candidate wants to relocate here
            prioritise_next_loc = True
        if token in job_locations:
            if ignore_next_loc:
                ignore_next_loc = False
                job_locations.remove(token)
                continue
            elif prioritise_next_loc:
                locations = [token]
                break
            else:
                locations.append(token)
    if not locations:
        # Candidate did not specify a location
        locations = list(job_locations)
    return locations
    

def rank_jobs(bio, job_titles):
    """
    Match key words from the bio to given job titles.
    """
    job_matches = {}
    for token in bio.split():
        for title in job_titles:
            # Don't match on short words like "I" or "an"
            # We could require words to match exactly, but then we would miss
            # out on partial matches like "design" for "designer"
            if token.lower() in title and len(token) > 4:
                if title not in job_matches:
                    job_matches[title] = 1
                else:
                    job_matches[title] += 1
    return job_matches