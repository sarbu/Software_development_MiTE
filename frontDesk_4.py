# GROUP PROJECT
# MiYE software

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
dayfun = lambda x: datetime.timedelta(x,0) # give a number of days and create a timedelta object

adict = {} # dictionary of check-in dates
bdict = {} # dictionary of check-out dates
sdict = {} # dictionary of services


# adict and bdict ressemble the following dictionary
# the keys are the guest id and the value is a datetime object
# see https://docs.python.org/2/library/datetime.html
# adict: {1: datetime.datetime(2015, 11, 20, 19, 0),
#         2: datetime.datetime(2015, 11, 19, 18, 0),
#         3: datetime.datetime(2015, 11, 20, 13, 30)}

# sdict looks like
# {1: [[3, datetime.datetime(2015, 11, 20, 19, 0), datetime.datetime(2015, 11, 21, 9, 0), datetime.timedelta(0, 1800)],
#       [5, datetime.datetime(2015, 11, 20, 20, 0), datetime.datetime(2015, 11, 21, 11, 0), datetime.timedelta(0, 1800)]],
#  2: [[4, datetime.datetime(2015, 11, 20, 12, 0), datetime.datetime(2015, 11, 21, 13, 0), datetime.timedelta(0, 3600)]],
#  3: [[7, datetime.datetime(2015, 11, 20, 19, 0), datetime.datetime(2015, 11, 22, 19, 0), datetime.timedelta(0, 1800)],
#      [5, datetime.datetime(2015, 11, 20, 19, 0), datetime.datetime(2015, 11, 24, 16, 0), datetime.timedelta(0, 1800)]]}

# Once again the keys are the guest ID, and the values are a LIST of
# services. A 'service' consist of
# [serviceid, bookingtime, serviceTime, duration]




# dictionary of prices
pricedict = {1:2.5,2:3.0,3:3.0,4:3.0,5:2.0,6:2.0,7:3.5,8:3.5,9:3.5,10:3.5}

#dictionary of full name services
spaservices = {1:"Mineral bath| 60 or 90 mins| at $2.50/min",2:"Swedish massage| 30 or 60 mins| at $3.00/min",3:"Shiatsu massage| 30 or 60 mins| at $3.00/min",4:"Deep tissue massage| 30 or 60 mins| at $3.00/min",5:"Normal facial| 30 or 60 mins| at $2.00/min",\
6:"Collagen facial| 30 or 60 mins| at $2.00/min",7:"Hot stone ST| 60 or 90 mins| at $3.50/min",8:"Sugar scrub ST| 60 or 90 mins| at $3.50/min",9:"Herbal body Wrap ST| 60 or 90 mins| at $3.50/min",10:"Botanical mud wrap ST| 60 or 90 mins| at $3.50/min"}

servicenamedict = {
        1:"Mineral bath",
        2:"Swedish massage",
        3:"Shiatsu massage",
        4:"Deep tissue massage",
        5:"Normal facial",
        6:"Collagen facial",
        7:"Hot stone special treatment",
        8:"Sugar scub special treatment",
        9:"Herbal body wrap special treatment",
        10:"Botanical mud wrap special treatment",
        }

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
    
    # create the line to add to the file guestlist.csv and save it    
    newline = concatenate(([nbr],start, end))   # new line

    # open guestlist.csv and remove 'empty file' warning
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=UserWarning, append=1)
        oldstuff = genfromtxt(gfname, delimiter=',') # array with old clients
    
    # save newline to guestlist.
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
    ## this is trouble is you're talking about 2015/11/12 and 2016/11/12
    # if you intend to deal with that case, then just add
    # the following:     and (d1.year == d2.year)
    # to the flag line
    flag = ((d1.month == d2.month) and (d1.day == d2.day))
    return flag




