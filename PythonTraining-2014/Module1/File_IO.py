# Text Data Processing/ File Input/Output Program
# Python Data Analysis-Script 
# Author: Baburao Kamble



file_input = open("test.txt")
# Read everything into single string:
content = file_input.read()
# file.read(20) reads (at most) 20 bytes
print (len(content))
#print content





#or

for line in file_input:
    print(line.strip())   

# At End Of File
file_input.close()


#CSV file:
#import csv library
import csv
#open csv file 
myfile = open('weather.csv', "r")
#read content of file 
reader = csv.reader(myfile)
# iterate over the rows
for row in reader:
    print row,
myfile.close()
