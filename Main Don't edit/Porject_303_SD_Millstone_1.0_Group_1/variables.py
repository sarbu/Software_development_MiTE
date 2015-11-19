#!/usr/bin/python3
# variables.py by Bill Weinman [http://bw.org/]
# This is an exercise file from Python 3 Essential Training on lynda.com
# Copyright 2010 The BearHeart Group, LLC
import os


class Menu:
    def Home(self,option=''):
        print('                      ╔============================================================╗') 
        print('                               well come to the Millstone 1.0 of 303_SD_Project')
        print('                      ╚============================================================╝') 
        print('                      ╔============================================================╗') 
        print('                                 Choose One from the list of Options below',)
        print('                       1: Services' )
        print('                       2: Reservations') 
        print('                       3: Cancelation') 
        print('                       4: Billing')
        print('                       0: quit program ')
        print('                      ╚============================================================╝')
       #os.system('\n*100')    
    def Services(self,option1=''):
        #os.system('\n*100')
        print('                      ╔============================================================╗') 
        print('                            well come to the Millstone 1.0 of 303_SD_Project')
        print('                      ╚============================================================╝') 
        print('                      ╔============================================================╗') 
        print('                                Choose One from the list of Options below',)

        print('                       a: Show Services') 
        print('                       b: Search for Services')
        print('                       c: Update Services ')
        print('                      ╚============================================================╝')
    def Show_Services(self,option2=''):
        ft=open('services.csv')
        for line in ft:
            print((line.split(",")[0]).ljust(5) ,(line.split(",")[1]).ljust(20),\
            (line.split(",")[2]).ljust(15), line.split(",")[4].ljust(15), line.\
            split(",")[5].ljust(15),line.split(",")[6].ljust(15))
          
            #main()
    def Reservation(self,option3=''):
        ft=open('Guests.csv')
        check =False
        for line in ft:
            if line.split(",")[0]== option3:
                check=True
                print('        ╔================================================================================╗')
                print('        ║'+(line.split(",")[0]).ljust(5)+'║' ,(line.split(",")[1]).ljust(20)+'║',(line.split(",")[2]).ljust(15)+'║', line.split(",")[3].ljust(15)+'║', line.split(",")[4].ljust(20))
                print('        ╚================================================================================╝')
          
        print(check)                 
        if check ==False:
            print('                      ╔============================================================╗') 
            print('                         The Guest Id has been entered is not existed, try again')
            print('                      ╚============================================================╝')
            main()
                
                
       
 
def main():
    
    os.system('cls')
    user_int = Menu()
    user_int.Home()
    option=input('Enter your choice from the Menu:')
    if option == '1':
       user_int.Services()
       option1=input('Enter your choice from the Menu:')
       if option1=='a':
           user_int.Show_Services()
       else:
           main()
    elif  option =='2':
        user_int.Reservation(input('Enter Guest ID::'))                  
                                                                
    else:
        main()
      
   



if __name__ == "__main__": main()
