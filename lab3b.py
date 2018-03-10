#!/usr/bin/python


#get the information
#make the data structure
#analyze data structure

import csv
import sys

def main():
    if len(sys.argv) != 2:
        print("Wrong number of arguments")
        sys.exit()
    
    csvFile = []
    rowArray = []

    with open(sys.argv[1], 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if (row[0] == "INDIRECT"):
                print row        
            if (row[0] == "INODE"):
                print row

if __name__ == "__main__":
    main()
