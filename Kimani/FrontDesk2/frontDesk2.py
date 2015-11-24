# FAITH GROUP PROJECT
# concierge software

import datetime
import time
from numpy import *
import csv
import os
from sys import exit

import warnings

os.system("clear")
set_printoptions(precision=0)
set_printoptions(suppress=1)

dformat = "%a %b %d %H:%M:%S %Y"

dtfun = lambda d: datetime.datetime(*tuple(d)) # give a list and make a datetime object
drfun = lambda m: datetime.timedelta(0, m*60) # give number of minutes and make timedelta


adict = {} # check-in time
bdict = {} # check-out time
sdict = {} # Services dictionary


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
    adict[nbr] = dtfun(start)
    bdict[nbr] = dtfun(end)

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
    
    
    print 'On %s, service ID #%d is open from \n\n'%(date.strftime('%Y-%m-%d'),sid),
    print tic.strftime('%H:%M:%S'), ' to ',
    for sv in lst:
        print sv[0].strftime('%H:%M:%S')
        
        endt = sv[0] + sv[1]
        print endt.strftime('%H:%M:%S'),' to ',
    
    if len(lst) == 0:
        print toc.strftime('%H:%M:%S'), ' * OPEN ALL DAY *'
    else:
        print toc.strftime('%H:%M:%S')




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



