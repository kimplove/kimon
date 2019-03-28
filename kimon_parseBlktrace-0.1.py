#!/usr/bin/python

prefix = 'kimon-out'

import argparse
def arguments():
    global prefix
    parser = argparse.ArgumentParser()
    parser.add_argument( "--prefix", "-p", type=str, default=prefix, \
            help="output prefix" )
    args = parser.parse_args()

    if args.prefix: prefix = args.prefix

import os,re,glob, operator

def parseBlktraceSector( filename ):

    reqSizeDic = {}

    fh = open( filename,'r' )

    sectorCnt = 0
    prsector = -1
    preReqSize = -1
    contReqSize = 0
    for x in fh.xreadlines():
        x = x.strip()
        if not x: continue
        xE = x.split()

        sector, reqsize = xE
        if prsector == int(sector):
            prsector = int(sector) + int(reqsize)/512
            contReqSize += int(preReqSize)
            if unitdic.has_key( preReqSize/1024 ): unitdic[preReqSize/1024] += 1
            else: unitdic[preReqSize/1024] = 1
            preReqSize = int(reqsize)
            sectorCnt += 1
            continue
        elif sectorCnt >= 1:

            contReqSize += int(reqsize)
            if unitdic.has_key(int(reqsize)/1024 ): unitdic[int(reqsize)/1024] += 1
            else: unitdic[int(reqsize)/1024] = 1

#            print contReqSize, contReqSize / 1024, 'kb', sectorCnt, unitdic
            contReqSizeKb = contReqSize / 1024
            if reqSizeDic.has_key( contReqSizeKb ): reqSizeDic[contReqSizeKb] += 1 
            else: reqSizeDic[contReqSizeKb] = 1

        contReqSize = 0
        unitdic = {}
        prsector = int(sector) + int(reqsize)/512
        preReqSize = int(reqsize)
        sectorCnt = 0
    if sectorCnt >= 1:

#        print contReqSize, contReqSize / 1024, 'kb', sectorCnt, unitdic
        contReqSizeKb = contReqSize / 1024
        if reqSizeDic.has_key( contReqSizeKb ): reqSizeDic[contReqSizeKb] += 1 
        else: reqSizeDic[contReqSizeKb] = 1
    reqSizeTp = sorted( reqSizeDic.items(), key=operator.itemgetter(0))
#    print reqSizeTp
    
    for rs in reqSizeTp[::-1]:
        print str(rs[0])+'\t'+str(rs[1])

def parseBlktraceRequestSize( filename ):
    unitReqSizeDic = {}
    fh = open( filename,'r' )

    for x in fh.xreadlines():
        x = x.strip()
        if not x: continue
        xE = x.split()

        sector, reqsize = xE
        reqsize = int(reqsize) / 1024
        if unitReqSizeDic.has_key(reqsize): unitReqSizeDic[reqsize] += 1
        else: unitReqSizeDic[reqsize] = 1

    unitReqSizeTp = sorted( unitReqSizeDic.items(), key=operator.itemgetter(1))

    for rs in unitReqSizeTp[::-1]:
        print str(rs[0])+'\t'+str(rs[1])

if __name__=='__main__':
    arguments()

    print "ReadSize(KB)\tCount"
    readfile = prefix + '.read.blktrace'
    parseBlktraceSector( readfile )

    print "\nWritesize(KB)\tCount"
    writefile = prefix + '.write.blktrace'
    parseBlktraceSector( writefile )

    print "\nReadUnitSize(KB)\tCount"
    readfile = prefix + '.read.blktrace'
    parseBlktraceRequestSize ( readfile )

    print "\nWriteUnitSize(KB)\tCount"
    readfile = prefix + '.write.blktrace'
    parseBlktraceRequestSize ( readfile )

