# Bright Network Hiring Challenge
This repository contains a solution to the Bright Network Hiring Challenge.

## Running the code
This project is written in Python and makes use of Poetry.
First install dependencies with `poetry install` and then run the code with `poetry run python main.py`
You can also run the code manually, just make sure you install `requests` first.
Run the (very basic) unit tests with `poetry run pytest`.

## Approach taken
The code follows a two-step algorithm for matching candidates to jobs.
1. The candidate's bio is read to determine what location(s) they are looking to work in. Jobs outside of this area are excluded.
2. The candidate's bio is compared word-by-word to the title of the remaining jobs, and the job with the best match is returned.

### Location parsing
This code takes a naive approach based on the provided format of the candidate bios:
1. Determine what location(s) we have jobs in by reading the job listings.
2. Search through the bio for one of three sorts of tokens:
  a. A token which indicates that the candidate does *not* want to work in the following location, here just "outside".
  b. A token which indicates that the candidate *only* wants to work in the following location and hence all others should be ignored, here just "relocate".
  c. A token matching one of the locations.
3. If the token is a location:
  a. If the candidate has expressed a desire to only work in this location, stop iterating and return only that location
  b. If the candidate does not want to work in this location, remove it from the list of job locations and continue
  c. Otherwise, simply add it to the list.
4. If we get to the end and have not added any locations to the list, assume the candidate has no further preference and return all non-excluded locations.
5. Remove any jobs from the list which are not in a location acceptable to the candidate.

### Job description parsing
This step is more simple:
1. Iterate through the candidate's bio word by word and compare each word to the description.
  a. We ignore words shorter than 5 characters to avoid matching on words like "a".
2. If there word is contained within the description, give that job a point.
3. At the end, return all jobs with the highest number of points to the user.

## Improvements
### NLP / ML
This task is a good fit for using either a natural language processor or a machine learning model. However the former is too complex for the scope of this exercise and making use of an AI for this task feels a little bit like cheating.
I spent some time investigating (spaCy)[https://spacy.io/usage/] which offers powerful NLP tools in python; if I were implementing this as part of a work task I would probably try to use it to simplify the task of parsing bios. Python also has powerful ML/AI tooling, though I didn't investigate them here.

### Matching words in job descriptions
It works for the given data, but simply looking for substrings in the job description is fragile. "Design" in Hassan's bio matches "designer" but would not work the other way around, for example. We could make use of an NLP to determine semantic closeness of words, rather than looking for exact matches - so someone looking for a job in "user experience" would hopefully not miss out on a role looking for "UX". 
I also note that this system is open to exploitation; when used to scan CVs it incentivises candidates to fill their CVs with key words which they know the algorithm will be scanning for and making the scanning algorithm useless. Asking an AI to scan the CV runs into similar problems.

### Determining job locations
spaCy can identify "entities" in a text which refer to a proper noun; this can be used to spot locations (GPEs) without needing a pre-populated list. Here it is less useful because we are not interested in locations which aren't mentioned in a job advert.
If continuing with this naive approach it would be worth putting further thought into how to deal with multiple named locations (and cities with multiple words in their name) and locations where a candidate does not want to be. In addition to "outside" we could search for phrases such as "not in", "anywhere but", and so on. It's also possible that some candidates might be willing to move, for example Joe states he is from London, but it doesn't necessarily follow that he wants only to work there.

### Don't give candidates free-form bios
It might be easier to process the data if the candidates provide a list of locations and a list of jobs they're interested in rather than allowing them to present this information in arbitrary ways. They could still have a bio, but it would be easier to determine where Daisy wanted to work if her data looked like
```
    {
        "name": "Daisy",
        "bio": "I'm a software developer currently in Edinburgh but looking to relocate to London",
        "preferred_locations": "london",
        "job_titles": "software engineer", "software developer"
    }
```
