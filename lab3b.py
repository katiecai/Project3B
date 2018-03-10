#!/usr/bin/python


#get the information
#make the data structure
#analyze data structure

import csv
import sys

def block_consistency(csvFile):
    #first determine legal blocks
    inodeSize = -1
    totalBlocks = -1
    totalInodes = -1
    blockSize = -1;

    bitMap = -1
    inodeMap = -1
    inodeTable = -1;
    endOfInodeTable = -1;

    for row in csvFile:
        if (row[0] == "SUPERBLOCK"):
            totalBlocks = int(row[1])
            totalInodes = int(row[2])
            blockSize = int(row[3])
            inodeSize = int(row[4])
        if (row[0] == "GROUP"):
            bitMap = int(row[6])
            inodeMap = int(row[7])
            inodeTable = int(row[8])

    startOfDataBlocks = inodeTable + (totalInodes * inodeSize / blockSize)
    print("total blocks: {}".format(totalBlocks))

    # find invalid and reserved blocks
    for row in csvFile:
        if (row[0] == "INODE"):
            for i in range (12, 23):
                blockNum = int(row[i])
                if (blockNum != 0):
                    print(blockNum)
                    if (blockNum < 0 or blockNum > (totalBlocks-1)):
                        print("INVALID BLOCK {} IN INODE {} AT OFFSET {}".format(blockNum, row[1], blockNum*blockSize))
                    if (blockNum < endOfInodeTable):
                        print ("RESERVED BLOCK {} IN INODE {} AT OFFSET {}".format(blockNum, row[1], blockNum*blockSize))
        if (row[0] == "INDIRECT"):
            blockNum = int(row[4])
            print(blockNum)
            if (blockNum < 0 or blockNum > (totalBlocks-1)):
                if (row[2] == "1"):
                    print("INVALID INDIRECT BLOCK {} IN INODE {} AT OFFSET {}".format(blockNum, row[1], blockNum*blockSize))
                if (row[2] == "2"):
                    print("INVALID DOUBLE INDIRECT BLOCK {} IN INODE {} AT OFFSET {}".format(blockNum, row[1], blockNum*blockSize))
                if (row[2] == "3"):
                    print("INVALID TRIPLE INDIRECT BLOCK {} IN INODE {} AT OFFSET {}".format(blockNum, row[1], blockNum*blockSize))
            if (blockNum < endOfInodeTable):
                if (row[2] == "1"):
                    print("RESERVED INDIRECT BLOCK {} IN INODE {} AT OFFSET {}".format(blockNum, row[1], blockNum*blockSize))
                if (row[2] == "2"):
                    print("RESERVED DOUBLE INDIRECT BLOCK {} IN INODE {} AT OFFSET {}".format(blockNum, row[1], blockNum*blockSize))
                if (row[2] == "3"):
                    print("RESERVED DOUBLE INDIRECT BLOCK {} IN INODE {} AT OFFSET {}".format(blockNum, row[1], blockNum*blockSize))
                
def main():
    if len(sys.argv) != 2:
        print("Wrong number of arguments")
        sys.exit()
    
    csvFile = []

    with open(sys.argv[1], 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            csvFile.append(row)
        
    block_consistency(csvFile)

if __name__ == "__main__":
    main()
