__author__ = 'starsdeep'
import os,sys
from collections import defaultdict
from coursera_requests import getCourseraCategories, getCourseraCourses, getCourseraSessions
curPath = os.path.abspath(os.path.split(os.path.realpath(__file__))[0])
sys.path.append(curPath + "/../../common/python/")
from WriteTool import WriteTool

def alignCoursera(is_write=False):
    categories = getCourseraCategories(is_load=True,is_write=False)
    courses = getCourseraCourses(is_load=True,is_write=False)
    sessions = getCourseraSessions(is_load=True,is_write=False)

    id_catename_dict = dict()
    #session id
    id_session_dict = defaultdict(str)

    for cat in categories['elements']:
        id_catename_dict[cat['id']] = cat['name']
    for session in sessions['elements']:
        if 'homeLink' in session:
            id_session_dict[session['id']] += session['name']+'#'+session['homeLink'] 

    records = list()
    for course in courses['elements']:
        record = dict()
        record['name'] = course['name']
        record['language'] = course['language']
        record['shortDescription'] = course['shortDescription']
        record['aboutTheCourse'] = course['aboutTheCourse']
        #try
        record['categories'] = ''
        if 'categories' in course['links']:
            cat_ids = course['links']['categories']
            cat_names = [id_catename_dict[i] for i in cat_ids]
            record['categories'] = '#'.join(cat_names)
        
        session_ids = course['links']['sessions']
        session_infos = [id_session_dict[i] for i in session_ids]
        record['sessions'] = ';'.join(session_infos)
        
        records.append(record)
    
    print "categories: " + str(len(id_catename_dict))
    print 'sessions: ' + str(len(id_session_dict))
    print 'courses: ' + str(len(records))

    return records
     

if __name__ == '__main__':
    records = alignCoursera(is_write=True)
    WriteTool.write_dict_list(records,'../data/coursera_records.txt')




