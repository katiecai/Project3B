#!/usr/bin/python

import csv
import sys

def main():
    if sys.argc != 2:
        print("Wrong number of arguments")
        sys.exit()
    
    csvFile = []
    rowArray = []

    with open(sys.argv[1], 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if (row[0] == "INDIRECT"):
                print row        