# check if there is no other reservation of that service for that day/time
def isReserved(sid, cand,dur):
    ''' Check if anyone else has a reservation of the service ID 
        on the candidate day/time
        sid: service ID number 1 to 10
        cand: candidate date
        dur: duration of the service
    '''
    flag = 0
    if (sid == 1):
        return 0
    else:
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
        bktime, date, and duration are datetime objects, not lists !
    '''
    
    newline = concatenate(([nbr,sid],list(bktime.timetuple())[:5], \
                            list(date.timetuple())[:5], [duration.days, \
                            duration.seconds]))

    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=UserWarning, append=1)
        oldstuff = genfromtxt(sfname, delimiter=',') # array with old services

    # save new list of guests.
    if len(oldstuff) == 0: # if this is the first guest write it this way
        fp = open(sfname, 'w')
        fp.write(', '.join([str(i) for i in newline]))
        fp.close()
        sdict[nbr].append([nbr,sid,bktime,date, duration])

    else: # if we already have some other guests add the newline to others
        newstuff = vstack((oldstuff, newline))
        savetxt(sfname, newstuff,fmt='%i',delimiter=',')
        sdict[nbr].append([nbr,sid,bktime,date, duration])




def checkout(nbr):
    ''' Given a client ID, check him/her out i.e
        Delete the ID from guestlist and the dictionary
    '''

    if nbr not in adict.keys():
        print 'There is no guest with that ID'
        return

    else:
        if len(adict) == 1:
            savetxt(gfname, array([]))
        else:
            garray = genfromtxt(gfname, delimiter = ',')

            for j in range(shape(garray)[0]):
                if garray[j,0] == nbr:
                    del adict[garray[j,0]]
                    del bdict[garray[j,0]]
                    garray = delete(garray,j,0)
                    savetxt(gfname,garray,fmt='%i', delimiter=',')
                    return





def cancelRes(nbr, serviceindex, canceltime):
    '''
        Given the index of a service (would have to list the services for
        that client first), and a cancel time determine if it's ok to
        cancel within 10mins of booking or before 90mins to service
        time
    '''

    Cserv = sdict[nbr][serviceindex-1]
    Csid = Cserv[0]
    Cbktime = Cserv[1]
    Cstime = Cserv[2]
    Cdur = Cserv[3]
    
    aftbook = (canceltime - Cbktime).seconds/60
    bfservtime = (Cstime - canceltime).seconds/60
    
    if (aftbook <= 10) or (bfservtime >= 90):
        del sdict[nbr][serviceindex]
        sarray = genfromtxt(sfname, delimiter=',')

        for j in range(shape(sarray)[0]):
            gid = int(sarray[j][0])
            servid = int(sarray[j][1])
            bookingtime = dtfun([int(i) for i in sarray[j][2:7]])
            start = dtfun([int(i) for i in sarray[j][7:12]])
            dur = drfun(int(sarray[j][-1])/60)

            if ((gid == nbr) and (servid == Csid) and \
               (bookingtime == Cbktime) and (start == Cstime) and \
               (dur == Cdur)):
                sarray = delete(sarray,j,0)
                savetxt(sfname,sarray,fmt='%i', delimiter=',')
                print 'Service has been successfully cancelled'
                return

    else:
        print 'Sorry, you\'re no no longer allowed to cancel this reservation'




# RETURN WHAT SERVICES A GUEST CAN HAVE AT A GIVEN TIME & DURATION
def suggestions(date, dur):
    '''
    '''
    
    print 'The Following services are available: ',
    for sid in range(1,11):
        if (isReserved(sid,date,dur) == 0):
            print sid,

    



    



# main algorithm

#print 'Hello, Welcome to MiYe'
readguestlist()
readservicelist()
print 'We currently have %d guests'%len(adict)


kwd = ['checkin','q', 'guestlist', 'checkout','gservlst','savail','h', \
       'mkres', 'cres','suggs']

inp = raw_input('Enter a command: ').lower()




while (inp != 'q'):
    try:
        
        if inp not in kwd:
            print 'Invalid input. Please enter one of the correct inputs'

        elif (inp == 'h'):
            print kwd

        
        # LIST ALL GUESTS STAY
        elif (inp == 'guestlist'):
            for i in adict.keys():
                stay(i)


        # CHECK-IN CASE
        elif (inp == 'checkin'):
            print 'Checking in a new guest ...'
            
            gid = input('Enter a guest ID: ')

            while gid in adict.keys():
                print 'There\'s already a guest with this ID'
                gid = input('Enter a guest ID: ')
            
            ayr,amt,aday,ahr,amn = input('Enter the check-in date and time (yyyy,mm,dd,hh,min): ')
            byr,bmt,bday,bhr,bmn = input('Enter the check-out date and time (yyyy,mm,dd,hh,min): ')
            adate = [ayr,amt,aday,ahr,amn]
            bdate = [byr,bmt,bday,bhr,bmn]
            checkin(gid,adate, bdate)
            print 'Guest %i has been checked in'%gid

        # CHECK-OUT CASE
        elif (inp == 'checkout'):
            print 'Checking out a guest ...'
            gid = input('Enter a guest ID: ')
            while gid not in adict.keys():
                print 'There is no guest with that ID'
                gid = input('Enter an ID: ')
                
            checkout(gid)
            print 'Guest %i has been checked out'%gid


        # LIST SERVICES OF A CLIENT 
        elif (inp == 'gservlst'):
            print 'Listing all the services of a guest ...'  
            gid = input('Enter a guest ID: ')
            while gid not in adict.keys():
                print 'There is no guest with that ID'
                gid = input('Enter an ID: ')

            getServices(gid)
        
        # LIST AVAILABILITY OF A SERVICE ON A GIVEN DAY
        elif (inp == 'savail'):
            print 'Listing service availability ...'
            sid = input('Enter service ID: ')
            yr,mt,day,hr,mn = input('Enter date (yyyy,mm,dd,hh,min): ')
            date = datetime.datetime(yr,mt,day,hr,mn)

            availtimes(sid,date)


        # MAKE A RESERVATION
        elif (inp == 'mkres'):
            print 'Making a service reservation ...'
            gid = input('Enter a guest ID: ')
            while gid not in adict.keys():
                print 'There is no guest with that ID'
                gid = input('Enter an ID: ')

            sid = input('Enter a service ID (1-10): ')
            bkyr,bkmt,bkday,bkhr,bkmn = input('Enter booking day & time (yyyy,mm,dd,hh,min): ')
            dyr,dmt,dday,dhr,dmn = input('Enter service date & time (yyyy,mm,dd,hh,min): ')
            duration = input('Enter service duration (in mins): ')

            bk_dtime = datetime.datetime(bkyr,bkmt,bkday,bkhr,bkmn)
            d_dtime = datetime.datetime(dyr,dmt,dday,dhr,dmn)
            duration = datetime.timedelta(0,duration*60)

            makeReservation(gid, sid, bk_dtime, d_dtime, duration)
            
            print 'Reservation has been made.'


        # CANCEL A RESERVATION
        elif (inp == 'cres'):
            print 'Cancelling a reservation ...'
            
            gid = input('Enter a guest ID: ')
            servInd = input('Enter service index: ')

            yr,mt,day,hr,mn = input('Enter cancelling day & time (yyyy,mm,dd,hh,min): ')
            cctime = dtfun([yr, mt, day, hr, mn])

            cancelRes(gid, servInd, cctime)

        

        # ASKING FOR SUGGESTIONS
        
        elif (inp == 'suggs'):
            print 'Looking for suggestions ...'
            
            yr,mt,day,hr,mn = input('Enter convenient day & time (yyyy,mm,dd,hh,min): ')
            durmin = input('Enter duration (mins): ')
            
            date = dtfun([yr,mt,day,hr,mn])
            dur = drfun(durmin)
            
            suggestions(date, dur)





        inp = raw_input('Enter a command: ')
    except KeyboardInterrupt:
        exit(0)

        




    
        












































