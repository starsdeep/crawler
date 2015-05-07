import json
import urllib
import requests

def getCourses():
    response =requests.get('https://udacity.com/public-api/v0/courses')
    json_response = response.json()
    records = list()
    for course in json_response['courses']:
        record = dict()
        record['name'] = course['title']
        record['homepage'] = course['homepage']
        record['language'] = 'en'
        record['shortDescription'] = course['short_summary']
        record['description'] = course['summary']
        record['lectures'] = course['syllabus']
        records.append(record)
    return records

if __name__ == '__main__':
    records = getCourses()
    with open('./data/udacity_records.txt','w') as outfile:
        json.dump(records, outfile)

