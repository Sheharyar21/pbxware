import requests
from requests.auth import _basic_auth_str
import json
import os.path
import sys
import csv
from time import strftime, localtime

import time
import datetime

today_date  = datetime.datetime.now().date()
month = today_date.strftime("%b");
day = today_date.strftime("%d");
year = today_date.strftime("%Y");

date = month + "-" + day + "-" + year



end_date = date

starttime = '00:00:00'
endtime = '23:59:59'

file1 = open(date + ".csv","w",newline='')

writer = csv.writer(file1)


next_page = 1
page = 1
api_key = 'uEuPMLcKKxNMEbcwX7WJLUdY2lhM0M14'
limit = 1000
while next_page == 1:

  url = "http://sip.xinixworld.com/?apikey="+api_key+"&page="+str(page)+"&limit="+str(limit)+"&start="+date+"&end="+end_date+"&endtime="+endtime+"&action=pbxware.cdr.download"
  print(url)
  check = ''
  #files = {'attachments': open('file.extension','rb')}
  headers ={
      'Content-Type': 'multipart/form-data; boundary=--------------------------531818130631649698349478'
    }

  response = requests.request("GET", url, headers=headers)
  
#print(response.text)  

  x = response.text



   

  y = json.loads(x)
  print(y)
  if page == 1:
    headers = y['header']

    
    writer.writerow(headers)
    


    

  
  for i in range(0, len(y['csv'])) :
    pass
    

    
    mytimestamp = datetime.datetime.fromtimestamp( int(y['csv'][i][3]) )  
  
    # using strftime() function to convert  
    y['csv'][i][3] = mytimestamp.strftime( "%Y - %m - %d  %H : %M : %S") 
    row = y['csv'][i]
    
    #print(y['csv'][i]);
    writer.writerow(row)

      

  if y['next_page'] == False:
    next_page =0
  else:
    page = page + 1
    next_page = 1




print(page)
page = page + 1;
url = "http://sip.xinixworld.com/?apikey="+api_key+"&page="+str(page)+"&limit="+str(limit)+"&start="+date+"&end="+end_date+"&endtime="+endtime+"&action=pbxware.cdr.download"
print(url)
headers ={
      'Content-Type': 'multipart/form-data; boundary=--------------------------531818130631649698349478'
    }

response = requests.request("GET", url, headers=headers)
x = response.text



   

y = json.loads(x)
  #print(y)


    

  
for i in range(0, len(y['csv'])) :
  pass
  

  
  y['csv'][i][3] = strftime('%Y-%m-%d %H:%M:%S', localtime(int(y['csv'][i][3])))
  row = y['csv'][i]
  
  #print(y['csv'][i]);
  writer.writerow(row)



file1.close()