# function to return the times when a service is available
def availtimes(sid,date):
    ''' sid = service ID
        date = datetime object
    '''
    
    if sid > 1: # for services 2-10: check availability
        lst = []
        for cid in sdict.keys():
            slst = sdict[cid]
            for serv in slst:
                if isSameDay(serv[2],date) and (sid == serv[0]):
                    lst.append(serv[2:])    
        lst = sorted(lst)
    else: # service #1 is mineral baths, which is always available and more than one person can take one at the same time
        lst = []

    # datetime object representing 8am and 8pm.
    tic = datetime.datetime(*(date.year,date.month,date.day,8,0))
    toc = datetime.datetime(*(date.year,date.month,date.day,20,0))
    

    # loop through all the services with sid and print the
    # times in between appointments
    print 'On %s, service ID #%d is open from \n'%(date.strftime('%Y-%m-%d'),sid),
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

    # all the credit of this function go to stackoverflow.com ;-)
    # http://stackoverflow.com/questions/325933/determine-whether-two-date-ranges-overlap
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

                    if ((tic < cand+dur) and (toc > cand)):
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
        sdict[nbr] = [[sid,bktime,date, duration]]

    else: # if we already have some other guests add the newline to others
        newstuff = vstack((oldstuff, newline))
        savetxt(sfname, newstuff,fmt='%i',delimiter=',')
        
        if nbr not in sdict.keys(): # if this is a client 1st reservation
            sdict[nbr] = [[sid,bktime,date, duration]]
        else:
            sdict[nbr].append([sid,bktime,date, duration])
            

def checkout(nbr):
    ''' Given a client ID, check him/her out i.e
        Delete the ID from guestlist and the dictionary
    '''

    
 
    if len(adict) == 1: # if this is the only client,
        savetxt(gfname, array([])) # save an empty matrix in guestlist.csv

    else: # if this is one of many clients, delete row from a matrix of guests
        garray = genfromtxt(gfname, delimiter = ',')
        ind = [j for j in range(shape(garray)[0]) if garray[j][0] == nbr]
        garray = delete(garray,ind,0)
        savetxt(gfname,garray,fmt='%i', delimiter=',')


    # if this guest had any services, delete them from servicelist.csv
    if nbr in sdict.keys():
        sarray = genfromtxt(sfname, delimiter=',')
        ind = [j for j in range(shape(sarray)[0]) if sarray[j][0] == nbr]
        sarray = delete(sarray,ind,0)
        savetxt(sfname,sarray,fmt='%i', delimiter=',')
        del sdict[nbr]

    # del entries from dictionaries
    del adict[nbr]
    del bdict[nbr]





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
        del sdict[nbr][serviceindex-1]
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
        print 'Sorry, you\'re no longer allowed to cancel this reservation'


def getBookingTime(nbr, serviceindex):
    ''' Given the guest ID, nbr, and the index of the service, meaning
        if it's the first/second that the guest has booked, NOT
        THE SAME AS THE SERVICE ID NUMBER (1-10)
    '''

    serv = sdict[nbr][serviceindex-1]
    print 'THE %iTH SERVICE OF GUEST %i WAS BOOKED at %s'%(serviceindex,\
                                                           nbr, \
                                                           serv[1].ctime())


# RETURN WHAT SERVICES THE GUEST CAN HAVE AT A GIVEN TIME & DURATION
def suggestions(date, dur):
    '''Given date and time, figure out what services are available in 30 or 60 minutes
    '''
    
    print '\nThe Following services are available:\n' # \n(*Mineral Bath is always available)\n,
    print '+'+'-' * 70+'+'
    for sid in {2,3,4,5,6}:
        if (isReserved(sid,date,dur) == 0): # if a service is notReserved then it is available..
            print servicenamedict[sid]
    print servicenamedict[1]  
    print '+'+'-' * 70+'+'

def suggestions1(date, dur):
    '''Given date and time, figure out what services are available in 60 or 90 minutes
    '''
    
    print '\nThe Following services are available:\n'
    print '+'+'-' * 70+'+'
    for sid in {7,8,9}:
        if (isReserved(sid,date,dur) == 0): # if a service is notReserved then it is available..
            print servicenamedict[sid]  
    print servicenamedict[1]
    print '+'+'-' * 70+'+'   


def getBill(nbr):
    ''' Given a guest id, nbr, get the bill of all the services.
    '''
    
    servlst = sdict[nbr]
    total = 0

    # loop through the services of a client and add up the $$ for each
    for serv in servlst:
        unitprice = pricedict[serv[0]] # get the unit price of a service from the pricedict.Pricedict defined at beginning of file
        total = total + unitprice * (serv[-1].seconds/60)
    return total




def days_avail(sid, start, end):
    ndays = (end - start).days + 1

    print
    for k in range(ndays):
        day = start + dayfun(k)
        availtimes(sid, day)
        print
        print
    






# Main Menu

print 'Hello, Welcome to MiYe'

# read whatever is in the file. either it's empty: first run
# or there's stuff in it: state from a previous run

readguestlist()
readservicelist()
print 'We currently have %d guests'%len(adict)

# kwd is short for keyword
kwd = ['checkin','q','guestlist', 'checkout','gueststay','gservlist','savail','h', \
       'mkres', 'cres','suggs', 'bktime','servicelist','getbill',\
       'day_avail']

inp = raw_input('ENTER A COMMAND: ').lower()


# q = quit
while (inp != 'q'):
    try: 

        
        if inp not in kwd:
            print 'INVALID INPUT. PLEASE ENTER ONE OF THE RECOGNIZED INPUTS OR ENTER "h" FOR MORE INFORMATION'

        # help
        elif (inp == 'h'):
            print kwd

        
        # LIST ALL GUESTS STAY
        elif (inp == 'guestlist'):
            if len(adict) == 0:
                print 'THERE ARE NO GUESTS'
            else:
                print 'THERE ARE %i GUEST(s)'%len(adict)
                for i in adict.keys():
                    stay(i)
                    
        # LIST DURATION OF GUEST'S STAY
        elif (inp == 'gueststay'):
            gid = input('ENTER A GUEST ID: ')
            stay(gid)
            
        # LIST OF SPA SERVICES
        elif (inp == 'servicelist'):
            print
            for k, v in spaservices.items():
                print k,v
               
                 
        # CHECK-IN CASE
        elif (inp == 'checkin'):
            print 'CHECKING IN A NEW GUEST ...'
            
            gid = input('ENTER A GUEST ID: ')

            while gid in adict.keys():
                print 'THERE\'S ALREADY A GUEST WITH THAT ID'
                gid = input('ENTER A GUEST ID: ')
            
            ayr,amt,aday,ahr,amn = input('ENTER CHECK-IN DATE & TIME (yyyy,mm,dd,hh,min): ')
            byr,bmt,bday,bhr,bmn = input('ENTER CHECK-OUT DATE & TIME (yyyy,mm,dd,hh,min): ') #checkout
            adate = [ayr,amt,aday,ahr,amn]
            bdate = [byr,bmt,bday,bhr,bmn]
            checkin(gid,adate, bdate)
            print 'GUEST #%i HAS BEEN CHECKED IN'%gid

        # CHECK-OUT CASE
        elif (inp == 'checkout'):
            print 'CHECKING-OUT A  GUEST ...'
            gid = input('ENTER A GUEST ID: ')
            while gid not in adict.keys():
                print 'THERE IS NO GUEST WITH THAT ID'
                gid = input('ENTER A GUEST ID: ')
                
            checkout(gid)
            print 'GUEST %i HAS BEEN CHECKED-OUT'%gid


        # LIST SERVICES OF A CLIENT 
        elif (inp == 'gservlist'):
            print 'LISTING ALL THE SERVICES FOR A CLIENT ...'  
            gid = input('ENTER A GUEST ID: ')
            while gid not in adict.keys():
                print 'THERE IS NO GUEST WITH THAT IDs'
                gid = input('ENTER A GUEST ID: ')

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
            if sid in {1,7,8,9,10}:
                print 'The service you have chosen is offered for 60 or 90 minutes'
                while True:
                    duration = input('Enter service duration (in mins): ')
                    if duration not in {60, 90}:
                        print 'Please enter a valid number!'
                        continue
                    else:
                    #the user inputs the correct duration
                    #ready to exit the loop
                        break   
            elif sid in {2,3,4,5,6}:
                print 'The service you have chosen is offered for 30 or 60 minutes'
                while True:
                    duration = input('Enter service duration (in mins): ')
                    if duration not in {30, 60}:
                        print 'Please enter a valid number!'
                        continue
                    else:
                        #the user inputs the correct duration
                        #ready to exit the loop
                        break  
            else:
                print 'There is no service with that ID!'
                while True:
                    sid = input('Enter a service ID (1-10): ')
                    if sid not in {1,2,3,4,5,6,7,8,9,10}:
                        print 'There is no service with that ID!'
                        continue
                    else:
                        #the user inputs the correct duration
                        #ready to exit the loop
                        break  
                    
             
            bkyr,bkmt,bkday,bkhr,bkmn = input('Enter booking day & time (yyyy,mm,dd,hh,min): ')
            dyr,dmt,dday,dhr,dmn = input('Enter service date & time (yyyy,mm,dd,hh,min): ')
            #Call the beyondStay function, once we create it that is :)
            
            
            bk_dtime = datetime.datetime(bkyr,bkmt,bkday,bkhr,bkmn)
            d_dtime = datetime.datetime(dyr,dmt,dday,dhr,dmn)
            duration = datetime.timedelta(0,duration*60)

            makeReservation(gid, sid, bk_dtime, d_dtime, duration)
            
            print 'Reservation has been made.'
            money = getBill(gid)
            print 'Your total charge for service(s) is currently $%4.2f'%(money)


        # CANCEL A RESERVATION
        elif (inp == 'cres'):
            print 'Cancelling a reservation ...'
            gid = input('Enter a guest ID: ')
            while gid not in adict.keys():
                print 'There is no guest with that ID'
                gid = input('ENTER AN ID: ')
 
            servInd = input('ENTER SERVICE INDEX: ')
            #index is number of services, start counting from 1 not 0!

            yr,mt,day,hr,mn = input('Enter cancelling day & time (yyyy,mm,dd,hh,min): ')
            #cancelling is the time of cancellation now
            cctime = dtfun([yr, mt, day, hr, mn])

            cancelRes(gid, servInd, cctime)

        

        # ASKING FOR SUGGESTIONS
        
        elif (inp == 'suggs'):
            print 'Looking for suggestions ...'
            
            yr,mt,day,hr,mn = input('Enter convenient day & time (yyyy,mm,dd,hh,min):')
            while True:
                durmin = input('Enter duration of 30, 60 or 90 (mins):')
                if durmin not in {30, 60, 90}:
                    print 'Please enter 30, 60 or 90 minutes'
                    continue
                else:
                    break
            
            date = dtfun([yr,mt,day,hr,mn])
            dur = drfun(durmin)
            if durmin in {30,60}:
                suggestions(date, dur)
            else:
                suggestions1(date, dur)
            

        # ASKING FOR SOMEONE'S BOOKING TIME
        elif (inp == 'bktime'):
            print 'CHECKING BOOKING TIME OF A SERVICE ...'
            gid = input('ENTER A GUEST ID: ')
            while gid not in adict.keys():
                print 'THERE IS NO GUEST WITH THAT ID'
                gid = input('ENTER A GUEST ID: ')

            sindex = input('ENTER SERVICE INDEX: ')
            getBookingTime(gid,sindex)

        # GETTING SOMEONE'S BILL
        elif (inp == 'getbill'):
            print 'FETCHING THE BILL OF A CLIENT ...'
            gid = input('ENTER A GUEST ID: ')
            while gid not in adict.keys():
                print 'THERE IS NO GUEST WITH THAT ID'
                gid = input('ENTER A GUEST ID: ')

            money = getBill(gid)
            print 'GUEST ID #%i owes $%4.2f'%(gid,money)



        elif (inp == 'day_avail'):
            print 'CHECKING SERVICE DAY AVAILABILITY'
            sid = input('ENTER SERVICE INDEX: ')
            yr_a,mt_a,day_a = input('ENTER START DAY (yyyy,mm,dd): ')
            yr_b,mt_b,day_b = input('ENTER END DAY (yyyy,mm,dd): ')

            start_day = dtfun([yr_a, mt_a, day_a])
            end_day = dtfun([yr_b, mt_b, day_b])
            days_avail(sid, start_day, end_day)

        
        print
        print
        inp = raw_input('ENTER A COMMAND: ').lower()
    except KeyboardInterrupt:
        exit(0)

        
