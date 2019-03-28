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

import os,re,glob

def parsePS():
    TCNT = 4
    sumlst = [0]*TCNT
    maxlst = [0]*TCNT
    minlst = [9999999999]*TCNT
    avglst = [0]*TCNT

    cnt = 0
    fh = open( prefix + '.ps','r' )
    header = fh.readline().strip()
    headers = header.split('\t')
    for x in fh.xreadlines():
        x = x.strip()
        if not x: continue
        xE = x.split('\t')

        vidx = 0
        for value in xE[1:5]:
            sumlst[vidx] += float(value)
            if float(value) > maxlst[vidx]: maxlst[vidx] = float(value)
            if float(value) < minlst[vidx]: minlst[vidx] = float(value)
            vidx += 1

        cnt += 1

    sidx = 0
    for svalue in sumlst:
        avglst[sidx] = round( float(sumlst[sidx]) / cnt, 1 )
        sidx += 1

    for idx in range( TCNT ):
        print '\t'.join([headers[idx+1],str(sumlst[idx]),str(maxlst[idx]),str(minlst[idx]),str(avglst[idx]),str(cnt)])

def parseIostat():
    TCNT = 5
    sumlst = [0]*TCNT
    maxlst = [0]*TCNT
    minlst = [9999999999]*TCNT
    avglst = [0]*TCNT

    cnt = 0
    fh = open( prefix + '.iostat','r' )
    header = fh.readline().strip()
    headers = header.split('\t')
    for x in fh.xreadlines():
        x = x.strip()
        if not x: continue
        xE = x.split()

        vidx = 0
        for value in xE[1:6]:
            sumlst[vidx] += float(value)
            if float(value) > maxlst[vidx]: maxlst[vidx] = float(value)
            if float(value) < minlst[vidx]: minlst[vidx] = float(value)
            vidx += 1

        cnt += 1

    sidx = 0
    for svalue in sumlst:
        avglst[sidx] = round( float(sumlst[sidx]) / cnt, 1 )
        sidx += 1

    for idx in range( TCNT ):
        print '\t'.join([headers[idx+1],str(sumlst[idx]),str(maxlst[idx]),str(minlst[idx]),str(avglst[idx]),str(cnt)])
    
def parseIostatX():
    TCNT = 13
    sumlst = [0]*TCNT
    maxlst = [0]*TCNT
    minlst = [9999999999]*TCNT
    avglst = [0]*TCNT

    cnt = 0
    fh = open( prefix + '.iostatx','r' )
    header = fh.readline().strip()
    headers = header.split('\t')
    for x in fh.xreadlines():
        x = x.strip()
        if not x: continue
        xE = x.split()

        vidx = 0
        for value in xE[1:14]:
            sumlst[vidx] += float(value)
            if float(value) > maxlst[vidx]: maxlst[vidx] = float(value)
            if float(value) < minlst[vidx]: minlst[vidx] = float(value)
            vidx += 1

        cnt += 1

    sidx = 0
    for svalue in sumlst:
        avglst[sidx] = round( float(sumlst[sidx]) / cnt, 1 )
        sidx += 1

    for idx in range( TCNT ):
        print '\t'.join([headers[idx+1],str(sumlst[idx]),str(maxlst[idx]),str(minlst[idx]),str(avglst[idx]),str(cnt)])

def parseBlktraceReadSize():
    TCNT = 1
    sumlst = [0]*TCNT
    maxlst = [0]*TCNT
    minlst = [9999999999]*TCNT
    avglst = [0]*TCNT

    cnt = 0
    fh = open( prefix + '.read.blktrace','r' )
    header = 'Sector\tReadSize'
    headers = header.split('\t')
    for x in fh.xreadlines():
        x = x.strip()
        if not x: continue
        xE = x.split()

        vidx = 0
        for value in xE[1:2]:
            sumlst[vidx] += float(value)
            if float(value) > maxlst[vidx]: maxlst[vidx] = float(value)
            if float(value) < minlst[vidx]: minlst[vidx] = float(value)
            vidx += 1

        cnt += 1

    sidx = 0
    for svalue in sumlst:
        avglst[sidx] = round( float(sumlst[sidx]) / cnt, 1 )
        sidx += 1

    for idx in range( TCNT ):
        print '\t'.join([headers[idx+1],str(sumlst[idx]),str(maxlst[idx]),str(minlst[idx]),str(avglst[idx]),str(cnt)])

def parseBlktraceWriteSize():
    TCNT = 1
    sumlst = [0]*TCNT
    maxlst = [0]*TCNT
    minlst = [9999999999]*TCNT
    avglst = [0]*TCNT

    cnt = 0
    fh = open( prefix + '.write.blktrace','r' )
    header = 'Sector\tWrtnSize'
    headers = header.split('\t')
    for x in fh.xreadlines():
        x = x.strip()
        if not x: continue
        xE = x.split()

        vidx = 0
        for value in xE[1:2]:
            sumlst[vidx] += float(value)
            if float(value) > maxlst[vidx]: maxlst[vidx] = float(value)
            if float(value) < minlst[vidx]: minlst[vidx] = float(value)
            vidx += 1

        cnt += 1

    sidx = 0
    for svalue in sumlst:
        avglst[sidx] = round( float(sumlst[sidx]) / cnt, 1 )
        sidx += 1

    for idx in range( TCNT ):
        print '\t'.join([headers[idx+1],str(sumlst[idx]),str(maxlst[idx]),str(minlst[idx]),str(avglst[idx]),str(cnt)])

if __name__=='__main__':
    arguments()

    print '\t'.join(['item','sum','max','min','avg','cnt'])
    parsePS()
    parseIostat()
    parseIostatX()
    parseBlktraceReadSize()
    parseBlktraceWriteSize()

