#!/usr/bin/env python
# coding: utf-8

# In[106]:


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


scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']


# In[87]:


creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

client = gspread.authorize(creds)


# In[88]:


#def rotateMotor():
#    ch = bytes("R", 'utf-8')
#    ser.write(ch)


# In[89]:


#schedule.every(3).hours.do(rotateMotor())


# In[ ]:


if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout = 1)
    ser.flush()
        
    while True:
    
        #schedule.run_pending()
        latestDate = time.strftime("%d/%m/%y")
    
        if ser.in_waiting > 0:
                
            line = ser.readline().decode('utf-8').rstrip()        
            
            if(len(line) > 0):             
                while True:          
                    try:
                        sheet = client.open("IoT Data Sheet").worksheet(latestDate)
                        print("Loaded sheet: "+ latestDate)
                        break
                    except WorksheetNotFound:
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
                    
                #for ii in sheet:
                
                curr_time = time.localtime()
                time_str = time.strftime("%m/%d/%Y %H:%M:%S",curr_time)

                currentUsedDate = time.strftime("%d/%m/%Y", curr_time)
                sheet.append_row([time_str, line])
                print("["+time_str+"] "+line)

                time.sleep(0.08)
                
        elif ser.in_waiting > 1:        
            
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

                time.sleep(0.17)
            


# In[ ]:




