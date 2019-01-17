#!/usr/bin/python

# by Woo-Yeon Kim
# 16-01-2019
# kimon: a process monitoring script
# using ps and iostat

PERIOD = 1
USER = 'wykim'
DEV = 'sdb'
keyFile = 'kimon_process.conf'
output = 'kimon-out'

import os,re,glob,time,argparse,sys

# global
dic_keyValue = {}

# parameter
def arguments():
    global PERIOD, USER, DEV, keyFile, output
    parser = argparse.ArgumentParser()
    parser.add_argument( "--period", "-p", type=int, default=PERIOD, \
            help="monitoring interval seconds" )
    parser.add_argument( "--user", "-u", type=str, default=USER, \
            help="process owner" )
    parser.add_argument( "--disk", "-d", type=str, default=DEV, \
            help="dev name (eg. sdb)")
    parser.add_argument( "--file", "-f", type=str, default=keyFile, \
            help="including process names (multi-lines) with key and value tab-deliminated format \
            (eg. Name<tab>ProcessNameToGrep)" )
    parser.add_argument( "--output", "-o", type=str, \
            help="prefix of output file name" )
    args = parser.parse_args()
#    if not args.user: sys.stderr.write( "User parameter is required\n" )
#    if not args.disk: sys.stderr.write("Disk name parameter is required\n" )
#    if not args.file: sys.stderr.write("File name including process names is required\n" )

    if args.period: PERIOD = args.period
    if args.user: USER = args.user
    if args.disk: DEV = args.disk
    if args.file: keyFile = args.file
    if args.output: output = args.output

# get process name from a file which includes process names with tab-deliminated format
def getProcessName():
    for x in open( keyFile,'r' ).xreadlines():
        x = x.strip()
        xE = x.split()
        if len(xE) < 2: continue
        key = ' '.join( xE[1:] )
        value = xE[0]
        dic_keyValue[ key ] = value

# execute ps command
def grepProcessName():
    result = []
    for key in dic_keyValue:
        psaux = os.popen( "\
                ps -ax -o user,%cpu,%mem,vsz,rss,cmd | \
                tr -s [:blank:] | \
                grep '"+USER+"' | \
                grep -i '"+key+"' | grep -v grep\
                " ).read()
        psaux = psaux.strip()
        if not( psaux ): continue
        cpuper = 0.0
        memper = 0.0
        vsz = 0
        rss = 0
        cmd = []

        for oneps in psaux.split('\n'):
            psE = oneps.split()
            cpuper += float(psE[1])
            memper += float(psE[2])
            vsz += int(psE[3])
            rss += int(psE[4])
            mstart = re.search( key, ' '.join(psE[5:]) ).start()
            mend = re.search( key, ' '.join(psE[5:]) ).end()
            cmd.append(' '.join(psE[5:])[mstart-5:mstart]+"XXX"+' '.join(psE[5:])[mend:mend+5])

        result = [ key, str(round(cpuper,2)), str(round(memper,2)), str(vsz), str(rss) ]#, ','.join(cmd)
        break
    return result

# execute iostat with default option
def iostat():
    header = ['dev','tps','kbreads','kbwrtns','kbread','kbwrtn']
    io1name = output + ".iostat"
    rfh = open( io1name,'w' )
    rfh.write( '\t'.join(header) + '\n' )
    rfh.close()
    os.system( "iostat -d /dev/"+DEV+" -y "+str(PERIOD)+" | grep "+DEV+" >> "+io1name )

# execute iostat with -x option
def iostatx():
    header = ['dev','rrqms','wrqms','rs','ws','rkbs','wkbs','avgrqsz','avgqusz','await','rawait','wawait','svctm','util']
    io2name = output + ".iostatx"
    rfh = open( io2name,'w' )
    rfh.write( '\t'.join(header) + '\n' )
    rfh.close()
    os.system( "iostat -d /dev/"+DEV+" -xy "+str(PERIOD)+" | grep "+DEV+" >> "+io2name )

# main
if __name__=='__main__':

    pid = os.fork()
    
    #child process
    if pid == 0:
        pid = os.fork()

        #grandchild process
        if pid == 0:
            iostat()
        else:
            iostatx()
    
    else:
        arguments()
        getProcessName()

        outname = output + '.ps'
        rfh = open( outname,'w' )

        header = ['key','cpuper','memper','vsz','rss']
        print >> rfh, '\t'.join(header)

        while( 1 ):
            printline = []
            printline = grepProcessName()
            if not printline: break
            print >> rfh, '\t'.join(printline)
            time.sleep( PERIOD )

        os.system( "killall -u "+USER+" iostat" )
        
        rfh.close()

