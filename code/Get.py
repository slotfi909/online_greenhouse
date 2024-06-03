import requests
from time import sleep
import datetime

URL = r"http://192.168.43.160/"

INTERVAL_MINUTE = 1

 
def get_current_time():
    global INTERVAL_MINUTE
    current_day = str(datetime.date.today())
    temp_time_obj = datetime.datetime.now()
    current_time = str(temp_time_obj.hour) + "_" + str(temp_time_obj.minute - temp_time_obj.minute % INTERVAL_MINUTE)
    final_string = current_day + "_" + current_time
    return final_string  

def get_command():
    
    command = ""
    file_name = r"..\data\command\water.txt"
    with open(file_name,'r') as file:
        command = file.readline()
    
    return command
        

while True:
    response = requests.get(URL)
    response = response.text.split('\n')
    
    
    temperature = response[0]
    moisture = response[1]

    file_name = get_current_time()

    temperature_file_path =  r"..\data\temperature\{file_name}.txt".format(file_name=file_name) 
    moisture_file_path = r"..\data\moisture\{file_name}.txt".format(file_name=file_name) 
    
    with open(temperature_file_path,'w') as temperature_file:
        temperature_file.write(temperature)
        
    with open(moisture_file_path,'w') as moisture_file:
        moisture_file.write(moisture)
    
    command = get_command()
    try:
        res = requests.post(URL+"post",command)
    except:
        print(f"Repair connection")
    
    sleep(3) #second
    