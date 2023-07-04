#THIS SOURCE CODE IS MADE FOR THE FOLLOWING COURSE:
#
#  COURSE NAME    : INTERNET OF THINGS (ITT569)
# INSTITUTION    : UNIVERSITI TEKNOLOGI MARA CAWANGAN TERENGGANU KAMPUS KUALA TERENGGANU
# PROGRAME       : BACHELORS OF COMPUTER SCIENCE (HONS.) MOBILE COMPUTING
# GROUP          : CS2706B (MARCH - AUGUST 2023)
# PROJECT        : EGGSPERT CHICKEN INCUBATOR (ECI)
# GROUP MEMBERS  :
  
#   MUHAMAD RAHMAT BIN MUSTAFA          2021858398
#   MUHAMAD DANISH FAZWAN BIN ROSOLIZA  2020490082
#   ISMAH HADIRAH BINTI MD ISA          2020476688
#   MIRZA AFRINA BINTI YUSOF            2020872682
#   NURUL ANNISA BINTI ADAM             2021868368


#!/usr/bin/env python
# coding: utf-8

# In[106]:

#importing the needed external libraries
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
import schedule
from time import strftime
from gspread.exceptions import SpreadsheetNotFound
from gspread.exceptions import WorksheetNotFound
import serial
import sys


# In[86]:

#initializes the type of api to be used, which are GoogleSheet and GoogleDrive API
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']


# In[87]:

#loads the 'creds.json' which contains the authorization over the project's in Google Services
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

#invokes gspread functions from the imported library to attempt authorization using the creds variable
client = gspread.authorize(creds)


# In[89]:


#schedule.every(3).hours.do(rotateMotor())


# In[ ]:


