# FAITH GROUP PROJECT
# concierge software

import datetime
import time
from numpy import *
import csv
import os

os.system("clear")
set_printoptions(precision=0)
set_printoptions(suppress=1)

dformat = "%a %b %d %H:%M:%S %Y"

dtfun = lambda d: datetime.datetime(*tuple(d)) # give a list and make a datetime object
drfun = lambda m: datetime.timedelta(0, m*60) # give number of minutes and make timedelta


adict = {} #check-in time
bdict = {} #check-out time
sdict = {} #services


gfname = 'guestlist.csv'
sfname = 'servicelist.csv'


def readguestlist():
    ''' read guestlist and update dictionaries
    '''
    lst = list(csv.reader(open(gfname)))
    for guest in lst:
        nbr = int(guest[0])
        start = [int(i) for i in guest[1:6]]
        end = [int(i) for i in guest[6:]]
            
        adict[nbr] = datetime.datetime(*start)
        bdict[nbr] = datetime.datetime(*end)



def checkin(nbr, start, end):
    '''Check-in a new client
        IN: nbr = id number
            start = beginning of stay [year, month, day, hour, min]
            end = end of stay [year, month, day, hour, min] 
    '''
        
    # create the line to add the file guestlist.csv and save it    
    newline = concatenate(([nbr],start, end))   # new line  
    oldstuff = genfromtxt(gfname, delimiter=',') # array with old clients
    
    # save new list of guests.
    if len(oldstuff) == 0: # if this is the first guest write it this way
        fp = open(gfname, 'w')
        fp.write(', '.join([str(i) for i in newline]))
        fp.close()

    else: # if we already have some other guests add the newline to others
        newstuff = vstack((oldstuff, newline))
        savetxt(gfname, newstuff,fmt='%i',delimiter=',')
    
    # update adict, bdict
    readguestlist()


def stay(nbr):
    ''' Small function to print out the start and end of a client's stay
    '''
    if nbr not in adict.keys():
        print 'There is no client with ID #%i'%(nbr)
    else:
        start = adict[nbr]
        end = bdict[nbr]
        print 'guest #%i: %s <==> %s'%(nbr,start.ctime(),end.ctime())



def readservicelist():
    ''' read guestlist and update dictionary
    '''
    lst = list(csv.reader(open(sfname)))
    for service in lst:
        nbr = int(service[0])
        servid = int(service[1])
        
        bookingtime = datetime.datetime(*[int(i) for i in service[2:7]])
        
        start = datetime.datetime(*[int(i) for i in service[7:12]])
        dur = datetime.timedelta(int(service[-2]), int(service[-1]))
        
        if nbr not in sdict.keys():
            sdict[nbr] = [[servid,bookingtime, start, dur]]
        else:
            sdict[nbr].append([servid,bookingtime, start,dur])


def isSameDay(d1,d2):
    ''' Check if two dates are the same: same month and same day.'''
    flag = ((d1.month == d2.month) and (d1.day == d2.day))
    return flag


# function to return the times when a service is available
def availtimes(sid,date):
    ''' sid = service ID
        date = datetime object
    '''
    
    if sid > 1:
        lst = []
        for cid in sdict.keys():
            slst = sdict[cid]
            for serv in slst:
                if isSameDay(serv[2],date) and (sid == serv[0]):
                    lst.append(serv[2:])    
        lst = sorted(lst)
    else:
        lst = []
    
    tic = datetime.datetime(*(date.year,date.month,date.day,8,0))
    toc = datetime.datetime(*(date.year,date.month,date.day,20,0))
    
    
    print 'On %s, service ID #%d is open from \n\n'%(date.ctime(),sid),
    print tic.ctime(), ' to ',
    for sv in lst:
        print sv[0].ctime()
        
        endt = sv[0] + sv[1]
        print endt.ctime(),' to ',
    
    if len(lst) == 0:
        print toc.ctime(), ' * OPEN ALL DAY *'
    else:
        print toc.ctime()




# small function to print out the reservations of a client
def getServices(nbr):
    
    if nbr not in sdict.keys():
        print 'Client ID #%i has no Services.'%nbr
    else:
        print ' Client ID #%i has the following reservation(s): '%nbr
        print
        for bk in sdict[nbr]:
            print ' Service ID #%i: %s until %s'%(bk[0], bk[2].ctime(),\
                                                (bk[2] + bk[3]).ctime())



# check overlap
def isOverlapped(nbr,cand,dur):
    ''' check if the client with ID has any other reservation on this 
        day/time
        nbr: client ID
        cand: candidate date
        dur: duration of the service
        
    '''
    slst = sdict[nbr]
    flag = 0
    
    for serv in slst:
        tic = serv[2]
        toc = serv[2]+serv[3]
        
        if ((cand > tic) and (cand < toc)) or \
            (( cand+dur > tic) and (cand+dur < toc)):
            flag = 1 
            return flag
    return flag



# check there is no other reservation of that service for that day/time
def isReserved(sid, cand,dur):
    ''' Check if anyone else has a reservation of the service ID 
        on the candidate day/time
        sid: service ID number 1 to 10
        cand: candidate date
        dur: duration of the service
    '''
    flag = 0
    for cid in sdict.keys():
        slst = sdict[cid]
        for serv in slst:
            if isSameDay(cand, serv[2]) and (serv[0] == sid):
                tic = serv[2]
                toc = tic + serv[3]
                if ((cand > tic) and (cand < toc)) or \
                    (( cand+dur > tic) and (cand+dur < toc)):
                    flag = 1
                    return flag
    
    return flag

        

def isTimed(cand,dur):
    ''' Check if the proposed reservation start after 8am AND ends
        before 8pm
    '''

    morning = datetime.datetime(*(cand.year,cand.month,cand.day,8,0))
    night = datetime.datetime(*(cand.year,cand.month,cand.day,20,0))


    if (morning <= cand) and ((cand+dur) <= night):
        return 1
    else:
        return 0
        


readguestlist()
readservicelist()


def getAllReservations():
    ''' Print the reservations of all clients
    '''
    
    
    for cl in adict.keys():
        print '+'+'-' * 70+'+'
        getServices(cl)
        print '+'+'-'* 70+'+'
        print



def isPossible(nbr, sid, cand, duration):
    ''' check if a date is possible
    '''
    if nbr in sdict.keys():
        if not isOverlapped(nbr,cand,duration) and \
            not isReserved(sid,cand,duration) and \
            isTimed(cand, dur):
                return 1
        else:
            return 0
    
    else:
        if not isReserved(sid,cand,duration) and \
           isTimed(cand, duration):
            return 1
        else:
            return 0

    

def makeReservation(nbr,sid,bktime, date, duration):
    ''' Make a reservation for a service
    '''
    
    newline = concatenate(([nbr,sid],list(bktime.timetuple())[:5], \
                            list(date.timetuple())[:5], [duration.days, \
                            duration.seconds]))
    
    oldstuff = genfromtxt(sfname, delimiter=',') # array with old services

    # save new list of guests.
    if len(oldstuff) == 0: # if this is the first guest write it this way
        fp = open(sfname, 'w')
        fp.write(', '.join([str(i) for i in newline]))
        fp.close()

    else: # if we already have some other guests add the newline to others
        newstuff = vstack((oldstuff, newline))
        savetxt(sfname, newstuff,fmt='%i',delimiter=',')

    readservicelist()



















































