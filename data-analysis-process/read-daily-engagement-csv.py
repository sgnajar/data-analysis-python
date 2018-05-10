import unicodecsv


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

# print (enrollments[0])
# print (dailyEngagement[0])
# print (projectSubmissions[0])