if __name__ == '__main__':
    #aims at the port the Arduino is connected at
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout = 1)
    ser.flush()

    #exploit an infinite loop to ensure continuous data tramission to the cloud
    while True:
    
        #schedule.run_pending()
        latestDate = time.strftime("%d/%m/%y")

        #checks whether there is a serial line from the Arduino
        if ser.in_waiting > 0:
            #reads the line
            line = ser.readline().decode('utf-8').rstrip()        
            #check whether the line is not null 
            if(len(line) > 0):   
                #exploits infinite loop to continuously attempt to open the GoogleSheet
                while True:
                    #the try-clause attempts to load the worksheet named IoT Data Sheet,
                    #and opening a sheet within that which is named the current date
                    try:
                        sheet = client.open("IoT Data Sheet").worksheet(latestDate)
                        print("Loaded sheet: "+ latestDate)
                        #when the opertaions above succeed, the loop is broken since
                        #the connection is now established with the correct sheet
                        break
                    except WorksheetNotFound:
                        #when the error thrown is worksheet not found, it means that
                        #a new day has commenced. hence, rspi create a new one named
                        #as current date
                        sheet = client.open("IoT Data Sheet")
                        sheet.add_worksheet(title=latestDate, rows=5000, cols=20)
                        sheet = client.open("IoT Data Sheet").worksheet(latestDate)
                        sheet.append_row(["datetime", "data", "extra"])
                        print("Created sheet: "+ latestDate)
                        break
                    except APIError as aE:
                        print("API error, retrying in 10 seconds...")
                        errorSheet = client.open("IoT Data Sheet").worksheet("ERROR LOG")
                        print("Loaded error log sheet")
                        curr_time = time.localtime()
                        time_str = time.strftime("%m/%d/%Y %H:%M:%S",curr_time)
                        errorMsg = repr(aE);
                        errorSheet.append_row([time_str, "Exception caught: "+errorMsg])
                        time.sleep(0.17)
                    except KeyboardInterrupt as kI:
                        print("Keyboard interrupt raised! Program exiting...")
                        errorSheet = client.open("IoT Data Sheet").worksheet("ERROR LOG")
                        print("Loaded error log sheet")
                        curr_time = time.localtime()
                        time_str = time.strftime("%m/%d/%Y %H:%M:%S",curr_time)
                        errorMsg = repr(kI);
                        errorSheet.append_row([time_str, "Keyboard interrupt, program exited: "+errorMsg])
                        sys.exit(1)
                    except Exception as e:
                        self.exc_info = sys.exc_info()
                        errorSheet = client.open("IoT Data Sheet").worksheet("ERROR LOG")
                        print("Loaded error log sheet")
                        curr_time = time.localtime()
                        time_str = time.strftime("%m/%d/%Y %H:%M:%S",curr_time)
                        errorMsg = repr(e);
                        errorSheet.append_row([time_str, "Other exception caught, program retrying: "+errorMsg])

                #gets the latest system datetime
                curr_time = time.localtime()
                time_str = time.strftime("%m/%d/%Y %H:%M:%S",curr_time)

                currentUsedDate = time.strftime("%d/%m/%Y", curr_time)
                sheet.append_row([time_str, line])
                #append the serial read onto the worksheet in a new row, in their own columns
                print("["+time_str+"] "+line)

                time.sleep(0.08)
                
        elif ser.in_waiting > 1:
            #this elif-clause handles the case of multiple serial lines in waiting from the Arduino
            #using the same concept as the if-clause only with additional output to the worksheet
            
            line = ser.readline().decode('utf-8').rstrip()
            line2 = ser.readline().decode('utf-8').rstrip() 
            
            if(len(line) > 0 and len(line2) > 0):
                
                while True:
                    try:
                        sheet = client.open("IoT Data Sheet").worksheet(latestDate)
                        print("Loaded sheet: "+ latestDate)
                        break
                    except WorksheetNotFound:
                        sheet = client.open("IoT Data Sheet")
                        sheet.add_worksheet(title=latestDate, rows=10000, cols=20)
                        sheet = client.open("IoT Data Sheet").worksheet(latestDate)
                        sheet.append_row(["datetime", "data", "extra"])
                        print("Created sheet: "+ latestDate)
                        break
                    except APIError as aE:
                        print("API error, retrying in 10 seconds...")
                        errorSheet = client.open("IoT Data Sheet").worksheet("ERROR LOG")
                        print("Loaded error log sheet")
                        curr_time = time.localtime()
                        time_str = time.strftime("%m/%d/%Y %H:%M:%S",curr_time)
                        errorMsg = repr(aE);
                        errorSheet.append_row([time_str, "Exception caught: "+errorMsg])
                    except KeyboardInterrupt as kI:
                        print("Keyboard interrupt raised! Program exiting...")
                        errorSheet = client.open("IoT Data Sheet").worksheet("ERROR LOG")
                        print("Loaded error log sheet")
                        curr_time = time.localtime()
                        time_str = time.strftime("%m/%d/%Y %H:%M:%S",curr_time)
                        errorMsg = repr(kI);
                        errorSheet.append_row([time_str, "Keyboard interrupt, program exited: "+errorMsg])
                        sys.exit(1)
                    except Exception as e:
                        self.exc_info = sys.exc_info()
                        errorSheet = client.open("IoT Data Sheet").worksheet("ERROR LOG")
                        print("Loaded error log sheet")
                        curr_time = time.localtime()
                        time_str = time.strftime("%m/%d/%Y %H:%M:%S",curr_time)
                        errorMsg = repr(e);
                        errorSheet.append_row([time_str, "Other exception caught, program retrying: "+errorMsg])
                        
                        
                #for ii in sheet:
                curr_time = time.localtime()
                time_str = time.strftime("%m/%d/%Y %H:%M:%S",curr_time)

                sheet.append_row([time_str, line, line2])
                print("["+time_str+"] "+line+", "+line2)

                #ensures a 5 second gap between each read/write from/to the Arduino/worksheet
                time.sleep(0.17)
            


# In[ ]:




