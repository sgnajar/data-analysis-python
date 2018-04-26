# By: Sasan Najar
# Email: sasangnajar@gmail.com


# Function of this code is to read CSV files in Python
# You need to install unicodecsv library on your machine

import unicodecsv

# enrollments = []
# inFile = open('enrollments.csv', 'rb')
# reader = unicodecsv.DictReader(inFile)
# for row in reader:
#     enrollments.append(row)
# inFile.close()

with open('enrollments.csv', 'rb') as inFile:
    reader = unicodecsv.DictReader(inFile)
    enrollments = list(reader)

print(enrollments[0])
