#!/usr/bin/python


#get the information
#make the data structure
#analyze data structure

import csv
import sys

class inodeInfo:
    offsets = -1
    inode = -1
    indirection = -1

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

    freeBlocks = set([])

    #key is the block number                                                                                                                                                
    #value is a list of classes
    allocatedBlocks = {}

    for row in csvFile:
        if (row[0] == "BFREE"):
            freeBlocks.add(int(row[1]))
        if (row[0] == "INODE"):
            offset = 0
            for i in range (12, 27):
                blockNum = int(row[i])
                if (blockNum != 0):
                    if (blockNum < 0 or blockNum > (totalBlocks-1)):
                        if (i < 24):
                            print("INVALID BLOCK {} IN INODE {} AT OFFSET {}".format(blockNum, row[1], offset))
                        if (i == 24):
                            print("INVALID INDIRECT BLOCK {} IN INODE {} AT OFFSET {}".format(blockNum, row[1], offset + 12))
                        if (i == 25):
                            print("INVALID DOUBLE INDIRECT BLOCK {} IN INODE {} AT OFFSET {}".format(blockNum, row[1], offset + 12 + 256))
                        if (i == 26):
                            print("INVALID TRIPLE INDIRECT BLOCK {} IN INODE {} AT OFFSET {}".format(blockNum, row[1], offset + 12 + 256 + 256))
                    if (blockNum < endOfInodeTable):
                        print ("RESERVED BLOCK {} IN INODE {} AT OFFSET {}".format(blockNum, row[1], blockNum*blockSize))
                    else:
                        newInodeInfo = inodeInfo()
                        newInodeInfo.inode = int(row[1])
                        newInodeInfo.indirection = 0
                        newInodeInfo.offsets = 12-i
                        if (allocatedBlocks.has_key(blockNum) == False):
                            allocatedBlocks[blockNum] = [newInodeInfo]
                        else:
                            allocatedBlocks[blockNum].append(newInodeInfo)
                    offset = offset + 1
        if (row[0] == "INDIRECT"):
            blockNum = int(row[4])
            if (blockNum < 0 or blockNum > (totalBlocks-1)):
                if (row[2] == "1"):
                    print("INVALID INDIRECT BLOCK {} IN INODE {} AT OFFSET {}".format(blockNum, row[1], blockNum*blockSize))
                if (row[2] == "2"):
                    print("INVALID DOUBLE INDIRECT BLOCK {} IN INODE {} AT OFFSET {}".format(blockNum, row[1], blockNum*blockSize))
                if (row[2] == "3"):
                    print("INVALID TRIPLE INDIRECT BLOCK {} IN INODE {} AT OFFSET {}".format(blockNum, row[1], blockNum*blockSize))
                continue
            elif (blockNum < endOfInodeTable):
                if (row[2] == "1"):
                    print("RESERVED INDIRECT BLOCK {} IN INODE {} AT OFFSET {}".format(blockNum, row[1], blockNum*blockSize))
                if (row[2] == "2"):
                    print("RESERVED DOUBLE INDIRECT BLOCK {} IN INODE {} AT OFFSET {}".format(blockNum, row[1], blockNum*blockSize))
                if (row[2] == "3"):
                    print("RESERVED TRIPLE INDIRECT BLOCK {} IN INODE {} AT OFFSET {}".format(blockNum, row[1], blockNum*blockSize))
            else:
                indir = int(row[2])
                if (indir == 1):
                    offset = row[3]
                if (indir ==  2):
                    offset = 12+256
                if (indir == 3):
                    offset = 12 + 256 + 256
                newInodeInfo = inodeInfo()
                newInodeInfo.inode = int(row[1])
                newInodeInfo.indirection = indir
                newInodeInfo.offsets = offset
                blockNum = int(row[5])
                if (allocatedBlocks.has_key(blockNum) == False):
                    allocatedBlocks[blockNum] = [newInodeInfo]
                else:
                    allocatedBlocks[blockNum].append(newInodeInfo)

    # allocated and unreferenced blocks
    for i in range(totalBlocks):
        if i in freeBlocks and allocatedBlocks.has_key(i):
            print("ALLOCATED BLOCK {} ON FREELIST".format(i);
        if i not in freeBlocks and allocatedBlocks.has_key(i) == False:
            print("UNREFERENCED BLOCK {}".format(i));
            
                 
    #checking for duplicates
    for i in range(startOfDataBlocks, totalBlocks):
        if (allocatedBlocks.has_key(i) == True):
            if (len(allocatedBlocks[i]) > 1):
                for j in range(len(allocatedBlocks[i])):
                    print "DUPLICATE"
                    indir = allocatedBlocks[i][j].indirection
                    if (indir == 1):
                        print "INDIRECT"
                    if (indir == 2):
                        print "DOUBLE INDIRECT"
                    if (indir == 3):
                        print "TRIPLE INDIRECT"
                    print("BLOCK {} IN INODE {} AT OFFSET {}".format(i, allocatedBlocks[i][j].inode, allocatedBlocks[i][j].offsets))

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
