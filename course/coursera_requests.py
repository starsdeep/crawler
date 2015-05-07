import requests
import json
import sys

def getCourseraCategories(is_load=False,is_write=False):
    filename = "../data/coursera/categories.json"
    if is_load:
        return json.load(open(filename))

    # Define fields to be retrieved from Coursera API
    fields = ["name", "shortName", "id", "description"]
    link = "https://api.coursera.org/api/catalog.v1/categories?fields="
    link = link + ','.join(fields)

    # Retrieve categories, convert to JSON, format
    categories = requests.get(link)
    categories = categories.json()
    # categories = categories["elements"]

    # Write to file
    if(is_write):
        with open(filename, 'w') as outfile:
            json.dump(categories, outfile, indent=4)
    return categories

def getCourseraCourses(is_load=False,is_write=False):
    filename = "../data/coursera/courses.json"
    if is_load:
        return json.load(open(filename))
    
    # Define fields to be retrieved from Coursera API
    fields = [  "name",
                "language",
                "shortDescription",
                "aboutTheCourse"]                
    link = "https://api.coursera.org/api/catalog.v1/courses?fields="
    link = link + ','.join(fields)
    link = link + "&includes=categories,universities,sessions,instructors";
    
    # Retrieve courses, convert to JSON, format
    courses = requests.get(link)
    courses = courses.json()
    #courses = courses["elements"]

    # Write to file
    with open(filename, 'w') as outfile:
        json.dump(courses, outfile, indent=4)
    return courses 

def getCourseraInstructors():
    # Define fields to be retrieved from Coursera API
    fields = ["fullName", "id"]
    link = "https://api.coursera.org/api/catalog.v1/instructors?fields="
    link = link + ','.join(fields)
    link = link + "&includes=universities"

    # Retrieve categories, convert to JSON, format
    instructors = requests.get(link)
    instructors = instructors.json()
    # categories = categories["elements"]

    # Write to file
    filename = "../data/coursera/instructors.json"
    with open(filename, 'w') as outfile:
        json.dump(instructors, outfile, indent=4)
    

def getCourseraSessions(is_load=False,is_write=False):
    filename = "../data/coursera/sessions.json"
    if is_load:
        return json.load(open(filename))
    # Define fields to be retrieved from Coursera API
    fields = ["homeLink",
              "courseId",
              "name"]
    link = "https://api.coursera.org/api/catalog.v1/sessions?fields="
    link = link + ','.join(fields)

    # Retrieve sessions, convert to JSON, format
    sessions = requests.get(link)
    sessions = sessions.json()
    # sessions = sessions["elements"]

    # Write to file
    if is_write:
        with open(filename, 'w') as outfile:
            json.dump(sessions, outfile, indent=4)
    return sessions

def getCourseraUniversities():
    # Define fields to be retrieved from Coursera API
    fields = ["name", "id", "website"]
    link = "https://api.coursera.org/api/catalog.v1/universities?fields="
    link = link + ','.join(fields)

    # Retrieve universities, convert to JSON, format
    universities = requests.get(link)
    universities = universities.json()
    # universities = universities["elements"]

    # Write to file
    filename = "../data/coursera/universities.json"
    with open(filename, 'w') as outfile:
        json.dump(universities, outfile, indent=4)
