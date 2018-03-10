#!/usr/bin/python

import csv

if __name__ == "__main__":
    csvFile=[]
    rowArray = []

    with open("trivial.csv", "rb") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if (row[0] == "INDIRECT"):
                print row
