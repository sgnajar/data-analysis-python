import unicodecsv
from datetime import datetime as dt


# Read in the data from daily_engagement.csv and project_submissions.csv
# and storre the results in the dailyEngagement and projectSubmissions variables.
# Then look at the first row of each table

def read_csv(filename):
    with open(filename, 'rb') as inFile:
        reader = unicodecsv.DictReader(inFile)
        return list(reader)

enrollments = read_csv('enrollments.csv')
dailyEngagement = read_csv('daily_engagement.csv')
projectSubmissions = read_csv('project_submissions.csv')

# takes a date as a string and returns a Python datetime objectself.
# if there is no date given,return None
def parse_date(date):
    if date == '':
        return None
    else:
        return dt.strptime(date, '%Y-%m-%d')

# print (enrollments[0])
# print (dailyEngagement[0])
# print (projectSubmissions[0])

def parse_maybe_int(i):
    if i == '':
        return None
    else:
        return int(i)

# clean up the data types in the enrollment
for enrollment in enrollments:
    enrollment['cancel_date'] = parse_date(enrollment['cancel_date'])
    enrollment['days_to_cancel'] = parse_maybe_int(enrollment['days_to_cancel'])
    enrollment['is_canceled'] = enrollment['is_canceled'] == 'True'
    enrollment['is_udacity'] = enrollment['is_udacity'] == 'True'
    enrollment['join_date'] = parse_date(enrollment['join_date'])

# print (enrollments[0])

# clean up the data types in the engagement table
for engagement_record in dailyEngagement:
    engagement_record['lessons_completed'] = int(float(engagement_record['lessons_completed']))
    engagement_record['num_courses_visited'] = int(float(engagement_record['num_courses_visited']))
    engagement_record['projects_completed'] = int(float(engagement_record['projects_completed']))
    engagement_record['total_minutes_visited'] = float(engagement_record['total_minutes_visited'])
    engagement_record['utc_date'] = parse_date(engagement_record['utc_date'])
    engagement_record['account_key'] = engagement_record['acct']
    del[engagement_record['acct']]
# print (dailyEngagement[0])

# clean up the data types in the submissons table
for submisson in projectSubmissions:
    submisson['completion_date'] = parse_date(submisson['completion_date'])
    submisson['creation_date'] = parse_date(submisson['creation_date'])

# print (projectSubmissions[0])


def get_unique_students(data):
    unique_students = set()
    for data_point in data:
        unique_students.add(data_point['account_key'])
    return unique_students

print (len(enrollments))
unique_enrolled_students = get_unique_students(enrollments)
print (len(unique_enrolled_students))
print (len(dailyEngagement))
unique_engagement_students = get_unique_students(dailyEngagement)
print (len(unique_engagement_students))
print(len(projectSubmissions))
unique_project_submitters = get_unique_students(projectSubmissions)
print(len(unique_project_submitters))

# check if the 'acct' column changed by 'account_key'
print (dailyEngagement[0]['account_key'])
