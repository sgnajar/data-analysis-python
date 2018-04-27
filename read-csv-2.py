# By Sasan Najar -- sasangnajar@gmail.com

import unicodecsv
from datetime import datetime as dt
from collections import defaultdict
import numpy as np

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

# print (len(enrollments))
unique_enrolled_students = get_unique_students(enrollments)
# print (len(unique_enrolled_students))
# print (len(dailyEngagement))
unique_engagement_students = get_unique_students(dailyEngagement)
# print (len(unique_engagement_students))
# print(len(projectSubmissions))
unique_project_submitters = get_unique_students(projectSubmissions)
# print(len(unique_project_submitters))

# check if the 'acct' column changed by 'account_key'
# print (dailyEngagement[0]['account_key'])

num_problem_student = 0

for enrollment in enrollments:
    student = enrollment['account_key']
    if student not in unique_engagement_students:
        # print (enrollment)
        break

for enrollment in enrollments:
    student = enrollment['account_key']
    if student not in unique_engagement_students \
    and enrollment['join_date'] != enrollment['cancel_date']:
        num_problem_student += 1
        # print (enrollment)

# print (num_problem_student) # these are the Udacity test accounts

## Fixing this problem by deleting the Udacity test accounts
udacity_test_accounts = set()
for enrollment in enrollments:
    if enrollment['is_udacity']:
        udacity_test_accounts.add(enrollment['account_key'])

# print (len(udacity_test_accounts))

def remove_udacity_accounts(data):
    non_udacity_data = []
    for data_point in data:
        if data_point['account_key'] not in udacity_test_accounts:
            non_udacity_data.append(data_point)
    return non_udacity_data

non_udacity_enrollments = remove_udacity_accounts(enrollments)
non_udacity_engagement = remove_udacity_accounts(dailyEngagement)
non_udacity_submissions = remove_udacity_accounts(projectSubmissions)

# print (len(non_udacity_enrollments))
# print (len(non_udacity_engagement))
# print (len(non_udacity_submissions))

## Phase 2: Data Exploration
## Create a "paid_students" dictionary of students who either:
# have not canceled yet (days_to_cancel is None)
# stayed enrolled more than 7 days (days_to_cancel > 7)
# keys: account_key Values: enrollment date

paid_students = {}
for enrollment in non_udacity_enrollments:
    if not enrollment['is_canceled'] or enrollment['days_to_cancel'] > 7:
        account_key = enrollment['account_key']
        enrollment_date = enrollment['join_date']
        paid_students[account_key] = enrollment_date
# print(len(paid_students))

# Takes a student's join date and the date of a specific engagement record,
# and returns True if that engagement record happened within one week,
# of the student joining

def within_one_week(join_date, engagement_date):
    time_delta = engagement_date - join_date
    return time_delta.days < 7

## Create a list of engagement records containing only data,
## for paid students during their first week.

def remove_free_trial_cancels(data):
    new_data = []
    for data_point in data:
        if data_point['account_key'] in paid_students:
            new_data.append(data_point)
    return new_data

paid_enrollments = remove_free_trial_cancels(non_udacity_enrollments)
paid_engagement = remove_free_trial_cancels(non_udacity_engagement)
paid_submissions = remove_free_trial_cancels(non_udacity_submissions)

# print (len(paid_enrollments))
# print (len(paid_engagement))
# print (len(paid_submissions))

paid_engagement_in_first_week = []

for engagement_record in paid_engagement:
    account_key = engagement_record['account_key']
    join_date = paid_students[account_key]
    engagement_record_date = engagement_record['utc_date']

    if within_one_week(join_date, engagement_record_date):
        paid_engagement_in_first_week.append(engagement_record)

# print(len(paid_engagement_in_first_week))

# another task: average min a student spent in classroom

engagement_by_account = defaultdict(list)
for engagement_record in paid_engagement_in_first_week:
    account_key = engagement_record['account_key']
    engagement_by_account[account_key].append(engagement_record)

total_minutes_by_account = {}

for account_key, engagement_for_student in engagement_by_account.items():
    total_minutes = 0
    for engagement_record in engagement_for_student:
        total_minutes += engagement_record['total_minutes_visited']
    total_minutes_by_account[account_key] = total_minutes

total_minutes_temp = total_minutes_by_account.values()
total_minutes = list(total_minutes_temp)

# print (np.mean(total_minutes))
# print (np.std(total_minutes))
# print (np.max(total_minutes))
# print (np.min(total_minutes))

student_with_max_minutes = None
max_minutes = 0

for student, total_minutes in total_minutes_by_account.items():
    if total_minutes > max_minutes:
        max_minutes = total_minutes
        student_with_max_minutes = student

# print(max_minutes)
